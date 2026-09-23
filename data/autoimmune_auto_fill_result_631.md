# 631 B1 · auto 42 条 liveness 字段填充结果

- 方案来源：630 A2 方案甲（`mode == auto`）：**42 条**
- 来源独立复核：**42/42** 条通过（重推导符号一致 + 引用卡原文出现该符号）
- 填充：`--apply` 已改 **0** 张卡 / **0** 处（dry_run=True）
- 备份目录：`data/autoimmune_backup_631/`（原文件逐张留档）

## 一、填了什么（按卡汇总）

| 卡 | 填充处数 | 符号 |
|---|---|---|

## 二、来源复核（每条值的出处）

| # | 卡 / 命题 | 符号 | 引用卡 | 复核 |
|---|---|---|---|---|
| 1 | `ATOM-CONC-FENCE-001` / prop-1 | `_Z10spin_plainv` | evidence\conc\EV-CONC-001.md | ✅ |
| 2 | `ATOM-CONC-LOCK-001` / prop-1 | `_Z12bench_singlev` | evidence\conc\EV-CONC-003.md | ✅ |
| 3 | `ATOM-CONC-RACE-001` / prop-1 | `_Z12bench_singlev` | evidence\conc\EV-CONC-005.md，evidence\conc\EV-CONC-006.md | ✅ |
| 4 | `ATOM-HIST-AUTOPTR-001` / prop-1 | `_ZNSt8auto_ptr` | evidence\hist\EV-HIST-001.md，evidence\mem\EV-MEM-003.md | ✅ |
| 5 | `ATOM-HIST-AUTOPTR-001` / prop-2 | `_ZNSt8auto_ptr` | evidence\hist\EV-HIST-001.md，evidence\mem\EV-MEM-003.md | ✅ |
| 6 | `ATOM-HIST-AUTOPTR-001` / prop-4 | `_ZNSt8auto_ptr` | evidence\hist\EV-HIST-001.md | ✅ |
| 7 | `ATOM-MEM-ALIGN-001` / prop-1 | `Padded` | evidence\mem\EV-MEM-019.md | ✅ |
| 8 | `ATOM-MEM-ALIGN-001` / prop-2 | `Aligned` | evidence\mem\EV-MEM-020.md | ✅ |
| 9 | `ATOM-MEM-ALLOC-001` / prop-1 | `allocation only` | evidence\mem\EV-MEM-026.md | ✅ |
| 10 | `ATOM-MEM-ALLOC-001` / prop-2 | `arena` | evidence\mem\EV-MEM-027.md | ✅ |
| 11 | `ATOM-MEM-ALLOC-001` / prop-3 | `monotonic` | evidence\mem\EV-MEM-028.md | ✅ |
| 12 | `ATOM-MEM-LEAK-001` / prop-1 | `destroyed after scope=` | evidence\mem\EV-MEM-036.md | ✅ |
| 13 | `ATOM-MEM-LEAK-001` / prop-2 | `destroyed after scope=` | evidence\mem\EV-MEM-037.md | ✅ |
| 14 | `ATOM-MEM-MOVE-002` / prop-1 | `_ZL8g_allocs` | evidence\mem\EV-MEM-001.md | ✅ |
| 15 | `ATOM-MEM-MOVE-002` / prop-2 | `_ZL8g_allocs` | evidence\mem\EV-MEM-002.md | ✅ |
| 16 | `ATOM-MEM-NEW-001` / prop-1 | `_Znwm` | evidence\mem\EV-MEM-017.md | ✅ |
| 17 | `ATOM-MEM-NEW-001` / prop-2 | `_Znay` | evidence\mem\EV-MEM-018.md | ✅ |
| 18 | `ATOM-MEM-PERF-001` / prop-1 | `_Znay` | evidence\mem\EV-MEM-008.md | ✅ |
| 19 | `ATOM-MEM-PERF-002` / prop-1 | `max_zero_alloc_len` | evidence\mem\EV-MEM-029.md | ✅ |
| 20 | `ATOM-MEM-PERF-003` / prop-1 | `first_heap_len=` | evidence\mem\EV-MEM-038.md | ✅ |
| 21 | `ATOM-MEM-RAII-001` / prop-1 | `g_live` | evidence\mem\EV-MEM-009.md | ✅ |
| 22 | `ATOM-MEM-RAII-001` / prop-2 | `dtor C` | evidence\mem\EV-MEM-010.md | ✅ |
| 23 | `ATOM-MEM-RAII-002` / prop-1 | `rule zero` | evidence\mem\EV-MEM-023.md | ✅ |
| 24 | `ATOM-MEM-RAII-002` / prop-2 | `Buggy` | evidence\mem\EV-MEM-024.md | ✅ |
| 25 | `ATOM-MEM-RAII-002` / prop-3 | `relocation` | evidence\mem\EV-MEM-025.md | ✅ |
| 26 | `ATOM-MEM-RVREF-001` / prop-1 | `_ZN5Probe6copiesE` | evidence\mem\EV-MEM-004.md | ✅ |
| 27 | `ATOM-MEM-RVREF-001` / prop-2 | `_ZN5Probe6copiesE` | evidence\mem\EV-MEM-005.md | ✅ |
| 28 | `ATOM-MEM-SHARED-001` / prop-1 | `destroyed` | evidence\mem\EV-MEM-013.md | ✅ |
| 29 | `ATOM-MEM-SHARED-001` / prop-2 | `destroyed` | evidence\mem\EV-MEM-014.md | ✅ |
| 30 | `ATOM-MEM-SHARED-002` / prop-1 | `_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv` | evidence\mem\EV-MEM-034.md | ✅ |
| 31 | `ATOM-MEM-SHARED-002` / prop-2 | `_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv` | evidence\mem\EV-MEM-034.md | ✅ |
| 32 | `ATOM-MEM-UNIQUE-001` / prop-1 | `unique_ptr` | evidence\mem\EV-MEM-011.md | ✅ |
| 33 | `ATOM-MEM-UNIQUE-001` / prop-2 | `destroyed` | evidence\mem\EV-MEM-012.md | ✅ |
| 34 | `ATOM-MEM-UNIQUE-002` / prop-1 | `unique_ptrIi12StatelessDelE` | evidence\mem\EV-MEM-032.md | ✅ |
| 35 | `ATOM-MEM-UNIQUE-002` / prop-2 | `Sp_counted_deleterIPi6TagDel` | evidence\mem\EV-MEM-033.md | ✅ |
| 36 | `ATOM-MEM-VALUE-001` / prop-1 | `xvalue` | evidence\mem\EV-MEM-006.md | ✅ |
| 37 | `ATOM-MEM-VALUE-001` / prop-2 | `xvalue` | evidence\mem\EV-MEM-007.md | ✅ |
| 38 | `ATOM-MEM-VALUE-002` / prop-1 | `sink_lvalue` | evidence\mem\EV-MEM-021.md | ✅ |
| 39 | `ATOM-MEM-VALUE-002` / prop-2 | `wrap_forward` | evidence\mem\EV-MEM-022.md | ✅ |
| 40 | `ATOM-MEM-WEAK-001` / prop-1 | `destroyed` | evidence\mem\EV-MEM-015.md | ✅ |
| 41 | `ATOM-MEM-WEAK-001` / prop-2 | `destroyed` | evidence\mem\EV-MEM-016.md | ✅ |
| 42 | `ATOM-UB-GRAY-001` / prop-1 | `_Z1gv` | evidence\ub\EV-UB-001.md | ✅ |

## 三、填充后自身免疫率复算

> 未复算（需 `--apply` 后跑 gate）。

## 四、诚实登记

1. **只填 `liveness`**：`object`（语义）与 `signed_by`（人签）**一条没填**（§零.3 不代签、机器不做语义判断）；
2. **写入方式是逐行最小编辑**：改前备份 + 改后用 YAML 结构比对，确认除 `liveness` 外零变化（`unexpected_diffs` 为空）；
3. 符号取自**引用卡的 artifact_assert**，与 gate 判定 `OBSERVATION-LIVENESS` 的口径一致；但「符号存在」**不等于**「该符号确为本命题的观测证据」——语义正确性仍需人复核（B2 清单的 human 项不含这些，但建议抽检）；
4. 若填充后 warn 数未下降，如实记录（见 §三 与验收报告偏差表）。
