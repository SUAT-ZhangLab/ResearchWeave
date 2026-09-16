# ERA：角色、提示词和工作方法

**ERA 可以称为一个会反复写代码、运行代码并根据成绩继续改进的研究 agent 系统。当前公开示例中，只有写代码这一步调用语言模型；选择候选、执行程序和计算成绩由普通程序完成。**

本说明依据本机安装的官方源码提交 `b836730b5c000526af95116b1d0e2c60c8cf0a10`，不是对其他未公开 ERA 版本的推测。这里的中文说明是本次整理；`original/` 内的英文内容来自指定提交。

## 1. 提取出了什么

| 文件 | 内容 | 精确来源 |
|---|---|---|
| [01-gemini-role-template.md](original/01-gemini-role-template.md) | 通用角色：数据科学家与 Python 程序员；要求只返回 Python 代码 | `implementation/llm.py`，17–25 行，`full_prompt` |
| [02-program-improvement-template.md](original/02-program-improvement-template.md) | 房价回归任务：读取问题、数据预览、已有代码和成绩，生成改进版函数 | `implementation/playground_s3e1.py`，76–123 行，`prompt` |
| [03-single-cell-overview.md](original/03-single-cell-overview.md) | 单细胞批次整合任务概述 | `implementation/notebooks/single_cell_batch_integration.ipynb`，cell 0（第 1 格） |
| [04-single-cell-task.md](original/04-single-cell-task.md) | 单细胞任务的输入、输出、评分、可用工具、限制与专家建议 | 同一 notebook，cell 1（第 2 格） |
| [05-flu-overview.md](original/05-flu-overview.md) | 流感住院人数概率预测任务概述 | `implementation/notebooks/flu-cornell-jhu-hierarchsir.ipynb`，cell 0（第 1 格） |
| [06-flu-task.md](original/06-flu-task.md) | 流感任务的函数接口、资料、预测要求和指定建模方法 | 同一 notebook，cell 1（第 2 格） |

前两份原来嵌在 Python 的 f-string 中，即运行时会填入变量的字符串；本次只去掉字符串外面的 `f` 和三引号，保留全部英文、换行和 `{变量}`。它们还没有填入实际问题与数据。

后四份原来是 notebook 的 Markdown 格，本次逐格保存。它们是公开的任务定义；当前源码没有给出这两个 benchmark 实验发送给模型的完整消息记录，因此不能把这四格称为完整 system prompt。

**该提交没有单独定义人格的原生角色 Markdown 文件。** 本次生成的文件便于阅读和复用，不表示 ERA 原来会从这些文件载入 agent。候选程序、运行结果、初始示例程序和带 `[exclude_from_prompt]` 标记的格没有被当作角色定义提取。

## 2. 各部分由谁完成

| 部分 | 输入 | 做什么 | 输出 | 是否由角色提示词驱动 |
|---|---|---|---|---|
| 写代码的模型 | 角色模板，加上问题、数据预览、已有程序和该程序的成绩 | 提出新的实现，遵守函数接口、库和速度要求 | 完整 Python 程序文本 | 是，模板 01 和 02 |
| `PlaygroundGenerator` | 问题、被选中的程序及成绩 | 读取训练数据前几行；把负 RMSE 转回正 RMSE；拼出任务提示词；调用模型 | `Solution`，里面保存程序字符串 | 它负责组织模型调用，本身没有另一个人格 |
| FUTS 搜索程序 | 全部历史候选、成绩、访问次数、迭代次数 | 综合成绩排名和探索次数，选择下一次要改进的旧程序；记下新程序及其来源 | 最终成绩最高的程序和分数 | 否，是 Python 算法 |
| 执行器 | 新程序、训练与测试数据 | 运行约定函数，拿到预测值；处理运行失败或输出长度不符 | 预测结果或失败状态 | 否，是普通程序 |
| 评分函数 | 预测值和真实值 | 计算任务指定指标；回归示例用 RMSE（均方根误差，越低越好） | 给搜索程序的分数；示例使用负 RMSE，所以越高越好 | 否，是计算公式 |

FUTS 全称 Flat UCB Tree Search。这里可以理解为“依据过去成绩和尝试次数选择下一步改哪份代码”的搜索方法。它会再次尝试已有的高分方案，也会尝试过去较少探索的方案。

源码位置：`llm.py:16`；`playground_s3e1.py:66`、`:127`；`futs.py:69`、`:79`、`:89`、`:96`。官方 `sandbox.py` 只声明执行接口并抛出 `NotImplementedError`，因此角色文本本身也不能提供可运行的代码执行环境。

## 3. 提示词怎样组合

回归示例的实际顺序是：

1. FUTS 选出一份历史程序，把它和成绩交给 `PlaygroundGenerator`。
2. 模板 02 填入 `{problem.description}`、`{data_preview}`、`{rmse:.5f}` 和 `{parent_solution.program}`。
3. 模板 01 用上一步完整内容替换 `{prompt}`，加上数据科学家、Python 程序员的角色要求。
4. `GeminiLLM.draw_sample` 把组合后的整段文字放入 API 的 `contents` 参数。代码没有把模板 01 作为独立 `system_instruction` 参数发送。
5. 模型返回代码；调用代码去掉可能出现的 Markdown 代码围栏。
6. 执行器运行新代码并评分；FUTS 保存它，进入下一次选择。

模板 02 中的具体要求包括：函数叫 `train_and_predict`；接受训练和测试文件路径；返回预测数组；不使用 XGBoost、LightGBM 或网格搜索；随机森林或 boosting 的树数不超过 50；预期运行限制为 60 秒。这些是这个示例的任务要求，不是所有 ERA 任务都必须遵守的规则。

## 4. 两份科学任务说明怎样用

### 单细胞批次整合

将模板 03 和 04 作为任务说明，并同时提供相应数据、函数接口及评分程序。

- 输入：`AnnData` 对象，`.X` 为原始表达计数，`obs['batch']` 为批次；另有 `config` 参数字典。
- 输出：`eliminate_batch_effect_fn` 的代码与配置；运行后返回 `AnnData`，把整合结果放在 `obsm['X_emb']`。
- 方法要求：去除批次差异，同时保留生物学差异；原文禁止实现使用 `cell_type` 标签；说明可用的数值计算工具、内存需求、出错时的处理和评分指标。
- 专家建议：条件变分自编码器，区分生物学与批次相关的潜在表示，并用对抗损失减少生物学表示中的批次信息。它是该任务原文提供的具体建议。

### 流感住院人数预测

将模板 05 和 06 作为任务说明，并提供时间序列数据、地理信息及滚动时间窗口的评分程序。

- 输入：`train_x`、`train_y`、`test_x`，以及文中说明的历史 ILINet 资料等。
- 输出：`fit_and_predict_fn` 的代码；运行后返回预测分位数的 DataFrame，行索引必须对应 `test_x`，同一行分位数必须递增。
- 方法要求：用加权区间分数 WIS 衡量预测误差与不确定性；指定采用跨季节的贝叶斯分层 SIR 方法，并要求保留原方法的核心原理。
- 原文还要求先在代码顶部用注释列出 3–4 条核心原理，再写实现。

这两份任务定义分别适用于各自的任务。若换成你的研究问题，应改写目标、数据接口、允许使用的资料和评分办法，并同时接好相应的工具与程序。

## 5. 来源、许可与复现

- 官方仓库：[google-research/era](https://github.com/google-research/era/tree/b836730b5c000526af95116b1d0e2c60c8cf0a10)。
- 原始许可：[Apache License 2.0](original/LICENSE)。原项目归属 Google Research ERA；有版权头的文件注明 `Copyright 2026 Google LLC.`。
- [manifest.json](manifest.json) 为每一项记录来源、源码行号或 notebook 格号、源文件 SHA-256、提取文件 SHA-256；前两项还保存含 `f` 和三引号的完整原始字符串表达式。
- [extract.py](extract.py) 直接读取指定 Git 提交，不执行原项目代码，也不读取 notebook 输出；它和本说明均为本次新增。
- `original/` 中英文照原文保留，包括原有拼写、符号和对性能的表述；这些表述的原样保留不代表本次重新证明了性能。

在项目根目录中重建这六份文件：

```powershell
python agent-prompts/era/extract.py
```

2026-09-15 已执行提取并检查 6 份输出文件与记录的 SHA-256 一致。所有提取结果均写入 `agent-prompts/era/`；未修改 `vendor/era/`。
