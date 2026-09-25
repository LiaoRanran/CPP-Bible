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
| HEAD | `1438cd5e` | `48485622` | **不符**（实测 48485622） |
| 远程 | `1438cd5e（同步）` | `33e02efb`（ahead=10 / behind=0） | **不符**（实测 33e02efb） |
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
| `tools/*.py` | 375 |
| `tests/*.py` | 388 |
| 629 工具 | 10 |
| 630 工具 | 9 |
| 631 工具（本批，随任务增长） | 10 |

### recent commits

```
48485622 633 [E1]：测试债深化分类与长期方案(不改测试)——slow 6/跨批脆弱30/环境依赖117/快照25(针对A2后剩余54项),给动态基线读/conftest统一skipif/快照触发更新/slow分层四方案设计;--check只读+6例单测
7e838b10 633 [D2]：文档债清理——修306文档3处裸文件名死链接(改为../../atoms/mem/实际路径,已核实目标存在);368的6处file://为假阳性不改;过期标注0处;登记.pytest_tmp残留652目录(不删)与扫描器file://口径;矛盾描述登记不改
6694b291 633 [D1]：PCK/镜像边/ref_missing 交人项整理——统一清单+P1-P4优先级+处置建议+依赖;登记627/628 ref_missing口径出入(2 vs 1)待核;不代签不自动填充;镜像边194全自动证明其中118条缺ReviewItem属治理决策;PCK authorized 27/83
```

## 五、偏差登记（§零.10）

1. **§一 `触达规则 37/67`**：629 台账记 36/67，630 任务书写 37/67（差 1 来自 629 D2 第八轮重跑）。631 沿用 37/67 并标注口径分歧（未裁定）。
2. **CI pytest 失败清单为**本地实测**：CI 端的真实失败集合可能因 `_arch_v2x/` 未跟踪 残留而与本地不同（本地 4 项环境依赖型在 CI 不应成立）；**无 token ⇒ 未取 CI 日志**，630 已登记为缺口，本批沿用。
3. 630 冻结基线 12 项 ↔ 631 开工实测项数若有差异，在 A1 逐条解释（本批正是要修掉其中跨批脆弱型与工具自检过期型）。

## 六、局限

- 只读测量：数字取自 git 与既有工具，**未跑监工四门禁**（§零.1）；
- `gate_hits` 等冻结数字不重测（需 `gate_engine --check`，属监工门禁）；
- 631 工具计数随本批后续任务增长（快照性质）。


## 边界三元组 + v26 补充字段（635 1.1 回填）

- `mutation_set_hash`: `d7556d622e92fbf918cf9b49c39d97da0733c88fb686be7e734df7fca294ac57`
- `mutation_count`: 1593
- `generator_version`: `mutation_fuzz@v7`
- `evidence_channel`: `standard_textbook`
- `materiality_flag`: true


## 635 V26-2 系统误差二分（不可合并为单一健康分）

**可收敛指标**（加样本可改善）：
- 逃逸率：多测 mutation 可更准确估计漏报率（统计量）
- τ_d（逃逸→修补间隔）：样本量增加可收紧分位数
- 接地覆盖率：可补实验把「部分/未接地」转「已接地」
- 工具数/测试数：持续增加

**不可收敛指标**（加样本无效，须换方法）：
- coverage 缺口：剩下的是**没测过的攻击面**，不是测不准
- 自身免疫率：是**规则设计问题**，不是样本问题
- Horizon 断崖（60-80 桶）：是**载体天花板**，不是样本量
- N/A 率：主因是载体无法施加（634 B3），加样本无效
- gate 规则数：是**设计选择**，非估计量
