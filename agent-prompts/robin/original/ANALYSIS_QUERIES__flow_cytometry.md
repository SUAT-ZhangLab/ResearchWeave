# ANALYSIS_QUERIES__flow_cytometry

**性质：官方代码中的提示词字符串，英文内容未改写。**

- 出处：[ANALYSIS_QUERIES['flow_cytometry']](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/prompts.py#L279-L328)
- 提交号：4a5cce310f3bc7663a67117db88af43b84733ffe
- 作者/来源：FutureHouse technical staff / Future-House/robin
- 许可：Apache-2.0，全文见 ../LICENSE。
- 提取方式：Python AST literal_eval；合并相邻字符串并还原源码转义，不执行原程序。
- 模板变量（仅供阅读）：无。
- 下面是替换变量前的字符串；不会自动调用原系统的检索或执行工具。

## 原文

~~~~text
Analyze the .fcs files to measure Alexa Fluor 647 signal in live retinal pigment epithelial cells across different drug treatments.
Use the metadata file to match well positions  (e.g., A1) with their corresponding drug treatments and plate information.
Determine an appropriate gating strategy using a DMSO control well.

Start by using the flowMeans package to identify all of the clusters in the FCS vs SSC plot. Next, identify which cluster is most likely to contain the main cell population. 
Next, use a gating strategy to identify the live, singlet cell population from the clustered FCS vs SSC plot. Make the necessary plots to identify the required gating thresholds. Make sure to exclude all debris, and that the singlet gating is not too strict. Adjust the gating if the percentage gated population is too high or too low. Once you have the best gating strategy possible that gives reasonable percentage gated events, check the gating on the other two control wells to make sure comparable percentage gated events. If not, go back and adjust the strategy until the gating makes sense in all three control wells. Do not give up.

If there are multiple plates in the experiment, determine if there are plate-to-plate effect. If there is, take appropriate normalization steps using the DMSO control before downstream analysis. Make sure to keep each replicate separate after normalisation.

Determine if there are any drug treatments that significantly increased signal compared to DMSO control. Perform a suitable statistical test to compare the drug treatments to the DMSO control. Consider carefully the alternative hypothesis as we are only looking for an increase in signal, also consider multiple testing adjustment if necessary. 
Output only a single CSV file named “flow_results.csv”, containing only the following columns: “drug”, “mean_intensity”, “std_error”, “p_val”, “adj_p_val”. Include control labelled as “DMSO control” under the column “drug”. Do not include other columns in the CSV. 

Do not stop early. Make sure you have processed all files available. If you come across any errors, keep trying, do not give up until you completed the analysis.

~~~~
