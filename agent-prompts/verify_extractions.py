import ast, hashlib, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"agent-prompts"
digest=lambda b: hashlib.sha256(b).hexdigest()
checks=[]
m=json.loads((BASE/"robin"/"manifest.json").read_text(encoding="utf-8-sig"))
src=ROOT/"vendor"/"robin"/"robin"/"prompts.py"
values={n.targets[0].id:ast.literal_eval(n.value) for n in ast.parse(src.read_text(encoding="utf-8")).body
        if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name)}
for item in m["static_prompts"]:
    value=values[item["symbol"]]
    if item["key"] is not None: value=value[item["key"]]
    assert digest(value.encode())==item["text_sha256"],item["name"]
    assert "\n"+value+"\n" in (BASE/"robin"/item["path"]).read_text(encoding="utf-8"),item["name"]
checks.append({"system":"Robin","exact_source_literals_verified":len(m["static_prompts"])})
e=json.loads((BASE/"era"/"manifest.json").read_text(encoding="utf-8-sig"))
for item in e["items"]:
    assert digest((BASE/"era"/item["file"]).read_bytes())==item["sha256"],item["file"]
checks.append({"system":"ERA","output_hashes_verified":len(e["items"])})
c=json.loads((BASE/"co-scientist"/"manifest.json").read_text(encoding="utf-8-sig"))
assert digest((BASE/"co-scientist"/"source"/"41586_2026_10644_MOESM1_ESM.pdf").read_bytes())==c["pdf_sha256"]
fence=chr(96)*3
for item in c["templates"]:
    md=(BASE/"co-scientist"/item["file"]).read_text(encoding="utf-8")
    prompt=md.split(fence+"text\n",1)[1].rsplit("\n"+fence,1)[0]
    assert digest(prompt.encode())==item["prompt_sha256"],item["file"]
checks.append({"system":"Co-Scientist","source_pdf_hash_verified":True,"prompt_bodies_verified":len(c["templates"])})
f=json.loads((BASE/"robin-components"/"manifest.json").read_text(encoding="utf-8-sig"))
for item in f["prompts"]:
    md=(BASE/"robin-components"/item["output"]).read_text(encoding="utf-8")
    match=re.search("(?m)^("+chr(96)+"{3,}|~{3,})text\n",md)
    assert match, item["name"]
    body=md[match.end():].rsplit(match[1]+"\n",1)[0]
    prompt=body[:item["characters"]]
    assert body[item["characters"]:] in ("", "\n"), item["name"]
    assert digest(prompt.encode())==item["string_sha256"],item["name"]
checks.append({"system":"Finch","prompt_bodies_verified":len(f["prompts"])})
print(json.dumps(checks,ensure_ascii=False,indent=2))

