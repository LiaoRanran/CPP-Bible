# 608 C0 · metrics 现状与缺口盘点（只读）

> 实跑日期：2026-09-20｜口径：所有数字来自本仓真实文件，不编不猜。

## 1. 当前 metrics_collector 已采指标（27 项 + 曲线）

来源：`tools/metrics_collector.py`（质量度量 L1，508 落地；**只采集只 WARN，不 BLOCK**）。

| 组 | 指标数 | 字段 |
|---|---|---|
| Quality 9 | gate_block/warn/rule_count、poison_pass/total/coverage_pct、replay_confirm/refute/infra_error_count | 门禁/毒样例/重放 |
| Assets 7 | atoms_total/verified/draft、evidence_total/confirm、misconceptions_total、asm_files_count | 知识资产 |
| Performance 4 | pytest_wall_seconds、replay_wall_seconds、gate_wall_seconds、ci_total_seconds | 性能 |
| Cost 3 | cost_tracker_total_tokens/atoms_per_batch/avg_per_atom | 成本 |
| Health 4 | git_ahead_count、git_untracked_count、debt_ledger_open_count、golden_state_atoms_match | 健康度 |

曲线（`collect_curves()`，565 Part 4b）：
- `mutation_escape_rate`（v7 当前口径，含双侧 C-P95 `cp_low`/`cp_high` 与 `*_raw` 全精度原值）
- `mutation_escape_rate_history`：**v1→v7 共 7 个时点**（v1–v6 保留为历史，不覆盖）
- `overturned_by_stronger_verifier`（读只追加事件流）、`escape_survival_batches`

## 2. 历史数据点

`data/metrics.jsonl`（被 gitignore，未跟踪）：当前 **9 个时点**采集记录，可做趋势查询。

## 3. 识别的 5 个缺口（对应 608 C1）

| # | 缺口 | 现状 | 数据真源（只读） |
|---|---|---|---|
| G1 | **人审进度指标** | 无（388 边人审 0/388 未入 metrics） | `attack_edge_review.load_annotations()` + `attack_edge_generator.load_edges()`（`stats()` 已给 pending/approved/rejected/modified） |
| G2 | **论证层状态指标** | 无（W2 判决未入 metrics） | `data/grounded_labels_w2.json`（IN79/OUT42/UNDEC0）+ `attack_edges_candidates.jsonl`（388 边 / 42 MIS 组） |
| G3 | **编译可复现指标** | 仅有 603 的 `build_reproducibility` 采样 + `invariants.build_reproducibility` 布尔；无"时间宏漂移/符号表一致"细分 | `replay_invariants.check_build_reproducibility()`（B1 已加 cross_time / symtab / sections 字段） |
| G4 | **逃逸率收敛曲线** | `collect_curves` 已有 v1→v7 历史 + C-P，但作为嵌套 `curves` 字段，未作为"收敛曲线"显式暴露 | 同上（复用，重排为 `escape_rate_convergence` 显式字段） |
| G5 | **统计上界（C-P95）** | `collect_curves` 已对每点算 `cp_low`/`cp_high`，但未以 `escape_rate_cp_lower/upper` 命名 | `stat_bounds.proportion`（工具内 `from stat_bounds import proportion`） |

## 4. 597 调研建议对齐

- **PAC / VC 统计上界**：用 Clopper-Pearson 双侧 95% 区间（已落地于 `stat_bounds`），对逃逸率 `1/1406` 给出区间（C-P95 ≈ 点估计 0.071% ∈ [0.0018%, 0.3956%] 量级），避免"点估计冒充上界"。
- **收敛曲线**：多时点同口径（v1→v7）对比，但必须标注"尺子变更史"（v1→v5 是口径修正，非同一量时间序列），不得声称单调收敛（仅 1 含曲线时点）。

## 5. 实施原则（硬纪律）

- `metrics_collector.py` **不在 CORE_TOOLS 内** ⇒ 修改后**无需** `tool_integrity --update`。
- 新增指标**只读**读取上述数据文件，**不修改** `attack_edge_review` / `weighted_af_solver` / `replay_invariants` 的判决逻辑（`human_review_queue` 同理：人审权力，只聚合）。
- 不重新生成 mutation 基线（v7 冻结，591）；逃逸率读数只取自已提交基线文件。
- 新增指标以**嵌套字段 `metrics_608`** 挂载到快照，避免破坏既有 27 项扁平 schema 与 history 工具（存量零误伤）。
