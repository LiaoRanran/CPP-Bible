# metrics 字段 schema（616 版）

> 本文档记录 `metrics_collector` 产出字段的含义与计算方法；**明确标注历史参考 vs 推荐使用**。

## 一、扁平 27 项（`snap["metrics"]`，未变）
5 类：Quality 9 / Assets 7 / Performance 4 / Cost 3 / Health 4（`ALL_METRICS`，**本批未增删**）。
- Quality：`gate_block_count` / `gate_warn_count` / `gate_rule_count` / `poison_pass_count` /
  `poison_total_count` / `poison_coverage_pct` / `replay_confirm_count` / `replay_refute_count` /
  `replay_infra_error_count`。
- Assets：`atoms_total` / `atoms_verified` / `atoms_draft` / `evidence_total` / `evidence_confirm` /
  `misconceptions_total` / `asm_files_count`。
- Performance：`pytest_wall_seconds` / `replay_wall_seconds` / `gate_wall_seconds` / `ci_total_seconds`。
- Cost / Health：`cost_tracker_*` / `git_ahead_count` / `git_untracked_count` /
  `debt_ledger_open_count` / `golden_state_atoms_match`。

## 二、逃逸率口径字段（`collect_curves()["mutation_escape_rate"]`）
| 字段 | 含义 | 计算 | 状态 |
|---|---|---|---|
| `point` / `point_raw` | 逃逸率点估计 | escaped / (blocked+escaped) | 参考 |
| `cp_low` / `cp_high` | **固定样本** Clopper-Pearson 双侧 95% 区间 | `stat_bounds.proportion` | ⚠ **历史参考**（连续偷看下无效） |
| `cs_lower` / `cs_upper` | **置信序列** anytime 区间 | `confidence_sequence.cs_interval` | ✅ **推荐** |
| `cs_alpha` | 置信序列显著性水平 | 默认 0.05 | ✅ |
| `peeking_correction` | 是否已用 CS 修正偷看 | `True` | ✅ |
| `cp_vs_cs_note` | 口径说明 | 常量文本 | ✅ |
| `judged` / `n_a` / `numerator` / `denominator` / `conf` | 分母/计数元数据 | 基线文件 | 参考 |

> **口径纪律**：**连续监控看 cs_***（anytime-valid）；**里程碑终点看 cp_***（固定样本）。
> **二者均为 95%，不可混用**；引用时须标注引用的是哪一个。

## 三、历史版本对照（`mutation_escape_rate_history`）
逐版本（v1–v6）同结构，含 `baseline_version` / `frozen_at_commit` / `cs_*`（本批新增）。

## 四、其他曲线字段
- `overturned_by_stronger_verifier` / `overturned_recent`；`escape_survival_batches`。
- `collect_build_reproducibility` 的结果写入 `notes["reproducible_rate"]`。

## 五、版本
- v616：新增 `cs_*` / `peeking_correction` / `cp_vs_cs_note`（**不删** `cp_*`，保留历史可比性）。
