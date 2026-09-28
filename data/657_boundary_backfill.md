# 657 B · 边界三元组回填报告

> 生成：2026-09-28T10:53:35。工具：`tools/boundary_backfill_657.py`。

## 一、总览

- 扫描卡：**47** 张（status 分布 `{'draft': 21, 'red-team-verified': 3, 'verified': 23}`）；
- **可回填（目标状态 + 有真实变异基线覆盖）**：**26** 张；
  - 其中**已写入卡内**：**26** 张（`action=write` 待写入 0 张）；
- 照实留空（无覆盖 / 状态不在回填范围）：**21** 张。

## 二、逐卡（回填对象：边界三元组）

| 卡 | status | 变异数 | hash 前 12 | generator_version | 已落卡 |
|---|---|---:|---|---|---|
| `atoms/conc/ATOM-CONC-FENCE-001.md` | verified | 10 | `c1ae0bb1c8b5…` | `full_baseline_v7.json` | 是 |
| `atoms/conc/ATOM-CONC-LOCK-001.md` | verified | 10 | `c1ae0bb1c8b5…` | `full_baseline_v7.json` | 是 |
| `atoms/conc/ATOM-CONC-RACE-001.md` | verified | 11 | `ce578a4d5d2a…` | `full_baseline_v7.json` | 是 |
| `atoms/hist/ATOM-HIST-AUTOPTR-001.md` | verified | 10 | `328ba275db73…` | `full_baseline_v7.json` | 是 |
| `atoms/mem/ATOM-MEM-ALIGN-001.md` | verified | 10 | `328ba275db73…` | `full_baseline_v7.json` | 是 |
| `atoms/mem/ATOM-MEM-ALLOC-001.md` | verified | 10 | `47a858cf4e70…` | `full_baseline_v7.json` | 是 |
| `atoms/mem/ATOM-MEM-ALLOC-002.md` | red-team-verified | 10 | `1acd55822037…` | `full_baseline_v7.json` | 是 |
| `atoms/mem/ATOM-MEM-LEAK-001.md` | verified | 10 | `328ba275db73…` | `full_baseline_v7.json` | 是 |
| `atoms/mem/ATOM-MEM-LEAK-002.md` | red-team-verified | 10 | `1acd55822037…` | `full_baseline_v7.json` | 是 |
| `atoms/mem/ATOM-MEM-MOVE-002.md` | verified | 10 | `f8b75ec83bef…` | `full_baseline_v7.json` | 是 |
| `atoms/mem/ATOM-MEM-NEW-001.md` | verified | 10 | `328ba275db73…` | `full_baseline_v7.json` | 是 |
| `atoms/mem/ATOM-MEM-PERF-001.md` | verified | 10 | `d8379e84b246…` | `full_baseline_v7.json` | 是 |
| `atoms/mem/ATOM-MEM-PERF-002.md` | verified | 10 | `b47a6fb89478…` | `full_baseline_v7.json` | 是 |
| `atoms/mem/ATOM-MEM-PERF-003.md` | verified | 11 | `c5a6b393fcc2…` | `full_baseline_v7.json` | 是 |
| `atoms/mem/ATOM-MEM-PERF-004.md` | red-team-verified | 10 | `1c4d40b9d0a5…` | `full_baseline_v7.json` | 是 |
| `atoms/mem/ATOM-MEM-RAII-001.md` | verified | 10 | `328ba275db73…` | `full_baseline_v7.json` | 是 |
| `atoms/mem/ATOM-MEM-RAII-002.md` | verified | 10 | `5827a1d70e7d…` | `full_baseline_v7.json` | 是 |
| `atoms/mem/ATOM-MEM-RVREF-001.md` | verified | 10 | `328ba275db73…` | `full_baseline_v7.json` | 是 |
| `atoms/mem/ATOM-MEM-SHARED-001.md` | verified | 10 | `328ba275db73…` | `full_baseline_v7.json` | 是 |
| `atoms/mem/ATOM-MEM-SHARED-002.md` | verified | 10 | `f8b75ec83bef…` | `full_baseline_v7.json` | 是 |
| `atoms/mem/ATOM-MEM-UNIQUE-001.md` | verified | 10 | `328ba275db73…` | `full_baseline_v7.json` | 是 |
| `atoms/mem/ATOM-MEM-UNIQUE-002.md` | verified | 10 | `f8b75ec83bef…` | `full_baseline_v7.json` | 是 |
| `atoms/mem/ATOM-MEM-VALUE-001.md` | verified | 10 | `328ba275db73…` | `full_baseline_v7.json` | 是 |
| `atoms/mem/ATOM-MEM-VALUE-002.md` | verified | 10 | `f8b75ec83bef…` | `full_baseline_v7.json` | 是 |
| `atoms/mem/ATOM-MEM-WEAK-001.md` | verified | 10 | `328ba275db73…` | `full_baseline_v7.json` | 是 |
| `atoms/ub/ATOM-UB-GRAY-001.md` | verified | 10 | `d8379e84b246…` | `full_baseline_v7.json` | 是 |

## 三、照实留空（诚实：没证据就是没证据）

| 卡 | status | 原因 |
|---|---|---|
| `atoms/draft650/ATOM-DRAFT650-001.md` | draft | 卡状态 `draft` 不在回填范围 ('verified', 'red-team-verified')（判决未定，不预先写边界） |
| `atoms/draft650/ATOM-DRAFT650-002.md` | draft | 卡状态 `draft` 不在回填范围 ('verified', 'red-team-verified')（判决未定，不预先写边界） |
| `atoms/draft650/ATOM-DRAFT650-003.md` | draft | 卡状态 `draft` 不在回填范围 ('verified', 'red-team-verified')（判决未定，不预先写边界） |
| `atoms/draft650/ATOM-DRAFT650-004.md` | draft | 卡状态 `draft` 不在回填范围 ('verified', 'red-team-verified')（判决未定，不预先写边界） |
| `atoms/draft650/ATOM-DRAFT650-005.md` | draft | 卡状态 `draft` 不在回填范围 ('verified', 'red-team-verified')（判决未定，不预先写边界） |
| `atoms/draft650/ATOM-DRAFT650-006.md` | draft | 卡状态 `draft` 不在回填范围 ('verified', 'red-team-verified')（判决未定，不预先写边界） |
| `atoms/draft650/ATOM-DRAFT650-007.md` | draft | 卡状态 `draft` 不在回填范围 ('verified', 'red-team-verified')（判决未定，不预先写边界） |
| `atoms/draft650/ATOM-DRAFT650-008.md` | draft | 卡状态 `draft` 不在回填范围 ('verified', 'red-team-verified')（判决未定，不预先写边界） |
| `atoms/draft650/ATOM-DRAFT650-009.md` | draft | 卡状态 `draft` 不在回填范围 ('verified', 'red-team-verified')（判决未定，不预先写边界） |
| `atoms/draft650/ATOM-DRAFT650-010.md` | draft | 卡状态 `draft` 不在回填范围 ('verified', 'red-team-verified')（判决未定，不预先写边界） |
| `atoms/lang/ATOM-LANG-BITFIELD-001.md` | draft | 卡状态 `draft` 不在回填范围 ('verified', 'red-team-verified')（判决未定，不预先写边界） |
| `atoms/lang/ATOM-LANG-DECAY-001.md` | draft | 卡状态 `draft` 不在回填范围 ('verified', 'red-team-verified')（判决未定，不预先写边界） |
| `atoms/lang/ATOM-LANG-FNPTR-001.md` | draft | 卡状态 `draft` 不在回填范围 ('verified', 'red-team-verified')（判决未定，不预先写边界） |
| `atoms/lang/ATOM-LANG-INLINE-001.md` | draft | 卡状态 `draft` 不在回填范围 ('verified', 'red-team-verified')（判决未定，不预先写边界） |
| `atoms/lang/ATOM-LANG-INTPROMO-001.md` | draft | 卡状态 `draft` 不在回填范围 ('verified', 'red-team-verified')（判决未定，不预先写边界） |
| `atoms/lang/ATOM-LANG-MACRO-001.md` | draft | 卡状态 `draft` 不在回填范围 ('verified', 'red-team-verified')（判决未定，不预先写边界） |
| `atoms/lang/ATOM-LANG-SETJMP-001.md` | draft | 卡状态 `draft` 不在回填范围 ('verified', 'red-team-verified')（判决未定，不预先写边界） |
| `atoms/lang/ATOM-LANG-VOLATILE-001.md` | draft | 卡状态 `draft` 不在回填范围 ('verified', 'red-team-verified')（判决未定，不预先写边界） |
| `atoms/mem/ATOM-MEM-MALLOC-001.md` | draft | 卡状态 `draft` 不在回填范围 ('verified', 'red-team-verified')（判决未定，不预先写边界） |
| `atoms/mem/ATOM-MEM-STRBOUND-001.md` | draft | 卡状态 `draft` 不在回填范围 ('verified', 'red-team-verified')（判决未定，不预先写边界） |
| `atoms/ub/ATOM-UB-SIGNEDOVF-001.md` | draft | 卡状态 `draft` 不在回填范围 ('verified', 'red-team-verified')（判决未定，不预先写边界） |

## 四、与 639 overlay 交叉校验

- 同源重算一致：**23** 张；不一致：**0** 张；仅 639 有：0 张（639 口径 `n_cards=23`）。

## 五、四态重跑（写盘后口径）

- verified 卡：**23** 张；分布 `{'pass': 23}`；
- 有边界卡：**23** 张。

> 说明：`unknown` 里剩下的卡**没有**任何变异基线覆盖 ⇒ 按 657 红线「没证据的卡照实留空」，**不补假边界**。

## 六、诚实边界（口径）

1. 三元组由 `data/mutation/full_baseline_v*.json` 的**历史** per-variant 记录**现算**，**不是卡生成时的运行时原生三元组**（历史卡从未产出过）；
2. `generator_version` 取基线文件名，是**最接近的代理**，不是生成器自报版本；
3. 迁移 #1（`unknown → pass/fail`）在规格里还要求「**证据复验非 infra**」；本批只补了**边界**这一半，证据复验的逐卡留痕在 651 H1 只覆盖 10 张 draft 卡 ⇒ 23 张 verified 卡的这一半**未逐卡留痕**（登记为交人项）；
4. 写入**只加三行**，卡正文与其它字段逐字节不变（`--apply` 内置断言）。
