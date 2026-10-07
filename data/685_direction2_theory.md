# 685 · 方向 2 理论：鲁棒资产选择（检测器噪声下的稳定性）

- **批次**：685 ｜ **承接**：676m（~5% 跑间不稳定）、684 子模框架
- **配套**：`685_direction2_experiment.json`、`685_direction2_report.md`
- **理论根**：覆盖函数对 verdict 矩阵的 1-Lipschitz 性；对照 Orlin-Saha (S7)、Mitrović (S8) 鲁棒子模。

---

## 1. 动机

676m 报告检测器有 ~5% 跑间不稳定（同一 (样本, 资产) 的 verdict 可能 flip）。这引发一个问题：**基于（有噪声的）矩阵选出的 FD 资产集合，是否稳健？** 是否需要引入鲁棒子模优化（S7/S8）？本方向给出理论界 + 实验回答：**不需要**。

---

## 2. 符号

令 $\mathbf{V}$ 为 $n\times 8$ 判定矩阵，元素 $V_{i,a}\in\{\text{catch},\text{miss},\text{unknown}\}$。覆盖函数
$$ f(S;\mathbf{V}) = \big|\{i : \exists a\in S,\ V_{i,a}=\text{catch}\}\big|. $$
FD 贪心在矩阵 $\mathbf{V}$ 上选 $S^*(\mathbf{V})=\arg\max_{|S|\le k}f(S;\mathbf{V})$。

---

## 3. 引理：覆盖函数对 verdict 矩阵的 1-Lipschitz 性

**引理 1（逐格 Lipschitz）**：对任意两矩阵 $\mathbf{V},\mathbf{V}'$ 与任意资产集 $S$，
$$ \big|f(S;\mathbf{V}) - f(S;\mathbf{V}')\big| \le H(\mathbf{V},\mathbf{V}'), $$
其中 $H$ 为两矩阵在 $\{\text{catch},\text{miss}\}$ 维度上的 Hamming 距离（翻转格数；`unknown` 为结构量，不计入噪声）。

*证明*：翻转单个 $(i,a)$ 格至多改变样本 $i$ 是否被 $S$ 覆盖（且只有当 $a\in S$ 时才可能），故单次翻转使 $f(S)$ 变化 $\le 1$；叠加得总变化 $\le$ 翻转格数。∎

**推论（期望界）**：在每格独立以概率 $\varepsilon$ 翻转 `catch↔miss` 的噪声模型下，期望翻转数 $\mathbb{E}[H]=\varepsilon\cdot n\cdot 8\cdot \rho$，其中 $\rho$ 为非 `unknown` 格占比（本数据 $\rho\approx 0.88$）。于是
$$ \mathbb{E}\big[\,|f(S;\mathbf{V})-f(S;\mathbf{V}')|\,\big] \le \varepsilon\, n\cdot 8\cdot \rho. $$
对 $n{=}1137,\ \varepsilon{=}0.05$ 得期望翻转 $\approx 400$ 格，给出覆盖的**最坏情况**上界 $\approx 400/1137\approx 35$pp（极松的 union bound）。

---

## 4. 选择稳定性（本文真正关心的量）

FD 的产出是**选出的集合** $S^*(\mathbf{V})$，而非覆盖值本身。集合稳定的条件是：噪声不使两个资产的边际排序发生交叉。

**引理 2（大间隔 ⇒ 选择稳定）**：若两资产 $a,b$ 在干净矩阵上的边际满足 $|\Delta_a - \Delta_b| \gg \varepsilon\cdot n$，则其贪心排序以高概率不变。本数据中 `asan` 边际 $\approx 35\%$ 远超其余资产（13%–22%），大间隔使第一步选择几乎确定；后续步骤的间隔虽小，但 300 次实验显示 Jaccard 仍达 0.96（ε=0.05）。

**定理（无需鲁棒优化）**：当选择稳定性高（Jaccard≈1）时，噪声贪心集在**干净真值**上的覆盖掉点由引理 1 的紧化版本控制：
$$ \mathbb{E}\big[\,f(S^*(\mathbf{V}');\mathbf{V})-f(S^*(\mathbf{V});\mathbf{V})\,\big] \le \varepsilon\cdot n\cdot 8\cdot \rho \cdot \Pr[\text{该格影响已选集}]. $$
因已选集仅含 4 资产且间隔大，上式远小于引理 1 的宽松 union bound——实证掉点仅 0.11pp（ε=0.05）。

---

## 5. 与 684 子模框架的关系

- 684 证明 $f$ 子模、贪心达最优；本方向证明该最优解对**判定噪声**具有 Lipschitz 稳定性——是子模框架的鲁棒性补丁。
- 对照 S7/S8（鲁棒/对抗子模）：那些方法针对的是**最坏情况对抗移除**，本数据仅是温和随机 flip（且 `unknown` 结构量受保护）。实验表明普通贪心已足够稳健，引入鲁棒优化属**过度工程**——这是一个**有用的负结果**。

---

## 6. 创新性诚实评估

- **本质**：1-Lipschitz 引理是覆盖函数的显然性质（非新定理）；选择稳定性论证是引理 1 的标准推论。
- **增量价值**：首次在"验证器资产选择"场景**实证量化** FD 对 ~5% 检测器噪声的稳健性（Jaccard 0.96 / 掉点 0.11pp），并据此论证**无需**鲁棒优化——闭合了 676m 噪声风险的疑问。
- **定位**：应用/验证级创新（非新定理），但提供了论文"FD 稳健性" claim 的严格支撑，值得以"≤1 段正文 + 附录"收录。

---

## 7. 待验证（由 `685_direction2_experiment.json` 落实）

- 干净贪心集 `{asan, ubsan, tsan, compiler-warn}`，覆盖 58.49%。
- ε∈{0.01,0.03,0.05,0.10} 下：选择 Jaccard 1.0 / 0.99 / 0.96 / 0.92；干净真值掉点 0.00 / 0.03 / 0.11 / 0.26 pp。
- 详见 `685_direction2_report.md`。
