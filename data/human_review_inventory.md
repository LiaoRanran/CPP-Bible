# 人审库存清单（604 任务 0）

> 生成时间：2026-09-19 · MIS 群组数：42 · 候选边：388
> 歧义度定义：关联卡数 × 每卡命题数的总体标准差（ambiguity = n_cards × pstdev(props_per_card)）
> 歧义度越高，说明该 MIS 关联的卡之间命题数差异越大，越需要人审判断「误解到底驳斥哪条命题」。

## 按歧义度降序排列

| # | MIS ID | 歧义度 | 关联卡数 | 命题总数 | 候选边数 | 反驳文本数 | 关联卡 |
|---|--------|--------|----------|----------|----------|------------|--------|
| 1 | MIS-MEM-028 | 2.45 | 3 | 9 | 18 | 3 | ATOM-MEM-PERF-003, ATOM-MEM-PERF-002, ATOM-MEM-ALLOC-001 |
| 2 | MIS-MEM-023 | 2.0 | 2 | 6 | 12 | 2 | ATOM-MEM-PERF-002, ATOM-MEM-ALLOC-001 |
| 3 | MIS-MEM-019 | 1.0 | 2 | 7 | 14 | 2 | ATOM-MEM-RAII-002, ATOM-MEM-MOVE-002 |
| 4 | MIS-MEM-020 | 1.0 | 2 | 7 | 14 | 2 | ATOM-MEM-RAII-002, ATOM-MEM-UNIQUE-001 |
| 5 | MIS-MEM-021 | 1.0 | 2 | 7 | 14 | 2 | ATOM-MEM-ALLOC-001, ATOM-MEM-NEW-001 |
| 6 | MIS-MEM-022 | 1.0 | 2 | 5 | 10 | 2 | ATOM-MEM-PERF-002, ATOM-MEM-NEW-001 |
| 7 | MIS-MEM-029 | 1.0 | 2 | 5 | 10 | 3 | ATOM-MEM-PERF-003, ATOM-MEM-PERF-001 |
| 8 | MIS-MEM-030 | 1.0 | 2 | 7 | 14 | 3 | ATOM-MEM-ALLOC-002, ATOM-MEM-ALLOC-001 |
| 9 | MIS-CONC-001 | 0 | 1 | 2 | 4 | 2 | ATOM-UB-GRAY-001 |
| 10 | MIS-CONC-003 | 0 | 1 | 3 | 6 | 3 | ATOM-CONC-RACE-001 |
| 11 | MIS-HIST-001 | 0 | 1 | 4 | 8 | 1 | ATOM-HIST-AUTOPTR-001 |
| 12 | MIS-HIST-002 | 0 | 1 | 4 | 8 | 2 | ATOM-HIST-AUTOPTR-001 |
| 13 | MIS-HIST-003 | 0 | 1 | 4 | 8 | 2 | ATOM-HIST-AUTOPTR-001 |
| 14 | MIS-LANG-001 | 0 | 1 | 3 | 6 | 3 | ATOM-LANG-INLINE-001 |
| 15 | MIS-MEM-001 | 0 | 1 | 3 | 6 | 2 | ATOM-MEM-MOVE-002 |
| 16 | MIS-MEM-002 | 0 | 1 | 3 | 6 | 2 | ATOM-MEM-MOVE-002 |
| 17 | MIS-MEM-003 | 0 | 1 | 3 | 6 | 2 | ATOM-MEM-MOVE-002 |
| 18 | MIS-MEM-004 | 0 | 1 | 3 | 6 | 1 | ATOM-MEM-MOVE-002 |
| 19 | MIS-MEM-005 | 0.0 | 2 | 6 | 12 | 4 | ATOM-MEM-MOVE-002, ATOM-MEM-RVREF-001 |
| 20 | MIS-MEM-011 | 0 | 1 | 4 | 8 | 2 | ATOM-HIST-AUTOPTR-001 |
| 21 | MIS-MEM-012 | 0 | 1 | 3 | 6 | 2 | ATOM-MEM-MOVE-002 |
| 22 | MIS-MEM-013 | 0 | 1 | 3 | 6 | 2 | ATOM-MEM-RAII-001 |
| 23 | MIS-MEM-014 | 0 | 1 | 3 | 6 | 2 | ATOM-MEM-RAII-001 |
| 24 | MIS-MEM-015 | 0 | 1 | 3 | 6 | 2 | ATOM-MEM-ALIGN-001 |
| 25 | MIS-MEM-016 | 0.0 | 2 | 6 | 12 | 2 | ATOM-MEM-SHARED-001, ATOM-MEM-WEAK-001 |
| 26 | MIS-MEM-017 | 0.0 | 2 | 6 | 12 | 2 | ATOM-MEM-VALUE-002, ATOM-MEM-MOVE-002 |
| 27 | MIS-MEM-018 | 0.0 | 2 | 6 | 12 | 2 | ATOM-MEM-VALUE-002, ATOM-MEM-VALUE-001 |
| 28 | MIS-MEM-024 | 0.0 | 3 | 9 | 18 | 3 | ATOM-MEM-UNIQUE-002, ATOM-MEM-UNIQUE-001, ATOM-MEM-SHARED-001 |
| 29 | MIS-MEM-025 | 0.0 | 2 | 6 | 12 | 3 | ATOM-MEM-UNIQUE-002, ATOM-MEM-NEW-001 |
| 30 | MIS-MEM-026 | 0.0 | 3 | 9 | 18 | 4 | ATOM-MEM-SHARED-002, ATOM-MEM-SHARED-001, ATOM-MEM-WEAK-001 |
| 31 | MIS-MEM-027 | 0.0 | 3 | 9 | 18 | 3 | ATOM-MEM-LEAK-001, ATOM-MEM-WEAK-001, ATOM-MEM-SHARED-001 |
| 32 | MIS-MEM-031 | 0.0 | 4 | 12 | 24 | 4 | ATOM-MEM-LEAK-002, ATOM-MEM-LEAK-001, ATOM-MEM-WEAK-001 ...(+1) |
| 33 | MIS-MEM-032 | 0.0 | 2 | 6 | 12 | 3 | ATOM-MEM-PERF-004, ATOM-MEM-PERF-003 |
| 34 | MIS-UB-001 | 0 | 1 | 2 | 4 | 2 | ATOM-UB-GRAY-001 |
| 35 | MIS-UB-002 | 0 | 1 | 2 | 4 | 2 | ATOM-UB-GRAY-001 |
| 36 | MIS-UB-003 | 0 | 1 | 2 | 4 | 2 | ATOM-UB-GRAY-001 |
| 37 | MIS-UB-004 | 0 | 1 | 2 | 4 | 2 | ATOM-UB-GRAY-001 |
| 38 | MIS-UB-008 | 0 | 1 | 2 | 4 | 2 | ATOM-UB-GRAY-001 |
| 39 | MIS-UB-012 | 0 | 1 | 2 | 4 | 2 | ATOM-UB-GRAY-001 |
| 40 | MIS-UB-013 | 0 | 1 | 2 | 4 | 2 | ATOM-UB-GRAY-001 |
| 41 | MIS-UB-014 | 0 | 1 | 2 | 4 | 2 | ATOM-UB-GRAY-001 |
| 42 | MIS-UB-015 | 0 | 1 | 2 | 4 | 2 | ATOM-UB-GRAY-001 |

## 统计摘要

- MIS 群组总数：42
- 候选边总数：388
- 歧义度范围：0 - 2.45
- 平均歧义度：0.25
- 关联卡数范围：1 - 4
- 命题总数范围：2 - 12

## 建议审核顺序

按歧义度降序审核（上表 #1 → #42）。歧义度高的 MIS 关联的卡之间命题数差异大，
人审判断「误解驳斥哪条命题」的价值最高；歧义度低的 MIS 关联的卡命题数均匀，判断相对简单。

预计总时间：42 组 × 35s ≈ 24.5 分钟（595 调研实证，比边级 1.89 小时快 4.6 倍）。