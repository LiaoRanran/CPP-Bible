# 643 C3 · 攻击效果模拟（智能层：自动生成攻击 #3；沙箱隔离）

> 计划 **20** 条（`limit=20`，种子 `None`）；有效（非 noop）**20** 条；判定分布 `{'triggered': 2, 'oracle_mismatch': 11, 'not_triggered': 7}`。
> **生产零副作用**：`atoms/` 树指纹跑前跑后一致 = **True**（指纹 `479190c6c583687b`）。

## 一、判定口径

| verdict | 含义 |
|---|---|
| `noop` | 空变异（未改文本）⇒ 不计入攻击 |
| `blocked` | 方向 A：变异后**仍命中** ⇒ 规则没被绕开 |
| `evaded` | 方向 A：变异后**不再命中** ⇒ **逃逸（真发现）** |
| `triggered` | 方向 B：变异后**命中** ⇒ 规则可达 |
| `not_triggered` | 方向 B：仍不命中 ⇒ 规则**不可达候选** |
| `oracle_mismatch` | 目标规则没动但**别的**规则动了 ⇒ 预期可能猜错 |

## 二、逐条结果

| mutation_id | 目标规则 | 方向 | 卡 | 算子 | verdict | 新增 firing | 消失 firing |
|---|---|---|---|---|---|---|---|
| `ATOM-FM-REQUIRED#field_delete#0` | `ATOM-FM-REQUIRED` | B | `atoms/conc/ATOM-CONC-FENCE-001.md` | `field_delete` | **triggered** | `ATOM-FM-REQUIRED`, `S2-EVIDENCE-VERDICT` | — |
| `ATOM-FM-REQUIRED#break_ref#1` | `ATOM-FM-REQUIRED` | B | `atoms/conc/ATOM-CONC-LOCK-001.md` | `break_ref` | **oracle_mismatch** | `S2-EVIDENCE-VERDICT` | — |
| `ATOM-FM-REQUIRED#equiv_rewrite#2` | `ATOM-FM-REQUIRED` | B | `atoms/conc/ATOM-CONC-RACE-001.md` | `equiv_rewrite` | **not_triggered** | — | — |
| `ATOM-ID-FORMAT#field_delete#0` | `ATOM-ID-FORMAT` | B | `atoms/conc/ATOM-CONC-FENCE-001.md` | `field_delete` | **oracle_mismatch** | `ATOM-FM-REQUIRED` | — |
| `ATOM-ID-FORMAT#format_perturb#1` | `ATOM-ID-FORMAT` | B | `atoms/conc/ATOM-CONC-LOCK-001.md` | `format_perturb` | **not_triggered** | — | — |
| `ATOM-ID-FORMAT#break_ref#2` | `ATOM-ID-FORMAT` | B | `atoms/conc/ATOM-CONC-RACE-001.md` | `break_ref` | **oracle_mismatch** | `S2-EVIDENCE-VERDICT` | — |
| `ATOM-ID-FORMAT#equiv_rewrite#3` | `ATOM-ID-FORMAT` | B | `atoms/hist/ATOM-HIST-AUTOPTR-001.md` | `equiv_rewrite` | **not_triggered** | — | — |
| `ATOM-ID-UNIQUE#field_delete#0` | `ATOM-ID-UNIQUE` | B | `atoms/conc/ATOM-CONC-FENCE-001.md` | `field_delete` | **oracle_mismatch** | `ATOM-FM-REQUIRED` | — |
| `ATOM-ID-UNIQUE#break_ref#1` | `ATOM-ID-UNIQUE` | B | `atoms/conc/ATOM-CONC-LOCK-001.md` | `break_ref` | **oracle_mismatch** | `S2-EVIDENCE-VERDICT` | — |
| `ATOM-ID-UNIQUE#equiv_rewrite#2` | `ATOM-ID-UNIQUE` | B | `atoms/conc/ATOM-CONC-RACE-001.md` | `equiv_rewrite` | **not_triggered** | — | — |
| `ATOM-VERIFIED-BOUND#field_delete#0` | `ATOM-VERIFIED-BOUND` | B | `atoms/conc/ATOM-CONC-FENCE-001.md` | `field_delete` | **triggered** | `ATOM-FM-REQUIRED`, `ATOM-REL-TARGET`, `ATOM-VERIFIED-BOUND` | — |
| `ATOM-VERIFIED-BOUND#break_ref#1` | `ATOM-VERIFIED-BOUND` | B | `atoms/conc/ATOM-CONC-LOCK-001.md` | `break_ref` | **oracle_mismatch** | `S2-EVIDENCE-VERDICT` | — |
| `ATOM-VERIFIED-BOUND#equiv_rewrite#2` | `ATOM-VERIFIED-BOUND` | B | `atoms/conc/ATOM-CONC-RACE-001.md` | `equiv_rewrite` | **not_triggered** | — | — |
| `ATOM-NO-UNVERIFIED#field_delete#0` | `ATOM-NO-UNVERIFIED` | B | `atoms/conc/ATOM-CONC-FENCE-001.md` | `field_delete` | **oracle_mismatch** | `ATOM-FM-REQUIRED` | — |
| `ATOM-NO-UNVERIFIED#break_ref#1` | `ATOM-NO-UNVERIFIED` | B | `atoms/conc/ATOM-CONC-LOCK-001.md` | `break_ref` | **oracle_mismatch** | `S2-EVIDENCE-VERDICT` | — |
| `ATOM-NO-UNVERIFIED#equiv_rewrite#2` | `ATOM-NO-UNVERIFIED` | B | `atoms/conc/ATOM-CONC-RACE-001.md` | `equiv_rewrite` | **not_triggered** | — | — |
| `ATOM-STATUS-VALUE#field_delete#0` | `ATOM-STATUS-VALUE` | B | `atoms/conc/ATOM-CONC-FENCE-001.md` | `field_delete` | **oracle_mismatch** | `ATOM-FM-REQUIRED` | — |
| `ATOM-STATUS-VALUE#break_ref#1` | `ATOM-STATUS-VALUE` | B | `atoms/conc/ATOM-CONC-LOCK-001.md` | `break_ref` | **oracle_mismatch** | `S2-EVIDENCE-VERDICT` | — |
| `ATOM-STATUS-VALUE#equiv_rewrite#2` | `ATOM-STATUS-VALUE` | B | `atoms/conc/ATOM-CONC-RACE-001.md` | `equiv_rewrite` | **not_triggered** | — | — |
| `ATOM-STATUS-TRANSITION#field_delete#0` | `ATOM-STATUS-TRANSITION` | B | `atoms/conc/ATOM-CONC-FENCE-001.md` | `field_delete` | **oracle_mismatch** | `ATOM-FM-REQUIRED` | — |

## 三、重点结果

- **逃逸（真发现）0 条**：（无）
- **触发成功 2 条**：`ATOM-FM-REQUIRED#field_delete#0`；`ATOM-VERIFIED-BOUND#field_delete#0`
- **oracle_mismatch 11 条**（生成器预期猜错，§十二.7）：`ATOM-FM-REQUIRED#break_ref#1`；`ATOM-ID-FORMAT#field_delete#0`；`ATOM-ID-FORMAT#break_ref#2`；`ATOM-ID-UNIQUE#field_delete#0`；`ATOM-ID-UNIQUE#break_ref#1`；`ATOM-VERIFIED-BOUND#break_ref#1`

## 诚实登记

1. **沙箱逃逸率 ≠ 生产逃逸率**（§十二.6）：沙箱是整树副本，生产可能有额外状态（锁、外部工具、时间窗口）；
2. **样本量极小**（`limit=20`）⇒ 本表**只作线索**，任何"比例"都**没有统计意义**（C4 会做等预算对比并显式说明）；
3. **`noop` 不算攻击失败**：它说明该算子在这张卡上**无从下手**，是算子-载体不匹配的信息（C4 会把它计入"有效攻击率"的分母以外）；
4. **`not_triggered` 不等于规则坏**：可能是「卡本来就合规」⇒ 只作「不可达候选」线索（同 C2 登记）；
5. **`oracle_mismatch` 是刻意的**：生成器的预期可能猜错（§十二.7）；本工具**记录**它，但**不改**预期，也不据此改判据；
6. 本工具**不碰生产**：沙箱由 `mutation_fuzz.sandbox()` 提供，另有 `atoms/` 树指纹硬校验（实测一致）。
