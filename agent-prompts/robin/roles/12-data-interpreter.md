# 实验结果解释

**本文件是根据官方代码整理的中文角色说明，不是作者原有的角色 MD，也不代表一个独立常驻 agent。**

## 职责和方法

将实际数据结果与研究目标放在一起，整理发现、问题和机制线索。

## 输入

goal、data_html。

## 输出

以 <> 分开的药物列表、结果总结、新问题和机制线索。

## 使用哪些原始提示词

- [DATA_INTERPRETATION_SYSTEM_MESSAGE](../original/DATA_INTERPRETATION_SYSTEM_MESSAGE.md)
- [DATA_INTERPRETATION_CONTENT_MESSAGE](../original/DATA_INTERPRETATION_CONTENT_MESSAGE.md)

## 谁负责调用

[官方 robin/analyses.py](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/analyses.py) 负责组合这些提示词并调用服务。原文在 original/，变量填充与服务调用仍需要程序完成。
