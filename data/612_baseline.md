# 612 基线（任务0 · 先量，只读统计）

> 所有数字来自 611 各工具同源真源，可逐字节复算。A/B/C 分类、优先级得分、难度分级均为**自动估算的建议**，明确标「待细化」，不声称客观结论。

## 1 · 桥接候选分布（98 条）

- 主题分布：{'MEM': 97, 'CONC': 1}
- 跨分量对：7 对；Top：[{'pair': [7, 10], 'bridges': 46}, {'pair': [8, 10], 'bridges': 23}, {'pair': [6, 10], 'bridges': 23}, {'pair': [7, 8], 'bridges': 2}, {'pair': [6, 7], 'bridges': 2}, {'pair': [4, 9], 'bridges': 1}, {'pair': [6, 8], 'bridges': 1}]
- 出现最多的 MIS（在候选中）：[{'mis': 'MIS-MEM-011', 'in_candidates': 26}, {'mis': 'MIS-MEM-015', 'in_candidates': 26}, {'mis': 'MIS-MEM-013', 'in_candidates': 25}, {'mis': 'MIS-MEM-014', 'in_candidates': 25}, {'mis': 'MIS-MEM-001', 'in_candidates': 4}, {'mis': 'MIS-MEM-002', 'in_candidates': 4}, {'mis': 'MIS-MEM-003', 'in_candidates': 4}, {'mis': 'MIS-MEM-004', 'in_candidates': 4}, {'mis': 'MIS-MEM-005', 'in_candidates': 4}, {'mis': 'MIS-MEM-012', 'in_candidates': 4}]
- 论证关系强度预估（refutations 词频 Jaccard 启发式）：{'high': 2, 'medium': 36, 'low': 60}

## 2 · 活性锚缺口分类（50 条缺 liveness 的 observation）

- 初步分类：A（高置信可自动补）49 · B（中置信需人审选）1 · C（建议改标 inference）0
- A/B/C 为**初步**自动分类（符号重叠启发式），待 B1 用更细的符号唯一性/可观测性评估细化

| 命题 | 类 | 理由 |
|---|---|---|
| `prop-1` | A | 证据卡符号与命题陈述有重叠（1 个）：['atomic_signal_fence'] |
| `prop-1` | A | 证据卡符号与命题陈述有重叠（15 个）：['CAS', 'CONC', 'EV', 'Examples', '_atom_lock_cost'] |
| `prop-1` | A | 证据卡符号与命题陈述有重叠（7 个）：['kIters', 'race', 'race_ops_total', 'safe', 'safe_final'] |
| `prop-1` | A | 证据卡符号与命题陈述有重叠（4 个）：['GCC', 'O2', 'auto_ptr', 'unique_ptr'] |
| `prop-2` | A | 证据卡符号与命题陈述有重叠（9 个）：['CopyConstructible', 'auto_ptr', 'false', 'is_constructible' |
| `prop-4` | A | 证据卡符号与命题陈述有重叠（11 个）：['CI', 'EV', 'GCC', 'HIST', 'Ubuntu'] |
| `prop-1` | A | 证据卡符号与命题陈述有重叠（10 个）：['O0', 'O2', 'TU', 'ab_tu_a', 'ab_tu_b'] |
| `prop-2` | A | 证据卡符号与命题陈述有重叠（5 个）：['TU', 'stable', 'stable_a', 'stable_b', 'token'] |
| `prop-1` | A | 证据卡符号与命题陈述有重叠（4 个）：['Padded', 'bytes', 'offsetof', 'padding'] |
| `prop-2` | A | 证据卡符号与命题陈述有重叠（3 个）：['Aligned', 'alignof', 'memcpy'] |
| `prop-1` | A | 证据卡符号与命题陈述有重叠（10 个）：['allocate', 'allocator', 'allocator_traits', 'allocs', 'con |
| `prop-2` | A | 证据卡符号与命题陈述有重叠（7 个）：['allocator', 'arena', 'bytes', 'calls', 'heap_new'] |
| `prop-3` | A | 证据卡符号与命题陈述有重叠（6 个）：['bytes', 'delegating', 'monotonic_buffer_resource', 'pmr', ' |
| `prop-1` | A | 证据卡符号与命题陈述有重叠（9 个）：['O2', 'arena', 'bit', 'bitmap', 'bookkeeping_bytes'] |
| `prop-2` | A | 证据卡符号与命题陈述有重叠（8 个）：['EV', 'MEM', 'bit', 'bitmap', 'bookkeeping'] |
| `prop-1` | A | 证据卡符号与命题陈述有重叠（11 个）：['O0', 'O2', 'after', 'children', 'constructed'] |
| `prop-2` | A | 证据卡符号与命题陈述有重叠（11 个）：['EV', 'MEM', 'after', 'children', 'constructed'] |
| `prop-1` | A | 证据卡符号与命题陈述有重叠（5 个）：['cycle_allocated', 'cycle_destroyed', 'cycle_live_objects',  |
| `prop-2` | A | 证据卡符号与命题陈述有重叠（16 个）：['AddressSanitizer', 'EV', 'LSan', 'MEM', 'Node'] |
| `prop-1` | A | 证据卡符号与命题陈述有重叠（4 个）：['GCC', 'O0', 'O2', 'call'] |
| `prop-2` | A | 证据卡符号与命题陈述有重叠（5 个）：['FixedBuf', 'HeapBuf', 'array', 'movaps', 'pshufd'] |
| `prop-1` | A | 证据卡符号与命题陈述有重叠（5 个）：['after', 'alloc', 'ctor', 'dealloc', 'dtor'] |
| `prop-2` | A | 证据卡符号与命题陈述有重叠（6 个）：['array', 'calls', 'huge', 'nothrow', 'null'] |
| `prop-1` | A | 证据卡符号与命题陈述有重叠（7 个）：['O0', 'O2', 'Value32', 'intact', 'move'] |
| `prop-1` | A | 证据卡符号与命题陈述有重叠（7 个）：['GCC', 'SSO', 'allocs', 'first_heap_len', 'len'] |
| `prop-1` | A | 证据卡符号与命题陈述有重叠（13 个）：['O0', 'O2', 'capacity_at_len1', 'capacity_at_len8', 'first_ |
| `prop-1` | A | 证据卡符号与命题陈述有重叠（6 个）：['alignas', 'padded_offset_bytes', 'padded_same_line', 'padde |
| `prop-2` | A | 证据卡符号与命题陈述有重叠（8 个）：['EV', 'Linux', 'MEM', 'counters_all_advanced', 'e7'] |
| `prop-1` | A | 证据卡符号与命题陈述有重叠（4 个）：['RAII', 'g_live', 'leak_path', 'safe_path'] |
| `prop-2` | A | 证据卡符号与命题陈述有重叠（3 个）：['RAII', 'ctor', 'dtor'] |
| … | | 其余 20 条见 JSON |

## 3 · oracle 验证优先级（83 张卡）

- 优先级维度=卡类型(证据2/原子1)*2 + 命题数 + 关联MIS数；逃逸率/覆盖率缺口维度待 C 线结合 mutation/poison 基线细化

| 排名 | 卡 | 类型 | 命题数 | 关联MIS | 得分 | 已验 |
|---|---|---|---|---|---|---|
| 1 | `ATOM-UB-GRAY-001` | atom | 2 | 10 | 14 | 否 |
| 2 | `ATOM-MEM-MOVE-002` | atom | 3 | 8 | 13 | 否 |
| 3 | `ATOM-HIST-AUTOPTR-001` | atom | 4 | 4 | 10 | 否 |
| 4 | `ATOM-MEM-ALLOC-001` | atom | 4 | 4 | 10 | 否 |
| 5 | `ATOM-MEM-SHARED-001` | atom | 3 | 5 | 10 | 否 |
| 6 | `ATOM-MEM-WEAK-001` | atom | 3 | 4 | 9 | 否 |
| 7 | `ATOM-MEM-NEW-001` | atom | 3 | 3 | 8 | 否 |
| 8 | `ATOM-MEM-PERF-003` | atom | 3 | 3 | 8 | 否 |
| 9 | `ATOM-MEM-RAII-002` | atom | 4 | 2 | 8 | 否 |
| 10 | `ATOM-MEM-LEAK-001` | atom | 3 | 2 | 7 | 否 |
| 11 | `ATOM-MEM-PERF-002` | atom | 2 | 3 | 7 | 否 |
| 12 | `ATOM-MEM-RAII-001` | atom | 3 | 2 | 7 | 否 |
| 13 | `ATOM-MEM-UNIQUE-001` | atom | 3 | 2 | 7 | 否 |
| 14 | `ATOM-MEM-UNIQUE-002` | atom | 3 | 2 | 7 | 否 |
| 15 | `ATOM-MEM-VALUE-002` | atom | 3 | 2 | 7 | 否 |
| 16 | `ATOM-CONC-RACE-001` | atom | 3 | 1 | 6 | 否 |
| 17 | `ATOM-LANG-INLINE-001` | atom | 3 | 1 | 6 | 否 |
| 18 | `ATOM-MEM-ALIGN-001` | atom | 3 | 1 | 6 | 否 |
| 19 | `ATOM-MEM-ALLOC-002` | atom | 3 | 1 | 6 | 否 |
| 20 | `ATOM-MEM-LEAK-002` | atom | 3 | 1 | 6 | 否 |

## 4 · KC 台账基线（27 原子卡）

- KC=27 原子卡；难度为自动估算建议，非客观难度；前置依赖待 D1 结合 evidence 引用细化

| 原子卡 | obs | inf | 关联MIS数 | 难度 |
|---|---|---|---|---|
| `ATOM-CONC-FENCE-001` | 1 | 1 | 0 | 1 |
| `ATOM-CONC-LOCK-001` | 1 | 1 | 0 | 1 |
| `ATOM-CONC-RACE-001` | 1 | 2 | 1 | 2 |
| `ATOM-HIST-AUTOPTR-001` | 3 | 1 | 4 | 2 |
| `ATOM-LANG-INLINE-001` | 2 | 1 | 1 | 2 |
| `ATOM-MEM-ALIGN-001` | 2 | 1 | 1 | 2 |
| `ATOM-MEM-ALLOC-001` | 3 | 1 | 4 | 2 |
| `ATOM-MEM-ALLOC-002` | 2 | 1 | 1 | 2 |
| `ATOM-MEM-LEAK-001` | 2 | 1 | 2 | 2 |
| `ATOM-MEM-LEAK-002` | 2 | 1 | 1 | 2 |
| `ATOM-MEM-MOVE-002` | 2 | 1 | 8 | 2 |
| `ATOM-MEM-NEW-001` | 2 | 1 | 3 | 2 |
| `ATOM-MEM-PERF-001` | 1 | 1 | 1 | 1 |
| `ATOM-MEM-PERF-002` | 1 | 1 | 3 | 2 |
| `ATOM-MEM-PERF-003` | 1 | 2 | 3 | 2 |
| `ATOM-MEM-PERF-004` | 2 | 1 | 1 | 2 |
| `ATOM-MEM-RAII-001` | 2 | 1 | 2 | 2 |
| `ATOM-MEM-RAII-002` | 3 | 1 | 2 | 2 |
| `ATOM-MEM-RVREF-001` | 2 | 1 | 1 | 2 |
| `ATOM-MEM-SHARED-001` | 2 | 1 | 5 | 2 |
| `ATOM-MEM-SHARED-002` | 2 | 1 | 1 | 2 |
| `ATOM-MEM-UNIQUE-001` | 2 | 1 | 2 | 2 |
| `ATOM-MEM-UNIQUE-002` | 2 | 1 | 2 | 2 |
| `ATOM-MEM-VALUE-001` | 2 | 1 | 1 | 2 |
| `ATOM-MEM-VALUE-002` | 2 | 1 | 2 | 2 |
| `ATOM-MEM-WEAK-001` | 2 | 1 | 4 | 2 |
| `ATOM-UB-GRAY-001` | 1 | 1 | 10 | 2 |

## 5 · 偏差登记（实测 vs 任务书预期）

- 任务书预期 A 20-30 / B 15-20 / C 5-10；实测见 §2（初步，待 B1 细化）。
- oracle Top20 验证优先级已给出；逃逸率/覆盖率缺口维度待 C 线细化。


## 边界三元组 + v26 补充字段（635 1.1 回填）

- `mutation_set_hash`: `d7556d622e92fbf918cf9b49c39d97da0733c88fb686be7e734df7fca294ac57`
- `mutation_count`: 1593
- `generator_version`: `mutation_fuzz@v7`
- `evidence_channel`: `standard_textbook`
- `materiality_flag`: false
