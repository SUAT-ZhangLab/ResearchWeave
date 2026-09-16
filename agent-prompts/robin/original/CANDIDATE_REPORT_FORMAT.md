# CANDIDATE_REPORT_FORMAT

**性质：官方代码中的提示词字符串，英文内容未改写。**

- 出处：[CANDIDATE_REPORT_FORMAT](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/prompts.py#L671-L689)
- 提交号：4a5cce310f3bc7663a67117db88af43b84733ffe
- 作者/来源：FutureHouse technical staff / Future-House/robin
- 许可：Apache-2.0，全文见 ../LICENSE。
- 提取方式：Python AST literal_eval；合并相邻字符串并还原源码转义，不执行原程序。
- 模板变量（仅供阅读）：disease_name。
- 下面是替换变量前的字符串；不会自动调用原系统的检索或执行工具。

## 原文

~~~~text
Provide your response in the following format, like an evaluation for a scientific proposal:
Overview of Therapeutic Candidate: Explain the natural or synthetic origins of this therapeutic candidate, including how it was synthesized or discovered. Explain which class of therapeutic compounds this belongs to, and how this class of compounds has previously been used in general. 
Therapeutic History: Summarize previous biochemical, clinical or veterinary uses of this drug or drug class, if any. Examine to see if the therapeutic candidate has ever been used for treating {disease_name} or any similar disease.
Mechanism of Action: Explain the known mechanism(s) of action of this compound to the full extent of molecular detail that is known. Explain the biochemistry and molecular interactions of the therapeutic candidate in any relevant literature.
Expected Effect: Explain the expected effect of this compound in the assay proposed and the mechanism by which it will act. If the drug is acting on proteins, reference literature which shows this gene is expressed in the cell type being assayed.  
Overall Evaluation: Give your overall thoughts on this therapeutic candidate. Include strengths and weaknesses of this therapeutic candidate for treating {disease_name}.
~~~~
