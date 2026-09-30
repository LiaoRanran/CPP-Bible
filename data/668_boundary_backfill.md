# 668 · 逐卡边界总账（provenance / semantic scope / evidence / 四态）

> 由 `python tools/semantic_scope_backfill_668.py --report` 生成，**禁止手改**。
> 三元组与四态都不在这里造：分别复用 `boundary_backfill_657` 与 `four_state_verdict_638`。

## 0. 一句话

实测**推翻**了规划里的前提（原文假设『47 卡 0 边界 ⇒ 全 unknown』）：**26 张已有真边界**（四态 `pass`），26 张缺边界 —— 其中**26 张是 `draft`**（按 657 规则不该预写边界），回填范围内真正缺边界的 = **0 张**。

## 1. 四态分布（现算）

| 口径 | 卡数 | 四态分布 |
|---|---:|---|
| 实卡（不含 draft650） | 42 | `{'pass': 26, 'unknown': 16}` |
| 草稿卡（draft650） | 10 | `{'pass': 26, 'unknown': 26}`（含实卡） |

与 `counts_659` 对账：实卡 42 vs 42（应相等）、草稿 10 vs 10（应相等）。

## 2. 缺口清单

- 缺三元组：**26** 张（26 张为 `draft`）
- 在回填范围内却缺三元组：**0** 张
- semantic scope 有缺字段：**21** 张（其中回填范围内 0 张）

> 没有可补的卡：回填范围内（verified / red-team-verified）且缺三元组的卡 = 0 张；其余 26 张全是 `draft`，按 657 既定规则『判决未定，不预先写边界』**不应**回填。

## 3. 逐卡总账

| 卡 | 状态 | 边界 | 来源基线 | 变体 | scope 缺 | 证据数 | 四态 |
|---|---|:--:|---|---:|---|---:|---|
| `atoms/conc/ATOM-CONC-FENCE-001.md` | verified | ✅ | full_baseline_v7.json | 10 | — | 1 | pass |
| `atoms/conc/ATOM-CONC-LOCK-001.md` | verified | ✅ | full_baseline_v7.json | 10 | — | 3 | pass |
| `atoms/conc/ATOM-CONC-RACE-001.md` | verified | ✅ | full_baseline_v7.json | 11 | — | 1 | pass |
| `atoms/draft650/ATOM-DRAFT650-001.md` | draft | ❌ | — | 0 | cpp_standard,compiler,platform,input_domain | 0 | unknown |
| `atoms/draft650/ATOM-DRAFT650-002.md` | draft | ❌ | — | 0 | cpp_standard,compiler,platform,input_domain | 0 | unknown |
| `atoms/draft650/ATOM-DRAFT650-003.md` | draft | ❌ | — | 0 | cpp_standard,compiler,platform,input_domain | 0 | unknown |
| `atoms/draft650/ATOM-DRAFT650-004.md` | draft | ❌ | — | 0 | cpp_standard,compiler,platform,input_domain | 0 | unknown |
| `atoms/draft650/ATOM-DRAFT650-005.md` | draft | ❌ | — | 0 | cpp_standard,compiler,platform,input_domain | 0 | unknown |
| `atoms/draft650/ATOM-DRAFT650-006.md` | draft | ❌ | — | 0 | cpp_standard,compiler,platform,input_domain | 0 | unknown |
| `atoms/draft650/ATOM-DRAFT650-007.md` | draft | ❌ | — | 0 | cpp_standard,compiler,platform,input_domain | 0 | unknown |
| `atoms/draft650/ATOM-DRAFT650-008.md` | draft | ❌ | — | 0 | cpp_standard,compiler,platform,input_domain | 0 | unknown |
| `atoms/draft650/ATOM-DRAFT650-009.md` | draft | ❌ | — | 0 | cpp_standard,compiler,platform,input_domain | 0 | unknown |
| `atoms/draft650/ATOM-DRAFT650-010.md` | draft | ❌ | — | 0 | cpp_standard,compiler,platform,input_domain | 0 | unknown |
| `atoms/hist/ATOM-HIST-AUTOPTR-001.md` | verified | ✅ | full_baseline_v7.json | 10 | — | 1 | pass |
| `atoms/lang/ATOM-LANG-BITFIELD-001.md` | draft | ❌ | — | 0 | cpp_standard,compiler,platform,input_domain | 8 | unknown |
| `atoms/lang/ATOM-LANG-DECAY-001.md` | draft | ❌ | — | 0 | cpp_standard,compiler,platform,input_domain | 6 | unknown |
| `atoms/lang/ATOM-LANG-FNPTR-001.md` | draft | ❌ | — | 0 | cpp_standard,compiler,platform,input_domain | 7 | unknown |
| `atoms/lang/ATOM-LANG-INLINE-001.md` | draft | ❌ | — | 0 | cpp_standard,compiler,platform,input_domain | 1 | unknown |
| `atoms/lang/ATOM-LANG-INTPROMO-001.md` | draft | ❌ | — | 0 | cpp_standard,compiler,platform,input_domain | 9 | unknown |
| `atoms/lang/ATOM-LANG-MACRO-001.md` | draft | ❌ | — | 0 | cpp_standard,compiler,platform,input_domain | 11 | unknown |
| `atoms/lang/ATOM-LANG-SETJMP-001.md` | draft | ❌ | — | 0 | cpp_standard,compiler,platform,input_domain | 9 | unknown |
| `atoms/lang/ATOM-LANG-VOLATILE-001.md` | draft | ❌ | — | 0 | cpp_standard,compiler,platform,input_domain | 7 | unknown |
| `atoms/mem/ATOM-MEM-ALIGN-001.md` | verified | ✅ | full_baseline_v7.json | 10 | — | 1 | pass |
| `atoms/mem/ATOM-MEM-ALLOC-001.md` | verified | ✅ | full_baseline_v7.json | 10 | — | 1 | pass |
| `atoms/mem/ATOM-MEM-ALLOC-002.md` | red-team-verified | ✅ | full_baseline_v7.json | 10 | — | 2 | pass |
| `atoms/mem/ATOM-MEM-LEAK-001.md` | verified | ✅ | full_baseline_v7.json | 10 | — | 1 | pass |
| `atoms/mem/ATOM-MEM-LEAK-002.md` | red-team-verified | ✅ | full_baseline_v7.json | 10 | — | 2 | pass |
| `atoms/mem/ATOM-MEM-MALLOC-001.md` | draft | ❌ | — | 0 | cpp_standard,compiler,platform,input_domain | 12 | unknown |
| `atoms/mem/ATOM-MEM-MOVE-002.md` | verified | ✅ | full_baseline_v7.json | 10 | — | 1 | pass |
| `atoms/mem/ATOM-MEM-NEW-001.md` | verified | ✅ | full_baseline_v7.json | 10 | — | 1 | pass |
| `atoms/mem/ATOM-MEM-NEWARR-001.md` | machine-verified | ❌ | — | 0 | — | 0 | unknown |
| `atoms/mem/ATOM-MEM-PERF-001.md` | verified | ✅ | full_baseline_v7.json | 10 | — | 1 | pass |
| `atoms/mem/ATOM-MEM-PERF-002.md` | verified | ✅ | full_baseline_v7.json | 10 | — | 1 | pass |
| `atoms/mem/ATOM-MEM-PERF-003.md` | verified | ✅ | full_baseline_v7.json | 11 | — | 2 | pass |
| `atoms/mem/ATOM-MEM-PERF-004.md` | red-team-verified | ✅ | full_baseline_v7.json | 10 | — | 2 | pass |
| `atoms/mem/ATOM-MEM-RAII-001.md` | verified | ✅ | full_baseline_v7.json | 10 | — | 1 | pass |
| `atoms/mem/ATOM-MEM-RAII-002.md` | verified | ✅ | full_baseline_v7.json | 10 | — | 1 | pass |
| `atoms/mem/ATOM-MEM-RVREF-001.md` | verified | ✅ | full_baseline_v7.json | 10 | — | 1 | pass |
| `atoms/mem/ATOM-MEM-SHARED-001.md` | verified | ✅ | full_baseline_v7.json | 10 | — | 1 | pass |
| `atoms/mem/ATOM-MEM-SHARED-002.md` | verified | ✅ | full_baseline_v7.json | 10 | — | 1 | pass |
| `atoms/mem/ATOM-MEM-STRBOUND-001.md` | draft | ❌ | — | 0 | cpp_standard,compiler,platform,input_domain | 7 | unknown |
| `atoms/mem/ATOM-MEM-UNIQUE-001.md` | verified | ✅ | full_baseline_v7.json | 10 | — | 1 | pass |
| `atoms/mem/ATOM-MEM-UNIQUE-002.md` | verified | ✅ | full_baseline_v7.json | 10 | — | 1 | pass |
| `atoms/mem/ATOM-MEM-VALUE-001.md` | verified | ✅ | full_baseline_v7.json | 10 | — | 1 | pass |
| `atoms/mem/ATOM-MEM-VALUE-002.md` | verified | ✅ | full_baseline_v7.json | 10 | — | 1 | pass |
| `atoms/mem/ATOM-MEM-WEAK-001.md` | verified | ✅ | full_baseline_v7.json | 10 | — | 1 | pass |
| `atoms/ub/ATOM-UB-DIVZERO-001.md` | machine-verified | ❌ | — | 0 | — | 0 | unknown |
| `atoms/ub/ATOM-UB-GRAY-001.md` | verified | ✅ | full_baseline_v7.json | 10 | — | 1 | pass |
| `atoms/ub/ATOM-UB-NULLDEREF-001.md` | machine-verified | ❌ | — | 0 | — | 0 | unknown |
| `atoms/ub/ATOM-UB-OOB-001.md` | machine-verified | ❌ | — | 0 | — | 0 | unknown |
| `atoms/ub/ATOM-UB-SIGNEDOVF-001.md` | draft | ❌ | — | 0 | cpp_standard,compiler,platform,input_domain | 8 | unknown |
| `atoms/ub/ATOM-UB-WRAP-001.md` | machine-verified | ❌ | — | 0 | — | 0 | unknown |

## 4. 口径说明

- **provenance** = 边界三元组（`mutation_set_hash` / `mutation_count` / `generator_version`）＋它的来源基线文件；哈希由该卡的 per-variant 记录现算（确定性）。
- **semantic scope** = `cpp_standard` / `compiler` / `platform` / `input_domain`（663 回填的四个字段）。
- **evidence** = 卡面 `evidence:` / `refutations:` 里引用的证据卡 id。
- **四态** = `four_state_verdict_638.classify_card` 的输出（缺边界一律降级 `unknown`，这是设计而非缺陷）。
