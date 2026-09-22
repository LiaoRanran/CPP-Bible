# 626 A3 · Authority Schema v2（`review_method` 五级 + `decision_origin` 四级）

> 工具：`tools/authority_schema_v2_626.py`（纯标准库，`--check` 自检）
> **根治 P0-A**：把「人类判断」和「人类授权执行」彻底拆成两个概念。

---

## 一、为什么必须拆

原 schema 只有一维 `review_method`：`batch_authorization | item_by_item_executed`。
这导致「人授权流程执行了 30 条」被**误计为**「30 条独立人类语义审查」——
而事实是：这 30 条的理由**全部模板化**，文档自述「未新增任何人工判断」。

626 的做法是把它拆成**两个正交维度**：

- **`review_method`**（方法）：人是怎么审的？（五级）
- **`decision_origin`**（来源）：这个决定实际来自谁？（四级）

## 二、`review_method` 五级

| 级别 | 含义 | 计入独立人类确认 |
|---|---|---|
| `BATCH_AUTH` | 批量授权（一人 + 模板 + 分钟级） | ❌ |
| `MIRROR_DERIVED` | 镜像边派生（由对称关系自动派生，未独立审查） | ❌ |
| `ITEM_OPEN` | 逐条开放式审查（**看得到** AI 推荐 ⇒ 有 automation bias 风险） | ❌ |
| `ITEM_BLIND` | 逐条盲审（**看不到** AI 推荐） | ✅ |
| `ITEM_SECOND_REVIEW` | 二次复核（对已有决定再审查一次） | ✅ |

## 三、`decision_origin` 四级

| 值 | 含义 |
|---|---|
| `human_observed` | 人真实观察证据后判断 |
| `user_authorized_execution` | 用户授权执行（流程代落，人未逐条判断） |
| `machine_projection` | 机器投影（由 Authority 派生视图推出） |
| `mirror_projection` | 镜像投影（由对称关系推出） |

## 四、独立人类确认强度（判据 1 的核心）

```
is_independent_human_review(m, o) ⟺
    m ∈ {ITEM_BLIND, ITEM_SECOND_REVIEW}  且  o == human_observed
```

| 组合 | 是否计入 |
|---|---|
| `ITEM_OPEN` + `user_authorized_execution`（**622 的 30 条**） | ❌ |
| `BATCH_AUTH` + `human_observed`（388 条批量授权） | ❌ |
| `MIRROR_DERIVED` + `mirror_projection`（194 条镜像边） | ❌ |
| `ITEM_BLIND` + `human_observed` | ✅ |
| `ITEM_SECOND_REVIEW` + `human_observed` | ✅ |

⇒ **当前独立人类确认强度 = 0 条**（622 的 30 条不计入）。这是本项目当前最大的诚信缺口，
只能通过 **Blind Review（626 C1）** 由人真实执行后才会变为非 0。

## 五、与 `operation` / `result` 的关系（P0-D）

`review_method` 描述**怎么审**，`operation`/`result` 描述**做了什么操作、得到什么结果**：

| 维度 | 取值 |
|---|---|
| `operation` | `CREATE` / `REPLACE` / `REVOKE` |
| `result` | `APPROVE` / `REJECT` / `MODIFY` / `ABSTAIN` |

旧 `power: OVERRIDE` 是「操作+结果」合一的坏设计 ⇒ 映射为 `operation: REPLACE` + 具体 `result`（见 626 C2）。

## 六、旧 → v2 兼容映射

| 旧值 | v2 |
|---|---|
| `review_method: batch_authorization` | `BATCH_AUTH` |
| `review_method: item_by_item_executed` | `ITEM_OPEN` |
| `power: ACCEPT` | `operation: CREATE` |
| `power: OVERRIDE` | `operation: REPLACE` |
| `power: REVOKE` | `operation: REVOKE` |
| `action: approve/modify/reject` | `result: APPROVE/MODIFY/REJECT` |

未知旧值一律**保守**映射为 `BATCH_AUTH`（不夸大审查强度）。

## 七、验证

- `tools/authority_schema_v2_626.py --check` → PASS（12 项断言，含「622 的 30 条不计独立」）
- `tests/test_authority_schema_v2_626.py` → 7 例全绿
- 原始 JSONL 数据**未修改**（append-only）
