# ASSAY_HYPOTHESIS_FORMAT

**性质：官方代码中的提示词字符串，英文内容未改写。**

- 出处：[ASSAY_HYPOTHESIS_FORMAT](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/prompts.py#L440-L455)
- 提交号：4a5cce310f3bc7663a67117db88af43b84733ffe
- 作者/来源：FutureHouse technical staff / Future-House/robin
- 许可：Apache-2.0，全文见 ../LICENSE。
- 提取方式：Python AST literal_eval；合并相邻字符串并还原源码转义，不执行原程序。
- 模板变量（仅供阅读）：disease_name。
- 下面是替换变量前的字符串；不会自动调用原系统的检索或执行工具。

## 原文

~~~~text
Provide your response in the following format, like an evaluation for a scientific proposal:
Assay Overview: Explain the assay idea, including the following key points: which aspect of the disease pathogenesis does the assay model, what measurements will be taken from the assay and how they will be taken, which cells or other biological material are used in the assay. 
Biomedical Evidence: Make a compelling argument for how the aspect of the disease represented in the assay is central to the pathogenesis of the disease. Make sure to consider both the biomedical and clinical literature. 
Previous Use: Explain how this assay has previously been used for drug discovery (if this has been done). Explain any key scientific discoveries which have been made using this assay. 
Overall Evaluation: Strengths and weaknesses of this assay for testing therapeutics for {disease_name}.
~~~~
