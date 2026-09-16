# R_SPECIFIC_GUIDELINES

**性质：官方代码中的提示词字符串，英文内容未改写。**

- 出处：[R_SPECIFIC_GUIDELINES](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/prompts.py#L194-L224)
- 提交号：4a5cce310f3bc7663a67117db88af43b84733ffe
- 作者/来源：FutureHouse technical staff / Future-House/robin
- 许可：Apache-2.0，全文见 ../LICENSE。
- 提取方式：Python AST literal_eval；合并相邻字符串并还原源码转义，不执行原程序。
- 模板变量（仅供阅读）：无。
- 下面是替换变量前的字符串；不会自动调用原系统的检索或执行工具。

## 原文

~~~~text
Guidelines for using the R programming language:
1. Load packages using this format to minimize verbose output:
   ```r
   if (!requireNamespace("package_name", quietly = TRUE)) {{
     install.packages("package_name")
   }}
   suppressPackageStartupMessages(library(package_name))
   ```
2. You must use the tidyverse wherever possible: dplyr, tidyr, ggplot2, readr, stringr, forcats, purrr, tibble, and lubridate.

3. All plots must be made using ggplot2. Here is an example of how to make a plot:

   # Create a density scatter plot of FSC-A vs SSC-A
plot_data <- as.data.frame(dmso_data[, c("FSC-A", "SSC-A")])
scatter_plot <- ggplot2::ggplot(plot_data, ggplot2::aes(x = `FSC-A`, y = `SSC-A`)) +
  ggplot2::geom_hex(bins = 100) +
  ggplot2::scale_fill_viridis_c(trans = "log10") +
  ggplot2::labs(
    title = "FSC-A vs SSC-A Density Plot (DMSO Control)",
    x = "FSC-A",
    y = "SSC-A"
  ) +
  ggplot2::theme_minimal()

3. Use explicit namespace qualification for functions. For example, use dplyr::select() instead of select().

4. For data operations, suppress messages about column name repairs:
   ```r
   variable_name <- read_excel("<fpath>.csv", col_names = FALSE, .name_repair = "minimal")
   ```

~~~~
