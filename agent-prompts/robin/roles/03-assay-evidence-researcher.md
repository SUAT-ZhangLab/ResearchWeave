# 实验策略证据研究

**本文件是根据官方代码整理的中文角色说明，不是作者原有的角色 MD，也不代表一个独立常驻 agent。**

## 职责和方法

围绕单个实验策略形成较完整的文献报告。

## 输入

疾病、单个实验策略、报告要求。

## 输出

由 Crow 返回的研究报告。

## 使用哪些原始提示词

- [ASSAY_HYPOTHESIS_SYSTEM_PROMPT](../original/ASSAY_HYPOTHESIS_SYSTEM_PROMPT.md)
- [ASSAY_HYPOTHESIS_FORMAT](../original/ASSAY_HYPOTHESIS_FORMAT.md)

## 谁负责调用

[官方 robin/assays.py](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/assays.py) 负责组合这些提示词并调用服务。原文在 original/，变量填充与服务调用仍需要程序完成。
