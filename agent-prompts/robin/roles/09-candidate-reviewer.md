# 候选药物比较

**本文件是根据官方代码整理的中文角色说明，不是作者原有的角色 MD，也不代表一个独立常驻 agent。**

## 职责和方法

依据提示词中的标准逐对比较候选报告。

## 输入

疾病、两份候选报告及编号。

## 输出

比较理由和胜者；程序据此计算相对排名。

## 使用哪些原始提示词

- [CANDIDATE_RANKING_SYSTEM_PROMPT](../original/CANDIDATE_RANKING_SYSTEM_PROMPT.md)
- [CANDIDATE_RANKING_PROMPT_FORMAT](../original/CANDIDATE_RANKING_PROMPT_FORMAT.md)
- [utils__user_prompt](../original/utils__user_prompt.md)

## 谁负责调用

[官方 robin/candidates.py](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/candidates.py) 负责组合这些提示词并调用服务。原文在 original/，变量填充与服务调用仍需要程序完成。
