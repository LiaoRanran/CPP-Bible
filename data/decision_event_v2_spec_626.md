# 626 B1 · DecisionEvent v2 设计规范（Authority 单一真源核心）

> 工具：`tools/decision_event_v2_626.py`（纯标准库，`--check` 自检 30+ 项断言）
> 定位：**只有 Authority Ledger 有「人决定了什么」的权力**；W2 / PCK / golden / dashboard / textbook 全部是**派生视图**。

---

## 一、为什么需要 DecisionEvent v2

旧结构把三件事混在一个 `power` 字段里：

```
power: OVERRIDE  ── 既表示「操作=替换」，又表示「结果=通过」，还隐含「这是人审」
```

后果：`OVERRIDE` 无法回答"替换成了什么"；`item_by_item_executed` 被误当成"独立人审"。

v2 的做法：**正交拆分**

| 维度 | 取值 | 回答的问题 |
|---|---|---|
| `operation` | `CREATE` / `REPLACE` / `REVOKE` | 做了什么**操作** |
| `result` | `APPROVE` / `REJECT` / `MODIFY` / `ABSTAIN` | 得到什么**结果** |
| `review_method` | 五级 | **怎么审**的 |
| `decision_origin` | 四级 | 决定**来自谁** |

## 二、完整 schema（26 字段）

| 字段 | 类型 | 说明 |
|---|---|---|
| `event_id` | str | `AE-<seq>-<short_hash>`（由 self_hash 派生） |
| `seq` | int | 单调递增，从 1 开始 |
| `operation` | str | CREATE / REPLACE / REVOKE |
| `result` | str | APPROVE / REJECT / MODIFY / ABSTAIN |
| `supersedes` | list | 被取代的 event_id（REPLACE 必填） |
| `target_type` | str | edge / card / certificate / rule / golden_policy / warn_disposition |
| `target_id` | str | 目标 ID |
| `target_revision` | str | 目标 revision |
| `scope` | str | single_edge / card_all_claims / certificate_full |
| `confidence` | str | low / medium / high |
| `modification` | str | result=MODIFY 时的修改内容（**必填**） |
| `abstain_reason` | str | result=ABSTAIN 时的原因（**必填**） |
| `review_method` | str | BATCH_AUTH / MIRROR_DERIVED / ITEM_OPEN / ITEM_BLIND / ITEM_SECOND_REVIEW |
| `decision_origin` | str | human_observed / user_authorized_execution / machine_projection / mirror_projection |
| `blind_review_id` | str | Blind Review 关联 ID |
| `basis_refs` | list | 决定依据引用 |
| `view_digest` | str | 审查者看到的视图哈希 |
| `source_digest` | str | 源数据哈希 |
| `reviewer` | str | 审查者标识 |
| `decided_at` | str | ISO 8601 |
| `elapsed_ms` | int | 审查耗时 |
| `aggregation_policy_ref` | str | 聚合策略版本 |
| `cross_granularity_warning` | str | 跨粒度授权警告（判据 7） |
| `prev_hash` | str | 前一 event 的 SHA-256（首条为 `GENESIS`） |
| `self_hash` | str | 本 event 的 SHA-256 |

## 三、哈希链

```
payload    = JSON(所有字段 − {self_hash, event_id})   # 排序键，ensure_ascii=False
self_hash  = SHA256(prev_hash + "|" + payload)
event_id   = AE-{seq:06d}-{self_hash[:8]}
```

> **关键实现细节**：`event_id` 由 `self_hash` 派生，故**必须从 payload 中排除**，
> 否则构成循环依赖，且导出/导入往返后重算哈希会不一致（B1 自测已捕获并修复此 bug）。

## 四、AuthorityLedger（append-only）

| 方法 | 说明 |
|---|---|
| `append(event) -> str` | 追加（校验 + 分配 seq/prev_hash/event_id/self_hash），返回 self_hash |
| `get(event_id)` | 按 ID 查询 |
| `get_current(target_type, target_id)` | 当前有效决定（排除被 supersede 的） |
| `get_all(target_type, target_id)` | 目标全部历史决定 |
| `verify_chain() -> bool` | 哈希链完整性 |
| `export_jsonl(path)` / `import_jsonl(path)` | 往返 IO |
| `count_by_review_method()` / `count_by_decision_origin()` | 统计 |
| `independent_human_review_count()` | **独立人类确认强度** |

> **append-only**：刻意**不提供** `update` / `delete`（自测断言其不存在）。

## 五、校验规则（append 时强制）

1. `review_method` / `decision_origin` / `operation` / `result` 必须在枚举内
2. `target_id` 必填
3. `result=MODIFY` ⇒ `modification` 必填
4. `result=ABSTAIN` ⇒ `abstain_reason` 必填
5. **`operation=REPLACE` ⇒ `supersedes` 必填**（P0-D / 判据 5）

违反 ⇒ `append` 抛 `ValueError`，账本不变。

## 六、与旧 schema 的兼容映射

| 旧 | v2 |
|---|---|
| `power: ACCEPT` | `operation: CREATE` |
| `power: OVERRIDE` | `operation: REPLACE` + `supersedes` |
| `action: approve/modify/reject` | `result: APPROVE/MODIFY/REJECT` |
| `review_method: batch_authorization` | `BATCH_AUTH` |
| `review_method: item_by_item_executed` | `ITEM_OPEN` + `decision_origin: user_authorized_execution` |
| 镜像边（`kind` 派生） | `MIRROR_DERIVED` + `mirror_projection` |

## 七、迁移计划（626 B2）

1. 只读 `human_attack_edge_annotations.jsonl`（388）+ `authority_log.jsonl`（418）
2. 按 `decided_at` 升序分配 seq（同刻：annotations 先、authority_log 后）
3. 五元组去重；622 的 30 条与 annotations 同 target 者视为重复 ⇒ 标注 `supersedes`
4. 输出到 `data/authority/decision_event_v2_ledger.jsonl`
5. **旧文件不删不改**（append-only + 向后兼容）
