# 612 C1 · oracle 验证报告（只读 · 不填 verified_by_oracle）

> 三门禁：gate `--check` / poison / replay `--check`（**oracle 验证专用**，非监工验收）。**不填** `verified_by_oracle`（人审权力）。

## 一、三门禁结果（全局）

| 门 | 状态 | exit | 耗时(s) |
|---|---|---|---|
| gate | pass | 0 | 5.3 |
| poison | pass | 0 | 8.3 |
| replay | timeout | None | 90.0 |

- 关键数字：{'gate_block': 0, 'gate_warn': 186, 'gate_advice': 5, 'poison_covered': 63, 'poison_total': 63}
- replay `--check` 全量约 300s ⇒ 超预算时标记 `timeout`（任务书允许），不代表失败（已知基线 confirm=56/refute=0/infra=0）。

## 二、逐卡清单

| 卡 | gate block | warn | advice | 状态 |
|---|---|---|---|---|
| `ATOM-CONC-FENCE-001` | 0 | 4 | 0 | pass |
| `ATOM-CONC-LOCK-001` | 0 | 4 | 0 | pass |
| `ATOM-CONC-RACE-001` | 0 | 6 | 0 | pass |
| `ATOM-HIST-AUTOPTR-001` | 0 | 7 | 0 | pass |
| `ATOM-LANG-INLINE-001` | 0 | 5 | 0 | pass |
| `ATOM-MEM-ALIGN-001` | 0 | 6 | 0 | pass |
| `ATOM-MEM-ALLOC-001` | 0 | 8 | 0 | pass |
| `ATOM-MEM-ALLOC-002` | 0 | 6 | 0 | pass |
| `ATOM-MEM-LEAK-001` | 0 | 6 | 0 | pass |
| `ATOM-MEM-LEAK-002` | 0 | 6 | 0 | pass |
| `ATOM-MEM-MOVE-002` | 0 | 6 | 0 | pass |
| `ATOM-MEM-NEW-001` | 0 | 6 | 0 | pass |
| `ATOM-MEM-PERF-001` | 0 | 4 | 0 | pass |
| `ATOM-MEM-PERF-002` | 0 | 4 | 0 | pass |
| `ATOM-MEM-PERF-003` | 0 | 6 | 0 | pass |
| `ATOM-MEM-PERF-004` | 0 | 6 | 0 | pass |
| `ATOM-MEM-RAII-001` | 0 | 6 | 0 | pass |
| `ATOM-MEM-RAII-002` | 0 | 8 | 0 | pass |
| `ATOM-MEM-RVREF-001` | 0 | 6 | 0 | pass |
| `ATOM-MEM-SHARED-001` | 0 | 6 | 0 | pass |
| `ATOM-MEM-SHARED-002` | 0 | 6 | 0 | pass |
| `ATOM-MEM-UNIQUE-001` | 0 | 6 | 0 | pass |
| `ATOM-MEM-UNIQUE-002` | 0 | 6 | 0 | pass |
| `ATOM-MEM-VALUE-001` | 0 | 6 | 0 | pass |
| `ATOM-MEM-VALUE-002` | 0 | 6 | 0 | pass |
| `ATOM-MEM-WEAK-001` | 0 | 6 | 0 | pass |
| `ATOM-UB-GRAY-001` | 0 | 5 | 0 | pass |
| `EV-CONC-001` | 0 | 1 | 2 | pass |
| `EV-CONC-002` | 0 | 2 | 1 | pass |
| `EV-CONC-003` | 0 | 2 | 1 | pass |
| `EV-CONC-004` | 0 | 2 | 1 | pass |
| `EV-CONC-005` | 0 | 2 | 0 | pass |
| `EV-CONC-006` | 0 | 2 | 0 | pass |
| `EV-HIST-001` | 0 | 1 | 0 | pass |
| `EV-LANG-001` | 0 | 1 | 0 | pass |
| `EV-LANG-002` | 0 | 2 | 0 | pass |
| `EV-MEM-001` | 0 | 2 | 0 | pass |
| `EV-MEM-002` | 0 | 0 | 0 | pass |
| `EV-MEM-003` | 0 | 1 | 0 | pass |
| `EV-MEM-004` | 0 | 0 | 0 | pass |
| `EV-MEM-005` | 0 | 0 | 0 | pass |
| `EV-MEM-006` | 0 | 1 | 0 | pass |
| `EV-MEM-007` | 0 | 0 | 0 | pass |
| `EV-MEM-008` | 0 | 0 | 0 | pass |
| `EV-MEM-009` | 0 | 0 | 0 | pass |
| `EV-MEM-010` | 0 | 1 | 0 | pass |
| `EV-MEM-011` | 0 | 0 | 0 | pass |
| `EV-MEM-012` | 0 | 0 | 0 | pass |
| `EV-MEM-013` | 0 | 0 | 0 | pass |
| `EV-MEM-014` | 0 | 0 | 0 | pass |
| `EV-MEM-015` | 0 | 0 | 0 | pass |
| `EV-MEM-016` | 0 | 0 | 0 | pass |
| `EV-MEM-017` | 0 | 1 | 0 | pass |
| `EV-MEM-018` | 0 | 0 | 0 | pass |
| `EV-MEM-019` | 0 | 0 | 0 | pass |
| `EV-MEM-020` | 0 | 0 | 0 | pass |
| `EV-MEM-021` | 0 | 0 | 0 | pass |
| `EV-MEM-022` | 0 | 0 | 0 | pass |
| `EV-MEM-023` | 0 | 0 | 0 | pass |
| `EV-MEM-024` | 0 | 0 | 0 | pass |
| `EV-MEM-025` | 0 | 0 | 0 | pass |
| `EV-MEM-026` | 0 | 0 | 0 | pass |
| `EV-MEM-027` | 0 | 0 | 0 | pass |
| `EV-MEM-028` | 0 | 0 | 0 | pass |
| `EV-MEM-029` | 0 | 0 | 0 | pass |
| `EV-MEM-030` | 0 | 0 | 0 | pass |
| `EV-MEM-031` | 0 | 0 | 0 | pass |
| `EV-MEM-032` | 0 | 0 | 0 | pass |
| `EV-MEM-033` | 0 | 0 | 0 | pass |
| `EV-MEM-034` | 0 | 0 | 0 | pass |
| `EV-MEM-035` | 0 | 1 | 0 | pass |
| `EV-MEM-036` | 0 | 0 | 0 | pass |
| `EV-MEM-037` | 0 | 0 | 0 | pass |
| `EV-MEM-038` | 0 | 0 | 0 | pass |
| `EV-MEM-039` | 0 | 1 | 0 | pass |
| `EV-MEM-040` | 0 | 1 | 0 | pass |
| `EV-MEM-041` | 0 | 1 | 0 | pass |
| `EV-MEM-042` | 0 | 1 | 0 | pass |
| `EV-MEM-043` | 0 | 1 | 0 | pass |
| `EV-MEM-044` | 0 | 1 | 0 | pass |
| `EV-MEM-045` | 0 | 1 | 0 | pass |
| `EV-UB-001` | 0 | 0 | 0 | pass |
| `EV-UB-002` | 0 | 0 | 0 | pass |

## 三、失败卡详情

（无：本批扫描的卡 gate 无 block）

## 四、异常卡（超时/错误）

- replay

## 五、口径与边界

- **只读**：不填 `verified_by_oracle`、不改任何卡；每门调用前打印「oracle 验证专用」；
- 逐卡归因只对 **gate**（其输出带卡路径）有效；poison/replay 是**全局**门，逐卡状态沿用全局；
- 优先级 Top 排序复用 C2。
