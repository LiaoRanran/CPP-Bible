# _worklog_578 · 苦力收尾批：M5 报告口径翻盘 + slow 四红

> 任务书：`References/architecture_架构演进/578_苦力收尾_M5报告口径翻盘_slow四红.md`
> 承接：`a10c6e0`（575）｜分支 master（本地，未 push）｜本文件按惯例**不入库**。
> 提交：`b4173ac`（任务1）/ `76efae8`（任务2.1-2.2）/ `d116d9c`（任务2.3）。**任务 2.4 按令保持红**。

## 0 · 开工基线核对（实跑，勿凭记忆）

| 项 | 实测 |
|---|---|
| HEAD | `a10c6e0` ✓ |
| gate | `63 条 · 191 (block=0 warn=136→186 advice=5)` ✓（hmm：warn=186 是 575 之后的现状） |
| poison | `118/118` ✓ |
| `tool_integrity --check` | exit 0 ✓ |
| 工作树遗留 | `tools/mutation_fuzz.py` 有 575 回退时留下的 6 行注释（本批已随任务 1 同 commit 带上）✓ |

## 1 · 任务 1：`_findings_key` 并入文案（M5 报告口径翻盘）

**改动**（`tools/mutation_fuzz.py`）：
* `_findings_key` → 四元组 `(rule_id, severity, str(target), message)`，`_snapshot()` 标注同步；
* `classify()` 两处解包改 `for r, s, t, *_ in new`（报告仍只打 `规则:目标`，不刷爆输出）；
* 两条 548 用例（`test_548_diff_is_not_card_scoped` / `test_548_replay_runs_only_when_it_can_change_verdict`）
  自造假 `new` 集**升四元组**——语义不变，未删未恒真。

**v5 全量基线**（`data/mutation/full_baseline_v5.json`，7 算子 / 1183 变体 / 790s）：

| 算子 | v4 (b/e/n_a) | v5 (b/e/n_a) |
|---|---|---|
| M1 | 64/1/27 | 64/1/27 |
| M2 | 168/0/27 | 168/0/27 |
| M3 | 65/0/42 | 65/0/42 |
| M4 | 200/0/33 | 200/0/33 |
| **M5** | **0/29/56** | **29/0/56** ← 翻盘 |
| M6 | 324/8/0 | 324/8/0 |
| M7 | 139/0/0 | 139/0/0 |

* **总体逃逸率**：v4 38/998 → **v5 9/998 = 0.902%**，C-P95 **[0.004132, 0.017050]**（n_a 185）。
  metrics 时点升 v5，**v1–v4 保留为历史时点**（不覆盖）。
* **M5 两率**：**严格 3/29 = 10.34% [2.19%, 27.35%]**；**含 warn 处置 29/29 = 100%**；逃逸 **0/29**。

### 1.1 strict 那 3 条是哪条规则、为何是 block（提示词要求的"唯一真值"说明）

**关键：M5 的稳定分布是 `warn_only 29 / strict 0`**——单独复跑 M5（24s，`data/mutation/_578_m5.json`）
实测 `blocked=29（严格 0）escaped=0 n_a=56`，与监工探针（warn_only29/strict0）**一致**。

v5 全量里多出 3 条 `strict`，规则是**另一个既有 block 规则** `EV-ARTIFACT-FILE-EXISTS`
（`gate_engine.py:2629`，严重度按设计就是 block："卡声明的工件文件不存在 ⇒ 证据载体缺失，
replay 无对象可复算"）。命中的是 3 张卡引用的证据卡：
`ATOM-MEM-ALLOC-001/prop-4 → EV-LANG-001,002`、`ATOM-MEM-LEAK-001/prop-3 → EV-MEM-001`、
`ATOM-MEM-RAII-002/prop-4 → EV-MEM-005`。

**为什么不是 warn**：它不是 `OBSERVATION-LIVENESS` 的降级，而是**另一条规则**按其既定严重度
（block）报出来的；`OBSERVATION-LIVENESS` 自身在 26/29 上仍是 warn（本批未升 block，符合"苦力不得自行升级"）。

**成因（已定位到"跨算子共享沙箱态"，但未根因）**：探针实测①4 张卡的 `artifact` 在真仓库**都存在**
（`Examples/atoms/*.asm`，`is_file()=True`）；②存量跑 `EV-ARTIFACT-FILE-EXISTS` 命中 **0**（沙箱内/外都是 0）；
③`run_fuzz` 的 baseline 与 classify **同在** sandbox 内、`ROOT` 未被 patch ⇒ 单看 M5 复现不出来。
⇒ 结论：这 3 条只在"同一沙箱里连跑 7 个算子"时出现，**指向跨算子的卡状态/解析缓存泄漏**，
不是 M5 的性质。**已列后续跟进项**（见 §5），本批不改结论、不掩盖数字（两处都贴）。

## 2 · 任务 2：slow 四红

### 2.1 `test_observation_liveness_live_observation_passes` ✅ 转绿
新开 `_OBS_PROP_LIVE = _OBS_PROP` + 命题级锚（`liveness: {kind: fixture_symbol, symbol: spin_plain}`）。
**不改共享 `_OBS_PROP`**：它还被 526 规则2 的 4 例 + 530"死观测须 warn"用着，改它会缩小覆盖。

### 2.2 `test_observation_liveness_skips_when_no_artifact_assertion` ✅ 转绿（**含一处规则修正**）
**重要发现（偏离提示词处方，附证明）**：提示词说"给命题补合法锚 ⇒ `_prop_liveness_ok` 过 ⇒ 走到跳过分支"。
实测**做不到**：`_prop_liveness_ok` 要能过，符号必须出现在某张引用卡的 `artifact_assert` 里 ⇒
该卡 `_has_artifact_assertion()` 必为真 ⇒ 535 的跳过分支 `not cards or not any(...)` **永不触发**
（575 把锚检查无条件前置后，它成了**死代码**）。

**处置**：把"交 OBSERVATION-NEEDS-ARTIFACT"的推迟判断**提回锚检查之前**，条件写成
`cards and not any(_has_artifact_assertion(c) for c in cards)`——
* `cards` 为空（**M5 活雷形状**：inference 改标 observation 且无 evidence 引用）时**仍走锚检查** ⇒ 活雷照堵；
* **存量影响 0**：实测 50 条 observation 命题**全部**有工件断言 ⇒ 不变命中数。实测 gate 仍
  `63 条 · 191 (block=0 warn=186 advice=5)`（与改前逐字相同）。
* 测试：2.2 夹具改成"**带合法锚 + 证据卡无工件断言**"（这样"锚合法且不重复报"被真测到，
  而非靠"没锚所以不报"蒙对），并加**反证**：补上含该符号的工件断言后走"卡级三条件"同样放行。
* `gate_engine.py` 属 CORE_TOOLS ⇒ 同 commit 重钉（`--check` exit 0）。

### 2.3 `test_poison_attack_type.py` 两红 ✅ 转绿
台账 `tools/poison_surface_map.json` 是**加 P74/P75/P76→A3 映射之前**的旧版（P74-76 记 `A?`、
A3 计数 18 < 静态登记 20）⇒ 用当前代码重跑 `--write-surface-map`（drill `118/118`）。
刷新后：P74/P76 → **A3**、台账 A3 **21** ≥ 静态 20、A2 13 ≥ 11 ⇒ 两红转绿（16/16）。
连带更新**锁已提交台账**的 syrupy 快照 `test_poison_surface_map_committed`（台账是派生产物，
快照记录的就是它的已提交基线；不改测试断言）。

### 2.4 `test_json_output.py::test_golden_lock_json` ⛔ **按令保持红**
warn 136→186 是 575 暴露的存量债务（50 条 observation 缺命题锚）。**未 accept、未改测试**，
交监工/人审。

## 3 · 收工门禁（fresh）

| 项 | 实测 |
|---|---|
| pytest `-m "not slow" -n auto` | **exit 0** ✓ |
| pytest `-m slow -n0` | **exit 1，唯一失败 = `test_json_output.py::test_golden_lock_json`（预期红）**；其余 4 条已转绿 ✓ |
| `tool_integrity.py --check` | exit 0 ✓ |
| gate | `63 条 · 191 (block=0 warn=186 advice=5)` ✓（本批未变命中数） |
| poison | `118/118` ✓（重写台账后只多不少） |
| replay | `confirm=56 refute=0 infra_error=0` ✓ |
| 受控目录 | `git diff --quiet -- atoms/ evidence/` exit 0 ✓（`EV-CONC-001.md` 内容零差异，只有行尾 stat 假 M） |

## 4 · 偏差表

1. **2.2 未按提示词处方做**（处方在该代码结构下不可达）⇒ 改为"修正规则顺序 + 夹具按新语义写"，
   并附死代码证明与存量影响实测（0）。**这是本批唯一一处改判定核心**，已单独 commit + 重钉。
2. **v5 用全量 7 算子**（不是"仅 M5"）：`full_baseline_v1–v4` 都是全算子口径 ⇒ 保持可比；
   M5 明细在其中可读。另单独跑了一次 M5-only 作为**分布的唯一真值**（`data/mutation/_578_m5.json`，
   未入库的临时报告），以免用全量里那 3 条 flaky 的 strict 当 M5 的性质。
3. **strict 3 条未根因**（已定位到"跨算子共享沙箱态"，附三个反证探针）⇒ 交后续，不在本批扩范围。
4. **额外发现（提示词未列）**：`tests/test_metrics_collector_curves.py` /
   `tests/test_overturned_curves.py` 的 3 处断言停留在 v3 口径（`997`/`38`），在 **fast** 里本是红的
   （575 只跑 targeted 未跑全量 fast 遗留）⇒ 本批随 metrics 升 v5 一并更新为 **9/998**、`n_a 185`。
5. **`data/mutation/full_baseline_v4.json` 曾被后台重跑覆写**（判定数字逐字一致，仅 elapsed 等字段不同）
   ⇒ 已从 HEAD 取回原文，避免把无关改动混进本批提交。
6. 工作树那 6 行 575 遗留注释：已改写成"578 已采用"的正式说明，随任务 1 同 commit。

## 5 · 交后续（精确施工点）

1. **跨算子沙箱态泄漏**（strict 3 条的成因）：最小复现 = 全量跑一次 M5 与单跑 M5 对比 `kind` 分布；
   嫌疑点 `run_fuzz` 每卡"先跑 7 算子共用同一沙箱副本"的写-还原与 `_meta` 解析缓存。
   本批已把"单算子分布"与"全量分布"都留证，别把两者混为一谈。
2. **golden 恶化 1 项**（warn 136→186）待人审 accept + 分类留痕（苦力不得自签）。
3. 50 条待补命题级锚（`data/prop_liveness_todo.md`，575 产出）＝知识活，交人或强模型轮。
4. `P74/P75/P76` 的 A3 映射已生效；若后续再加攻击面载荷，记得**重跑 `--write-surface-map`**（本批红因）。
