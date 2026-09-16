"""Extract the pinned Robin prompt strings without importing or running Robin."""
import ast
import hashlib
import json
from pathlib import Path
import re
import shutil

PROJECT = Path(__file__).resolve().parents[2]
SOURCE = PROJECT / "vendor" / "robin"
OUT = PROJECT / "agent-prompts" / "robin"
COMMIT = "4a5cce310f3bc7663a67117db88af43b84733ffe"
BASE = f"https://github.com/Future-House/robin/blob/{COMMIT}/"
def sha(data): return hashlib.sha256(data).hexdigest()
def fenced(s, language="text"):
    longest = max((len(x) for x in re.findall(r"~+", s)), default=0)
    fence = "~" * max(4, longest+1)
    return f"{fence}{language}\n{s}\n{fence}\n"

for d in ("original", "source", "roles"):
    (OUT / d).mkdir(parents=True, exist_ok=True)
shutil.copyfile(SOURCE / "LICENSE", OUT / "LICENSE")
for name in ("prompts.py", "assays.py", "candidates.py", "analyses.py", "utils.py", "configuration.py", "multitrajectory_runner.py"):
    shutil.copyfile(SOURCE / "robin" / name, OUT / "source" / name)
source_path = SOURCE / "robin" / "prompts.py"
text = source_path.read_text(encoding="utf-8")
entries = []
values = {}
for node in ast.parse(text).body:
    if not isinstance(node, ast.Assign) or not isinstance(node.targets[0], ast.Name):
        continue
    symbol = node.targets[0].id
    value = ast.literal_eval(node.value)
    variants = value.items() if isinstance(value, dict) else [(None, value)]
    for key, prompt in variants:
        if not isinstance(prompt, str):
            raise TypeError(symbol)
        name = symbol + (f"__{key}" if key else "")
        values[name] = prompt
        url = f"{BASE}robin/prompts.py#L{node.lineno}-L{node.end_lineno}"
        parameters = sorted(set(re.findall(r"(?<!{){([A-Za-z_][A-Za-z0-9_]*)[^}]*}(?!})", prompt)))
        path = f"original/{name}.md"
        header = (
            f"# {name}\n\n"
            "**性质：官方代码中的提示词字符串，英文内容未改写。**\n\n"
            f"- 出处：[{symbol}" + (f"[{key!r}]" if key else "") + f"]({url})\n"
            f"- 提交号：{COMMIT}\n"
            "- 作者/来源：FutureHouse technical staff / Future-House/robin\n"
            "- 许可：Apache-2.0，全文见 ../LICENSE。\n"
            "- 提取方式：Python AST literal_eval；合并相邻字符串并还原源码转义，不执行原程序。\n"
            f"- 模板变量（仅供阅读）：{', '.join(parameters) or '无'}。\n"
            "- 下面是替换变量前的字符串；不会自动调用原系统的检索或执行工具。\n\n"
            "## 原文\n\n"
        )
        (OUT / path).write_text(header + fenced(prompt), encoding="utf-8")
        entries.append(dict(name=name, source="robin/prompts.py", symbol=symbol, key=key,
                            line_start=node.lineno, line_end=node.end_lineno, source_url=url,
                            path=path, characters=len(prompt), text_sha256=sha(prompt.encode()),
                            template_variables=parameters, extraction="ast.literal_eval"))

# These strings are assembled dynamically. Keep the exact source expressions
# rather than inventing a completed prompt or evaluating unknown runtime values.
inline = []
for filename, target_names in {
    "utils.py": {"user_prompt"},
    "analyses.py": {"analysis_prompt", "consensus_prompt"},
}.items():
    source_text = (SOURCE / "robin" / filename).read_text(encoding="utf-8")
    for node in ast.walk(ast.parse(source_text)):
        if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.JoinedStr):
            continue
        if not isinstance(node.targets[0], ast.Name) or node.targets[0].id not in target_names:
            continue
        name = filename[:-3] + "__" + node.targets[0].id
        expression = ast.get_source_segment(source_text, node.value)
        path = f"original/{name}.md"
        url = f"{BASE}robin/{filename}#L{node.lineno}-L{node.end_lineno}"
        document = (
            f"# {name}\n\n**性质：官方动态提示词的原始 Python 表达式。不是变量已填好的最终提示词。**\n\n"
            f"来源：[robin/{filename}:{node.lineno}]({url})；提交 {COMMIT}；许可 Apache-2.0。\n\n"
            "## 原始表达式\n\n" + fenced(expression, "python"))
        (OUT / path).write_text(document, encoding="utf-8")
        inline.append(dict(name=name, source=f"robin/{filename}", line_start=node.lineno,
                           line_end=node.end_lineno, path=path, source_url=url,
                           expression_sha256=sha(expression.encode())))

# Preserve actual dispatch/formatting code as methods, rather than claiming it
# can be reproduced just by adding another role prompt.
method_parts = ["# Robin 的提示词组合与调用方法\n\n"
                "**下面保留官方源码片段；解释文字是本次整理。**变量模板由程序填入。"
                "只复制角色文字，不会自动获得原有检索、排序或文件处理能力。\n"]
for filename, wanted in {
    "multitrajectory_runner.py": {"cot_prompting", "format_prompt", "_create_task_requests"},
    "utils.py": {"run_comparisons"},
}.items():
    s = (SOURCE / "robin" / filename).read_text(encoding="utf-8")
    for node in ast.walk(ast.parse(s)):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in wanted:
            url=f"{BASE}robin/{filename}#L{node.lineno}-L{node.end_lineno}"
            method_parts.append(f"\n## {node.name}\n\n[原始位置]({url})\n\n"+fenced(ast.get_source_segment(s,node),"python"))
(OUT / "methods.md").write_text("\n".join(method_parts),encoding="utf-8")

groups=[
("01-assay-query-writer","实验文献检索问题设计","根据疾病名称提出能够帮助选择实验的检索问题。","疾病、检索问题数、预期实验数","检索问题文本；随后由 Crow 执行检索。",
 ["ASSAY_LITERATURE_SYSTEM_MESSAGE","ASSAY_LITERATURE_USER_MESSAGE"],"robin/assays.py"),
("02-assay-designer","实验策略设计","根据文献报告提出不同实验方法和相应理由。","疾病、实验候选数、Crow 检索结果","实验策略及理由。",
 ["ASSAY_PROPOSAL_SYSTEM_MESSAGE","ASSAY_PROPOSAL_USER_MESSAGE"],"robin/assays.py"),
("03-assay-evidence-researcher","实验策略证据研究","围绕单个实验策略形成较完整的文献报告。","疾病、单个实验策略、报告要求","由 Crow 返回的研究报告。",
 ["ASSAY_HYPOTHESIS_SYSTEM_PROMPT","ASSAY_HYPOTHESIS_FORMAT"],"robin/assays.py"),
("04-assay-reviewer","实验策略比较","按源码给出的科学标准比较两份实验报告。","疾病、两份报告、各自编号","包含胜者及理由的规定格式；随后由程序汇总排序。",
 ["ASSAY_RANKING_SYSTEM_PROMPT","ASSAY_RANKING_PROMPT_FORMAT","utils__user_prompt"],"robin/assays.py"),
("05-objective-writer","候选研究目标整理","把优先实验策略整理为后续药物候选生成目标。","疾病、选中的实验策略","candidate_generation_goal 文本。",
 ["SYNTHESIZE_SYSTEM_MESSAGE_CONTENT","SYNTHESIZE_USER_CONTENT"],"robin/assays.py"),
("06-candidate-query-writer","药物文献检索问题设计","为药物候选提出检索问题；后续轮次可加入实验反馈。","疾病、研究目标、检索问题数、可选实验解释","交给 Crow 的检索问题。",
 ["CANDIDATE_QUERY_GENERATION_SYSTEM_MESSAGE","CANDIDATE_QUERY_GENERATION_CONTENT_MESSAGE","EXPERIMENTAL_INSIGHTS_APPENDAGE"],"robin/candidates.py"),
("07-candidate-generator","药物候选与机制假设提出","利用已有报告提出候选药物和机制；可将实验反馈加入这一轮输入。","疾病、候选数、文献结果、可选实验反馈","候选名称、假设与理由。",
 ["CANDIDATE_GENERATION_SYSTEM_MESSAGE","CANDIDATE_GENERATION_USER_MESSAGE","EXPERIMENTAL_INSIGHTS_FOR_CANDIDATE_GENERATION"],"robin/candidates.py"),
("08-candidate-evidence-researcher","候选药物证据研究","为单个候选查找和整理更详细的科学依据。","疾病、候选药物与假设、报告格式","由 Falcon 返回的候选报告。",
 ["CANDIDATE_LIT_REVIEW_DIRECTION_PROMPT","CANDIDATE_REPORT_FORMAT"],"robin/candidates.py"),
("09-candidate-reviewer","候选药物比较","依据提示词中的标准逐对比较候选报告。","疾病、两份候选报告及编号","比较理由和胜者；程序据此计算相对排名。",
 ["CANDIDATE_RANKING_SYSTEM_PROMPT","CANDIDATE_RANKING_PROMPT_FORMAT","utils__user_prompt"],"robin/candidates.py"),
("10-data-analyst","实验数据分析","在 notebook 中读取数据、制定分析、运行计算并导出结果。","数据文件与对应说明、分析类型、任务提示","CSV、notebook 等云端任务产物。",
 ["COT","GUIDELINE","ANALYSIS_QUERIES__flow_cytometry","ANALYSIS_QUERIES__RNA_seq","analyses__analysis_prompt"],"robin/analyses.py"),
("11-analysis-comparison","多次分析结果汇总","读取同一批数据的多次分析结果，按公开提示组织汇总。","多次分析输出、分析类型","汇总结果 CSV。",
 ["COT","GUIDELINE","CONSENSUS_QUERIES__flow_cytometry","CONSENSUS_QUERIES__RNA_seq","analyses__consensus_prompt"],"robin/analyses.py"),
("12-data-interpreter","实验结果解释","将实际数据结果与研究目标放在一起，整理发现、问题和机制线索。","goal、data_html","以 <> 分开的药物列表、结果总结、新问题和机制线索。",
 ["DATA_INTERPRETATION_SYSTEM_MESSAGE","DATA_INTERPRETATION_CONTENT_MESSAGE"],"robin/analyses.py"),
("13-followup-planner","后续实验建议","根据结果总结、问题和机制线索判断是否值得继续实验。","goal、analysis_summary、mechanistic_insights、questions_raised","实验名称和简明科学理由；无必要时允许不提出新实验。",
 ["FOLLOWUP_SYSTEM_MESSAGE","FOLLOWUP_CONTENT_MESSAGE"],"robin/analyses.py"),
("14-report-formatter","研究报告格式整理","将代理返回的正文和来源整理成规定格式。","answer_text、sources_text","格式统一的报告。",
 ["FINAL_REPORT_FORMATTING_SYSTEM_MESSAGE","FINAL_REPORT_FORMATTING_USER_MESSAGE"],"robin/utils.py"),
]
for slug,title,method,inputs,outputs,names,source in groups:
    document=f"# {title}\n\n**本文件是根据官方代码整理的中文角色说明，不是作者原有的角色 MD，也不代表一个独立常驻 agent。**\n\n"
    document+=f"## 职责和方法\n\n{method}\n\n## 输入\n\n{inputs}。\n\n## 输出\n\n{outputs}\n\n## 使用哪些原始提示词\n\n"
    for name in names:
        document+=f"- [{name}](../original/{name}.md)\n"
    document+=f"\n## 谁负责调用\n\n[官方 {source}]({BASE}{source}) 负责组合这些提示词并调用服务。原文在 original/，变量填充与服务调用仍需要程序完成。\n"
    if slug=="11-analysis-comparison":
        document+="\n源码的汇总提示保留了合并 P 值等原始做法。它没有被本次提取修改；多次计算使用同一批样本，不会新增独立生物学重复。实际使用时须结合实验设计判断是否采用。\n"
    (OUT/"roles"/f"{slug}.md").write_text(document,encoding="utf-8")

guide_names=["GENERAL_NOTEBOOK_GUIDELINES","R_SPECIFIC_GUIDELINES","CHAIN_OF_THOUGHT_AGNOSTIC"]
(OUT/"roles"/"15-notebook-method.md").write_text(
    "# Notebook 通用方法\n\n**这是本次整理的方法说明，不是一个新增 agent。**\n\n"
    "这些模板规定语言、单元格大小、出错后修改方式、包安装和图表要求。它们由 Step.cot_prompting/format_prompt 按实际配置组合；仅出现在源码中不代表每次运行都会使用。\n\n"
    +"\n".join(f"- [{n}](../original/{n}.md)" for n in guide_names)+"\n",encoding="utf-8")

manifest={"system":"Robin","repository":"https://github.com/Future-House/robin","commit":COMMIT,
          "license":"Apache-2.0","source_file_sha256":sha(source_path.read_bytes()),
          "static_prompt_count":len(entries),"dynamic_expression_count":len(inline),
          "static_prompts":entries,"dynamic_expressions":inline,
          "role_descriptions_are_editorial":True,"role_description_count":len(groups),
          "upstream_files_modified":False}
(OUT/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
overview="# Robin：角色与原始提示词\n\n**已提取 35 个原始字符串模板、3 个动态组合表达式，并整理14种任务职责和1份通用方法说明。**这些数量不是论文所称的agent数量；多数职责由同一配置的模型在不同步骤承担。\n\n"
overview+="[原始代码 prompts.py]("+BASE+"robin/prompts.py)；[完整清单](manifest.json)；[提示组合方法](methods.md)。\n\n"
overview+="## 按工作职责阅读\n\n"
for slug,title,*_ in groups: overview+=f"- [{title}](roles/{slug}.md)\n"
overview+="- [Notebook 通用方法](roles/15-notebook-method.md)\n\n"
overview+="## 什么被保留\n\noriginal/ 保留英文提示词、占位符和原始格式要求；source/ 保存提取依据。字符串由AST静态读取，没有运行原系统。单个模板没有附带Crow/Falcon/Finch的服务内部提示、模型权重、可用工具或执行状态。\n\n"
overview+="原文里的推理和输出要求属于作者模板，本次仅提取；并不承诺其他模型会以同样方式执行，也没有将其所有统计处理建议视为适用。\n\n"
overview+="## 全部原始模板\n\n| 名称 | 源码行 | 原文字符数 |\n|---|---:|---:|\n"
for x in entries: overview+=f"| [{x['name']}]({x['path']}) | {x['line_start']} | {x['characters']} |\n"
for x in inline: overview+=f"| [{x['name']}]({x['path']}) | {x['line_start']} | 动态表达式 |\n"
(OUT/"roles.md").write_text(overview,encoding="utf-8")
# Check every extracted literal against the precise text in its Markdown block.
for x in entries:
    actual=(OUT/x["path"]).read_text(encoding="utf-8")
    prompt=values[x["name"]]
    assert fenced(prompt) in actual
    assert x["text_sha256"]==sha(prompt.encode())
print(json.dumps({"static_prompts":len(entries),"dynamic_expressions":len(inline),
                  "role_cards":len(groups)+1,"verified":"exact literal text and hashes",
                  "output":str(OUT)},ensure_ascii=False))

