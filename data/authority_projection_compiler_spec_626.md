# 626 D1 · Authority → Projection Compiler 规范（**唯一方向，禁止反向**）

> 工具：`tools/authority_projection_compiler_626.py`（纯标准库，`--check` 自检）
> 判据：6（Authority 是唯一裁定真源）、7（edge→card 不自动授权升级）

---

## 一、核心原则

```
Authority Ledger ──▶ Projection Compiler ──▶ {W2, PCK, GOLDEN, DASHBOARD, TEXTBOOK}
        ▲                                            │
        └──────────── 禁止反向写回 ───────────────────┘
```

- **只有 Authority Ledger 有「人决定了什么」的权力**
- W2 / PCK / golden / dashboard / textbook 全部是**派生视图**，不再各自拥有独立权威
- 编译器**只读** ledger，`--check` 断言编译后 ledger 条数不变且哈希链仍有效

## 二、三类保证

| 保证 | 实现 | 验证 |
|---|---|---|
| **只读** | 不提供任何写 ledger 的方法 | 编译后 `len(ledger)` 不变 + `verify_chain()` |
| **确定性** | 相同输入 ⇒ 相同输出 | `verify_determinism()`：两次编译摘要一致 |
| **可追溯** | 每个投影带 `source_authority_events` | `trace_projection(type, target)` 返回 event_id 列表 |

## 三、W2 投影

从 Authority 的 **edge 级决定**推导攻击图，用 Dung grounded 语义计算：

- `result=APPROVE` 的边 ⇒ **攻击成立**（攻击者击败目标）
- `REJECT/MODIFY/ABSTAIN` ⇒ 攻击不成立/存疑，不产生击败
- grounded 迭代至不动点：有 IN 攻击者 ⇒ OUT；攻击者全 OUT ⇒ IN；无攻击者 ⇒ IN

### ⚠ 与现有 `grounded_labels_w2.json` 的偏差（诚实登记）

| 项 | 现有 grounded_labels | 本投影 |
|---|---|---|
| 节点 | **121**（79 命题 + 35 MIS + 7 OUT） | **519** |
| IN/OUT | IN 114 / OUT 7 / UNDEC 0 | IN 484 / OUT 35 / UNDEC 0 |

**原因**：两者**节点粒度不同**。现有 grounded_labels 以「命题 / MIS」为节点；
本投影以 Authority ledger 的 **`edge_id`（含 `::prop-N` 后缀）** 为节点，粒度更细。

**处置**：本批**不做数值对齐**，作为偏差登记，留 **627 做节点归一化**（把 edge_id 归一到
命题/MIS 级后再比对）。判据 6 的**结构性要求**（W2 由 Authority 投影而来）已满足；
**数值一致性**未满足。

## 四、PCK 投影（双聚合策略）

| 策略 | 规则 | 版本 |
|---|---|---|
| **严格（默认）** | CARD_APPROVED ⟺ 每个 material claim 有直接 evidence authority **且** 每个 critical negative test 有 verified result **且** 无未解决矛盾 **且** 有 card-level human authority | `v0.1-strict` |
| **宽松** | CARD_APPROVED ⟺ 无未解决矛盾 **且** 有 card-level human authority | `v0.1-relaxed` |

报告**同时列出两种策略的 authorized 数量与差异**，让人看到"放松聚合策略会多出多少"。

### 实测

| 项 | 值 |
|---|---|
| PCK 总数 | 83 |
| 严格策略 authorized | **0** |
| 宽松策略 authorized | **0** |
| 差异（宽松 − 严格） | **0** |
| 触发跨粒度警告 | 0（当前 ledger 无 card-level 事件可比对） |

> **根因**：Authority Ledger 的 452 条事件**全部是 edge 级**，没有 card-level authority
> ⇒ 严格/宽松策略都判 `pending`。这正是**判据 7「edge→card 不再自动授权升级」**的直接体现：
> edge 级授权**不会**自动升级为 card 级发布授权。

## 五、feature flag 与向后兼容

统一环境变量 **`QUEYI_AUTHORITY_V2`**（与 B2 共用，不再分两个 flag）：

| 路径 | 默认 | 说明 |
|---|---|---|
| **dashboard 投影** | **默认启用 V2** | 只影响展示，让 626 价值可见 |
| **W2 / PCK（关键路径）** | 默认**旧投影** | 需人确认后才切换（向后兼容） |
| 回滚 | `QUEYI_AUTHORITY_V2=0` | 立即回滚 625 行为；新 ledger 保留供审计 |

## 六、验证

- `authority_projection_compiler_626.py --check` → PASS（13 项断言）
- `tests/test_authority_projection_compiler_626.py` → 13 例全绿
- 确定性、只读、可追溯三项保证均有断言覆盖
