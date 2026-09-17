# 待补命题级活性锚清单（575 任务 3）

> 机器产出清单，**绝不自动写入卡面**：补锚是知识活，交人或 576 之后的强模型知识轮。
> 判据：`claim_structured[*].liveness = {kind: fixture_symbol, symbol: <夹具特有符号>}`，
> 符号须真实出现在本命题引用卡的工件断言中、且非通用符号。

**缺锚 observation 命题：50 条**

| 卡 | 命题 | 引用卡 | 可锚形态 | 建议可锚符号（仅提示） |
|---|---|---|---|---|
| ATOM-CONC-FENCE-001 | prop-1 | EV-CONC-001,EV-CONC-002 | fixture_symbol,quantified,run_key | `_Z10spin_plainv` |
| ATOM-CONC-LOCK-001 | prop-1 | EV-CONC-003,EV-CONC-004 | fixture_symbol,quantified,run_key | `_Z12bench_singlev` |
| ATOM-CONC-RACE-001 | prop-1 | EV-CONC-005,EV-CONC-006 | fixture_symbol,quantified,run_key | `_Z12bench_singlev` |
| ATOM-HIST-AUTOPTR-001 | prop-1 | EV-HIST-001,EV-MEM-003 | fixture_symbol | `_ZNSt8auto_ptr` |
| ATOM-HIST-AUTOPTR-001 | prop-2 | EV-HIST-001,EV-MEM-003 | fixture_symbol | `_ZNSt8auto_ptr` |
| ATOM-HIST-AUTOPTR-001 | prop-4 | EV-HIST-001 | fixture_symbol | `_ZNSt8auto_ptr` |
| ATOM-LANG-INLINE-001 | prop-1 | EV-LANG-001,EV-LANG-002 | fixture_symbol,quantified,run_key | `_Z10tu_a_valuev` |
| ATOM-LANG-INLINE-001 | prop-2 | EV-LANG-001,EV-LANG-002 | fixture_symbol,quantified,run_key | `_Z10tu_a_valuev` |
| ATOM-MEM-ALIGN-001 | prop-1 | EV-MEM-019 | fixture_symbol,quantified | `Padded` |
| ATOM-MEM-ALIGN-001 | prop-2 | EV-MEM-020 | fixture_symbol,quantified | `Aligned` |
| ATOM-MEM-ALLOC-001 | prop-1 | EV-MEM-026 | fixture_symbol,quantified | `allocation only` |
| ATOM-MEM-ALLOC-001 | prop-2 | EV-MEM-027 | fixture_symbol,quantified | `arena` |
| ATOM-MEM-ALLOC-001 | prop-3 | EV-MEM-028 | fixture_symbol,quantified | `monotonic` |
| ATOM-MEM-ALLOC-002 | prop-1 | EV-MEM-040,EV-MEM-041 | fixture_symbol,quantified | `%s_meta_total_bytes=` |
| ATOM-MEM-ALLOC-002 | prop-2 | EV-MEM-040,EV-MEM-041 | fixture_symbol,quantified | `%s_meta_total_bytes=` |
| ATOM-MEM-LEAK-001 | prop-1 | EV-MEM-036 | fixture_symbol,quantified | `destroyed after scope=` |
| ATOM-MEM-LEAK-001 | prop-2 | EV-MEM-037 | fixture_symbol,quantified | `destroyed after scope=` |
| ATOM-MEM-LEAK-002 | prop-1 | EV-MEM-042,EV-MEM-043 | fixture_symbol,quantified | `scoped_dtor_count=` |
| ATOM-MEM-LEAK-002 | prop-2 | EV-MEM-042,EV-MEM-043 | fixture_symbol,quantified | `scoped_dtor_count=` |
| ATOM-MEM-MOVE-002 | prop-1 | EV-MEM-001 | fixture_symbol,quantified | `_ZL8g_allocs` |
| ATOM-MEM-MOVE-002 | prop-2 | EV-MEM-002 | fixture_symbol,quantified | `_ZL8g_allocs` |
| ATOM-MEM-NEW-001 | prop-1 | EV-MEM-017 | quantified | `-` |
| ATOM-MEM-NEW-001 | prop-2 | EV-MEM-018 | fixture_symbol,quantified | `_Znay` |
| ATOM-MEM-PERF-001 | prop-1 | EV-MEM-008 | fixture_symbol,quantified | `_Znay` |
| ATOM-MEM-PERF-002 | prop-1 | EV-MEM-029 | fixture_symbol,quantified | `max_zero_alloc_len` |
| ATOM-MEM-PERF-003 | prop-1 | EV-MEM-038 | fixture_symbol,quantified | `first_heap_len=` |
| ATOM-MEM-PERF-004 | prop-1 | EV-MEM-044,EV-MEM-045 | fixture_symbol,quantified | `tight_same_line=` |
| ATOM-MEM-PERF-004 | prop-2 | EV-MEM-044,EV-MEM-045 | fixture_symbol,quantified | `tight_same_line=` |
| ATOM-MEM-RAII-001 | prop-1 | EV-MEM-009 | fixture_symbol,quantified | `g_live` |
| ATOM-MEM-RAII-001 | prop-2 | EV-MEM-010 | fixture_symbol | `dtor C` |
| ATOM-MEM-RAII-002 | prop-1 | EV-MEM-023 | fixture_symbol,quantified | `rule zero` |
| ATOM-MEM-RAII-002 | prop-2 | EV-MEM-024 | fixture_symbol,quantified | `Buggy` |
| ATOM-MEM-RAII-002 | prop-3 | EV-MEM-025 | fixture_symbol,quantified | `relocation` |
| ATOM-MEM-RVREF-001 | prop-1 | EV-MEM-004 | fixture_symbol,quantified | `_ZN5Probe6copiesE` |
| ATOM-MEM-RVREF-001 | prop-2 | EV-MEM-005 | fixture_symbol,quantified | `_ZN5Probe6copiesE` |
| ATOM-MEM-SHARED-001 | prop-1 | EV-MEM-013 | fixture_symbol,quantified | `destroyed` |
| ATOM-MEM-SHARED-001 | prop-2 | EV-MEM-014 | fixture_symbol,quantified | `destroyed` |
| ATOM-MEM-SHARED-002 | prop-1 | EV-MEM-034 | fixture_symbol,quantified | `_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv` |
| ATOM-MEM-SHARED-002 | prop-2 | EV-MEM-034 | fixture_symbol,quantified | `_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv` |
| ATOM-MEM-UNIQUE-001 | prop-1 | EV-MEM-011 | fixture_symbol,quantified | `unique_ptr` |
| ATOM-MEM-UNIQUE-001 | prop-2 | EV-MEM-012 | fixture_symbol,quantified | `destroyed` |
| ATOM-MEM-UNIQUE-002 | prop-1 | EV-MEM-032 | fixture_symbol,quantified | `unique_ptrIi12StatelessDelE` |
| ATOM-MEM-UNIQUE-002 | prop-2 | EV-MEM-033 | fixture_symbol,quantified | `Sp_counted_deleterIPi6TagDel` |
| ATOM-MEM-VALUE-001 | prop-1 | EV-MEM-006 | fixture_symbol | `xvalue` |
| ATOM-MEM-VALUE-001 | prop-2 | EV-MEM-007 | fixture_symbol,quantified | `xvalue` |
| ATOM-MEM-VALUE-002 | prop-1 | EV-MEM-021 | fixture_symbol,quantified | `sink_lvalue` |
| ATOM-MEM-VALUE-002 | prop-2 | EV-MEM-022 | fixture_symbol,quantified | `wrap_forward` |
| ATOM-MEM-WEAK-001 | prop-1 | EV-MEM-015 | fixture_symbol,quantified | `destroyed` |
| ATOM-MEM-WEAK-001 | prop-2 | EV-MEM-016 | fixture_symbol,quantified | `destroyed` |
| ATOM-UB-GRAY-001 | prop-1 | EV-UB-001 | fixture_symbol,quantified | `_Z1gv` |
