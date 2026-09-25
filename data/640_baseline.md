# 640 批次 · 开工快照（Task 0）

> 生成：2026-09-25。基线 commit：34b4b8ef（639 E1 收尾）。

## 一、快照

| 维度 | 值 |
|---|---|
| tools/*.py | 434（开工时；收工时 437，见 §四 A3） |
| tests/test_*.py | 437（收工时） |
| pytest 全量 | **36 FAILED / 0 ERROR**（与 639 R4 登记完全一致，无新增） |
| ruff / mypy | 绿（430+ 文件 0 errors） |
| ahead | 25+（639 全程未 push） |

## 四、A3（D11）数表实测更新

| 数表 | 值 | 来源（动态取值处） |
|---|---|---|
| tools/*.py | **437** | `self_observer_637.collect()['metrics']['tools_total']`（运行时统计） |
| tests/test_*.py | **437** | 同上 `tests_total` |
| 有 --check 的工具 | 430 | `data/640_check_scan.json`（640 A4 全量扫描） |
| 缺 --check | 4（均为无 CLI 库模块，例外已注明） | 同上 |

- 实测复核：`self_observer_637` 与文件系统直数**一致**（437/437）；
- 测试层无硬编码工具数（仅 `> 0` 与键集断言，动态安全）；
- 638 status.json 叙述文本里的"417"为**历史叙述**（收工时点的快照），不属活数表；
- `data/634_soft_baseline.json` 的 `check_tools_min=10` 为下限型软基线（min 语义），
  与 437 不冲突。**D11 结论：活数表均动态取值，无过期硬编码 ⇒ 无需改码，登记实测值。**

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
