# EXPERIMENTAL_INSIGHTS_FOR_CANDIDATE_GENERATION

**性质：官方代码中的提示词字符串，英文内容未改写。**

- 出处：[EXPERIMENTAL_INSIGHTS_FOR_CANDIDATE_GENERATION](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/prompts.py#L649-L657)
- 提交号：4a5cce310f3bc7663a67117db88af43b84733ffe
- 作者/来源：FutureHouse technical staff / Future-House/robin
- 许可：Apache-2.0，全文见 ../LICENSE。
- 提取方式：Python AST literal_eval；合并相邻字符串并还原源码转义，不执行原程序。
- 模板变量（仅供阅读）：candidate_generation_goal, experimental_insights_analysis_summary, experimental_insights_mechanistic_insights, experimental_insights_questions_raised。
- 下面是替换变量前的字符串；不会自动调用原系统的检索或执行工具。

## 原文

~~~~text
Experimental tests have been conducted previously to {candidate_generation_goal}. Here is a summary of the results:
{experimental_insights_analysis_summary}.
Here are some mechanistic insights that may be relevant: {experimental_insights_mechanistic_insights}.
Here are some important questions that have been raised about the experimental results: {experimental_insights_questions_raised}.

~~~~
