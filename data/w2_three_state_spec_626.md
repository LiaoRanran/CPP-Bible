# 626 C2 · W2 三态解耦规范 + OVERRIDE 语义拆开 + 镜像边有条件事实

> 工具：`w2_three_state_626.py` / `override_semantics_verify_626.py` / `mirror_edge_audit_626.py`
> 判据：5（Override 有明确 replacement/result）、8（W2 与 truth/publication 解耦）、9（镜像边 symmetry proof）

---

## 一、W2 三态解耦（判据 8）

国外大模型要求：W2 必须把「图论状态」和「知识真假」分开。

| 状态 | 含义 | 取值 | 来源 |
|---|---|---|---|
| `argument_status` | 图论语义状态（Dung grounded 语义） | IN / OUT / UNDEC | `grounded_labels_w2.json`（**只读现有**） |
| `truth_support` | 知识真假支持程度 | supported / refuted / unresolved | PCK 证书 `human_authority.status` |
| `publication_status` | 发布状态（受治理） | authorized / blocked / pending | Authority Ledger 的 **card-level** authority |

### 三态独立，互不替代

- **`IN ≠ 真`**——只表示"在当前攻击图中未被击败"
- **`OUT ≠ 假`**——只表示"被某个攻击击败"
- `publication_status` 必须有**显式 aggregation policy**（本批 `v0.1-strict`）

### 实测三态（626）

| 状态 | 实测 |
|---|---|
| `argument_status` | IN 114 / OUT 7 / UNDEC 0（nodes 121） |
| `truth_support` | supported 27 / refuted 0 / unresolved 56（83 张 PCK） |
| `publication_status` | authorized 0 / blocked 0 / pending（card-level authority 事件 0 条） |

> **诚实说明**：`publication_status.authorized = 0` 是因为当前 Authority Ledger 中
> **没有 card-level 的 authority 事件**（452 条全是 edge 级）——这正是**判据 7「edge→card 不再自动授权升级」**
> 要解决的问题：edge 级授权**不会**自动升级为 card 级发布授权。

### 向后兼容

- 三态是**新增投影**，**不修改 `gate_engine.py` 的 W2 计算逻辑**（留 627+）
- 现有 `grounded_labels_w2.json` 仍可用（三态读取它，不替换）

## 二、OVERRIDE 语义拆开（判据 5）

| 旧 | v2 |
|---|---|
| `power: OVERRIDE`（操作+结果合一） | `operation: REPLACE` + 具体 `result` |
| `overrides: <id>` | `supersedes: [<id>]` |

### 实测验证（452 条 ledger）

| 项 | 值 |
|---|---|
| REPLACE 事件 | **51** |
| 缺 `result` | 0 |
| 缺 `supersedes` | **0** |
| 硬问题 | **0** ⇒ 判据 5 满足 |
| 旧式引用告警 | **51**（34 × `legacy:pre_annotation:*` + 17 × `dec-0001xx`） |

> **告警说明**：51 条 `supersedes` 引用的是**旧式 ID**（尚未重映射到 v2 `event_id`）。
> 它们**非空且可溯源**，故满足「每个 REPLACE 都有 result 和 supersedes」；
> **ID 重映射留 627**。

## 三、镜像边有条件事实（判据 9）

「镜像边」从**自动事实**变为**有条件事实**：只有存在可验证的 `symmetry_proof_id`
才允许镜像边作为实质性攻击边。

### 实测审计

| 项 | 值 |
|---|---|
| 候选边 | 388 |
| 镜像边（`direction == "mis_to_prop"`） | **194** |
| 已验证 symmetry proof | **0** |
| 未验证（null） | **194** |
| 源数据缺字段 | 194（审计层已归一为 `null`） |

- `symmetry_proof_id` 字段已在 **626 B3 的 `ReviewItem`** 中预留（默认空），本任务不修改其结构。
- 审计层把源数据中缺失的字段**归一为 `null`**，使每条镜像边在账本中都有该字段（判据 9 的字段要求）。
- **当前 0 条已验证** ⇒ 镜像边**不可作为已验证事实**使用。补 `symmetry_proof` 需人审验证（留 627）。

## 四、验证

- 三个工具 `--check` 全 PASS
- 新增测试：`test_override_semantics_626.py`(7) + `test_w2_three_state_626.py`(6) + `test_mirror_edge_audit_626.py`(4) = **17 例**
