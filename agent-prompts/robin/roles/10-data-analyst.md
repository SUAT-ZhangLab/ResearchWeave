# 实验数据分析

**本文件是根据官方代码整理的中文角色说明，不是作者原有的角色 MD，也不代表一个独立常驻 agent。**

## 职责和方法

在 notebook 中读取数据、制定分析、运行计算并导出结果。

## 输入

数据文件与对应说明、分析类型、任务提示。

## 输出

CSV、notebook 等云端任务产物。

## 使用哪些原始提示词

- [COT](../original/COT.md)
- [GUIDELINE](../original/GUIDELINE.md)
- [ANALYSIS_QUERIES__flow_cytometry](../original/ANALYSIS_QUERIES__flow_cytometry.md)
- [ANALYSIS_QUERIES__RNA_seq](../original/ANALYSIS_QUERIES__RNA_seq.md)
- [analyses__analysis_prompt](../original/analyses__analysis_prompt.md)

## 谁负责调用

[官方 robin/analyses.py](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/analyses.py) 负责组合这些提示词并调用服务。原文在 original/，变量填充与服务调用仍需要程序完成。
