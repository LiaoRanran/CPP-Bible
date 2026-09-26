# 643 D3 · 规则草案 MDL 准入（智能层：自动提案规则 #3；**新增抗冗余闸**）

> 草案 **10** 条；`ADMIT` **0** 条；`REJECT_冗余` **6** 条（阈值 overlap > 0.8）；结论分布 `{'PENDING_HUMAN': 4, 'REJECT_冗余': 6}`。
> 在册规则 67 条（642 MDL 器的 `REFUSE_已有规则` 依据）。

## 一、逐条判定

| 草案 | 形态 | overlap | 依据 | 642 MDL 结论 | 最终结论 | 是否准入 |
|---|---|---|---|---|---|---|
| `ATOM-DRAFT-001` | NEW | 0.0 | 该卡已被 0 条规则命中（密度代理） | `PENDING_HUMAN` | **PENDING_HUMAN** | — |
| `MOD-ATOM-DAL-MATCH` | MODIFY | 0.5 | 与 `ATOM-ID-UNIQUE` 的字段重叠 | `PENDING_HUMAN` | **PENDING_HUMAN** | — |
| `MOD-ATOM-GRAY-ZONE` | MODIFY | 0.0 | 无可比规则/无字段 | `PENDING_HUMAN` | **PENDING_HUMAN** | — |
| `MOD-ATOM-ID-FORMAT` | MODIFY | 1.0 | 与 `ATOM-REL-DAG` 的字段重叠 | `PENDING_HUMAN` | **REJECT_冗余** | — |
| `MOD-ATOM-ID-UNIQUE` | MODIFY | 1.0 | 与 `ATOM-VERIFY-REASON` 的字段重叠 | `PENDING_HUMAN` | **REJECT_冗余** | — |
| `MOD-ATOM-FM-REQUIRED` | MODIFY | 0.0 | 无可比规则/无字段 | `PENDING_HUMAN` | **PENDING_HUMAN** | — |
| `MOD-ATOM-NO-UNVERIFIED` | MODIFY | 1.0 | 与 `ATOM-ID-UNIQUE` 的字段重叠 | `PENDING_HUMAN` | **REJECT_冗余** | — |
| `MOD-ATOM-CLAIM-STRUCTURED` | MODIFY | 1.0 | 与 `ATOM-REL-CONFLICT` 的字段重叠 | `PENDING_HUMAN` | **REJECT_冗余** | — |
| `MOD-ATOM-MISCONCEPTION-REF` | MODIFY | 1.0 | 与 `ATOM-MISCONCEPTION-LEVELS` 的字段重叠 | `PENDING_HUMAN` | **REJECT_冗余** | — |
| `MOD-ATOM-MISCONCEPTION-LEVELS` | MODIFY | 1.0 | 与 `ATOM-MISCONCEPTION-REF` 的字段重叠 | `PENDING_HUMAN` | **REJECT_冗余** | — |

## 二、判定顺序说明

1. **先判抗冗余**（`overlap > 0.8` ⇒ `REJECT_冗余`，不再往下判）；
2. 否则跑 **642 的 `admit_new_rule()`**（六档），取其结论为最终结论。

## 三、642 MDL 的已知口径问题（逐条标注）

- **NEW 草案必然「不在热力图」** ⇒ 会命中 `REJECT_热力图缺失`：这是**口径必然**（624 的热力图早于草案存在），**不是草案的错** ⇒ NEW 草案应看「若非此条是否还有别的否决」，而不是直接否决；
- **MODIFY 草案不是「新规则」** ⇒ 642 的器本不为它设计，本工具仍跑它并标 `MODIFY（近似）`，其 `savings/cost` 衡量的是**新增条件的边际收益**（近似，需人判）。

## 诚实登记

1. **MDL/抗冗余通过 ≠ 规则正确**（§十二.3）：这只是**费用与冗余**两道闸，规则**对不对**必须人审；
2. **`overlap` 对两类草案的定义不同**（NEW 用覆盖密度代理、MODIFY 用字段重叠）⇒ 两者的 `overlap` **不可互相比较**，已在表里分列依据；
3. **阈值 0.8 是本批新定的经验值**（642 没有这一档）⇒ 边界已在单测固定，改阈值会改变结论；
4. **本工具不改 642 的 MDL 器**：`REJECT_冗余` 是本工具**新增的第五档**，不写回 642 的 `DECISIONS` 常量（避免改动已入库工具）；
5. 本工具**只读**：不改规则库、不写侧车元数据（写侧车是 D2 的产出）。
