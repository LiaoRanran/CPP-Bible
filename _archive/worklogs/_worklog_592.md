# 592 worklog：数据层诚实化 + 命题闭包工具

仓库：`CPP-Bible`；解释器：`.venv\Scripts\python.exe`（Py3.13）。
批次边界：只改 `tools/metrics_collector.py`、新增 `tools/overturned_events.py` / `tools/prop_closure.py` /
`tools/prop_network_inventory.py` / `tests/test_*_592.py` + `data/overturned_events.jsonl` /
`data/prop_network_inventory.md`；**不碰 CORE 五文件**（gate/replay/poison/toolchain/cppbible）、不碰卡、不 push。

---

## 任务 0：开工基线（fresh 实跑）

| 项 | 命令 | 实测 |
|---|---|---|
| tool_integrity | `tools/tool_integrity.py --check` | exit **0**（5 核心工具与基准一致） |
| gate | `tools/gate_engine.py --check` | exit **0**；**规则 63 · 命中 191（block=0 warn=186 advice=5）** |
| poison | `tools/poison_drill.py` | **124/124** |
| replay | `tools/atom_evidence_replay.py --check` | confirm=56 |
| v7 基线 | `full_baseline_v7.json` | **1593 / blocked 1405 / escaped 1 / n_a 179 / equivalent 8**、strict 811 |
| v7 逐算子可判 | by_operator | M1 65 · M2 168 · M3 65 · M4 224 · M5 29 · M6 716 · M7 139（escaped 唯 M1=1） |
| overturned 通道 | `Test-Path data/overturned_events.jsonl` | **False**（未创建，与任务书预期一致） |
| `tools/overturned_events.py` | `Test-Path` | **False**（不存在，需新建） |
| prop_graph | `prop_graph.py stats` | **79 命题 / 27 卡** · inference 29 / observation 50 · 签署 card_signed 76 / unsigned 3 · 机验 79 |

### 预置偏差 D0（重要，先量后动发现）
任务书 §开工前基线 第 3 条预期「`data/metrics.jsonl` 最后一条 = 2026-09-17T17:40:45，curves 仍是 v1 的 0.2374」。
**实测不符**：该文件实有 **5 行**，最后一行是 `2026-09-19T00:00:00`、顶层带 `ruler_version: "v7"`、
`metrics.mutation_escape_rate.point = 0.000711`（`1/1406`）。
进一步核对 `tools/metrics_collector.py::collect_curves()`：**591 已把当前口径升到 v7**
（`_rate(v7, …)`；v1–v6 进 `mutation_escape_rate_history`）。即任务 1 的「v1→v7」主干**已由 591 完成**。

因此 592 任务 1 的**剩余真实缺口**只有四项（本批补）：
1. 曲线块未自报 `baseline_version` / `frozen_at_commit`（报告层无法机器核对口径来源）；
2. `overturned` 没有「通道是否已初始化」标志（文件缺失 ⇒ 计数 0 会被误读成"没有推翻"）；
3. `escape_survival_batches` 只有 M3，缺任务书要求的 M5/M6/M2 显式条目；
4. `monotone_convergence` 文案未点明「尺子变更史 v1→v7，非同一量时间序列」。

另注意：`data/metrics.jsonl` 被 `.gitignore:88` 忽略（**未跟踪**）⇒ 本批采集出的新行**不入库**
（与 591 偏差 D3 同源，本批 D3）。

`data/metrics.jsonl` 第 5 行为**手写/一次性探针**产物（顶层 `ruler_version`，非 `collect()` 的 schema：
`{timestamp, metrics, notes, curves, alerts}`）；仓内**没有任何工具**会写出 `ruler_version` 键（已全仓 grep）。
不影响本批：本批采集的行是标准 `collect()` schema，追加在末行之后。

---

## 任务 1：metrics curves 度量诚实化（commit 见下）

### 修前（实测 `collect_curves()` 原样输出，节选）
```
monotone_convergence: "不可声称（只有 1 个时点，勿据单点画趋势）"
mutation_escape_rate: {source: v7, judged 1406, n_a 179, 1/1406, point 0.000711,
                       cp [1.8e-05, 0.003956]}          ← 无 baseline_version / frozen_at_commit
overturned_by_stronger_verifier: 0, overturned_recent: []  ← 无 channel_initialized
escape_survival_batches: {M3: {batches 1, escapes 52, 571→572}, M2: null, M2_note: …, others: null}
escape_survival_note: "其余算子尚无'产生→收口'的完整批次 ⇒ None（不填 0）"
```

### 改后
1. **`_rate()` 自报口径来源**：新增 `baseline_version`（v7/v6/…/v1）与 `frozen_at_commit`
   —— **从基线文件自身读** `d["frozen_at_commit"]`（= `d36d5c8`），**不在代码里抄常量**
   （抄了就会在下次重冻结时静默脱节，那正是"度量不诚实"的老病）。
2. **精度口径（实测修正）**：曲线的 `point`/`cp_low`/`cp_high` 是**6 位小数展示值**（报告口径，
   既有测试锁死）。任务书要求的「1e-9 容差」在任何实现下都不可能落在展示值上
   （1/1406 取 6 位小数后只剩 2 位有效数字，误差 ~2.4e-7）。故新增**全精度**字段
   `point_raw` / `cp_low_raw` / `cp_high_raw`，1e-9 级断言在 `*_raw` 上做（等价且更强）。
3. **overturned 通道标志**：新增 `overturned_channel_initialized`（= `OVERTURNED_FILE.is_file()`），
   区分"没有通道（计数 0）"与"没有推翻（计数 0）"。
4. **survival 补条目**：M5 `{batches 1, escapes 29, 574 → 575, measurement_visible_closed_in 578}`、
   M2 `{batches 0, 假逃逸}`、M6 `{batches 0, 8 条等价变异体}`、`others: null`。
5. **monotone_convergence** → `"不可声称（尺子变更史 v1→v7，非同一量时间序列；仅 1 个含曲线时点）"`。

### 实测（改后）
- 新增测试 `tests/test_metrics_curves_v7_592.py`：**8 passed**；连同存量
  `test_metrics_collector_curves.py` + `test_overturned_curves.py` 共 **20 passed**（`-n0`）。
- `metrics_collector.py --no-heavy` 实跑：`data/metrics.jsonl` **5 行 → 6 行**（新增
  `2026-09-19T16:18:50`）；新行 `curves.mutation_escape_rate` = **1/1406 · point 0.000711 ·
  point_raw 0.0007112375533428165 · cp [1.8e-05, 0.003956] · baseline_version v7 ·
  frozen_at_commit d36d5c8**；`overturned_channel_initialized=False`；survival 含 M3/M5/M2/M6。
- ruff（启用族 E4,E7,E9,F,I001,FURB167）对改动文件 **All checks passed**。

### 非回归（存量测试同步）
- `tests/test_metrics_collector_curves.py` + `tests/test_overturned_curves.py`：
  `escape_survival_batches["M2"]` 由 `None` 改为 `{"batches": 0, …}`
  —— **非回归**：M2 的 207 条已被 571 证伪为 `GATE_READ_KEYS` 尺子 bug 的**假逃逸**，
  "非真逃逸"是**真值 0**（573 立的口径：0 = 真值、None = 缺数据），M6 同理；`others` 仍为 `None`。

### 偏差 D1
任务书「断言 point = 1/1406（浮点容差 1e-9）」：**展示口径下不可达**（见上第 2 条）。
处理：`*_raw` 全精度字段上做 1e-9 断言 + 展示值断言 `point == round(1/1406, 6)`（更强，且与既有测试一致）。

commit：`6250d1d`

---

## 任务 2：overturned 事件通道初始化

### 修前（实测）
- `data/overturned_events.jsonl`：**不存在**（`Test-Path` False；`count()` 概念上 = 没有通道）。
- `tools/overturned_events.py`：**不存在**（573 只把 CLI/schema 设计在 `metrics_collector` 里）。
- 后果：曲线里 `overturned_by_stronger_verifier = 0` 读作"零推翻"，与"**没有通道**"含义相反。

### 做什么
1. 新建 `tools/overturned_events.py`（573 设计落地；单一实现）：
   - `ensure_channel(path=None)`：缺失 ⇒ 建**空文件**；已存在 ⇒ **只逐行校验** JSON（幂等、不写）；
     坏行 ⇒ **fail-loud**（带行号）—— 事件流是审计证据，静默跳过坏行等于篡改证据链。
   - `count(path=None)` / `read_events(path=None)`：事件总数 / 事件列表。
   - `channel_state(path=None)`：`{exists, initialized, events}` —— 把"有没有通道"与"有几条事件"
     **分开成两个事实**（这就是 592 任务1.3 那个标志的数据面）。
   - `append(event, path=None)`：**fail-closed**（缺字段 / 卡解析不到 / git 不可用 / human 名与该卡
     最后一次 git 提交作者不匹配 / by 形态不对 / ts 非 ISO8601 ⇒ `ValueError`，**不落行、不建文件**）；
     只追加、不覆盖、不删除。加 `make_event(...)` 供 CLI 参数形态复用。
   - CLI：`ensure` / `count` / `check`（**不提供 append 子命令** —— 写入面只有库函数，减少误用面）。
2. `metrics_collector.log_overturned()/read_overturned_events()` 改为**委托**到本模块
   （签名/错误文案逐字保留 ⇒ 573 的 5 条回归锁不改一行；**同一套 fail-closed 规则不留两份实现**）。
   顺带把 573 首版的「坏行 continue 静默跳过」改为显形（见 ensure 说明）——**唯一行为收严点**，
   已有测试未覆盖该路径，新测试补上（`test_corrupt_channel_line_fails_loud`）。
3. 建真实通道 `data/overturned_events.jsonl`（**0 字节 / 0 行**）。它**不在 .gitignore**（与
   `propositions.db`/`metrics.jsonl` 不同）⇒ 空文件本身入库，通道在干净 checkout 里也存在。

### 实测（改后）
- `tools/overturned_events.py ensure` → exit **0**，输出 `initialized=True，事件 0 条`；`Get-Item` 长度 **0**。
- `count` → 打印 `0`（exit 0）；`check` → `通道合法…（0 条事件）`（exit 0）。
- 新增 `tests/test_overturned_channel_592.py`：**11 passed**（含幂等、空文件合法、
  缺字段/冒名/git 不可用/坏 by/坏卡/坏 ts 全拒且不落行、坏行 fail-loud、真实通道只读校验）。
  连同存量 `test_overturned_curves.py` / `test_metrics_curves_v7_592.py` /
  `test_metrics_collector_curves.py` 共 **30 passed**（`-n0`，exit 0）。
- ruff（同启用族）对 `tools/overturned_events.py` / `tools/metrics_collector.py` /
  `tests/test_overturned_channel_592.py` **All checks passed**。

### 偏差 D2
任务书说「在 `tools/overturned_events.py`（如不存在则从 573 设计恢复）中**加** ensure_channel/count/append」。
实测：573 的设计**不在独立文件里**，而在 `metrics_collector.py` 内（`--log-overturned` CLI + schema）。
处理：新建独立模块并**把 `metrics_collector` 的旧实现改为委托**（避免同一套"谁能推翻"的规则两份实现、
日后分叉）；573 的对外契约（签名/错误文案/schema/只追加）**逐字保留**，5 条 573 回归锁一行未改、全绿。

### 偏差 D3（沿用 591）
`data/metrics.jsonl` 被 `.gitignore` ⇒ 任务 1 采集的新行**不入库**（但通道文件本身入库）。

commit：`a54d16b`

---

## 任务 3：prop_closure 命题闭包工具（582 N2 落地）

### 修前（实测）
`tools/prop_closure.py` **不存在**（582 只做了调研设计）。`data/propositions.db` 已有：
props 79 行 / prop_evidence 116 行 / 27 卡 / 53 张不同证据卡（**引用的证据卡全部真实存在，0 缺失**）。

### 做什么
新建 `tools/prop_closure.py`（**纯只读**：全文件无 `open('w'`/`write_text`/`unlink`/临时表/subprocess）：
- 边定义（**双实现共用的唯一真源** `EDGE_UNION_SQL`）：`card → prop_key`（卡引用命题）、
  `prop_key → card`（命题引用本卡）、`prop_key → evidence_id`（命题引用证据卡）；
- `closure(start, adjacency)`：**Python 显式 BFS** + visited 去重（环不死循环）；
- `closure_sql(conn, start, edges=None)`：**SQL `WITH RECURSIVE`**（`UNION` 天然去重）；
  `edges` 给列表时用内联 `VALUES` 构造边 CTE（**不建临时表**，合成图对账也保持只读）；
- `cross_check(db)`：逐命题比对两实现，返回不一致清单；CLI 有不一致 ⇒ **exit 2**；
- `stats(db)`、`load_edges`、`build_adjacency`、`prop_keys`、`resolve`（CLI `--id` 解析）；
- `_connect`：缺库/缺表/缺列 ⇒ fail-loud + 直接给 `prop_graph.py build` 重建命令。

**`prop_graph.py` 一行未改**（闭包是独立工具）。

### 实测（改后）
- `prop_closure.py stats`（exit 0）：**命题 79 · 命题所属卡 27 · 卡节点 80（含证据卡 53）·
  边 274 · 连通分量 26**；闭包大小（全体节点，含命题+卡两类 id）**avg 6.076 / max 8 / min 4**，
  分布 `{4:4, 5:6, 6:57, 7:4, 8:8}`；**可达命题数 avg 3.025 / max 4**；**孤立命题 0 条**。
- `prop_closure.py cross-check`（exit **0**）：**双实现 79/79 一致**。
- `prop_closure.py from --id prop-1`（exit 0）：卡内 id 跨卡重名 ⇒ 命中 27 条，逐条打闭包。
- 新增 `tests/test_prop_closure_592.py`：**9 passed**。含
  ① 手工小图（5 命题 + 1 卡、6 条边、含环 p1→p2→p3→p1、含**孤立** p5）逐元素正确；
  ② 同一边集上 Python ≡ SQL；
  ③ 自环 + 二元环终止；
  ④ 边推导口径（卡↔命题、命题→证据卡，8 条边逐条断言）；
  ⑤ `resolve` 精确优先 / 卡内 id 全量；
  ⑥ **可证伪**：把 `closure_sql` monkeypatch 成"只返回自身"⇒ `cross_check` 必须报 **79 条**不一致；
  ⑦ 真实库 79/27/274 + 与 `prop_graph.stats` 命题数交叉一致；
  ⑧ **只读证明**：跑完 `propositions.db` sha256 不变；
  ⑨ 缺库/缺表/缺列 fail-loud。
- ruff（同启用族）对 `tools/prop_closure.py` / `tests/test_prop_closure_592.py` **All checks passed**。

### 偏差 D4
任务书测试项写「小手工图（**5 命题 6 边**）」。实测：本工具边是**从库表推导**的
（每条命题至少产 2 条边：命题↔本卡），在真实 schema 下"5 命题 = 6 边"不可得。
处理：手工图仍用 **6 条边**（5 命题 + 1 卡），但边以**内联边集**传入双实现
（`closure_sql(..., edges=[...])` 走 `VALUES` 分支），因此"5 命题 6 边"这条**被逐字满足**；
库表推导路径另用 3 命题/8 边的临时库单测覆盖（`test_edge_derivation_and_stats_on_temp_db`）。

commit：`938be48`

---

## 任务 4：命题网络台账 `data/prop_network_inventory.md`

### 修前（实测）
该台账**不存在**。生成所需的事实源已就位：`propositions.db`（79/27）+ `prop_closure.stats`
（任务 3）+ 卡面 `claim_structured`（活性锚判定单点 `gate_engine._prop_liveness_ok`）+
`metrics_collector.oracle_report`（oracle 字段只读统计）。

### 做什么
新建 `tools/prop_network_inventory.py`（**只读生成器**：只读库 + 卡面，唯一写动作是 `--out` 台账文件；
`--check` 模式一个字节都不写）→ `data/prop_network_inventory.md`（151 行，**入库**，
与 `data/matrix_value_inventory.md` / `data/prop_liveness_todo.md` 同惯例）。四节：
0 汇总 + 完整性校验；1 命题列表（79 条：id / 类型 / 引用卡 / 闭包大小 / 签署 / **活性锚状态**）；
2 卡列表（27 张：命题数 / `verified_by` / **oracle 状态** / 闭包区间）；3 边统计；4 闭包口径与对账。

### 实测（改后）
- `prop_network_inventory.py` 实跑：**命题 79 · 卡 27 · 边 274 · 异常 引用卡 0 / 无命题卡 0 / 闭包 0**。
- 台账三行完整性校验全 ✓：**引用卡不存在的命题 0 · 无命题的原子卡 0 · 闭包异常（>50 或 =1）0**
  （与任务 4 验收一致，也与 589 的口径一致）。
- 事实基线（台账可复核）：observation 命题 **50** 条、**有活性锚 0** 条（全部缺锚，与
  `data/prop_liveness_todo.md` 的"缺锚 observation 命题：50 条"一致）；`verified_by_oracle` **0 张卡填了**
  （oracle 状态逐卡记「未填（正常状态）」，放权开关全 OFF）；闭包 avg 6.076 / max 8 / min 4。
- `prop_network_inventory.py --check` → exit **0**（台账与事实源一致，151 行）。
- 新增 `tests/test_prop_inventory_592.py`：**4 passed**（五节存在 · 79 命题行 + 27 卡行 ·
  三条完整性校验全 0 · **台账与现读事实源重新渲染逐字节一致**——既锁幂等也锁"不过期"）。
- ruff（同启用族）对 `tools/prop_network_inventory.py` / `tests/test_prop_inventory_592.py`
  **All checks passed**。

### 偏差 D5
任务书任务 4 只要求"跑 `prop_graph.py stats` 和 `prop_closure.py stats`，生成台账"，未指明生成器。
处理：新增**独立只读生成器** `tools/prop_network_inventory.py`（而不是把渲染塞进 `prop_closure.py`）
—— 因为任务 3 要求 `prop_closure.py` **源码无写调用**，台账写盘不能污染那个"纯只读"属性；
并额外提供 `--check`（供测试与 CI 检测台账过期）。

commit：`85c2ec2`

### 补：任务 2 漏 add 的补救 commit `95eae3a`
任务 2 提交 `a54d16b` 时只 add 了新模块/新测试/通道文件，**`tools/metrics_collector.py`
里 `read_overturned_events`/`log_overturned` 的委托化改动漏在暂存区外**（本批唯一流程失误，
如实登记）。该改动在任务 2/3/4 的全部测试运行中一直生效（工作树即如此），故 `95eae3a` 只是
**入库补齐、无行为变化**；补齐后 `git status` 已跟踪修改项**只剩预存在的 v4 CRLF 假脏**。

---

## 任务 5：收工总验收（fresh，串行，退出码定论）

| # | 命令 | 退出码 | 数字 |
|---|---|---|---|
| 1 | `tools/tool_integrity.py --check` | **0** | 5 个核心工具与基准一致（无需重钉） |
| 2 | `tools/gate_engine.py --check` | **0** | **规则 63 · 命中 191（block=0 warn=186 advice=5）**逐字不变 |
| 3 | `tools/poison_drill.py` | **0** | **124/124**；RULE-COVERAGE 39/63；表观 100.0%（63/63）；诚实 95.2%（60/63） |
| 4 | `tools/atom_evidence_replay.py --check` | **0** | **confirm=56 refute=0 infra_error=0**（共 56 张） |
| 5 | `tools/metrics_collector.py`（全量，含 poison/replay） | **0** | 采集 **27/27** 项；新行 `2026-09-19T16:30:51`：`1/1406 · point 0.000711 · cp[1.8e-05, 0.003956] · baseline_version v7 · frozen_at_commit d36d5c8`；`poison 124/124` · `replay confirm 56` · `overturned_channel_initialized True` · `alerts []` |
| 6 | `tools/prop_closure.py cross-check` | **0** | **79/79 一致** |
| 7 | `tools/prop_closure.py stats` | **0** | 命题 79 · 卡 27 · 卡节点 80（证据卡 53）· 边 274 · 连通分量 26 · 闭包 avg 6.076/max 8/min 4 · 孤立 0 |
| 8 | `tools/prop_network_inventory.py --check` | **0** | 台账与事实源一致（151 行） |
| 9 | `tools/overturned_events.py check` | **0** | 通道合法 · **0 条事件** · 文件 0 字节 |
| 10 | `pytest -m "not slow" -n auto` | **1**（见 D8） | 508–509 passed / 1 skipped；3 红 = 1 条**预存在文档漂移** + 2 条 **`-n auto` 并发假红** |
| 11 | `pytest tests/test_metrics_curves_v7_592.py tests/test_overturned_channel_592.py tests/test_prop_closure_592.py tests/test_prop_inventory_592.py -n0` | **0** | 全绿（与存量 573/565 曲线测试合并复跑 **43 passed**） |
| 12 | `ruff check`（本批 4 新增 + 4 改动文件 + 2 存量同步文件） | **0** | **All checks passed** |
| 13 | `git diff --quiet -- atoms evidence Examples Book` | **0** | 受控目录**零污染**；两条 CRLF 假脏（`full_baseline_v4.json`、`EV-CONC-001.md`）全程未提交未还原 |

- **CORE 零 diff**：`git diff --quiet -- gate_engine.py atom_evidence_replay.py poison_drill.py toolchain.py cppbible.py` **exit 0**
  ⇒ **无需 `tool_integrity --update`**。`tools/prop_graph.py` 亦一行未改（exit 0）。
- `-n auto` 三条红的**串行复核**：`pytest tests/test_output_snapshots.py tests/test_replay_lock_serial.py -n0`
  → **10 passed / 5 snapshots passed，exit 0**；`test_governance_doc_guard_591.py::test_verify_real_manifest_matches`
  串行**仍红**且**与本批无关**（见 D8）。
- **未跑**：`pytest -m slow`（本批收工验收清单未列；MEMORY 记其唯一红 = 预存在的 golden 待人工 accept）。

---

## §6 偏差表（如实）

| # | 任务书假设 | 实测 | 处理 |
|---|---|---|---|
| D0 | `metrics.jsonl` 最后一条停在 2026-09-17T17:40:45 的 **v1 0.2374** | 实有 5 行，末行 `2026-09-19T00:00:00` 顶层 `ruler_version: v7`；`collect_curves()` **591 已升 v7** | 照实记录；只补 4 项真缺口（口径来源字段 / 通道标志 / survival 条目 / 单时点文案）。**未改任何已有 v7 口径**，`1/1406` 未动 |
| D1 | 断言 `point = 1/1406`（容差 **1e-9**） | `point`/`cp_*` 是 **6 位小数展示值**（1/1406 取 6 位只剩 2 位有效数字，误差 ~2.4e-7）⇒ 1e-9 在任何实现下都会红 | 新增**全精度** `point_raw`/`cp_low_raw`/`cp_high_raw`，1e-9 断言落在 `*_raw`；展示值断言 `point == round(1/1406, 6)`（更强、与既有测试一致） |
| D2 | 「在 `tools/overturned_events.py`（如不存在则从 573 设计恢复）中**加** …」 | 573 的设计**不在独立文件**，在 `metrics_collector.py` 内（`--log-overturned` + schema） | 新建独立模块并把 `metrics_collector` 旧实现**改为委托**（对外签名/错误文案/schema/只追加逐字保留，573 的 5 条回归锁一行未改、全绿） |
| D3 | — | `data/metrics.jsonl` 被 `.gitignore:88` 忽略（**未跟踪**） | 任务 1 采集的新行**不入库**（沿用 591 同源偏差）；通道文件 `data/overturned_events.jsonl` 不在忽略表 ⇒ 空文件本身入库 |
| D4 | 单测「小手工图（**5 命题 6 边**）」 | 本工具边**从库表推导**（每命题至少 2 条：命题↔本卡）⇒ 真实 schema 下"5 命题 = 6 边"不可得 | 手工图仍用 6 条边（5 命题 + 1 卡，含环与孤立点），但边以**内联边集**传入双实现（`closure_sql(..., edges=[...])` 走 `VALUES` 分支）⇒ 该条被逐字满足；库表推导路径另用 3 命题/8 边临时库单测覆盖 |
| D5 | 任务 4 未指明生成器 | — | 新增独立只读生成器 `tools/prop_network_inventory.py` + `--check`（不污染 `prop_closure.py` 的"无写调用"属性） |
| D6 | M5 survival「574 浮出 29 → **575 收口**」 | 台账实测：v3(574) `M5 escaped=29`、**v4(575) 仍 29**、v5(578) 才 0 | 条目记 `closed_in 575`（规则生效批次）+ **`measurement_visible_closed_in 578`**（度量可见收口），两个批次都写进 note，**不只留好看的那个** |
| D7 | 任务书未提 | `tools/metrics_collector.py` 的委托改动在任务 2 提交时**漏 add** | 补 commit `95eae3a`（补入库、无行为变化），并如实登记为流程失误 |
| D8 | `pytest -m "not slow" -n auto  # exit 0` | **exit 1**：① `test_governance_doc_guard_591.py::test_verify_real_manifest_matches` **串行也红** —— 591 的治理台账缺 **5 处新增** References 文档（592/593/594/PM 整理报告/PUSH 总览），全部是**人**在我开工前后新增的投喂词/报告，**本批未碰** manifest/scan（`git status` 空）；② `test_kg_stats_counts`、`test_replay_lock_serial.py::test_replay_serial_fixture_contract` 在 `-n auto` 下红、**串行全绿**（10 passed）⇒ 既有并发假红类 | ①**不修**（不在 592 边界：属 591 台账刷新 + 人审清单，擅自重扫会把未人审的 5 篇文档刷成"已过"）→ 交人（§7-4）；② 判为并发假红，按 MEMORY 记录口径处理，串行证据已贴 |
| D9 | 收工清单含 `prop_closure.py stats  # 79 命题` | 实测一致（79） | 无偏差 |

---

## §7 交人项

1. **metrics 新行需人审确认 curves 数字**：`data/metrics.jsonl` 末行（2026-09-19T16:30:51）
   `mutation_escape_rate` = **1/1406**，双侧 C-P95 `[1.8e-05, 0.003956]`（全精度 `cp_*_raw`）。该行**不入库**
   （gitignore），人审请直接看文件或 `metrics_collector.py history`。
2. **overturned 通道首次真实推翻事件需人审触发**：通道已建（0 事件）。写入接口 =
   `tools/overturned_events.py::append()`（或 `metrics_collector.py --log-overturned --target … --old … --new … --by human:<git名> --reason … --card <卡>`），
   human 须过 git 作者绑定，否则 fail-closed 拒写。**系统绝不自动产生推翻**。
3. **`data/prop_network_inventory.md` 中闭包异常命题需人审确认**：当前 **0 条**（>50 或 =1 皆无）。
   台账另有 2 项既有知识债（**非本批引入、本批不动**）：observation 命题 **50 条全部缺活性锚**
   （`data/prop_liveness_todo.md` 同源）、`verified_by_oracle` **0 张卡填**（放权开关全 OFF）。
4. **591 治理台账已过期（预存在，非本批）**：`governance_doc_guard.py verify` 报 **5 处新增**
   （592/593/594/PM_产品经理仓库整理报告/PUSH_健康状态总览）⇒ 需人决定是否
   `governance_doc_guard.py update` 重扫（重扫会把 5 篇未人审文档刷进 manifest，**属人审权力，本批不代做**）。
   这也是 fast 套件当前唯一"串行仍红"的用例。
5. **`-n auto` 并发假红类**（预存在）：`test_kg_stats_counts`、
   `test_replay_lock_serial.py::test_replay_serial_fixture_contract` 在 `-n auto` 下红、串行绿
   （建议按 MEMORY 口径挂 `replay_serial` / 进 `SERIAL_EXTRA`，属测试卫生批次）。
6. **M5 survival 的"收口批次"口径**（D6）：规则生效在 575、度量可见在 578 —— 若监工认为应统一按
   度量可见批次记 `closed_in 578 / batches 4`，本批按"规则生效 = 1 批"记，请裁决。

