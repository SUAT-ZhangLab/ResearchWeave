# ANALYSIS_QUERIES__RNA_seq

**性质：官方代码中的提示词字符串，英文内容未改写。**

- 出处：[ANALYSIS_QUERIES['RNA_seq']](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/prompts.py#L279-L328)
- 提交号：4a5cce310f3bc7663a67117db88af43b84733ffe
- 作者/来源：FutureHouse technical staff / Future-House/robin
- 许可：Apache-2.0，全文见 ../LICENSE。
- 提取方式：Python AST literal_eval；合并相邻字符串并还原源码转义，不执行原程序。
- 模板变量（仅供阅读）：无。
- 下面是替换变量前的字符串；不会自动调用原系统的检索或执行工具。

## 原文

~~~~text
Determine the effect of the treatment in the context of this data. 

Perform differential expression analysis and pathway analysis on relevant comparison groups. Map all gene IDs to gene symbols using annotation package such as 'org.Hs.eg.db'.

Generate volcano plots and heatmap of differentially expressed genes, and dot plots for enriched pathways, use gene symbols for labels where relevant.

Output a single csv file named "dea_results.csv"  with the results for all tested genes of the most relevant contrast, report both gene ID and gene symbol.

If there is an error, keep trying, do not give up until you reach the end of the analysis. When mapping gene ID to gene symbol, consider all possible forms of gene IDs, keep trying until the gene symbols are obtained.

~~~~
