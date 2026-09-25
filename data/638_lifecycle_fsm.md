# 638 3.2 · Lifecycle FSM（五态状态机 · 真落地）

> 生成时间：2026-09-25T09:31:39。工具：`tools/lifecycle_fsm_638.py`。

## 一、五态定义

| 态 | 含义 |
|---|---|
| `draft` | 刚创建，未验证 |
| `verified` | 验证通过 |
| `stale` | 边界漂移/证据老化 |
| `disputed` | 有争议/被击败器触发 |
| `retired` | 退役，带复活条件 |

## 二、迁移合法性矩阵（25 组）

- 合法迁移：**11 / 25** 组；

| from \ to | draft | verified | stale | disputed | retired |
|---|---|---|---|---|---|
| `draft` | — | 合法 | — | — | 合法 |
| `verified` | — | — | 合法 | 合法 | 合法 |
| `stale` | — | 合法 | — | 合法 | 合法 |
| `disputed` | — | 合法 | — | — | 合法 |
| `retired` | 合法 | — | — | — | — |

## 三、复活条件（`retired → draft` 必填其一）

| 条件 | 含义 |
|---|---|
| `new_evidence` | 新证据出现 |
| `boundary_change` | 边界变化（三元组改变） |
| `defeater_resolved` | 击败器被解决 |

> 未提供或提供非法条件 ⇒ **判非法**（`can_transition` 返回 False）。

## 四、全库当前态普查（真实）

- 扫描 `atoms/**/*.md`：**28** 张卡；
- 四态分布：`{'draft': 2, 'verified': 26}`；
- 其中有显式 `lifecycle:` 字段的：**0** 张；
- 迁移 ledger：**0** 条；链校验错误：**0** 条。

### 4.1 初态推导口径（诚实说明）

实测 28 张卡**全部无 `lifecycle:` 字段**，故「当前态」按 `status:` 推导：
`verified`/`red-team-verified → verified`；`draft → draft`；无 `status` → `draft`。
该映射是**兼容性推导**，不是卡上的真实 FSM 态（后者需后续批次回填）。

## 五、诚实登记

1. **ledger 默认不存在**（本批首次上线）：`--check` 不创建 ledger，`--record` 才追写；
2. ledger **append-only + 哈希链**（seq/prev_hash/self_hash），`verify_ledger()` 可校验；
3. 初态推导用 `status:` 兼容映射（见 §4.1），**非**卡上真实字段；
4. 迁移规则**严格按 §三.3.2.2**，未自行扩充；`retired → draft` 必须给复活条件；
5. 本工具**不改任何卡**（只读卡、只写自己的 ledger/报告）。
