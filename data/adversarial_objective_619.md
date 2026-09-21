# 619 A1 · 攻击目标函数 v1（可计算代理定义）

> 配套代码：`tools/adversarial_objective_619.py`（纯标准库、`--check` 自检、不写盘）
> 数据面：只读 `data/mutation/full_baseline_v7.json`（1593 variants / 1406 可判 / 8 等效 / 179 n_a）
> 口径约束：619 §五/§六（只读、不新生成 mutation、不跑监工门禁）；冻结门禁数字取 SNAPSHOT_MANIFEST_617。

## 一、目标

把「攻击强度」变成一个**可以逐条计算**的纯函数，使后续攻击者（A2）能按分数降序挑 mutation 来 fuzz，
而不是盲打。目标 = **优先 fuzz 那些最可能让 verifier（gate + replay）出错 / 被攻破的变异**。

四个子目标（37 号路线图 雷2）：

| # | 子目标 | 语义 | 可计算？ |
|---|---|---|---|
| 1 | `verifier_disagreement` | 多 verifier 对同一卡的判决不一致 | **N/A**（当前 `verifier_count=1`，需 ≥2 个独立 verifier 才有分歧可言） |
| 2 | `evidence_ambiguity` | 证据可说服性模糊（解析层 / 判别力层歧义） | ✅（替身 `verdict_regime_disagreement` 见下） |
| 3 | `rule_blind_spot` | 规则盲区（应有规则该拦却没拦，或薄拦截） | ✅ |
| 4 | `provenance_inconsistency` | 溯源不一致（哈希/路径/签名绑定被绕过） | ✅ |

> **口径诚实说明**：子目标 1「verifier_disagreement」在 `second_implementation = 1/63`、独立验证 `verifier=1 硬上限`
> 的现状下**无法测量**，故恒置 `N/A`、权重 0（不改变分母）。为覆盖「判决分歧」这一类攻击面，
> 定义**替身指标** `verdict_regime_disagreement`（严格口径 vs treated 口径的判决分歧）——它**不是**多 verifier 分歧，
> 命名上已显式区分，避免与子目标 1 混淆。

## 二、可计算代理（逐条，全部来自 v7 既有字段，不编造）

| 子目标 | 代理公式 | 取值 |
|---|---|---|
| `verdict_regime_disagreement` | `kind=="warn_only"`（严格口径不拦、treated 口径才拦） | 1.0；`strict` / `escaped` ⇒ 0.0；n_a ⇒ None |
| `evidence_ambiguity` | `equivalent?0.6` + `op∈{M4,M6}?0.25` + `replay_skipped` 非空?0.15 | 截断 ≤1.0 |
| `rule_blind_spot` | `escaped` 真逃逸 | 1.0 |
| | `blocked` 且命中规则**全属 GENERIC 结构性集** | 0.6 |
| | `blocked` 且恰好命中 1 条规则 | 0.3 |
| | 其余（含 `warn_only`，因 `new_block` 为空 ⇒ 由口径分歧承担） | 0.0 |
| `provenance_inconsistency` | `point` 关键词分级（有序命中）：`sha256`/`signed_by` 1.0、`run_match` 0.8、路径类（`路径`/反斜杠/`Examples/`）0.7、`artifact`/`fixture` 0.6 | 否则 0.0 |

`GENERIC_RULES`（结构性/格式类，命中它们只说明卡形状不对，不含语义判断）：
`EV-FM-REQUIRED, EV-FM-DUP-KEY, EV-FM-YAML-HARDENING, EV-ID-UNIQUE, ATOM-FM-REQUIRED, ATOM-ID-FORMAT, ATOM-ID-UNIQUE`。

**双计避免**：`warn_only` 记录 `new_block` 为空 ⇒ `rule_blind_spot=0.0`（没有 block 级命中谈不上「盲区」），
其风险只由 `verdict_regime_disagreement` 覆盖。

**口径一致性（与 v7 报告同一口径）**：`verdict=="n_a"`（179 条）⇒ `composite=None`、**不进分母**；
`equivalent`（8 条）⇒ 标记 `known_equivalent`、**剔出排序**（已知无害），但保留子目标分数供歧义分析。

## 三、组合方式：加权和 + 帕累托前沿（多目标兜底）

**主排序 = 加权和** `composite = Σ WEIGHTS[k]·sub[k]`（仅对 4 个可计算子目标；`sub` 缺失按 0）。

**提议默认权重 W1（待拍板）**：`rule_blind_spot 0.40 / verdict_regime_disagreement 0.25 / evidence_ambiguity 0.20 / provenance_inconsistency 0.15`（和为 1.0）。

**多目标兜底**：加权和会掩盖 trade-off（一个变体可能 a 高 b 低），故同时提供 `pareto_front()` 取 4 子目标上的
**非支配集**（最大化语义），A2 报告同时给「加权 Top20」与「帕累托前沿」两套，权重选择不隐藏矛盾。

## 四、与 mutation 算子的关系（实测：哪些算子对哪个子目标最有效）

来自 `summarize()` 对 1593 条的真实聚合（mean_sub 为已判 1406 子集均值）：

| 算子 | n(可判) | mean_composite | vrd | evidence_ambiguity | rule_blind_spot | provenance |
|---|---|---|---|---|---|---|
| M1 字段删除 | 65 | 0.398 | 0 | 0.129 | **0.569** | **0.960** |
| M2 路径变形 | 168 | 0.355 | **1.000** | 0 | 0 | 0.700 |
| M3 断言弱化 | 65 | 0.255 | 0.923 | 0 | 0.023 | 0.098 |
| M4 恒真注入 | 224 | 0.170 | 0 | **0.250** | 0.300 | 0 |
| M5 claim 自标 | 29 | 0.250 | **1.000** | 0 | 0 | 0 |
| M6 YAML 变形 | 724 | 0.262 | 0.465 | **0.257** | 0.237 | 0 |
| M7 哈希/计数篡改 | 139 | 0.173 | 0 | 0.090 | 0.237 | **0.403** |

> 读法：M2/M3/M5 几乎只贡献「口径分歧」（warn_only）；M4/M6 主要贡献「证据歧义」（解析层）；
> M1 同时拉满「规则盲区(薄拦截)」与「溯源」；M7 主贡献「溯源」。⇒ A2 的 Top20 由各算子混合组成，
> 不会单一算子垄断。

## 五、权重决策（人拍板项）—— 敏感度表

真逃逸 `evidence/conc/EV-CONC-001.md · M1 删 negative_controls` 在**不同权重**下的排名（1406 可判集中）：

| 权重集 | 权重（rbs/vrd/ea/pi） | 真逃逸 composite | 真逃逸排名 | Top1 |
|---|---|---|---|---|
| **W1 默认** | 0.40/0.25/0.20/0.15 | 0.400 | **57 / 1406** | M1 删 artifact_sha256 0.420 |
| **W2 盲区优先** | 0.50/0.20/0.15/0.15 | 0.500 | **1 / 1406** | M1 删 negative_controls 0.500 |
| W3 等权 | 0.25/0.25/0.25/0.25 | 0.250 | 634 / 1406 | M3 删 run_match_keys 0.450 |
| W4 口径优先 | 0.25/0.40/0.20/0.15 | 0.250 | 651 / 1406 | M3 删 run_match_keys 0.520 |

**结论**：权重的选择**直接决定「已知最强攻击」是否被排到顶部**（排名跨度 1 → 651）——这是不可回避的
**人拍板项**，不是技术问题。

- 只有 `W2`（rule_blind_spot 0.50）让唯一的真逃逸排到第 1（0.500），与「攻击目标=找盲区」的直觉一致 ⇒ 建议把 W2 作为**校准锚定默认**。
- 其余权重集下，Top1 被「M1 删 artifact_sha256（被 EV-FM-REQUIRED 薄拦截兜住，0.42）」或「M3 删 run_match_keys（warn_only 口径分歧，0.45+）」占据。
- 本批**默认仍用 W1**（保守、不过度拟合已知真逃逸），但把「采用 W2 作为校准默认」登记为 **620 人拍板项**。

## 六、已知限制 / 待拍板（诚实登记，留 620）

1. `verifier_disagreement` 恒 N/A（1 verifier）。恢复该子目标需先做 B 线（PCK 第二 verifier）或 `second_implementation` 覆盖。
2. `rule_blind_spot` 的 `0.6/0.3` 分支是**反事实薄拦截假设**（若某规则被豁免/调整则逃逸），非已验证事实——常数先验待拍板。
3. 权重是**人决策**，默认 W1；W2 校准锚定建议待拍板（见 §五）。
4. 目标函数只覆盖「单变异体」强度；**攻击-验证迭代**（A4）的增益/收敛尚未定义（A4 只写协议，不跑）。
5. v7 的 `results[]` 无「攻击强度」字段，全部子目标由既有字段纯计算；若将来 `mutation_fuzz` 增加分数，需重对齐口径且**不破坏冻结基线**。

## 七、自检契约

`tools/adversarial_objective_619.py --check` 断言：权重和=1.0、声明的 5 子目标中 4 可计算、确定性、
真逃逸 composite > warn_only 路径变形、verifier_disagreement 恒 N/A、n_a 不进分母、warn_only 不双计、
sha256 篡改触溯源 1.0、真逃逸盲区 1.0、帕累托前沿含真逃逸、summarize 覆盖全部算子。⇒ exit 0。
