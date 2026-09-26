# 642 A3 · blind_protocol 上岗（新入队判决强制盲化 · 历史只标记不修改）

## 一、上岗流程

| 环节 | 行为 |
|---|---|
| 开单 `open_item()` | `review_method=ITEM_BLIND` ⇒ 注入式盲化 `masked = value + sign × offset` |
| 人审期 `visible_view()` | 只给 `masked` / `residual`，**不含 AI 推荐** |
| 提交后 `reveal_after_human()` | 揭盲（校验可逆）+ 算分歧，**只 staged 不写账本** |
| 非 ITEM_BLIND | 不盲化（BATCH_AUTH / MIRROR_DERIVED / ITEM_OPEN 照旧） |

## 二、盲化演示（新开单）

| 条目 | 方法 | 盲态 | 可见字段 | 揭盲后 |
|---|---|---|---|---|
| `NEW-001` | ITEM_BLIND | 盲 | `blind_state, item_id, masked, residual, review_method` | — |
| `NEW-002` | ITEM_BLIND | 盲 | `blind_state, item_id, masked, residual, review_method` | — |
| `NEW-003` | BATCH_AUTH | 公开 | `ai_recommendation, blind_state, item_id, masked, residual, review_method` | — |

- 已揭盲 1 条（NEW-001：人 40.0 vs AI 35.8）⇒ 分歧率 **1.0**（1/1）
- **无已揭盲条时 `disagreement_rate` 返回 `None`**（不编造）；历史分歧率仍**无法计算**（636 同结论：无盲评基线）

## 三、历史判决扫描（452 条，**只标记不修改**）

- 判决总数：**452**
- **AI 推荐可见（违规）：258** 条（口径：`decision_origin ∈ ('human_observed', 'user_authorized_execution')`）
- 账本字节前后一致：**True**（sha256 `ec8cbf5cca2def3d…`）

| 违规条数 | 处置 |
|---|---|
| 258 | **只标记**（append-only 铁律：不修改、不删除、不回填） |

## 四、误判风险评估 + 回滚方案

| 风险 | 触发条件 | 回滚动作 |
|---|---|---|
| 盲化降低人审吞吐（审者失去 AI 提示） | 人审队列 waiting 增加 / throughput 下降 | 只对**新开单**生效 ⇒ 停止新开 ITEM_BLIND 单即可回到旧流程；已开单可 `reveal_after_human()` 立即揭盲 |
| 协议级盲化非密码学承诺（载荷仍在内存） | 有人直接读 `BlindItem.ai_recommendation` | 真实盲性需前端 + 流程纪律（交人项）；本批不接管前端 |
| 分歧率无历史基线 ⇒ 新开单样本少时不可解读 | 用 1–2 条样本推断盲评收益 | 无已揭盲条时返回 **None**（不编造）；样本充足后再解读 |

## 诚实登记

1. **协议级盲化 ≠ 密码学盲化**：AI 推荐仍在对象载荷里，「不可见」指**人审视图不含它**；真实盲性靠前端 + 流程纪律（交人项）；
2. **历史一字未改**（sha256 前后一致已实测）；258 条违规**只标记**；
3. **分歧率无历史基线**：本批只对新开单可算，样本为 1/1，**不可解读为盲评收益**；
4. 不代签：揭盲结果只 `staged`，不写权威账本；
5. 灰度期**不接管任何人审前端**，新判决是否真走 ITEM_BLIND 由人审流程决定。
