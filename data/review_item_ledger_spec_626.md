# 626 B3 · 唯一审查账本规范（93 unique，**禁止重复计数**）

> 工具：`tools/review_item_ledger_626.py`（纯标准库，`--check` 自检）
> 账本：`data/review_item_ledger.jsonl`
> **根治 P0-B** / 完成判据 2

---

## 一、问题

624 E2 生成 80 条新清单，与 615 的 30 条合计被表述为「110 条待审」。
实测：**110 只是记录条数**，其中 **17 条完全重复** ⇒ 唯一复核对象 = **93**。

| 项 | 数量 |
|---|---|
| 615 清单唯一 edge ID | 30 |
| 624 清单唯一 edge ID | 80 |
| 两者 overlap | **17** |
| **唯一复核对象（union）** | **93** |
| 记录条数（30 + 80） | 110 |

## 二、数据结构

| 字段 | 说明 |
|---|---|
| `review_item_id` | `RI-<target_type>-<target_id>`；revision > 1 追加 `-r<N>` ⇒ **全局唯一** |
| `review_revision` | 从 1 开始；同一 target 的再次审查递增 |
| `target_type` / `target_id` / `target_revision` | 审查目标 |
| `first_seen_at` / `last_seen_at` | 首次/最近出现时间 |
| `symmetry_proof_id` | 镜像边对称性证明 ID（**默认空 = 未验证**；C2 使用，B3 只预留字段） |
| `supersedes` | 被取代的 review_item_id |
| `status` | pending / in_review / decided / superseded / invalid |
| `current_decision_id` | 当前决定的 Authority event_id |
| `ambiguity_score` | 歧义度 0-1 |
| `priority` | high / medium / low |
| `source_batch` | 首次生成批次（overlap 项标 `615+624`） |
| `tags` | 标签（migrated / from_615 / from_624 / overlap） |

## 三、唯一性规则

1. `review_item_id` **全局唯一**（revision 编码进 ID）。
2. 同一 `target_id` 的多次审查 = 不同的 `review_revision`，旧的被 `supersedes`。
3. `add()` 遇到已存在**且 `status=pending`** 的 target：**不新建**，只更新 `last_seen_at` 并合并 `source_batch`。
4. `verify_uniqueness()`：不存在重复 target 的 pending item。

## 四、迁移结果（实测）

```
from_615 = 30, from_624 = 80, overlap = 17
records  = 110        # 记录条数
unique   = 93         # 唯一复核对象  ← 审计口径以此为准
ledger_records = 93   # 账本 item 数（17 条重复被合并，未新建）
pending  = 93
```

17 条 overlap 项：`source_batch = "615+624"`，`ambiguity_score = 0.9`，`tags` 含 `overlap`。

## 五、与 Authority Ledger 的关系

- 审查完成 ⇒ `mark_decided(review_item_id, decision_event_id)`，
  `current_decision_id` 指向 **Authority Ledger 的 event_id**（626 B1/B2）。
- 账本**只记录"要审什么"**，Authority Ledger **记录"决定了什么"**——两者分离，不互相替代。

## 六、验证

- `review_item_ledger_626.py --check` → PASS（16 项断言）
- `tests/test_review_item_ledger_626.py` → 9 例全绿
- 唯一性验证通过；导出/导入往返一致
