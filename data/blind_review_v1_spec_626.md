# 626 C1 · Blind Review v1 规范（Pass A 盲审 + Pass B 解盲）

> 工具：`tools/blind_review_v1_626.py`（纯标准库，`--check` 自检）
> 示例：`data/blind_review_example_626.jsonl`（**模拟数据，非真实人审**）
> **根治 P0-C** / 完成判据 3（工具就绪，**执行需人授权**）

---

## 一、为什么需要 Blind Review

如果人第一眼就看到 AI 的推荐，那不是"独立人审"，而是"对 AI 推荐的确认"——
这是 **automation bias**。当前项目独立人类确认强度为 **0**，
Blind Review 是把它变成非 0 的**唯一途径**。

## 二、两阶段设计

### Pass A（盲审）——看不到 AI 推荐

| 字段 | 说明 |
|---|---|
| `decision` | APPROVE / REJECT / MODIFY / ABSTAIN |
| `reason` | 人审理由 |
| `view_digest` | 看到的视图哈希（验证证据内容，可复算比对） |
| `evidence_shown` | 展示给人的证据列表 |
| `ai_recommendation_shown` | **必须 `False`** |
| `elapsed_ms` / `decided_at` | 耗时与时间 |

> **硬保证**：`submit_pass_a(..., ai_recommendation_shown=True)` ⇒ **抛 `ValueError` 拒绝提交**。

### Pass B（解盲）——揭示 AI 推荐并比对

| 字段 | 说明 |
|---|---|
| `ai_recommendation` / `ai_reason` | AI 推荐与理由 |
| `human_decision` | 解盲后人的最终决定 |
| `changed_after_reveal` | 是否改变 |
| `change_reason` | 改变原因 |
| `consistency` | `agree` / `disagree` / `changed` |
| `automation_bias_risk` | `high`（改变）/ `medium`（不一致未改）/ `low`（一致未改） |

**风险判定**：`changed ⇒ high`；否则 `agree ⇒ low`、`disagree ⇒ medium`。

## 三、与 Authority Ledger 的集成（**只提供接口，不自动写入**）

`BlindReviewManager.to_authority_event_kwargs(session_id)` 返回：

```python
{"review_method": "ITEM_BLIND", "decision_origin": "human_observed",
 "result": <Pass A decision>, "blind_review_id": ..., "view_digest": ...,
 "target_type": "edge", "target_id": <review_item_id>}
```

- 这组参数是**唯一**能让 `independent_human_review_count()` 增加的输入。
- **本批不自动写入 Authority Ledger**——需人确认后由人授权写入（不代签）。

## 四、状态机

```
pass_a_pending ──submit_pass_a──▶ pass_a_done ──reveal+submit_pass_b──▶ pass_b_done
```

- 未完成 Pass A 直接解盲 ⇒ 抛错
- 未解盲直接提交 Pass B ⇒ 抛错

## 五、本批边界（诚实声明）

1. **不执行真实 Blind Review**——需要人审者配合；本批只交付工具 + 示例数据。
2. 示例 session（3 条，含 agree/changed/abstain 场景）标注为**模拟数据，非真实人审**，
   不得计入任何"独立人类确认强度"统计。
3. 因此判据 3 的状态为：**工具就绪，待执行**。

## 六、验证

- `blind_review_v1_626.py --check` → PASS（18 项断言）
- `tests/test_blind_review_v1_626.py` → 11 例全绿
