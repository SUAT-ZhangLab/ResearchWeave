# 药物候选与机制假设提出

**本文件是根据官方代码整理的中文角色说明，不是作者原有的角色 MD，也不代表一个独立常驻 agent。**

## 职责和方法

利用已有报告提出候选药物和机制；可将实验反馈加入这一轮输入。

## 输入

疾病、候选数、文献结果、可选实验反馈。

## 输出

候选名称、假设与理由。

## 使用哪些原始提示词

- [CANDIDATE_GENERATION_SYSTEM_MESSAGE](../original/CANDIDATE_GENERATION_SYSTEM_MESSAGE.md)
- [CANDIDATE_GENERATION_USER_MESSAGE](../original/CANDIDATE_GENERATION_USER_MESSAGE.md)
- [EXPERIMENTAL_INSIGHTS_FOR_CANDIDATE_GENERATION](../original/EXPERIMENTAL_INSIGHTS_FOR_CANDIDATE_GENERATION.md)

## 谁负责调用

[官方 robin/candidates.py](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/candidates.py) 负责组合这些提示词并调用服务。原文在 original/，变量填充与服务调用仍需要程序完成。
