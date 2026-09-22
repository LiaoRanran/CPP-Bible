# 626 D2 · 投影规则 v0.1（Projection Rules）

> 版本：**v0.1**（受治理，变更须走治理流程）
> 编译器：`tools/authority_projection_compiler_626.py`
> 原则：**唯一方向 Authority → Projection，禁止反向写回**

---

## 一、五种投影

| 投影 | 输入 | 输出 | 默认启用 |
|---|---|---|---|
| **W2** | edge 级 Authority 决定 | `{node: IN/OUT/UNDEC}` + 汇总 | 否（关键路径，需人确认） |
| **PCK** | card/certificate 级 Authority | `{pck_id: {strict, relaxed}}` + authorized 计数 | 否（关键路径） |
| **GOLDEN** | `warn_disposition` 级 Authority | warn 分类 / accepted_legacy 计数 | 是（展示） |
| **DASHBOARD** | 全部 Authority + ReviewItem 账本 | 进度 / 分布 / 独立确认强度 | **是（默认 V2）** |
| **TEXTBOOK** | PCK + W2 投影 | 每个知识点的渲染状态 | 是（展示） |

## 二、W2 投影规则（v0.1）

1. `result=APPROVE` 的 edge ⇒ **攻击成立**（攻击者击败目标）
2. `REJECT/MODIFY/ABSTAIN` ⇒ 攻击不成立/存疑，**不产生击败**
3. grounded 迭代至不动点：
   - 存在 `IN` 的攻击者 ⇒ 目标 `OUT`
   - 所有攻击者均为 `OUT` ⇒ 目标 `IN`
   - 无攻击者 ⇒ `IN`
4. 其余 ⇒ `UNDEC`

> ⚠ **已知偏差**：节点粒度为 `edge_id`（含 `::prop-N`），与现有 `grounded_labels_w2.json`
> 的「命题/MIS」级粒度不同 ⇒ **数值未对齐**，留 627 做节点归一化。

## 三、PCK 聚合策略（v0.1）

### 严格策略（默认）`v0.1-strict`

```
CARD_APPROVED ⟺ 每个 material claim 有直接 evidence authority
             ∧ 每个 critical negative test 有 verified result
             ∧ 无未解决矛盾
             ∧ 有 card-level human authority
```

### 宽松策略 `v0.1-relaxed`

```
CARD_APPROVED ⟺ 无未解决矛盾 ∧ 有 card-level human authority
```

报告**同时列出两种策略的 authorized 数量与差异**。

> **实测**：83 张 PCK，严格 0 / 宽松 0 / 差异 0 —— 因为 ledger 中**无 card-level authority 事件**
> （452 条全是 edge 级）⇒ 判据 7「edge→card 不自动授权升级」生效。

## 四、GOLDEN 投影规则（v0.1）

**核心：不自动采纳 legacy。**

- 任何自动采纳 legacy 的路径必须关闭
- 只有 Authority event（`result=APPROVE` ∧ `target_type=warn_disposition` ∧ `scope=accept_legacy`）
  才能把 warn 标记为 `accepted_legacy`
- 分类：real / false_positive / accepted_legacy / needs_rule_change

## 五、DASHBOARD 投影规则（v0.1）

统计项：
- 人审进度（`by_status`: pending/in_review/decided/superseded/invalid）
- `review_method` 分布（BATCH_AUTH / MIRROR_DERIVED / ITEM_OPEN / ITEM_BLIND / ITEM_SECOND_REVIEW）
- `decision_origin` 分布（human_observed / user_authorized_execution / machine_projection / mirror_projection）
- 歧义度分布（high ≥0.8 / medium ≥0.5 / low）
- **独立人类确认强度**（ITEM_BLIND 及以上 + human_observed）
- 人机一致性（Blind Review 的 agree/disagree/changed）

**默认启用 V2**（只影响展示）。

## 六、TEXTBOOK 投影规则（v0.1）

| 状态 | 条件 |
|---|---|
| `CERTIFIED` | PCK authorized ∧ W2 IN ∧ 无未解决矛盾 |
| `CONDITIONALLY_VERIFIED` | PCK authorized 但有条件（如部分 claim 未验证） |
| `ABSTAIN` | PCK pending 或 W2 UNDEC |
| `DISPUTED` | W2 OUT 或有未解决矛盾 |
| `UNVERIFIED` | 无 PCK 且无 Authority |

> **只读投影**：不修改 `atoms/`、`evidence/`、`Book/` 受控目录。

## 七、通用保证

| 保证 | 机制 |
|---|---|
| 只读 | 编译器不提供写 ledger 的方法；`--check` 断言编译后 ledger 不变且链有效 |
| 确定性 | `verify_determinism()`：两次编译的 SHA-256 摘要一致 |
| 可追溯 | 每个投影结果带 `source_authority_events`；`trace_projection()` 可反查 event_id |

## 八、feature flag

统一环境变量 **`QUEYI_AUTHORITY_V2`**：
- `dashboard` 路径默认启用 V2
- `W2` / `PCK` 关键路径默认旧逻辑（向后兼容）
- 回滚：`QUEYI_AUTHORITY_V2=0`

## 九、验证

- `--check` → PASS
- `tests/test_projection_extended_626.py` → 11 例全绿
