# 643 E3 · 闭环第 4 次运行（R4）

> 候选 **20**（B5 10 + D2 10）、采纳 **0**（人审未批）、事后验证子集 **20**、兑现 **2** ⇒ **校准度 0.1**。
> 门槛 **60%** ⇒ **未达标**。
> 校准度依据：C4 的定向组 20 条有效候选里，**预期兑现 2 条**（`oracle_hit_rate=0.1`）
> 口径：**可验证子集口径**（预期兑现率）≠ R1/R2/R3 的口径

## 一、R1→R4 四点（**口径各不相同，不可直接连线**）

| 轮次 | 批次 | 候选 | 采纳 | 事后验证 | 校准度 | 口径 |
|---|---|---|---|---|---|---|
| R1 | 637 | 8 | 3 | 8 | **37.5%** | 建议靠谱率（人工逐条打分） |
| R2 | 638 | 4 | 3 | 4 | **50.0%** | 1 − 误报率（异常检出准确率，派生） |
| R3 | 642 | 157 | 0 | 0 | **None** | 未代决 ⇒ 无从验证（**不是 0**） |
| **R4** | **643** | 20 | 0 | 20 | **0.1** | 可验证子集：预期兑现率 |

## 二、本轮替代了什么（inbox 要求）

- 观测器：**B5 issue_dispatcher_643（问题发现器替代静态指标）**；
- 生成器：**C2 targeted_mutator_643（攻击生成器替代方案库）**。

## 三、候选明细（含 637 打分对照）

| 候选 | 来源 | 类别 | 目标 | cost | benefit | 643 score | 637 score |
|---|---|---|---|---|---|---|---|
| `B4:na_capability:N/A 能力不足候选` | B5 | `na_capability` | N/A 能力不足候选 | 2 | 123 | 123.0 | 0.5 |
| `B1:block_rule_zero_hit:共44项` | B5 | `block_rule_zero_hit` | 共44项 | 1 | 44 | 88.0 | 1.0 |
| `B3:rule_inapplicable:共41规则` | B5 | `rule_inapplicable` | 共41规则 | 1 | 41 | 82.0 | 1.0 |
| `B3:rule_dead:共26规则` | B5 | `rule_dead` | 共26规则 | 1 | 26 | 52.0 | 1.0 |
| `B2:attack_structural_only:高风险低深度共14向量` | B5 | `attack_structural_only` | 高风险低深度共14向量 | 1 | 14 | 28.0 | 0.5 |
| `B2:attack_structural_only:共13向量` | B5 | `attack_structural_only` | 共13向量 | 2 | 13 | 13.0 | 0.5 |
| `B2:attack_underrun:共6向量` | B5 | `attack_underrun` | 共6向量 | 2 | 6 | 9.0 | 0.5 |
| `B4:escape_capability:共8案例` | B5 | `escape_capability` | 共8案例 | 1 | 8 | 8.0 | 0.5 |
| `B3:missing_dimension:每规则判决级别统计` | B5 | `missing_dimension` | 每规则判决级别统计 | 2 | 3 | 3.0 | 0.5 |
| `B4:escape_rule_missing:共1案例` | B5 | `escape_rule_missing` | 共1案例 | 2 | 1 | 1.5 | 1.0 |
| `feccc0bd885e` | D2 | `NEW` | ATOM-DRAFT-001 | 2 | 1 | 0.414 | 1.0 |
| `58bde5cd6dbe` | D2 | `MODIFY` | MOD-ATOM-DAL-MATCH | 2 | 1 | 0.296 | 1.5 |
| `2b12c8d7fd97` | D2 | `MODIFY` | MOD-ATOM-GRAY-ZONE | 2 | 1 | 0.296 | 1.5 |
| `733144de59c8` | D2 | `MODIFY` | MOD-ATOM-ID-FORMAT | 2 | 1 | 0.296 | 1.5 |
| `73431a3c9727` | D2 | `MODIFY` | MOD-ATOM-ID-UNIQUE | 2 | 1 | 0.296 | 1.5 |
| `0e0a12193354` | D2 | `MODIFY` | MOD-ATOM-FM-REQUIRED | 2 | 1 | 0.276 | 1.5 |
| `b4871afeacfc` | D2 | `MODIFY` | MOD-ATOM-NO-UNVERIFIED | 2 | 1 | 0.258 | 1.5 |
| `bc05d8f7a3f7` | D2 | `MODIFY` | MOD-ATOM-CLAIM-STRUCTURED | 2 | 1 | 0.235 | 1.5 |
| `701195317873` | D2 | `MODIFY` | MOD-ATOM-MISCONCEPTION-REF | 2 | 1 | 0.229 | 1.5 |
| `893d06b0016c` | D2 | `MODIFY` | MOD-ATOM-MISCONCEPTION-LEVELS | 2 | 1 | 0.211 | 1.5 |

## 诚实登记

1. **R4 的校准度口径与 R1/R2/R3 都不同** ⇒ **不能连成趋势**（642 C2 已登记「口径不同」的坑，本批继续显式标注）；
2. **采纳数 0 是实情**：机器**不代签**，草案与人审项都未获批准 ⇒ 「采纳」一栏为 0 不是失败；
3. **事后验证的是「可验证子集」**（C4 的 20 条）**不是候选全集**（20 条）⇒ 校准度是**子集指标**；
4. **未并入 642 的台账**（`data/642_loop_calibration.json` 属 642 批产物）⇒ R4 写 643 自己的文件，**是否并入交人裁决**；
5. **复用 637 只是纯函数**（`score_one`）：未跑 637 的 observer/detector/memo IO，避免跨批污染与重跑成本；
6. 门槛 60% 是 642 定下的经验值，本工具**不改**它。
