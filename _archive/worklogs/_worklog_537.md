# 537 苦力白天收尾施工日志（535 遗留机械活 · T1–T7）

> 依据：`References/architecture_架构演进/537_苦力白天收尾_535遗留机械活.md`
> 纪律：每条独立 commit；不 push；不 `--no-verify`；不 golden accept；不改 56 卡信任结论；新规则先 warn 后 block；**做不完停在 T 边界，不留半成品**。

## 幂等进度看板（新会话从这里续）

```
T1 V-iso 毒样例 N1–N7 进 poison        [ ] 未开始（施工点见 §3.1）
T2 增量指纹 .out 缺口                  [x] 实测已覆盖，不做（证据见 §2，无 commit）
T3 observation 活性判据拦自标绕过       [x] 实测已覆盖，不做（证据见 §2，无 commit）
T4 complete touch 审计沙箱豁免         [x] a804ef0（+1 例）
T5 warn 136 四桶分类建议文档           [ ] 未开始（施工点见 §3.2）
T6 CI ruff 存量 15 项                  [ ] 未开始（施工点见 §3.3）
T7 V-iso 56 卡迁移 backlog 文档        [ ] 未开始（施工点见 §3.4）
```

## 0. 开工基线（亲手实测，HEAD=`ee1d7c8`，与 535 收工同一 fresh run）

| 项 | 实测 |
|---|---|
| `gate_engine.py --check` | `[gate] 规则 60 条 · 命中 141 (block=0 warn=136 advice=5)` |
| `poison_drill.py` | `90/90`；`RULE-COVERAGE 35/60`（豁免 27）；`零覆盖攻击面：无` |
| `atom_evidence_replay.py --check --no-sanitizer` | `confirm=56 refute=0 infra_error=0`（全量 167.1s；增量 0.3s 全命中缓存） |
| `pytest -m fast -q` | **274 passed** |
| `knowledge_graph.py` | 325 节点 / 291 边；conflicts 候选 1 组 |
| `tool_integrity.py` | `OK：5 个核心工具与基准一致` |

---

## 1. T4 · complete touch 审计的沙箱正式豁免（**已完成**，`a804ef0`）

**问题**：535 C6 的收尾审计按规格只豁免 `data/tasks/**`，在真实仓库跑一次会列出 **772 个**未跟踪沙箱文件（`_arch_*/_adv_*/_worklog_*/_t53*`…）⇒ 告警疲劳，真漏报会被噪声淹没。

**做**（选 537 给的第二个方案：集中常量放 `task_queue.py` 内，与审计同文件、不新增跨模块依赖）：

- 新增 `SANDBOX_GLOBS = ("_arch_*", "_adv_*", "_worklog_*", "_t*", "_po*", "_rp*")` 与 `_is_sandbox_path(rel)`；**只看路径第一段**。
- `_touch_audit` 豁免集合 = handoff_path + 声明 touch_set + `data/tasks/**` + 沙箱白名单。
- 纪律写进注释：白名单**显式可审**（新增前缀必须加一行），正式目录（tools/tests/atoms/evidence/Book/Examples）内一切**永不豁免**——`atoms/_t_x.md` 这种"文件名像沙箱"的照样报。

**验收实测**：`pytest tests/test_task_queue.py -q` → **47 passed**（+1 例：沙箱目录不报 / 正式目录未声明文件仍被抓 / 白名单可审 / 正式目录内文件名像沙箱也不豁免）；ruff 0.6.9 `All checks passed!`；gate/poison/replay 与开工逐字一致（见 §4）。

---

## 2. T2 / T3 · 核实后判定"已覆盖，不做"（无 commit，附证据）

### T2 增量指纹的 .out 缺口 —— **实测已覆盖**

- 磁盘现状：`tools/atom_evidence_replay.py` 的 `card_fingerprint` 已把 `actual.run_match_file` 指向的 `.out` **字节**计入指纹（缺文件 ⇒ `MISSING` 强制重跑）；本轮 535 V3 又追加了 `negative_controls[*].fixture` 字节。
- 既有回归锁（`tests/test_incremental_replay.py`，530 T1 落）：`test_card_fingerprint_sensitive_to_out_530`（改 `.out` 必改指纹 / 缺 `.out` ⇒ MISSING）、`test_card_fingerprint_ignores_undeclared_out_530`（旧形态卡不受影响，逐字节一致）。
- 结论：**不改代码、不加重复测试**（537 §T2 已给此分支："若已含则在 worklog 写'实测已覆盖，不做'"）。

### T3 observation 活性判据能否拦"自标绕过" —— **实测拦得住**

- 磁盘现状（行号按当前磁盘，规格说的"约 940 行"已漂移到 2000+，**以磁盘为准**）：
  - **第 0 层（block，零容忍）**：`OBSERVATION-NEEDS-ARTIFACT`（`tools/gate_engine.py:2049` 定义、`:2079` 注册）——observation 必须挂工件断言载体，否则直接 block。
  - **第 1 层（warn 观察期）**：`OBSERVATION-LIVENESS`（`:2087` 三条活性条件单点判定、`:2143` 规则）——自标观测还须"活的观测"（量化证伪 / 夹具特有符号 / 非环境量 run 键，至少其一）。
  - 毒样例：`P68`（只挂 run_match 卡的 observation 须 warn）与 `P68-阴`（有活性对照须放行）在 `tools/poison_drill.py:1513/1533`，并登记 `ATTACK_TYPES`（`:1642`，归 A1）。
- 实测：`pytest tests/test_gate_engine.py -q -k observation` → **7 passed**；poison 90/90（含 P68 对）。
- **诚实边界**：第 1 层是 **warn 不是 block**（530 的刻意设计：先看见全库曲线再谈升级）；第 2 层（V-iso `OBSERVATION-NEEDS-CONTROL`）尚未注册。故"把推断自标 observation"当前**会被看见但不会拦死**——升级为 block 只允许走 G-iso 开关/人裁，**不是苦力能做主的**。→ 交人（见 §5）。

---

## 3. 未做的 T（施工点写清，照做即可）

### 3.1 T1 · V-iso 毒样例 N1–N7 进 poison

- 现成资产：`_arch_v2_round2/probe_fence_iso/` 的 6 个攻击阴面 + `tools/viso_diff.py` 判据 + `tests/test_viso_diff.py` 的 41 例（已逐类锁判据）。
- 缺的是**端到端**：在 `tools/poison_drill.py` 里按既有体例（tempdir 沙箱、真调 g++、断言 verdict/拦截规则）建 N1–N7 卡+夹具对，期望判决照 533 §2.5 表：
  N1 阳=阴复制 ⇒ `negative_control_passed`（diff 侧先拦零语义）；N2 冒名 ⇒ `_diff` 且 reasons ≥3；N3 阴面写坏（同次阳面 rc=0）⇒ `_broken` **不得落 infra**；N4 形式阴面（42→43 / 删 anchor 外）⇒ `_diff`；N5 阴面缺失 ⇒ `_missing`；N6 连主体删 ⇒ `_diff`（retain 缺 + 比率兜底）；N7 干净卡 ⇒ confirm 不变。
- 注意（537 已点明，实测同款坑）：poison 覆盖判定只认字面量 `"RULE-ID" in who`，参数化比较会"样例过但规则算未覆盖"，必须照既有写法补 `RULE-COVERAGE`（并重算 `poison_surface_map.json` 台账）。
- 验收：N1–N6 `trap_block_rate=100%`、N7 `clean_pass_rate=100%`；poison 全过、无新增 uncovered、存量 0 新 block。
- 判决实现已在 `tools/atom_evidence_replay.py::check_negative_controls`（535 V3），毒样例只需把 verdict 字符串断言上。

### 3.2 T5 · warn 136 四桶分类建议文档

- 现成命令：`.venv\Scripts\python.exe tools/golden_lock.py buckets`（逐规则计数）+ `check`（同一批命中的逐条明细）。
- 530 已盘出的存量构成（可直接引用，但**要重新实测**）：`ATOM-CLAIM-CONCEPT-NORMALIZED 77`、`INFERENCE-NOT-MACHINE-VERIFIED 28`、`EV-MATRIX-UNBACKED 16`、`EV-OUT-UNDECLARED-KEY 6`、`EV-FALSIFICATION-QUANT 4`、`ATOM-REL-TARGET 2`、`EV-ASSERT-SYMBOL-MAPPED 2`、`EV-SERVES-EXIST 1`；其中 79 条 object 非概念名（真债，清单见 `_worklog_530.md` §4）、28 条 inference 卡级签署中间态（建议 `legacy`）、16 条 EV-MATRIX 分 A/B/C 三类（A 6 卡待补外部锚 ⇒ 建议 `false_positive`；B 7 卡零留痕 ⇒ `real`；C 3 卡假锚 ⇒ `real` 并触发 §6.4 缺陷）。
- 产出 `docs/kernel/warn_136_分类建议.md`：规则 / 卡 / 桶 / 建议理由，**不执行 `--accept`**（认可权唯人）。
- 注意：分类是**人审动作**，文档只能给"建议值 + 理由"，不得写成既成事实。

### 3.3 T6 · CI ruff 存量 15 项

- 口径必须钉版本：`uv tool run --from ruff==0.6.9 ruff check tools/`（本地 PATH 的 ruff 0.16.5 会虚增到 803 项，**不可用于判 CI 口径**）。
- 归属已由 530 §6.6 盘清：`gate_engine.py:2076 F541`、`:3100 E741`、`poison_drill.py:1193 E741`、`:1806 E401`（本批已改过这两个文件，行号会漂）+ 未改文件 11 项（`artifact_version_stamp.py` F401、`backup.py` F401、`book_atom_sync.py` F541×3、`cost_tracker.py` E731+F841、`env_check.py` E401+E741×2、`metrics_collector.py` F401）。
- 9 项可 `--fix` 安全自动修；6 项（E741×3/E731/F841）需逐个判语义后手改并在 commit 里写清语义。**改完必须复跑全量 fast pytest**（改的是工具代码）。
- ⚠️ 本条会动**未改过的**文件，属"扩范围"，建议**独立小任务**做，别和其它 T 混在一个 commit。

### 3.4 T7 · V-iso 56 卡迁移 backlog 文档

- 数据源：`_arch_v2_round2/survey_cards.py` / `survey_props.py`（可复跑）+ 533 §2.4 的分批结论（B1 asm 11 命题/13 卡、B2 run 双路径 14 命题/14 卡、B3 24 命题、不迁 5 卡）。
- 产出 `docs/kernel/viso_migration_backlog.md`：每卡标 **候选通道**（artifact 计数 / run 键 / 结构性做不出）、**anchor 候选**（夹具里的自由函数名）、优先级（B1→B3）、以及"做不出阴面的机器理由"（B 档三判据）。
- 只出清单：**不改任何卡、不自动降级 claim_type**（错降级率是观察期指标，改 type 永远是人/红队动作）。

---

## 4. 收工门禁（fresh run，HEAD=`a804ef0`，串行执行）

| 门禁 | 实测 | 判定 |
|---|---|---|
| `gate_engine.py --check` | `规则 60 条 · 命中 141 (block=0 warn=136 advice=5)` | ✅ 与开工逐字一致（T4 未碰规则） |
| `poison_drill.py` | `90/90`；`RULE-COVERAGE 35/60`（豁免 27）；`零覆盖攻击面：无` | ✅ |
| `atom_evidence_replay.py --check --no-sanitizer` | `confirm=56 / refute=0 / infra_error=0`，全量 **173.4s** | ✅ |
| replay `--incremental` | 56 张全部命中缓存，0.3s 级 | ✅ |
| `pytest -m fast -q` | **275 passed**（274 → +1 = T4 的用例） | ✅ |
| ruff 0.6.9（改动文件） | `tools/task_queue.py` + `tests/test_task_queue.py` → `All checks passed!` | ✅ |
| `tool_integrity.py` | OK（T4 未碰被钉核心工具） | ✅ |
| 受控目录 / 56 卡 | 未动任何卡、未动 `golden_state.json` | ✅ |

**537 交付**：1 个 commit（`a804ef0`）+ 2 条"实测已覆盖，不做"的核实结论；本地 **ahead 13 个提交（未 push）**。

---

## 5. 做不了 / 交人（诚实清单）

1. **T1/T5/T6/T7 未做**——都是"照规格机械做"的活，施工点见 §3；本会话上下文预算见底，按纪律**停在 T 边界**（未留半成品：正式代码里只有 T4 一处改动，且自带回归锁）。
2. **T3 的层级问题交人**：`OBSERVATION-LIVENESS` 目前是 **warn**（530 刻意设计），自标 observation **会被看见但不会拦死**；升 block 的唯一入口是 G-iso 开关（条件：迁移卡 0 误伤 + N1–N6 100% 拦截 + NC 一次通过率 ≥70%），**需人裁**，苦力不得自行升级。
3. **T2 无需动作**：指纹已含 `.out`（530 T1 落 + 两个既有用例），规格里的"若已含则不做"分支成立。
4. **T6 建议独立小任务**：会动 8 个此前未改过的文件（F401/F541/E731/E741/F841），需逐个判语义 + 全量 pytest，不适合与其它 T 混批。
5. 沙箱未跟踪目录（`_arch_*`/`_adv_*`/`_t537_p.txt`/`_worklog_*`）不入库；T4 落地的白名单让 `complete` 审计不再被它们淹没（这本身是 T4 的验收面）。

## 6. 关键证据复跑命令

```powershell
# T4：沙箱不报、正式目录仍抓
.venv\Scripts\python.exe -m pytest tests/test_task_queue.py -q -k t4

# T2：.out 进指纹（530 T1 既有锁）
.venv\Scripts\python.exe -m pytest tests/test_incremental_replay.py -q -k out_530

# T3：活性判据 + 自标绕过毒样例
.venv\Scripts\python.exe -m pytest tests/test_gate_engine.py -q -k observation
.venv\Scripts\python.exe tools/poison_drill.py | Select-String "P68|90/90"

# T5/T7 起步命令
.venv\Scripts\python.exe tools/golden_lock.py buckets
.venv\Scripts\python.exe _arch_v2_round2\survey_cards.py
```
