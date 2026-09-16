# FOLLOWUP_CONTENT_MESSAGE

**性质：官方代码中的提示词字符串，英文内容未改写。**

- 出处：[FOLLOWUP_CONTENT_MESSAGE](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/prompts.py#L147-L178)
- 提交号：4a5cce310f3bc7663a67117db88af43b84733ffe
- 作者/来源：FutureHouse technical staff / Future-House/robin
- 许可：Apache-2.0，全文见 ../LICENSE。
- 提取方式：Python AST literal_eval；合并相邻字符串并还原源码转义，不执行原程序。
- 模板变量（仅供阅读）：analysis_summary, goal, mechanistic_insights, questions_raised。
- 下面是替换变量前的字符串；不会自动调用原系统的检索或执行工具。

## 原文

~~~~text

    Context: The overall research goal is "{goal}".

    An initial analysis of experimental data yielded the following:

    Analysis Summary:
    {analysis_summary}

    Potential Mechanistic Insights:
    {mechanistic_insights}

    Questions Raised:
    {questions_raised}

    Task: Based *only* on the summary and insights above, suggest if specific and valuable follow-up experiments, or output none if none are necessary.

    For each assay suggestion, provide a string of:
    Assay Name: The specific type of assay (e.g., 'RNA-seq', 'Flow Cytometry', 'Western Blot', 'High-Content Imaging', 'ELISA', 'qPCR', 'Co-Immunoprecipitation', 'Metabolomics'). Be specific.
    Reasoning: A concise scientific reason explaining *why* this specific assay is the logical next step to investigate the mechanisms, confirm findings, or address questions raised by the initial analysis summary and insights. Explain what specific question this assay will answer.

    If there are multiple assays suggested, separate the assay suggestions with two new lines.
    

~~~~
