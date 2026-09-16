# Robin 依赖的外部 Agent：哪些提示能取得

**已提取 Finch 独立开源版本的 17 段提示。它们定义生物数据分析角色、Notebook 工作方法、任务格式和答案提交方式。** 这些文件适合阅读和改编，但不能当作当前 Edison 云端 Finch/Analysis 服务的全部内部提示。

提取日期：2026-09-15。固定版本：[`aea66fdf2dd2be827727de50a73cae60dff59972`](https://github.com/Future-House/finch/tree/aea66fdf2dd2be827727de50a73cae60dff59972)。来源与原文许可：[Finch 官方仓库](https://github.com/Future-House/finch)，Apache-2.0。

## 1. Crow、Falcon 和 Finch 各取得了什么

| 组件 | 公开角色 | 本次取得的材料 | 尚未取得的材料 |
|---|---|---|---|
| Crow | 检索文献，给出简洁、有文献依据的回答 | Robin 源码中发给服务的任务提示由上级目录的 Robin 提取整理；官方对角色的说明 | 当前托管服务完整 system prompt、运行配置和全部工具定义 |
| Falcon | 深入检索并综合多篇文献 | 同上；Robin 当前 README 把 Crow/Falcon 标为 Edison Literature | 当前托管服务完整 system prompt、运行配置和全部工具定义 |
| Finch | 围绕数据和问题，逐步编写、运行、修改 Jupyter Notebook | 独立开源 Finch 的完整 `prompts.py`，17 段提示的 Markdown，以及必要调用代码 | 当前 Edison Analysis 的全部内部提示，以及开源版本与当前服务逐项一致的证据 |

Crow/Falcon 的角色依据是 [FutureHouse 官方平台发布说明](https://www.futurehouse.org/news/launching-futurehouse-platform-ai-agents)。当前命名依据是 [Robin 官方 README](https://github.com/Future-House/robin#prerequisites)。

[PaperQA 官方仓库](https://github.com/Future-House/paper-qa)提供公开的文献 Agent 实现和可定制提示；官方也说明其内部工具及论文访问权限与开源版本不同。没有证据表明拿到 PaperQA 的提示，就拿到了目前 Crow/Falcon 服务的完整定义。因此，本次没有把 PaperQA 的提示冒充为 Crow/Falcon 提示，也没有额外下载整个 PaperQA 仓库。

## 2. 先看这几份 Markdown

以下目录中的英文文本来自源码，不是本次撰写的新角色指令。代码中重复引用的固定片段已展开，任务变量仍保留。

| 想了解的内容 | 文件 | 要点 |
|---|---|---|
| Finch 面对普通用户问题时的角色 | [CAPSULE_SYSTEM_PROMPT_QUERY](prompts/CAPSULE_SYSTEM_PROMPT_QUERY.md) | 专业生物信息学和生物数据分析人员；先理解问题与数据，再写代码；产物为包含所需分析证据的 Notebook |
| 分析方法 | [CHAIN_OF_THOUGHT_AGNOSTIC](prompts/CHAIN_OF_THOUGHT_AGNOSTIC.md) | 数据与描述统计 → 分析计划 → 实施分析 → 总结和提交；覆盖缺失值、混杂因素、统计假设等 |
| Notebook 使用约定 | [GENERAL_NOTEBOOK_GUIDELINES](prompts/GENERAL_NOTEBOOK_GUIDELINES.md) | 使用适当大小的单元；修改出错单元；查看数据规模；检查单元执行；只建立代码单元 |
| 在先前 Notebook 上继续回答 | [CONTINUATION_PROMPT_TEMPLATE](prompts/CONTINUATION_PROMPT_TEMPLATE.md) | 加入前一个问题、前一个答案、新问题，要求更新相关单元及后续结果 |

`CHAIN_OF_THOUGHT_AGNOSTIC` 是原仓库的变量名；本次保留其公开原文。

## 3. 全部 17 段提示

### 角色定义：4 段

- [CAPSULE_SYSTEM_PROMPT_HYPOTHESIS](prompts/CAPSULE_SYSTEM_PROMPT_HYPOTHESIS.md)：判断给定数据是否支持假设。
- [CAPSULE_SYSTEM_PROMPT_MCQ](prompts/CAPSULE_SYSTEM_PROMPT_MCQ.md)：分析数据，回答选择题。
- [CAPSULE_SYSTEM_PROMPT_OPEN](prompts/CAPSULE_SYSTEM_PROMPT_OPEN.md)：分析数据，回答开放问题。
- [CAPSULE_SYSTEM_PROMPT_QUERY](prompts/CAPSULE_SYSTEM_PROMPT_QUERY.md)：分析数据，回答用户的一般问题。

### 工作方法和工具提示：5 段

- [CHAIN_OF_THOUGHT_AGNOSTIC](prompts/CHAIN_OF_THOUGHT_AGNOSTIC.md)：分析阶段与应考虑的事项。
- [GENERAL_NOTEBOOK_GUIDELINES](prompts/GENERAL_NOTEBOOK_GUIDELINES.md)：Notebook 单元和执行规范；含 `{language}`。
- [R_SPECIFIC_GUIDELINES](prompts/R_SPECIFIC_GUIDELINES.md)：R 包、tidyverse、ggplot2 和函数命名方式。
- [AVOID_IMAGES](prompts/AVOID_IMAGES.md)：可选的偏好表格与打印输出的指令，并非通用入口一定启用。
- [BASH_TOOL_USAGE](prompts/BASH_TOOL_USAGE.md)：BUSCO 及部分生物信息学命令工具的公开使用提示，并非通用入口一定启用。

### 答案提交格式：4 段

- [SUBMIT_ANSWER_HYPOTHESIS](prompts/SUBMIT_ANSWER_HYPOTHESIS.md)：提交 `True` 或 `False`。
- [SUBMIT_ANSWER_SINGLE](prompts/SUBMIT_ANSWER_SINGLE.md)：用 `<answer>` 标签提交单个答案。
- [SUBMIT_ANSWER_OPEN](prompts/SUBMIT_ANSWER_OPEN.md)：用 `<answer>` 标签提交简短文字答案。
- [SUBMIT_ANSWER_MCQ](prompts/SUBMIT_ANSWER_MCQ.md)：用 `<answer>` 标签提交选项字母。

### 已组合的任务模板：4 段

- [HYPOTHESIS_PROMPT_TEMPLATE](prompts/HYPOTHESIS_PROMPT_TEMPLATE.md)：`{hypothesis}` 加工作方法、提交格式和 Notebook/R 规则。
- [MCQ_PROMPT_TEMPLATE](prompts/MCQ_PROMPT_TEMPLATE.md)：`{question}` 加工作方法、提交格式和 Notebook/R 规则。
- [OPEN_PROMPT_TEMPLATE](prompts/OPEN_PROMPT_TEMPLATE.md)：`{question}` 加工作方法、提交格式和 Notebook/R 规则。
- [CONTINUATION_PROMPT_TEMPLATE](prompts/CONTINUATION_PROMPT_TEMPLATE.md)：`{previous_research_question}`、`{previous_final_answer}`、`{query}` 加 Notebook 规则；还含 `{language}`。

## 4. 代码怎样把这些文本变成 Agent 行为

普通用户任务入口见 [data_analysis_env.py](original/src/fhda/data_analysis_env.py) 的 `DataAnalysisEnv.from_task()`。

1. 接收 `<data_path> | <query>`，或已上传数据所在位置与用户问题。
2. 创建本次任务目录，放入数据和 `notebook.ipynb`。
3. 把用户问题与分析方法、Notebook 规则组成任务消息。
4. 用 `CAPSULE_SYSTEM_PROMPT_QUERY` 作为系统角色提示。
5. 提供 Notebook 工具，让模型根据执行结果继续操作。
6. `submit_answer` 保存最终答案、结束本次任务并关闭环境。

[notebook_env.py](original/src/fhda/notebook_env.py) 注册的基本工具如下。这些 Python 函数及其说明也是 Agent 行为定义的一部分，仅复制提示文字不会复制这些能力。

| 工具 | 输入 | 处理和返回 |
|---|---|---|
| `edit_cell` | `contents` 代码；可选 `idx` 单元编号 | 新增或修改代码单元，保存并运行 Notebook；下一步观察包含更新后的 Notebook 状态 |
| `list_workdir` | 无 | 返回工作目录内容的 JSON |
| `submit_answer` | 答案 | 记录答案并结束任务 |
| `download_from_bucket` | 存储位置、任务目录内目标位置 | 启用 GCS 下载时才提供，下载后返回文件内容列表 |

**这些 MD 是从 Python 字符串生成的阅读副本。** 官方程序不会自动加载本目录中的 MD；修改这些副本也不会自动改变现有 Robin 或 Finch 的行为。需要改编时，应把选定的角色提示、任务模板与实际 Notebook 工具接在一起。

17 段提示也不是 17 个独立 Agent。多数是同一个数据分析 Agent 按任务类型选用的片段。

公开源码不同入口还有未同步的命名：例如 `dataset.py` 引用了 `CAPSULE_PROMPT_TEMPLATES`，但该版本 `prompts.py` 未定义它；普通用户入口拼入的方法文本仍含 `{language}`。本次保留原样，不把这些模板描述为已经安装、跑通的新 Finch 系统。

## 5. 保存和检查方式

- `original/`：官方 6 个原文件，包括提示、调用代码、README 和 LICENSE；没有修改内容。
- `prompts/`：17 个独立 Markdown，保留源码字符串值及固定版本、行号、许可证说明。
- [manifest.json](manifest.json)：每段提示的名称、来源行号、文件链接、字符数和 SHA-256；另有下载原文件的 SHA-256。
- [extract_finch.py](extract_finch.py)：只解析 Python 语法中的字符串和固定字符串引用，不导入或执行 Finch 源码。

提取脚本已经运行；17 个 Markdown 提示正文均已与解析所得源码字符串逐项比较一致。未调用付费模型，也未安装新的 Finch 环境。
