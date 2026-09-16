# 后续实验建议

**本文件是根据官方代码整理的中文角色说明，不是作者原有的角色 MD，也不代表一个独立常驻 agent。**

## 职责和方法

根据结果总结、问题和机制线索判断是否值得继续实验。

## 输入

goal、analysis_summary、mechanistic_insights、questions_raised。

## 输出

实验名称和简明科学理由；无必要时允许不提出新实验。

## 使用哪些原始提示词

- [FOLLOWUP_SYSTEM_MESSAGE](../original/FOLLOWUP_SYSTEM_MESSAGE.md)
- [FOLLOWUP_CONTENT_MESSAGE](../original/FOLLOWUP_CONTENT_MESSAGE.md)

## 谁负责调用

[官方 robin/analyses.py](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/analyses.py) 负责组合这些提示词并调用服务。原文在 original/，变量填充与服务调用仍需要程序完成。
