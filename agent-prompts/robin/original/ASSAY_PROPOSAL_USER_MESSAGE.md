# ASSAY_PROPOSAL_USER_MESSAGE

**性质：官方代码中的提示词字符串，英文内容未改写。**

- 出处：[ASSAY_PROPOSAL_USER_MESSAGE](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/prompts.py#L419-L425)
- 提交号：4a5cce310f3bc7663a67117db88af43b84733ffe
- 作者/来源：FutureHouse technical staff / Future-House/robin
- 许可：Apache-2.0，全文见 ../LICENSE。
- 提取方式：Python AST literal_eval；合并相邻字符串并还原源码转义，不执行原程序。
- 模板变量（仅供阅读）：assay_lit_review_output, disease_name, num_assays。
- 下面是替换变量前的字符串；不会自动调用原系统的检索或执行工具。

## 原文

~~~~text
Generate exactly **{num_assays}** distinct and scientifically rigorous proposals for cell culture assays that can evaluate drugs to treat {disease_name}. Here is some relevant background information that can guide your proposals:
{assay_lit_review_output}

~~~~
