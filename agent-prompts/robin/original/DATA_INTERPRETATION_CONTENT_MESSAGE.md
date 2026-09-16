# DATA_INTERPRETATION_CONTENT_MESSAGE

**性质：官方代码中的提示词字符串，英文内容未改写。**

- 出处：[DATA_INTERPRETATION_CONTENT_MESSAGE](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/prompts.py#L110-L136)
- 提交号：4a5cce310f3bc7663a67117db88af43b84733ffe
- 作者/来源：FutureHouse technical staff / Future-House/robin
- 许可：Apache-2.0，全文见 ../LICENSE。
- 提取方式：Python AST literal_eval；合并相邻字符串并还原源码转义，不执行原程序。
- 模板变量（仅供阅读）：data_html, goal。
- 下面是替换变量前的字符串；不会自动调用原系统的检索或执行工具。

## 原文

~~~~text
You are an expert biochemist. Review the following experimental data in the context of the research goal: "{goal}".
Data:
{data_html}

Your task is to extract meaningful information to guide future hypothesis generation. Please provide four answers:
1.  **List of drugs tested in data:** List out all the drugs tested in this dataset.
2.  **Summary of Key Findings and Insights:** Concisely summarize the main trends, significant results (e.g., top performers, ineffective treatments), or patterns observed in the data that are directly relevant to the research goal. Focus on comparisons and magnitudes.
3.  **Specific Questions Raised:** Based *only* on this data and the research goal, list specific, answerable scientific questions that arise. These questions might guide further literature searches or experimental design. If the data is clear and raises no questions, state that clearly.
4.  **Mechanistic Insights:** What are the key biological or biochemical mechanisms suggested by the data? What are the potential biological pathways or processes that explain the observed results, with respect to the research goal?

Format your response in a string, separating each of the four answers with <>. The **List of drugs tested in data** should be in a comma separated string. Then there should be a <>. The **Summary of Key Findings and Insights** should be in a single paragraph. Then there should be a <>. **Specific Questions Raised** should be in a numbered list, with each question separated by a new line. Then there should be a <>. Finally, **Mechanistic Insights** should be a bulleted list, with each insight separated by a new line.

~~~~
