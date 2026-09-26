# zero_pollution.md · _arch_v20 零污染自证

> 调研轮次：_arch_v20（异族调研·向外求索）· 日期：2026-09-21
> 纪律：全程只读；未修改 tools/evidence/atoms/examples/tests/data 任何正式文件；
> 未跑 pytest/poison_drill/mutation_fuzz/tool_integrity --update；未 git commit/checkout/reset/push。

## 一、开工基线（调研开始前，git status --porcelain 机器输出）

```
 M _adv_v80/probes/p57.cpp
 M data/metrics_612.md
?? _arch_v19/
?? _arch_v19_brief.md
?? _arch_v20_brief.md
```
HEAD：708f430（"615 A2：30 条真逐条复核决策清单（交人审）"）。

## 二、收工状态（调研结束，同一命令机器输出）

```
 M _adv_v80/probes/p57.cpp
 M data/metrics_612.md
?? _arch_v19/
?? _arch_v19_brief.md
?? _arch_v20/
?? _arch_v20_brief.md
?? tools/learner_transition_detector.py
```

## 三、集合差比对（机器结论）

| 项 | 开工 | 收工 | 归属 |
|---|---|---|---|
| `_arch_v20/` 全部内容 | 无 | **新增（本轮唯一有意产出）** | 本调研 |
| `_adv_v80/probes/p57.cpp` | 已 M | 仍 M | 开工前既有，未触碰（CRLF 假脏，git 提示 CRLF will be replaced） |
| `data/metrics_612.md` | 已 M | 仍 M | 开工前既有，未触碰（CRLF 假脏；git diff --stat 显示 1 行差异，开工前即存在） |
| `_arch_v19/`、`_arch_v19_brief.md`、`_arch_v20_brief.md` | 已 ?? | 仍 ?? | 开工前既有 |
| `tools/learner_transition_detector.py` | **不存在** | ?? | **非本调研创建**，见第四节披露 |

`git diff --stat`（排除 _arch_v20）仅见 `data/metrics_612.md | 2 +-`，与开工基线一致；本调研未改动任何已跟踪文件。

## 四、异常项如实披露：tools/learner_transition_detector.py

- 事实：该文件在开工基线中不存在，收工时为未跟踪状态；创建/修改时间 **2026-09-21 13:26:40**，426 字节。
- 内容：文件 docstring 自述为"**615 D3 · 跃迁触发条件机器判定（新建工具）**"，属 615 批次实施线产物（与 HEAD 的 615 批次工作同线），输入 data/learner_state.json 等，含 --check/--report。
- 与本调研的关系：**本调研全部写操作（Write 工具）仅落在 `_arch_v20/` 路径下**（15 个 Markdown + probes/ 内 3 个脚本与 README）；三个探针脚本经代码自查仅 open() 读取 data/ 与 tools/poison_surface_map.json，写操作仅 stdout（经 Tee 落 _arch_v20/probes/output/）。本会话无任何对 tools/ 目录的写入/重定向命令。
- 处理：按"不删除、不还原、不提交非本调研文件"纪律**原样保留**；推断为同机并行的 615 实施会话产物（【推断】，无法从 git 直接归因未跟踪文件的创建进程）。提请监工在合并 615 批次时按其正常流程验收该文件。

## 五、本调研实际新增清单（全部位于 _arch_v20/）

```
_arch_v20/00_总览_向外求索_范式级突破候选与缺口分析.md
_arch_v20/01_形式化验证与证明工程.md
_arch_v20/02_AI对齐与可解释性.md
_arch_v20/03_零知识证明与可信计算.md
_arch_v20/04_知识表示与神经符号.md
_arch_v20/05_统计学习序贯分析与因果推断.md
_arch_v20/06_科学哲学与元科学.md
_arch_v20/07_人机协作与众包.md
_arch_v20/08_软件工程混沌工程与可观测性.md
_arch_v20/09_教育技术与学习科学.md
_arch_v20/10_法律合规与证据标准.md
_arch_v20/11_复杂系统与网络科学.md
_arch_v20/12_信息论与编码理论.md
_arch_v20/13_自由探索方向.md
_arch_v20/14_跨方向综合分析.md
_arch_v20/zero_pollution.md（本文件）
_arch_v20/probes/README.md
_arch_v20/probes/p01_arggraph_robustness.py
_arch_v20/probes/p02_confidence_sequence.py
_arch_v20/probes/p03_conformal_abstention.py
_arch_v20/probes/output/p01_output.txt
_arch_v20/probes/output/p02_output.txt
_arch_v20/probes/output/p03_output.txt
```
对照 brief 交付清单 17 件：00-14 共 15 份分析文件（含 00 mandatory 两句话）、probes/ 目录（3 脚本+3 原始输出+README）、本自证文件——齐全。

## 六、探针临时文件与命令记录

- 探针仅用 `python` 运行，输出写入 `_arch_v20/probes/output/`；PowerShell Tee-Object 为唯一额外写句柄，目标路径均在 _arch_v20 内。
- 未使用 --update；**未运行任何 --check 类监工只读命令**（brief 允许但建议少跑）；git 子命令仅 log/status/diff（只读）。
- Shell 通配/内联 python -c 的一次引号失败（SyntaxError）未产生任何文件写入。

## 七、关于 brief 提及的两条长期 CRLF 假脏文件

brief 点名 full_baseline_v4.json / EV-CONC-001.md 两条假脏"不要提交不要还原"；本轮开工/收工两次 status 均**未出现**这两个路径（当前工作树的两个 M 是 p57.cpp 与 metrics_612.md，同为 CRLF 提示，同样未触碰）。记录此差异，未做任何处理。

## 八、结论

除 `_arch_v20/` 新增外，本调研**零修改、零删除、零提交**；唯一例外项 tools/learner_transition_detector.py 已在第四节用时间戳与内容证据如实披露并排除归属。
