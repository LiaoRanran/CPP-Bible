# 622 C2 · 原子卡 verdict 提取（27 张）

> 提取总数：**37**（**未修改任何原始卡**）

## 一、提取结果分布

| verdict | 张数 |
| SUPPORTED | 37 |

## 二、置信度分布

| 置信度 | 张数 |
| high | 26 |
| medium | 10 |
| low | 1 |

## 三、提取依据分布

| basis | 张数 |
| `status=verified` | 23 |
| `draft+observation+evidence` | 10 |
| `status=red-team-verified` | 3 |
| `evidence_only` | 1 |

## 四、与 621 C2 的对比

| 项 | 621 C2（分类器 v1） | 622 C2（提取后） |
|---|---|---|
| 原子卡 UNDECIDED | **27 / 27** | **0 / 37** |
| 原子卡 SUPPORTED | 0 | **37** |
| 原子卡 REFUTED | 0 | **0** |

## 五、逐卡明细

| 卡 ID | verdict | 置信度 | basis | status | 证据数 |
| ATOM-CONC-FENCE-001 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-CONC-LOCK-001 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-CONC-RACE-001 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-HIST-AUTOPTR-001 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-LANG-BITFIELD-001 | SUPPORTED | medium | `draft+observation+evidence` | draft | 1 |
| ATOM-LANG-DECAY-001 | SUPPORTED | medium | `draft+observation+evidence` | draft | 1 |
| ATOM-LANG-FNPTR-001 | SUPPORTED | medium | `draft+observation+evidence` | draft | 1 |
| ATOM-LANG-INLINE-001 | SUPPORTED | low | `evidence_only` | draft | 2 |
| ATOM-LANG-INTPROMO-001 | SUPPORTED | medium | `draft+observation+evidence` | draft | 1 |
| ATOM-LANG-MACRO-001 | SUPPORTED | medium | `draft+observation+evidence` | draft | 1 |
| ATOM-LANG-SETJMP-001 | SUPPORTED | medium | `draft+observation+evidence` | draft | 1 |
| ATOM-LANG-VOLATILE-001 | SUPPORTED | medium | `draft+observation+evidence` | draft | 1 |
| ATOM-MEM-ALIGN-001 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-MEM-ALLOC-001 | SUPPORTED | high | `status=verified` | verified | 3 |
| ATOM-MEM-ALLOC-002 | SUPPORTED | high | `status=red-team-verified` | red-team-verified | 2 |
| ATOM-MEM-LEAK-001 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-MEM-LEAK-002 | SUPPORTED | high | `status=red-team-verified` | red-team-verified | 2 |
| ATOM-MEM-MALLOC-001 | SUPPORTED | medium | `draft+observation+evidence` | draft | 1 |
| ATOM-MEM-MOVE-002 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-MEM-NEW-001 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-MEM-PERF-001 | SUPPORTED | high | `status=verified` | verified | 3 |
| ATOM-MEM-PERF-002 | SUPPORTED | high | `status=verified` | verified | 3 |
| ATOM-MEM-PERF-003 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-MEM-PERF-004 | SUPPORTED | high | `status=red-team-verified` | red-team-verified | 2 |
| ATOM-MEM-RAII-001 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-MEM-RAII-002 | SUPPORTED | high | `status=verified` | verified | 3 |
| ATOM-MEM-RVREF-001 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-MEM-SHARED-001 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-MEM-SHARED-002 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-MEM-STRBOUND-001 | SUPPORTED | medium | `draft+observation+evidence` | draft | 1 |
| ATOM-MEM-UNIQUE-001 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-MEM-UNIQUE-002 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-MEM-VALUE-001 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-MEM-VALUE-002 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-MEM-WEAK-001 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-UB-GRAY-001 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-UB-SIGNEDOVF-001 | SUPPORTED | medium | `draft+observation+evidence` | draft | 1 |

