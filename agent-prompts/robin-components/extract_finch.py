"""Extract public Finch prompt strings without importing or executing Finch code."""
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMMIT = "aea66fdf2dd2be827727de50a73cae60dff59972"
BASE = f"https://github.com/Future-House/finch/blob/{COMMIT}/"
source = ROOT / "original/src/fhda/prompts.py"
tree = ast.parse(source.read_text(encoding="utf-8"))
values = {}


def string_value(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.Name) and node.id in values:
        return values[node.id]
    if isinstance(node, ast.JoinedStr):
        parts = []
        for part in node.values:
            if isinstance(part, ast.FormattedValue):
                if part.conversion != -1 or part.format_spec is not None:
                    raise ValueError("Unsupported formatting in source")
                parts.append(string_value(part.value))
            else:
                parts.append(string_value(part))
        return "".join(parts)
    raise ValueError(f"Unsupported AST node: {ast.dump(node)}")


records = []
(ROOT / "prompts").mkdir(exist_ok=True)
for node in tree.body:
    if not isinstance(node, ast.Assign):
        raise ValueError(f"Unexpected statement: {type(node).__name__}")
    if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
        raise ValueError("Unexpected assignment")
    name = node.targets[0].id
    value = string_value(node.value)
    values[name] = value
    dest = ROOT / "prompts" / f"{name}.md"
    header = (
        f"# {name}\n\n"
        f"来源：[Finch / src/fhda/prompts.py 第 {node.lineno}–{node.end_lineno} 行]"
        f"({BASE}src/fhda/prompts.py#L{node.lineno}-L{node.end_lineno})。\n\n"
        "许可：Apache-2.0，完整许可证在 `../original/LICENSE`。\n\n"
        "下方为公开源码中的字符串值。f-string 中引用的固定文本已按源码展开，"
        "任务变量保留原样。未翻译或修改正文；Markdown 标题和说明为本次添加。\n\n"
        "````text\n"
    )
    body = value + ("" if value.endswith("\n") else "\n")
    dest.write_text(header + body + "````\n", encoding="utf-8", newline="\n")
    assert dest.read_text(encoding="utf-8").split("````text\n", 1)[1].rsplit("````\n", 1)[0] == body
    records.append({
        "name": name,
        "source_file": "src/fhda/prompts.py",
        "source_lines": [node.lineno, node.end_lineno],
        "source_url": f"{BASE}src/fhda/prompts.py#L{node.lineno}-L{node.end_lineno}",
        "output": dest.relative_to(ROOT).as_posix(),
        "string_sha256": hashlib.sha256(value.encode()).hexdigest(),
        "characters": len(value),
    })

files = []
for path in sorted((ROOT / "original").rglob("*")):
    if path.is_file():
        rel = path.relative_to(ROOT / "original").as_posix()
        files.append({"source_file": rel, "source_url": BASE + rel, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size})

(ROOT / "manifest.json").write_text(json.dumps({
    "project": "Future-House/finch (public standalone source)",
    "commit": COMMIT,
    "retrieved": "2026-09-15",
    "license": "Apache-2.0",
    "scope": "Public Finch prompt constants only; not a recovery of hosted Edison system prompts.",
    "extraction": "Static AST string evaluation; source files were not imported or executed; source originals retained byte-for-byte as downloaded.",
    "prompt_count": len(records),
    "prompts": records,
    "original_files": files,
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(f"Extracted {len(records)} prompt constants; all Markdown prompt bodies match the source string values.")
