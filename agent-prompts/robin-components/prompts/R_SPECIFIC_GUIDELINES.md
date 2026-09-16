# R_SPECIFIC_GUIDELINES

来源：[Finch / src/fhda/prompts.py 第 28–58 行](https://github.com/Future-House/finch/blob/aea66fdf2dd2be827727de50a73cae60dff59972/src/fhda/prompts.py#L28-L58)。

许可：Apache-2.0，完整许可证在 `../original/LICENSE`。

下方为公开源码中的字符串值。f-string 中引用的固定文本已按源码展开，任务变量保留原样。未翻译或修改正文；Markdown 标题和说明为本次添加。

````text
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
````
