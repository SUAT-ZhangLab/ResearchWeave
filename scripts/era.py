"""Stepwise ERA search for Codex, using upstream FUTS core functions.

Codex writes a candidate between ask and tell; no separate model API is called.
The session contains all data on the same host. Final data are excluded from
ask responses, but are not technically hidden from Codex or the same user.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import sys
from typing import Any
import uuid

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "vendor" / "era" / "implementation"))
import futs
from era_sandbox import DockerSandbox


class SessionError(ValueError):
    """A request cannot be completed with the current session."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _atomic_json(path: Path, value: Any) -> None:
    content = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)
    temporary = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    try:
        with temporary.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(content + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


@contextmanager
def _locked(session: Path, create: bool = False):
    if create:
        session.mkdir(parents=True, exist_ok=True)
    if not session.is_dir():
        raise SessionError("Session directory does not exist.")
    lock = session / ".write.lock"
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise SessionError("Session is busy. If a previous process stopped, confirm it has ended before removing .write.lock.") from exc
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump({"pid": os.getpid(), "created_at": _now()}, handle)
        yield
    finally:
        lock.unlink(missing_ok=True)


def _finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _label(value: Any) -> bool:
    return isinstance(value, (str, bool)) or _finite_number(value)


def _validate_spec(spec: Any) -> dict:
    if not isinstance(spec, dict):
        raise SessionError("Spec must be a JSON object.")
    spec = dict(spec)
    if not isinstance(spec.get("problem"), str) or not spec["problem"].strip():
        raise SessionError("Spec requires a nonempty problem string.")
    spec.setdefault("function", "predict")
    spec.setdefault("metric", "rmse")
    spec.setdefault("iterations", 3)
    spec.setdefault("timeout_seconds", 60)
    if not isinstance(spec["function"], str) or not spec["function"].isidentifier():
        raise SessionError("function must be a Python identifier.")
    if spec["metric"] not in ("rmse", "accuracy"):
        raise SessionError("metric must be rmse or accuracy.")
    if type(spec["iterations"]) is not int or not 1 <= spec["iterations"] <= 20:
        raise SessionError("iterations must be an integer from 1 to 20.")
    if not _finite_number(spec["timeout_seconds"]) or not 0 < spec["timeout_seconds"] <= 3600:
        raise SessionError("timeout_seconds must be positive and at most 3600.")
    for name in ("development", "final"):
        if name == "final" and name not in spec:
            continue
        dataset = spec.get(name)
        if not isinstance(dataset, dict) or "input" not in dataset or "target" not in dataset:
            raise SessionError(f"{name} requires input and target.")
        target = dataset["target"]
        predicate = _finite_number if spec["metric"] == "rmse" else _label
        if not isinstance(target, list) or not target or not all(predicate(x) for x in target):
            raise SessionError(f"{name}.target must be a nonempty list of finite numbers (rmse) or scalar labels (accuracy).")
    try:
        json.dumps(spec, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise SessionError("Spec contains unsupported or nonfinite JSON values.") from exc
    return spec


def _score(predictions: Any, target: list, metric: str) -> tuple[float, float]:
    if not isinstance(predictions, list) or len(predictions) != len(target):
        raise SessionError("prediction_count_or_type_mismatch")
    if metric == "rmse":
        if not all(_finite_number(x) for x in predictions):
            raise SessionError("predictions_must_be_finite_numbers")
        try:
            # hypot avoids squaring overflow for otherwise finite differences.
            value = math.hypot(*(a - b for a, b in zip(predictions, target))) / math.sqrt(len(target))
        except (ArithmeticError, ValueError) as exc:
            raise SessionError("nonfinite_metric") from exc
        if not math.isfinite(value):
            raise SessionError("nonfinite_metric")
        return -value, value
    if not all(_label(x) for x in predictions):
        raise SessionError("predictions_must_be_scalar_labels")
    value = sum(a == b for a, b in zip(predictions, target)) / len(target)
    return value, value


def _evaluate(program: str, spec: dict, dataset: dict) -> dict:
    sandbox = DockerSandbox(timeout_seconds=spec["timeout_seconds"])
    output, success = sandbox.run(program, spec["function"], dataset["input"], spec["timeout_seconds"])
    if not success:
        return {"score": None, "metric_value": None, "error": sandbox.last_error or "candidate_failed", "output": None}
    try:
        score, value = _score(output, dataset["target"], spec["metric"])
        return {"score": score, "metric_value": value, "error": None, "output": output}
    except SessionError as exc:
        return {"score": None, "metric_value": None, "error": str(exc), "output": output}


def _spec_hash(spec: dict) -> str:
    canonical = json.dumps(spec, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _read_spec(session: Path, state: dict) -> dict:
    if not state.get("spec_hash"):
        raise SessionError("Session has no spec_hash; its original scoring specification cannot be verified. Start a new session.")
    spec = _read_json(session / "spec.json")
    try:
        current_hash = _spec_hash(spec)
    except (TypeError, ValueError) as exc:
        raise SessionError("spec.json contains unsupported values after initialization.") from exc
    if current_hash != state["spec_hash"]:
        raise SessionError("spec.json changed after initialization. Restore the original specification or start a new session; existing scores cannot be reused with changed data or scoring rules.")
    return spec


def _read_candidate(session: Path, record: dict) -> str:
    content = (session / record["code"]).read_bytes()
    if not record.get("sha256") or hashlib.sha256(content).hexdigest() != record["sha256"]:
        raise SessionError(f"Saved candidate {record['code']} changed or has no recorded SHA-256. Restore the original file or start a new session; its old score does not apply to modified code.")
    return content.decode("utf-8")


def _state(session: Path) -> dict:
    if not (session / "state.json").is_file():
        raise SessionError("Session is not initialized.")
    state = _read_json(session / "state.json")
    _read_spec(session, state)
    for record in state["candidates"]:
        _read_candidate(session, record)
    return state


def _active(state: dict) -> None:
    if state["phase"] != "active":
        raise SessionError(f"Session phase is {state['phase']}; search is unavailable.")


def _nodes(session: Path, state: dict) -> list:
    return [futs.Node(index=record["index"], parent_index=record["parent_index"],
                      solution=futs.Solution(_read_candidate(session, record)),
                      score=record["score"] if record["score"] is not None else float("-inf"),
                      num_visits=record["num_visits"])
            for record in state["candidates"]]


def _save_candidate(session: Path, index: int, parent: int | None, program: str, evaluation: dict, request_id: str | None) -> dict:
    code_name = f"candidate_{index:03d}.py"
    encoded = program.encode("utf-8")
    (session / code_name).write_bytes(encoded)
    output_name = f"candidate_{index:03d}_output.json"
    _atomic_json(session / output_name, evaluation["output"])
    return {"index": index, "parent_index": parent, "request_id": request_id,
            "code": code_name, "sha256": hashlib.sha256(encoded).hexdigest(),
            "score": evaluation["score"], "metric_value": evaluation["metric_value"],
            "error": evaluation["error"], "output": output_name,
            "num_visits": 0, "created_at": _now()}


def _summary(session: Path, state: dict) -> dict:
    candidates = state["candidates"]
    valid = [x for x in candidates if x["score"] is not None]
    best = max(valid, key=lambda x: x["score"]) if valid else None
    return {"session": str(session.resolve()), "phase": state["phase"],
            "metric": state["metric"], "completed_iterations": max(0, len(candidates) - 1),
            "iterations": state["iterations"], "pending_request": state.get("pending_request"),
            "best": best, "final_evaluation": state.get("final_evaluation"),
            "data_visibility": "All session data are readable by the same user and Codex; final targets are only omitted from ask responses."}


def initialize(session: Path, spec_path: Path, baseline_path: Path) -> dict:
    spec = _validate_spec(_read_json(spec_path))
    program = baseline_path.read_text(encoding="utf-8-sig")
    with _locked(session, create=True):
        if (session / "state.json").exists() or (session / "spec.json").exists():
            raise SessionError("Session already contains a run; choose a new directory.")
        _atomic_json(session / "spec.json", spec)
        state = {"schema_version": 1, "phase": "initializing", "created_at": _now(),
                 "implementation": "Project stepwise adapter using official ERA FUTS core functions",
                 "metric": spec["metric"], "iterations": spec["iterations"],
                 "spec_hash": _spec_hash(spec),
                 "candidates": [], "pending_request": None}
        _atomic_json(session / "state.json", state)
        evaluation = _evaluate(program, spec, spec["development"])
        state["candidates"].append(_save_candidate(session, 0, None, program, evaluation, None))
        state["phase"] = "active" if evaluation["score"] is not None else "initial_failed"
        _atomic_json(session / "state.json", state)
        if evaluation["score"] is None:
            raise SessionError("Baseline failed: " + evaluation["error"] + ". Details saved in session.")
        return _summary(session, state)


def ask(session: Path) -> dict:
    with _locked(session):
        state = _state(session)
        _active(state)
        spec = _read_spec(session, state)
        request = state["pending_request"]
        if request is None:
            if len(state["candidates"]) - 1 >= state["iterations"]:
                raise SessionError("Iteration budget reached; finalize or inspect this session.")
            nodes = _nodes(session, state)
            futs.compute_rank_scores(nodes)
            futs.compute_pucts(nodes, 1.0)
            parent = max(nodes, key=lambda x: x.puct)
            request = {"request_id": uuid.uuid4().hex, "parent_index": parent.index,
                       "iteration": len(state["candidates"]), "created_at": _now()}
            state["pending_request"] = request
            _atomic_json(session / "state.json", state)
        parent = state["candidates"][request["parent_index"]]
        return {**request, "problem": spec["problem"], "function": spec["function"],
                "metric": spec["metric"], "maximize_score": True,
                "parent_code": _read_candidate(session, parent),
                "parent_score": parent["score"], "parent_metric_value": parent["metric_value"],
                "parent_error": parent["error"], "candidate_contract": "Return complete Python defining the named function(input), returning one scalar per target. No network or host files are available."}


def tell(session: Path, candidate_path: Path, request_id: str) -> dict:
    program = candidate_path.read_text(encoding="utf-8-sig")
    with _locked(session):
        state = _state(session)
        _active(state)
        request = state["pending_request"]
        if request is None or request["request_id"] != request_id:
            raise SessionError("Stale or unknown request_id; call ask and use its current request.")
        spec = _read_spec(session, state)
        evaluation = _evaluate(program, spec, spec["development"])
        record = _save_candidate(session, len(state["candidates"]), request["parent_index"], program, evaluation, request_id)
        state["candidates"].append(record)
        nodes = _nodes(session, state)
        futs.backpropagate_visit(nodes, nodes[-1])
        for saved, node in zip(state["candidates"], nodes):
            saved["num_visits"] = node.num_visits
        state["pending_request"] = None
        _atomic_json(session / "state.json", state)
        return {"candidate": record, "summary": _summary(session, state)}


def finalize(session: Path) -> dict:
    with _locked(session):
        state = _state(session)
        if state["phase"] == "finalized":
            return _summary(session, state)
        if state["phase"] == "finalizing":
            raise SessionError("Final evaluation was started previously. It will not be repeated automatically; inspect the saved files.")
        _active(state)
        if state["pending_request"] is not None:
            raise SessionError("A candidate request is pending; complete tell before finalizing.")
        spec = _read_spec(session, state)
        best = max((x for x in state["candidates"] if x["score"] is not None), key=lambda x: x["score"])
        state["phase"] = "finalizing"
        state["selected_best_index"] = best["index"]
        _atomic_json(session / "state.json", state)
        if "final" in spec:
            program = _read_candidate(session, best)
            evaluation = _evaluate(program, spec, spec["final"])
            _atomic_json(session / "final_output.json", evaluation.pop("output"))
            final_result = {"evaluated": True, "dataset": "provided_final", "candidate_index": best["index"],
                            **evaluation, "output": "final_output.json",
                            "note": "Provided final data were evaluated once. Their independence must be established by the research design; they remain accessible on this host."}
        else:
            final_result = {"evaluated": False, "dataset": None, "candidate_index": best["index"],
                            "score": None, "metric_value": None, "error": None,
                            "note": "No final dataset provided; there is no independent final evaluation."}
        state["final_evaluation"] = final_result
        state["phase"] = "finalized"
        state["finalized_at"] = _now()
        _atomic_json(session / "state.json", state)
        return _summary(session, state)


def status(session: Path) -> dict:
    return _summary(session, _state(session))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("init", "ask", "tell", "finalize", "status"):
        command = commands.add_parser(name)
        command.add_argument("--session", required=True, type=Path)
        if name == "init":
            command.add_argument("--spec", required=True, type=Path)
            command.add_argument("--baseline", required=True, type=Path)
        if name == "tell":
            command.add_argument("--candidate", required=True, type=Path)
            command.add_argument("--request-id", required=True)
    arguments = parser.parse_args(argv)
    try:
        if arguments.command == "init":
            result = initialize(arguments.session, arguments.spec, arguments.baseline)
        elif arguments.command == "tell":
            result = tell(arguments.session, arguments.candidate, arguments.request_id)
        else:
            result = {"ask": ask, "finalize": finalize, "status": status}[arguments.command](arguments.session)
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return 0
    except (SessionError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
