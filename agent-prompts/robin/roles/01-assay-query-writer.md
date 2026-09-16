# 实验文献检索问题设计

**本文件是根据官方代码整理的中文角色说明，不是作者原有的角色 MD，也不代表一个独立常驻 agent。**

## 职责和方法

根据疾病名称提出能够帮助选择实验的检索问题。

## 输入

疾病、检索问题数、预期实验数。

## 输出

检索问题文本；随后由 Crow 执行检索。

## 使用哪些原始提示词

- [ASSAY_LITERATURE_SYSTEM_MESSAGE](../original/ASSAY_LITERATURE_SYSTEM_MESSAGE.md)
- [ASSAY_LITERATURE_USER_MESSAGE](../original/ASSAY_LITERATURE_USER_MESSAGE.md)

## 谁负责调用

[官方 robin/assays.py](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/assays.py) 负责组合这些提示词并调用服务。原文在 original/，变量填充与服务调用仍需要程序完成。
