# utils__user_prompt

**性质：官方动态提示词的原始 Python 表达式。不是变量已填好的最终提示词。**

来源：[robin/utils.py:600](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/utils.py#L600-L617)；提交 4a5cce310f3bc7663a67117db88af43b84733ffe；许可 Apache-2.0。

## 原始表达式

~~~~python
f"""Please evaluate and compare the following two candidates based on the criteria provided.

            **Candidate 1 (ID: {hypo_1_info['index']})**
            Name: {hypo_1_info['hypothesis']}
            Reasoning: {hypo_1_info['answer']}

            --- VERSUS ---

            **Candidate 2 (ID: {hypo_2_info['index']})**
            Name: {hypo_2_info['hypothesis']}
            Reasoning: {hypo_2_info['answer']}


            Provide your evaluation STRICTLY in the following JSON format. Do NOT include any text before or after the JSON object.
            Ensure the entire output is a single, valid JSON object

            {ranking_prompt_format}
            """
~~~~
