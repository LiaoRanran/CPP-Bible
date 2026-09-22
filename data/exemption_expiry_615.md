# 615 C2 · 豁免到期制（legacy + 624 新增）

> **豁免总数 `31` = `27` legacy + `4` HC**（两个集合，**不可混用**）：
> - **27 条 legacy**（`redteam_seen: legacy`，创建于 batch 15）；
> - **4 条 HC**（`redteam_seen: 624_b2_regression`，创建于 batch 21；624 B1 高复杂度带 block 变体
>   `EV-SERVES-EXIST-HC` / `ATOM-REL-TARGET-HC` / `ATOM-REL-UNKNOWN-HC` / `CARD-PATH-NOT-CANONICAL-HC`）。
>
> ⚠ **口径修正（2026-09-22，外部大模型发现 + 626 A1 核实）**：README 等处用「27 条 legacy 豁免」
> 概括**总豁免数**是错误的——27 只是 legacy 子集，当前**总豁免为 31**。引用时必须写明是哪个集合。
> 到期 = **创建批次 + 10**（批次轴 = `golden_state.accepted[]` 时间线）。**只算到期日与提醒，不删/不改任何豁免**。

## 一、状态汇总

| 状态 | 条数 |
|---|---|
| active（未到期） | 31 |
| due_soon（≤3 批内到期） | 0 |
| expired（已到期，须重评估） | 0 |

## 二、到期日列表

| 规则 ID | 创建日期 | 创建批次 | 到期批次 | 当前批次 | 状态 |
|---|---|---|---|---|---|
| `ATOM-AUDIENCE` | 2026-09-12 | 15 | 25 | 21 | active |
| `ATOM-DAL-MATCH` | 2026-09-12 | 15 | 25 | 21 | active |
| `ATOM-FM-REQUIRED` | 2026-09-12 | 15 | 25 | 21 | active |
| `ATOM-GRAY-ZONE` | 2026-09-12 | 15 | 25 | 21 | active |
| `ATOM-ID-FORMAT` | 2026-09-12 | 15 | 25 | 21 | active |
| `ATOM-MISCONCEPTION-LEVELS` | 2026-09-12 | 15 | 25 | 21 | active |
| `ATOM-MISCONCEPTION-REF` | 2026-09-12 | 15 | 25 | 21 | active |
| `ATOM-NO-UNVERIFIED` | 2026-09-12 | 15 | 25 | 21 | active |
| `ATOM-PREREQ-READABLE` | 2026-09-12 | 15 | 25 | 21 | active |
| `ATOM-REL-DAG` | 2026-09-12 | 15 | 25 | 21 | active |
| `ATOM-REL-TARGET` | 2026-09-12 | 15 | 25 | 21 | active |
| `ATOM-STATUS-TRANSITION` | 2026-09-12 | 15 | 25 | 21 | active |
| `ATOM-STATUS-VALUE` | 2026-09-12 | 15 | 25 | 21 | active |
| `ATOM-SUPERIORITY-WORDS` | 2026-09-12 | 15 | 25 | 21 | active |
| `DOC-ZERO-PLACEHOLDER` | 2026-09-12 | 15 | 25 | 21 | active |
| `EV-FM-REQUIRED` | 2026-09-12 | 15 | 25 | 21 | active |
| `EV-MATRIX` | 2026-09-12 | 15 | 25 | 21 | active |
| `EV-SERVES-EXIST` | 2026-09-12 | 15 | 25 | 21 | active |
| `HUMAN-GOLDEN-REVIEW` | 2026-09-12 | 15 | 25 | 21 | active |
| `HYBRID-TEACHING-DEPTH` | 2026-09-12 | 15 | 25 | 21 | active |
| `LLM-SUPERIORITY-QUALITY` | 2026-09-12 | 15 | 25 | 21 | active |
| `META-MANIFEST` | 2026-09-12 | 15 | 25 | 21 | active |
| `MIS-LIBRARY` | 2026-09-12 | 15 | 25 | 21 | active |
| `PED-MISCONCEPTION` | 2026-09-12 | 15 | 25 | 21 | active |
| `PED-MOTIVATION` | 2026-09-12 | 15 | 25 | 21 | active |
| `PED-PREDICT-FIRST` | 2026-09-12 | 15 | 25 | 21 | active |
| `PED-SOCRATIC` | 2026-09-12 | 15 | 25 | 21 | active |
| `ATOM-REL-TARGET-HC` | 2026-09-22 | 21 | 31 | 21 | active |
| `ATOM-REL-UNKNOWN-HC` | 2026-09-22 | 21 | 31 | 21 | active |
| `CARD-PATH-NOT-CANONICAL-HC` | 2026-09-22 | 21 | 31 | 21 | active |
| `EV-SERVES-EXIST-HC` | 2026-09-22 | 21 | 31 | 21 | active |

## 三、即将到期 / 已到期

- 即将到期（≤3 批）：（无）
- 已到期：（无）

## 四、到期后重新评估流程（需人审授权）

1. **继续豁免**：确认该规则仍「端到端毒样例不适用/不经济」（须有 pytest 正反例兜底）⇒ 续期 +10 批；
2. **修复规则**：若该规则本应有端到端毒样例 ⇒ 补毒样例、删豁免（改分母=口径动作，须人审）；
3. **删除豁免**：规则被合并/废弃 ⇒ 删豁免并说明。

> **重要声明**：本工具**只算到期日与提醒**，**不自动删除或修改任何豁免**；续期/修复/删除均需**人审授权**。


