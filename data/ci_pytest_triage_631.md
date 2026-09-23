# 631 A1 · CI pytest 失败用例逐条对齐

> 输入：`data/ci_pytest_raw_631.txt`（631 开工实测）· 共 **14** 项失败

## 一、分类统计

| 分类 | 项数 | 本批处置 |
|---|---|---|
| 跨批脆弱型 | 6 | A2 修断言（本批授权） |
| 工具自检过期型 | 3 | A3 修断言；改工具越界 ⇒ 交人 |
| 环境依赖型 | 5 | 不修（CI 不成立） |
| 真实缺陷型 | 0 | 不修，交人 |
| **合计** | **14** | |

## 二、逐条分类（证据 → 根因 → 修复建议）

### 跨批脆弱型（6 项）

| # | 用例 | 断言证据 | 根因 | 修复建议 |
|---|---|---|---|---|
| 1 | `tests/test_pre_push_630.py::test_check_all_ok_and_ahead` | `—` | 630 B1 的闸门语义是『push 时工作区干净』；但本测试跑在套件里，而套件总会留下本批未提交的新文件（631 工具/测试）⇒ 聚合 all_ok 在套件内必假 | 改断言：不再断言聚合 all_ok，改为断言各分量（受控干净/ci.yml 合法/交付物齐/630 代码无未提交） |
| 2 | `tests/test_run_628_gate_628.py::test_acceptance_report_exists_and_complete` | `—` | 断言 `status['batch'] == 628`；629/630 收工后 status 已推进到 630 | 改单调断言：`status['batch'] >= 628` 且 `last_completed_batch >= 628` |
| 3 | `tests/test_run_628_gate_628.py::test_gate_other_steps_pass` | `—` | 628 门禁内的 `v2_flag_integration_verify_628 --check` 断言『tool_integrity --update 已重钉（628 基准）』；629/630/631 新增工具后该基准过期 | 条件跳过 + 交人（修它要改 628 工具的门禁检查） |
| 4 | `tests/test_run_629_gate.py::test_gate_other_steps_pass` | `—` | 同上（该核验跑在 629 门禁内部，测试只是把它跑起来） | 条件跳过 + 交人（工具侧改法同上，需改 629 门禁 ⇒ 越界） |
| 5 | `tests/test_run_629_gate.py::test_selftest_passes` | `—` | 同上（629 门禁 selftest 含同一核验） | 条件跳过 + 交人 |
| 6 | `tests/test_run_629_gate.py::test_tool_manifest_is_complete` | `—` | 629 门禁用 `git diff BATCH_BASE..HEAD -- tools/` 核验『本批工具无遗漏』；630/631 新增工具被判为『遗漏』 | 改断言：按批次标记 `*_629.py` 核验（630 门禁已用此修正） |

### 工具自检过期型（3 项）

| # | 用例 | 断言证据 | 根因 | 修复建议 |
|---|---|---|---|---|
| 1 | `tests/test_baseline_629.py::test_selftest_and_baseline_failure_freeze` | `—` | 629 工具 `baseline_629.py` 的 selftest 断言『push 前 ahead ≥ 62』；630 B2 完成 push 后 ahead = 0 ⇒ 工具自检过期 | 测试侧：去掉对 `B.selftest()` 的依赖（保留基线计数断言）；工具侧（需改 629 工具 ⇒ §零.11 越界）交人 |
| 2 | `tests/test_pre_push_checklist_627.py::test_run_all_aggregates_ok` | `—` | 同上（627 pre-push 清单聚合依赖该工具自检） | 同上：条件跳过 + 交人 |
| 3 | `tests/test_pre_push_checklist_627.py::test_tools_all_check_pass` | `—` | 627 工具 `pck_hash_drift_analyzer_627 --check` 仍断言 628 之前的状态（实测『无健康证书（全部有缺口）』在 628 A2 修复后已不成立） | 工具自检过期 ⇒ 修它要改 627 工具（§零.11 越界）⇒ 条件跳过 + 交人 |

### 环境依赖型（5 项）

| # | 用例 | 断言证据 | 根因 | 修复建议 |
|---|---|---|---|---|
| 1 | `tests/test_ci_pytest_fix_625.py::test_governance_manifest_verified` | `—` | 治理 manifest 判定『29 处新增』源于本地**未跟踪**的 `_arch_v21/` 并行会话产物 | 不修（CI 检出无这些文件 ⇒ CI 不成立） |
| 2 | `tests/test_governance_doc_guard_591.py::test_verify_real_manifest_matches` | `—` | 同上：`_arch_v2x/` 未跟踪残留使 manifest 比对失败 | 不修（环境依赖型） |
| 3 | `tests/test_governance_self_hash_601.py::test_real_manifest_has_valid_self_hash` | `—` | 同上：manifest 自哈希随未跟踪文件变化 | 不修（环境依赖型） |
| 4 | `tests/test_pe_timestamp_caliber_611.py::test_603_capture_untouched_by_this_batch` | `—` | 603 字节捕获产物是 UTF-16，测试按 UTF-8 解码 ⇒ `UnicodeDecodeError: 'utf-16-le' codec can't decode byte` | 不修（编码/环境依赖型；改断言需理解 611 原始意图 ⇒ 交人） |
| 5 | `tests/test_supply_chain_chain_601.py::test_chain_verify_with_real_inspections` | `—` | 链里含 governance_check，同样被 `_arch_v21/` 未跟踪产物判为『manifest 不一致』 | 不修（环境依赖型） |

## 三、与 630 冻结基线的差额

- 630 冻结基线 **12 项** → 631 开工实测 **14 项**（+2）：
  1. `test_pre_push_630.py::test_check_all_ok_and_ahead`（跨批脆弱型，630 自己引入）；
  2. `test_run_628_gate_628.py::test_gate_other_steps_pass`（628 门禁的 tool_integrity 重钉基准过期）。

## 四、诚实登记

1. **分类里的根因是人读断言后的结论**，写进 `REASONS` 逐条可审；机器只做解析/归类/统计；
2. **环境依赖型在 CI 是否成立无法确证**（无 token ⇒ 未取 CI 日志）：依据是『未跟踪 `_arch_v2x/` 不会进 CI 检出』这一推断；
3. 本批 **A2/A3 只改测试断言**，不改任何 625-630 工具的生产逻辑（§零.11）。
