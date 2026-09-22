# 615 A1 · 人审诚实化（388 条真实审核方式重述）

> **只读** annotations；标签为独立文件，**不改**任何人审结果。

## 一、诚实声明（核心）

- 388 条「人审」中，**0 条为逐条独立判断**，**388 条为批量授权**（非逐条复核）；
- 其中 **194 条为镜像边**（命题↔MIS 对称推断，一次判断算两条，不提供独立信息）。
- ⇒ 独立人类确认强度 = **0 条**（不含镜像票、不含抽样外推票）。

## 二、审核方式对比

| 方式 | 条数 |
|---|---|
| 逐条独立判断 item_by_item | 0 |
| 批量授权 batch_authorization | 388 |
| 其中镜像边 is_mirror | 194 |

## 三、模板化理由分布（5 模板）

| 模板 | 条数 | 特征 |
|---|---|---|
| T1 | 177 | 镜像(approve) |
| T2 | 176 | 抽样外推 |
| T3 | 17 | 批量 adjust |
| T4 | 17 | 镜像(modify) |
| T5 | 1 | T2 变体 |

## 四、理由长度分布

- min/max/**median** = 47/80/**67.5**（mean ≈ 69.20）

> ⚠ **已修正（2026-09-22）**：原写 `median = 75`，与 388 条真实数据不符。
> 该错误由**外部大模型独立重算**发现，并经 `tools/stats_recalc_verifier_626.py` 复算确认：
> **median = 67.5**（min 47 / max 80 / mean 69.20）。原值 75 为笔误，现据实测修正。

| 区间(字符) | 条数 |
|---|---|
| 40-49 | 17 |
| 50-59 | 1 |
| 60-69 | 176 |
| 70-79 | 17 |
| 80-89 | 177 |

## 五、边界

- 原 `data/human_attack_edge_annotations.jsonl` **未被修改**（sha256 对照锚）。
- 标签只描述「审核方式」，**不改变**任何 approve/modify 结论。

## 六、622 授权执行的口径说明（2026-09-22 补）

> 由外部大模型审阅发现（硬伤 2），626 A3 落地。核心：**「人类判断」≠「人类授权执行」**。

| 概念 | 含义 | 本项目的量 |
|---|---|---|
| **人类判断** | 人真实观察证据后做出的语义判断 | **0 条**（388 条全是批量授权） |
| **人类授权执行** | 人授权后，由流程把决定落到日志 | **30 条**（622 D1） |

- 622 D1 执行的 30 条属于**后者**：`review_method = ITEM_OPEN`（旧名 `item_by_item_executed`）、
  `decision_origin = user_authorized_execution`。
- 证据：17 条 OVERRIDE + 13 条 ACCEPT，理由**全部模板化**（沿用 615 清单模板 / 「复核 approve」），
  文档自述「本批未新增任何人工判断，只做了把授权落到日志」。
- ⇒ **独立人类确认强度 = 0**，30 条不得计入强人审证据（626 完成判据 1）。

### review_method 五级（626 A3 定义，见 `tools/authority_schema_v2_626.py`）

| 级别 | 含义 | 是否计入独立确认 |
|---|---|---|
| `BATCH_AUTH` | 批量授权 | ❌ |
| `MIRROR_DERIVED` | 镜像边派生 | ❌ |
| `ITEM_OPEN` | 逐条开放式审查（**看得到** AI 推荐） | ❌ |
| `ITEM_BLIND` | 逐条盲审（**看不到** AI 推荐） | ✅ |
| `ITEM_SECOND_REVIEW` | 二次复核 | ✅ |

### decision_origin 四级

`human_observed` / `user_authorized_execution` / `machine_projection` / `mirror_projection`

> **计入规则**：`review_method ∈ {ITEM_BLIND, ITEM_SECOND_REVIEW}` **且** `decision_origin == human_observed`。
> 622 的 30 条（ITEM_OPEN + user_authorized_execution）**不满足**，故强度仍为 0。

