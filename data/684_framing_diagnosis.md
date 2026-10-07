# 684 · C1 当前 Framing 诊断

- **批次**：684 ｜ **审视对象**：`research/latex/queyi_neurips2027_v1.1.tex`（v1.3 / 677d 合并版）
- **方法**：逐条抽取「算法/选择机制」相关 claim，用 676f/677c/682 及本批 A/B 实验证据评估是否被支持。
- **红线**：只读论文，不改论文正文（683 可能并行改附录）；行号基于 684 读取时快照，合并前需与 683 最终版对齐。

---

## 1. 逐 claim 诊断

### Claim A：「failure-driven evolution is superior」（FD 演化更优）

- **论文当前状态（已降级）**：摘要 L94-96 与正文 L655-662 已明确改为**方向性**陈述——「does not support superiority over a real static detector」「Our central empirical result is therefore directional: … evidence for the mechanism, not a confirmatory …」。677d 头注释也写明「The claim stays DIRECTIONAL」。
- **证据评估**：✅ **已得到实验支持（作为方向性 claim）**。676f/677c/682 证实：剔除退化资产后，non-degenerate 池 $k\le3$ 仍有 +7.4~+11.3pp 选择效应（$p$ 低）；clone-aware 重切分不改变结论（677b）。本批 A4 进一步把这一现象量化为「FD=避免零信息资产，不是更聪明的排序」——与 L1809 一致。
- **残留风险**：摘要 L94 仍以「+24.0pp full pool」领起，虽 L95-96 立即补充「excluding degenerate assets … +7.4-11.3pp」，但读者第一眼易被 +24pp 锚定。建议摘要首句改为直接给 non-degenerate 选择效应，+24pp 降级为括号补充（见 C3）。

### Claim B：「evolution operator」（演化算子）

- **论文当前状态**：L1036-1052 已把它算法化为可执行 score 函数，并**披露两个坍缩**：(i) `novel ≡ failure`（规格字面坍缩）；(ii) FD = frequency-only 特例（$w_1{=}1$）。消融给出「full operator 在 3/14 tiers 胜过 676f FD，最佳 +1.41pp, $p{=}0.302$，不显著」。
- **证据评估**：⚠️ **部分支持，但「novel」主张必须降级**。677c 与本批 A1 共同确认：`fd_only ≡ greedy`（子模贪心），`novel` 分量与 `failure` 坍缩 → 算子在数学上不超越经典子模选择。论文已诚实披露，但 L64 标题与 L145 贡献(1)仍把「evolution operator」作为卖点之一，易被读作「新算法」。
- **处置**：将其定位从「novel operator」改为「an instantiation of failure-driven selection with four scoring components」（见 C2 贡献重述），价值锚定在**可证伪性**而非检测增益（L1052 已如此说，需上移到摘要/贡献层）。

### Claim C：「novel selection mechanism」（新颖选择机制）

- **论文当前状态**：L1808-1809 已承认「FD's value is avoiding zero-information assets, not superior ranking」。但全文未显式形式化「选择 ≡ 子模贪心」这一数学事实。
- **证据评估**：❌ **「novel」不成立**。677c 证明 `frequency ≡ fd`；本批 A1/A2 证明 FD 选择 ≡ 标准子模贪心，且 greedy 在该实例达到精确最优（比值 1.0）。因此选择机制**不是新颖的**，它是经典子模最大化的直接应用。
- **处置**：把「novel selection mechanism」重写为「we *formalize* the asset-selection problem as submodular maximization and prove the greedy choice carries a $(1-1/e)$ approximation guarantee」（见 C2 新增贡献 2），这是**诚实且有发表价值**的升级——形式化与理论保证本身是新贡献，而非「新算法」。

---

## 2. 诊断总表

| Claim | 当前论文状态 | 是否被证据支持 | 684 建议处置 |
|---|---|---|---|
| A: FD 演化更优 | 已降级为方向性 | ✅ 支持（方向性）| 摘要领起句改 non-degenerate 效应 |
| B: evolution operator | 已算法化+披露坍缩 | ⚠️ 支持但 novel 须降级 | 改为「four-component instantiation」 |
| C: novel selection mechanism | 仅 L1809 部分承认 | ❌ novel 不成立 | 改为「submodular formalization + 保证」|

---

## 3. 对本批 C2/C3 的预示

诊断结论与任务卡预言一致：**论文的核心竞争力不在「算法创新」，而在「评估方法论/治理创新」**。本批 A/B 提供的子模形式化、(1-1/e) 保证、退化资产理论、信息论分析，恰好能把 Claim C 从「伪新颖」转化为「真形式化贡献」，且不触碰任何已落地的方向性 claim。详见 C2 提案与 C3 修改清单。
