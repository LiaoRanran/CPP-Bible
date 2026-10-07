# 684 · C2 新 Framing 提案

- **批次**：684 ｜ **承接**：C1 诊断、A1–A4、B1–B3
- **目标**：把论文从「算法创新」叙事转向「**评估方法论 + 治理创新**」叙事，同时把本批理论分析固化为一个**诚实的新贡献**。

---

## 1. 核心 Framing 句（建议用作摘要/引言锚点）

> *"We propose an auditable governance framework for evolving evidence-acquisition
> apparatus, with a formal analysis of asset selection as **submodular
> maximization** and an empirical study of selection-strategy behavior across
> 1147+ samples."*

这一句的三个支点：

1. **auditable governance framework**（治理框架）——论文最强、最独特的卖点；
2. **formal analysis as submodular maximization**（子模形式化）——本批新增的理论贡献，把「选择」从模糊的「failure-driven」提升为可引用的数学对象与近似保证；
3. **empirical study of strategy behavior**（策略行为实证）——676f/677c/682 已有的 1147 样本 × 8 资产 + clone-aware split + 敏感性分析 + 真实靶场（683）。

---

## 2. 三贡献重构

### 贡献 1 · 治理框架（保留并强化，最强）
可审计的演化治理：四态判定（unknown 一等公民）、Merkle 链、失败驱动的迭代纪律、能力边界声明、append-only 账本。这是论文区别于所有「self-evolving benchmark」的根本——**谁评判、评判是否可信，本身成为可审计的科学对象**。

### 贡献 2 · 理论分析（**新增**，本批主体）
资产选择的**子模优化形式化** + FD 贪心的 $(1-1/e)$ 近似保证 + 退化资产的理论解释。具体交付：
- A1：把资产选择写成 $\max_{|S|\le k} f(S)$，$f$ 为 OR 覆盖，并证明 FD 的 greedy/frequency ≡ 标准子模贪心；
- A2：全枚举 17496 组验证 100% 子模；
- A3：$(1-1/e)$ 推导 + 与实验值对照（正本清源「63.2% vs 54.6%」的量纲混淆）；
- A4：退化资产 $\Delta\approx c\cdot kd/n$ 公式与验证。
- 价值：把「FD 不是更聪明的排序，而是避免零信息资产的稳健选择」从定性观察升级为**有保证的形式化结论**。

### 贡献 3 · 大规模实证（已有，保留）
1147 样本 × 8 资产 + clone-aware split（677b）+ 非退化池多 baseline（677c）+ 敏感性分析（682）+ 真实缺陷重建（683 靶场）。

---

## 3. 弱化的 claim（明确清单）

| 原（易误读）表述 | 改为（诚实）表述 |
|---|---|
| 「our algorithm is superior / novel」 | 「we *formalize* the selection problem and prove the greedy choice carries a $(1-1/e)$ guarantee; we do not claim a novel algorithm」 |
| 「novel evolution operator」 | 「an instantiation of failure-driven selection with four scoring components, valued for *falsifiability*, not detection gain」 |
| 「FD beats random / static」 | 「FD reliably *avoids zero-information assets*; the non-degenerate selection effect is directional (+7–12pp), never confirmatory」 |
| 「+24.0pp」作为领起数字 | 「non-degenerate selection effect +7–12pp (the +24pp full-pool figure is dominated by degenerate-asset avoidance)」 |

---

## 4. 为什么这个 Framing 更稳（评审视角）

- **不依赖「更优」**：方向性结论 + 治理框架本身可独立成立，即使选择效应进一步缩小也不动摇核心贡献。
- **理论贡献可引用**：子模形式化 + $(1-1/e)$ 是 ML/优化社区熟悉的语言，审稿人可快速定位价值，且不与「算法新颖」硬碰。
- **与既有诚实披露一致**：677c 的坍缩披露、677d 的方向性 claim、L1809 的「avoiding zero-information assets」都被本批形式化**收口**而非推翻。

---

## 5. 落地位置建议（详见 C3 / paper_modification_checklist）

- 摘要 L76-99：首句加 submodular 形式化；领起数字改 non-degenerate 效应。
- 贡献 L145-167：新增贡献 2（子模形式化 + 保证）；贡献 1 的 operator 表述降级。
- Method L1012-1052：新增「Selection as submodular maximization」小节（引用 Nemhauser 1978, Krause & Golovin 2014）。
- Experiments：补充理论近似比与实验对比段落。
- Related Work L174-205：补 submodular maximization / active testing / evaluation governance 文献（见 D）。
- Conclusion：调整结论措辞（去掉「更优」暗示）。
