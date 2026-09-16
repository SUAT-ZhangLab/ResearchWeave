# CANDIDATE_RANKING_PROMPT_FORMAT

**性质：官方代码中的提示词字符串，英文内容未改写。**

- 出处：[CANDIDATE_RANKING_PROMPT_FORMAT](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/prompts.py#L762-L780)
- 提交号：4a5cce310f3bc7663a67117db88af43b84733ffe
- 作者/来源：FutureHouse technical staff / Future-House/robin
- 许可：Apache-2.0，全文见 ../LICENSE。
- 提取方式：Python AST literal_eval；合并相邻字符串并还原源码转义，不执行原程序。
- 模板变量（仅供阅读）：无。
- 下面是替换变量前的字符串；不会自动调用原系统的检索或执行工具。

## 原文

~~~~text
Evaluate the preclinical drug candidate data package using the structure below. This evaluation informs a critical decision.

**Respond ONLY in the specified JSON format, do not include any text outside the JSON object itself.**

{{
    "Analysis": {"type": "string", "description": "[Provide a detailed analysis of the two drug candidates, based on the evaluation criteria and the evidence provided.]"},
    "Reasoning": {"type": "string", "description": "[Choose which drug candidate is better. Provide a detailed explanation for why you think the winner is better than the loser, based on the evaluation criteria and the evidence provided.]"},
    "Winner": {"type": "string", "description": "[Return the name and ID number of the candidate that you think is better between the two candidates, as a tuple. It should be formatted as (winner_name, winner_id)]"},
    "Loser": {"type": "string", "description": "[Return the name and ID number of the candidate that you think is worse between the two candidates, as a tuple. It should be formatted as (loser_name, loser_id)]"},
}}
~~~~
