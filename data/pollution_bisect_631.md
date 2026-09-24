# 631 C1 · ATOM-CONC-FENCE-001 污染根因二分定位

- 污染目标：`atoms\conc\ATOM-CONC-FENCE-001.md`（M1「删字段」变异残留：`id:` 行缺失）
- 当前是否已污染：**False**
- 静态疑似候选：**23** 个测试文件

## 一、静态候选（import 沙箱/变异工具 或 字面量提到该卡）

| # | 测试文件 |
|---|---|
| 1 | `tests\test_619_b2.py` |
| 2 | `tests\test_620_a1.py` |
| 3 | `tests\test_620_a2.py` |
| 4 | `tests\test_620_a3.py` |
| 5 | `tests\test_620_a4.py` |
| 6 | `tests\test_620_c2.py` |
| 7 | `tests\test_621_c1.py` |
| 8 | `tests\test_621_c2.py` |
| 9 | `tests\test_621_c3.py` |
| 10 | `tests\test_622_a1.py` |
| 11 | `tests\test_622_a2.py` |
| 12 | `tests\test_622_a3.py` |
| 13 | `tests\test_622_a4.py` |
| 14 | `tests\test_622_c1.py` |
| 15 | `tests\test_argument_audit_610.py` |
| 16 | `tests\test_argument_audit_report_610.py` |
| 17 | `tests\test_autoimmune_auto_fill_631.py` |
| 18 | `tests\test_cross_card_attack_624.py` |
| 19 | `tests\test_defense_chain_610.py` |
| 20 | `tests\test_defense_chain_cli_610.py` |
| 21 | `tests\test_learner_behavior_logger_614.py` |
| 22 | `tests\test_learner_twin_validation_615.py` |
| 23 | `tests\test_weighted_af_solver_596.py` |

## 二、二分过程

> 未执行**自动二分**（`bisect()` 需要每次跑组都稳定复现；本批实测污染**不可复现**，见 §二 执行记录）。

### 真实执行记录（逐组跑后查污染标记）

| 组 | 文件 | rc | 污染 | 备注 |
|---|---|---|---|---|
| 623/624 沙箱候选 | `tests/test_cross_card_attack_624.py`、`tests/test_high_complexity_mutator_623.py`、`tests/test_high_complexity_sandbox_run_623.py` | 0 | **False** | 24 例全过，跑后 `id:` 行仍在 |
| 613/588/601 候选 | `tests/test_bridge_edge_proposal_613.py`、`tests/test_mutation_shape_588.py`、`tests/test_supply_chain_601.py` | 0 | **False** | 44 例全过，跑后 `id:` 行仍在 |
| 622 组复核（630 曾排除，本批再验） | `tests/test_622_a1.py`、`tests/test_622_a2.py`、`tests/test_622_a4.py` | 0 | **False** | 34 例全过，跑后 `id:` 行仍在 |
| 631 两次**全量**非 slow 复跑（任务0 采集 + A4 复跑） | `<tests -m not slow>` | None | **False** | 两次全量结束受控目录均**零污染**（`git status -- atoms evidence` 空） |

## 三、结论：未能复现，未定位到具体测试函数（§十二.2 诚实登记）

1. **已排除**：619/620/621/622 组（630）、623/624 沙箱候选组、613/588/601 组（本批逐组实跑），**均不污染**；631 的**两次全量**跑完受控目录也都**零污染**；
2. **因此自动二分不适用**：`bisect()` 依赖「每组跑完都能稳定判定」，而污染不可复现 ⇒ 二分会在某一步误收缩。工具对此显式返回 `inconclusive`，不谎报定位结果；
3. **最可能的根因假设（有证据支撑，未证实）**：污染源是一个「**在沙箱 apply 之后、restore 之前失败**」的测试。依据三条：
   - 污染形态 = M1 删字段，正是沙箱 `plan_edit` 的算子；
   - 630 那次全量里**有 11-14 项测试失败**（其中既有失败会打断用例流程）；
   - 631 A2/A3 修掉 8 项失败后，**两次全量都不再出现污染**。
   若该假设成立，则修法不是「找某个文件」，而是**结构上保证 restore 不被跳过**（见 C2 防护设计）；
4. 最小范围交付：静态候选 **23** 个文件（§一），其中「真正 import 沙箱/变异工具或 subprocess 驱动它们」的窄集为 `test_622_a1/a2`、`test_622_a4`、`test_cross_card_attack_624`、`test_high_complexity_mutator_623`、`test_high_complexity_sandbox_run_623`、`test_bridge_edge_proposal_613`、`test_mutation_shape_588` —— 逐组实跑**均未复现**。

## 四、诚实登记

- 本工具**不修复**（§七 C1.4）；
- `--check` 只读：不跑 pytest、不写任何文件（除报告由 `--report` 显式生成）；
- 静态候选是**启发式**（按 import 模块名/字面量），可能漏（如动态 import）；
- 根因假设**未证实**：要证实需人为让候选沙箱测试在 apply 后失败并观察残留（本批不做——那需要有目的地破坏测试，属下一批/C2 验证范畴）。
