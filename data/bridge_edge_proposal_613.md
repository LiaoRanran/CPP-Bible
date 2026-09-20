# 613 · 桥接边画像与提案（D1）

> 生成：`python tools/bridge_edge_proposal_613.py` ｜ 时间：2026-09-20T23:55:23
> 源：`data/bridge_edge_candidates_611.jsonl`（98 条）。**默认 dry-run**；
> `--apply` 只写 `data/bridge_edges_applied_613.jsonl`，**不动权威边文件**。

## 一、画像总览

| 项 | 值 |
|---|---|
| 候选边总数 | 98 |
| 有共享证据/原子（A 档） | **0** |
| 仅主题匹配（B 档） | **98** |
| 两者皆无（C 档） | 0 |
| 带实据（shared_* 非空）条数 | 0 |
| 主题分布 | {'MEM': 97, 'CONC': 1} |

## 二、分量对热度 Top5（优先修这些对，单条收益最大）

| 分量对 | 候选条数 |
|---|---|
| [7, 10] | 46 |
| [8, 10] | 23 |
| [6, 10] | 23 |
| [7, 8] | 2 |
| [6, 7] | 2 |

## 三、提案清单（前 20 条）

| # | edge_id | source → target | 主题 | 分量对 | 热度 | 档 | 旗标 |
|---|---|---|---|---|---|---|---|
| 1 | `bridge-MIS-MEM-001->MIS-MEM-013` | MIS-MEM-001 → MIS-MEM-013 | MEM | [7, 10] | 46 | B | NO_SHARED_EVIDENCE、SAME_TOPIC_ONLY |
| 2 | `bridge-MIS-MEM-001->MIS-MEM-014` | MIS-MEM-001 → MIS-MEM-014 | MEM | [7, 10] | 46 | B | NO_SHARED_EVIDENCE、SAME_TOPIC_ONLY |
| 3 | `bridge-MIS-MEM-002->MIS-MEM-013` | MIS-MEM-002 → MIS-MEM-013 | MEM | [7, 10] | 46 | B | NO_SHARED_EVIDENCE、SAME_TOPIC_ONLY |
| 4 | `bridge-MIS-MEM-002->MIS-MEM-014` | MIS-MEM-002 → MIS-MEM-014 | MEM | [7, 10] | 46 | B | NO_SHARED_EVIDENCE、SAME_TOPIC_ONLY |
| 5 | `bridge-MIS-MEM-003->MIS-MEM-013` | MIS-MEM-003 → MIS-MEM-013 | MEM | [7, 10] | 46 | B | NO_SHARED_EVIDENCE、SAME_TOPIC_ONLY |
| 6 | `bridge-MIS-MEM-003->MIS-MEM-014` | MIS-MEM-003 → MIS-MEM-014 | MEM | [7, 10] | 46 | B | NO_SHARED_EVIDENCE、SAME_TOPIC_ONLY |
| 7 | `bridge-MIS-MEM-004->MIS-MEM-013` | MIS-MEM-004 → MIS-MEM-013 | MEM | [7, 10] | 46 | B | NO_SHARED_EVIDENCE、SAME_TOPIC_ONLY |
| 8 | `bridge-MIS-MEM-004->MIS-MEM-014` | MIS-MEM-004 → MIS-MEM-014 | MEM | [7, 10] | 46 | B | NO_SHARED_EVIDENCE、SAME_TOPIC_ONLY |
| 9 | `bridge-MIS-MEM-005->MIS-MEM-013` | MIS-MEM-005 → MIS-MEM-013 | MEM | [7, 10] | 46 | B | NO_SHARED_EVIDENCE、SAME_TOPIC_ONLY |
| 10 | `bridge-MIS-MEM-005->MIS-MEM-014` | MIS-MEM-005 → MIS-MEM-014 | MEM | [7, 10] | 46 | B | NO_SHARED_EVIDENCE、SAME_TOPIC_ONLY |
| 11 | `bridge-MIS-MEM-012->MIS-MEM-013` | MIS-MEM-012 → MIS-MEM-013 | MEM | [7, 10] | 46 | B | NO_SHARED_EVIDENCE、SAME_TOPIC_ONLY |
| 12 | `bridge-MIS-MEM-012->MIS-MEM-014` | MIS-MEM-012 → MIS-MEM-014 | MEM | [7, 10] | 46 | B | NO_SHARED_EVIDENCE、SAME_TOPIC_ONLY |
| 13 | `bridge-MIS-MEM-013->MIS-MEM-016` | MIS-MEM-013 → MIS-MEM-016 | MEM | [7, 10] | 46 | B | NO_SHARED_EVIDENCE、SAME_TOPIC_ONLY |
| 14 | `bridge-MIS-MEM-013->MIS-MEM-017` | MIS-MEM-013 → MIS-MEM-017 | MEM | [7, 10] | 46 | B | NO_SHARED_EVIDENCE、SAME_TOPIC_ONLY |
| 15 | `bridge-MIS-MEM-013->MIS-MEM-018` | MIS-MEM-013 → MIS-MEM-018 | MEM | [7, 10] | 46 | B | NO_SHARED_EVIDENCE、SAME_TOPIC_ONLY |
| 16 | `bridge-MIS-MEM-013->MIS-MEM-019` | MIS-MEM-013 → MIS-MEM-019 | MEM | [7, 10] | 46 | B | NO_SHARED_EVIDENCE、SAME_TOPIC_ONLY |
| 17 | `bridge-MIS-MEM-013->MIS-MEM-020` | MIS-MEM-013 → MIS-MEM-020 | MEM | [7, 10] | 46 | B | NO_SHARED_EVIDENCE、SAME_TOPIC_ONLY |
| 18 | `bridge-MIS-MEM-013->MIS-MEM-021` | MIS-MEM-013 → MIS-MEM-021 | MEM | [7, 10] | 46 | B | NO_SHARED_EVIDENCE、SAME_TOPIC_ONLY |
| 19 | `bridge-MIS-MEM-013->MIS-MEM-022` | MIS-MEM-013 → MIS-MEM-022 | MEM | [7, 10] | 46 | B | NO_SHARED_EVIDENCE、SAME_TOPIC_ONLY |
| 20 | `bridge-MIS-MEM-013->MIS-MEM-023` | MIS-MEM-013 → MIS-MEM-023 | MEM | [7, 10] | 46 | B | NO_SHARED_EVIDENCE、SAME_TOPIC_ONLY |

## 四、判定与交人

- 98 条候选**全部为 weak 优先级、且无共享证据/原子**（仅同主题跨分量）
  ⇒ 机器**无法**断言这些桥接边真实成立，全部需**人审**（方向/是否成立由人裁定）。
- 本工具只做画像与排序，**不代替人审**；`--apply` 也不写权威边文件。
