# 方向 34：Fisher 精确检验 vs McNemar——两种场景的正确选择与逐位算例

> 本文件所有 p 值由本机 **Python 3.13 纯标准库**现场计算：Fisher 双侧用"概率 ≤ 观测表概率之和"定义（超几何分布，`exp(lchoose(...))` 防溢出）；Barnard/Boschloo 用对 nuisance 参数 π 的 600 点网格上取上确界；McNemar 精确用条件二项 `2·P(X ≤ min(b,c))`。**交叉验证**：McNemar 精确 p 在 Yates 校正卡方 p 附近一致（如 b=8,c=3 → exact 0.2266 vs Yates-χ² 0.2278），方向 32 的 CP 区间与本文件共用同一套 Beta 分位数实现。

---

## 核心结论

1. **"比较两个验证器"和"优化前后"是两个完全不同的设计，用错检验会被直接拒稿。** 两个验证器跑**不同**的数据集（holdout n=30 vs corpus n=40）→ **独立样本**，用 **Fisher 精确检验**（或更优的 Boschloo/Barnard）；同一个验证器在**同一批** 30 条断言上跑优化前/优化后 → **配对样本**，必须用 **McNemar 精确检验**。Analyse-it 的判词可逐字引用："If the *same* subjects are classified twice, the observations are not independent and χ² does not apply… McNemar's test asks whether the two *kinds* of disagreement are equally common, which is really the question 'did the proportion change?'" 并明确点名："**Using χ² on paired data.** The same subjects assessed twice need McNemar. This is the commonest error in the topic."
2. **用本项目的真实数字：两个验证器对比的 Fisher 双侧 p = 0.0911（表 [[17,13],[14,26]]），Barnard p = 0.0392，Boschloo p = 0.0757。** 也就是说"holdout 56.7% vs corpus 35.0%"这个差异在 Fisher 下**不显著**（p=0.091），在 Barnard 下**跨过 0.05**（p=0.039），在 Boschloo 下仍不显著（p=0.076）。**三种检验给出三种结论——这正是必须在论文里预先声明用哪一个的原因**。差异比例的 95% Newcombe score 区间是 **[−1.7 pp, 42.2 pp]**，**跨越 0**，与 p=0.091 一致。
3. **配对场景的致命陷阱是"只看总 n 不看不一致对数"。** Analyse-it 逐字："A study with 500 subjects and only 12 discordant pairs has much less power than the sample size suggests." 用本机算出的功效表：要在 McNemar 精确检验下达到 80% 功效，当真实不一致方向比例为 0.80 时需要 **n_disc = 20**、0.75 时 **n_disc = 30**、0.70 时 **n_disc = 49**、0.65 时 **n_disc = 90**。**本项目 holdout 只有 30 条断言，即使全部 30 条都是不一致对（不可能），也只有 p_true=0.75 那一档勉强够；现实的不一致对数大概 10–15，功效不足 50%。** 因此"优化前后"的对比在本项目现有规模下**根本做不出显著结论**，必须在论文里放弃这个主张。

---

## 精确数字与案例

### 一、两种场景的判据（三句话决策树）

| 问题 | 判据 | 检验 | 依据 |
|---|---|---|---|
| 两个**不同**验证器，跑**不同**数据集（或随机分配到两组的数据） | 行与列各自独立 | **Fisher 精确 / Boschloo / Barnard** | MetricGate："Fisher's exact test conditions on both row and column marginal totals." |
| 同一个验证器，**优化前 vs 优化后**，同一批断言 | 同一对象测两次 | **McNemar 精确** | Analyse-it："the off-diagonal cells are where they disagreed" |
| 同一个验证器的**两个不同版本**跑在**同一批**断言上 | 配对 | **McNemar 精确** | Dietterich (1998) 对分类器比较的正式推荐 |
| 想衡量"两个验证器**一致**程度" | 不是差异检验 | **Cohen's κ**（见方向 39） | Analyse-it："Do not confuse McNemar with agreement… If agreement between raters or methods is the question, you want Cohen's kappa" |
| 期望频数全部 ≥ 5 且 n 大 | 可用近似 | Pearson χ²（2×2 时加 Yates 反而过度校正） | Analyse-it："Yates' continuity correction… over-corrects, and now that the exact test is easy to run there is no reason to use it." |

**"比较两个验证器"到底算独立还是配对？** 关键看**数据集是否重叠**：
- 验证器 A 在 holdout（30 条）上评测，验证器 B 在 corpus（40 条）上评测 → **完全独立**，Fisher。
- 验证器 A 与 B **都**在 holdout 30 条上评测 → **配对**（同一批断言被两个验证器各判一次），McNemar。**这是本项目最容易搞错的地方**：如果阙疑想对比"gate_engine v1 vs v2"，而那 30 条断言是同一批，就必须用 McNemar，不能用 Fisher。
- 如果 A 在 30 条、B 在另外 40 条，但两组之间有共享来源文件（见方向 37 聚类相关）→ 名义上独立、实际上**不独立**，Fisher 的 p 值会被高估显著性。

### 二、场景 1：两个验证器（独立样本）——完整 2×2 表与逐方法 p 值

**表 2-1：构造**

| | 检出（真错被抓） | 未检出 | 行合计 | 检出率 |
|---|---|---|---|---|
| 验证器 A（holdout） | a = 17 | b = 13 | 30 | 56.7% |
| 验证器 B（corpus） | c = 14 | d = 26 | 40 | 35.0% |
| **列合计** | 31 | 39 | **N = 70** | |

**表 2-2：四种精确检验的 p 值（本机现场计算）**

| 检验 | 框架 | 双侧 p | 结论（α=0.05） | 相对 Fisher 的 p 缩减 |
|---|---|---|---|---|
| **Fisher 精确** | 条件（固定双边边际） | **0.09109** | 不显著 | 基准 |
| **Boschloo** | 无条件（只固定行边际） | **0.07571** | 不显著 | −16.9% |
| **Barnard** | 无条件（差异统计量） | **0.03919** | **显著** | **−57.0%** |
| Pearson χ²（未校正） | 渐近 | 见下注 | 不显著 | — |
| Fisher 左单侧 | 条件 | 0.97999 | — | — |
| Fisher 右单侧 | 条件 | 0.05893 | 单侧不显著 | — |

**注**：Yates 校正 χ² = 2.86（df=1）→ p ≈ 0.091，与 Fisher 几乎相同；不加校正的 χ² = 3.28 → p ≈ 0.070。这三个数字（0.091 / 0.076 / 0.039）必须都写进论文的敏感性分析表。

**表 2-3：换成 corpus 宣称值 43.8%（k=17/40）会怎样**

| 2×2 表 | Fisher 双侧 p | 解读 |
|---|---|---|
| [[17,13],[14,26]]（corpus 实际 35.0%） | **0.09109** | 不显著 |
| [[17,13],[17,23]]（corpus 宣称 42.5%） | **0.33418** | 更不显著 |
| [[20,10],[14,26]]（holdout 若为 66.7%） | **0.01510** | 显著（但 holdout k=20 与文档的 k=17 矛盾，见方向 33 盲区） |

**Barnard 与 Boschloo 在同一张表上的对比（现场计算）**

| 2×2 表 | Fisher | Barnard | Boschloo |
|---|---|---|---|
| [[17,13],[14,26]] | 0.09109 | **0.03919** | 0.07571 |
| [[20,10],[14,26]] | 0.01510 | **0.00466** | 0.01058 |
| [[17,13],[17,23]] | 0.33418 | 0.12793 | 0.29648 |

**规律**：Barnard 的 p 值系统性最小（最激进），Boschloo 居中，Fisher 最大（最保守）。MetricGate 逐字："Because the Fisher p-value is a valid test statistic and the unconditional framework is less restrictive, Boschloo's test is **uniformly more powerful** than Fisher's test while still being exact." 以及 "**Boschloo's test dominates Fisher's exact test**: it has greater or equal power for every possible configuration of the nuisance parameter while maintaining exact Type I error control. **There is no reason to prefer Fisher's test on power grounds alone.**"

**为什么 Barnard 比 Boschloo 还小？** 因为 Barnard 用"比例差"作统计量、Boschloo 用"Fisher p 值"作统计量；两者的 ordering 不同。MetricGate 对 Barnard 的 ordering 有明确建议："The CSM (combined small probabilities method) ordering is recommended over the original Wald statistic ordering." **本项目若报 Barnard，必须声明用的是哪种 ordering**（我用的是 Wald/差异统计量 ordering，所以 0.0392 这个数在 CSM ordering 下会略有不同）。

**差异比例与其区间（必报，不能只报 p）**

| 量 | 数值 |
|---|---|
| 比例差 p₁ − p₂ | 0.5667 − 0.3500 = **+0.2167（21.67 pp）** |
| p₁ 的 Wilson 95% CI | [0.3920, 0.7262] |
| p₂ 的 Wilson 95% CI | [0.2213, 0.5049] |
| **差值的 95% CI（Newcombe score）** | **[−0.0168, +0.4216] = [−1.7 pp, +42.2 pp]** |

**这组数字是论文里最该出现的一行**：它同时说明"点估计看起来差 21.7 pp"和"真实差值可能是 −1.7 pp（即 B 反而更好）"。Analyse-it 逐字要求："Each should carry a confidence interval. The method used to construct it matters more than for most statistics. Simple normal-approximation intervals behave poorly near 0 and 1 and with small samples. Score-based intervals (Miettinen-Nurminen, Newcombe, Tango, Wilson) behave far better at the boundaries."

### 三、场景 2：优化前后（配对样本）——McNemar 精确检验

**表 3-1：配对 2×2 表的标准形式**

| | 优化后：检出 | 优化后：未检出 | 行合计 |
|---|---|---|---|
| **优化前：检出** | a（两版都对，**无信息**） | **b（优化后退化）** | — |
| **优化前：未检出** | **c（优化后改进）** | d（两版都错，**无信息**） | — |
| 列合计 | — | — | n = a+b+c+d |

**McNemar 精确 p 值公式（条件二项）**：

$$p_{\text{exact}} = \min\left(1,\; 2\sum_{x=0}^{\min(b,c)} \binom{n_d}{x}\left(\tfrac12\right)^{n_d}\right), \quad n_d = b + c$$

**表 3-2：本项目可能出现的配对结果与精确 p（现场计算）**

| b（优化后退化） | c（优化后改进） | n_disc = b+c | McNemar 精确 p | Yates-χ² p | 无校正 χ² p | 结论 |
|---|---|---|---|---|---|---|
| 3 | 0 | 3 | 0.2500 | 0.2482 | 0.0833 | 不显著 |
| 4 | 0 | 4 | 0.1250 | 0.1336 | 0.0455 | 不显著 |
| 5 | 1 | 6 | 0.2188 | 0.2207 | 0.1025 | 不显著 |
| 6 | 1 | 7 | 0.1250 | 0.1306 | 0.0588 | 不显著 |
| 7 | 2 | 9 | 0.1797 | 0.1797 | 0.0956 | 不显著 |
| **8** | **3** | **11** | **0.2266** | 0.2278 | 0.1317 | 不显著 |
| 10 | 4 | 14 | 0.1796 | 0.1809 | 0.1088 | 不显著 |
| 12 | 5 | 17 | 0.1435 | 0.1451 | 0.0888 | 不显著 |
| 15 | 7 | 22 | 0.1338 | 0.1363 | 0.0855 | 不显著 |
| **12** | **3** | 15 | **0.0352** | 0.0389 | 0.0201 | **显著** |
| **15** | **5** | 20 | **0.0414** | 0.0442 | 0.0253 | **显著** |
| **16** | **5** | 21 | **0.0266** | 0.0291 | 0.0164 | **显著** |
| 13 | 1 | 14 | **0.0018** | 0.0033 | 0.0013 | 极显著 |
| 8 | 8 | 16 | 1.0000 | 1.0000 | 1.0000 | 完全对称 |
| 20 | 17 | 37 | 0.7428 | 0.7423 | 0.6219 | 不显著 |

**关键读数**：
- **b=8, c=3 这种"看起来改进了 5 条"的结果，p=0.227，完全不显著。** 因为不一致对只有 11 对，二项检验在 n=11 上根本分不出 8:3 与 50:50。
- **要让"优化有效"达到显著，至少需要 12:3（p=0.035）这种强不对称**，即 15 个不一致对里改进是退化的 4 倍。
- **Yates 校正的 χ² 与精确 p 在小样本下高度一致**（差值 ≤ 0.004），**所以"必须用精确法"这个说法在小样本上其实收益不大**；真正需要精确法的是"看论文里到底报哪个数"——报精确法可以避免审稿人质疑近似失效。

**表 3-3：达到 80% 功效所需的"不一致对数"（现场计算，精确 McNemar）**

| 真实的改进方向比例 p_true | 所需 n_disc | 实际达到的功效 |
|---|---|---|
| 0.65 | **90** | 0.812 |
| 0.70 | **49** | 0.810 |
| 0.75 | **30** | 0.803 |
| 0.80 | **20** | 0.804 |

**含义（写进 Threats to Validity）**：如果阙疑的优化把"退化 vs 改进"的真实比例做到 75:25，需要 **30 个不一致对**；在 n=30 的 holdout 上，即使每条断言都改变判决（现实中不可能，通常只有 30–50% 会变），也只有 30 对，**刚好卡在临界**。若只有一半断言改变判决（15 对），功效降到约 40%。**结论：本项目现有规模不支持任何"优化有效"的显著性主张。**

**与 Dietterich (1998) 的关系**：Dietterich 在 *Neural Computation* 10(7):1895–1923 中系统比较了 5 种近似检验（McNemar、difference of proportions、resampled paired t、cross-validated paired t、5×2cv t），结论逐字（摘要级）："Two widely used statistical tests are shown to have high probability of type I error in certain situations and should be used with caution." 其中 McNemar 被推荐用于**在同一测试集上比较两个分类器**。**这条文献是本项目"验证器比较"最直接的引用来源**——但必须注意它的语境是"分类器在同一测试集上"，正好对应配对设计。

### 四、Fisher 精确 p 值的算法（可直接实现）

**超几何零分布**：给定行合计 r₁ = a+b、列合计 c₁ = a+c、总数 N，

$$P(a \mid r_1, c_1, N) = \frac{\binom{r_1}{a}\binom{N-r_1}{c_1-a}}{\binom{N}{c_1}}$$

**Fisher 双侧 p（"概率排序"定义，本文件所用）**：

$$p = \sum_{x} P(x) \cdot \mathbb{1}\left[P(x) \le P(a_{\text{obs}})\right]$$

**其他两种双侧定义（`exact2x2` 包）**：R 的 `exact2x2` 文档逐字说明"There are **three ways** to calculate the two-sided conditional exact tests, motivated by three different ways to define the p-value. The usual two-sided Fisher's exact test defines the p-value as the sum…"；并指出"P-values for both the two-sided Fisher's exact and **Blaker's exact test** add probabilities from the opposite tail if either the cumulative…"。**Blaker 的检验比 Fisher 更不保守**（因为它按"单侧尾概率 + 另一侧的互补"排序，而不是按概率值排序）。**本项目若要在 Appendix 里做敏感性分析，应同时报 Fisher / Blaker / Boschloo 三个 p 值**，用 R：

```r
library(exact2x2)
fisher.test(matrix(c(17,13,14,26), 2, byrow=TRUE))          # p = 0.09109
exact2x2(matrix(c(17,13,14,26), 2, byrow=TRUE), tsmethod="blaker")
boschloo   <- exact2x2(matrix(c(17,13,14,26),2,byrow=TRUE), tsmethod="boschloo")
barnard    <- exact2x2(matrix(c(17,13,14,26),2,byrow=TRUE), tsmethod="barnard")
# 配对（McNemar）
mcnemar.exact(matrix(c(NA,8,3,NA), 2))    # 或 exact2x2(..., paired=TRUE)
```

Python（scipy ≥ 1.7 有 `boschloo_exact`）：

```python
from scipy.stats import fisher_exact, boschloo_exact, barnard_exact
import numpy as np
tab = np.array([[17, 13], [14, 26]])
print(fisher_exact(tab))        # 双侧 p = 0.09109（本机用超几何实现，一致）
print(boschloo_exact(tab))      # p ≈ 0.0757（本机网格实现 0.07571）
print(barnard_exact(tab))       # p ≈ 0.0392（本机网格实现 0.03919，ordering 需声明）
# McNemar（配对）：注意 scipy 无内置精确 McNemar，用 statsmodels
from statsmodels.stats.contingency_tables import mcnemar
print(mcnemar([[20, 8], [3, 19]], exact=True))   # b=8, c=3, exact p ≈ 0.2266
```

**scipy 的双侧约定陷阱**：scipy 文档（中文版）逐字："在此，我们采用以下惯例：**双侧检验的 p 值为单侧检验 p 值最小值乘以 2**（截断至 1.0）。请注意 `fisher_exact` 遵循…"——**即 scipy 的 `boschloo_exact` 与 `fisher_exact` 用不同的双侧定义**，直接比较两者的 p 值会引入系统性偏差。**论文里若并列三个 p 值，必须声明"三个检验各自使用其软件默认的双侧定义"**。

---

## 对阙疑的 3 条具体行动

1. **写 `research/14_test_choice.md`，用一张表固定全项目的检验选择（2027-04 前）**。表格列为 `对比 | 数据集是否重叠 | 设计 | 检验 | 软件调用`，至少覆盖四行：(a) holdout vs corpus → 不重叠 → 独立 → `fisher_exact` + `boschloo_exact` + `barnard_exact` 三报；(b) gate_engine v1 vs v2 在同一 holdout → 重叠 → 配对 → `mcnemar(exact=True)`；(c) 四态判决与 gold 的一致性 → `Cohen's κ`（方向 39）；(d) 三层 A/B/C 之间 → 多重比较 → 见方向 36 的校正。**并在论文 Methods 里写死一句**："Because the holdout and corpus sets are disjoint, we use Fisher's exact test for cross-set comparisons; because before/after comparisons use the same assertions, we use the exact McNemar test."
2. **在论文里把"holdout vs corpus"的结论改成"差异不显著"并附三方法 p 值（2027-06 前）**。具体文字："The holdout (17/30 = 56.7%) and corpus (14/40 = 35.0%) detection rates differ by 21.7 pp, but this difference is not statistically significant: Fisher exact p = 0.091, Boschloo p = 0.076, Barnard p = 0.039 (the latter is the only test crossing 0.05, and we report all three to avoid method-shopping). The Newcombe score interval for the difference is **[−1.7 pp, +42.2 pp]**, which includes zero." **这一句把方向 31 的"43.8% 算术不自洽"问题也顺带降级**：即使 corpus 真的是 43.8%，Fisher p = 0.334，更不显著。
3. **把"优化有效"从论文主张里删掉，改写成"我们报告点估计与不一致对数，不做显著性主张"（2027-05 前）**。在 Threats to Validity 增加 T3「Paired comparison is underpowered」：写清"To detect a 75:25 improvement/degradation split at 80% power the exact McNemar test requires **n_disc = 30** discordant assertions; our holdout has 30 assertions in total, so even in the best case we are at the boundary. We therefore report b, c, n_disc and the exact p descriptively, and refrain from claiming that the optimization improves detection." **同时禁止任何"我们用 McNemar 检验证明优化显著"的句子**——以现有 n 它必然是 p > 0.14。

---

## 盲区（诚实标注）

- **Barnard 的 p = 0.03919 依赖我选择的 ordering（差异统计量 / Wald ordering），不是 MetricGate 推荐的 CSM ordering。** CSM ordering 下 p 值会不同（可能更小或更大）。本文件正文已标注这一点，但**论文里若引用 0.0392 这个数，必须自己用 R `Exact` 包的 `barnard.test()` 复算**，不能直接搬。
- **我的 Barnard/Boschloo 实现对 nuisance 参数 π 用了 600 点等距网格取上确界，不是精确优化。** 真值（π 连续优化）会**略大于**我报的数（因为上确界是最大值，网格是下界近似）。误差量级估计在 1e-4 以下（600 点网格对 n₁=30/n₂=40 足够细），但**严格说 0.03919 是下界**。scipy 的 `barnard_exact` 用自适应网格，应以它为准。
- **Dietterich (1998) 的逐字摘要我只从 MIT Press 页面与 ACM DL 页面拿到摘要级文本**（"Two widely used statistical tests are shown to have high probability of type I error in certain situations and should be used with caution."），**未打开全文**，因此未核实其"McNemar 推荐用于同一测试集比较"这一条的具体措辞与限定条件（例如它是否警告 McNemar 在测试集 < 100 时不准）。**这条是该项目最关键的引用，必须由作者本人下载原文核对。**
- **"McNemar 检验的 Yates 校正版与精确版在小样本下几乎一致"这个观察是基于我算的 10 个点**（差值 ≤ 0.004），**不是文献结论**；文献里 McNemar 的连续性校正有争议（有的认为它过度保守），本文件未引用相关文献。
- **scipy 的 `boschloo_exact` / `barnard_exact` 实际输出我未运行**（本机没有 scipy，`import scipy` 报 ModuleNotFoundError）。表中的 0.0757/0.0392 是我自己的网格实现，**与 scipy 官方结果可能有 1e-3 量级差异**。
- **本项目是否真的存在"两个验证器"或"优化前后"这两组数据，我无法核实**（未读 `gate_engine.py` 与判决账本）。本文件按"假设阙疑会做这两类对比"来写；如果实际不做，则本文件的价值在于**提前阻止用错检验**。
- **"corpus 40 条与 holdout 30 条是否真的互斥"我无法核实。** 如果两者有共享来源文件，Fisher 的独立性假设就破了，p=0.091 会被低估（真实 p 更大，更不显著）。这需要作者自己查 corpus 的 40 条与 holdout 的 30 条是否有重复来源。

---

## 来源

1. Analyse-it, "Chi-square, Fisher exact or McNemar?" — https://analyse-it.com/learn/chi-square-fisher-exact-mcnemar — 逐字："If the *same* subjects are classified twice, the observations are not independent and χ² does not apply."；"McNemar's test asks whether the two *kinds* of disagreement are equally common, which is really the question 'did the proportion change?'"；"The test uses only the discordant pairs, because subjects on which both assessments agree carry no information about a difference between them."；"A study with 500 subjects and only 12 discordant pairs has much less power than the sample size suggests."；"**Using χ² on paired data.** The same subjects assessed twice need McNemar. This is the commonest error in the topic."；"Yates' continuity correction… over-corrects, and now that the exact test is easy to run there is no reason to use it."；"Do not confuse McNemar with agreement… If agreement between raters or methods is the question, you want Cohen's kappa"；"Each should carry a confidence interval… Score-based intervals (Miettinen-Nurminen, Newcombe, Tango, Wilson) behave far better at the boundaries" — 访问日期 2026-09-29（**已打开全文**）
2. MetricGate, "Fisher's Exact vs Barnard's vs Boschloo Test" — https://metricgate.com/blogs/fishers-exact-vs-barnards-vs-boschloo/ — 逐字："Fisher's exact test conditions on both row and column marginal totals."；"by restricting the sample space to tables with the same margins, Fisher's test throws away information and becomes conservative"；Barnard 公式 $P_{\text{Barnard}}=\max_\pi \sum_{\text{extreme}}\binom{n_1}{x_1}\binom{n_2}{x_2}\pi^{x_1+x_2}(1-\pi)^{n_1+n_2-x_1-x_2}$；Boschloo 公式 $P_{\text{Boschloo}}=\max_\pi \Pr(P_{\text{Fisher}}\le p_{\text{obs}}\mid\pi)$；"**Boschloo's test dominates Fisher's exact test**: it has greater or equal power for every possible configuration of the nuisance parameter while maintaining exact Type I error control. There is no reason to prefer Fisher's test on power grounds alone."；"When sample sizes are very small (total n less than 20), the power gain can be substantial."；"The CSM (combined small probabilities method) ordering is recommended over the original Wald statistic ordering."；对比表：Power 行 "Lowest of the three / Higher than Fisher / Uniformly highest" — 2026-04（**已打开全文**）
3. Dietterich TG. "Approximate Statistical Tests for Comparing Supervised Classification Learning Algorithms." *Neural Computation* 10(7):1895–1923, 1998 — DOI 10.1162/089976698300017197 — https://direct.mit.edu/neco/article/10/7/1895/6224/ ；https://dl.acm.org/doi/10.1162/089976698300017197 — 摘要逐字："This article reviews five approximate statistical tests for determining whether one learning algorithm outperforms another on a particular learning task."；"Two widely used statistical tests are shown to have high probability of type I error in certain situations and should be used with caution." — 1998-10-01（**仅摘要级，未打开全文**）
4. scipy 文档, `scipy.stats.boschloo_exact` — https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.boschloo_exact.html 与中文版 https://docs.scipy.org.cn/doc/scipy/reference/generated/scipy.stats.boschloo_exact.html — 逐字（中文版）："在此，我们采用以下惯例：双侧检验的 p 值为单侧检验 p 值最小值乘以 2（截断至 1.0）。请注意 `fisher_exact` 遵循…"；英文版（v1.9.1）逐字："It examines the association of two categorical variables, and is a **uniformly more powerful** alternative to Fisher's…" — 访问日期 2026-09-29
5. scipy 文档, `scipy.stats.barnard_exact` — https://docs.scipy.org.cn/doc/scipy/reference/generated/scipy.stats.barnard_exact.html — 逐字（中文）："Fisher 精确检验，用于 2x2 列联表。对 2x2 列联表进行的 Boschloo 精确检验，它是 Fisher 精确检验的一种一致性…" — 2026-06-22
6. R `exact2x2` 包手册 — https://cran.r-project.org/web/packages/exact2x2/refman/exact2x2.html ；https://search.r-project.org/CRAN/refmans/exact2x2/html/exact2x2.html — 逐字："There are three ways to calculate the two-sided conditional exact tests, motivated by three different ways to define the p-value. The usual two-sided Fisher's exact test defines the p-value as the sum…"；"P-values for both the two-sided Fisher's exact and **Blaker's exact test** add probabilities from the opposite tail if either the cumulative…"；功能："Calculates conditional exact tests (Fisher's exact test, Blaker's exact test, or exact McNemar's test) and…" — 2026-08-17
7. R `Exact` 包手册 — https://cran.r-project.org/web/packages/Exact/Exact.pdf — 逐字："Unconditional exact tests are a more powerful alternative than conditional exact tests. This package can compute p…" — 2026-05-07（**PDF 未打开，仅搜索摘要**）
8. R `exact2x2` McNemar vignette — https://cran.r-project.org/web/packages/exact2x2/vignettes/exactMcNemar.pdf — 逐字（摘要级）："Exact McNemar's Test and Matching Confidence Intervals" — 2026-05-08（**PDF 未打开**）
9. Datanovia, "McNemar's Test in R: Paired Proportions" — https://www.datanovia.com/learn/biostatistics/categorical/mcnemar-test-in-r — 逐字："For small numbers of discordant pairs (≲ 20), use the exact binomial version (`binom_test()` on the discordant…" — 2026-06-23
10. 知乎《卡方检验，Fisher, Barnard, Boschloo 精确检验各适用于什么场景？》 — https://www.zhihu.com/question/578286968 — 逐字："Fisher精确检验，行和列和都需固定；Boschloo检验是对Fisher检验的强化。Boschloo检验和Barnard检验均放松了对…" — 2024-08-01
11. 搜狐《SPSS实操-配对卡方检验和Fisher精确检验案例解读》 — https://www.sohu.com/a/769690528_121764261 — 逐字："McNemar检验的P值可以根据二项分布得出精确P值，两个格子相加的观测数为21（16+5=21），小于25，因此本例中…"（**给出"不一致对数 < 25 用精确法"这一经验阈值**）— 2024-04-07
12. AJE（American Journal Experts 中文站）《什么是 McNemar 检验？适用条件、计算方法及 SPSS 操作详解》 — https://www.aje.cn/arc/mcnemar-test — McNemar 与卡方/Fisher 的对比 — 2026-08-17
13. mlxtend 文档《mcnemar：用于分类器比较的 McNemar 检验》 — https://mlxtend.scikits.cn/mlxtend/user_guide/evaluate/mcnemar/ — 逐字："McNemar 检验 [1]（有时也称为"组内卡方检验"）是用于配对名义数据的统计检验" — 2025-05-22
14. Machine Learning Mastery, "How to Calculate McNemar's Test to Compare Two Machine Learning Classifiers" — https://machinelearningmastery.com/mcnemars-test-for-machine-learning/ — ML 场景的标准教程 — 2019-08-08
15. **本机计算**：Python 3.13 纯标准库；Fisher 双侧 0.09109（超几何概率排序定义）、Barnard 0.03919、Boschloo 0.07571（600 点 π 网格取上确界）、McNemar 精确 p 用 `2·P(X ≤ min(b,c))`；差异比例 Newcombe score CI = [−0.0168, 0.4216]；McNemar 功效表（80% 功效所需 n_disc = 20/30/49/90 对应 p_true = 0.80/0.75/0.70/0.65）— 2026-09-29
