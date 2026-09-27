# 判决形式规格 v1（Verdict Formal Specification v1）

> 655 B 产出。**这是规格文档，不是代码**；每条不变量都给出**可测试形式**（能跑的命令 / 能断言的谓词），
> 为后续 Rust + Verus 形式化（`_arch_v34` 地基 2）提供目标语义。
>
> 上位依据：[`docs/uvk_manifesto.md`](uvk_manifesto.md)（五条纲领：永不自证 / 永不全信 / 永不 fail-open /
> 最小可信内核 / 持续进化）；实现现状见 `tools/queyi_core_v10_641.py`（内核）、
> `tools/four_state_verdict_638.py`（四态执行器）、`tools/verdict_extension_651.py`（扩展 schema）、
> `tools/decision_event_v2_626.py`（账本事件）、`queyi-core/tools/conflict_detector_647.py`（冲突保护器）。

---

## §0 版本与范围

### 0.1 三个版本轴

| 版本 | 含义 | 现状 |
|---|---|---|
| **v0** | 历史二态：`APPROVE / MODIFY`（452 条 Authority 账本）与 `pass / block`（baseline 报告） | **已存在，冻结不改** |
| **v0.5** | 四态 `pass / pass_with_exception / fail / unknown` + **边界三元组强制**（638 真上线） | **已实现且有真实数据** |
| **v1** | v0.5 **+ 扩展轴**（`conditions[]` / `partial_atoms[]` / `conflict_state` / `unknown_reason`）+ 与保护器/账本的接口契约 | **本文档**；代码侧仅有 schema 与校验，卡级**无真实数据**（见 §7） |

### 0.2 规格边界（本规格**不**定义什么）

1. **不定义**"证据是否充分"的领域判据（那是 Domain Pack 的职责，见 `tools/queyi_core_cpp_641.py`）；
2. **不定义**规则集内容（67 条规则的语义属 `tools/gate_engine.py`）；
3. **不定义**人审组织流程（属 Authority/M7 队列）；
4. **不改变**任何历史判决与历史账本（向后兼容见 §6）。

### 0.3 命名冲突警告（必读）

本仓库存在**另一条"四"轴**：知识卡生命周期状态
`draft / machine-verified / red-team-verified / human-verified / verified / rejected`（`gate_engine.ATOM_STATUSES`，
规范见 `docs/kernel/G6_status_levels.md`）。**判决四态与卡状态轴正交、不得互相推导**：
卡 `status: verified` 只说明"卡本身整备完毕"，**不**说明对某条断言判了 `pass`（详见 INV-13）。

---

## §1 数据模型

判决对象有三种载荷形态，语义相同、承载不同：**内核决策**（`Decision`）、**账本事件**（`DecisionEvent v2`）、**卡片/报告记录**（frontmatter/表格）。

### 1.1 D-域：内核决策 `Decision`（`tools/queyi_core_v10_641.py:205`）

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `decision_id` | `str` | 确定性摘要，64hex；**不含时间戳** | = `sha256(canonical_json({a:artifact_id, s:state, r:reasons, rid:rule_ids, p:policy_ref}))` |
| `artifact_id` | `str` | 非空 | 判决对象（内容寻址 Artifact）。注意：**不含** `evidence_ids`，故补证据不改变 ID |
| `state` | `enum` | **封闭**：`pass / pass_with_exception / fail / unknown` | 违反 ⇒ `ValueError`（构造期即拒） |
| `reasons` | `tuple[str,...]` | 可空 | 人类可读依据；进 ID 摘要 |
| `evidence_ids` | `tuple[str,...]` | 可空；**去重排序** | 支撑该判决的证据 |
| `rule_ids` | `tuple[str,...]` | 可空；去重排序 | 触发/判定所用规则 |
| `policy_ref` | `str` | 可空 | 规则集指纹（`policy_digest`） |
| `exceptions` | `tuple[str,...]` | `state=pass_with_exception` ⇒ **非空** | 例外条款 |
| `abstained` | `bool` | — | 弃权（与 `unknown` 不同：弃权是**主动**不判） |
| `decided_at` | `str` | ISO-8601 秒精度；**不进 ID** | 时间不参与确定性 |

**配套枚举**——证据复验状态 `EVIDENCE_STATES = ("confirm","refute","infra","unknown")`（同上文件 `:51`）。

### 1.2 L-域：账本事件 `DecisionEvent v2`（`tools/decision_event_v2_626.py`）

实测：`data/authority/decision_event_v2_ledger.jsonl` 共 **452** 条，每条 **25** 个字段（25 个键在全部 452 条中**无缺失**；626 报告曾记作"26 字段"，以本实测为准）
（`result`：`APPROVE 367 / MODIFY 85`；`decision_origin`：`human_observed 228 / mirror_projection 194 / user_authorized_execution 30`）。

- **必填集合**（`REQUIRED_FIELDS`，缺任一 ⇒ `StrictEventError`，**不再用默认值补全**）：
  `operation`、`result`、`target_type`、`target_id`、`review_method`、`decision_origin`、`reviewer`、`decided_at`。
  口径原文："一条可追溯到人的判决至少要说清：做了什么/结论/对象/怎么审/来自谁/谁签/何时"。
- **链字段**：`seq`、`prev_hash`、`self_hash`（首条 `prev_hash="GENESIS"`）、`supersedes[]`（改判指向被取代事件）。
- **四态映射**（`Decision.V2_STATE_MAP`）：
  `pass→PASS`、`pass_with_exception→PASS_WITH_EXCEPTION`、`fail→FAIL`、`unknown→UNKNOWN`；
  反向映射**未知值一律落 `unknown`**（fail-closed，不猜）。

### 1.3 C-域：卡片/报告记录 + 边界三元组（638）

| 字段 | 类型 | 约束 | 缺省语义 |
|---|---|---|---|
| `mutation_set_hash` | `str` | **64 hex** | 缺失 ⇒ 该记录**不可能**判 `pass/fail` |
| `mutation_count` | `int>0`（允许字符串数字） | `> 0` | 同上 |
| `generator_version` | `str` | 非空白 | 同上 |
| `explanation` | `str` | `pass_with_exception` ⇒ 非空 | 缺失 ⇒ 降级 `unknown` |
| `verdict` / `result` / `decision` | `str` | 词表：pass 类 / fail 类（见 §4.1） | 空 ⇒ 按 `pass` 处理（但**仍需边界**） |

### 1.4 X-域：v1 扩展字段（651，全部**可选**）

| 字段 | 类型 | 取值/约束 | 缺省语义 |
|---|---|---|---|
| `schema_version` | `int` | `1` = 无扩展；`2` = 有扩展 | 1 |
| `conditions[]` | `array<{kind, expr, evidence_ref}>` | `kind ∈` **7 值白名单**（§1.5） | `[]` = 结论无条件 |
| `partial_atoms[]` | `array<{atom_id, covered: bool, note?}>` | `covered` 必须是 `bool` | `[]` = 覆盖全命题 |
| `conflict_state` | `enum` | `none / detected / resolved` | `none` |
| `conflict_detail` | `object\|null` | `{left, right, c_value, evidence_both_sides}`；`resolved` ⇒ 必填 | `null` |
| `unknown_reason` | `enum\|null` | **8 值白名单**（§1.5）；`other` ⇒ 必须附 `unknown_note` | `null`（兼容 v0） |

**不可变字段**（回填/改判时**一字不许动**）：`state`、`decision_id`、`event_id`、`result`、`prev_hash`、`entry_hash`。

### 1.5 封闭枚举（fail-closed 白名单）

```text
conditions[].kind  : platform | compiler_version | std_version | optimization
                     | input_domain | assumption | other
conflict_state     : none | detected | resolved
unknown_reason     : no_evidence | evidence_conflict | out_of_scope | implementation_defined
                     | insufficient_samples | tool_unavailable | not_applicable | other
```

**纪律**：白名单之外的值 ⇒ **拒绝**（不是"默认放行、事后告警"）。

### 1.6 粒度轴语义（`partial_atoms` 与条件的交互）

- `partial_atoms` 表达"**结论覆盖到哪几个原子命题**"：`covered=false` 的项 = 未覆盖面，**不得**被读成"该面通过"；
- 与 `conditions` 的区别：`conditions` 说"**在什么前提下**结论成立"，`partial_atoms` 说"**结论覆盖了哪部分**"；
- 两者**同时**出现时：结论范围 = `conditions` 成立 ∧ `partial_atoms.covered=true` 的子集；
- **保守读取规则**：`partial_atoms` 非空且全为 `covered=false` ⇒ 该判决等价于 `unknown`（"什么都没覆盖"）——
  这是**规格新增**的语义（当前代码未实现，见 §7 G-2）。

---

## §2 状态机（四态迁移）

```
                 ┌──────── (1) 补边界 + 判定通过 ────────┐
                 │                                      ▼
   ┌──────────┐  │  (2) 冲突保护器 C≥0.8 且双方有证据  ┌───────┐
   │  pass    │──┴────────────────────────────────────► │ fail  │
   └──────────┘  ◄────────── (3) 人审 supersede ──────── └───────┘
        │  (4) 加例外（需 explanation）                       │
        ▼                                                    │
  ┌────────────────────┐                                     │
  │ pass_with_exception│── (2) 同上 ────────────────────────►┘
  └────────────────────┘
        ▲   │
   (1)  │   │ (5) 撤回证据 / 边界失效 / 复验 infra
        │   ▼
   ┌────────────────────┐
   │      unknown       │◄── (6) 任一态缺边界或畸形 ⇒ 降级
   └────────────────────┘
```

| # | 迁移 | 触发条件（前置） | 后置 | 是否需人 |
|---|---|---|---|---|
| 1 | `unknown → {pass, pass_with_exception, fail}` | **补齐**边界三元组 + 证据复验非 `infra`（§4.4） | 新事件（`supersedes` 指向旧事件），`unknown_reason=null` | 否（机器可做），但需**新证据** |
| 2 | `{pass, pass_with_exception} → fail` | 冲突保护器：`C ≥ 0.8` **且**双方均有证据（`conflict_detector_647`） | `state=fail`，`conflict_state=detected`，`conflict_detail` 必填 | 否（保护器自动），但 **detected 必须转人审** |
| 3 | `fail → {pass, pass_with_exception}` | **只能**由人审判决 + 新事件 `supersedes`；机器不得自动回滚 | 新事件，`conflict_state ∈ {resolved}` 时须 `resolution` 理由 | **是** |
| 4 | `pass → pass_with_exception` | 出现适用例外条款 + `explanation` 非空 | `exceptions[]` 非空 | 否 |
| 5 | `{pass, pass_with_exception, fail} → unknown` | 证据撤回 / 边界字段失效 / 证据复验 `infra` | `unknown_reason` 必填（v1 新写入） | 否 |
| 6 | `* → unknown`（降级） | 边界三元组缺失或格式非法；或 `pass_with_exception` 缺 `explanation` | 见 §4.4 | 否 |

**非法迁移（必须拒绝）**：`pass ⇄ fail` 无新证据；`unknown → unknown` 改原因（应新事件）；任何**原地修改**已封存对象。

---

## §3 不变量表（每条可测试）

> "可测试形式"列给出**具体谓词或命令**。`638`/`651`/`kernel` 指对应工具的 `--check` 自检已覆盖的项。

| ID | 不变量（规格陈述） | 可测试形式 | 现状 |
|---|---|---|---|
| **INV-1** | `state` 必须落在四态封闭集内，否则**构造即失败** | `Decision(state="maybe")` 抛 `ValueError`（`kernel:223`） | ✅ 已实现（`638`/`kernel` `--check`） |
| **INV-2** | `state ∈ {pass, pass_with_exception, fail}` ⇒ **边界三元组齐备且合法** | `enforce({...b,"verdict":"pass"})=="pass"` 而 `enforce({"verdict":"pass"})=="unknown"` | ✅ 已实现（638） |
| **INV-3** | `state=pass_with_exception` ⇒ `explanation` 非空（或 `exceptions[]` 非空，两轴取一后**统一为 `exceptions[]`**） | `enforce({**b,"exception":"x"})=="unknown"`；`enforce({**b,"exception":"x","explanation":"y"})=="pass_with_exception"` | ✅（当前实现认 `explanation`；`Decision.exceptions` 为内核轴，**双轴并存**=规格待收敛，见 §7 G-1） |
| **INV-4** | **新写入**的 `unknown` 必须给出 `unknown_reason`（白名单内）；`other` ⇒ `unknown_note` 非空 | `validate({"state":"unknown","unknown_reason":"wat"}) != []`；`validate({"unknown_reason":"other"}) != []` | 🟡 枚举拒绝已实现（651）；"unknown 必须带 reason"**未强制**（§7 G-3） |
| **INV-5** | `conflict_state=resolved` ⇒ `conflict_detail` 非空；`detected` ⇒ 必须进入人审队列 | `validate({"conflict_state":"resolved"}) != []` | 🟡 前件已实现（651）；"detected ⇒ 入队"靠流程（M7 队列），**非硬校验** |
| **INV-6** | 回填/改判**不得改动** `state/decision_id/event_id/result/prev_hash/entry_hash` | `backfill(v)` 后逐字段相等且 `diff` 只含新增键 | ✅ 已实现（651） |
| **INV-7** | 回填**幂等**：`backfill(backfill(x))` 无 diff | `diff3 == {}` | ✅ 已实现（651） |
| **INV-8** | 枚举**fail-closed**：白名单外的值一律拒绝，不得默认放行 | `validate` 对 `conflict_state/unknown_reason/conditions[].kind` 越界均报错 | ✅ 已实现（651） |
| **INV-9** | 账本 **append-only 哈希链**：`self_hash = H(prev_hash ‖ 规范化载荷)`，首条锚 `GENESIS` | 649/651 的链校验：改一字节 ⇒ 链断；删一条 ⇒ 断 | ✅ 已实现（626 ledger + 651 checkpoint） |
| **INV-10** | `decision_id` **确定性**：同一 `(artifact, state, reasons, rule_ids, policy_ref)` ⇒ 同 ID；且**不含时间** | 同输入两次 `Decision.make(...).decision_id` 相等；`decided_at` 变化不影响 ID | ✅ 已实现（kernel） |
| **INV-11** | 证据状态封闭 `{confirm, refute, infra, unknown}`；`state=pass` ⇒ **不得**存在 `refute` 证据 | 伪造 `refute` 后判决必须降级或改判（探针：`tools/atom_evidence_replay.py` 口径） | 🟡 枚举封闭已实现；"pass 与 refute 互斥"**未强制**（§7 G-4） |
| **INV-12** | 冲突改判**不可机器回滚**：`fail` 只能由人审 `supersedes` 回到 `pass/pass_with_exception` | 迁移表 #3；任何自动路径产生该迁移 ⇒ 违规 | ✅ 语义务实（647 无自动回滚路径） |
| **INV-13** | 判决四态与**卡状态轴**正交：卡 `status: verified` **不蕴含** `pass` | 638 实测：23 张 verified 卡**全部** `unknown`（无边界） | ✅ 已实测（638 §三） |
| **INV-14** | 判决变更必须**留痕**：任何状态变化产生新事件（含 `supersedes`），不得原地改写 | 历史文件 sha256 前后不变（回填 dry-run 断言） | ✅ 已实现（651 dry-run 报告 `unchanged: true`） |
| **INV-15** | `partial_atoms` 全 `covered=false` ⇒ 等价 `unknown`（保守读取） | 见 §1.6 规则 | ❌ **未实现**（§7 G-2） |

---

## §4 操作语义（前置 / 后置条件）

### 4.1 `classify(record) → verdict`（638 核心）

**前置**：`record` 为映射；`verdict` 词取自词表（fail 类：`block/fail/failed/reject/rejected/refut/refuted/false`；
pass 类：`pass/passed/approve/approved/true/ok`）。
**后置**（按序短路）：

1. 若推导出的原始态为 `unknown` ⇒ 返回 `unknown`（`downgraded=false`）；
2. 否则若 `has_boundary(record)=false` ⇒ `unknown` 且 `downgraded=true`，`reasons` 含**缺失字段名**或"格式非法"；
3. 否则若原始态 `pass_with_exception` 且 `explanation` 为空 ⇒ `unknown` 且 `downgraded=true`；
4. 否则返回原始态（`downgraded=false`）。
**输出**：`{state, requested, downgraded, boundary_ok, reasons[]}` —— **`requested` 必须保留**（可追溯"本想要什么"）。

### 4.2 `has_boundary(record) → bool`（638）

**后置**：`mutation_set_hash` 匹配 `^[0-9a-fA-F]{64}$` ∧ `int(mutation_count) > 0` ∧ `generator_version.strip() != ""`；
任一不满足 ⇒ `false`（**不抛错**，由调用方决定降级）。

### 4.3 `validate(record) → errors[]`（651，fail-closed 校验）

**后置**：返回空列表 **当且仅当**：

- `state/decision_id/event_id/result/prev_hash/entry_hash` 若出现**不得为 `null`**；
- `conditions` 若出现必须是数组，且每项含白名单内 `kind`；
- `partial_atoms` 若出现必须是数组，且每项含 `atom_id` 与 **`bool` 类型**的 `covered`；
- `conflict_state` 若出现必须在白名单内，且 `resolved` ⇒ `conflict_detail` 是对象；
- `unknown_reason` 若出现必须在白名单内，且 `other` ⇒ `unknown_note` 非空；
- **旧记录（无任何 v1 字段）必须通过**（v0 兼容）。

### 4.4 `downgrade_to_unknown(record, cause) → verdict'`（规格新增，规范化）

**前置**：`cause ∈ {missing_boundary, malformed_boundary, missing_explanation, evidence_withdrawn, verify_infra}`。
**后置**：`state=unknown`；`downgraded=true`；`unknown_reason` 按 cause 映射
（`missing_boundary/malformed_boundary → no_evidence`… —— **注意**：当前实现**不臆测**根因，只在显式 unknown 时填 `other`+note；
映射表属 v1 目标，见 §7 G-3）；**原始 `requested` 与全部证据引用必须保留**。

### 4.5 `conflict_override(decision, pair) → decision'`（647 保护器）

**前置**：保护器处于 `enforce`；`C ≥ θ_block=0.8` **且** `both_sides_have_evidence=true`。
**后置**：`state=fail`；附 `conflict_*` 三字段（`conflict_state=detected`、`conflict_detail.c_value`、`evidence_both_sides=true`）；
**除该三字段外逐字段与 shadow 输出相等**（652/653 的差分契约：`decision_id`/`state` 之外的字段不得漂移）；
历史判决**不回溯**（只对新判决生效）。
**`0.5 ≤ C < 0.8`** ⇒ 只加标记（`warn`）交人审；**`C < 0.5`** ⇒ `pass` 不带标记。
**θ 是设计值**（未用真实样本回填）——诚实登记见 `conflict_detector_647` docstring。

### 4.6 `append(event) → ledger'`（626 账本）

**前置**：`REQUIRED_FIELDS` 全非空；`event_id` 未出现过（重复写入应可**去重**）。
**后置**：追加一行；`seq` 递增；`prev_hash` = 前一条 `self_hash`；`self_hash` 可独立重算；
`supersedes` 指向被取代事件（改判专用）。**现状约束**：账本写入属**代签风险区**（642 C1 已裁定），
自动化工具**不得**写入，仅人/授权流程可写。

### 4.7 `review(edge, verdict) → credibility'`（人审，`tools/defense_chain.py`）

`verdict ∈ {approve, modify, reject, unreviewed}`；`credibility` 映射：
`approve → medium`（命题默认 `medium`）、`modify / reject / unreviewed ⇒ 保持 low`。

---

## §5 边界情况（必须给出确定行为）

| 情况 | 规格要求的行为 | 现状 |
|---|---|---|
| **空输入** `{}` | `classify({})` ⇒ `unknown`（无边界），`downgraded=true`；**不得**抛错、**不得**默认 `pass` | ✅（638）；⚠ 账本侧 `DecisionEvent.from_dict({})` 曾默认 `APPROVE + human_observed` ⇒ 已在 626 改为**必填集合 + 无默认值**（INV-4 前身） |
| **边界字段畸形**（hash 非 64hex / count≤0 / version 空白） | ⇒ `unknown`，`reasons` 说明"格式非法" | ✅（638） |
| **冲突证据**（两证据一 `confirm` 一 `refute`） | 记 `conflict_state=detected`；`C≥0.8` 且双方有证据 ⇒ `fail`；**不得**自行选边 | ✅（647）；`resolved` 需人审 + `resolution` 理由 |
| **证据不足**（无证据或全 `infra`） | ⇒ `unknown` + `unknown_reason ∈ {no_evidence, tool_unavailable}` | 🟡 枚举就位；**未自动填**（§7 G-3） |
| **保护器触发**（预算超限 / 熔断 / 工具级门拒绝 / 盲化违规） | 判决流程**中断**，事件标记 `halted/protection_raised`，**不得**产出 `pass`（fail-closed） | ✅（649/653：`BudgetExceeded` 抛错、熔断 fail-closed、`ToolGateDenied`） |
| **复验 `infra`**（编译器缺失 / 超时） | 该证据**不可**支撑 `pass`；判决落 `unknown`（`tool_unavailable`） | 🟡 证据状态有 `infra`；判决侧映射未强制（§7 G-3） |
| **同一输入重复判决** | 幂等：`decision_id` 相同 ⇒ 可去重，不产生第二条等价事件 | ✅（INV-10 + 账本去重） |
| **v0 记录（无任何 v1 字段）** | 校验 PASS，视为 `schema_version=1` | ✅（651） |

---

## §6 向后兼容：v0 → v1 迁移规则

| 规则 | 内容 |
|---|---|
| **M1 只加不改** | 迁移**只新增字段**；`state / decision_id / event_id / result / prev_hash / entry_hash` 一字不动（硬断言：迁移前后该 6 字段逐字相等） |
| **M2 默认值** | 新增字段默认：`schema_version=2`、`conditions=[]`、`partial_atoms=[]`、`conflict_state="none"`、`unknown_reason=null` |
| **M3 不臆测根因** | 旧 `unknown` 记录回填 `unknown_reason` **只能填 `other` + `unknown_note`**（人工判定前不得猜） |
| **M4 dry-run 先行** | 迁移必须先出**计划**（将改条数 / 逐条 diff / **原文件 sha256 不变**）；`--migrate` **只打印**，不自动执行 |
| **M5 幂等** | 二次迁移无 diff；`dry_run` 与 `apply` 语义分离 |
| **M6 历史标签不重分类** | 452 条账本的 `APPROVE/MODIFY` 原值保留；只提供映射函数（`APPROVE→pass` 类、`MODIFY→` 待判） |
| **M7 词表映射（旧→新）** | `pass/APPROVE → pass`；`block/REJECT/fail → fail`；`MODIFY →` **不明映射**（现口径：`modify` 不抬 credibility、不等于 `fail`）；其余 → `unknown` |

---

## §7 未实现 / 待形式化清单（诚实登记）

| ID | 缺口 | 现状事实 | 达到 v1 需要 |
|---|---|---|---|
| **G-1** | `explanation`（638）与 `exceptions[]`（内核）**双轴并存** | 两处各自实现，未统一 | 规定唯一承载（建议 `exceptions[]` 为准，`explanation` 视为其文本化投影） |
| **G-2** | `partial_atoms` 全 `false` ⇒ 等价 `unknown`（INV-15） | **无实现**，无数据 | 校验器增加该语义 + 用例 |
| **G-3** | `unknown_reason` **自动**归类（§4.4 cause→reason 映射） | 只在显式 unknown 时填 `other`+note；**不臆测** | 建立 cause→reason 映射表并由执行器写入（仍需人审确认 `other`） |
| **G-4** | `pass` 与 `refute` 证据**互斥**检查（INV-11 后半） | 无实现 | 判决写入前做证据一致性检查 |
| **G-5** | 卡级**真实** v1 数据 | 实测：**0** 张卡带 `conditions/partial_atoms/conflict_state/unknown_reason` | 逐卡回填（需人；属"边界回填"欠债的同族） |
| **G-6** | `conflict_state=detected ⇒ 入人审队列` 的**硬**校验 | 现为流程约定（M7 队列），非校验 | 队列写入作为 `detected` 的后置条件（工具级） |
| **G-7** | Verus 形式化 | **未开始**（本规格是其输入） | 见 §8 |

**已知的真实样本（可作回归夹具）**：
`ATOM-MEM-PERF-003`（`C=1.333`，双方有证据 ⇒ 保护器改判 `fail`，EE 侧可能是假悬挂 ⇒ **最大风险点**）、
`ATOM-MEM-UNIQUE-002`（`C=0.5` ⇒ `warn` 档）、23 张 verified 卡（**全部** `unknown`，边界缺失）。

---

## §8 面向 Rust + Verus 的形式化衔接

目标：把 §3 的不变量写成**可机检**的 `requires/ensures`。建议编码要点（不含实现）：

1. **类型即约束**：`enum State { Pass, PassWithException, Fail, Unknown }` —— 四态由**类型系统**保证（对应 INV-1）；
2. **记录类型**：`struct Decision { id: Vec<u8>, artifact: ArtifactId, state: State, reasons: Seq<u8>, evidence: Set<EvidenceId>, rules: Set<RuleId>, policy: PolicyRef, exceptions: Seq<u8>, abstained: bool }` ——
   `id` 用 `Seq<u8>` 并声明 `decision_id(x) == decision_id(x)`（确定性，INV-10）；
3. **纯函数 + 契约**：
   - `classify(rec) -> (state, downgraded)`，`ensures state == Unknown ==> (downgraded || requested == Unknown)`（INV-2）；
   - `has_boundary(rec) -> bool`，`ensures result == true ==> hash_len == 64 && count > 0 && version.len() > 0`（§4.2）；
   - `backfill(rec) -> rec'`，`ensures immutables(rec) == immutables(rec')`（INV-6）且 `backfill(backfill(rec)) == backfill(rec)`（INV-7）；
   - `validate(rec) -> Result<(), Err>`，`ensures is_err ==> 枚举越界 || 必填缺失 || 约束违反`（INV-8，fail-closed）；
4. **链式结构**：账本用 `Seq<Entry>` + 归纳不变式"每条 `self_hash` 由 `prev_hash` 与载荷唯一确定"（INV-9）；
5. **非目标**：域判定（证据是否充分）**不进**形式化范围 —— 那是环境依赖 + 人类判断（对应 UVK 纲领"永不自证"）。

---

## §9 附：与现有实现的对照总表

| 规格 § | 实现位置 | 状态 |
|---|---|---|
| §1.1 D-域 + 四态封闭 | `tools/queyi_core_v10_641.py:42,205` | ✅ 真实现 |
| §1.2 L-域 + 25 字段 + 哈希链 | `tools/decision_event_v2_626.py`、`data/authority/decision_event_v2_ledger.jsonl`（452 条） | ✅ 真实现 |
| §1.3 C-域 边界三元组 | `tools/four_state_verdict_638.py`（`has_boundary/classify/enforce`） | ✅ 真实现 |
| §1.4 X-域 扩展字段 | `tools/verdict_extension_651.py` + `docs/verdict_extension.md` | 🟡 只有 schema + 校验 + dry-run |
| §1.5 封闭枚举 | 同上（`CONDITION_KINDS/CONFLICT_STATES/UNKNOWN_REASONS`） | ✅ 真实现 |
| §2 状态机 | 本文新增（迁移 #2 来自 647，其余来自 638/内核语义） | 📄 规格 |
| §4.5 冲突改判 | `queyi-core/tools/conflict_detector_647.py`（θ=0.8/0.5） | ✅ 真上岗（enforce） |
| §4.7 人审可信度映射 | `tools/defense_chain.py` | ✅ 真实现 |
| §3 INV-1..INV-14 | 见各行现状列 | ✅ 12 项 / 🟡 3 项 / ❌ 1 项 |

---

_655 B 产出 · 生成即冻结语义；任何语义变更必须新增版本（v2）并保留本文件。_
