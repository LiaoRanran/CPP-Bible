# 629 D1 · 攻击目标函数精化（第八轮种子选择）

> 工具：`tools/attack_objective_629.py`（纯标准库，只读 v7 候选集）
> 候选池：`data/mutation/full_baseline_v7.json` 共 **1593** 条（任务书 1593 ✓）· 选出 **Top 20** 种子

## 一、目标函数

```
maximize  verifier_disagreement_rate × evidence_ambiguity × provenance_inconsistency
```

**乘积**（非加权和）的意义：三项**同时**高才排前；任一项为 0 则总分 0 —— 避免「只在一个面上凶」的样本挤进种子。

## 二、代理定义（显式假设，静态候选无法直接测）

| 分量 | 代理 | 依据 |
|---|---|---|
| verifier_disagreement | `escaped`→1.0；否则 `min(去重触发规则数/3, 1.0)` | 逃逸 = 所有验证者都不拦（最危险）；触发规则越多 = 判据间越不一致 |
| evidence_ambiguity | 形态/结构/引用三组关键词命中加权（上限 1.0） | 变异点描述里的模糊性词汇 |
| provenance_inconsistency | 哈希/时间戳/artifact/provenance→1.0；`evidence/` 卡→0.5；否则 0.2 | 溯源类变异优先打「不可复现」面 |

## 三、Top20 种子

| # | 卡 | op | v7 判决 | 触发规则数 | disagreement | ambiguity | provenance | **score** |
|---|---|---|---|---|---|---|---|---|
| 1 | `evidence/conc/EV-CONC-001.md` | M1 | blocked | 1 | 0.3333 | 1.0 | 1.0 | **0.3333** |
| 2 | `evidence/conc/EV-CONC-001.md` | M7 | blocked | 1 | 0.3333 | 1.0 | 1.0 | **0.3333** |
| 3 | `evidence/conc/EV-CONC-002.md` | M1 | blocked | 1 | 0.3333 | 1.0 | 1.0 | **0.3333** |
| 4 | `evidence/conc/EV-CONC-002.md` | M7 | blocked | 1 | 0.3333 | 1.0 | 1.0 | **0.3333** |
| 5 | `evidence/conc/EV-CONC-003.md` | M1 | blocked | 1 | 0.3333 | 1.0 | 1.0 | **0.3333** |
| 6 | `evidence/conc/EV-CONC-003.md` | M7 | blocked | 1 | 0.3333 | 1.0 | 1.0 | **0.3333** |
| 7 | `evidence/conc/EV-CONC-004.md` | M1 | blocked | 1 | 0.3333 | 1.0 | 1.0 | **0.3333** |
| 8 | `evidence/conc/EV-CONC-004.md` | M7 | blocked | 1 | 0.3333 | 1.0 | 1.0 | **0.3333** |
| 9 | `evidence/conc/EV-CONC-005.md` | M1 | blocked | 1 | 0.3333 | 1.0 | 1.0 | **0.3333** |
| 10 | `evidence/conc/EV-CONC-005.md` | M7 | blocked | 1 | 0.3333 | 1.0 | 1.0 | **0.3333** |
| 11 | `evidence/conc/EV-CONC-006.md` | M1 | blocked | 1 | 0.3333 | 1.0 | 1.0 | **0.3333** |
| 12 | `evidence/conc/EV-CONC-006.md` | M7 | blocked | 1 | 0.3333 | 1.0 | 1.0 | **0.3333** |
| 13 | `evidence/hist/EV-HIST-001.md` | M1 | blocked | 1 | 0.3333 | 1.0 | 1.0 | **0.3333** |
| 14 | `evidence/hist/EV-HIST-001.md` | M7 | blocked | 1 | 0.3333 | 1.0 | 1.0 | **0.3333** |
| 15 | `evidence/lang/EV-LANG-001.md` | M1 | blocked | 1 | 0.3333 | 1.0 | 1.0 | **0.3333** |
| 16 | `evidence/lang/EV-LANG-001.md` | M7 | blocked | 1 | 0.3333 | 1.0 | 1.0 | **0.3333** |
| 17 | `evidence/lang/EV-LANG-002.md` | M1 | blocked | 1 | 0.3333 | 1.0 | 1.0 | **0.3333** |
| 18 | `evidence/lang/EV-LANG-002.md` | M7 | blocked | 1 | 0.3333 | 1.0 | 1.0 | **0.3333** |
| 19 | `evidence/mem/EV-MEM-001.md` | M1 | blocked | 1 | 0.3333 | 1.0 | 1.0 | **0.3333** |
| 20 | `evidence/mem/EV-MEM-001.md` | M7 | blocked | 1 | 0.3333 | 1.0 | 1.0 | **0.3333** |

## 四、为什么这些种子优先级高

- 池内 score 分布：>0 的有 **1105** 条，=0 的有 488 条（乘积极强筛：多数候选在某一面为 0）；
- Top20 全部命中 `provenance` 强相关的变异点（哈希/artifact/引用类），且 `ambiguity` 分量 ≥ 1.0 —— 意味着**判据要用到歧义证据、且溯源链上有可动手的字段**，这正是 verifier 攻击面L2（证据漂移）/L4（规则绕过）交叉的位置；
- Top20 中 v7 判决为 neutral 的有 **0** 条 —— 这些是 v7 时代**完全没被拦住**的样本，优先复跑检验「现在是否仍拦不住」。

## 五、局限

- 三个代理都是**静态启发式**（读变异点文本与 v7 判决），不是真实测量；真实 disagreement 需要两个独立验证器各跑一遍（本批只做了 gate 判决）；
- `target_rule` 从 `new_block/new_warn` 反推（v7 无该字段），neutral 样本反推为空；
- v7 池是 621-622 生成的，**不含 M8/M9 算子**（新算子样本在 `data/mutation/new_mutations_62*.jsonl`）⇒ 种子偏向 M1-M7 家族。
