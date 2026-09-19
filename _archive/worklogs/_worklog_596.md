# 596 worklog：攻击关系数据地基 + W2 加权 AF 落地

仓库：`CPP-Bible`；解释器：`.venv\Scripts\python.exe`（Py3.13，纯标准库，无 scipy/numpy/networkx）。
批次边界：只新增 `tools/attack_edge_generator.py` / `tools/weighted_af_solver.py` / `tools/grounded_audit.py` /
`tools/attack_edge_review.py` + `tests/test_*_596.py` + `data/attack_edges_candidates.jsonl` /
`data/grounded_labels_w2.json` / `data/grounded_audit_report.md` / `data/human_attack_edge_annotations.jsonl`；
**不碰 CORE 五文件、不碰 prop_graph.py、不改任何卡**；不 push、不 golden accept。

---

## 任务 0：开工先量（实跑，无 commit）

| 项 | 命令 | 实测 |
|---|---|---|
| tool_integrity | `--check` | exit **0**（5 核心工具与基准一致） |
| gate | `gate_engine.py --check` | exit **0**；**规则 63 · 命中 191（block=0 warn=186 advice=5）** |
| prop_graph | `prop_graph.py stats` | **79 命题 / 27 卡** · inference 29 / observation 50 · 签署 card_signed 76 / unsigned 3 · 机验 79 |
| 误区库 | `misconceptions/MIS-*.md` | **79 个文件**（字段齐：id/name/level/domain/trigger_patterns/refutations/source/related_atoms 各 79 张都有该键） |
| 带 `related_atoms` | 独立复算 | **42 个 MIS**（另 37 个该字段为空） |
| 候选边（MIS→命题） | 独立复算 | **194 条**（每 MIS 去重后 min 2 / max 12 / avg 4.619） |
| 关联原子卡 | 独立复算 | **25 张不同原子卡**；**0 张悬空引用**（引用的卡全部存在且有命题） |
| 命题 id 总数 | — | 节点 = 79 命题 + 42 MIS = **121** |
| MIS 可信度字段 | 独立复算 | `verified_by` **0 张**、`machine_verified` **0 张** ⇒ 全部落 `low` |
| 原子卡可信度字段 | 独立复算 | `verified_by` 非空 **26/27**；`machine_verified` **0/27**（命题级 `signed_by` 0 条） |
| 另一条潜在种子 | 独立复算 | **8 张原子卡**有 `misconceptions: [MIS-…]`（反向字段），**79 张 MIS 均无该字段** |
| refutations 总数 | 独立复算 | **160 条** |

**关键核实（任务书任务 0 要求）**：594 说的「42 MIS 带 `related_atoms` / 194 条候选边」**独立复算完全一致**（非照抄）。
另发现 594 未提的一条事实：反向种子 `misconceptions` 在**原子卡**上有 8 张（MIS 侧 0 张）——
本批生成规则按任务书写的是"遍历 MIS 文件读 `related_atoms` 和 `misconceptions`"，故该反向字段
**不参与**生成（否则边数会 ≠ 194）；如实登记为偏差 D5。

---

## 任务 1：候选攻击边自动生成（`tools/attack_edge_generator.py`）

### 做什么
- 生成规则（严格按 596 任务1）：MIS `related_atoms`（→ 原子卡的**全部**命题）⇒ `mis_to_prop`
  （kind `related_atom`）；MIS `misconceptions` 字段同样解析为卡 id ⇒ kind `misconception`
  （当前 0 张 MIS 有该字段 ⇒ 0 条，规则保留并有沙箱正例）；**每条 `mis_to_prop` 再配一条对称边**
  `prop_to_mis`（kind `misconception_refutation`）——594 实证没有对称边就退化。
- 字段：`id`(= `ae-{source}->{target}`) / `source` / `target`(= `卡id::prop-N`) / `kind` / `evidence`
  (= 该 MIS 的 `refutations` 拼接后前 200 字) / `confidence`(high|medium|low) / `direction` /
  `generated_at` / `generator_version`。
- 去重：同 `(source, target, kind)` 只留可信度最高。
- CLI：`generate` / `stats` / `--check`（独立复算 + 字段完整 + source/target 存在 + 无重复；失败 exit 2）。

### 实测
- `generate` → exit **0**：**388 条**（`mis_to_prop` 194 + `prop_to_mis` 194）· kind
  `{related_atom: 194, misconception_refutation: 194}` · **confidence 全 `low`**（MIS 卡面无可信度字段，
  实测事实，不假装有分级）· source MIS 42 个（另 75 个 target 侧）· 文件 227 KB。
- `stats` → exit **0**（总边 / 按 kind / 按 confidence / 按 direction / 按 source Top5 / 按 target）。
- `--check` → exit **0**（388 条：独立复算一致 · 字段完整 · source/target 存在 · 无重复）。
- 新增 `tests/test_attack_edge_generator_596.py`：**10 passed**（正例成对边 + 字段 + 分级 /
  无反例三连（无关联、悬空卡告警不崩、重复去重、无 claim_structured）/ 幂等逐字节 / `--check`
  正反例 + CLI 退出码 / **真实语料独立复算 42+194+388**）。ruff **All checks passed**。

### 偏差 D4（幂等的代价）
任务书同时要求「每条边带 `generated_at`（ISO 时间）」与「幂等：连续生成两次输出逐字一致」——
两者本质冲突（时间戳就是变化源）。处理：字段保留但**默认 `null`**，需要打点时显式 `--now <ISO8601>`；
对账靠内容而非时间戳。测试锁"两次生成逐字节一致"。

### 偏差 D5（反向种子不参与生成）
实测 **8 张原子卡**有 `misconceptions: [MIS-…]`（反向字段），而 **79 张 MIS 无该字段**。
任务书生成规则写的是"遍历 MIS 文件读 `related_atoms` 和 `misconceptions`"⇒ 反向字段不产边
（否则边数 ≠ 194）。**后果**：`ATOM-CONC-FENCE-001` / `ATOM-CONC-LOCK-001` 的 4 条命题
没有任何误解攻击（任务 3 审计里会显形为"无攻击者的 IN 命题"）。若要合并反向种子，边数须重定基线，交人裁决。

commit：`c2a12ba`

---

## 任务 2：W2 加权 AF 求解器（`tools/weighted_af_solver.py`）

### 做什么
- 节点 = 79 命题（`卡id::prop-N`）∪ 边里出现的误解（实测 42）= **121**；
- **可信度**：命题 = 命题级 `signed_by`→high(3) / 卡级 `verified_by` 或 `machine_verified`→medium(2) / 否则 low(1)；
  误解 = 其候选边的 `confidence`（实测全 low(1)）⇒ 命题 2 > 误解 1；
- **击败关系**：`cred(A) > cred(B)`（**严格大于**）才构成击败；
- **grounded 不动点**：`IN` ⇔ 全部（击败意义下）攻击者 `OUT`；`OUT` ⇔ 存在 `IN` 的攻击者；最多 100 轮（超限 fail-loud）；
- 输出 `data/grounded_labels_w2.json`（入库）：逐节点 `id/type/label/attackers/defeated_attackers/defenders`
  + 命题附 `card/claim_type/signoff_state`；CLI `solve/stats/--check`。
- 另附**对照实现** `w1_threshold_labels()`（594 W1：阈值二值化、不做可信度比较），docstring 明写"已知失败、
  仅供复现"，让"为什么选 W2"在仓内可执行。

### 一次真实翻车与修正（如实登记 D6）
初版把「**全部**攻击边」用于 IN 判定、只用「**击败边**」用于 OUT 判定 ⇒ 两个关系不一致，
迭代互相卡死：实测 **IN=4 / OUT=0 / UNDEC=117**（全部误解 UNDEC，只有 4 条无攻击者的命题 IN）。
**根因**：W2 的语义是"不构成击败的攻击**不算攻击**"，两个判定必须用**同一个**关系。
修正为「击败关系即攻击关系」（`_defeat_attackers()` 单点定义 + docstring 留坑注释）⇒ 立刻复现 594：
**IN=79 / OUT=42 / UNDEC=0（3 轮收敛 · 击败边 194/388）**。
附带修掉一个健壮性 bug：`--check` 读到结构不完整的 JSON 时抛 `KeyError`（应为干净 exit 2）——
现在先校验必需键，缺键 ⇒ exit 2 并说明。

### 实测
- `solve` → exit **0**：节点 **121**（命题 79 / 误解 42）· **IN 79 / OUT 42 / UNDEC 0** ·
  3 轮收敛 · 击败边 **194/388** · 命题标签 `{IN: 79}`、误解标签 `{OUT: 42}`。
- `stats` → exit **0**：平均攻击者 3.21（命题 2.46 / 误解 4.62）· 平均辩护者 5.09。
- `--check` → exit **0**（与 594 实证 IN=79/OUT=42/UNDEC=0 一致）。
- 新增 `tests/test_weighted_af_solver_596.py`：**9 passed**（沙箱小图 / 真实数据对账 + 字段契约 /
  **反例 1** 缺对称边两种走法都退化 / **反例 2** W1 阈值扫描 θ∈{0,0.2,…,1.0} 误解恒 IN /
  **反例 3** 可信度相等不构成击败（严格大于）/ 不动点 <100 轮 / `solve` 幂等 / `check` 三重可证伪 /
  CLI 退出码）。ruff **All checks passed**。

commit：`574707e`

---

## 任务 3：grounded 标注实测与对照（`tools/grounded_audit.py` → `data/grounded_audit_report.md`）

### 做什么
只读生成器（`--check` 检测报告过期/异常，**零写入**），六节：§1 总览 · §2 与 `claim_type` 对照 ·
§3 与 replay verdict 对照 · §4 辩护链示例（攻击者最多的 3 个 IN 命题）· §5 异常检测 · §6 与 594 对账。
**异常 fail-loud**：命题 OUT / 误解 IN / UNDEC 三类 ⇒ 报告 §5 标 ❌ 清单，且生成器 **exit 2**
（报告仍落盘供人读）——"全绿"和"没检查"绝不许看起来一样。

### 实测
- `grounded_audit.py` → exit **0**（报告 83 行，无异常）；`--check` → exit **0**。
- §2：observation 50 / inference 29，**全 IN**。
- §3：引用卡 replay 归类（来源 = `build/replay_manifest.json`，56 张实跑）：**confirm 79 / refute 0**，全 IN；
  误解 `refutations` 条数分布 `{1:2, 2:28, 3:9, 4:3}`（判决由可信度决定，与反驳条数无关）。
- §4 辩护链示例（如 `ATOM-UB-GRAY-001::prop-1`，10 个误解攻击它，全部 OUT、各被 2 条命题击败）。
- §6 与 594 对账四行全 ✓。
- 新增 `tests/test_grounded_audit_596.py`：**5 passed**（六节 + 对账 / 注入 OUT 命题 + IN 误解 ⇒
  报告标 ❌ 且 CLI exit 2 / UNDEC 亦异常 / 幂等 + `--check` 正反例 / 已提交报告与现读事实源逐字节一致）。
  ruff **All checks passed**。

commit：`d989d5d`

---

## 任务 4：候选攻击边人审接口（`tools/attack_edge_review.py` + W2 集成）

### 做什么
- `data/human_attack_edge_annotations.jsonl`（**0 字节，入库**，只追加）；记录
  `{edge_id, action, reason, reviewer, timestamp[, new_confidence]}`。
- CLI：`list [--status]` / `show <id>` / `approve|reject|modify <id> --reason …` / `stats` / `--check`。
- **fail-closed**（一行都不写）：缺 `--reason` / `action` 非法 / `edge_id` 不存在 /
  `modify` 缺 `--confidence` / 取不到 `git config user.name` / **冒名**（`--reviewer` ≠ 当前 git 作者）/
  git 不可用 / 审查人不是该边**误解卡**最后一次 git 提交作者（与 573 推翻通道同款绑定；实测
  `git user.name=LiaoRanran` 与 `MIS-*.md` 最后提交作者一致 ⇒ 正常路径可用）。
- 生效规则（**同一 id 取最后一条**，历史全留）：`reject` 剔除 · `approve` 升一级（low→medium→high）·
  `modify` 指定档。**只剔除被审的那一条**（对称边要另审，docstring 写明）。
- W2 集成：`weighted_af_solver.py solve` 新增 `--include-human-reviewed`（**默认开启**）与
  `--annotations`；打印"边 388 ⇒ N（剔除 k 条被拒边）"。**人审一旦真介入** ⇒ `--check` 自动退化为
  只查结构不变量（594 基线只对"未审候选图"权威）——不拿旧基线去卡人审结果，也不假装仍一致。

### 实测
- `stats` → exit **0**：候选边 388 · **待审 388** · 已确认/已拒绝/已改权 0（初始）。
- `list` → exit 0（388 条 · pending）；`--check` → exit **0**（0 条记录）。
- `solve`（默认含人审）→ exit **0**，`IN 79 / OUT 42 / UNDEC 0` 不变（空标注 ⇒ 无影响）。
- 新增 `tests/test_attack_edge_review_596.py`：**12 passed**（approve/reject/modify 三条路径 ·
  只追加历史 + 最后一条生效 · 五类 fail-closed · 生效规则三条 · **W2 集成：reject 掉某误解全部"被击败"边
  ⇒ 该误解真的翻成 IN（IN_misconceptions=1）** ⇒ 人审有后果 · CLI 全量往返 + `--check` 正反例 ·
  真实标注文件为空且合法）。ruff **All checks passed**。

commit：`2af99a3`

---

## 任务 5：收工总验收（fresh，串行，退出码定论）

| # | 命令 | 退出码 | 结果 |
|---|---|---|---|
| 1 | `tool_integrity.py --check` | **0** | 5 核心工具与基准一致（本批未改 CORE ⇒ 无需重钉） |
| 2 | `tool_integrity.py --check-test-config` | **0** | 2 个测试器配置与基准一致（本批未改 conftest.py） |
| 3 | `gate_engine.py --check` | **0** | **规则 63 · 命中 191（block=0 warn=186 advice=5）**逐字同基线 |
| 4 | `poison_drill.py` | **0** | **124/124** · RULE-COVERAGE 39/63 · 表观 100.0% · 诚实 95.2%（逐字同基线） |
| 5 | `atom_evidence_replay.py --check` | **0** | **confirm=56 refute=0 infra_error=0**（逐字同基线） |
| 6 | `attack_edge_generator.py generate` | **0** | 388 条（重跑逐字节幂等） |
| 7 | `attack_edge_generator.py --check` | **0** | 独立复算一致 · 字段完整 · source/target 存在 · 无重复 |
| 8 | `attack_edge_generator.py stats` | **0** | 总 388 · kind {related_atom 194, misconception_refutation 194} · confidence 全 low |
| 9 | `weighted_af_solver.py solve` | **0** | 节点 121 · **IN 79 / OUT 42 / UNDEC 0**（3 轮 · 击败边 194/388） |
| 10 | `weighted_af_solver.py --check` | **0** | 与 594 实证一致 |
| 11 | `weighted_af_solver.py stats` | **0** | IN 79 / OUT 42 / UNDEC 0 · 平均攻击者 3.21（命题 2.46 / 误解 4.62）· 平均辩护者 5.09 |
| 12 | `attack_edge_review.py stats` | **0** | 候选边 388 · **待审 388** · 已确认/拒绝/改权 0（初始） |
| 12b | `grounded_audit.py --check` | **0** | 报告与事实源一致且无异常（额外项） |
| 13 | `pytest -m "not slow" -n auto` | **1** ⚠️ | **541 passed / 1 skipped / 1 failed** —— 唯一红 = `test_governance_doc_guard_591.py::test_verify_real_manifest_matches`（**预存在、与本批无关**，见 D7） |
| 14 | `pytest -m slow -n0`（**分批 5 块**，合计 340 例） | **1** ✓预期 | 132+80+57+39 = **308 passed**、末块 **31 passed / 1 failed** ⇒ **唯一红 = `test_json_output.py::test_golden_lock_json`**（golden 待人工 accept，预期红） |
| 15 | `ruff check`（本批 8 个 .py） | **0** | **All checks passed** |
| 16 | `git diff --quiet -- atoms evidence Examples Book` | **0** | 受控目录**零污染** |
| 17 | `git status --short` | — | 已跟踪修改项**仅剩** `data/mutation/full_baseline_v4.json`（**预存在 CRLF 假脏**，全程未提交未还原）；本批 12 个文件全部已入库；无临时件残留 |

- 本批 4 个 commit，**零改 CORE 五文件 / 零改 `prop_graph.py` / 零改卡**：
  `c2a12ba`(T1) → `574707e`(T2) → `d989d5d`(T3) → `2af99a3`(T4)。
- 验收重跑后 `data/attack_edges_candidates.jsonl` / `grounded_labels_w2.json` / `grounded_audit_report.md`
  与库里版本**逐字节不变**（幂等，`git status` 无 M）。
- **未做**：mutation 端到端反例验证（任务书明令留后续）、grounded Web 界面（任务书明令 595 后再定）、
  合并原子卡侧 `misconceptions` 反向种子（D5，需人裁决）、根目录 149 临时件清理（卫生债，非本批）。

---

## §6 偏差表（如实）

| # | 任务书假设 | 实测 | 处理 |
|---|---|---|---|
| D1 | 594 说 42 MIS 带 `related_atoms`、194 条候选边 | **独立复算完全一致**（79 MIS；42 带关联；194 条 MIS→命题；25 张关联卡；0 悬空；每 MIS 2–12 条 avg 4.619） | 无偏差；写进任务 0 表 |
| D2 | W2 结果 IN=79/OUT=42/UNDEC=0 | **完全一致**（3 轮收敛，击败边 194/388） | 无偏差 |
| D3 | 可信度分级 high/medium/low | **MIS 卡面 0 张有 `verified_by`/`machine_verified`** ⇒ 42 个误解**全部 `low`**；命题侧 79 条全 `medium`（卡级签或机器锚） | 分级照实现（high 分支留待语义/机器字段出现），W2 靠"命题 2 > 误解 1"成立；`stats` 明写"当前全 low"，不假装有分级 |
| D4 | 每条边带 `generated_at`（ISO）+ 幂等"逐字一致" | 两者本质冲突（时间戳即变化源） | `generated_at` 默认 `null`，打点走显式 `--now`；测试锁逐字节幂等 |
| D5 | 生成规则读 MIS 的 `related_atoms` 与 `misconceptions` | MIS 侧 `misconceptions` **0 张**；**原子卡侧** 8 张有该反向字段 | 严格按任务书（只读 MIS 侧）⇒ 反向种子不产边，边数 == 194；**后果**：`ATOM-CONC-FENCE-001`/`ATOM-CONC-LOCK-001` 的 **4 条命题无任何误解攻击**（审计 §6 已标注）；合并反向种子会改基线，交人裁决 |
| D6 | 任务书给的 grounded 迭代式（"IN ⇔ 全部攻击者 OUT / OUT ⇔ ∃ IN 的攻击者"） | 若"攻击者"取**全部攻击边**、而 OUT 只认**击败边**，两关系不一致 ⇒ 实测卡死 **IN=4 / OUT=0 / UNDEC=117** | 判为**任务书表述的歧义**：W2 语义下"不构成击败的攻击不算攻击"，两个判定必须用**同一关系**；修正后立刻复现 594。已在代码 docstring 留坑注释 + worklog 记录（这是本批唯一一次真实翻车） |
| D7 | `pytest -m "not slow" -n auto` → exit 0 | **exit 1**：唯一红 = 591 治理台账缺 **4 处新增** References 文档（596/597/PM_六维度/PUSH+grounded 综合结论），**全是人新加的、本批未碰**（`git status` 无 M）；另 592 尾批监工已修的两条并发假红本批**未复现** | **不修**（不在 596 边界；`update` 会把 4 篇未人审文档刷进 manifest，属人审权力）⇒ 交人（§7-4） |
| D8 | 收工清单第 14 项 `pytest -m slow -n0` 一次跑完 | 340 例串行 > 6 分钟（`test_mutation_*`/`ccache` 占 ≈5:51），单条命令超时上限 | **分 5 块**跑完（132 / 80 / 57 / 39 / 32），逐块贴退出码；结论不变：唯一红 = golden 预期红 |

---

## §7 交人项

1. **候选攻击边需人审**：388 条全部 `pending`（`attack_edge_review.py list`）——
   本批只建通道，**不做任何 approve/reject**（系统绝不自动产生人审标注）。
   注意：MIS 全 `low` ⇒ 人审 `approve` 升一级到 `medium`（仍 < 命题 `medium` ⇒ **不会**改变判决，
   只有 `modify --confidence high` 才会让误解反压命题）——这是**预期语义**，别误当 bug。
2. **D5 反向种子裁决**：原子卡侧 `misconceptions` 字段（8 张卡）是否也参与生成攻击边？
   合并后边数会 > 194 且 4 条"无攻击者命题"会获得攻击者 ⇒ 需重定基线，本批不动。
3. **D6 迭代式歧义**：任务书任务 2.3 的迭代表述与 594 预期值不自洽（见 D6）；
   本批按"击败关系即攻击关系"实现并复现 594，请确认口径。
4. **591 治理台账过期（预存在）**：`governance_doc_guard.py verify` 报 4 处新增（见 D7）⇒
   是否 `update` 由人定（592 尾批曾由监工自行 update 收口）；这是 fast 套件唯一"串行仍红"。
5. **golden 待人工 accept**：`test_json_output.py::test_golden_lock_json`（slow 唯一红，预期）。
6. **后续批次**：mutation 端到端反例验证（任务书明确留后续）；grounded Web 界面（595 之后再定）；
   4 条"无攻击者命题"的证据/误解关联补全（知识活）。
