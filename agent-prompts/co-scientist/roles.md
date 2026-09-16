# Co-Scientist：角色、方法与公开提示词

**Co-Scientist 是由多个 agent 协作的系统。可以把 agent 理解为：有明确职责、获得指定材料、按要求使用模型或工具，并把结果交给其他角色的工作单元。**角色的差别主要在任务、处理方法和输出要求。

这里提取的是作者正式发表在论文补充材料中的提示词。原材料是 PDF，并没有公开一个由这些 Markdown 文件构成的官方软件目录。本目录将英文原文转换成 MD，便于阅读和复用。

## 已经提取了什么

- **8 份逐任务提示词**：对应 Generation、Reflection、Ranking、Evolution、Meta-review 五种角色。
- **完整 Note 9**：便于对照八份拆分文件。
- **完整 Note 8 伪代码**：描述 Supervisor 和六种专门角色如何协作。
- 官方补充 PDF、原始文字提取结果、来源与 SHA256 记录、可重复运行的提取脚本。

**完整源码尚未公开，公开提示词可以获取。这是两件不同的事。**这些是论文报告的公开研究模板；它们不能证明当前在线服务仍逐字使用相同模板，也不代表在线服务的全部内部指令。[论文 Code availability](https://www.nature.com/articles/s41586-026-10644-y#code-availability)

## 各个 agent 怎么工作

下表是依据论文方法和 Note 8–9 整理的中文说明，**不是官方提示词原文**。

| 角色 | 输入 | 主要处理 | 输出 | 本次可获取的原材料 |
|---|---|---|---|---|
| Supervisor：安排工作 | 研究目标、已完成任务、运行状态 | 把目标整理成研究计划；安排各角色；新假设交给 Reflection，评价完成后交给 Ranking；按运行情况继续比较、改进或总结 | 研究计划、待执行任务、更新后的共享记录 | Note 8，PDF 第 56–57 页；Note 9 没有单独提示词 |
| Generation：提出假设 | 目标、评价要求、已读文献与分析、已有假设或讨论记录 | 从文献提出具体解释，或者模拟专家讨论；讨论中比较、追问和改进候选 | 具有具体对象、机制和预期结果的假设 | 两份模板，PDF 第 62–64 页 |
| Reflection：检查假设 | 假设、相关文献或观察 | 整体方法包括检索证据、检查新颖性与正确性、逐项检查关键假定；本次公开模板专门判断假设能否解释文章观察、是否有更好的解释或反证 | 评价意见、关键问题；该模板输出五类判断之一 | 一份观察分析模板，PDF 第 64–65 页；整体方法另见 Note 8 |
| Ranking：比较假设 | 两个假设、各自评价、目标和比较标准 | 直接比较，或模拟专家讨论后选出一个；程序根据比较结果更新 Elo 相对分数 | 胜出候选、比较理由、更新后的相对排名 | 两份模板，PDF 第 65–67 页 |
| Evolution：改进假设 | 已有假设、目标和评价要求 | 一类任务将方案改得更容易实际检验；另一类任务借鉴其他方案的原理，提出不同的新假设 | 改进或新提出的假设，随后再接受评价和比较 | 两份模板，PDF 第 67–68 页 |
| Proximity：判断思路相近程度 | 已有假设集合 | Note 8 描述逐对计算相似度，例如将文本转换为表示其含义的数值后比较，并更新假设关系图 | 相似度和假设关系 | Note 8，PDF 第 60 页；Note 9 没有单独提示词 |
| Meta-review：汇总评价 | 各候选的评价、比较讨论、研究目标及要求 | 找出反复出现的优点和问题，形成改进建议；另可根据优先候选组织研究概览 | 总体建议或研究概览 | 一份评价汇总模板，PDF 第 69 页；概览生成另见 Note 8 |

Elo 是通过两两比较更新的相对分数。它表示系统内部对方案的评价，不是实验成功概率。

## 8 份英文提示词

| 文件 | 用途 | 必要输入中的重点 |
|---|---|---|
| [01-generation-literature-review.md](original/01-generation-literature-review.md) | 读完文献后形成假设 | `{goal}`、`{preferences}`、`{articles_with_reasoning}`；后者应当是实际阅读得到的材料 |
| [02-generation-scientific-debate.md](original/02-generation-scientific-debate.md) | 在模拟专家讨论中提出和完善假设 | `{idea_attributes}`、`{reviews_overview}`、`{transcript}` |
| [03-reflection-observations.md](original/03-reflection-observations.md) | 对照文章观察，判断假设能否提供新的因果解释 | `{article}`、`{hypothesis}` |
| [04-ranking-comparison.md](original/04-ranking-comparison.md) | 直接比较两个假设 | 两个假设、各自评价、`{preferences}`、`{notes}` |
| [05-ranking-scientific-debate.md](original/05-ranking-scientific-debate.md) | 经模拟讨论比较两个假设 | 两个假设及评价、目标、标准和备注 |
| [06-evolution-feasibility.md](original/06-evolution-feasibility.md) | 改进实际可行性 | `{hypothesis}`、`{goal}`、`{preferences}` |
| [07-evolution-out-of-the-box.md](original/07-evolution-out-of-the-box.md) | 借鉴已有方案，形成一个不同的新假设 | `{hypotheses}`、`{goal}`、`{preferences}` |
| [08-meta-review.md](original/08-meta-review.md) | 汇总评价中的共性问题和建议 | `{reviews}`、`{goal}`、`{preferences}`、`{instructions}` |

[完整提示词 Note 9](original/00-all-published-prompts.md) · [工作安排与各角色方法 Note 8](original/00-orchestration-pseudocode.md) · [官方 PDF](source/41586_2026_10644_MOESM1_ESM.pdf)

## 如何复用

1. 按需要选择一份 MD，取其中 `text` 代码块里的原文。
2. 填入花括号字段。文献内容、其他 agent 输出和讨论记录需要由调用程序提供。
3. 把填写后的内容交给模型，并为该任务提供实际需要的检索等工具。
4. 若要重复比较和改进，需要另写程序保存假设、评价与分数，安排下一轮任务。单独复制一份提示词只能执行该任务。

**保留了原文中的不一致，未擅自改写：**直接排序模板同时使用 `better idea` 和 `better hypothesis` 两种结尾要求；字段中有 `{review1}`、`{review 1}`、`{review 2}` 等不同写法；Reflection 最后一行的括号不匹配。自行接入程序时，应在单独的改编副本里统一字段和输出格式，不要把修改后的内容继续标成原文。

原文中的 `meta-analysis` 在该模板里指汇总模型评价意见；这份模板本身不执行统计学荟萃分析。

## 提取方式与来源

提取日期：2026-09-15。页码使用 **PDF 物理页码，封面算第 1 页**。

- 作者：Juraj Gottweis、Wei-Hung Weng、Alexander Daryin 等。
- 论文：[Accelerating scientific discovery with Co-Scientist](https://www.nature.com/articles/s41586-026-10644-y)，Nature 655, 487–496 (2026)。DOI：10.1038/s41586-026-10644-y。
- 官方文件：[Supplementary Information](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-026-10644-y/MediaObjects/41586_2026_10644_MOESM1_ESM.pdf)。Note 8 在第 56–61 页；Note 9 在第 62–69 页。
- 许可：[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。论文 Rights and permissions 授权复制、分享和改编，并要求保留作者与来源、许可链接和修改说明。Note 8–9 未发现另列的限制性版权说明。
- 转换：使用 pypdf 6.18.1 的 layout 模式读取 PDF 文字。完整 Note 文件保留 PDF 中显示的 `None` 标签；独立提示词删除该标签及分页，去除共同左侧缩进。没有翻译、补写或修复原文内容。
- PDF 转文字可能改变换行、跨页缩进或复杂表格的阅读顺序；本次提示词按 Note 9 的标题及英文起止位置拆分，跨页提示词已检查连续性。需要确认原版排版时，以保存的 PDF 为准。

[manifest.json](manifest.json) 保存来源、版本、页码、变量和内容指纹。[原始提取文字](source/supplementary-extracted-layout.txt) 可用于检查拆分结果。[提取脚本](scripts/extract_prompts.py) 可重新生成八份模板、完整 Note 文件和 manifest；运行环境只在本目录 `.extraction-deps` 添加 pypdf，没有修改 ERA 环境的依赖。
