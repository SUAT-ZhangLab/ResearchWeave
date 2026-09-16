# 候选药物证据研究

**本文件是根据官方代码整理的中文角色说明，不是作者原有的角色 MD，也不代表一个独立常驻 agent。**

## 职责和方法

为单个候选查找和整理更详细的科学依据。

## 输入

疾病、候选药物与假设、报告格式。

## 输出

由 Falcon 返回的候选报告。

## 使用哪些原始提示词

- [CANDIDATE_LIT_REVIEW_DIRECTION_PROMPT](../original/CANDIDATE_LIT_REVIEW_DIRECTION_PROMPT.md)
- [CANDIDATE_REPORT_FORMAT](../original/CANDIDATE_REPORT_FORMAT.md)

## 谁负责调用

[官方 robin/candidates.py](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/candidates.py) 负责组合这些提示词并调用服务。原文在 original/，变量填充与服务调用仍需要程序完成。
