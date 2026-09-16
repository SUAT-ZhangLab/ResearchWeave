# CANDIDATE_QUERY_GENERATION_CONTENT_MESSAGE

**性质：官方代码中的提示词字符串，英文内容未改写。**

- 出处：[CANDIDATE_QUERY_GENERATION_CONTENT_MESSAGE](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/prompts.py#L559-L589)
- 提交号：4a5cce310f3bc7663a67117db88af43b84733ffe
- 作者/来源：FutureHouse technical staff / Future-House/robin
- 许可：Apache-2.0，全文见 ../LICENSE。
- 提取方式：Python AST literal_eval；合并相邻字符串并还原源码转义，不执行原程序。
- 模板变量（仅供阅读）：candidate_generation_goal, disease_name, double_queries, num_queries。
- 下面是替换变量前的字符串；不会自动调用原系统的检索或执行工具。

## 原文

~~~~text
Return a list of {double_queries} queries (separated by <>) that would be useful in doing background research for the goal of {candidate_generation_goal}. 
These queries will be given to a highly-trained research team to investigate the scientific literature in depth, so the queries should be able to capture broadly relevant information (30+ words) and search relevant literature across 
biomedical, clinical, and biochemical literature about the disease or therapeutic landscape. You don't need to propose specific drugs, but the queries should be able to capture relevant scientific information that may help with proposing drug candidates. 
You have {double_queries} queries, so spread your queries out to cover as much ground as possible. Generate {num_queries} queries to cover literature about the therapeutic landscape, especially those that can help {candidate_generation_goal} and generate {num_queries} queries to cover literature about the biological and mechanistic aspects about {disease_name} itself. In formatting, don't number the queries, just output a string with {double_queries} queries separated by <>.

Generate queries for the goal of {candidate_generation_goal} that actively seek and prioritize:
*   **Target Validation:** Studies demonstrating the target pathway's dysregulation or causative role.
*   **Efficacy in Relevant Models:** Evidence of the drug candidate's efficacy in cell or animal models that *closely mimic* disease pathology, or in patient-derived cells. Prefer this over general mechanism-of-action studies.
*   **Mechanism Confirmation:** Studies confirming the candidate engages the target and modulates the specific pathway *as hypothesized* in a relevant biological system.
*   **Pharmacokinetics/Safety Data:** Existing data on the candidate's ADME properties, safety profile (especially human data), and known ability to reach relevant tissues.
~~~~
