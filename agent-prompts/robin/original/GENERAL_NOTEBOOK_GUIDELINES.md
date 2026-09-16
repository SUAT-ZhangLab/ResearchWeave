# GENERAL_NOTEBOOK_GUIDELINES

**性质：官方代码中的提示词字符串，英文内容未改写。**

- 出处：[GENERAL_NOTEBOOK_GUIDELINES](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/prompts.py#L181-L192)
- 提交号：4a5cce310f3bc7663a67117db88af43b84733ffe
- 作者/来源：FutureHouse technical staff / Future-House/robin
- 许可：Apache-2.0，全文见 ../LICENSE。
- 提取方式：Python AST literal_eval；合并相邻字符串并还原源码转义，不执行原程序。
- 模板变量（仅供阅读）：language。
- 下面是替换变量前的字符串；不会自动调用原系统的检索或执行工具。

## 原文

~~~~text

General Guidelines:
- Write small to medium-sized cells for easier debugging.
- Edit existing cells by their index number when fixing bugs, rather than creating new ones.
- Check dataframe shapes before printing. Use head() for large dataframes.
- Ensure each cell executes successfully before moving to the next.
- Assume you already have the packages you need installed and only install new ones if you receive errors.
- If you need to install packages, use pip or mamba.
- All cells are by default {language} cells. Use {language} or bash tools for all analysis.
- You can use bash cells by adding %%bash to the first line of the cell or running a subprocess.
- You can only create code cells, no markdown cells.

~~~~
