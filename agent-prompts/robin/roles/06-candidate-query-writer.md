# 药物文献检索问题设计

**本文件是根据官方代码整理的中文角色说明，不是作者原有的角色 MD，也不代表一个独立常驻 agent。**

## 职责和方法

为药物候选提出检索问题；后续轮次可加入实验反馈。

## 输入

疾病、研究目标、检索问题数、可选实验解释。

## 输出

交给 Crow 的检索问题。

## 使用哪些原始提示词

- [CANDIDATE_QUERY_GENERATION_SYSTEM_MESSAGE](../original/CANDIDATE_QUERY_GENERATION_SYSTEM_MESSAGE.md)
- [CANDIDATE_QUERY_GENERATION_CONTENT_MESSAGE](../original/CANDIDATE_QUERY_GENERATION_CONTENT_MESSAGE.md)
- [EXPERIMENTAL_INSIGHTS_APPENDAGE](../original/EXPERIMENTAL_INSIGHTS_APPENDAGE.md)

## 谁负责调用

[官方 robin/candidates.py](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/candidates.py) 负责组合这些提示词并调用服务。原文在 original/，变量填充与服务调用仍需要程序完成。
