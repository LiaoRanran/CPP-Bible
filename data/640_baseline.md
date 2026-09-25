# 640 批次 · 开工快照（Task 0）

> 生成：2026-09-25。基线 commit：34b4b8ef（639 E1 收尾）。

## 一、快照

| 维度 | 值 |
|---|---|
| tools/*.py | 434（含 4 个无 CLI 入口的库模块） |
| tests/test_*.py | 446+ |
| pytest 全量 | **36 FAILED / 0 ERROR**（与 639 R4 登记完全一致，无新增） |
| ruff / mypy | 绿（430+ 文件 0 errors） |
| ahead | 25+（639 全程未 push） |

## 二、36 项失败清单（分类 = 639 R3/R4 结论的逐项落实）

| # | 测试 | 类型 | 初判根因 |
|---|---|---|---|
| 1 | autoimmune_diagnose_630::test_report_json_and_selftest | 断言过期 | 自身免疫率 100%→0%（632/634 签署修复后） |
| 2-5 | autoimmune_human_queue_631 ×4 | 断言过期 | human 队列 90→65；signed_by 已填（不再属机器禁填字段） |
| 6 | autoimmune_recalc_630::test_read_only_report_and_selftest | 断言过期 | 同 1 |
| 7 | baseline_629::test_gate_counts_measured_equals_standing | 断言过期 | gate 命中 191→121（639 放权闸修复后） |
| 8-10 | bridge_edge_impact_612 ×3 | 断言过期+语义重推导 | approved 基线数变；2 例依赖 modify 语义 |
| 11-13 | metrics_612 ×3 | 断言过期 | keep-low (114,7)→(79,42)；--check/报告连带 |
| 14 | metrics_grounded_status_610::test_divergence | 断言过期 | grounded 114→79 |
| 15-19 | modify_mode_611 ×5 | 断言过期+语义重推导 | 双模式结果趋同（annotation 集 632 后演进） |
| 20-22 | modify_mode_analysis_611 ×3 | 断言过期 | 同上分析件 |
| 23-30 | prop_graph ×8 | 断言过期 | 命题 79 全签/0 未签（566 时代期望"存在未签"） |
| 31-35 | replay_invariants 605/606/608 ×5 | 工具口径变更 | 工具降级 load-only，CLI 无不变量明细/JSON |
| 36 | weighted_af_human_review_609::test_single_approve | 断言过期+语义重推导 | approve 翻转行为随 annotation 演进 |

**诚实声明**：以上"断言过期"为初判；修复时逐项以实际输出取值，发现真实回归即停（§四.1）。

## 三、原始失败清单

全量 pytest 输出：`data/640_pytest_task0.txt`（--tb=no -rA，36 FAILED / 0 ERROR）。
