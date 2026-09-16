# 多次分析结果汇总

**本文件是根据官方代码整理的中文角色说明，不是作者原有的角色 MD，也不代表一个独立常驻 agent。**

## 职责和方法

读取同一批数据的多次分析结果，按公开提示组织汇总。

## 输入

多次分析输出、分析类型。

## 输出

汇总结果 CSV。

## 使用哪些原始提示词

- [COT](../original/COT.md)
- [GUIDELINE](../original/GUIDELINE.md)
- [CONSENSUS_QUERIES__flow_cytometry](../original/CONSENSUS_QUERIES__flow_cytometry.md)
- [CONSENSUS_QUERIES__RNA_seq](../original/CONSENSUS_QUERIES__RNA_seq.md)
- [analyses__consensus_prompt](../original/analyses__consensus_prompt.md)

## 谁负责调用

[官方 robin/analyses.py](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/analyses.py) 负责组合这些提示词并调用服务。原文在 original/，变量填充与服务调用仍需要程序完成。

源码的汇总提示保留了合并 P 值等原始做法。它没有被本次提取修改；多次计算使用同一批样本，不会新增独立生物学重复。实际使用时须结合实验设计判断是否采用。
