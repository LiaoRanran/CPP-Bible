# 691 标准化分析正文突出（B4）：−17.92pp 是"整体率相似"的真正解释

- 数据源：`data/689_standardized_analysis.json`（689 已算，**691 只改写法/位置，未改数字**）
- 触发：690 指出该发现的科学价值高于 TOST，却埋在附录

---

## 1. 689 状态（问题诊断）

689 的 Finding 4 已把标准化写进正文，但**顺序与措辞**仍以 TOST 为主、标准化为辅：

> *"A two-one-sided-test audit at ±10pp does not pass… Standardization answers why the headline
> rates look similar: re-weighting the synthetic family rates by the real family composition raises
> the synthetic prediction to 77.01%—a −17.92pp forward difference—while the reverse weighting
> nearly closes (+1.70pp)…"*

⇒ 读者会先读到"检验没过"，再读到"其实有个更大的偏移"；**主次颠倒**。690 的判断成立：
"−17.9pp 证明整体率相似是构成抵消"比"TOST 未过"更有信息量。

## 2. 691 改写（正文 §5.4，原文摘录）

> ***Standardization is the substantive result here, and it is a correction of the headline
> story:*** the aggregate rates agree (59.09% vs. 61.64%), but they agree for the wrong reason.
> Re-weighting the synthetic family rates by the real family composition raises the synthetic
> prediction to 77.01%—a **−17.92pp** forward difference—while the reverse weighting nearly closes
> (+1.70pp). The apparent agreement is therefore produced by ***opposed* family-level differences
> that cancel**: real defects concentrate in families our instrument is good at
> (bounds+memory+integer = 64.5% of samples vs. 36.9% in the synthetic corpus) while being markedly
> *worse* where the synthetic corpus is dense (`language_oop`/logic: real 1/31 vs. synthetic 9/35).
> Two corpora can share a headline rate and still measure different things; **the adjusted gap, not
> the raw gap, is the quantity a reader should carry away.**

TOST 保留为后续补充（"equivalence is not established"，含 CI 与最小通过 margin），
**不再作为该段的结论句**。

## 3. 三个层次的数字（同一份产物，三种口径）

| 口径 | 值 | 含义 |
|---|---:|---|
| 原始差值 | **−2.55pp**（59.09 vs 61.64） | 表面"几乎一样"（但 CI 宽，TOST 未过） |
| **正向标准化**（合成家族率 × 真实家族权重） | **−17.92pp**（$R^{\text{syn}}_{\text{std}}=77.01\%$） | **同口径下合成更"好"17.9pp** |
| 反向标准化（真实家族率 × 合成权重，6 共同家族归一） | **+1.70pp**（59.94 vs 61.64） | 反向几乎闭合 ⇒ 支撑"抵消"解释 |
| 类型级（9 个共同类型） | −13.52pp（反向 +11.76pp） | 方向一致，非家族聚合假象 |

家族举证（决定性）：memory 真实 100% vs 合成 71.05%；`language_oop` 真实 3.23% vs 合成 62.07%；
alias_type 真实 0% vs 合成 36.56%；共同支撑覆盖合成池 79.8%。

## 4. 为什么这条比 TOST 更有价值（可迁移）

1. **它解释了机制**：TOST 只说"不能断言等价"，标准化说了"为什么看起来等价"——**构成抵消**；
2. **它对所有基准研究者有用**：任何"合成/真实语料率相近"的比较都可能踩同一个坑；
3. **它把命名纠正连起来**：source-derived reconstruction ≠ naturalistic artifact，
   构成差异正是"来源不同 ⇒ 缺陷类型配比不同"的直接后果；
4. **它是 5 条规则中 R5 的实证支撑**（"apparent improvement must survive composition audits"）。

## 5. 前后对比

| 项 | 689 | 691 |
|---|---|---|
| 该段结论句 | "TOST does not pass"（检验为主） | **"标准化是实质结果"**（机制为主） |
| 是否给"抵消"的家族级证据 | 部分（一句话带过） | ✅ 三个家族对比 + 共同支撑比例 |
| 是否给读者行动指引 | ❌ | ✅ "the adjusted gap, not the raw gap, is the quantity to carry away" |
| TOST 位置 | 段首 | 段中补充（数字不变） |
| 数字 | 不变（−17.92 / +1.70 / −13.52） | 不变（**无新计算**） |
