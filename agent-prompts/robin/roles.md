# Robin：角色与原始提示词

**已提取 35 个原始字符串模板、3 个动态组合表达式，并整理14种任务职责和1份通用方法说明。**这些数量不是论文所称的agent数量；多数职责由同一配置的模型在不同步骤承担。

[原始代码 prompts.py](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/prompts.py)；[完整清单](manifest.json)；[提示组合方法](methods.md)。

## 按工作职责阅读

- [实验文献检索问题设计](roles/01-assay-query-writer.md)
- [实验策略设计](roles/02-assay-designer.md)
- [实验策略证据研究](roles/03-assay-evidence-researcher.md)
- [实验策略比较](roles/04-assay-reviewer.md)
- [候选研究目标整理](roles/05-objective-writer.md)
- [药物文献检索问题设计](roles/06-candidate-query-writer.md)
- [药物候选与机制假设提出](roles/07-candidate-generator.md)
- [候选药物证据研究](roles/08-candidate-evidence-researcher.md)
- [候选药物比较](roles/09-candidate-reviewer.md)
- [实验数据分析](roles/10-data-analyst.md)
- [多次分析结果汇总](roles/11-analysis-comparison.md)
- [实验结果解释](roles/12-data-interpreter.md)
- [后续实验建议](roles/13-followup-planner.md)
- [研究报告格式整理](roles/14-report-formatter.md)
- [Notebook 通用方法](roles/15-notebook-method.md)

## 什么被保留

original/ 保留英文提示词、占位符和原始格式要求；source/ 保存提取依据。字符串由AST静态读取，没有运行原系统。单个模板没有附带Crow/Falcon/Finch的服务内部提示、模型权重、可用工具或执行状态。

原文里的推理和输出要求属于作者模板，本次仅提取；并不承诺其他模型会以同样方式执行，也没有将其所有统计处理建议视为适用。

## 全部原始模板

| 名称 | 源码行 | 原文字符数 |
|---|---:|---:|
| [COT](original/COT.md) | 3 | 3113 |
| [GUIDELINE](original/GUIDELINE.md) | 63 | 1768 |
| [DATA_INTERPRETATION_SYSTEM_MESSAGE](original/DATA_INTERPRETATION_SYSTEM_MESSAGE.md) | 105 | 84 |
| [DATA_INTERPRETATION_CONTENT_MESSAGE](original/DATA_INTERPRETATION_CONTENT_MESSAGE.md) | 110 | 1650 |
| [FOLLOWUP_SYSTEM_MESSAGE](original/FOLLOWUP_SYSTEM_MESSAGE.md) | 139 | 419 |
| [FOLLOWUP_CONTENT_MESSAGE](original/FOLLOWUP_CONTENT_MESSAGE.md) | 147 | 1060 |
| [GENERAL_NOTEBOOK_GUIDELINES](original/GENERAL_NOTEBOOK_GUIDELINES.md) | 181 | 717 |
| [R_SPECIFIC_GUIDELINES](original/R_SPECIFIC_GUIDELINES.md) | 194 | 1212 |
| [CHAIN_OF_THOUGHT_AGNOSTIC](original/CHAIN_OF_THOUGHT_AGNOSTIC.md) | 226 | 2748 |
| [ANALYSIS_QUERIES__flow_cytometry](original/ANALYSIS_QUERIES__flow_cytometry.md) | 279 | 2174 |
| [ANALYSIS_QUERIES__RNA_seq](original/ANALYSIS_QUERIES__RNA_seq.md) | 279 | 772 |
| [CONSENSUS_QUERIES__flow_cytometry](original/CONSENSUS_QUERIES__flow_cytometry.md) | 331 | 882 |
| [CONSENSUS_QUERIES__RNA_seq](original/CONSENSUS_QUERIES__RNA_seq.md) | 331 | 781 |
| [ASSAY_LITERATURE_SYSTEM_MESSAGE](original/ASSAY_LITERATURE_SYSTEM_MESSAGE.md) | 367 | 223 |
| [ASSAY_LITERATURE_USER_MESSAGE](original/ASSAY_LITERATURE_USER_MESSAGE.md) | 374 | 938 |
| [ASSAY_PROPOSAL_SYSTEM_MESSAGE](original/ASSAY_PROPOSAL_SYSTEM_MESSAGE.md) | 392 | 1290 |
| [ASSAY_PROPOSAL_USER_MESSAGE](original/ASSAY_PROPOSAL_USER_MESSAGE.md) | 419 | 256 |
| [ASSAY_HYPOTHESIS_SYSTEM_PROMPT](original/ASSAY_HYPOTHESIS_SYSTEM_PROMPT.md) | 428 | 610 |
| [ASSAY_HYPOTHESIS_FORMAT](original/ASSAY_HYPOTHESIS_FORMAT.md) | 440 | 882 |
| [ASSAY_RANKING_SYSTEM_PROMPT](original/ASSAY_RANKING_SYSTEM_PROMPT.md) | 458 | 1186 |
| [ASSAY_RANKING_PROMPT_FORMAT](original/ASSAY_RANKING_PROMPT_FORMAT.md) | 478 | 1068 |
| [SYNTHESIZE_USER_CONTENT](original/SYNTHESIZE_USER_CONTENT.md) | 499 | 543 |
| [SYNTHESIZE_SYSTEM_MESSAGE_CONTENT](original/SYNTHESIZE_SYSTEM_MESSAGE_CONTENT.md) | 513 | 158 |
| [CANDIDATE_QUERY_GENERATION_SYSTEM_MESSAGE](original/CANDIDATE_QUERY_GENERATION_SYSTEM_MESSAGE.md) | 523 | 1355 |
| [EXPERIMENTAL_INSIGHTS_APPENDAGE](original/EXPERIMENTAL_INSIGHTS_APPENDAGE.md) | 548 | 391 |
| [CANDIDATE_QUERY_GENERATION_CONTENT_MESSAGE](original/CANDIDATE_QUERY_GENERATION_CONTENT_MESSAGE.md) | 559 | 1895 |
| [CANDIDATE_GENERATION_SYSTEM_MESSAGE](original/CANDIDATE_GENERATION_SYSTEM_MESSAGE.md) | 592 | 2960 |
| [CANDIDATE_GENERATION_USER_MESSAGE](original/CANDIDATE_GENERATION_USER_MESSAGE.md) | 642 | 251 |
| [EXPERIMENTAL_INSIGHTS_FOR_CANDIDATE_GENERATION](original/EXPERIMENTAL_INSIGHTS_FOR_CANDIDATE_GENERATION.md) | 649 | 391 |
| [CANDIDATE_LIT_REVIEW_DIRECTION_PROMPT](original/CANDIDATE_LIT_REVIEW_DIRECTION_PROMPT.md) | 659 | 595 |
| [CANDIDATE_REPORT_FORMAT](original/CANDIDATE_REPORT_FORMAT.md) | 671 | 1272 |
| [CANDIDATE_RANKING_SYSTEM_PROMPT](original/CANDIDATE_RANKING_SYSTEM_PROMPT.md) | 691 | 5140 |
| [CANDIDATE_RANKING_PROMPT_FORMAT](original/CANDIDATE_RANKING_PROMPT_FORMAT.md) | 762 | 1079 |
| [FINAL_REPORT_FORMATTING_USER_MESSAGE](original/FINAL_REPORT_FORMATTING_USER_MESSAGE.md) | 785 | 2816 |
| [FINAL_REPORT_FORMATTING_SYSTEM_MESSAGE](original/FINAL_REPORT_FORMATTING_SYSTEM_MESSAGE.md) | 832 | 111 |
| [utils__user_prompt](original/utils__user_prompt.md) | 600 | 动态表达式 |
| [analyses__analysis_prompt](original/analyses__analysis_prompt.md) | 34 | 动态表达式 |
| [analyses__consensus_prompt](original/analyses__consensus_prompt.md) | 43 | 动态表达式 |
