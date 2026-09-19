# 608 A0 · 人审 backlog 现状盘点（只读）

> 数据源：`data/attack_edges_candidates.jsonl`（596 生成，388 条候选攻击边）、`data/grounded_labels_w2.json`（596/594 W2 求解结果）。本文件为**只读盘点**，不修改任何数据/卡/命题；A1 才会建聚合队列工具。

## 1 · 总览

- 候选攻击边总数：**388 条**
- 误群组（MIS 去重）：**42 组**（= W2 判 OUT 的 42 个误解节点）
- 目标命题去重：**75 个**（79 命题中有 **4 个**从未出现在任何攻击边里：ATOM-CONC-FENCE-001::prop-1、ATOM-CONC-FENCE-001::prop-2、ATOM-CONC-LOCK-001::prop-1、ATOM-CONC-LOCK-001::prop-2）
- 可信度分布：**全部 388 条为 `low`**（生成器口径：MIS 卡面 0 张有 `verified_by`/`machine_verified` ⇒ 全 low；见 596 报告）
- W2 判决（全仓）：IN=79 / OUT=42 / UNDEC=0（79 命题全 IN、42 误解全 OUT）

## 2 · 按 MIS 分组（42 组，按边数降序）

> 建议 verdict 来源 = 该 MIS 节点在 W2 的标签（OUT ⇒ 误解出局，建议 reject）。42 组**全部 OUT**，故群组级建议 verdict 统一为 reject。

| MIS 组 | 边数 | 涉及卡 | 涉及命题 | W2 标签 |
|--------|-----:|-------:|---------:|--------|
| `MIS-MEM-031` | 24 | 4 | 12 | OUT |
| `MIS-MEM-024` | 18 | 3 | 9 | OUT |
| `MIS-MEM-026` | 18 | 3 | 9 | OUT |
| `MIS-MEM-027` | 18 | 3 | 9 | OUT |
| `MIS-MEM-028` | 18 | 3 | 9 | OUT |
| `MIS-MEM-019` | 14 | 2 | 7 | OUT |
| `MIS-MEM-020` | 14 | 2 | 7 | OUT |
| `MIS-MEM-021` | 14 | 2 | 7 | OUT |
| `MIS-MEM-030` | 14 | 2 | 7 | OUT |
| `MIS-MEM-005` | 12 | 2 | 6 | OUT |
| `MIS-MEM-016` | 12 | 2 | 6 | OUT |
| `MIS-MEM-017` | 12 | 2 | 6 | OUT |
| `MIS-MEM-018` | 12 | 2 | 6 | OUT |
| `MIS-MEM-023` | 12 | 2 | 6 | OUT |
| `MIS-MEM-025` | 12 | 2 | 6 | OUT |
| `MIS-MEM-032` | 12 | 2 | 6 | OUT |
| `MIS-MEM-022` | 10 | 2 | 5 | OUT |
| `MIS-MEM-029` | 10 | 2 | 5 | OUT |
| `MIS-HIST-001` | 8 | 1 | 4 | OUT |
| `MIS-HIST-002` | 8 | 1 | 4 | OUT |
| `MIS-HIST-003` | 8 | 1 | 4 | OUT |
| `MIS-MEM-011` | 8 | 1 | 4 | OUT |
| `MIS-CONC-003` | 6 | 1 | 3 | OUT |
| `MIS-LANG-001` | 6 | 1 | 3 | OUT |
| `MIS-MEM-001` | 6 | 1 | 3 | OUT |
| `MIS-MEM-002` | 6 | 1 | 3 | OUT |
| `MIS-MEM-003` | 6 | 1 | 3 | OUT |
| `MIS-MEM-004` | 6 | 1 | 3 | OUT |
| `MIS-MEM-012` | 6 | 1 | 3 | OUT |
| `MIS-MEM-013` | 6 | 1 | 3 | OUT |
| `MIS-MEM-014` | 6 | 1 | 3 | OUT |
| `MIS-MEM-015` | 6 | 1 | 3 | OUT |
| `MIS-CONC-001` | 4 | 1 | 2 | OUT |
| `MIS-UB-001` | 4 | 1 | 2 | OUT |
| `MIS-UB-002` | 4 | 1 | 2 | OUT |
| `MIS-UB-003` | 4 | 1 | 2 | OUT |
| `MIS-UB-004` | 4 | 1 | 2 | OUT |
| `MIS-UB-008` | 4 | 1 | 2 | OUT |
| `MIS-UB-012` | 4 | 1 | 2 | OUT |
| `MIS-UB-013` | 4 | 1 | 2 | OUT |
| `MIS-UB-014` | 4 | 1 | 2 | OUT |
| `MIS-UB-015` | 4 | 1 | 2 | OUT |

- 边数区间：**4 ~ 24**；最大组 `MIS-MEM-031`（24 边），最小 4 边。

## 3 · 按目标命题分组（75 个，按边数降序）

| 命题 id | 卡 | 边数 | 涉及 MIS 数 | W2 标签 |
|---------|----|-----:|-----------:|--------|
| `ATOM-UB-GRAY-001::prop-1` | `ATOM-UB-GRAY-001` | 20 | 10 | IN |
| `ATOM-UB-GRAY-001::prop-2` | `ATOM-UB-GRAY-001` | 20 | 10 | IN |
| `ATOM-MEM-MOVE-002::prop-1` | `ATOM-MEM-MOVE-002` | 16 | 8 | IN |
| `ATOM-MEM-MOVE-002::prop-2` | `ATOM-MEM-MOVE-002` | 16 | 8 | IN |
| `ATOM-MEM-MOVE-002::prop-3` | `ATOM-MEM-MOVE-002` | 16 | 8 | IN |
| `ATOM-MEM-SHARED-001::prop-1` | `ATOM-MEM-SHARED-001` | 10 | 5 | IN |
| `ATOM-MEM-SHARED-001::prop-2` | `ATOM-MEM-SHARED-001` | 10 | 5 | IN |
| `ATOM-MEM-SHARED-001::prop-3` | `ATOM-MEM-SHARED-001` | 10 | 5 | IN |
| `ATOM-HIST-AUTOPTR-001::prop-1` | `ATOM-HIST-AUTOPTR-001` | 8 | 4 | IN |
| `ATOM-HIST-AUTOPTR-001::prop-2` | `ATOM-HIST-AUTOPTR-001` | 8 | 4 | IN |
| `ATOM-HIST-AUTOPTR-001::prop-3` | `ATOM-HIST-AUTOPTR-001` | 8 | 4 | IN |
| `ATOM-HIST-AUTOPTR-001::prop-4` | `ATOM-HIST-AUTOPTR-001` | 8 | 4 | IN |
| `ATOM-MEM-ALLOC-001::prop-1` | `ATOM-MEM-ALLOC-001` | 8 | 4 | IN |
| `ATOM-MEM-ALLOC-001::prop-2` | `ATOM-MEM-ALLOC-001` | 8 | 4 | IN |
| `ATOM-MEM-ALLOC-001::prop-3` | `ATOM-MEM-ALLOC-001` | 8 | 4 | IN |
| `ATOM-MEM-ALLOC-001::prop-4` | `ATOM-MEM-ALLOC-001` | 8 | 4 | IN |
| `ATOM-MEM-WEAK-001::prop-1` | `ATOM-MEM-WEAK-001` | 8 | 4 | IN |
| `ATOM-MEM-WEAK-001::prop-2` | `ATOM-MEM-WEAK-001` | 8 | 4 | IN |
| `ATOM-MEM-WEAK-001::prop-3` | `ATOM-MEM-WEAK-001` | 8 | 4 | IN |
| `ATOM-MEM-NEW-001::prop-1` | `ATOM-MEM-NEW-001` | 6 | 3 | IN |
| `ATOM-MEM-NEW-001::prop-2` | `ATOM-MEM-NEW-001` | 6 | 3 | IN |
| `ATOM-MEM-NEW-001::prop-3` | `ATOM-MEM-NEW-001` | 6 | 3 | IN |
| `ATOM-MEM-PERF-002::prop-1` | `ATOM-MEM-PERF-002` | 6 | 3 | IN |
| `ATOM-MEM-PERF-002::prop-2` | `ATOM-MEM-PERF-002` | 6 | 3 | IN |
| `ATOM-MEM-PERF-003::prop-1` | `ATOM-MEM-PERF-003` | 6 | 3 | IN |
| `ATOM-MEM-PERF-003::prop-2` | `ATOM-MEM-PERF-003` | 6 | 3 | IN |
| `ATOM-MEM-PERF-003::prop-3` | `ATOM-MEM-PERF-003` | 6 | 3 | IN |
| `ATOM-MEM-LEAK-001::prop-1` | `ATOM-MEM-LEAK-001` | 4 | 2 | IN |
| `ATOM-MEM-LEAK-001::prop-2` | `ATOM-MEM-LEAK-001` | 4 | 2 | IN |
| `ATOM-MEM-LEAK-001::prop-3` | `ATOM-MEM-LEAK-001` | 4 | 2 | IN |
| `ATOM-MEM-RAII-001::prop-1` | `ATOM-MEM-RAII-001` | 4 | 2 | IN |
| `ATOM-MEM-RAII-001::prop-2` | `ATOM-MEM-RAII-001` | 4 | 2 | IN |
| `ATOM-MEM-RAII-001::prop-3` | `ATOM-MEM-RAII-001` | 4 | 2 | IN |
| `ATOM-MEM-RAII-002::prop-1` | `ATOM-MEM-RAII-002` | 4 | 2 | IN |
| `ATOM-MEM-RAII-002::prop-2` | `ATOM-MEM-RAII-002` | 4 | 2 | IN |
| `ATOM-MEM-RAII-002::prop-3` | `ATOM-MEM-RAII-002` | 4 | 2 | IN |
| `ATOM-MEM-RAII-002::prop-4` | `ATOM-MEM-RAII-002` | 4 | 2 | IN |
| `ATOM-MEM-UNIQUE-001::prop-1` | `ATOM-MEM-UNIQUE-001` | 4 | 2 | IN |
| `ATOM-MEM-UNIQUE-001::prop-2` | `ATOM-MEM-UNIQUE-001` | 4 | 2 | IN |
| `ATOM-MEM-UNIQUE-001::prop-3` | `ATOM-MEM-UNIQUE-001` | 4 | 2 | IN |
| `ATOM-MEM-UNIQUE-002::prop-1` | `ATOM-MEM-UNIQUE-002` | 4 | 2 | IN |
| `ATOM-MEM-UNIQUE-002::prop-2` | `ATOM-MEM-UNIQUE-002` | 4 | 2 | IN |
| `ATOM-MEM-UNIQUE-002::prop-3` | `ATOM-MEM-UNIQUE-002` | 4 | 2 | IN |
| `ATOM-MEM-VALUE-002::prop-1` | `ATOM-MEM-VALUE-002` | 4 | 2 | IN |
| `ATOM-MEM-VALUE-002::prop-2` | `ATOM-MEM-VALUE-002` | 4 | 2 | IN |
| `ATOM-MEM-VALUE-002::prop-3` | `ATOM-MEM-VALUE-002` | 4 | 2 | IN |
| `ATOM-CONC-RACE-001::prop-1` | `ATOM-CONC-RACE-001` | 2 | 1 | IN |
| `ATOM-CONC-RACE-001::prop-2` | `ATOM-CONC-RACE-001` | 2 | 1 | IN |
| `ATOM-CONC-RACE-001::prop-3` | `ATOM-CONC-RACE-001` | 2 | 1 | IN |
| `ATOM-LANG-INLINE-001::prop-1` | `ATOM-LANG-INLINE-001` | 2 | 1 | IN |
| `ATOM-LANG-INLINE-001::prop-2` | `ATOM-LANG-INLINE-001` | 2 | 1 | IN |
| `ATOM-LANG-INLINE-001::prop-3` | `ATOM-LANG-INLINE-001` | 2 | 1 | IN |
| `ATOM-MEM-ALIGN-001::prop-1` | `ATOM-MEM-ALIGN-001` | 2 | 1 | IN |
| `ATOM-MEM-ALIGN-001::prop-2` | `ATOM-MEM-ALIGN-001` | 2 | 1 | IN |
| `ATOM-MEM-ALIGN-001::prop-3` | `ATOM-MEM-ALIGN-001` | 2 | 1 | IN |
| `ATOM-MEM-ALLOC-002::prop-1` | `ATOM-MEM-ALLOC-002` | 2 | 1 | IN |
| `ATOM-MEM-ALLOC-002::prop-2` | `ATOM-MEM-ALLOC-002` | 2 | 1 | IN |
| `ATOM-MEM-ALLOC-002::prop-3` | `ATOM-MEM-ALLOC-002` | 2 | 1 | IN |
| `ATOM-MEM-LEAK-002::prop-1` | `ATOM-MEM-LEAK-002` | 2 | 1 | IN |
| `ATOM-MEM-LEAK-002::prop-2` | `ATOM-MEM-LEAK-002` | 2 | 1 | IN |
| `ATOM-MEM-LEAK-002::prop-3` | `ATOM-MEM-LEAK-002` | 2 | 1 | IN |
| `ATOM-MEM-PERF-001::prop-1` | `ATOM-MEM-PERF-001` | 2 | 1 | IN |
| `ATOM-MEM-PERF-001::prop-2` | `ATOM-MEM-PERF-001` | 2 | 1 | IN |
| `ATOM-MEM-PERF-004::prop-1` | `ATOM-MEM-PERF-004` | 2 | 1 | IN |
| `ATOM-MEM-PERF-004::prop-2` | `ATOM-MEM-PERF-004` | 2 | 1 | IN |
| `ATOM-MEM-PERF-004::prop-3` | `ATOM-MEM-PERF-004` | 2 | 1 | IN |
| `ATOM-MEM-RVREF-001::prop-1` | `ATOM-MEM-RVREF-001` | 2 | 1 | IN |
| `ATOM-MEM-RVREF-001::prop-2` | `ATOM-MEM-RVREF-001` | 2 | 1 | IN |
| `ATOM-MEM-RVREF-001::prop-3` | `ATOM-MEM-RVREF-001` | 2 | 1 | IN |
| `ATOM-MEM-SHARED-002::prop-1` | `ATOM-MEM-SHARED-002` | 2 | 1 | IN |
| `ATOM-MEM-SHARED-002::prop-2` | `ATOM-MEM-SHARED-002` | 2 | 1 | IN |
| `ATOM-MEM-SHARED-002::prop-3` | `ATOM-MEM-SHARED-002` | 2 | 1 | IN |
| `ATOM-MEM-VALUE-001::prop-1` | `ATOM-MEM-VALUE-001` | 2 | 1 | IN |
| `ATOM-MEM-VALUE-001::prop-2` | `ATOM-MEM-VALUE-001` | 2 | 1 | IN |
| `ATOM-MEM-VALUE-001::prop-3` | `ATOM-MEM-VALUE-001` | 2 | 1 | IN |

## 4 · 按 confidence 分组

| confidence | 边数 |
|------------|-----:|
| `low` | 388 |

## 5 · 595 调研结论核验（群组级 vs 边级人审耗时）

- 边级：388 边 × 17.5s/边 ≈ **113.2 min（≈ 1.89 h）**
- 群组级（MIS 聚合）：42 组 × 35s/组 ≈ **24.5 min**
- 降速比：113.2 / 24.5 ≈ **4.62×**（与 595 报告的「4.6 倍」一致）
- 注：17.5s/35s 为 595 调研给出的**单条边/单个群组**人审时间假设，本盘点只做乘法核验，不重新做计时实验；若监工要更精确，需重做 595 计时。

## 6 · 关键发现（交人项前置）

1. **42 组建议 verdict 全部 reject**：W2 把 42 个误解全判 OUT（命题全 IN），意味着当前攻击图在 W2 下已经「一边倒」——群组级人审若照 W2 建议全 reject，则人审价值主要在**复核 W2 是否正确**（而非发现新结论）。这是论证层 6.0/10 的根因之一。
2. **全部 low 可信度**：候选边的可信度无分级，人审时无法按「可信度低→优先人工看」排序，A1 的歧义度排序需另找维度（命题分散度/可信度方差）。
3. **4 个命题无任何攻击边**：这些命题的论证层状态完全未经攻击图检验，是论证层覆盖盲区（含 ATOM-CONC-FENCE-001::prop-1、ATOM-CONC-FENCE-001::prop-2、ATOM-CONC-LOCK-001::prop-1、ATOM-CONC-LOCK-001::prop-2 等）。
4. **数据一致性自检**：388 边 = W2 的 `edges=388`、generator `--check` 口径一致；42 MIS 组 = W2 `OUT=42`，无孤儿节点。

