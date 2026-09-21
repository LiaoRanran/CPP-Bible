# 614 E1 · oracle 验证优先级（只读 · 建议）

> 612 五维基线 + **614 叠加**（known_tce×5 + kc_related×1）。优先级是**建议**，最终验证顺序由**人审**决定。

## 一、优先级清单

| 排名 | 卡 | 类型 | 命题 | 逃逸 | 缺口 | MIS | known_tce | KC | 614 得分 | 基线得分 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `EV-CONC-001` | evidence | 0 | 1 | 0 | 0 | ⚠ |  | **18** | 13 |
| 2 | `ATOM-UB-GRAY-001` | atom | 2 | 0 | 0 | 10 |  | ● | **15** | 14 |
| 3 | `ATOM-MEM-MOVE-002` | atom | 3 | 0 | 0 | 8 |  | ● | **14** | 13 |
| 4 | `ATOM-HIST-AUTOPTR-001` | atom | 4 | 0 | 0 | 4 |  | ● | **11** | 10 |
| 5 | `ATOM-MEM-ALLOC-001` | atom | 4 | 0 | 0 | 4 |  | ● | **11** | 10 |
| 6 | `ATOM-MEM-SHARED-001` | atom | 3 | 0 | 0 | 5 |  | ● | **11** | 10 |
| 7 | `ATOM-MEM-WEAK-001` | atom | 3 | 0 | 0 | 4 |  | ● | **10** | 9 |
| 8 | `ATOM-MEM-NEW-001` | atom | 3 | 0 | 0 | 3 |  | ● | **9** | 8 |
| 9 | `ATOM-MEM-PERF-003` | atom | 3 | 0 | 0 | 3 |  | ● | **9** | 8 |
| 10 | `ATOM-MEM-RAII-002` | atom | 4 | 0 | 0 | 2 |  | ● | **9** | 8 |
| 11 | `ATOM-MEM-LEAK-001` | atom | 3 | 0 | 0 | 2 |  | ● | **8** | 7 |
| 12 | `ATOM-MEM-PERF-002` | atom | 2 | 0 | 0 | 3 |  | ● | **8** | 7 |
| 13 | `ATOM-MEM-RAII-001` | atom | 3 | 0 | 0 | 2 |  | ● | **8** | 7 |
| 14 | `ATOM-MEM-UNIQUE-001` | atom | 3 | 0 | 0 | 2 |  | ● | **8** | 7 |
| 15 | `ATOM-MEM-UNIQUE-002` | atom | 3 | 0 | 0 | 2 |  | ● | **8** | 7 |
| 16 | `ATOM-MEM-VALUE-002` | atom | 3 | 0 | 0 | 2 |  | ● | **8** | 7 |
| 17 | `ATOM-CONC-RACE-001` | atom | 3 | 0 | 0 | 1 |  | ● | **7** | 6 |
| 18 | `ATOM-LANG-INLINE-001` | atom | 3 | 0 | 0 | 1 |  | ● | **7** | 6 |
| 19 | `ATOM-MEM-ALIGN-001` | atom | 3 | 0 | 0 | 1 |  | ● | **7** | 6 |
| 20 | `ATOM-MEM-ALLOC-002` | atom | 3 | 0 | 0 | 1 |  | ● | **7** | 6 |
| 21 | `ATOM-MEM-LEAK-002` | atom | 3 | 0 | 0 | 1 |  | ● | **7** | 6 |
| 22 | `ATOM-MEM-PERF-004` | atom | 3 | 0 | 0 | 1 |  | ● | **7** | 6 |
| 23 | `ATOM-MEM-RVREF-001` | atom | 3 | 0 | 0 | 1 |  | ● | **7** | 6 |
| 24 | `ATOM-MEM-SHARED-002` | atom | 3 | 0 | 0 | 1 |  | ● | **7** | 6 |
| 25 | `ATOM-MEM-VALUE-001` | atom | 3 | 0 | 0 | 1 |  | ● | **7** | 6 |
| 26 | `ATOM-MEM-PERF-001` | atom | 2 | 0 | 0 | 1 |  | ● | **6** | 5 |
| 27 | `EV-MEM-009` | evidence | 0 | 0 | 0 | 2 |  |  | **6** | 6 |
| 28 | `EV-MEM-021` | evidence | 0 | 0 | 0 | 2 |  |  | **6** | 6 |
| 29 | `EV-MEM-023` | evidence | 0 | 0 | 0 | 2 |  |  | **6** | 6 |
| 30 | `EV-MEM-029` | evidence | 0 | 0 | 0 | 2 |  |  | **6** | 6 |
| 31 | `EV-MEM-032` | evidence | 0 | 0 | 0 | 2 |  |  | **6** | 6 |
| 32 | `ATOM-CONC-FENCE-001` | atom | 2 | 0 | 0 | 0 |  | ● | **5** | 4 |
| 33 | `ATOM-CONC-LOCK-001` | atom | 2 | 0 | 0 | 0 |  | ● | **5** | 4 |
| 34 | `EV-LANG-001` | evidence | 0 | 0 | 0 | 1 |  |  | **5** | 5 |
| 35 | `EV-LANG-002` | evidence | 0 | 0 | 0 | 1 |  |  | **5** | 5 |
| 36 | `EV-MEM-014` | evidence | 0 | 0 | 0 | 1 |  |  | **5** | 5 |
| 37 | `EV-MEM-019` | evidence | 0 | 0 | 0 | 1 |  |  | **5** | 5 |
| 38 | `EV-MEM-020` | evidence | 0 | 0 | 0 | 1 |  |  | **5** | 5 |
| 39 | `EV-MEM-022` | evidence | 0 | 0 | 0 | 1 |  |  | **5** | 5 |
| 40 | `EV-MEM-024` | evidence | 0 | 0 | 0 | 1 |  |  | **5** | 5 |
| 41 | `EV-MEM-026` | evidence | 0 | 0 | 0 | 1 |  |  | **5** | 5 |
| 42 | `EV-MEM-027` | evidence | 0 | 0 | 0 | 1 |  |  | **5** | 5 |
| 43 | `EV-MEM-028` | evidence | 0 | 0 | 0 | 1 |  |  | **5** | 5 |
| 44 | `EV-MEM-030` | evidence | 0 | 0 | 0 | 1 |  |  | **5** | 5 |
| 45 | `EV-MEM-031` | evidence | 0 | 0 | 0 | 1 |  |  | **5** | 5 |
| 46 | `EV-MEM-033` | evidence | 0 | 0 | 0 | 1 |  |  | **5** | 5 |
| 47 | `EV-MEM-034` | evidence | 0 | 0 | 0 | 1 |  |  | **5** | 5 |
| 48 | `EV-MEM-035` | evidence | 0 | 0 | 0 | 1 |  |  | **5** | 5 |
| 49 | `EV-MEM-036` | evidence | 0 | 0 | 0 | 1 |  |  | **5** | 5 |
| 50 | `EV-MEM-037` | evidence | 0 | 0 | 0 | 1 |  |  | **5** | 5 |
| 51 | `EV-MEM-038` | evidence | 0 | 0 | 0 | 1 |  |  | **5** | 5 |
| 52 | `EV-MEM-039` | evidence | 0 | 0 | 0 | 1 |  |  | **5** | 5 |
| 53 | `EV-CONC-002` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 54 | `EV-CONC-003` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 55 | `EV-CONC-004` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 56 | `EV-CONC-005` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 57 | `EV-CONC-006` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 58 | `EV-HIST-001` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 59 | `EV-MEM-001` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 60 | `EV-MEM-002` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 61 | `EV-MEM-003` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 62 | `EV-MEM-004` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 63 | `EV-MEM-005` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 64 | `EV-MEM-006` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 65 | `EV-MEM-007` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 66 | `EV-MEM-008` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 67 | `EV-MEM-010` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 68 | `EV-MEM-011` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 69 | `EV-MEM-012` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 70 | `EV-MEM-013` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 71 | `EV-MEM-015` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 72 | `EV-MEM-016` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 73 | `EV-MEM-017` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 74 | `EV-MEM-018` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 75 | `EV-MEM-025` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 76 | `EV-MEM-040` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 77 | `EV-MEM-041` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 78 | `EV-MEM-042` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 79 | `EV-MEM-043` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 80 | `EV-MEM-044` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 81 | `EV-MEM-045` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 82 | `EV-UB-001` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |
| 83 | `EV-UB-002` | evidence | 0 | 0 | 0 | 0 |  |  | **4** | 4 |

## 二、Top 20 理由

1. `EV-CONC-001` 得分 18（基线 13）：**已知结构性逃逸（TCE）** · 历史逃逸 · 命题 0 · 关联MIS 0
2. `ATOM-UB-GRAY-001` 得分 15（基线 14）：核心 KC · 命题 2 · 关联MIS 10
3. `ATOM-MEM-MOVE-002` 得分 14（基线 13）：核心 KC · 命题 3 · 关联MIS 8
4. `ATOM-HIST-AUTOPTR-001` 得分 11（基线 10）：核心 KC · 命题 4 · 关联MIS 4
5. `ATOM-MEM-ALLOC-001` 得分 11（基线 10）：核心 KC · 命题 4 · 关联MIS 4
6. `ATOM-MEM-SHARED-001` 得分 11（基线 10）：核心 KC · 命题 3 · 关联MIS 5
7. `ATOM-MEM-WEAK-001` 得分 10（基线 9）：核心 KC · 命题 3 · 关联MIS 4
8. `ATOM-MEM-NEW-001` 得分 9（基线 8）：核心 KC · 命题 3 · 关联MIS 3
9. `ATOM-MEM-PERF-003` 得分 9（基线 8）：核心 KC · 命题 3 · 关联MIS 3
10. `ATOM-MEM-RAII-002` 得分 9（基线 8）：核心 KC · 命题 4 · 关联MIS 2
11. `ATOM-MEM-LEAK-001` 得分 8（基线 7）：核心 KC · 命题 3 · 关联MIS 2
12. `ATOM-MEM-PERF-002` 得分 8（基线 7）：核心 KC · 命题 2 · 关联MIS 3
13. `ATOM-MEM-RAII-001` 得分 8（基线 7）：核心 KC · 命题 3 · 关联MIS 2
14. `ATOM-MEM-UNIQUE-001` 得分 8（基线 7）：核心 KC · 命题 3 · 关联MIS 2
15. `ATOM-MEM-UNIQUE-002` 得分 8（基线 7）：核心 KC · 命题 3 · 关联MIS 2
16. `ATOM-MEM-VALUE-002` 得分 8（基线 7）：核心 KC · 命题 3 · 关联MIS 2
17. `ATOM-CONC-RACE-001` 得分 7（基线 6）：核心 KC · 命题 3 · 关联MIS 1
18. `ATOM-LANG-INLINE-001` 得分 7（基线 6）：核心 KC · 命题 3 · 关联MIS 1
19. `ATOM-MEM-ALIGN-001` 得分 7（基线 6）：核心 KC · 命题 3 · 关联MIS 1
20. `ATOM-MEM-ALLOC-002` 得分 7（基线 6）：核心 KC · 命题 3 · 关联MIS 1

## 三、口径与边界

- 612 基线五维见 `tools/oracle_priority.py`；614 叠加 known_tce×5、kc_related×1；
- `known_tce` 读 `data/known_tce.jsonl`（status=known-structural）；
- `kc_related` 读 `kc_inventory`（本仓 KC 图，联动学习者镜像线）；
- **只读**、**建议**；不重跑任何监工门禁；**优先级≠裁决**（裁决权在人）。

