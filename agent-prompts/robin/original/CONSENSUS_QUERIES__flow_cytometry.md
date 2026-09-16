# CONSENSUS_QUERIES__flow_cytometry

**性质：官方代码中的提示词字符串，英文内容未改写。**

- 出处：[CONSENSUS_QUERIES['flow_cytometry']](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/prompts.py#L331-L362)
- 提交号：4a5cce310f3bc7663a67117db88af43b84733ffe
- 作者/来源：FutureHouse technical staff / Future-House/robin
- 许可：Apache-2.0，全文见 ../LICENSE。
- 提取方式：Python AST literal_eval；合并相邻字符串并还原源码转义，不执行原程序。
- 模板变量（仅供阅读）：无。
- 下面是替换变量前的字符串；不会自动调用原系统的检索或执行工具。

## 原文

~~~~text
Perform a meta-analysis on these analyses, consider what is a suitable method to combine the p values. The aim is to determine whether any drug treatment significantly increased Alexa Fluor 647 fluorescence compared to DMSO control. Note that there may be variations in naming of the control samples. 

Consider the range of average Alexa Fluor 647 intensity for each analysis and whether further processing is required for the values to be comparable across analyses.
Output a single CSV file named "consensus_results.csv", containing only the following columns: “drug”, “mean_intensity”, “std_error”.

Generate a barplot showing the average Alexa Fluor 647 fluorescence values for each drug treatment and DMSO control with error bars showing the standard error of the mean, use asterisks to denote significance on the plot. Remember to include DMSO control in the final bar plot.

~~~~
