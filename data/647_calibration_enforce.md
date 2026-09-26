# 647 B4 · 校准追踪器**真上岗**（error_rate > 20% 降级 warn / > 50% 暂停）

- 当前模式：**enforce**（enforce = 真降级/真暂停；shadow = 642 观察态，只记账）
- 阈值：降级 **> 0.2** · 暂停 **> 0.5**（均**设计值**）
- 数据来路：`data/646_authority_rule_annotation.jsonl`（452 条）**×** 账本 `result` 连表

## 一、实测（逐规则样本，**647 首次做到**）

- 在册规则：**67**；**有实测样本：67**；
- 动作分布：`{'ok': 62, 'suspended': 2, 'degraded_warn': 3}`
- 与 642 的差别：642 的 67/67 是**全库代理**（同值）；647 是**逐规则实测**（来自注释×账本）。

### 1.1 error_rate 最高的 5 条规则

| 规则 | total | error | rate | 动作 |
|---|---|---|---|---|
| `ATOM-NO-UNVERIFIED` | 15 | 15 | 1.0 | suspended |
| `ATOM-GRAY-ZONE` | 64 | 40 | 0.625 | suspended |
| `ATOM-MISCONCEPTION-LEVELS` | 57 | 15 | 0.2632 | degraded_warn |
| `ATOM-MISCONCEPTION-REF` | 57 | 15 | 0.2632 | degraded_warn |
| `PED-MISCONCEPTION` | 57 | 15 | 0.2632 | degraded_warn |

### 1.2 被降级/暂停的规则（真实数据）

| 规则 | rate | 动作 | 理由 |
|---|---|---|---|
| `ATOM-NO-UNVERIFIED` | 1.0 | **suspended** | error_rate 1.0 > 0.5 ⇒ 暂停（恢复需人审） |
| `ATOM-GRAY-ZONE` | 0.625 | **suspended** | error_rate 0.625 > 0.5 ⇒ 暂停（恢复需人审） |
| `ATOM-MISCONCEPTION-LEVELS` | 0.2632 | **degraded_warn** | error_rate 0.2632 > 0.2 ⇒ 降级为 warn |
| `ATOM-MISCONCEPTION-REF` | 0.2632 | **degraded_warn** | error_rate 0.2632 > 0.2 ⇒ 降级为 warn |
| `PED-MISCONCEPTION` | 0.2632 | **degraded_warn** | error_rate 0.2632 > 0.2 ⇒ 降级为 warn |

## 二、合成数据验证两条阈值

| 规则 | error_rate | 期望 | 实测 | active | 生效严重度 | 通过 |
|---|---|---|---|---|---|---|
| `R-OK` | 0.2 | ok | **ok** | True | block | ✅ |
| `R-DEG` | 0.21 | degraded_warn | **degraded_warn** | True | warn | ✅ |
| `R-SUS` | 0.51 | suspended | **suspended** | False | off | ✅ |
| `R-SUS` | 0.51 | suspended(不改动作) | **suspended** | True | block | ✅ |

## 三、暂停状态与恢复（恢复必须人审）

- 显式暂停清单：`（空）`
- 操作历史：0 条
- `restore()` 未带 `human_authorized=True` ⇒ **抛 `HumanReviewRequired`**（机器不得自行解停）

## 四、误判风险评估 + 回滚方案

| 风险 | 触发条件 | 回滚动作 |
|---|---|---|
| 把 `MODIFY` 当「规则错」是**口径近似**（也可能是人改口径） | 大量规则被降级/暂停，人工复核发现规则本身没问题 | `QUEYI_PROTECTOR_MODE=shadow` 一键退回观察态（只记账不改动作） |
| **暂停规则 = 该规则不再拦** ⇒ 可能放行真实攻击 | 被暂停规则对应真实逃逸样本 | `restore(rule_id, by=..., human_authorized=True)` 人审恢复；或调低 THETA_SUSPEND |
| 阈值 0.20/0.50 是**设计值** | 降级清单与人工判断严重不符 | 改两个常量后重跑（单点配置） |

## 诚实登记

1. **`MODIFY` ≠ 规则错**：人改判可能是改口径 ⇒ rate 是**近似**；
2. **真实数据无 >0.50 规则** ⇒ 暂停分支未被真实数据触发，由**合成数据**验证；
3. **阈值 0.20/0.50 是设计值**，未用历史回填；
4. **暂停是真的**：enforce 下 `active=False`（规则不生效）——这是 647 与 642 的行为差别；
5. 无实测样本的规则**不改动**（不把「没数据」当「没问题」）。
