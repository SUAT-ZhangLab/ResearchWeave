# ASSAY_LITERATURE_USER_MESSAGE

**性质：官方代码中的提示词字符串，英文内容未改写。**

- 出处：[ASSAY_LITERATURE_USER_MESSAGE](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/prompts.py#L374-L389)
- 提交号：4a5cce310f3bc7663a67117db88af43b84733ffe
- 作者/来源：FutureHouse technical staff / Future-House/robin
- 许可：Apache-2.0，全文见 ../LICENSE。
- 提取方式：Python AST literal_eval；合并相邻字符串并还原源码转义，不执行原程序。
- 模板变量（仅供阅读）：disease_name, num_queries。
- 下面是替换变量前的字符串；不会自动调用原系统的检索或执行工具。

## 原文

~~~~text
Return a list of {num_queries} queries (separated by <>) that would be useful in doing research to develop detailed, mechanistic cell culture assays that would be used to evaluate drugs to treat {disease_name}. 
These queries will be given to a 20-person scientific team to research in depth, so they should be able to capture broadly relevant information (30+ words) and search relevant literature across 
biomedical, clinical, and biochemical literature about the disease or therapeutic landscape. Don't look up specific drugs, but any relevant scientific information that may help with assay development. 
You have {num_queries} queries, so spread your queries out to cover as much ground as possible. Create queries both about the general biochemistry and mechanistic underpinnings of {disease_name} as well as about the assays.
In formatting, don't number the queries, just output a string with {num_queries} queries separated by <>.
~~~~
