# 621 A3 · 新 mutation 质量评估 + 去重

> 输入 50 条 · 去重丢弃 **0** · 保留 **50**

## 一、质量分布（均值）

| 维度 | 均值 |
| novelty | 0.5 |
| attack_strength | 0.14 |
| semantic_validity | 1.0 |
| reproducibility | 1.0 |
| composite | 0.506 |

## 二、预测判决分布

| 判决 | 条数 |
| blocked | 36 |
| n_a | 14 |

## 三、Top 10 高价值 mutation

| # | mutation_id | 策略 | 卡 | 新颖性 | 攻击强度 | 语义 | 可复现 | 综合 |
| 1 | `MUT-621-030f3c3bc310` | rule_blind_spot | ATOM-MEM-LEAK-002.md | 0.5 | 0.5 | 1.0 | 1.0 | **0.65** |
| 2 | `MUT-621-201c02b6fc1b` | provenance_inconsistency | ATOM-MEM-NEW-001.md | 0.5 | 0.5 | 1.0 | 1.0 | **0.65** |
| 3 | `MUT-621-28e2f889141b` | provenance_inconsistency | ATOM-MEM-RAII-002.md | 0.5 | 0.5 | 1.0 | 1.0 | **0.65** |
| 4 | `MUT-621-48aefcf7dc09` | rule_blind_spot | EV-MEM-007.md | 0.5 | 0.5 | 1.0 | 1.0 | **0.65** |
| 5 | `MUT-621-4c17f4c0f010` | provenance_inconsistency | ATOM-MEM-VALUE-001.md | 0.5 | 0.5 | 1.0 | 1.0 | **0.65** |
| 6 | `MUT-621-5349e8eee3f2` | evidence_ambiguity | ATOM-MEM-MOVE-002.md | 0.5 | 0.5 | 1.0 | 1.0 | **0.65** |
| 7 | `MUT-621-795e8ee5c498` | rule_blind_spot | EV-HIST-001.md | 0.5 | 0.5 | 1.0 | 1.0 | **0.65** |
| 8 | `MUT-621-817ddf2fce05` | rule_blind_spot | ATOM-MEM-RVREF-001.md | 0.5 | 0.5 | 1.0 | 1.0 | **0.65** |
| 9 | `MUT-621-8ba9178bcf4a` | provenance_inconsistency | ATOM-CONC-RACE-001.md | 0.5 | 0.5 | 1.0 | 1.0 | **0.65** |
| 10 | `MUT-621-9934e6f9b1b8` | provenance_inconsistency | ATOM-UB-GRAY-001.md | 0.5 | 0.5 | 1.0 | 1.0 | **0.65** |


## 四、与 v7 基线的新颖性对比

| 新颖性档位 | 含义 | 条数 |
|---|---|---|
| 1.0 | 卡不在 v7，或 v7 无此（卡,算子）组合 | **0** |
| 0.5 | （卡,算子）已存在但**变异点不同** | **50（100%）** |
| 0.0 | 与 v7 完全重合（卡,算子,变异点） | 0 |

**关键诚实发现**：50 条新 mutation 的**（卡,算子）组合 100% 已存在于 v7**，
新颖性全部落在 0.5 档 —— 即只有"变异点（point）"是新的，攻击面组合本身没有突破 v7。

⇒ 这说明：**621 A1 的生成器虽然能产生"新" mutation，但候选空间并未真正被打散**。
真正的新颖攻击需要：
1. 覆盖 v7 从未组合过的（卡,算子）对；或
2. 引入 v7 没有的第 8 类算子（M8+）；或
3. 能真正把变异施加到沙箱并复算（有 apply API）。

这三条**本批都未实现**（见 §五 局限）。

## 五、局限性声明

1. **attack_strength 是估计不是实测**：它完全建立在 A2 的**预测判决**之上
   （621 §六.3 不跑门禁 + 无沙箱施加 API）。预测为 blocked ⇒ 强度 0，
   这不代表"真的被拦住"。
2. **可复现性 = 1.0 只证明"标识自洽"**：它校验的是 mutation_id 可由字段重算，
   **不是**"该变异被真实施加并复算过"。真正的可复现性需要沙箱执行。
3. **新颖性只有三档（0/0.5/1.0）**：是粗粒度规则，不是语义相似度计算。
4. **去重键较严**（content hash + rule + card），本轮 50 条无重复（dropped=0），
   故去重在本轮**没有实际淘汰**任何条目 —— 去重能力未被真正检验。
5. **Top10 全部是 n_a 预测项**：因为攻击强度权重最高（0.40）而 blocked 项强度为 0，
   ⇒ Top10 实际是"**最不可判**"的 10 条，而非"最可能逃逸"的 10 条。
   这个排序语义要在 A4 使用时注意。

## 六、产出

- 报告：data/mutation_quality_report_621.md（本文件）
- 高价值清单：data/mutation/high_value_621.json（Top 10）
