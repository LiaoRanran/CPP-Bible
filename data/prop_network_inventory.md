# 命题网络台账（592 任务4 · R4 grounded 层输入基线）

> **只读生成**：`.venv\Scripts\python.exe tools/prop_network_inventory.py`（`--check` 校验本文件与事实源一致）。
> 数据源：`data/propositions.db`（`prop_graph.py build` 的派生视图）+ 卡面 `claim_structured` + `tools/prop_closure.py` 的闭包。
> 本文件是**人审清单**，不参与任何判决；数字与事实源不一致即视为台账过期。

## 0. 汇总与完整性校验

- 命题 **79** · 命题所属卡 **27** · 卡节点 80（含证据卡 53）· 边 **274** · 连通分量 26
- 闭包大小（全体节点口径，含命题+卡两类 id）：avg 6.076 / max 8 / min 4 · 分布 {'4': 4, '5': 6, '6': 57, '7': 4, '8': 8}
- 可达命题数：avg 3.025 / max 4
- 活性锚：observation 命题 50 条，其中有锚 42 条

| 完整性校验 | 期望 | 实测 | 结论 |
|---|---|---|---|
| 引用卡不存在的命题 | 0 | 0 | ✓ |
| 无命题的原子卡 | 0 | 0 | ✓ |
| 闭包大小异常（>50 或 =1） | 0 | 0 | ✓ |

## 1. 命题列表（逐条）

| # | 命题 | 类型 | 引用卡 | 闭包大小 | 签署 | 活性锚 |
|---|---|---|---|---|---|---|
| 1 | `ATOM-CONC-FENCE-001/prop-1` | observation | EV-CONC-001, EV-CONC-002 | 5 | human:liaoranran | 有锚 |
| 2 | `ATOM-CONC-FENCE-001/prop-2` | inference | EV-CONC-002 | 5 | human:liaoranran | n/a（inference） |
| 3 | `ATOM-CONC-LOCK-001/prop-1` | observation | EV-CONC-003, EV-CONC-004 | 5 | human:liaoranran | 有锚 |
| 4 | `ATOM-CONC-LOCK-001/prop-2` | inference | EV-CONC-003, EV-CONC-004 | 5 | human:liaoranran | n/a（inference） |
| 5 | `ATOM-CONC-RACE-001/prop-1` | observation | EV-CONC-005, EV-CONC-006 | 6 | human:liaoranran | 有锚 |
| 6 | `ATOM-CONC-RACE-001/prop-2` | inference | EV-CONC-005, EV-CONC-006 | 6 | human:liaoranran | n/a（inference） |
| 7 | `ATOM-CONC-RACE-001/prop-3` | inference | EV-CONC-005, EV-CONC-006 | 6 | human:liaoranran | n/a（inference） |
| 8 | `ATOM-HIST-AUTOPTR-001/prop-1` | observation | EV-HIST-001, EV-MEM-003 | 7 | human:liaoranran | 有锚 |
| 9 | `ATOM-HIST-AUTOPTR-001/prop-2` | observation | EV-HIST-001, EV-MEM-003 | 7 | human:liaoranran | 有锚 |
| 10 | `ATOM-HIST-AUTOPTR-001/prop-3` | inference | EV-HIST-001, EV-MEM-003 | 7 | human:liaoranran | n/a（inference） |
| 11 | `ATOM-HIST-AUTOPTR-001/prop-4` | observation | EV-HIST-001 | 7 | human:liaoranran | 有锚 |
| 12 | `ATOM-LANG-INLINE-001/prop-1` | observation | EV-LANG-001, EV-LANG-002 | 6 | human:liaoranran | 缺锚（无 liveness 字段） |
| 13 | `ATOM-LANG-INLINE-001/prop-2` | observation | EV-LANG-001, EV-LANG-002 | 6 | human:liaoranran | 缺锚（无 liveness 字段） |
| 14 | `ATOM-LANG-INLINE-001/prop-3` | inference | EV-LANG-001, EV-LANG-002 | 6 | human:liaoranran | n/a（inference） |
| 15 | `ATOM-MEM-ALIGN-001/prop-1` | observation | EV-MEM-019 | 6 | human:liaoranran | 有锚 |
| 16 | `ATOM-MEM-ALIGN-001/prop-2` | observation | EV-MEM-020 | 6 | human:liaoranran | 有锚 |
| 17 | `ATOM-MEM-ALIGN-001/prop-3` | inference | EV-MEM-019, EV-MEM-020 | 6 | human:liaoranran | n/a（inference） |
| 18 | `ATOM-MEM-ALLOC-001/prop-1` | observation | EV-MEM-026 | 8 | human:liaoranran | 有锚 |
| 19 | `ATOM-MEM-ALLOC-001/prop-2` | observation | EV-MEM-027 | 8 | human:liaoranran | 有锚 |
| 20 | `ATOM-MEM-ALLOC-001/prop-3` | observation | EV-MEM-028 | 8 | human:liaoranran | 有锚 |
| 21 | `ATOM-MEM-ALLOC-001/prop-4` | inference | EV-MEM-026 | 8 | human:liaoranran | n/a（inference） |
| 22 | `ATOM-MEM-ALLOC-002/prop-1` | observation | EV-MEM-040, EV-MEM-041 | 6 | human:liaoranran | 缺锚（无 liveness 字段） |
| 23 | `ATOM-MEM-ALLOC-002/prop-2` | observation | EV-MEM-040, EV-MEM-041 | 6 | human:liaoranran | 缺锚（无 liveness 字段） |
| 24 | `ATOM-MEM-ALLOC-002/prop-3` | inference | EV-MEM-040, EV-MEM-041 | 6 | human:liaoranran | n/a（inference） |
| 25 | `ATOM-MEM-LEAK-001/prop-1` | observation | EV-MEM-036 | 6 | human:liaoranran | 有锚 |
| 26 | `ATOM-MEM-LEAK-001/prop-2` | observation | EV-MEM-037 | 6 | human:liaoranran | 有锚 |
| 27 | `ATOM-MEM-LEAK-001/prop-3` | inference | EV-MEM-036, EV-MEM-037 | 6 | human:liaoranran | n/a（inference） |
| 28 | `ATOM-MEM-LEAK-002/prop-1` | observation | EV-MEM-042, EV-MEM-043 | 6 | human:liaoranran | 缺锚（无 liveness 字段） |
| 29 | `ATOM-MEM-LEAK-002/prop-2` | observation | EV-MEM-042, EV-MEM-043 | 6 | human:liaoranran | 缺锚（无 liveness 字段） |
| 30 | `ATOM-MEM-LEAK-002/prop-3` | inference | EV-MEM-042, EV-MEM-043 | 6 | human:liaoranran | n/a（inference） |
| 31 | `ATOM-MEM-MOVE-002/prop-1` | observation | EV-MEM-001 | 6 | human:liaoranran | 有锚 |
| 32 | `ATOM-MEM-MOVE-002/prop-2` | observation | EV-MEM-002 | 6 | human:liaoranran | 有锚 |
| 33 | `ATOM-MEM-MOVE-002/prop-3` | inference | EV-MEM-001, EV-MEM-002 | 6 | human:liaoranran | n/a（inference） |
| 34 | `ATOM-MEM-NEW-001/prop-1` | observation | EV-MEM-017 | 6 | human:liaoranran | 有锚 |
| 35 | `ATOM-MEM-NEW-001/prop-2` | observation | EV-MEM-018 | 6 | human:liaoranran | 有锚 |
| 36 | `ATOM-MEM-NEW-001/prop-3` | inference | EV-MEM-017, EV-MEM-018 | 6 | human:liaoranran | n/a（inference） |
| 37 | `ATOM-MEM-PERF-001/prop-1` | observation | EV-MEM-008 | 5 | human:liaoranran | 有锚 |
| 38 | `ATOM-MEM-PERF-001/prop-2` | inference | EV-MEM-008, EV-MEM-001 | 5 | human:liaoranran | n/a（inference） |
| 39 | `ATOM-MEM-PERF-002/prop-1` | observation | EV-MEM-029 | 4 | human:liaoranran | 有锚 |
| 40 | `ATOM-MEM-PERF-002/prop-2` | inference | EV-MEM-029 | 4 | human:liaoranran | n/a（inference） |
| 41 | `ATOM-MEM-PERF-003/prop-1` | observation | EV-MEM-038 | 6 | human:liaoranran | 有锚 |
| 42 | `ATOM-MEM-PERF-003/prop-2` | inference | EV-MEM-038 | 6 | human:liaoranran | n/a（inference） |
| 43 | `ATOM-MEM-PERF-003/prop-3` | inference | EV-MEM-039 | 6 | human:liaoranran | n/a（inference） |
| 44 | `ATOM-MEM-PERF-004/prop-1` | observation | EV-MEM-044, EV-MEM-045 | 6 | human:liaoranran | 缺锚（无 liveness 字段） |
| 45 | `ATOM-MEM-PERF-004/prop-2` | observation | EV-MEM-044, EV-MEM-045 | 6 | human:liaoranran | 缺锚（无 liveness 字段） |
| 46 | `ATOM-MEM-PERF-004/prop-3` | inference | EV-MEM-044, EV-MEM-045 | 6 | human:liaoranran | n/a（inference） |
| 47 | `ATOM-MEM-RAII-001/prop-1` | observation | EV-MEM-009 | 6 | human:liaoranran | 有锚 |
| 48 | `ATOM-MEM-RAII-001/prop-2` | observation | EV-MEM-010 | 6 | human:liaoranran | 有锚 |
| 49 | `ATOM-MEM-RAII-001/prop-3` | inference | EV-MEM-009, EV-MEM-010 | 6 | human:liaoranran | n/a（inference） |
| 50 | `ATOM-MEM-RAII-002/prop-1` | observation | EV-MEM-023 | 8 | human:liaoranran | 有锚 |
| 51 | `ATOM-MEM-RAII-002/prop-2` | observation | EV-MEM-024 | 8 | human:liaoranran | 有锚 |
| 52 | `ATOM-MEM-RAII-002/prop-3` | observation | EV-MEM-025 | 8 | human:liaoranran | 有锚 |
| 53 | `ATOM-MEM-RAII-002/prop-4` | inference | EV-MEM-023, EV-MEM-024, EV-MEM-025 | 8 | human:liaoranran | n/a（inference） |
| 54 | `ATOM-MEM-RVREF-001/prop-1` | observation | EV-MEM-004 | 6 | human:liaoranran | 有锚 |
| 55 | `ATOM-MEM-RVREF-001/prop-2` | observation | EV-MEM-005 | 6 | human:liaoranran | 有锚 |
| 56 | `ATOM-MEM-RVREF-001/prop-3` | inference | EV-MEM-004, EV-MEM-005 | 6 | human:liaoranran | n/a（inference） |
| 57 | `ATOM-MEM-SHARED-001/prop-1` | observation | EV-MEM-013 | 6 | human:liaoranran | 有锚 |
| 58 | `ATOM-MEM-SHARED-001/prop-2` | observation | EV-MEM-014 | 6 | human:liaoranran | 有锚 |
| 59 | `ATOM-MEM-SHARED-001/prop-3` | inference | EV-MEM-013, EV-MEM-014 | 6 | human:liaoranran | n/a（inference） |
| 60 | `ATOM-MEM-SHARED-002/prop-1` | observation | EV-MEM-034 | 6 | human:liaoranran | 有锚 |
| 61 | `ATOM-MEM-SHARED-002/prop-2` | observation | EV-MEM-034 | 6 | human:liaoranran | 有锚 |
| 62 | `ATOM-MEM-SHARED-002/prop-3` | inference | EV-MEM-034, EV-MEM-035 | 6 | human:liaoranran | n/a（inference） |
| 63 | `ATOM-MEM-UNIQUE-001/prop-1` | observation | EV-MEM-011 | 6 | human:liaoranran | 有锚 |
| 64 | `ATOM-MEM-UNIQUE-001/prop-2` | observation | EV-MEM-012 | 6 | human:liaoranran | 有锚 |
| 65 | `ATOM-MEM-UNIQUE-001/prop-3` | inference | EV-MEM-011, EV-MEM-012 | 6 | human:liaoranran | n/a（inference） |
| 66 | `ATOM-MEM-UNIQUE-002/prop-1` | observation | EV-MEM-032 | 6 | human:liaoranran | 有锚 |
| 67 | `ATOM-MEM-UNIQUE-002/prop-2` | observation | EV-MEM-033 | 6 | human:liaoranran | 有锚 |
| 68 | `ATOM-MEM-UNIQUE-002/prop-3` | inference | EV-MEM-032, EV-MEM-033 | 6 | human:liaoranran | n/a（inference） |
| 69 | `ATOM-MEM-VALUE-001/prop-1` | observation | EV-MEM-006 | 6 | human:liaoranran | 有锚 |
| 70 | `ATOM-MEM-VALUE-001/prop-2` | observation | EV-MEM-007 | 6 | human:liaoranran | 有锚 |
| 71 | `ATOM-MEM-VALUE-001/prop-3` | inference | EV-MEM-006, EV-MEM-007 | 6 | human:liaoranran | n/a（inference） |
| 72 | `ATOM-MEM-VALUE-002/prop-1` | observation | EV-MEM-021 | 6 | human:liaoranran | 有锚 |
| 73 | `ATOM-MEM-VALUE-002/prop-2` | observation | EV-MEM-022 | 6 | human:liaoranran | 有锚 |
| 74 | `ATOM-MEM-VALUE-002/prop-3` | inference | EV-MEM-021, EV-MEM-022 | 6 | human:liaoranran | n/a（inference） |
| 75 | `ATOM-MEM-WEAK-001/prop-1` | observation | EV-MEM-015 | 6 | human:liaoranran | 有锚 |
| 76 | `ATOM-MEM-WEAK-001/prop-2` | observation | EV-MEM-016 | 6 | human:liaoranran | 有锚 |
| 77 | `ATOM-MEM-WEAK-001/prop-3` | inference | EV-MEM-015, EV-MEM-016 | 6 | human:liaoranran | n/a（inference） |
| 78 | `ATOM-UB-GRAY-001/prop-1` | observation | EV-UB-001 | 4 | human:liaoranran | 有锚 |
| 79 | `ATOM-UB-GRAY-001/prop-2` | inference | EV-UB-001 | 4 | human:liaoranran | n/a（inference） |

## 2. 卡列表（27 张原子卡）

| 卡 | 命题数 | verified_by（卡级人签） | oracle 状态 | 本卡命题闭包大小 |
|---|---|---|---|---|
| `ATOM-CONC-FENCE-001` | 2 | human:liaoranran | 未填（正常状态） | 5–5 |
| `ATOM-CONC-LOCK-001` | 2 | human:liaoranran | 未填（正常状态） | 5–5 |
| `ATOM-CONC-RACE-001` | 3 | human:liaoranran | 未填（正常状态） | 6–6 |
| `ATOM-HIST-AUTOPTR-001` | 4 | human:liaoranran | 未填（正常状态） | 7–7 |
| `ATOM-LANG-INLINE-001` | 3 | — | 未填（正常状态） | 6–6 |
| `ATOM-MEM-ALIGN-001` | 3 | human:liaoranran | 未填（正常状态） | 6–6 |
| `ATOM-MEM-ALLOC-001` | 4 | human:liaoranran | 未填（正常状态） | 8–8 |
| `ATOM-MEM-ALLOC-002` | 3 | redteam:g5_batch5 | 未填（正常状态） | 6–6 |
| `ATOM-MEM-LEAK-001` | 3 | human:liaoranran | 未填（正常状态） | 6–6 |
| `ATOM-MEM-LEAK-002` | 3 | redteam:g5_batch5 | 未填（正常状态） | 6–6 |
| `ATOM-MEM-MOVE-002` | 3 | human:liaoranran | 未填（正常状态） | 6–6 |
| `ATOM-MEM-NEW-001` | 3 | human:liaoranran | 未填（正常状态） | 6–6 |
| `ATOM-MEM-PERF-001` | 2 | human:liaoranran | 未填（正常状态） | 5–5 |
| `ATOM-MEM-PERF-002` | 2 | human:liaoranran | 未填（正常状态） | 4–4 |
| `ATOM-MEM-PERF-003` | 3 | human:liaoranran | 未填（正常状态） | 6–6 |
| `ATOM-MEM-PERF-004` | 3 | redteam:g5_batch5 | 未填（正常状态） | 6–6 |
| `ATOM-MEM-RAII-001` | 3 | human:liaoranran | 未填（正常状态） | 6–6 |
| `ATOM-MEM-RAII-002` | 4 | human:liaoranran | 未填（正常状态） | 8–8 |
| `ATOM-MEM-RVREF-001` | 3 | human:liaoranran | 未填（正常状态） | 6–6 |
| `ATOM-MEM-SHARED-001` | 3 | human:liaoranran | 未填（正常状态） | 6–6 |
| `ATOM-MEM-SHARED-002` | 3 | human:liaoranran | 未填（正常状态） | 6–6 |
| `ATOM-MEM-UNIQUE-001` | 3 | human:liaoranran | 未填（正常状态） | 6–6 |
| `ATOM-MEM-UNIQUE-002` | 3 | human:liaoranran | 未填（正常状态） | 6–6 |
| `ATOM-MEM-VALUE-001` | 3 | human:liaoranran | 未填（正常状态） | 6–6 |
| `ATOM-MEM-VALUE-002` | 3 | human:liaoranran | 未填（正常状态） | 6–6 |
| `ATOM-MEM-WEAK-001` | 3 | human:liaoranran | 未填（正常状态） | 6–6 |
| `ATOM-UB-GRAY-001` | 2 | human:liaoranran | 未填（正常状态） | 4–4 |

## 3. 边统计

| 边类型 | 条数 | 说明 |
|---|---|---|
| 命题 → 本卡 | 79 | 每条命题引用自己所属的原子卡 |
| 命题 → 证据卡 | 116 | `claim_structured[*].evidence` 逐条 |
| 卡 → 命题 | 79 | 卡声明自己的命题（反向边） |
| **合计（去重后）** | **274** | 三类合计 274（含重复对） |
| 卡节点 | 80 | 命题所属卡 27 + 证据卡 53 |

## 4. 闭包口径与对账

- 闭包定义：从命题出发，沿 `card→prop` / `prop→card` / `prop→evidence` 有向边可达的**全部节点**（含命题与卡两类 id）。
- 双实现对账：`tools/prop_closure.py cross-check`（Python BFS vs SQL `WITH RECURSIVE`）必须逐集合相等；不一致时该命令 **exit 2**。
- oracle 统计（报告层只读，不改判决）：未填字段 83 张 · stale 0 张 · 放权开关 {"G-iso": false, "oracle_auto_accept": false, "llm_as_judge": false}

