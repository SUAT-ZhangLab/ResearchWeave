"""Project-added Docker sandbox for ERA; this is not Google upstream code.

Generated code runs only inside the configured Docker image through Docker CLI or WSL. The
constructor timeout is a maximum; an individual run can request a shorter one.
No host execution path, host bind mounts, or model/API calls are provided.
"""

from __future__ import annotations

import json
import math
import os
import shutil
import re
import subprocess
import threading
import time
import uuid
from typing import Any


_BOOTSTRAP = r'''
import contextlib
import json
import resource
import sys

# Bound regular files created by candidate code; /tmp also has a Docker quota.
resource.setrlimit(resource.RLIMIT_FSIZE, (1048576, 1048576))
output = sys.stdout
try:
    request = json.load(sys.stdin)
    with contextlib.redirect_stdout(sys.stderr):
        namespace = {"__name__": "__era_candidate__"}
        exec(compile(request["program"], "<era-candidate>", "exec"), namespace)
        function = namespace[request["function"]]
        if not callable(function):
            raise TypeError("Candidate entry point is not callable")
        result = function(request["input"])

        def json_default(value):
            import numpy as np
            if isinstance(value, np.ndarray):
                return value.tolist()
            if isinstance(value, np.generic):
                return value.item()
            raise TypeError("Unsupported result type")

        response = json.dumps(
            {"success": True, "result": result},
            default=json_default,
            allow_nan=False,
            ensure_ascii=True,
        )
        if len(response) > 1048576:
            raise ValueError("Result is too large")
except BaseException:
    # Do not send candidate exceptions, environment values, or tracebacks back.
    response = '{"success": false, "error": "candidate_failed"}'
output.write(response + "\n")
output.flush()
'''


class DockerSandbox:
    """ERA-compatible runner using an isolated, disposable Docker container.

    ``last_error`` contains a fixed diagnostic code, never captured tool output.
    JSON-compatible inputs are preserved; strings remain strings. NumPy arrays
    and scalars in results are converted to JSON lists and Python scalars.
    """

    max_input_bytes = 8 * 1024 * 1024
    max_output_bytes = 1024 * 1024 + 1

    def __init__(
        self,
        timeout_seconds: float = 60,
        image: str = "zhangluo-runner:0.1.0",
        distribution: str = "Ubuntu-22.04",
    ) -> None:
        self.timeout_seconds = self._timeout(timeout_seconds)
        if not isinstance(image, str) or not re.fullmatch(
            r"[A-Za-z0-9][A-Za-z0-9._/:@-]*", image
        ):
            raise ValueError("Invalid Docker image name")
        if not isinstance(distribution, str) or not distribution or "\x00" in distribution:
            raise ValueError("Invalid WSL distribution name")
        self.image = image
        self.distribution = os.environ.get("ZHANGLUO_WSL_DISTRO", distribution)
        self.last_error: str | None = None

    @staticmethod
    def _timeout(value: float) -> float:
        seconds = float(value)
        if not math.isfinite(seconds) or seconds <= 0:
            raise ValueError("timeout_seconds must be finite and positive")
        return seconds

    def _command(self, docker_arguments: list[str]) -> list[str]:
        mode = os.environ.get("ZHANGLUO_DOCKER_MODE", "auto")
        if mode not in {"auto", "native", "wsl"}:
            raise ValueError("ZHANGLUO_DOCKER_MODE must be auto, native, or wsl")
        if mode == "native" or (mode == "auto" and shutil.which("docker")):
            return ["docker", *docker_arguments]
        if mode == "auto" and os.name != "nt":
            return ["docker", *docker_arguments]
        # Shell code is constant. Docker arguments are positional, not interpolated.
        return [
            "wsl.exe", "-d", self.distribution, "-u", "root", "--cd", "/",
            "--exec", "sh", "-c",
            'systemctl start docker && exec docker "$@"',
            "zhangluo", *docker_arguments,
        ]

    def _remove_container(self, name: str) -> bool:
        try:
            completed = subprocess.run(
                self._command(["rm", "--force", name]),
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=10,
                check=False,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            # Already removed by --rm is also harmless, but Docker does not give
            # a distinct exit code for that case. Keep diagnostics conservative.
            return completed.returncode == 0
        except (OSError, subprocess.SubprocessError):
            return False

    def _execute(
        self, command: list[str], request: bytes, seconds: float
    ) -> tuple[bytes | None, str | None]:
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        chunks: list[bytes] = []
        overflow = threading.Event()
        capture_error = threading.Event()

        def write_input() -> None:
            try:
                assert process.stdin is not None
                process.stdin.write(request)
                process.stdin.close()
            except (OSError, ValueError):
                pass

        def read_output() -> None:
            total = 0
            try:
                assert process.stdout is not None
                while True:
                    chunk = process.stdout.read1(65536)
                    if not chunk:
                        return
                    total += len(chunk)
                    if total > self.max_output_bytes:
                        overflow.set()
                        return
                    chunks.append(chunk)
            except (OSError, ValueError):
                capture_error.set()

        writer = threading.Thread(target=write_input, daemon=True)
        reader = threading.Thread(target=read_output, daemon=True)
        writer.start()
        reader.start()
        deadline = time.monotonic() + seconds
        error = None
        try:
            while process.poll() is None:
                if overflow.is_set():
                    error = "output_limit_exceeded"
                    break
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    error = "timeout"
                    break
                try:
                    process.wait(timeout=min(remaining, 0.05))
                except subprocess.TimeoutExpired:
                    pass
            if error is not None:
                process.kill()
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    pass
            reader.join(timeout=1)
            writer.join(timeout=1)
            if error is not None:
                return None, error
            if overflow.is_set():
                return None, "output_limit_exceeded"
            if reader.is_alive() or capture_error.is_set():
                return None, "output_capture_failed"
            if process.returncode != 0:
                return None, "docker_or_candidate_failed"
            return b"".join(chunks), None
        finally:
            if process.poll() is None:
                process.kill()
            # Never block closing a stream while a pump thread still owns it.
            if not reader.is_alive() and process.stdout is not None:
                process.stdout.close()
            if not writer.is_alive() and process.stdin is not None:
                process.stdin.close()

    def run(
        self,
        program: str,
        function_to_run: str,
        test_input: Any,
        timeout_seconds: float = 60,
    ) -> tuple[Any, bool]:
        """Return ``(function(test_input), True)`` or ``(None, False)``.

        The smaller of the constructor and call timeouts is used. Cleanup may
        take up to ten additional seconds after a failed run.
        """
        self.last_error = None
        try:
            seconds = min(self.timeout_seconds, self._timeout(timeout_seconds))
            if not isinstance(program, str) or not isinstance(function_to_run, str):
                raise ValueError("Program and function name must be strings")
            if not function_to_run.isidentifier():
                raise ValueError("Function name must be an identifier")
            request = json.dumps(
                {"program": program, "function": function_to_run, "input": test_input},
                allow_nan=False,
            ).encode("utf-8")
            if len(request) > self.max_input_bytes:
                self.last_error = "input_limit_exceeded"
                return None, False
        except (TypeError, ValueError, OverflowError, RecursionError):
            self.last_error = "invalid_input"
            return None, False

        name = "zhangluo-runner-" + uuid.uuid4().hex
        command = self._command([
            "run", "--rm", "--pull", "never", "--log-driver", "none", "--interactive", "--name", name,
            "--network", "none", "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges", "--user", "65534:65534",
            "--pids-limit", "128", "--memory", "2g", "--cpus", "2",
            "--tmpfs", "/tmp:rw,nosuid,nodev,size=512m",
            self.image, "python", "-c", _BOOTSTRAP,
        ])
        succeeded = False
        try:
            raw, error = self._execute(command, request, seconds)
            if error is not None:
                self.last_error = error
                return None, False
            response = json.loads(raw)
            if not isinstance(response, dict) or response.get("success") is not True:
                self.last_error = "candidate_failed"
                return None, False
            if "result" not in response:
                self.last_error = "invalid_response"
                return None, False
            succeeded = True
            return response["result"], True
        except (OSError, subprocess.SubprocessError):
            self.last_error = "docker_unavailable"
            return None, False
        except (ValueError, TypeError, UnicodeError, RecursionError):
            self.last_error = "invalid_response"
            return None, False
        finally:
            if not succeeded:
                self._remove_container(name)
