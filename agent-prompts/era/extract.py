"""Extract ERA role/task text from a pinned Git commit without running it.
Adapted for ResearchWeave; not an upstream ERA file.
Run: python agent-prompts/era/extract.py
"""
from __future__ import annotations
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path

COMMIT = "b836730b5c000526af95116b1d0e2c60c8cf0a10"
REPOSITORY = "https://github.com/google-research/era"
OUT = Path(__file__).resolve().parent
REPO = OUT.parents[1] / "vendor" / "era"

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def blob(path: str) -> bytes:
    data = (REPO / path).read_bytes()
    manifest = json.loads((OUT / "manifest.json").read_text(encoding="utf-8"))
    expected = manifest["license_file"]["sha256"] if path == "LICENSE" else next(
        item["source_sha256"] for item in manifest["items"] if item["source_file"] == path)
    if digest(data) != expected:
        raise ValueError("Source snapshot does not match its pinned hash: " + path)
    return data

def write_item(filename, text, source, source_bytes, kind, location, **extra):
    relative = "original/" + filename
    data = text.encode("utf-8")
    (OUT / relative).write_bytes(data)
    return {
        "file": relative, "kind": kind, "source_file": source,
        "source_url": f"{REPOSITORY}/blob/{COMMIT}/{source}",
        "source_sha256": digest(source_bytes), "location": location,
        "sha256": digest(data), "encoding": "UTF-8", "license": "Apache-2.0",
        **extra,
    }

def main():
    (OUT / "original").mkdir(parents=True, exist_ok=True)
    items = []
    for source, assignment, name in [
        ("implementation/llm.py", "full_prompt", "01-gemini-role-template.md"),
        ("implementation/playground_s3e1.py", "prompt", "02-program-improvement-template.md"),
    ]:
        raw = blob(source)
        code = raw.decode("utf-8")
        matches = [node for node in ast.walk(ast.parse(code))
            if isinstance(node, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == assignment for t in node.targets)]
        assert len(matches) == 1, (source, assignment, len(matches))
        node = matches[0].value
        assert isinstance(node, ast.JoinedStr)
        literal = ast.get_source_segment(code, node)
        assert literal is not None
        opening = re.match(r'(?i)([fr]*)("""|\'\'\')', literal)
        assert opening is not None
        quote = opening.group(2)
        assert literal.endswith(quote)
        # Retain every source-body character, newline, brace and format spec.
        # Do not evaluate the f-string or convert escape sequences.
        body = literal[opening.end():-len(quote)]
        items.append(write_item(name, body, source, raw, "python_f_string_body",
            {"assignment": assignment, "start_line": node.lineno, "end_line": node.end_lineno},
            source_literal=literal,
            transformation="Removed only the Python string prefix and triple-quote delimiters; placeholders are not evaluated."))
    for source, names in [
        ("implementation/notebooks/single_cell_batch_integration.ipynb",
         ["03-single-cell-overview.md", "04-single-cell-task.md"]),
        ("implementation/notebooks/flu-cornell-jhu-hierarchsir.ipynb",
         ["05-flu-overview.md", "06-flu-task.md"]),
    ]:
        raw = blob(source)
        notebook = json.loads(raw)
        for index, name in enumerate(names):
            cell = notebook["cells"][index]
            assert cell["cell_type"] == "markdown"
            source_text = cell["source"]
            text = "".join(source_text) if isinstance(source_text, list) else source_text
            items.append(write_item(name, text, source, raw, "notebook_task_definition",
                {"cell_index_zero_based": index, "cell_number_one_based": index + 1,
                 "cell_type": "markdown", "cell_id": cell.get("id")},
                transformation="Decoded notebook JSON and concatenated this cell's source strings; cell content is unchanged."))
    license_raw = blob("LICENSE")
    (OUT / "original" / "LICENSE").write_bytes(license_raw)
    manifest = {
        "description": "Published ERA role and task prompts extracted from pinned upstream source; not a reconstruction of an unreleased system.",
        "repository": REPOSITORY, "commit": COMMIT, "extracted_on": "2026-09-15",
        "upstream_license": "Apache-2.0",
        "attribution": "Google Research ERA; Copyright 2026 Google LLC. where present in source headers.",
        "license_file": {"file": "original/LICENSE", "sha256": digest(license_raw)},
        "count": len(items), "items": items,
        "excluded": [
            "Notebook outputs and model-generated candidate programs",
            "Initial baseline programs, execution setup code and score implementation",
            "Notebook cells marked [exclude_from_prompt]",
            "Application papers in era_applications/pdfs (not extracted as software role definitions)"],
        "notes": [
            "The two f-string bodies are unexpanded source templates, not captured API requests.",
            "Notebook task definitions are published task context; the repository does not establish a complete serialized model request for these benchmark notebooks.",
            "The English task text is copied as published, including spelling, notation and scientific claims; extraction does not verify those claims.",
            "roles.md and this extraction script are new explanatory files, not upstream role MD files."]}
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for item in items:
        assert digest((OUT / item["file"]).read_bytes()) == item["sha256"]
    print(f"Extracted and checked {len(items)} prompt/task files from {COMMIT}.")

if __name__ == "__main__":
    main()
