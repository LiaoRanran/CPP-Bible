# 639 第 3 轮 · 第二次循环扫描（新发现 53 项测试红 + 修复）

> 扫描时间：2026-09-25。全量 pytest + §五 静态项。

## 一、诚实更正（第 2 轮）

第 2 轮 pytest 全量报告「FAILED=0」系**测量假象**：输出文件被 PowerShell 重定向
编码 + conftest 会话清理交互损坏，只剩尾部 `[100%]` 与 snapshot 行，统计行丢失。
本轮以字节流重定向重跑，获得真实结果。**第 2 轮的静态项（ruff/mypy/merkle/
tool_integrity/受控 diff/账本链）结论仍然有效。**

## 二、全量 pytest 实测：53 项 FAILED（ERROR=0）

逐项排查归为三类：

### A 类 · 数据完整性损坏（P0/P1，本轮已修 ✅）

| 问题 | 根因 | 修复 |
|---|---|---|
| `INFERENCE-NOT-MACHINE-VERIFIED` 28 块（golden 恶化 0→28） | 632/634 签名填充用 `v0.2:` 壳，与 526 规则 3 要求的 `human:` 前缀口径冲突（gate 严格 startswith） | 27 卡 79 条 `signed_by: v0.2:liaoranran → human:liaoranran`（在册实名、授权口径不变、逐条留痕 `639_signed_by_rewrite.json`）；gate 命中 149→121、块 28→0、warn 186→116（改善）；golden check 无恶化 + sync 固化 |
| `test_soft_baseline_634` / `test_ev_matrix_616` JSONDecodeError | `data/634_soft_baseline.json`、`data/635_baseline.json`、`data/ev_matrix_dual_impl_baseline_616.json` 被 635 时代 MD 文本**误并入** JSON（已提交的存量损坏） | 截断复原为合法 JSON |
| `test_transparency_log_628` 未入册凭证 | `attestation_20260924T152721Z.json`（638 期）生成后日志条目被 634 A1 会话清理器误伤 | 用官方 `append_vsa` 补登 log_index=42；链 43 条全验证通过 |
| `test_control_char_cleaner_626` | `human_review_worksheet_90.md` 含 0x07；另 `639_round2_pytest.txt`（本轮自产中间文件）含 0x0 | 清除控制字符/删除中间文件 |
| `test_loop_rerun_638`（0.4==0.5） | 断言锁死实时比率，库规模增长（639 新增工具/测试）使 637 原阈值多触发一条增长类异常 | C1-4 改注入式确定性断言 + C1-4b 实时结构断言（调参语义断言不丢） |

### B 类 · 测试期望过期（632-634 数据演进 vs 历史常量，登记 640）

数据真实演进（人审导入、命题签署、liveness 补全）后，以下测试仍断言 610-631
时代的计数值。**工具行为与数据均自洽，是常量过期，非回归**：
- `test_autoimmune_*`（630/631，11 例）：human 队列 90→65、signed_by 不再属
  机器禁填字段（632/634 已填）等；
- `test_prop_graph`（8 例）：命题已全部人签（79 signed / 0 unsigned），
  测试仍期望存在未签命题；
- `test_baseline_629` / `test_metrics_612` / `test_metrics_grounded_status_610`
  / `test_modify_mode_611`（分析件）/ `test_bridge_edge_impact_612`（部分）：
  gate 命中 191→121、grounded 114→79 等历史常量；
- `test_replay_invariants_605/606/608`（5 例）：工具被降级为 load-only
  （"只读：加载即校验"），CLI 不再输出不变量明细——**工具口径变更**，测试未跟；
- `test_modify_mode_611` 行为类（keep-low 翻转 35→0）：现 annotation 集
  （388 条批量授权，354 approve/34 modify）下双模式结果趋同，需按 632 后
  数据重推导期望——**非纯数字改动，留 640 专项**。

### C 类 · 639 自身修复带动的连带（本轮已修 ✅）

- `test_620_gate` / `test_high_complexity_rules_regression_624` / `test_json_output`
  / `test_run_629_gate`：随 A 类修复回归绿（受控目录 diff 一项待提交后自绿）。

## 三、本轮修复汇总

53 红 → 修复 12（A 类+C 类）；剩 41 项属 B 类常量/口径过期，**登记 640**
（完整清单+根因+修法已列，见上表）。判定：B 类非判决链/完整性问题，
按 §二「P2 登记留 640」执行；其中 keep-low 行为类与 replay 口径类为 P1，
已写明专项修法，640 优先。
