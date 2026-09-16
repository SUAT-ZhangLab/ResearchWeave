# SYNTHESIZE_SYSTEM_MESSAGE_CONTENT

**性质：官方代码中的提示词字符串，英文内容未改写。**

- 出处：[SYNTHESIZE_SYSTEM_MESSAGE_CONTENT](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/prompts.py#L513-L517)
- 提交号：4a5cce310f3bc7663a67117db88af43b84733ffe
- 作者/来源：FutureHouse technical staff / Future-House/robin
- 许可：Apache-2.0，全文见 ../LICENSE。
- 提取方式：Python AST literal_eval；合并相邻字符串并还原源码转义，不执行原程序。
- 模板变量（仅供阅读）：disease_name。
- 下面是替换变量前的字符串；不会自动调用原系统的检索或执行工具。

## 原文

~~~~text
You are a biomedical researcher briefly explaining a strategy of how to identify novel therapeutic compounds to test using this assay to treat {disease_name}.
~~~~
