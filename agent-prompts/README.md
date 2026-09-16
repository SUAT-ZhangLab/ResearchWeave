# 三个科研系统的 Agent 提示词与方法

提取日期：2026-09-15。

**可以把 Robin 和 Co-Scientist 看作多智能体系统。ERA 则主要由“代码生成模型 + 搜索算法 + 执行与评分程序”组成。**同一个模型可以在不同步骤承担不同职责；每份提示词不一定对应一个独立运行的 agent。

这里所说的“人格”主要是角色定位、任务目标、判断标准、工具用法和输出格式。例如“实验生物学家”“研究方案评议员”“数据科学家”。系统的文件访问、文献检索、候选排序、运行状态和反复修改，还需要程序或在线服务提供。


## 1. 按系统查看

| 系统 | 提取依据与内容 | 阅读入口 |
|---|---|---|
| Robin | 官方 Python 中的角色提示、任务模板、报告格式、分析步骤及动态组合表达式；另按实际调用整理中文职责说明 | [角色目录](robin/roles.md) · [组合与调用方法](robin/methods.md) · [清单](robin/manifest.json) |
| Co-Scientist | 论文官方补充材料中的提示词与伪代码；按公开角色整理 | [角色与方法说明](co-scientist/roles.md) |
| ERA | 官方代码生成提示、程序改进提示及领域任务 notebook 中的原始任务定义 | [角色与方法说明](era/roles.md) · [清单](era/manifest.json) |
| Robin 的外部组件 | 额外提取独立开源 Finch 的提示词；说明 Crow/Falcon/Edison 哪些内容能取得 | [组件说明](robin-components/README.md) |

Robin 与 ERA 的当前源码并非用一套 PERSONA.md 或 AGENTS.md 来定义各角色。本次把它们分散在 Python、notebook 和论文中的公开内容转换成便于阅读的 Markdown。

## 2. 原文和整理说明怎样区分

- **官方原文**：保留英文、变量名、输出格式和方法要求，并给出源码版本或 PDF 页码。
- **源码表达式**：对动态 f-string 保留完整表达式；其中变量尚未填入，不能当作某次实际发送的完整消息。
- **中文角色说明**：解释“负责什么、输入什么、怎么做、交出什么、原始模板在哪里”。这是本次根据材料整理的说明。
- **程序方法**：保留或说明搜索、比较、调度和执行方式。它们不一定由语言模型扮演角色。

各系统文件保留来源与许可。代码材料遵循各自仓库许可；Co-Scientist 论文材料的许可和作者信息见其目录说明。

## 3. 最适合先读的角色

### Robin：容易直接理解和复用的任务分工

- [实验策略设计](robin/roles/02-assay-designer.md)
- [候选药物与机制假设提出](robin/roles/07-candidate-generator.md)
- [候选药物比较](robin/roles/09-candidate-reviewer.md)
- [实验结果解释](robin/roles/12-data-interpreter.md)
- [后续实验建议](robin/roles/13-followup-planner.md)

每份角色说明都链接到对应 system/user 提示词。Robin 此处整理出14种任务职责和1份通用 notebook 方法，便于按用途阅读；这个数量不是作者声称的独立 agent 数量。

### Co-Scientist：生成与评议假设

重点看 Generation、Reflection、Ranking、Evolution、Proximity、Meta-review 六类工作，以及 Supervisor 如何安排它们。论文公开提示词可以提取；当前在线服务内部的完整设置仍不公开。

### ERA：把想法变成可以评分的程序

重点看代码生成角色、问题与评分要求，以及上一份代码和分数怎样传回下一轮。FUTS 搜索、执行器和评分器由程序完成，不能仅靠一份角色 MD 自动获得这些功能。

## 4. 怎样把这些文件用于自己的 Agent

1. **先选职责。** 例如，只需要根据实验结果提出后续实验，就先读 Robin 的“后续实验建议”。
2. **保持消息分工。** 按原代码的消息方式组织角色和任务。Robin 区分 system/user；ERA 该示例将角色模板与任务一起放进 contents。
3. **填写实际输入。** 例如该角色需要 goal、analysis_summary、mechanistic_insights、questions_raised。没有的数据要明确说明缺失。
4. **按任务接好工具与代码。** 文献代理需要检索工具；代码代理需要实际执行与评分；多候选系统还需要保存候选和安排下一轮。
5. **用一个小任务检查结果。** 看它是否按约定输出、是否引用了输入依据，再决定是否扩大使用。

提取出的原始模板保留了作者的具体实验设定和方法选择，实际使用时应结合自己的任务逐项决定。尤其不能把模型给出的相对排名当作实验测量，把同一批数据的多次计算当作新的独立实验。

## 5. 原始材料

- [Robin 官方仓库](https://github.com/Future-House/robin)
- [Co-Scientist 论文](https://www.nature.com/articles/s41586-026-10644-y)
- [ERA 官方仓库](https://github.com/google-research/era)
- [独立 Finch 官方仓库](https://github.com/Future-House/finch)

完整路径、提取数量与内容摘要值见各目录 manifest.json。中文说明与原始文件分开保存，便于以后按来源检查或重新提取。
