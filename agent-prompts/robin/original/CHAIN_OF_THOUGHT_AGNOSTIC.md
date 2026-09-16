# CHAIN_OF_THOUGHT_AGNOSTIC

**性质：官方代码中的提示词字符串，英文内容未改写。**

- 出处：[CHAIN_OF_THOUGHT_AGNOSTIC](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/prompts.py#L226-L276)
- 提交号：4a5cce310f3bc7663a67117db88af43b84733ffe
- 作者/来源：FutureHouse technical staff / Future-House/robin
- 许可：Apache-2.0，全文见 ../LICENSE。
- 提取方式：Python AST literal_eval；合并相邻字符串并还原源码转义，不执行原程序。
- 模板变量（仅供阅读）：language。
- 下面是替换变量前的字符串；不会自动调用原系统的检索或执行工具。

## 原文

~~~~text

Follow these steps to create your notebook, using chain-of-thought reasoning at each stage:

1. Load Data and Perform Descriptive Statistics:
<analysis_planning>
- Identify which data files are most relevant to resolving the task.
- Plan how to load these files efficiently in {language}.
- List the specific descriptive statistics you plan to use (e.g., summary(), str(), head()).
- Consider potential issues like missing data or unexpected formats. How will you handle each?
- Plan how to present this information clearly in the notebook.
- Write down key statistics you expect to see and how you'll interpret them.
- Consider potential data quality issues and how you'll address them.
</analysis_planning>
Execute your plan to load data and perform descriptive statistics.

2. Develop Analysis Plan:
<analysis_planning>
- Break down each task into testable components. List these components.
- For each component, list appropriate statistical tests or visualizations.
- Consider alternative approaches for each component and justify your choices.
- Identify potential confounding factors and how to address them.
- Plan the sequence of your analysis steps, explaining the rationale for each.
- Consider how this analysis plan will be documented in the notebook.
- List potential statistical assumptions for your chosen methods and how you'll test them.
- Think about how your analysis plan addresses your original task.
</analysis_planning>
Write out your analysis plan as comments in the notebook.

3. Execute Analysis Plan:
<analysis_planning>
- For each step in your analysis plan, list the {language} or bash functions and libraries you'll use.
- Think about how to structure your code for readability and efficiency.
- Plan how to document your code with clear comments.
- Consider how to present results clearly, using tables or visualizations where appropriate.
- Ensure that all outputs are clearly labeled and explained in the context of the task.
- Plan how you'll interpret each result in relation to the original task.
- Consider potential unexpected results and how you'll handle them.
</analysis_planning>
Execute your analysis plan, creating new cells as needed.

4. Conclude and Submit Answer:
<thought_process>
- Reflect on how your results relate to the original task.
- Consider any limitations or uncertainties in your analysis.
- Plan a concise summary of your findings.
- Think about how to phrase your conclusion as clear statements.
- Ensure that the notebook contains all necessary information for another model to derive these answers.
- Consider any additional insights or patterns you've noticed during the analysis.
- Think about potential follow-up questions or areas for further investigation.
</thought_process>

~~~~
