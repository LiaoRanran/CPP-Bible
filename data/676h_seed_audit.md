# 676h · 随机种子审计（tools/ + data/）

- 生成时间：2026-10-04T09:14:32+08:00
- 扫描范围：tools, data
- 使用随机性的脚本：**30**；实验类已固定种子 16；**实验类未固定种子 0**；非实验/未知 14

## 1. 种子注册表（各脚本实际引用的种子常量）

| 种子 | 用到它的脚本 |
|---|---|
| `1234` | `tools/learner_behavior_logger.py`, `tools/learner_state.py` |
| `20260920` | `tools/learner_twin_dashboard.py` |
| `20260928` | `tools/mutation_test_656.py` |
| `20260930` | `data/676f_analysis.py`, `data/676f_pipeline.py`, `tools/attack_simulator_643.py`, `tools/baseline_670a.py`, `tools/baseline_672g.py`, `tools/blind_protocol_636.py`, `tools/mutation_test_656.py`, `tools/run_a5_experiment_673p.py` …(+5) |
| `20261001` | `tools/trajectory_floor_check_671g.py` |
| `20261003` | `data/676f_pipeline.py` |
| `5000` | `tools/eprocess_671g.py` |
| `636` | `tools/blind_protocol_636.py` |
| `6761` | `data/expansion_676c/analyze_676c.py`, `data/expansion_676c_D/spotcheck_D.py`, `data/expansion_676c_E/pool_E.py`, `data/expansion_676c_E/verify_E.py`, `data/expansion_676c_F/spotcheck_F.py` |
| `67610` | `data/blindspot_676g_runner.py` |
| `6762` | `data/expansion_676cC/finalize_676cC.py`, `data/expansion_676c_G/quality_check.py` |

### 1b. 漂移检测：产物登记的种子 vs 代码里的种子常量

| 产物 | 字段 | 登记值 | 说明 |
|---|---|---|---|
| `data/656_mutation_report.json` | `seed` | `20260928` | 变异（core） → 一致 |
| `data/656_mutation_report_all.json` | `seed` | `20260928` | 变异（all） → 一致 |
| `data/current_numbers.json` | `seed` | `20260930` | 672h 扩样 → 一致 |
| `data/experiments/a5_673p.json` | `seed` | `20260930` | A5 实验 → 一致 |
| `data/experiments/a5_673p.json` | `real_attribution.seed` | `20260930` | A5 Real Attribution → 一致 |
| `data/external_anchor_reveal_672j.json` | `runs` | `3` | 外部锚点（重复次数，非种子） → 一致 |

## 2. 实验类脚本中未固定种子的

（空）—— 所有被判为实验类的脚本都固定了种子或引用了固定种子常量。

## 3. 逐文件明细

| 文件 | 类别 | seed 调用 | 种子常量 |
|---|---|---|---|
| `data/676f_analysis.py` | experiment | no | `20260930` |
| `data/676f_pipeline.py` | experiment | no | `20260930`, `20261003` |
| `data/blindspot_676g_runner.py` | experiment | yes | `67610` |
| `data/expansion_676c/analyze_676c.py` | unknown | yes | `6761` |
| `data/expansion_676cC/finalize_676cC.py` | unknown | yes | `6762` |
| `data/expansion_676c_D/spotcheck_D.py` | unknown | yes | `6761` |
| `data/expansion_676c_E/pool_E.py` | unknown | yes | `6761` |
| `data/expansion_676c_E/verify_E.py` | unknown | yes | `6761` |
| `data/expansion_676c_F/spotcheck_F.py` | unknown | yes | `6761` |
| `data/expansion_676c_G/quality_check.py` | unknown | yes | `6762` |
| `tools/attack_simulator_643.py` | experiment | yes | `20260930` |
| `tools/baseline_670a.py` | experiment | yes | `20260930` |
| `tools/baseline_672g.py` | experiment | no | `20260930` |
| `tools/blind_protocol_636.py` | experiment | yes | `20260930`, `636` |
| `tools/confidence_sequence.py` | experiment | yes | — |
| `tools/eprocess_671g.py` | experiment | yes | `5000` |
| `tools/learner_behavior_logger.py` | non-experiment | yes | `1234` |
| `tools/learner_state.py` | non-experiment | yes | `1234` |
| `tools/learner_twin_dashboard.py` | non-experiment | no | `20260920` |
| `tools/metrics_collector.py` | non-experiment | yes | — |
| `tools/mutation_test_656.py` | experiment | yes | `20260928`, `20260930` |
| `tools/run_a5_experiment_673p.py` | experiment | no | `20260930` |
| `tools/seed_audit_676h.py` | unknown | yes | — |
| `tools/seed_check_671i.py` | unknown | yes | — |
| `tools/select_assets_671b.py` | experiment | yes | `20260930` |
| `tools/selection_strategies_673p.py` | experiment | yes | `20260930` |
| `tools/targeted_attacker_645.py` | experiment | yes | `20260930` |
| `tools/trajectory_floor_check_671g.py` | unknown | yes | `20261001` |
| `tools/verify_baseline_672f.py` | experiment | yes | `20260930` |
| `tools/verify_baseline_672g.py` | experiment | yes | `20260930` |
