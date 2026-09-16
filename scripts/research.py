"""Small persistent research workspace for the Codex ZhangLuo skill.

Uses immutable JSON records and actual Docker execution. Model decisions and
literature retrieval are performed in the calling Codex conversation.
"""
from __future__ import annotations
import argparse
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import uuid

PROJECT = Path(__file__).resolve().parents[1]
KINDS = {
    "evidence": {"claim": str, "source": str, "evidence_type": str},
    "hypothesis": {"statement": str, "predictions": list, "evidence_ids": list},
    "analysis": {"question": str, "inputs": list, "method": str, "comparison": str,
                 "success_criteria": str, "independent_unit": str, "hypothesis_ids": list},
    "code": {"summary": str},
    "result": {"summary": str, "analysis_id": str},
    "review": {"summary": str, "hypothesis_ids": list},
    "update": {"summary": str, "next_steps": list},
}
EVIDENCE_TYPES = {"literature", "project_measurement", "synthetic", "inference"}


def now():
    return datetime.now(timezone.utc).isoformat()


def read_json(path):
    def invalid(value):
        raise ValueError("Non-finite JSON number: " + value)
    return json.loads(Path(path).read_text(encoding="utf-8-sig"), parse_constant=invalid)


def atomic_json(path, value):
    path = Path(path)
    temp = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    try:
        temp.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


@contextmanager
def study_lock(study):
    path = study / ".writer.lock"
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise ValueError(f"Another operation holds {path}; if interrupted, check its process before removing this file.")
    try:
        with os.fdopen(fd, "w") as stream:
            stream.write(str(os.getpid()))
        yield
    finally:
        path.unlink(missing_ok=True)


def study_path(value):
    study = Path(value).expanduser().resolve()
    meta = read_json(study / "study.json")
    if meta.get("format") != "zhangluo.study.v1":
        raise ValueError("Unsupported study format")
    return study


def records(study):
    return sorted((read_json(p) for p in (study / "records").glob("*.json")), key=lambda r: (r["created_at"], r["id"]))


def nonempty_text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(name + " must be a non-empty string")


def validate(payload, existing):
    if not isinstance(payload, dict):
        raise ValueError("Record must be a JSON object")
    kind = payload.get("kind")
    if kind not in KINDS:
        raise ValueError("Unknown record kind; use " + ", ".join(KINDS))
    content = payload.get("content")
    if not isinstance(content, dict):
        raise ValueError("content must be an object")
    for key, typ in KINDS[kind].items():
        if key not in content or not isinstance(content[key], typ):
            raise ValueError(f"{kind}.content.{key} must be {typ.__name__}")
        if typ is str:
            nonempty_text(content[key], key)
    if kind == "evidence" and content["evidence_type"] not in EVIDENCE_TYPES:
        raise ValueError("evidence_type must be literature, project_measurement, synthetic, or inference")
    if kind == "hypothesis" and not content["predictions"]:
        raise ValueError("Provide at least one testable prediction")
    for name in ("sources", "parent_ids"):
        values = payload.get(name, [])
        if not isinstance(values, list) or any(not isinstance(v, str) or not v.strip() for v in values):
            raise ValueError(name + " must be a list of non-empty strings")
    refs = list(payload.get("parent_ids", []))
    expected_kinds = {"evidence_ids": "evidence", "hypothesis_ids": "hypothesis", "analysis_id": "analysis", "code_id": "code"}
    for key, expected in expected_kinds.items():
        if key not in content:
            continue
        ids = content[key] if key.endswith("_ids") else [content[key]]
        if not isinstance(ids, list) or any(not isinstance(v, str) for v in ids):
            raise ValueError(key + " must contain record IDs")
        for rid in ids:
            if rid not in existing or existing[rid]["kind"] != expected:
                raise ValueError(f"{key} references a missing or wrong-kind record: {rid}")
        refs.extend(ids)
    for rid in refs:
        if rid not in existing:
            raise ValueError("Unknown parent record: " + rid)
    json.dumps(payload, allow_nan=False)


def save_record(study, payload, artifacts=()):
    existing = {r["id"]: r for r in records(study)}
    validate(payload, existing)
    # Read every artifact before mutation; preserve bytes and a hash in the study.
    snapshots = []
    for item in artifacts:
        source = Path(item).resolve(strict=True)
        if not source.is_file():
            raise ValueError("Artifact must be a regular file")
        data = source.read_bytes()
        snapshots.append((source, data, hashlib.sha256(data).hexdigest()))
    rid = payload["kind"] + "-" + uuid.uuid4().hex
    record = {"id": rid, "kind": payload["kind"], "created_at": now(),
              "content": payload["content"], "sources": payload.get("sources", []),
              "parent_ids": payload.get("parent_ids", []), "artifacts": []}
    for number, (source, data, digest) in enumerate(snapshots):
        relative = Path("artifacts") / f"{rid}-{number}{source.suffix}"
        (study / relative).write_bytes(data)
        record["artifacts"].append({"path": relative.as_posix(), "original_path": str(source),
                                    "sha256": digest, "bytes": len(data)})
    atomic_json(study / "records" / (rid + ".json"), record)
    return record


def initialize(args):
    nonempty_text(args.question, "question")
    study = Path(args.study).expanduser().resolve()
    if study.exists() and any(study.iterdir()):
        raise ValueError("Choose a new or empty study directory")
    study.mkdir(parents=True, exist_ok=True)
    with study_lock(study):
        (study / "records").mkdir(exist_ok=True)
        (study / "artifacts").mkdir(exist_ok=True)
        (study / "work").mkdir(exist_ok=True)
        value = {"format": "zhangluo.study.v1", "id": "study-" + uuid.uuid4().hex,
                 "question": args.question, "label": args.label, "created_at": now(),
                 "model_execution": "calling Codex conversation"}
        atomic_json(study / "study.json", value)
    return {"study": str(study), **value}


def record_command(args):
    study = study_path(args.study)
    payload = read_json(args.file)
    with study_lock(study):
        return save_record(study, payload, args.artifact)


def status(args):
    study = study_path(args.study)
    entries = records(study)
    return {"study": str(study), "metadata": read_json(study / "study.json"),
            "counts": dict(Counter(r["kind"] for r in entries)),
            "records": [{"id": r["id"], "kind": r["kind"],
                         "summary": next((r["content"][k] for k in ("summary", "claim", "statement", "question") if k in r["content"]), "")}
                        for r in entries]}


def run(args):
    study = study_path(args.study)
    if not 0 < args.timeout <= 600:
        raise ValueError("timeout must be between 0 and 600 seconds")
    code_path, input_path = Path(args.code).resolve(), Path(args.input).resolve()
    from era_sandbox import DockerSandbox
    with study_lock(study):
        # Save the exact source and input that will be run, before execution.
        code_record = save_record(study, {"kind": "code", "content": {
            "summary": "Codex submitted Python program: " + code_path.name,
            "analysis_id": args.analysis_id, "function": args.function},
            "parent_ids": [args.analysis_id]}, [code_path, input_path])
        program = (study / code_record["artifacts"][0]["path"]).read_text(encoding="utf-8-sig")
        data = read_json(study / code_record["artifacts"][1]["path"])
        sandbox = DockerSandbox(timeout_seconds=args.timeout)
        value, success = sandbox.run(program, args.function, data, args.timeout)
        content = {"summary": "程序执行完成；结果的科学含义仍需结合研究问题解释。" if success else "程序执行失败。",
                   "analysis_id": args.analysis_id, "code_id": code_record["id"],
                   "run_status": "success" if success else "failed", "result": value,
                   "error": sandbox.last_error, "executor": "ERA DockerSandbox", "image": sandbox.image}
        result = save_record(study, {"kind": "result", "content": content,
                                   "parent_ids": [args.analysis_id, code_record["id"]]})
    return {"success": success, "record": result}


def report(args):
    study = study_path(args.study)
    titles = {"evidence": "证据", "hypothesis": "假设", "analysis": "分析安排", "code": "程序", "result": "结果", "review": "评议", "update": "研究更新"}
    with study_lock(study):
        meta = read_json(study / "study.json")
        lines = ["# 科研任务记录", "", meta["question"], "", "数据标记：" + meta["label"], "",
                 "这是已保存记录的汇总；综合解释由 Codex 根据这些记录另写。", ""]
        for entry in records(study):
            lines.extend(["## " + titles[entry["kind"]] + " · " + entry["id"], ""])
            lines.extend(["```json", json.dumps(entry["content"], ensure_ascii=False, indent=2), "```", ""])
            if entry["sources"]:
                lines.extend(["来源：", "", *["- " + s for s in entry["sources"]], ""])
            for artifact in entry["artifacts"]:
                lines.extend([f"- 文件：[{artifact['path']}]({artifact['path']})；SHA256：{artifact['sha256']}", ""])
        destination = study / "record-summary.md"
        destination.write_text("\n".join(lines), encoding="utf-8")
    return {"report": str(destination)}


def doctor(args):
    required = ["scripts/era_sandbox.py", "scripts/era.py", "vendor/era/implementation/futs.py",
                "SKILL.md"]
    result = {"project": str(PROJECT), "python": sys.executable,
              "files": {p: (PROJECT / p).is_file() for p in required},
              "extra_llm_api_key_required": False, "requires_active_agent_session": True}
    if args.container:
        from era_sandbox import DockerSandbox
        runner = DockerSandbox(timeout_seconds=30)
        value, ok = runner.run("def run(x):\n    return {'answer': sum(x)}\n", "run", [2, 3], 30)
        result["container"] = {"success": ok and value == {"answer": 5}, "error": runner.last_error}
    result["success"] = all(result["files"].values()) and result.get("container", {}).get("success", True)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    p = commands.add_parser("init")
    p.add_argument("--study", required=True)
    p.add_argument("--question", required=True)
    p.add_argument("--label", choices=["real", "synthetic"], default="real")
    p.set_defaults(handler=initialize)
    p = commands.add_parser("record")
    p.add_argument("--study", required=True)
    p.add_argument("--file", required=True)
    p.add_argument("--artifact", action="append", default=[])
    p.set_defaults(handler=record_command)
    for name, func in [("status", status), ("report", report)]:
        p = commands.add_parser(name)
        p.add_argument("--study", required=True)
        p.set_defaults(handler=func)
    p = commands.add_parser("run")
    p.add_argument("--study", required=True)
    p.add_argument("--code", required=True)
    p.add_argument("--input", required=True)
    p.add_argument("--function", default="run")
    p.add_argument("--analysis-id", required=True)
    p.add_argument("--timeout", type=float, default=60)
    p.set_defaults(handler=run)
    p = commands.add_parser("doctor")
    p.add_argument("--container", action="store_true")
    p.set_defaults(handler=doctor)
    args = parser.parse_args(argv)
    try:
        result = args.handler(args)
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return 1 if result.get("success") is False else 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({"success": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
