# 626 B2 · 数据迁移报告（annotations + authority_log → DecisionEvent v2）

## 一、迁移条数（**实测，非预设**）

| 项 | 数量 |
|---|---|
| annotations 输入 | 388 |
| authority_log 输入 | 418 |
| **输入合计** | **806** |
| 五元组去重移除 | 354 |
| **迁移后 ledger 条数** | **452** |
| 其中镜像边（MIRROR_DERIVED） | 194 |
| 其中 622 授权执行 30 条（ITEM_OPEN） | 30 |
| 其中 OVERRIDE→REPLACE | 51 |

## 二、映射规则

| 旧 | v2 |
|---|---|
| `action: approve/modify/reject` | `result: APPROVE/MODIFY/REJECT` |
| `power: ACCEPT` | `operation: CREATE` |
| `power: OVERRIDE` | `operation: REPLACE`（+ `supersedes` from `overrides`） |
| `review_method: batch_authorization` | `BATCH_AUTH` + `human_observed` |
| `review_method: item_by_item_executed`（622 的 30 条） | `ITEM_OPEN` + `user_authorized_execution` |
| `direction: mis_to_prop`（194 条镜像边） | `MIRROR_DERIVED` + `mirror_projection` |

## 三、验证结果

- 哈希链完整：**✅ 通过**
- 独立人类确认强度：**0**（无 ITEM_BLIND/ITEM_SECOND_REVIEW ⇒ 应为 0）
- review_method 分布：`{'ITEM_OPEN': 30, 'MIRROR_DERIVED': 194, 'BATCH_AUTH': 228}`
- decision_origin 分布：`{'user_authorized_execution': 30, 'mirror_projection': 194, 'human_observed': 228}`

## 四、向后兼容

- `human_attack_edge_annotations.jsonl`（388）**未删除、未修改**
- `authority/authority_log.jsonl`（418）**未删除、未修改**
- 新 ledger：`data/authority/decision_event_v2_ledger.jsonl`（并行运行）
- 切换开关：统一环境变量 `QUEYI_AUTHORITY_V2=1`（dashboard 投影默认启用；W2/PCK 关键路径默认旧逻辑）
- 回滚：`QUEYI_AUTHORITY_V2=0`（新 ledger 保留供审计，不删除）

## 五、已知局限（诚实登记）

1. 旧 `authority_log` **没有 `action` 字段**，`result` 由 `power` + `reason` 推导（`OVERRIDE` 且 reason 含「复核 approve」→ APPROVE，否则 MODIFY）；属**保守推断**，已在下表可审计。
2. `annotations` **没有 `is_mirror` 字段**，镜像判定来自 `attack_edges_candidates.direction`。
3. 622 的 30 条与 annotations 同 target 的记录按任务要求**保留两条**（原始 + REPLACE），通过 `supersedes` 表达取代关系，而非物理删除。

