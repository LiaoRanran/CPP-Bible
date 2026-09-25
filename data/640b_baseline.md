# 640b · 开工快照（28 项涟漪失败）

> 生成：2026-09-25。终扫来源：`data/640_pytest_final2.txt`（实测 28 FAILED / 0 ERROR）。

## 一、根因分层

**A 类（27 项）— W2 数字过期**：640 A1 重算权威产物
（IN 114→79 / OUT 7→42 / defeating_edges 17→194）后，所有**写死旧数字**的下游
测试/工具常量批量过期。不是新 bug，是"断言写死 + 涟漪"。

**B 类（1 项）— type:ignore 计数**：`test_mypy_fix_625::test_no_bulk_type_ignore`
阈值 28，实测 29。

## 二、清单（逐项）

| # | 测试/工具 | 写死位置 |
|---|---|---|
| 1-2 | defense_chain.py `check()`（汇总 + 可信度口径）| 114/7/0、PROP_CREDIBILITY=medium |
| 3 | test_defense_chain_610（8 处断言） | 114/7/17、链事实 |
| 4 | test_defense_chain_cli_610（4 处） | 114/7/115/6/113/8 |
| 5 | grounded_audit 报告（含退出码前提） | IN114/OUT7 + 异常 35 条 |
| 6 | test_grounded_audit_596（4 处） | 同上 |
| 7 | human_review_dashboard `check()` | OUT MIS 7 |
| 8 | test_human_review_dashboard_610（2 处） | OUT MIS 7 |
| 9 | human_review_dashboard_v2_628.EXPECT_W2 | 114/7/0 |
| 10 | test_human_review_dashboard_v2_628 | 同上 |
| 11 | run_628_gate.EXPECT_W2 | 114/7/0 |
| 12 | test_run_628_gate_628 | 同上 |
| 13 | test_independent_verifier_628（2 处） | 同上 |
| 14 | independent_verifier_628.EXPECT | 同上 |
| 15-16 | metrics_610/608 测试 | 114/7/17/42 |
| 17 | mirror_edge_symmetry_write_628.w2_unchanged | 114/7/0 |
| 18 | third_party_audit_demo_628.EXPECT_W2 | 114/7/0 |
| 19-22 | test_third_party_audit_demo_628（4 处） | 同上 + 凭证入册 |
| 23 | v2_flag_integration_verify_628 | 114/7/0 |
| 24 | test_v2_flag_integration_628 | 同上 |
| 25 | vsa_attestation 测试（2 处） | w2_in 114 + 全量有效 |
| 26 | test_transparency_log_628 | 未入册凭证 |
| 27 | test_weighted_af_solver_596 | auth 114/17 |
| 28 | test_mypy_fix_625::test_no_bulk_type_ignore | 阈值 28 vs 29 |

## 三、本轮额外定位的**真因**（非过期数字）

1. **conftest 会话清理制造无主凭证**：会话结束**还原**数据日志却**保留**新建凭证
   ⇒ `test_transparency_log_628` 反复红。修复：`data/vsa/` 下未跟踪的新凭证按
   "运行时产物"删除（凭证与日志同进同出）+ `third_party.step4` 显式清掉泄漏的
   `CPPBIBLE_TRANSPARENCY_LOG`；
2. **defense_chain 可信度口径落后**：写死 `PROP_CREDIBILITY=medium`，而 W2 内核
   已按命题级人签给 **high** ⇒ 逐节点可信度比对红。修复：与内核同口径取
   `w2.proposition_nodes()` 的 confidence；
3. **type:ignore 第 29 项（640 A2 引入）**：`roadmap_align_640.py:62` 的
   `# type: ignore[arg-type]` **可避免**（删掉后 mypy 仍 0 错）⇒ 真修删除，
   阈值维持 28（不抬阈值）。

## 四、语义后果（登记 641，不擅自改模型）

命题级人签把命题抬到 **high** 后：**误解即使被人审 approve（medium）也仍被判 OUT**
（medium < high ⇒ 被命题击败）。这是模型的直接推论，但暴露一个**设计问题**：
"人审 approve 一个误解"是否应把它抬到 high（与命题人签对等）？
本轮**不改模型**，只把测试改为锁定当前行为并在此登记，交 641 由人裁决。
