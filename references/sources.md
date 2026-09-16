# 来源、改编内容与许可

版本日期：2026-09-15。

`roles.md` 是为本项目的 agent 使用方式编写的中文适配指令。它重新安排职责、缩短循环、统一记录格式，并补充数据分析与结果保存要求。它没有照搬任何系统的全部运行行为。英文提取文件保持原样，位于下列本机来源目录。

当前 agent 负责模型交互、选择工具与安排任务；角色文档提供方法。多个角色可以由同一个 agent 承担。Google 官方 Co-Scientist 服务没有安装。使用公开方法编写的角色，不能称作 Google 官方服务或其完整复现。

## 1. Robin

- 项目与作者归属：FutureHouse / Future-House，Robin。
- [官方仓库及固定版本](https://github.com/Future-House/robin/tree/4a5cce310f3bc7663a67117db88af43b84733ffe)。Commit：`4a5cce310f3bc7663a67117db88af43b84733ffe`。
- [原始提示词代码](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/prompts.py)。本地副本：[原始提示词清单](../agent-prompts/robin/roles.md)、[组合与调用方法](../agent-prompts/robin/methods.md)、[提取记录](../agent-prompts/robin/manifest.json)。
- [正式论文](https://www.nature.com/articles/s41586-026-10652-y)，DOI `10.1038/s41586-026-10652-y`。
- 许可：[Apache License 2.0](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/LICENSE)。原始源码和提取内容的权利归属、版权声明与许可应保留；中文角色是本项目改编，不能标为原作者原文。

### 本次具体使用

| 中文角色 | 参考的公开源代码或提取文件 |
|---|---|
| 协调研究 | `robin/analyses.py` 的分析、解释、后续实验安排；`ASSAY_*` 和 `CANDIDATE_*` 任务次序 |
| 文献证据 | `ASSAY_LITERATURE_SYSTEM_MESSAGE`（`prompts.py` 第 367 行起）、`ASSAY_HYPOTHESIS_SYSTEM_PROMPT`（第 428 行起）、`CANDIDATE_LIT_REVIEW_DIRECTION_PROMPT`（第 659 行起） |
| 评议比较 | `ASSAY_RANKING_SYSTEM_PROMPT`（第 458 行起）、`CANDIDATE_RANKING_SYSTEM_PROMPT`（第 691 行起） |
| 制定数据分析 | `GENERAL_NOTEBOOK_GUIDELINES`（第 181 行起）、`ANALYSIS_QUERIES`（第 279 行起） |
| 解释与更新研究 | `DATA_INTERPRETATION_SYSTEM_MESSAGE`（第 105 行起）及对应 content；`FOLLOWUP_SYSTEM_MESSAGE`（第 139 行起）及对应 content |

[结果解释原文](../agent-prompts/robin/original/DATA_INTERPRETATION_CONTENT_MESSAGE.md) · [后续实验原文](../agent-prompts/robin/original/FOLLOWUP_CONTENT_MESSAGE.md)。

改编说明：保留“研究目标—证据—候选—分析—解释—后续工作”的组织方法；不采用全部药物、流式或特定统计设置；将原格式改为本项目 JSON 记录；用简短理由和来源替代要求展示完整内部思考的表述。

## 2. Co-Scientist

- 作者：Juraj Gottweis、Wei-Hung Weng、Alexander Daryin 等。
- [Accelerating scientific discovery with Co-Scientist](https://www.nature.com/articles/s41586-026-10644-y)，Nature 655, 487–496 (2026)，DOI `10.1038/s41586-026-10644-y`。
- [官方补充材料 PDF](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-026-10644-y/MediaObjects/41586_2026_10644_MOESM1_ESM.pdf)。SHA256：`e5595509a10da6e4d24c7df399d0f60e922d628cf1647df3880f8b0ba1c93fbc`。
- 本地：[原 PDF](../agent-prompts/co-scientist/source/41586_2026_10644_MOESM1_ESM.pdf)、[公开角色说明](../agent-prompts/co-scientist/roles.md)、[提取记录](../agent-prompts/co-scientist/manifest.json)。
- 许可：[Creative Commons Attribution 4.0 International（CC BY 4.0）](https://creativecommons.org/licenses/by/4.0/)。允许署名后复制、分享与改编；本项目保留作者、作品、来源、许可及修改说明。Co-Scientist 的中文改编段落使用该许可。

以下页码是 **PDF 物理页码，封面算第 1 页**。

| 本次使用的方法 | 公开材料与页码 | 提取的英文文本 |
|---|---|---|
| 工作安排 | Note 8，56–61；Supervisor 56–57 | [伪代码](../agent-prompts/co-scientist/original/00-orchestration-pseudocode.md) |
| 提出具体假设 | Note 9.1，62–64 | [文献后生成假设](../agent-prompts/co-scientist/original/01-generation-literature-review.md) |
| 对照观察检查假设 | Note 9.2，64–65 | [Reflection](../agent-prompts/co-scientist/original/03-reflection-observations.md) |
| 按共同标准比较 | Note 9.3，65–67 | [Ranking](../agent-prompts/co-scientist/original/04-ranking-comparison.md) |
| 改进实际可行性 | Note 9.4，67–68 | [Evolution](../agent-prompts/co-scientist/original/06-evolution-feasibility.md) |
| 汇总评议 | Note 9.5，69 | [Meta-review](../agent-prompts/co-scientist/original/08-meta-review.md) |

改编说明：中文文档合并了评议、比较、改进和汇总职责，默认候选最多 3 个、改进一轮，并按任务需要继续；新增共同记录格式、实际证据要求和停止条件。它不要求复现 Elo 排名或全部调度细节。Supervisor 和 Proximity 没有单独公开提示词，本项目协调角色是依据方法编写。

## 3. ERA

- 项目与作者归属：Google Research；有版权头的文件注明 `Copyright 2026 Google LLC.`。
- [官方仓库及固定版本](https://github.com/google-research/era/tree/b836730b5c000526af95116b1d0e2c60c8cf0a10)。Commit：`b836730b5c000526af95116b1d0e2c60c8cf0a10`。
- [正式论文](https://www.nature.com/articles/s41586-026-10658-6)，DOI `10.1038/s41586-026-10658-6`。
- 主要源码：`implementation/llm.py` 第 17–25 行的代码角色模板，`implementation/playground_s3e1.py` 第 76–123 行的改进提示词，以及 `implementation/futs.py` 的候选选择方法。
- 本地：[代码角色原文](../agent-prompts/era/original/01-gemini-role-template.md)、[程序改进原文](../agent-prompts/era/original/02-program-improvement-template.md)、[职责与方法](../agent-prompts/era/roles.md)、[提取记录](../agent-prompts/era/manifest.json)。
- 许可：[Apache License 2.0](https://github.com/google-research/era/blob/b836730b5c000526af95116b1d0e2c60c8cf0a10/LICENSE)。保留原始源码与提取材料的版权声明和许可。

改编说明：将原来的模型 API 调用职责交给当前 agent；保留“已有代码—实际反馈—提出修改—运行并评分”的方法。通用角色不继承房价示例的函数名、禁用库或树数限制，它们由当前分析与执行环境决定。FUTS 是普通 Python 搜索算法，不是独立人格提示词；只有实际调用该程序时才报告使用了 FUTS。

## 4. 原始设计与本项目新增部分

- 本项目新增：当前 agent 技能入口、中文职责、按需角色安排、统一研究记录、执行命令的接入方式、实际结果保存及简明报告。
- 已提取的英文原文：[总目录](../agent-prompts/README.md)。`agent-prompts/` 中保存的来源与提取清单用于追查，不能因有这些文件就认定原服务已经完整安装。
