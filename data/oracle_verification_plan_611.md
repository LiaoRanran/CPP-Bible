# 611 D3 · oracle 验证计划（只读 · 不跑验证）

> 83 张卡（56 证据卡 + 27 原子卡）逐张映射到**建议**验证 oracle 并标「已验/未验」。本工具**不跑** gate/replay/poison/mutation，只列计划。

## 一、总览

- 卡 **103** 张：证据卡 66 · 原子卡 37 · 其它 0
- **已填 `verified_by_oracle`：0 张** ⇒ 未验 **103** 张（保守 fail-closed：全体强制重验）

## 二、按主题的建议 oracle 分布

| 建议主 oracle | 卡数 |
|---|---|
| `valgrind_memcheck` | 70 |
| `gcc_compile` | 17 |
| `tsan` | 9 |
| `ubsan` | 5 |
| `gate` | 1 |
| `replay` | 1 |

## 三、逐卡计划（节选 Top 40）

| 卡 | 类型 | 已验 | 建议主 oracle |
|---|---|---|---|
| `ATOM-CONC-FENCE-001` | atom | — | `tsan` |
| `ATOM-CONC-LOCK-001` | atom | — | `tsan` |
| `ATOM-CONC-RACE-001` | atom | — | `tsan` |
| `ATOM-HIST-AUTOPTR-001` | atom | — | `gate` |
| `ATOM-LANG-BITFIELD-001` | atom | — | `gcc_compile` |
| `ATOM-LANG-DECAY-001` | atom | — | `gcc_compile` |
| `ATOM-LANG-FNPTR-001` | atom | — | `gcc_compile` |
| `ATOM-LANG-INLINE-001` | atom | — | `gcc_compile` |
| `ATOM-LANG-INTPROMO-001` | atom | — | `gcc_compile` |
| `ATOM-LANG-MACRO-001` | atom | — | `gcc_compile` |
| `ATOM-LANG-SETJMP-001` | atom | — | `gcc_compile` |
| `ATOM-LANG-VOLATILE-001` | atom | — | `gcc_compile` |
| `ATOM-MEM-ALIGN-001` | atom | — | `valgrind_memcheck` |
| `ATOM-MEM-ALLOC-001` | atom | — | `valgrind_memcheck` |
| `ATOM-MEM-ALLOC-002` | atom | — | `valgrind_memcheck` |
| `ATOM-MEM-LEAK-001` | atom | — | `valgrind_memcheck` |
| `ATOM-MEM-LEAK-002` | atom | — | `valgrind_memcheck` |
| `ATOM-MEM-MALLOC-001` | atom | — | `valgrind_memcheck` |
| `ATOM-MEM-MOVE-002` | atom | — | `valgrind_memcheck` |
| `ATOM-MEM-NEW-001` | atom | — | `valgrind_memcheck` |
| `ATOM-MEM-PERF-001` | atom | — | `valgrind_memcheck` |
| `ATOM-MEM-PERF-002` | atom | — | `valgrind_memcheck` |
| `ATOM-MEM-PERF-003` | atom | — | `valgrind_memcheck` |
| `ATOM-MEM-PERF-004` | atom | — | `valgrind_memcheck` |
| `ATOM-MEM-RAII-001` | atom | — | `valgrind_memcheck` |
| `ATOM-MEM-RAII-002` | atom | — | `valgrind_memcheck` |
| `ATOM-MEM-RVREF-001` | atom | — | `valgrind_memcheck` |
| `ATOM-MEM-SHARED-001` | atom | — | `valgrind_memcheck` |
| `ATOM-MEM-SHARED-002` | atom | — | `valgrind_memcheck` |
| `ATOM-MEM-STRBOUND-001` | atom | — | `valgrind_memcheck` |
| `ATOM-MEM-UNIQUE-001` | atom | — | `valgrind_memcheck` |
| `ATOM-MEM-UNIQUE-002` | atom | — | `valgrind_memcheck` |
| `ATOM-MEM-VALUE-001` | atom | — | `valgrind_memcheck` |
| `ATOM-MEM-VALUE-002` | atom | — | `valgrind_memcheck` |
| `ATOM-MEM-WEAK-001` | atom | — | `valgrind_memcheck` |
| `ATOM-UB-GRAY-001` | atom | — | `ubsan` |
| `ATOM-UB-SIGNEDOVF-001` | atom | — | `ubsan` |
| `EV-CONC-001` | evidence | — | `tsan` |
| `EV-CONC-002` | evidence | — | `tsan` |
| `EV-CONC-003` | evidence | — | `tsan` |
| … | | | 其余 63 张见 jsonl |

## 四、口径与边界

- 复用 `oracle_rotation._load_cards`（与 `metrics_collector.oracle_report()` 同源）；
- 建议 oracle 为**启发式**（按卡主题/类型），非裁决；真实采用由人/编排层决定；
- **绝不跑** gate/replay/poison/mutation（跑了会改基线，属另一批）；
- 诚实：0 张填 `verified_by_oracle` = 缺口未补的代价，不是「版本齐备」。
