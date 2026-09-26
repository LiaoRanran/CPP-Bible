# 647 B3 · blind_protocol **真上岗**（新判决强制盲化；历史只标记不回溯）

- 当前模式：**enforce**（enforce = **所有新判决强制 ITEM_BLIND**；shadow = 642 行为，仅 ITEM_BLIND 盲化）
- 强制方法：`ITEM_BLIND`；人审期读 AI 推荐 ⇒ **`BlindViolation`**（不返回 None）

## 一、新判决实跑（3 条，请求了 3 种不同方法）

- 生效方法分布：`{'ITEM_BLIND': 3}`；被盲化：**3/3**
- 已揭盲 1 条 ⇒ 分歧率 **1.0**（样本 1，**不可解读为盲评收益**）

| 条目 | 请求方法 | 生效方法 | 盲态 | 可见字段 | enforce |
|---|---|---|---|---|---|
| `NEW-001` | BATCH_AUTH | **ITEM_BLIND** | REVEALED | `ai_recommendation, blind_state, item_id, masked, residual, review_method` | True |
| `NEW-002` | ITEM_OPEN | **ITEM_BLIND** | BLIND | `blind_state, item_id, masked, residual, review_method` | True |
| `NEW-003` | ITEM_BLIND | **ITEM_BLIND** | BLIND | `blind_state, item_id, masked, residual, review_method` | True |

### 1.1 enforce vs shadow 对照（同一调用）

| 模式 | 生效方法分布 | 被盲化 |
|---|---|---|
| **enforce** | `{'ITEM_BLIND': 3}` | 3/3 |
| shadow（回滚态） | `{'BATCH_AUTH': 1, 'ITEM_BLIND': 1}` | 1/2 |

## 二、历史判决（**不回溯、只标记**）

- 判决总数：**452**；AI 可见（违规）：**258** 条
- 账本字节前后一致：**True**（sha256 `ec8cbf5cca2def3d…`）
- 处置：不回溯、只标记（append-only）

## 三、误判风险评估 + 回滚方案

| 风险 | 触发条件 | 回滚动作 |
|---|---|---|
| 强制盲化降低人审吞吐（审者失去 AI 提示） | 人审队列 waiting 增加 / throughput 下降 | `QUEYI_PROTECTOR_MODE=shadow` ⇒ 只有 ITEM_BLIND 才盲化（642 行为） |
| 协议级盲化**不是密码学盲化**（载荷在内存里，能绕过封装读属性） | 有人直接访问 `Judgment.item.ai_recommendation` | 真实盲性需前端 + 流程纪律（交人项）；本模块只保证「正常路径拿不到」 |
| 强制盲化对**所有**新判决生效 ⇒ 连 BATCH_AUTH 批量流程也被改 | 批量授权流程被盲化阻塞 | shadow 一键回滚；或仅对指定方法强制（需人裁决口径） |

## 诚实登记

1. **协议级盲化 ≠ 密码学盲化**：载荷仍在内存；`recommendation()` 的拒绝是**流程纪律**；
2. **历史一字未改**（642 已实测 sha256 前后一致）；258 条违规**只标记**；
3. **分歧率样本 1/1 ⇒ 不可解读**为盲评收益（无历史基线，不编造）；
4. **强制盲化扩到了所有新判决**（含 BATCH_AUTH）——这是 647 与 642 的行为差别，也是风险点；
5. 揭盲结果只 `staged`/内存，**不写权威账本、不代签**。
