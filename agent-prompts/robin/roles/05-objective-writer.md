# 候选研究目标整理

**本文件是根据官方代码整理的中文角色说明，不是作者原有的角色 MD，也不代表一个独立常驻 agent。**

## 职责和方法

把优先实验策略整理为后续药物候选生成目标。

## 输入

疾病、选中的实验策略。

## 输出

candidate_generation_goal 文本。

## 使用哪些原始提示词

- [SYNTHESIZE_SYSTEM_MESSAGE_CONTENT](../original/SYNTHESIZE_SYSTEM_MESSAGE_CONTENT.md)
- [SYNTHESIZE_USER_CONTENT](../original/SYNTHESIZE_USER_CONTENT.md)

## 谁负责调用

[官方 robin/assays.py](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/assays.py) 负责组合这些提示词并调用服务。原文在 original/，变量填充与服务调用仍需要程序完成。
