# 640c · 开工快照（派生量/历史门禁清算）

> 生成：2026-09-25。任务书：`_auto/inbox/640c.md`。
> 终扫来源：`data/640b_pytest_final.txt`（640b 收工，20 FAILED）。
> 本轮重跑：`data/640c_task0_subset.txt`（同批文件，实测 **19 FAILED** / 0 ERROR）。

## 一、清单核对（§一 与实测的差异，逐条）

640b 终扫列 20 项，本轮同文件重跑得 **19 项**。差异 1 项：

| 640b 清单 | 本轮实测 | 判定 |
|---|---|---|
| `test_run_629_gate.py::test_tool_manifest_is_complete` | **通过** | 640b 提交（2c50a563）新增 `tools/w2_authority_640b.py` 等文件后，该测试的 `LATER_BATCH_ADDED` 旁证成立 ⇒ 由红转绿。**非本轮修复，属清单过期**（640b 终扫与提交之间存在时差）。 |

其余 19 项与 640b 清单**逐条一致**，无遗漏、无多算。

## 二、逐项清单（19 项，实测）

### A 类：派生量写死（14 项）

当前真实口径（两路交叉校验一致，见 `tools/w2_authority_640b.py`）：

- W2：**IN 79 / OUT 42 / UNDEC 0**，击败边 **194**，边 388，节点 121
- 可信度分布：**high 79 / medium 35 / low 7**
- OUT 且无 W2 辩护者的 MIS：**42**（旧值 1）；无辩护者节点合计 **46**（旧值 7）
- 连通分量 11（孤立 4，最大 80）；2-环 194；modify 比例 = 1.0 的 MIS 7

| # | 测试 | 实测断言差异 | 写死位置 |
|---|---|---|---|
| 1 | test_611_tools.py::test_e1_metrics_611 | `out_mis_count` 42 ≠ 7 | 测试 |
| 2 | test_611_tools.py::test_e3_defense_chain_deepen | `nodes_whose_demote_changes_something` 0 ≠ 107 | 测试 |
| 3 | test_argument_audit_610.py::test_detect_no_defender_mis | 42 个 ≠ `['MIS-LANG-001']` | 测试 + `argument_audit.check()` |
| 4 | test_argument_audit_610.py::test_detect_no_defender_nodes_total | 46 ≠ 7 | 测试 + `argument_audit.check()` |
| 5 | test_argument_audit_610.py::test_detect_credibility_gaps | `{high:79,medium:35,low:7}` ≠ `{0,114,7}` | 测试 + `argument_audit.check()` |
| 6 | test_argument_audit_610.py::test_cli_basic_detectors | 同上（`no-defenders` 输出 42 行） | 测试 |
| 7 | test_argument_audit_610.py::test_check_consistency_strict | `argument_audit.check()` 报 3 项 | 工具常量 |
| 8 | test_argument_audit_report_610.py::test_generate_full_report_sections | `IN 114 / OUT 7` + `击败 17` | 测试 |
| 9 | test_argument_audit_report_610.py::test_report_has_p1_vulnerabilities | `无辩护者 1` / `击败边` 等 | 测试 |
| 10 | test_argument_audit_report_610.py::test_summary_json | `p1.no_defender_out_mis` 42 ≠ 1、`totals.defeating_edges` 194 ≠ 17 | 测试 + `summary_json` 写死 totals |
| 11 | test_defense_chain_html_610.py::test_edges_are_rendered_with_correct_weights | 击败边 194 ≠ 17（非击败 194 ≠ 371） | 测试 |
| 12 | test_defense_chain_html_610.py::test_interaction_and_static_fallback | OUT 静态表 42 行 ≠ 7 | 测试 |
| 13 | test_merkle_integrity_601.py::test_tool_integrity_check_includes_merkle | 见 B 类真因（ruler 漂移） | 工具基准 |
| 14 | test_merkle_integrity_601.py::test_tool_integrity_check_red_on_tampered_fake_repo | 同上（首个 assert 前置绿要求） | 工具基准 |

### B 类：工具完整性基准漂移 + 历史门禁（5 项）

**共同真因（不是"当时状态写死"）**：`tools/.tool_checksums` 的 `# ruler` 节里
`defense_chain.py` 的哈希为 `c5f15373106b…`，而磁盘实际为 `b6160a42652b…`。

- 640b 提交 2c50a563 改了 `tools/defense_chain.py`（可信度口径对齐内核），但**同提交的
  `.tool_checksums` 未同步重钉** ⇒ 尺子基准过期。
- 这是**真实完整性漂移**（§六.1），不是"跨批脆弱"：`tool_integrity --check` 的正确语义
  就是"尺子必须与基准一致"，本次是基准没跟上合法改动 ⇒ 修法 = `--update` 重钉（§四.3 正常流程）。

| # | 测试 | 实测 |
|---|---|---|
| 15 | test_ruler_coverage_extension_625.py::test_integrity_check_passes | `ti.main(["--check"])` == 1（ruler 漂移） |
| 16 | test_tool_integrity.py::test_567_check_flag_on_real_repo | 同上（真实仓库 --check 红） |
| 17 | test_tool_integrity_supply_chain_601.py::test_cli_check_and_check_supply_chain_green_on_real_repo | 同上 |
| 18 | test_run_625_gate.py::test_full_gate_passes | 门禁内 `tool_integrity --check` FAIL ⇒ gate FAIL |
| 19 | test_run_639_gate.py::test_static_checks_green | `G.check_tool_integrity()["ok"]` False（同因） |

## 三、清单外发现（本轮新增，登记不混入机械修复）

1. **报告自相矛盾（真 bug）**：`argument_audit.generate_full_report()` 把
   "**无 `high` 可信度节点**" 当作无条件 P0 段落输出，而同函数的 `summary_json()` 已按
   `high == 0` 动态判定（现为 False）。⇒ 现报告打印"分布 {'high': 79, …}"的同时仍声称
   "无 high 档节点"，且 §6 的 `P0 = 2` 是写死值、§7 建议里的 "4 个""7 个" 也是写死文本。
   属**真实不一致**（§零.5），本轮按真因修（条件化 + 动态计数），不放任。
2. **`argument_audit.check()` 名为"自洽校验"实为"快照锁定"**：8 条硬检查里 6 条是和
   写死常量比对，只有"未审边 0"是真正的不变量。⇒ 按 A1 要求改为**不变量 + 跨源
   （现算 vs 入库产物）**校验。
3. **`metrics_611.collect_out_mis()` 命名与语义不符**：`out_mis_count` 实际取的是
   **全部 OUT 节点数**（当前恰好全为 MIS）。⇒ 按 type 过滤（题名一致），并接权威源。
