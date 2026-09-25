# 640b A1 · W2 数字单一权威源（根治涟漪）

## 一、问题

W2 的 IN/OUT/defeating_edges 是**会随人签/重算演进**的量，但 27 处测试/工具各自
把当前数字写死 ⇒ 640 A1 重算后批量过期红（640b 的 28 项）。

## 二、设计：`tools/w2_authority_640b.py`

| 入口 | 路径 | 用途 |
|---|---|---|
| `compute_w2_summary()` | **现算**：事实源（边 + 人审）→ `weighted_af_solver.solve_reviewed` | 权威真值 |
| `artifact_summary()` | **读产物**：`data/grounded_labels_w2.json` | 入库快照 |
| `summary()["consistent"]` | 两路交叉校验 | **产物过期/漂移立刻可见** |
| `current()` / `triple()` | 便捷取值（测试用） | 避免各处写死 |

**为什么两条路径**：只留一条会出现"两边读同一物 ⇒ 恒相等 ⇒ 测了等于没测"
（§三.1 禁止自我证明）。现算 vs 产物是**同源不同物**（求解 vs 磁盘），
产物被误改会立刻报警（640b 实测：仅改产物 ⇒ 12 处漂移告警）。

**零导入纪律的例外**：`independent_verifier_628` / `run_628_gate` 有"不 import 项目
工具"的铁律（被测试锁死）⇒ 它们直读同一**数据文件**（`grounded_labels_w2.json`），
仍是同一权威源，只是取数方式不同（已在该两处注明）。

## 三、改造清单（写死 → 权威源）

- 工具：`defense_chain`（汇总 + 可信度口径）、`human_review_dashboard`、
  `human_review_dashboard_v2_628`、`run_628_gate`、`independent_verifier_628`、
  `mirror_edge_symmetry_write_628`、`third_party_audit_demo_628`、
  `v2_flag_integration_verify_628`、`w2_projection_normalizer_627`、
  `w2_projection_diff_627`；
- 测试：`test_defense_chain_610` / `_cli_610`、`test_grounded_audit_596`、
  `test_human_review_dashboard_610` / `_v2_628`、`test_independent_verifier_628`、
  `test_metrics_*_608/610`、`test_mirror_symmetry_write_628`、`test_run_628_gate_628`、
  `test_third_party_audit_demo_628`、`test_transparency_log_628`、
  `test_v2_flag_integration_628`、`test_vsa_attestation_628`、`test_w2_projection_627`、
  `test_weighted_af_solver_596`；
- 新增：`tests/test_w2_authority_640b.py`（6 例）。

## 四、验证（§四.3 模拟变化）

| 模拟 | 手段 | 结果 |
|---|---|---|
| A：仅改产物 | 翻转 1 个节点（artifact 80/41 vs 现算 79/42） | **12 红，全部为漂移告警**（交叉校验按设计报警），**0 处"写死数字"型红** |
| B：两路同步偏移 | 产物翻转 + `W2_SIM_OFFSET=1`（现算同步） | 6 红，全部来自**另有独立自算 W2 的 6 处实现**（normalizer / v2 编译器 / gate 子进程 / vsa 结果）与权威源不同步——同样是漂移告警 |
| 还原 | 恢复产物 | 18 个文件 133 项**全绿** |

**结论**：写死数字导致的批量红**已消除**（原 28 项无一因数字过期再现红）；
剩余告警都是"两条独立路径不一致"的**真实信号**——这正是治理要的。

## 五、诚实边界

1. `W2_SIM_OFFSET` 是测试用模拟开关（默认 0；仅 A 类文档与模拟使用）；
2. 历史**里程碑记录**（613/629/630/631/632 baseline 文档里的 "IN114/OUT7"）
   是时点快照，**保持不动**（§三.2 的"冻结里程碑"），仅加本次说明；
3. 权威源不自带"版本"概念：产物与现算不一致时只报 `consistent=False`，
   不自动改写任一方向——写盘权仍归各工具（`--report`/`sync`）。
