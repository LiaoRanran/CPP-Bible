# 612 C2 · oracle 验证优先级（只读 · 建议）

> 五维度加权：类型(证据2/原子1)×2 + 命题数 + 逃逸×3 + 覆盖缺口×2 + 关联MIS。优先级是**建议**，最终验证顺序由人审决定。

## 一、清单

| 排名 | 卡 | 类型 | 命题数 | 逃逸 | 缺口 | 关联MIS | 得分 |
|---|---|---|---|---|---|---|---|
| 1 | `ATOM-UB-GRAY-001` | atom | 2 | 0 | 0 | 10 | 14 |
| 2 | `ATOM-MEM-MOVE-002` | atom | 3 | 0 | 0 | 8 | 13 |
| 3 | `EV-CONC-001` | evidence | 0 | 1 | 0 | 0 | 13 |
| 4 | `ATOM-HIST-AUTOPTR-001` | atom | 4 | 0 | 0 | 4 | 10 |
| 5 | `ATOM-MEM-ALLOC-001` | atom | 4 | 0 | 0 | 4 | 10 |
| 6 | `ATOM-MEM-SHARED-001` | atom | 3 | 0 | 0 | 5 | 10 |
| 7 | `ATOM-MEM-WEAK-001` | atom | 3 | 0 | 0 | 4 | 9 |
| 8 | `ATOM-MEM-NEW-001` | atom | 3 | 0 | 0 | 3 | 8 |
| 9 | `ATOM-MEM-PERF-003` | atom | 3 | 0 | 0 | 3 | 8 |
| 10 | `ATOM-MEM-RAII-002` | atom | 4 | 0 | 0 | 2 | 8 |
| 11 | `ATOM-MEM-LEAK-001` | atom | 3 | 0 | 0 | 2 | 7 |
| 12 | `ATOM-MEM-PERF-002` | atom | 2 | 0 | 0 | 3 | 7 |
| 13 | `ATOM-MEM-RAII-001` | atom | 3 | 0 | 0 | 2 | 7 |
| 14 | `ATOM-MEM-UNIQUE-001` | atom | 3 | 0 | 0 | 2 | 7 |
| 15 | `ATOM-MEM-UNIQUE-002` | atom | 3 | 0 | 0 | 2 | 7 |
| 16 | `ATOM-MEM-VALUE-002` | atom | 3 | 0 | 0 | 2 | 7 |
| 17 | `ATOM-CONC-RACE-001` | atom | 3 | 0 | 0 | 1 | 6 |
| 18 | `ATOM-LANG-INLINE-001` | atom | 3 | 0 | 0 | 1 | 6 |
| 19 | `ATOM-MEM-ALIGN-001` | atom | 3 | 0 | 0 | 1 | 6 |
| 20 | `ATOM-MEM-ALLOC-002` | atom | 3 | 0 | 0 | 1 | 6 |
| 21 | `ATOM-MEM-LEAK-002` | atom | 3 | 0 | 0 | 1 | 6 |
| 22 | `ATOM-MEM-PERF-004` | atom | 3 | 0 | 0 | 1 | 6 |
| 23 | `ATOM-MEM-RVREF-001` | atom | 3 | 0 | 0 | 1 | 6 |
| 24 | `ATOM-MEM-SHARED-002` | atom | 3 | 0 | 0 | 1 | 6 |
| 25 | `ATOM-MEM-VALUE-001` | atom | 3 | 0 | 0 | 1 | 6 |
| 26 | `EV-MEM-009` | evidence | 0 | 0 | 0 | 2 | 6 |
| 27 | `EV-MEM-021` | evidence | 0 | 0 | 0 | 2 | 6 |
| 28 | `EV-MEM-023` | evidence | 0 | 0 | 0 | 2 | 6 |
| 29 | `EV-MEM-029` | evidence | 0 | 0 | 0 | 2 | 6 |
| 30 | `EV-MEM-032` | evidence | 0 | 0 | 0 | 2 | 6 |
| 31 | `ATOM-MEM-PERF-001` | atom | 2 | 0 | 0 | 1 | 5 |
| 32 | `EV-LANG-001` | evidence | 0 | 0 | 0 | 1 | 5 |
| 33 | `EV-LANG-002` | evidence | 0 | 0 | 0 | 1 | 5 |
| 34 | `EV-MEM-014` | evidence | 0 | 0 | 0 | 1 | 5 |
| 35 | `EV-MEM-019` | evidence | 0 | 0 | 0 | 1 | 5 |
| 36 | `EV-MEM-020` | evidence | 0 | 0 | 0 | 1 | 5 |
| 37 | `EV-MEM-022` | evidence | 0 | 0 | 0 | 1 | 5 |
| 38 | `EV-MEM-024` | evidence | 0 | 0 | 0 | 1 | 5 |
| 39 | `EV-MEM-026` | evidence | 0 | 0 | 0 | 1 | 5 |
| 40 | `EV-MEM-027` | evidence | 0 | 0 | 0 | 1 | 5 |
| 41 | `EV-MEM-028` | evidence | 0 | 0 | 0 | 1 | 5 |
| 42 | `EV-MEM-030` | evidence | 0 | 0 | 0 | 1 | 5 |
| 43 | `EV-MEM-031` | evidence | 0 | 0 | 0 | 1 | 5 |
| 44 | `EV-MEM-033` | evidence | 0 | 0 | 0 | 1 | 5 |
| 45 | `EV-MEM-034` | evidence | 0 | 0 | 0 | 1 | 5 |
| 46 | `EV-MEM-035` | evidence | 0 | 0 | 0 | 1 | 5 |
| 47 | `EV-MEM-036` | evidence | 0 | 0 | 0 | 1 | 5 |
| 48 | `EV-MEM-037` | evidence | 0 | 0 | 0 | 1 | 5 |
| 49 | `EV-MEM-038` | evidence | 0 | 0 | 0 | 1 | 5 |
| 50 | `EV-MEM-039` | evidence | 0 | 0 | 0 | 1 | 5 |
| 51 | `ATOM-CONC-FENCE-001` | atom | 2 | 0 | 0 | 0 | 4 |
| 52 | `ATOM-CONC-LOCK-001` | atom | 2 | 0 | 0 | 0 | 4 |
| 53 | `EV-CONC-002` | evidence | 0 | 0 | 0 | 0 | 4 |
| 54 | `EV-CONC-003` | evidence | 0 | 0 | 0 | 0 | 4 |
| 55 | `EV-CONC-004` | evidence | 0 | 0 | 0 | 0 | 4 |
| 56 | `EV-CONC-005` | evidence | 0 | 0 | 0 | 0 | 4 |
| 57 | `EV-CONC-006` | evidence | 0 | 0 | 0 | 0 | 4 |
| 58 | `EV-HIST-001` | evidence | 0 | 0 | 0 | 0 | 4 |
| 59 | `EV-MEM-001` | evidence | 0 | 0 | 0 | 0 | 4 |
| 60 | `EV-MEM-002` | evidence | 0 | 0 | 0 | 0 | 4 |
| 61 | `EV-MEM-003` | evidence | 0 | 0 | 0 | 0 | 4 |
| 62 | `EV-MEM-004` | evidence | 0 | 0 | 0 | 0 | 4 |
| 63 | `EV-MEM-005` | evidence | 0 | 0 | 0 | 0 | 4 |
| 64 | `EV-MEM-006` | evidence | 0 | 0 | 0 | 0 | 4 |
| 65 | `EV-MEM-007` | evidence | 0 | 0 | 0 | 0 | 4 |
| 66 | `EV-MEM-008` | evidence | 0 | 0 | 0 | 0 | 4 |
| 67 | `EV-MEM-010` | evidence | 0 | 0 | 0 | 0 | 4 |
| 68 | `EV-MEM-011` | evidence | 0 | 0 | 0 | 0 | 4 |
| 69 | `EV-MEM-012` | evidence | 0 | 0 | 0 | 0 | 4 |
| 70 | `EV-MEM-013` | evidence | 0 | 0 | 0 | 0 | 4 |
| 71 | `EV-MEM-015` | evidence | 0 | 0 | 0 | 0 | 4 |
| 72 | `EV-MEM-016` | evidence | 0 | 0 | 0 | 0 | 4 |
| 73 | `EV-MEM-017` | evidence | 0 | 0 | 0 | 0 | 4 |
| 74 | `EV-MEM-018` | evidence | 0 | 0 | 0 | 0 | 4 |
| 75 | `EV-MEM-025` | evidence | 0 | 0 | 0 | 0 | 4 |
| 76 | `EV-MEM-040` | evidence | 0 | 0 | 0 | 0 | 4 |
| 77 | `EV-MEM-041` | evidence | 0 | 0 | 0 | 0 | 4 |
| 78 | `EV-MEM-042` | evidence | 0 | 0 | 0 | 0 | 4 |
| 79 | `EV-MEM-043` | evidence | 0 | 0 | 0 | 0 | 4 |
| 80 | `EV-MEM-044` | evidence | 0 | 0 | 0 | 0 | 4 |
| 81 | `EV-MEM-045` | evidence | 0 | 0 | 0 | 0 | 4 |
| 82 | `EV-UB-001` | evidence | 0 | 0 | 0 | 0 | 4 |
| 83 | `EV-UB-002` | evidence | 0 | 0 | 0 | 0 | 4 |

## 二、Top 20 详细理由

1. `ATOM-UB-GRAY-001`（atom）得分 14：命题 2 · 逃逸 0 · 覆盖缺口 0 · 关联 MIS 10
2. `ATOM-MEM-MOVE-002`（atom）得分 13：命题 3 · 逃逸 0 · 覆盖缺口 0 · 关联 MIS 8
3. `EV-CONC-001`（evidence）得分 13：命题 0 · 逃逸 1 · 覆盖缺口 0 · 关联 MIS 0
4. `ATOM-HIST-AUTOPTR-001`（atom）得分 10：命题 4 · 逃逸 0 · 覆盖缺口 0 · 关联 MIS 4
5. `ATOM-MEM-ALLOC-001`（atom）得分 10：命题 4 · 逃逸 0 · 覆盖缺口 0 · 关联 MIS 4
6. `ATOM-MEM-SHARED-001`（atom）得分 10：命题 3 · 逃逸 0 · 覆盖缺口 0 · 关联 MIS 5
7. `ATOM-MEM-WEAK-001`（atom）得分 9：命题 3 · 逃逸 0 · 覆盖缺口 0 · 关联 MIS 4
8. `ATOM-MEM-NEW-001`（atom）得分 8：命题 3 · 逃逸 0 · 覆盖缺口 0 · 关联 MIS 3
9. `ATOM-MEM-PERF-003`（atom）得分 8：命题 3 · 逃逸 0 · 覆盖缺口 0 · 关联 MIS 3
10. `ATOM-MEM-RAII-002`（atom）得分 8：命题 4 · 逃逸 0 · 覆盖缺口 0 · 关联 MIS 2
11. `ATOM-MEM-LEAK-001`（atom）得分 7：命题 3 · 逃逸 0 · 覆盖缺口 0 · 关联 MIS 2
12. `ATOM-MEM-PERF-002`（atom）得分 7：命题 2 · 逃逸 0 · 覆盖缺口 0 · 关联 MIS 3
13. `ATOM-MEM-RAII-001`（atom）得分 7：命题 3 · 逃逸 0 · 覆盖缺口 0 · 关联 MIS 2
14. `ATOM-MEM-UNIQUE-001`（atom）得分 7：命题 3 · 逃逸 0 · 覆盖缺口 0 · 关联 MIS 2
15. `ATOM-MEM-UNIQUE-002`（atom）得分 7：命题 3 · 逃逸 0 · 覆盖缺口 0 · 关联 MIS 2
16. `ATOM-MEM-VALUE-002`（atom）得分 7：命题 3 · 逃逸 0 · 覆盖缺口 0 · 关联 MIS 2
17. `ATOM-CONC-RACE-001`（atom）得分 6：命题 3 · 逃逸 0 · 覆盖缺口 0 · 关联 MIS 1
18. `ATOM-LANG-INLINE-001`（atom）得分 6：命题 3 · 逃逸 0 · 覆盖缺口 0 · 关联 MIS 1
19. `ATOM-MEM-ALIGN-001`（atom）得分 6：命题 3 · 逃逸 0 · 覆盖缺口 0 · 关联 MIS 1
20. `ATOM-MEM-ALLOC-002`（atom）得分 6：命题 3 · 逃逸 0 · 覆盖缺口 0 · 关联 MIS 1

## 三、口径与边界

- **只读**：不修改任何文件；优先级为建议；
- 逃逸维度读 `data/mutation/full_baseline_v7.json` 的 `by_card.escaped`；
- 覆盖缺口读 `tools/poison_surface_map.json`：**今日 uncovered 为空**（11/11 全覆盖）⇒ 该维度全 0；
- 关联 MIS 数同 612 任务0 / 611 C2 口径。
