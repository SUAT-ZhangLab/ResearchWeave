# 实验策略比较

**本文件是根据官方代码整理的中文角色说明，不是作者原有的角色 MD，也不代表一个独立常驻 agent。**

## 职责和方法

按源码给出的科学标准比较两份实验报告。

## 输入

疾病、两份报告、各自编号。

## 输出

包含胜者及理由的规定格式；随后由程序汇总排序。

## 使用哪些原始提示词

- [ASSAY_RANKING_SYSTEM_PROMPT](../original/ASSAY_RANKING_SYSTEM_PROMPT.md)
- [ASSAY_RANKING_PROMPT_FORMAT](../original/ASSAY_RANKING_PROMPT_FORMAT.md)
- [utils__user_prompt](../original/utils__user_prompt.md)

## 谁负责调用

[官方 robin/assays.py](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/assays.py) 负责组合这些提示词并调用服务。原文在 original/，变量填充与服务调用仍需要程序完成。
