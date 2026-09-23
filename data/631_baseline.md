# 631 任务0 · 开工基线台账

> 工具：`tools/baseline_631.py`（只读）· **不改任何基线数字**（§零.10：不符只标注）

## 一、§一 standing baseline

| 指标 | 值 |
|---|---|
| gate_rules | 67 |
| gate_hits | 191 |
| gate_block | 0 |
| gate_warn | 186 |
| gate_advice | 5 |
| poison | 124/124 |
| replay | confirm=56 refute=0 infra=0 |
| tool_integrity | 22 尺子 |
| w2 | IN114/OUT7/UNDEC0 |
| pck | 83 张，authorized 27/83 |
| authority_v2_ledger | 452 |
| touched | 37/67 |
| escape | 1/1406（CS 0.9062%） |
| autoimmune | 100%（23/23，132 条 warn：auto 42 / human 90） |
| coverage | 16/35 = 45.7%（19 向量从未跑过） |
| ci_pytest | ❌ 红（至少 7 项在 CI 同样成立） |
| head | 1438cd5e |
| remote | 1438cd5e（同步） |

## 二、实测核对（任务书 vs 实测）

| 项 | 任务书 | 实测 | 判定 |
|---|---|---|---|
| HEAD | `1438cd5e` | `1438cd5e` | 一致 |
| 远程 | `1438cd5e（同步）` | `1438cd5e`（ahead=0 / behind=0） | 一致 |
| 干净卡（自身免疫率分母） | 23 | 23 | 一致 |
| 自身免疫率 | 100% | 100.0% | 一致 |
| 其中口径级 | 22 张 | 22 张 | 一致 |
| coverage | 16/35（45.7%） | 16/35 (45.7%) | 一致 |
| 630 冻结的既有失败基线 | — | 12 项 | （631 开工实测 14 项，见 §三） |

## 三、CI pytest 红的失败用例（本地实测）

- 共 **14** 项失败：

| # | 失败用例 |
|---|---|
| 1 | `tests/test_baseline_629.py::test_selftest_and_baseline_failure_freeze` |
| 2 | `tests/test_ci_pytest_fix_625.py::test_governance_manifest_verified` |
| 3 | `tests/test_governance_doc_guard_591.py::test_verify_real_manifest_matches` |
| 4 | `tests/test_governance_self_hash_601.py::test_real_manifest_has_valid_self_hash` |
| 5 | `tests/test_pe_timestamp_caliber_611.py::test_603_capture_untouched_by_this_batch` |
| 6 | `tests/test_pre_push_630.py::test_check_all_ok_and_ahead` |
| 7 | `tests/test_pre_push_checklist_627.py::test_run_all_aggregates_ok` |
| 8 | `tests/test_pre_push_checklist_627.py::test_tools_all_check_pass` |
| 9 | `tests/test_run_628_gate_628.py::test_acceptance_report_exists_and_complete` |
| 10 | `tests/test_run_628_gate_628.py::test_gate_other_steps_pass` |
| 11 | `tests/test_run_629_gate.py::test_gate_other_steps_pass` |
| 12 | `tests/test_run_629_gate.py::test_selftest_passes` |
| 13 | `tests/test_run_629_gate.py::test_tool_manifest_is_complete` |
| 14 | `tests/test_supply_chain_chain_601.py::test_chain_verify_with_real_inspections` |

> 这是 **A1 逐条分类**的输入；分类与根因见 `data/ci_pytest_triage_631.md`。

## 四、额外测量

| 项 | 值 |
|---|---|
| `tools/*.py` | 347 |
| `tests/*.py` | 360 |
| 629 工具 | 10 |
| 630 工具 | 9 |
| 631 工具（本批，随任务增长） | 1 |

### recent commits

```
1438cd5e 630 [E1]：门禁终跑PASS存档（12项既有失败/新增0/基线消失0/受控零污染/push后ahead=0）+验收报告§五回填真实结果与基线11→12来历
ec297396 630 [E1/D2] 终跑修正：629 git facts 断言 62→>=0（push后ahead=0，只改数字）+ 门禁基线并入1项（629工具selftest断言push前ahead，修它越界⇒交人）基线11→12 + 门禁自检同步
c067872d 630 [E1]：status更新（last_completed_batch=630, next_batch=631, awaiting_review）+休工报告
```

## 五、偏差登记（§零.10）

1. **§一 `触达规则 37/67`**：629 台账记 36/67，630 任务书写 37/67（差 1 来自 629 D2 第八轮重跑）。631 沿用 37/67 并标注口径分歧（未裁定）。
2. **CI pytest 失败清单为**本地实测**：CI 端的真实失败集合可能因 `_arch_v2x/` 未跟踪 残留而与本地不同（本地 4 项环境依赖型在 CI 不应成立）；**无 token ⇒ 未取 CI 日志**，630 已登记为缺口，本批沿用。
3. 630 冻结基线 12 项 ↔ 631 开工实测项数若有差异，在 A1 逐条解释（本批正是要修掉其中跨批脆弱型与工具自检过期型）。

## 六、局限

- 只读测量：数字取自 git 与既有工具，**未跑监工四门禁**（§零.1）；
- `gate_hits` 等冻结数字不重测（需 `gate_engine --check`，属监工门禁）；
- 631 工具计数随本批后续任务增长（快照性质）。
