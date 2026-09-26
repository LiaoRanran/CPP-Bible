# 647 D2 · 合并后接口统一验证（10 个核心工具）

- 现存核心工具：**10**（646 B4 计划 15 → 10，**647 D1 已执行**）
- 全部符合 645 D2 接口规范：**True**

## 一、合并前后对比

| 组 | 合并前成员 | 合并后目标 | 保留入口 | 成员文件已删除 |
|---|---|---|---|---|
| 耦合编排 + 反馈 + 效果评估 | three_layer_orchestrator_645, coupling_feedback_645, coupling_effect_645 | `three_layer_orchestrator_645` | `generate_feedback`, `evaluate`, `write_effect_report` | True |
| 证据等级 + 充分性 | evidence_grading_645, evidence_sufficiency_645 | `evidence_grading_645` | `judge`, `write_sufficiency_report` | True |
| R5 闭环 + error + 老化 | loop_r5_runner_645, rule_error_tracker_645, rule_aging_detector_645 | `loop_r5_runner_645` | `track`, `detect`, `load_ledger`, `write_error_report`, `write_aging_report` | True |

## 二、逐工具接口检查

| 工具 | docstring | main | selftest | `--check` 标志 | `--check` 退出码 | 报告路径在 data | 合规 |
|---|---|---|---|---|---|---|---|
| `smart_issue_finder_645` | True | True | True | True | 0 | True | ✅ |
| `targeted_attacker_645` | True | True | True | True | 0 | True | ✅ |
| `rule_drafter_645` | True | True | True | True | 0 | True | ✅ |
| `loop_r5_runner_645` | True | True | True | True | 0 | True | ✅ |
| `rule_card_mapper_646` | True | True | True | True | 0 | True | ✅ |
| `standard_fetcher_645` | True | True | True | True | 0 | True | ✅ |
| `compiler_probe_645` | True | True | True | True | 0 | True | ✅ |
| `counterexample_searcher_645` | True | True | True | True | 0 | True | ✅ |
| `evidence_grading_645` | True | True | True | True | 0 | True | ✅ |
| `three_layer_orchestrator_645` | True | True | True | True | 0 | True | ✅ |

## 三、合并无损验证（入口仍可调用）

| 目标模块 | 保留入口 | 缺失入口 | 通过 |
|---|---|---|---|
| `three_layer_orchestrator_645` | `generate_feedback`, `evaluate`, `write_effect_report` | — | ✅ |
| `evidence_grading_645` | `judge`, `write_sufficiency_report` | — | ✅ |
| `loop_r5_runner_645` | `track`, `detect`, `load_ledger`, `write_error_report`, `write_aging_report` | — | ✅ |

## 诚实登记

1. **合并是「文件组织」层面的**：被并入的成员代码**原样搬进**目标模块，只把 `write_report`/`selftest`/`main` 等会冲突的名字**重命名**（如 `write_effect_report`）⇒ 功能等价、测试逐条复用；
2. **同步改了测试 import**（646 自己就说了「执行合并需同步改测试」）；另外两个 646 工具（`tool_consolidation_646` / `docstring_quality_646`）改成**感知合并后状态**（现存 10 / 缺失成员自动跳过），并同步其单测；
3. **`--check` 是真跑的**（subprocess，300s 超时），不是纸面检查；
4. 本模块**只验证不改代码**。
