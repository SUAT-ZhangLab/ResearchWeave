# analyses__consensus_prompt

**性质：官方动态提示词的原始 Python 表达式。不是变量已填好的最终提示词。**

来源：[robin/analyses.py:43](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/analyses.py#L43-L50)；提交 4a5cce310f3bc7663a67117db88af43b84733ffe；许可 Apache-2.0。

## 原始表达式

~~~~python
f"""\
    Here is the user query to address:
    {CoT}
    {guideline}
    <query>
    {consensus_query}
    </query>
    """
~~~~
