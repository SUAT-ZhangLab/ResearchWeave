# ZhangLuo 操作说明

以下命令从项目根目录运行。安装为技能后，用 `python <技能目录>/zhangluo.py` 替换开头的调用。

## 研究记录

```sh
python zhangluo.py doctor
python zhangluo.py research init --study "research/example" --question "研究问题"
python zhangluo.py research record --study "research/example" --file "evidence.json" --artifact "measurements.csv"
python zhangluo.py research status --study "research/example"
python zhangluo.py research report --study "research/example"
```

合成示例在 init 中加 `--label synthetic`。record 的 `--artifact` 可重复。
程序复制原文件并记录 SHA256；研究记录不覆盖旧内容，修改结论时保存新记录并引用原 ID。
`report` 汇总已保存记录；agent 仍需撰写对研究问题的解释，不能只交程序生成的清单。

输入 JSON 示例：

```json
{"kind":"evidence","content":{"claim":"实际来源支持的观察","source":"论文链接或文件路径","evidence_type":"literature"},"sources":[],"parent_ids":[]}
```

kind 与字段详见 [角色方法中的记录格式](roles.md#记录格式)。evidence_type 取 literature、project_measurement、synthetic 或 inference。
所有引用记录的 ID 必须来自当前研究里已保存的记录。

## 执行一次分析

先保存 analysis 记录，明确 question、inputs、method、comparison、success_criteria、independent_unit 和 hypothesis_ids。

```sh
python zhangluo.py research run --study "research/example" --analysis-id "实际返回的ID" --code "analysis.py" --input "input.json" --function run
```

程序入口形如 `def run(data): ...; return result`，输入输出必须兼容 JSON。
运行会保存实际程序、输入、输出或失败记录。容器不能直接读取宿主文件；大型任务按实际需求另配环境。

## ERA 分轮改进

```sh
python zhangluo.py era init --session "research/example/work/era-01" --spec spec.json --baseline baseline.py
python zhangluo.py era ask --session "research/example/work/era-01"
python zhangluo.py era tell --session "research/example/work/era-01" --request-id "ask返回的ID" --candidate candidate.py
python zhangluo.py era finalize --session "research/example/work/era-01"
```

ask 之后由当前 agent 编写 candidate.py；tell 必须使用当前请求 ID。失败也记录。
示例 spec.json（仅用于功能演示）：

```json
{"problem":"合成示例 y=2*x+1","function":"predict","metric":"rmse","development":{"input":[0,1,2],"target":[1,3,5]},"final":{"input":[3,4],"target":[7,9]},"iterations":3,"timeout_seconds":30}
```

支持 rmse 与 accuracy。返回值是一维预测数组。finalize 在开发数据上选出程序，然后对提供的 final 数据执行一次。
应在比较方法之前划分最终评价数据，改进代码时不读取它；当前 agent 仍有宿主文件读取权，程序没有实现独立的数据保密服务。
合成示例的分数不是科学发现。将真实结果登记为 result 并关联 analysis_id，再写科学解释。

## 继续与失败恢复

新会话先读取 status、已有记录与 ResearchReport.md。锁文件提示其他操作仍可能进行，先确认进程已结束再处理遗留锁。
命令输出 JSON，失败返回非零退出码；不要把报错解释为保存或执行成功。
