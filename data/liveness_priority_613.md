# 613 · 活性锚补全优先级清单（A1）

> 生成：`python tools/liveness_priority_613.py` ｜ 时间：2026-09-20T23:30:23
> 依据：612 B1 候选 `data/liveness_candidates_612.jsonl` + KC 台账 `data/kc_inventory_612.json`。
> 评分 = 命题重要性 × 证据可用性 × 补全成本权重（见 tools/liveness_priority_613.py 文档串）。
> **只读**：本工具不写入受控目录；实际写卡需人授权（见 A2）。

## 汇总

| 成本档 | 命题数 | 说明 |
|---|---|---|
| low | 9 | class A / B+high ⇒ 锚可直接引用，优先批量补 |
| medium | 26 | class B+medium ⇒ 可补但需复核 |
| high | 15 | class C（无候选/需人工）⇒ 留作人审 |
| **合计** | **50** | observation 命题总数 |

## 优先级清单（降序）

| # | 命题 | 卡 | 域 | 难度 | 档 | 置信 | 候选数 | 最佳锚符号 | 来源 | 优先级 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `ATOM-HIST-AUTOPTR-001::prop-2` | ATOM-HIST-AUTOPTR-001 | HIST | 3 | A | high | 3 | `is_copy_constructible` | EV-MEM-003 | 77.28 |
| 2 | `ATOM-MEM-MOVE-002::prop-2` | ATOM-MEM-MOVE-002 | MEM | 4 | B | medium | 3 | `FixedBuf` | EV-MEM-002 | 51.84 |
| 3 | `ATOM-UB-GRAY-001::prop-1` | ATOM-UB-GRAY-001 | UB | 5 | B | medium | 2 | `alias_kill` | EV-UB-001 | 47.6 |
| 4 | `ATOM-MEM-PERF-003::prop-1` | ATOM-MEM-PERF-003 | MEM | 2 | A | high | 3 | `capacity_at_len1` | EV-MEM-038 | 47.04 |
| 5 | `ATOM-MEM-RAII-002::prop-2` | ATOM-MEM-RAII-002 | MEM | 2 | A | high | 3 | `Correct` | EV-MEM-024 | 47.04 |
| 6 | `ATOM-MEM-MOVE-002::prop-1` | ATOM-MEM-MOVE-002 | MEM | 4 | B | medium | 1 | `BadBuf` | EV-MEM-001 | 46.08 |
| 7 | `ATOM-MEM-UNIQUE-001::prop-1` | ATOM-MEM-UNIQUE-001 | MEM | 2 | A | high | 3 | `Big` | EV-MEM-011 | 43.68 |
| 8 | `ATOM-MEM-VALUE-001::prop-1` | ATOM-MEM-VALUE-001 | MEM | 2 | A | high | 3 | `type_traits` | EV-MEM-006 | 43.68 |
| 9 | `ATOM-MEM-LEAK-002::prop-1` | ATOM-MEM-LEAK-002 | MEM | 2 | A | high | 3 | `cycle_allocated` | EV-MEM-043 | 40.32 |
| 10 | `ATOM-MEM-PERF-004::prop-1` | ATOM-MEM-PERF-004 | MEM | 2 | A | high | 3 | `padded_offset_bytes` | EV-MEM-044 | 40.32 |
| 11 | `ATOM-MEM-SHARED-002::prop-2` | ATOM-MEM-SHARED-002 | MEM | 2 | A | high | 3 | `_M_release` | EV-MEM-034 | 40.32 |
| 12 | `ATOM-HIST-AUTOPTR-001::prop-1` | ATOM-HIST-AUTOPTR-001 | HIST | 3 | B | medium | 3 | `CopyConstructible` | EV-MEM-003 | 33.12 |
| 13 | `ATOM-HIST-AUTOPTR-001::prop-4` | ATOM-HIST-AUTOPTR-001 | HIST | 3 | B | medium | 3 | `_ZNSt8auto_ptr` | EV-HIST-001 | 33.12 |
| 14 | `ATOM-MEM-RAII-001::prop-2` | ATOM-MEM-RAII-001 | MEM | 2 | B | medium | 3 | `_ZN3TagD1Ev` | EV-MEM-010 | 28.8 |
| 15 | `ATOM-MEM-SHARED-001::prop-2` | ATOM-MEM-SHARED-001 | MEM | 2 | B | medium | 3 | `check_sanitizer` | EV-MEM-014 | 25.92 |
| 16 | `ATOM-MEM-SHARED-001::prop-1` | ATOM-MEM-SHARED-001 | MEM | 2 | B | medium | 1 | `use_count` | EV-MEM-013 | 23.04 |
| 17 | `ATOM-MEM-UNIQUE-002::prop-1` | ATOM-MEM-UNIQUE-002 | MEM | 2 | B | medium | 3 | `StatelessFinalDel` | EV-MEM-032 | 20.16 |
| 18 | `ATOM-MEM-UNIQUE-002::prop-2` | ATOM-MEM-UNIQUE-002 | MEM | 2 | B | medium | 3 | `_M_destroy` | EV-MEM-033 | 20.16 |
| 19 | `ATOM-MEM-VALUE-002::prop-2` | ATOM-MEM-VALUE-002 | MEM | 2 | B | medium | 3 | `wrap_bare` | EV-MEM-022 | 20.16 |
| 20 | `ATOM-MEM-NEW-001::prop-2` | ATOM-MEM-NEW-001 | MEM | 2 | B | medium | 3 | `_Znam` | EV-MEM-018 | 18.72 |
| 21 | `ATOM-MEM-VALUE-002::prop-1` | ATOM-MEM-VALUE-002 | MEM | 2 | B | medium | 1 | `static_assert` | EV-MEM-021 | 17.92 |
| 22 | `ATOM-CONC-RACE-001::prop-1` | ATOM-CONC-RACE-001 | conc | 2 | B | medium | 3 | `_Z10bench_racev` | EV-CONC-005 | 17.28 |
| 23 | `ATOM-LANG-INLINE-001::prop-1` | ATOM-LANG-INLINE-001 | LANG | 2 | B | medium | 3 | `_ASSERT_ALLOWED_KEYS` | EV-LANG-001 | 17.28 |
| 24 | `ATOM-LANG-INLINE-001::prop-2` | ATOM-LANG-INLINE-001 | LANG | 2 | B | medium | 3 | `_ASSERT_ALLOWED_KEYS` | EV-LANG-001 | 17.28 |
| 25 | `ATOM-MEM-ALLOC-002::prop-1` | ATOM-MEM-ALLOC-002 | MEM | 2 | B | medium | 3 | `bookkeeping_bytes` | EV-MEM-040 | 17.28 |
| 26 | `ATOM-MEM-ALLOC-002::prop-2` | ATOM-MEM-ALLOC-002 | MEM | 2 | B | medium | 3 | `bookkeeping_bytes` | EV-MEM-040 | 17.28 |
| 27 | `ATOM-MEM-LEAK-001::prop-2` | ATOM-MEM-LEAK-001 | MEM | 2 | B | medium | 3 | `ASAN_OPTIONS` | EV-MEM-037 | 17.28 |
| 28 | `ATOM-MEM-LEAK-002::prop-2` | ATOM-MEM-LEAK-002 | MEM | 2 | B | medium | 3 | `Node` | EV-MEM-043 | 17.28 |
| 29 | `ATOM-MEM-PERF-004::prop-2` | ATOM-MEM-PERF-004 | MEM | 2 | B | medium | 3 | `cache_line_size` | EV-MEM-044 | 17.28 |
| 30 | `ATOM-MEM-SHARED-002::prop-1` | ATOM-MEM-SHARED-002 | MEM | 2 | B | medium | 3 | `_M_release` | EV-MEM-034 | 17.28 |
| 31 | `ATOM-CONC-LOCK-001::prop-1` | ATOM-CONC-LOCK-001 | conc | 1 | A | high | 3 | `single_thread_baseline` | EV-CONC-003 | 16.8 |
| 32 | `ATOM-MEM-PERF-001::prop-1` | ATOM-MEM-PERF-001 | MEM | 1 | B | medium | 3 | `_Znam` | EV-MEM-008 | 13.68 |
| 33 | `ATOM-MEM-RVREF-001::prop-1` | ATOM-MEM-RVREF-001 | MEM | 2 | B | medium | 2 | `artifact_sha256` | EV-MEM-004 | 13.6 |
| 34 | `ATOM-MEM-RVREF-001::prop-2` | ATOM-MEM-RVREF-001 | MEM | 2 | B | medium | 2 | `refute:ambiguous_expected` | EV-MEM-005 | 13.6 |
| 35 | `ATOM-CONC-FENCE-001::prop-1` | ATOM-CONC-FENCE-001 | conc | 1 | B | medium | 3 | `_Z10spin_plainv` | EV-CONC-001 | 7.2 |
| 36 | `ATOM-MEM-RAII-001::prop-1` | ATOM-MEM-RAII-001 | MEM | 2 | C | low | 0 | `` |  | 6.0 |
| 37 | `ATOM-MEM-PERF-002::prop-1` | ATOM-MEM-PERF-002 | MEM | 2 | C | low | 0 | `` |  | 4.2 |
| 38 | `ATOM-MEM-RAII-002::prop-1` | ATOM-MEM-RAII-002 | MEM | 2 | C | low | 0 | `` |  | 4.2 |
| 39 | `ATOM-MEM-RAII-002::prop-3` | ATOM-MEM-RAII-002 | MEM | 2 | C | low | 0 | `` |  | 4.2 |
| 40 | `ATOM-MEM-ALLOC-001::prop-1` | ATOM-MEM-ALLOC-001 | MEM | 2 | C | low | 0 | `` |  | 4.05 |
| 41 | `ATOM-MEM-ALLOC-001::prop-2` | ATOM-MEM-ALLOC-001 | MEM | 2 | C | low | 0 | `` |  | 4.05 |
| 42 | `ATOM-MEM-ALLOC-001::prop-3` | ATOM-MEM-ALLOC-001 | MEM | 2 | C | low | 0 | `` |  | 4.05 |
| 43 | `ATOM-MEM-NEW-001::prop-1` | ATOM-MEM-NEW-001 | MEM | 2 | C | low | 0 | `` |  | 3.9 |
| 44 | `ATOM-MEM-UNIQUE-001::prop-2` | ATOM-MEM-UNIQUE-001 | MEM | 2 | C | low | 0 | `` |  | 3.9 |
| 45 | `ATOM-MEM-VALUE-001::prop-2` | ATOM-MEM-VALUE-001 | MEM | 2 | C | low | 0 | `` |  | 3.9 |
| 46 | `ATOM-MEM-WEAK-001::prop-1` | ATOM-MEM-WEAK-001 | MEM | 2 | C | low | 0 | `` |  | 3.9 |
| 47 | `ATOM-MEM-WEAK-001::prop-2` | ATOM-MEM-WEAK-001 | MEM | 2 | C | low | 0 | `` |  | 3.9 |
| 48 | `ATOM-MEM-ALIGN-001::prop-1` | ATOM-MEM-ALIGN-001 | MEM | 2 | C | low | 0 | `` |  | 3.6 |
| 49 | `ATOM-MEM-ALIGN-001::prop-2` | ATOM-MEM-ALIGN-001 | MEM | 2 | C | low | 0 | `` |  | 3.6 |
| 50 | `ATOM-MEM-LEAK-001::prop-1` | ATOM-MEM-LEAK-001 | MEM | 2 | C | low | 0 | `` |  | 3.6 |

## 低成本可批量补全集合（A2 输入）

| 命题 | 卡 | 锚类型 | 锚符号 | 来源 |
|---|---|---|---|---|
| `ATOM-HIST-AUTOPTR-001::prop-2` | ATOM-HIST-AUTOPTR-001 | fixture_symbol | `is_copy_constructible` | EV-MEM-003 |
| `ATOM-MEM-PERF-003::prop-1` | ATOM-MEM-PERF-003 | fixture_symbol | `capacity_at_len1` | EV-MEM-038 |
| `ATOM-MEM-RAII-002::prop-2` | ATOM-MEM-RAII-002 | fixture_symbol | `Correct` | EV-MEM-024 |
| `ATOM-MEM-UNIQUE-001::prop-1` | ATOM-MEM-UNIQUE-001 | fixture_symbol | `Big` | EV-MEM-011 |
| `ATOM-MEM-VALUE-001::prop-1` | ATOM-MEM-VALUE-001 | fixture_symbol | `type_traits` | EV-MEM-006 |
| `ATOM-MEM-LEAK-002::prop-1` | ATOM-MEM-LEAK-002 | fixture_symbol | `cycle_allocated` | EV-MEM-043 |
| `ATOM-MEM-PERF-004::prop-1` | ATOM-MEM-PERF-004 | fixture_symbol | `padded_offset_bytes` | EV-MEM-044 |
| `ATOM-MEM-SHARED-002::prop-2` | ATOM-MEM-SHARED-002 | fixture_symbol | `_M_release` | EV-MEM-034 |
| `ATOM-CONC-LOCK-001::prop-1` | ATOM-CONC-LOCK-001 | fixture_symbol | `single_thread_baseline` | EV-CONC-003 |

> 注：C 档命题在候选工件中无行（612 已知坑），其 class 由生成器回填；此处按「无可用锚」计入 high 成本。
