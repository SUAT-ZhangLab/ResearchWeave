# GENERAL_NOTEBOOK_GUIDELINES

来源：[Finch / src/fhda/prompts.py 第 62–73 行](https://github.com/Future-House/finch/blob/aea66fdf2dd2be827727de50a73cae60dff59972/src/fhda/prompts.py#L62-L73)。

许可：Apache-2.0，完整许可证在 `../original/LICENSE`。

下方为公开源码中的字符串值。f-string 中引用的固定文本已按源码展开，任务变量保留原样。未翻译或修改正文；Markdown 标题和说明为本次添加。

````text

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
````
