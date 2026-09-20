# 612 B1 · 活性锚自动候选（只读 · 建议，不填卡）

> 扫描 50 条缺 liveness 的 observation 命题的证据卡工件符号；三维度评估（唯一性/可观测性/相关性）。
> 候选只是**建议**（A 类可自动补 / B 类需人审选 / C 类建议改标 inference），本工具不填卡。

## 一、总览

- 缺锚命题 **50** 条；分类：A（高置信）**9** · B（中置信）**26** · C（建议改标 inference）**15**
- 候选总数 96（每条命题 ≤3）

## 二、逐条清单（节选 Top 30）

| 命题 | 卡 | 类 | 候选（符号/置信度） |
|---|---|---|---|
| `prop-1` | `ATOM-CONC-FENCE-001` | B | `_Z10spin_plainv`(medium), `_Z13spin_volatilev`(medium), `_Z15spin_with_fencev`(medium) |
| `prop-1` | `ATOM-CONC-LOCK-001` | A | `single_thread_baseline`(high), `_Z11bench_mutexv`(medium), `_Z12bench_singlev`(medium) |
| `prop-1` | `ATOM-CONC-RACE-001` | B | `_Z10bench_racev`(medium), `_Z10bench_safev`(medium), `_Z12bench_singlev`(medium) |
| `prop-1` | `ATOM-HIST-AUTOPTR-001` | B | `CopyConstructible`(medium), `_ZNSt8auto_ptr`(medium), `auto_ptr`(medium) |
| `prop-2` | `ATOM-HIST-AUTOPTR-001` | A | `is_copy_constructible`(high), `CopyConstructible`(medium), `_ZNSt8auto_ptr`(medium) |
| `prop-4` | `ATOM-HIST-AUTOPTR-001` | B | `_ZNSt8auto_ptr`(medium), `auto_ptr`(medium), `static_assert`(medium) |
| `prop-1` | `ATOM-LANG-INLINE-001` | B | `_ASSERT_ALLOWED_KEYS`(medium), `_Z10tu_a_valuev`(medium), `artifact_assert`(medium) |
| `prop-2` | `ATOM-LANG-INLINE-001` | B | `_ASSERT_ALLOWED_KEYS`(medium), `_Z10tu_a_valuev`(medium), `artifact_assert`(medium) |
| `prop-1` | `ATOM-MEM-ALIGN-001` | C | —（无） |
| `prop-2` | `ATOM-MEM-ALIGN-001` | C | —（无） |
| `prop-1` | `ATOM-MEM-ALLOC-001` | C | —（无） |
| `prop-2` | `ATOM-MEM-ALLOC-001` | C | —（无） |
| `prop-3` | `ATOM-MEM-ALLOC-001` | C | —（无） |
| `prop-1` | `ATOM-MEM-ALLOC-002` | B | `bookkeeping_bytes`(medium), `struct_bytes`(medium), `artifact_sha256`(low) |
| `prop-2` | `ATOM-MEM-ALLOC-002` | B | `bookkeeping_bytes`(medium), `struct_bytes`(medium), `artifact_sha256`(low) |
| `prop-1` | `ATOM-MEM-LEAK-001` | C | —（无） |
| `prop-2` | `ATOM-MEM-LEAK-001` | B | `ASAN_OPTIONS`(medium), `do_sanitizer`(medium), `shared_ptr`(medium) |
| `prop-1` | `ATOM-MEM-LEAK-002` | A | `cycle_allocated`(high), `cycle_destroyed`(high), `cycle_live_objects`(high) |
| `prop-2` | `ATOM-MEM-LEAK-002` | B | `Node`(medium), `cycle_allocated`(medium), `cycle_destroyed`(medium) |
| `prop-1` | `ATOM-MEM-MOVE-002` | B | `BadBuf`(medium) |
| `prop-2` | `ATOM-MEM-MOVE-002` | B | `FixedBuf`(medium), `HeapBuf`(medium), `claim_boundary`(medium) |
| `prop-1` | `ATOM-MEM-NEW-001` | C | —（无） |
| `prop-2` | `ATOM-MEM-NEW-001` | B | `_Znam`(medium), `_Znay`(medium), `artifact_sha256`(low) |
| `prop-1` | `ATOM-MEM-PERF-001` | B | `_Znam`(medium), `_Znay`(medium), `artifact_sha256`(low) |
| `prop-1` | `ATOM-MEM-PERF-002` | C | —（无） |
| `prop-1` | `ATOM-MEM-PERF-003` | A | `capacity_at_len1`(high), `first_heap_len`(high), `sizeof_string`(high) |
| `prop-1` | `ATOM-MEM-PERF-004` | A | `padded_offset_bytes`(high), `padded_same_line`(high), `padded_sizeof`(high) |
| `prop-2` | `ATOM-MEM-PERF-004` | B | `cache_line_size`(medium), `cross_object_same_line`(medium), `hardware_destructive_interference_size`(medium) |
| `prop-1` | `ATOM-MEM-RAII-001` | C | —（无） |
| `prop-2` | `ATOM-MEM-RAII-001` | B | `_ZN3TagD1Ev`(medium), `_ZN3TagD2Ev`(medium), `artifact_sha256`(low) |
| … | | | 其余 20 条见 JSON |

## 三、口径与边界

- **只读**：不填 `liveness`、不改命题文件；符号扫描用正则（不调 LLM，可复算）；
- **通用符号**（main/printf/malloc…）一律标 low，不作高置信候选；
- **C 类**：无单一工件符号可证伪 ⇒ 建议人审改标 inference（本工具不实际改）；
- A/B/C 为自动建议，最终由人审确认（见 B2）。
