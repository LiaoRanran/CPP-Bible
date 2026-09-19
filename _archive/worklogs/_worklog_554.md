# _worklog_554 · 批次 T —— 成熟测试库加固（Hypothesis 状态机 / syrupy 快照 / parser 差分）

> 任务：554。范围纪律：**纯测试/分析侧**，不改任何正式判定逻辑；依赖只进 `[dev]`。
> 解释器：`.venv\Scripts\python.exe`。前置：553 已验收合入（T3 不再等待）。

---

## 一、开工基线（本会话 HEAD=c15614e，即 553 合入后、554 未动）

| 项 | 值 |
|---|---|
| `gate --check` | 规则 61 · 命中 141（block=0 warn=136 advice=5） |
| `replay --check` | confirm=56 refute=0 infra_error=0（共 56 卡） |
| `poison`（台账） | 攻击面覆盖 11/11 · RULE-COVERAGE 36/61 + 豁免 27 |
| `git status`（受控目录） | 仅 `evidence/conc/EV-CONC-001.md M`（pre-existing，未触碰）+ 若干 pre-existing 未跟踪文件 |

---

## 二、交付（一任务一 commit）

| commit | 内容 |
|---|---|
| `c5dbe6c` | **T0**：`pyproject.toml` dev extras 加 `hypothesis>=6.100` / `syrupy>=4.7`；`uv export` 重生成 `requirements.lock.txt`（含哈希） |
| `f118866` | **T0-fix**：补提交 `uv.lock`（uv 原生锁，含 hypothesis/syrupy/sortedcontainers @ `extra == dev`） |
| `625a0b5` | **T1b**：`tests/test_task_queue_stateful.py`（RuleBasedStateMachine + 三洞确定性回归） |
| `4918f75` | **T1b-fix**：消除状态机 flaky（FlakyStrategyDefinition） |
| `fff577e` | **T2**：`tests/test_output_snapshots.py` + `tests/__snapshots__/test_output_snapshots.ambr` |
| `5cfd378` | **T3**：`tests/test_parser_differential.py`（三解析器一致性 / 547 B5 回归） |

**T1a 结论（侦察后）**：`task_queue.py` 的库函数（`_connect/enqueue/claim/checkpoint/heartbeat/yield_task/complete/done/fail/blocked/next_task/list_tasks/...`）**全部已接受 `db_path`**，DB 路径本就可注入 ⇒ **无需最小可测性改造，T1a 不产生 commit**；实测机器把库重定向到 `tempfile` 临时 sqlite，**绝不打真实 `data/tasks/`**。

---

## 三、T2 首次快照基线（**已人审**）

`tests/__snapshots__/test_output_snapshots.ambr` 首次基线值，逐条核对（与开工 gate 基线一致）：

- **gate**：`rules=61` `block=0` `warn=136` `advice=5`（= 开工「规则 61 · 命中 141」）✅ 一致
- **kg stats**：`nodes=326 edges=291 card_nodes=165 concepts=157 concept_edges=79 concepts_multi_atom=0 max_component=3 dangling=3`；
  `nodes_by_type={ARTIFACT:51, ATOM:30, EVIDENCE:56, FIXTURE:49, MISCONCEPTION:79, RULE:61}`
- **poison（live rule_coverage）**：`covered=36 total=61 uncovered=[]`；`attack_taxonomy=A1..A11`
- **poison（已提交台账 surface_map）**：`drill 92/92`；`coverage 11/11`；`rule_coverage covered=36 / exempt=27 / total=61`
- **mutation**：`variants=5 blocked=4 escaped=0 n_a=1 strict_blocked=4 strict_rate=1.0 treated_rate=1.0`

> 声明：**以上基线值我已人审**，与开工记录一致，未包含任何动态字段（timestamp/绝对路径/耗时/commit/分隔符均在构造待快照 dict 时排除）。
> 纪律：本批**未在同一 commit 里既改逻辑又 `--snapshot-update`**；本批未改任何判定逻辑，故基线即"现状快照"。

---

## 四、收工验收

| 判据 | 结果 |
|---|---|
| `pytest -m "not slow" -n auto` | ✅ 全绿（连续 4 次，~63s） |
| `pytest -m slow -n0` | ⚠️ **仅 1 条 pre-existing 失败**（见下）；deselect 该条后**全绿**（100%，exit 0） |
| `gate --check` | ✅ 规则 61 · 命中 141（block=0 warn=136 advice=5）—— **与开工逐字一致** |
| `replay --check` | ✅ confirm=56 refute=0 —— 与开工一致 |
| `poison` | ✅ 覆盖 11/11 · RULE-COVERAGE 36/61+27 —— 与开工一致 |
| 依赖隔离（核心不装 dev 仍可跑 gate） | ✅ T0 已验证（gate 不 import hypothesis/syrupy） |
| `git status`（受控目录） | ✅ 仅 pyproject/lock/uv.lock + tests/ 新增；`EV-CONC-001.md M` 为 pre-existing |

**新增测试点数 = 16**：T1b `test_task_queue_stateful.py` 7 点（6 确定性 + 1 状态机）、T2 `test_output_snapshots.py` 5 点（5 快照）、T3 `test_parser_differential.py` 4 点。
**stateful 实测耗时**：`max_examples=120` → 单跑 50–67s（含确定性共 ~66s）。**零违例** ⇒ 未发现新 bug，A3/A5/A7 三洞回归锁已就位。

### ⚠️ pre-existing 失败（**非 554 引入**，且本批无权修复）

- 用例：`tests/test_json_output.py::test_golden_lock_json`（断言 golden_lock `status==pass`，实得 `fail`）。
- 根因：`golden_lock check` 报 **`warn_findings: 59 → 136`** —— 已签署基线（`tools/golden_state.json`，最后一次 accept 在 `67c1962`，warn 54→59）**落后于**其后 `gate_engine` 新增规则（548 系列 / 553），当前 warn 已达 136。
- 证据链：开工（HEAD=`c15614e`，553 后、554 前）`gate --check` 已是 `warn=136`，而基线 59 ⇒ 该用例在**本批开工前就已红**；554 全程**未改 `tools/`**、warn 数 **136→136 未变**。
- 处置：修复需人工 `golden_lock check --accept`（**554 硬纪律明令"不 golden accept"**）⇒ 超出本批范围，如实上报，**不代签**。

---

## 五、过程发现（非 bug，口径修正）

- **T1b 调试插曲**：曾误报 `complete 无此任务`，根因是**测试第三处 `complete` 漏传 `db_path`**（读到真实库），**非 task_queue bug**，已修。
- **T1b flaky**：`hypothesis.errors.FlakyStrategyDefinition: Inconsistent data generation` —— 机器用 `st.sampled_from(变长外部状态)` 建策略。修法：固定整数策略 + 取模索引；并抑制全部健康检查（触真实时钟/sqlite/临时目录）。**未改任何判定逻辑**。
- **T3 口径修正**：初版谓词 P2 要求 `negative_controls` 必须是 `list[dict]`，误把"nc 为 map"判成灰色态——但该例两解析器**判决一致**（都收成 dict），只是 schema 非法（属 gate 的 `check_negative_controls` 职责）。已把 P2 收紧为"**仅两侧形状分歧时**要求硬化层 block"。

---

## 六、结论

554 批次 T 三项任务（T1 stateful / T2 快照 / T3 差分）交付完成，新增 16 个测试点全部计入 **fast** 组；未改任何正式判定逻辑，gate/poison/replay 数字与开工一致；stateful `max_examples=120` 零违例。唯一红旗是**本批开工前就存在的** `test_golden_lock_json`（golden 基线漂移），按硬纪律不在本批代签修复。
