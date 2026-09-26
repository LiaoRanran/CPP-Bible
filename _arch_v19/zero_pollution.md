# zero_pollution · _arch_v19（595）零污染自证

> 调研者：异族 seed-evolving（Trae）· 2026-09-21
> 方法：开工/收工 git 状态机器比对（脚本 [probes/p10_zero_pollution_check.py](probes/p10_zero_pollution_check.py)，输出 [output/p10_zero_pollution_check.out](probes/output/p10_zero_pollution_check.out)）。
> 结论先行：**PASS —— 本调研 37 个产出文件全部且仅在 `_arch_v19/` 内；对 tools/evidence/atoms/misconceptions/tests/data 等正式文件零修改。**

---

## 一、纪律执行声明

- 未运行：pytest、poison_drill、mutation_fuzz、tool_integrity 的任何写/更新模式，未运行 `git add/commit/checkout/reset/push`。
- 允许的动作均已使用：`git status/log/rev-parse/reflog/show`（只读）；`gate_engine.py --check`（只读，brief 明示允许）；探针全部纯标准库、只打开文件读取（`open(...,"rb")/read`），不创建/修改/删除任何 `_arch_v19/` 之外的文件；mutation 相关探针（p07）只对卡文本做**静态模式计数**，不调用 mutation_fuzz、不产变体文件。
- 编译临时文件：本调研未触发任何编译（p07 是静态计数；只有 gate --check 与探针的 python 执行）。

## 二、工作区状态三时点（含并发会话时序——重要）

本调研在一个**有并发建设会话持续提交**的仓库中进行，故基线发生了外部推进。如实记录三时点：

| 时点 | HEAD | 工作区（除 _arch_v19 外） | 来源 |
|---|---|---|---|
| T0 调研开工首次观察 | `3ac90d1` | 5 modified（`_adv_v80/probes/p57.cpp`、`data/613_accept_report_report.md`、`data/metrics_612.md`、`data/metrics_613.md`、`tools/run_613_gate.py`）+ 1 untracked（`_arch_v19_brief.md`） | 调研者首次 `git status` |
| T1 保存 before 快照 | `6861a7f` | 2 modified（`_adv_v80/probes/p57.cpp`、`data/metrics_612.md`）+ 1 untracked（brief） | [output/git_status_before.txt](probes/output/git_status_before.txt) |
| T2 收工 | `05b161b` | 2 modified（同上两条开工既有）+ 3 untracked：`_arch_v19_brief.md`（开工既有）、`tools/learner_ood_evaluator.py`、`tests/test_learner_ood_evaluator_614.py`（后两条为并发 614 批次新增）+ `_arch_v19/`（本调研） | [output/git_status_after.txt](probes/output/git_status_after.txt) |

**T0→T1 的变化归因**：并发会话提交 `6861a7f "F3: 收工门禁 + 验收报告（613 自身结论 PASS）"`，把 T0 的 3 条 613 相关 modified 收入提交，非调研者所为（调研者全程无写 git 命令）。

**T1→T2 的变化归因**：`git reflog` 显示并发会话在此期间推进了整个 **614 批次 6 个提交**（调研者未参与）：
```
05b161b 614 B2：学习者镜像仪表盘升级（真实数据版）
191fd35 614 B1：真实学习行为采集机制设计 + BKT 递推验证
4c9bbae 614 A3：CI 全绿里程碑记录
9fc6a33 614 A2：governance 台账更新 + tool_integrity 重钉
512d991 614 A1：CI gate 失败根因排查与彻底修复
a4d76f1 614 任务0：先量基线台账
```
收工时工作区里的 `tools/learner_ood_evaluator.py`、`tests/test_learner_ood_evaluator_614.py` 即该批次产物（文件名含批次号 614，且在 T1 快照中不存在）。

> 旁注：并发 614 B1 正在建"真实学习行为采集机制"——恰与本报告维度1/5/12 的开门数字（learner_behavior 真实事件 0→≥50）同向；本报告所有数字基于读取时刻的文件状态，614 是否最终改变 learner 数据需以后续批次重跑 p00 为准（本调研不越界代为结论）。

## 三、机器比对结果（p10，可复算）

- 收工时 `_arch_v19/` 之外工作区条目 5 条，**逐条归因全部成功**：
  - `_adv_v80/probes/p57.cpp`（M）、`data/metrics_612.md`（M）：T0 开工首次 status 即存在；
  - `_arch_v19_brief.md`（??）：开工前已在的投喂词，非本调研创建；
  - `tools/learner_ood_evaluator.py`、`tests/test_learner_ood_evaluator_614.py`（??）：并发 614 批次新增（T1 不存在、文件名含 614、reflog 有对应提交链）。
- 本调研产出 **37 个文件**（14 份 .md + 11 个探针脚本 p00–p10 + 12 个输出/快照），集合指纹（相对路径+字节内容的 sha256 摘要前缀）= `2a70a2777187f941`（p10 运行时刻；此后新增本文件与 p10 自身的 .out，故复跑指纹会增长文件数，属正常，关键不变量是"所有新增均在 _arch_v19/ 内"）。
- p10 判定行：`PASS — 本调研零写操作落在 _arch_v19/ 之外；外部变化全部可归因`。

## 四、对正式文件零影响的最终确认

- 探针只 `open(..., encoding=...)` 读取 atoms/evidence/misconceptions/data/tools 下文件；p03 通过 `sys.path` import gate_engine 并调用其 check 函数（进程内只读执行，不写文件）；p09 以子进程跑 `gate_engine.py --check`（只读，其 warn 退出码是设计行为）。
- 未修改任何卡片、证据、工具、测试、配置；未触碰 .tool_checksums、golden、build/、goldens/。
- 收工时正式文件区相对 T0 的所有变化均可由 reflog 上的并发提交链解释，与本调研无因果关系。

## 五、复现方式

```
.venv/Scripts/python.exe _arch_v19/probes/p10_zero_pollution_check.py
# 期望：[D] PASS；[A] 区除并发 614/开工既有条目外无其他；[B] 区路径全部以 _arch_v19/ 开头
```
