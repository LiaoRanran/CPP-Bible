# 活性锚补全 what-if 分析（612 线 B · B3 · 只读）

> 生成时间：2026-09-20T21:36:37 ｜ 命令：`python tools/liveness_completion_whatif.py --write`
>
> **只读推演**：完全复用 `gate_engine` 的 `OBSERVATION-LIVENESS` 两分支与判定单点，仅叠加假设的 `liveness` 再跑同一判定；不修改 gate / 不写命题卡。

## 1 · 三情景投影

| 情景 | OBSERVATION-LIVENESS warn | 说明 |
|---|---|---|
| `baseline`（当前真实门禁） | **50** | 50 条 observation 全缺命题级锚 |
| `full_anchor`（假设补全合法锚） | **0** （消 50） | 可锚的全补；不可锚的保持原状 |
| `with_review`（叠加 B2 人审锚） | **50** （已应用 0 条） | 随人审推进而更新 |

## 2 · 可达成的 warn 消除上限

- observation 命题总数：**50**
- **可锚**（引用卡有合法非通用工件符号，自动补 `fixture_symbol` 即可消除 warn）：**50**
- **须改标**（引用卡无合法非通用符号，只能靠人审改标 `inference` / `external_basis`）：**0**
- 交由 `OBSERVATION-NEEDS-ARTIFACT`（block）处置、不在本 warn 口径内：**0**

> 结论：自动补全**最多**能消除 **50 / 50** 条 warn；剩余 **0** 条必须靠人审改标（非自动工具可解）。合法的 fixture_symbol 锚会**同时**满足命题级锚（分支①）与卡级活性对照（`_has_fixture_specific_assert_symbol`，分支②），故补锚即两分支同消。

## 3 · 逐命题明细（50 条）

| 卡 | 命题 | 引用卡 | baseline | full_anchor | 可锚符号(首) | 分类 |
|---|---|---|---|---|---|---|
| `ATOM-CONC-FENCE-001` | `prop-1` | EV-CONC-001, EV-CONC-002 | branch1 | ok | `_Z10spin_plainv` | 可锚(补 fixture_symbol) |
| `ATOM-CONC-LOCK-001` | `prop-1` | EV-CONC-003, EV-CONC-004 | branch1 | ok | `_Z11bench_mutexv` | 可锚(补 fixture_symbol) |
| `ATOM-CONC-RACE-001` | `prop-1` | EV-CONC-005, EV-CONC-006 | branch1 | ok | `_Z10bench_racev` | 可锚(补 fixture_symbol) |
| `ATOM-HIST-AUTOPTR-001` | `prop-1` | EV-HIST-001, EV-MEM-003 | branch1 | ok | `_ZNSt8auto_ptr` | 可锚(补 fixture_symbol) |
| `ATOM-HIST-AUTOPTR-001` | `prop-2` | EV-HIST-001, EV-MEM-003 | branch1 | ok | `_ZNSt8auto_ptr` | 可锚(补 fixture_symbol) |
| `ATOM-HIST-AUTOPTR-001` | `prop-4` | EV-HIST-001 | branch1 | ok | `_ZNSt8auto_ptr` | 可锚(补 fixture_symbol) |
| `ATOM-LANG-INLINE-001` | `prop-1` | EV-LANG-001, EV-LANG-002 | branch1 | ok | `_Z10tu_a_valuev` | 可锚(补 fixture_symbol) |
| `ATOM-LANG-INLINE-001` | `prop-2` | EV-LANG-001, EV-LANG-002 | branch1 | ok | `_Z10tu_a_valuev` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-ALIGN-001` | `prop-1` | EV-MEM-019 | branch1 | ok | `Padded` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-ALIGN-001` | `prop-2` | EV-MEM-020 | branch1 | ok | `Aligned` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-ALLOC-001` | `prop-1` | EV-MEM-026 | branch1 | ok | `allocation only` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-ALLOC-001` | `prop-2` | EV-MEM-027 | branch1 | ok | `arena` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-ALLOC-001` | `prop-3` | EV-MEM-028 | branch1 | ok | `delegating` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-ALLOC-002` | `prop-1` | EV-MEM-040, EV-MEM-041 | branch1 | ok | `%s_meta_bookkeeping_bytes=` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-ALLOC-002` | `prop-2` | EV-MEM-040, EV-MEM-041 | branch1 | ok | `%s_meta_bookkeeping_bytes=` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-LEAK-001` | `prop-1` | EV-MEM-036 | branch1 | ok | `_Znwm` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-LEAK-001` | `prop-2` | EV-MEM-037 | branch1 | ok | `_Znwm` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-LEAK-002` | `prop-1` | EV-MEM-042, EV-MEM-043 | branch1 | ok | `cycle_allocated=` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-LEAK-002` | `prop-2` | EV-MEM-042, EV-MEM-043 | branch1 | ok | `cycle_allocated=` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-MOVE-002` | `prop-1` | EV-MEM-001 | branch1 | ok | `_ZL8g_allocs` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-MOVE-002` | `prop-2` | EV-MEM-002 | branch1 | ok | `_ZL8g_allocs` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-NEW-001` | `prop-1` | EV-MEM-017 | branch1 | ok | `_Znwm` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-NEW-001` | `prop-2` | EV-MEM-018 | branch1 | ok | `_Znam` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-PERF-001` | `prop-1` | EV-MEM-008 | branch1 | ok | `QWORD PTR` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-PERF-002` | `prop-1` | EV-MEM-029 | branch1 | ok | `max_zero_alloc_len` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-PERF-003` | `prop-1` | EV-MEM-038 | branch1 | ok | `capacity_at_sso_capacity=` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-PERF-004` | `prop-1` | EV-MEM-044, EV-MEM-045 | branch1 | ok | `counters_all_advanced=` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-PERF-004` | `prop-2` | EV-MEM-044, EV-MEM-045 | branch1 | ok | `counters_all_advanced=` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-RAII-001` | `prop-1` | EV-MEM-009 | branch1 | ok | `g_live` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-RAII-001` | `prop-2` | EV-MEM-010 | branch1 | ok | `Tag::~Tag` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-RAII-002` | `prop-1` | EV-MEM-023 | branch1 | ok | `owner_changed` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-RAII-002` | `prop-2` | EV-MEM-024 | branch1 | ok | `Buggy` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-RAII-002` | `prop-3` | EV-MEM-025 | branch1 | ok | `relocation` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-RVREF-001` | `prop-1` | EV-MEM-004 | branch1 | ok | `_ZN5Probe5movesE` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-RVREF-001` | `prop-2` | EV-MEM-005 | branch1 | ok | `_ZN5Probe6copiesE` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-SHARED-001` | `prop-1` | EV-MEM-013 | branch1 | ok | `destroyed` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-SHARED-001` | `prop-2` | EV-MEM-014 | branch1 | ok | `destroyed` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-SHARED-002` | `prop-1` | EV-MEM-034 | branch1 | ok | `_M_release_last_use_coldEv` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-SHARED-002` | `prop-2` | EV-MEM-034 | branch1 | ok | `_M_release_last_use_coldEv` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-UNIQUE-001` | `prop-1` | EV-MEM-011 | branch1 | ok | `unique_ptr` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-UNIQUE-001` | `prop-2` | EV-MEM-012 | branch1 | ok | `destroyed` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-UNIQUE-002` | `prop-1` | EV-MEM-032 | branch1 | ok | `Sp_counted_deleter` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-UNIQUE-002` | `prop-2` | EV-MEM-033 | branch1 | ok | `10_M_destroyEv` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-VALUE-001` | `prop-1` | EV-MEM-006 | branch1 | ok | `prvalue` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-VALUE-001` | `prop-2` | EV-MEM-007 | branch1 | ok | `xvalue` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-VALUE-002` | `prop-1` | EV-MEM-021 | branch1 | ok | `auto&& from` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-VALUE-002` | `prop-2` | EV-MEM-022 | branch1 | ok | `forward rvalue: copies=` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-WEAK-001` | `prop-1` | EV-MEM-015 | branch1 | ok | `destroyed` | 可锚(补 fixture_symbol) |
| `ATOM-MEM-WEAK-001` | `prop-2` | EV-MEM-016 | branch1 | ok | `destroyed` | 可锚(补 fixture_symbol) |
| `ATOM-UB-GRAY-001` | `prop-1` | EV-UB-001 | branch1 | ok | `_Z1gv` | 可锚(补 fixture_symbol) |

## 4 · 口径与边界（诚实）

- **不重复实现判据**：`_prop_liveness_ok` / `_has_fixture_specific_assert_symbol` / `_falsification_quantified` / `_has_non_env_run_key` / `_has_artifact_assertion` 全部直接 import 自 `gate_engine`，投影口径与门禁逐字一致。
- **假设 ≠ 提交**：本工具只做推演，不写命题卡、不改 gate；真正补全活性锚是 B2 人审的权力。
- **改标属人审**：`须改标` 类命题的引用卡里没有可由单一工件读数证伪的非通用符号，自动工具无法凭空造锚 —— 必须由人决定改标 `inference`（补 external_basis）或 `external_basis`。
- **`deferred`**：该命题引用卡均无工件断言，归 `OBSERVATION-NEEDS-ARTIFACT`（block）辖，不计入本 warn 口径。
