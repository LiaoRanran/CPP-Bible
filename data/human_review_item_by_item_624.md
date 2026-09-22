# 624 E2 · 人审逐条复核清单（30 → >100，**只生成不执行**）

> 新生成 **80** 条；连同 615 的 30 条，**记录条数**合计 **110** 条。
> 歧义度分布：{'high': 34, 'medium': 46}；推荐判决分布：{'approve': 80}。

> ⚠ **唯一性修正（2026-09-22，外部大模型发现 + 626 A1 核实）**：
> **"110" 只是记录条数相加，不是唯一复核对象数量。**
> 实测（`tools/stats_recalc_verifier_626.py` 重算）：
> 615 清单 **30** 个唯一 edge ID；624 清单 **80** 个唯一 edge ID；两者 **overlap = 17**；
> ⇒ 实际 **union = 93 个唯一 edge ID**。审计口径一律以 **93** 为准，禁止用 110 重复计数。

## 去重统计

| 项 | 数量 |
|---|---|
| 615 清单唯一 edge ID | 30 |
| 624 清单唯一 edge ID | 80 |
| 两者重复（overlap） | 17 |
| **唯一复核对象（union）** | **93** |
| 记录条数（30+80，含重复） | 110 |

> 17 条 overlap 的项在 626 B3 唯一审查账本中只生成**一个** ReviewItem，`source_batch` 标注 `615+624`。

> **不代签**：本清单**只生成、不执行判决**；执行需人授权。

## 逐条复核清单

| # | edge_id | 原子 | 动作 | 歧义度 | 推荐判决 | 理由 |
|---|---|---|---|---|---|---|
| 1 | `ae-MIS-LANG-001->ATOM-LANG-INLINE-001::prop-1` | ATOM-LANG-INLINE-001 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 2 | `ae-MIS-LANG-001->ATOM-LANG-INLINE-001::prop-2` | ATOM-LANG-INLINE-001 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 3 | `ae-MIS-LANG-001->ATOM-LANG-INLINE-001::prop-3` | ATOM-LANG-INLINE-001 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 4 | `ae-MIS-MEM-001->ATOM-MEM-MOVE-002::prop-1` | ATOM-MEM-MOVE-002 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 5 | `ae-MIS-MEM-001->ATOM-MEM-MOVE-002::prop-2` | ATOM-MEM-MOVE-002 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 6 | `ae-MIS-MEM-001->ATOM-MEM-MOVE-002::prop-3` | ATOM-MEM-MOVE-002 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 7 | `ae-MIS-MEM-003->ATOM-MEM-MOVE-002::prop-1` | ATOM-MEM-MOVE-002 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 8 | `ae-MIS-MEM-003->ATOM-MEM-MOVE-002::prop-2` | ATOM-MEM-MOVE-002 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 9 | `ae-MIS-MEM-003->ATOM-MEM-MOVE-002::prop-3` | ATOM-MEM-MOVE-002 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 10 | `ae-MIS-UB-001->ATOM-UB-GRAY-001::prop-1` | ATOM-UB-GRAY-001 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 11 | `ae-MIS-UB-001->ATOM-UB-GRAY-001::prop-2` | ATOM-UB-GRAY-001 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 12 | `ae-MIS-UB-004->ATOM-UB-GRAY-001::prop-1` | ATOM-UB-GRAY-001 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 13 | `ae-MIS-UB-004->ATOM-UB-GRAY-001::prop-2` | ATOM-UB-GRAY-001 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 14 | `ae-MIS-UB-008->ATOM-UB-GRAY-001::prop-1` | ATOM-UB-GRAY-001 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 15 | `ae-MIS-UB-008->ATOM-UB-GRAY-001::prop-2` | ATOM-UB-GRAY-001 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 16 | `ae-MIS-UB-014->ATOM-UB-GRAY-001::prop-1` | ATOM-UB-GRAY-001 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 17 | `ae-MIS-UB-014->ATOM-UB-GRAY-001::prop-2` | ATOM-UB-GRAY-001 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 18 | `ae-ATOM-LANG-INLINE-001::prop-1->MIS-LANG-001` | MIS-LANG-001 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 19 | `ae-ATOM-LANG-INLINE-001::prop-2->MIS-LANG-001` | MIS-LANG-001 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 20 | `ae-ATOM-LANG-INLINE-001::prop-3->MIS-LANG-001` | MIS-LANG-001 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 21 | `ae-ATOM-MEM-MOVE-002::prop-1->MIS-MEM-001` | MIS-MEM-001 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 22 | `ae-ATOM-MEM-MOVE-002::prop-2->MIS-MEM-001` | MIS-MEM-001 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 23 | `ae-ATOM-MEM-MOVE-002::prop-3->MIS-MEM-001` | MIS-MEM-001 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 24 | `ae-ATOM-MEM-MOVE-002::prop-1->MIS-MEM-003` | MIS-MEM-003 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 25 | `ae-ATOM-MEM-MOVE-002::prop-2->MIS-MEM-003` | MIS-MEM-003 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 26 | `ae-ATOM-MEM-MOVE-002::prop-3->MIS-MEM-003` | MIS-MEM-003 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 27 | `ae-ATOM-UB-GRAY-001::prop-1->MIS-UB-001` | MIS-UB-001 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 28 | `ae-ATOM-UB-GRAY-001::prop-2->MIS-UB-001` | MIS-UB-001 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 29 | `ae-ATOM-UB-GRAY-001::prop-1->MIS-UB-004` | MIS-UB-004 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 30 | `ae-ATOM-UB-GRAY-001::prop-2->MIS-UB-004` | MIS-UB-004 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 31 | `ae-ATOM-UB-GRAY-001::prop-1->MIS-UB-008` | MIS-UB-008 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 32 | `ae-ATOM-UB-GRAY-001::prop-2->MIS-UB-008` | MIS-UB-008 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 33 | `ae-ATOM-UB-GRAY-001::prop-1->MIS-UB-014` | MIS-UB-014 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 34 | `ae-ATOM-UB-GRAY-001::prop-2->MIS-UB-014` | MIS-UB-014 | modify | high | approve | W2 视 modify 为 UNRESOLVED（机器不确定） |
| 35 | `ae-MIS-HIST-001->ATOM-HIST-AUTOPTR-001::prop-1` | ATOM-HIST-AUTOPTR-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 36 | `ae-MIS-HIST-001->ATOM-HIST-AUTOPTR-001::prop-2` | ATOM-HIST-AUTOPTR-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 37 | `ae-MIS-HIST-001->ATOM-HIST-AUTOPTR-001::prop-3` | ATOM-HIST-AUTOPTR-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 38 | `ae-MIS-HIST-001->ATOM-HIST-AUTOPTR-001::prop-4` | ATOM-HIST-AUTOPTR-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 39 | `ae-MIS-HIST-002->ATOM-HIST-AUTOPTR-001::prop-1` | ATOM-HIST-AUTOPTR-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 40 | `ae-MIS-HIST-002->ATOM-HIST-AUTOPTR-001::prop-2` | ATOM-HIST-AUTOPTR-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 41 | `ae-MIS-HIST-002->ATOM-HIST-AUTOPTR-001::prop-3` | ATOM-HIST-AUTOPTR-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 42 | `ae-MIS-HIST-002->ATOM-HIST-AUTOPTR-001::prop-4` | ATOM-HIST-AUTOPTR-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 43 | `ae-MIS-HIST-003->ATOM-HIST-AUTOPTR-001::prop-1` | ATOM-HIST-AUTOPTR-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 44 | `ae-MIS-HIST-003->ATOM-HIST-AUTOPTR-001::prop-2` | ATOM-HIST-AUTOPTR-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 45 | `ae-MIS-HIST-003->ATOM-HIST-AUTOPTR-001::prop-3` | ATOM-HIST-AUTOPTR-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 46 | `ae-MIS-HIST-003->ATOM-HIST-AUTOPTR-001::prop-4` | ATOM-HIST-AUTOPTR-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 47 | `ae-MIS-MEM-011->ATOM-HIST-AUTOPTR-001::prop-1` | ATOM-HIST-AUTOPTR-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 48 | `ae-MIS-MEM-011->ATOM-HIST-AUTOPTR-001::prop-2` | ATOM-HIST-AUTOPTR-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 49 | `ae-MIS-MEM-011->ATOM-HIST-AUTOPTR-001::prop-3` | ATOM-HIST-AUTOPTR-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 50 | `ae-MIS-MEM-011->ATOM-HIST-AUTOPTR-001::prop-4` | ATOM-HIST-AUTOPTR-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 51 | `ae-MIS-MEM-021->ATOM-MEM-ALLOC-001::prop-1` | ATOM-MEM-ALLOC-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 52 | `ae-MIS-MEM-021->ATOM-MEM-ALLOC-001::prop-2` | ATOM-MEM-ALLOC-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 53 | `ae-MIS-MEM-021->ATOM-MEM-ALLOC-001::prop-3` | ATOM-MEM-ALLOC-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 54 | `ae-MIS-MEM-021->ATOM-MEM-ALLOC-001::prop-4` | ATOM-MEM-ALLOC-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 55 | `ae-MIS-MEM-023->ATOM-MEM-ALLOC-001::prop-1` | ATOM-MEM-ALLOC-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 56 | `ae-MIS-MEM-023->ATOM-MEM-ALLOC-001::prop-2` | ATOM-MEM-ALLOC-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 57 | `ae-MIS-MEM-023->ATOM-MEM-ALLOC-001::prop-3` | ATOM-MEM-ALLOC-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 58 | `ae-MIS-MEM-023->ATOM-MEM-ALLOC-001::prop-4` | ATOM-MEM-ALLOC-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 59 | `ae-MIS-MEM-028->ATOM-MEM-ALLOC-001::prop-1` | ATOM-MEM-ALLOC-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 60 | `ae-MIS-MEM-028->ATOM-MEM-ALLOC-001::prop-2` | ATOM-MEM-ALLOC-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 61 | `ae-MIS-MEM-028->ATOM-MEM-ALLOC-001::prop-3` | ATOM-MEM-ALLOC-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 62 | `ae-MIS-MEM-028->ATOM-MEM-ALLOC-001::prop-4` | ATOM-MEM-ALLOC-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 63 | `ae-MIS-MEM-030->ATOM-MEM-ALLOC-001::prop-1` | ATOM-MEM-ALLOC-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 64 | `ae-MIS-MEM-030->ATOM-MEM-ALLOC-001::prop-2` | ATOM-MEM-ALLOC-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 65 | `ae-MIS-MEM-030->ATOM-MEM-ALLOC-001::prop-3` | ATOM-MEM-ALLOC-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 66 | `ae-MIS-MEM-030->ATOM-MEM-ALLOC-001::prop-4` | ATOM-MEM-ALLOC-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 67 | `ae-MIS-MEM-027->ATOM-MEM-LEAK-001::prop-1` | ATOM-MEM-LEAK-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 68 | `ae-MIS-MEM-027->ATOM-MEM-LEAK-001::prop-2` | ATOM-MEM-LEAK-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 69 | `ae-MIS-MEM-027->ATOM-MEM-LEAK-001::prop-3` | ATOM-MEM-LEAK-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 70 | `ae-MIS-MEM-031->ATOM-MEM-LEAK-001::prop-1` | ATOM-MEM-LEAK-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 71 | `ae-MIS-MEM-031->ATOM-MEM-LEAK-001::prop-2` | ATOM-MEM-LEAK-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 72 | `ae-MIS-MEM-031->ATOM-MEM-LEAK-001::prop-3` | ATOM-MEM-LEAK-001 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 73 | `ae-MIS-MEM-031->ATOM-MEM-LEAK-002::prop-1` | ATOM-MEM-LEAK-002 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 74 | `ae-MIS-MEM-031->ATOM-MEM-LEAK-002::prop-2` | ATOM-MEM-LEAK-002 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 75 | `ae-MIS-MEM-031->ATOM-MEM-LEAK-002::prop-3` | ATOM-MEM-LEAK-002 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 76 | `ae-MIS-MEM-022->ATOM-MEM-PERF-002::prop-1` | ATOM-MEM-PERF-002 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 77 | `ae-MIS-MEM-022->ATOM-MEM-PERF-002::prop-2` | ATOM-MEM-PERF-002 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 78 | `ae-MIS-MEM-023->ATOM-MEM-PERF-002::prop-1` | ATOM-MEM-PERF-002 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 79 | `ae-MIS-MEM-023->ATOM-MEM-PERF-002::prop-2` | ATOM-MEM-PERF-002 | approve | medium | approve | 高复杂度原子（cx≥75） |
| 80 | `ae-MIS-MEM-028->ATOM-MEM-PERF-002::prop-1` | ATOM-MEM-PERF-002 | approve | medium | approve | 高复杂度原子（cx≥75） |

## 局限性声明

1. 清单为**机器排序建议**，歧义度与推荐判决均非人审结论。
2. 622 的 30 条以 `source=authority_log` 标识（已执行）；本清单覆盖其余未人审边。
3. 执行（写 Authority 日志）**需人授权**，本批不做。

