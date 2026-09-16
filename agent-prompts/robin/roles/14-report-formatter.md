# 研究报告格式整理

**本文件是根据官方代码整理的中文角色说明，不是作者原有的角色 MD，也不代表一个独立常驻 agent。**

## 职责和方法

将代理返回的正文和来源整理成规定格式。

## 输入

answer_text、sources_text。

## 输出

格式统一的报告。

## 使用哪些原始提示词

- [FINAL_REPORT_FORMATTING_SYSTEM_MESSAGE](../original/FINAL_REPORT_FORMATTING_SYSTEM_MESSAGE.md)
- [FINAL_REPORT_FORMATTING_USER_MESSAGE](../original/FINAL_REPORT_FORMATTING_USER_MESSAGE.md)

## 谁负责调用

[官方 robin/utils.py](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/utils.py) 负责组合这些提示词并调用服务。原文在 original/，变量填充与服务调用仍需要程序完成。
