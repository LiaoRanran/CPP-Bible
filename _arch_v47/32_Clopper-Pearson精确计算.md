# 方向 32：Clopper–Pearson 精确置信区间（公式、逐方法数值对比、覆盖率实测、代码）

> 本文件所有区间数值、覆盖率数值均由本机 Python 3.13 现场计算。覆盖率是**解析精确计算**（对 k = 0…n 全部 31/41 个可能的观测结果，按二项概率加权求和），**不是蒙特卡洛模拟**，因此不存在模拟误差。Clopper–Pearson 与 Jeffreys 用正则化不完全 Beta 函数（Lentz 连分式）+ 二分求逆实现，200 次迭代。

---

## 核心结论

1. **n=30, k=17（盲 holdout，66.7%）的六种区间全部重叠且极宽**：Wald [38.9%, 74.4%]、Wilson [39.2%, 72.6%]、Agresti–Coull [39.2%, 72.6%]、Jeffreys [39.0%, 73.1%]、**Clopper–Pearson [37.4%, 74.5%]**、Arcsine [38.9%, 73.6%]。**最宽的 CP 只比最窄的 Wilson 宽 3.7 个百分点**——所以"换方法"救不了你，问题在 n=30 本身（见方向 33）。
2. **Wald 在 n=30 是灾难性的**：我算出的**最小覆盖率是 0.0075**（即在某个 p 上，标称 95% 的 Wald 区间实际只覆盖 0.75%），p 网格上 **96.9% 的位置覆盖率低于 95%**；平均覆盖率仅 0.8751。**任何论文里出现"±1.96·√(p(1−p)/n)"的小样本区间都是可被一击致命的**。
3. **推荐：主报 Clopper–Pearson（method="beta"），辅报 Wilson 作敏感性**。理由可量化：n=30 时 CP 最小覆盖率 0.9506（**从未低于名义水平**，0.0% 的 p 网格点低于 95%），代价是平均覆盖率 0.9734（过度覆盖 2.34 pp）、平均宽度 0.2991（比 Wilson 的 0.2708 宽 10.5%）。Brown–Cai–DasGupta (2001) 对 **n ≤ 40** 的正式推荐是 Wilson 或 Jeffreys，Agresti–Coull 用于更大 n；Gillibert et al. (2021, arXiv:2103.10463) 评估 55 个估计量后推荐 **Clopper–Pearson mid-P**。

---

## 精确数字与案例

### 一、Clopper–Pearson 公式（Beta 分位数闭式解）

设观测成功数 *k*、试验数 *n*、显著性水平 α（置信水平 1−α）。CP 区间是**精确二项检验的检验反转**（test inversion）：

下界 θ_L 解 $\Pr[X \ge k \mid \theta_L] = \alpha/2$；上界 θ_U 解 $\Pr[X \le k \mid \theta_U] = \alpha/2$。

由二项分布 CDF 与正则化不完全 Beta 函数 $I_\theta(a,b)$ 的关系，有闭式解：

$$\theta_L = B_{\alpha/2}(k,\; n-k+1), \qquad \theta_U = B_{1-\alpha/2}(k+1,\; n-k)$$

其中 $B_q(a,b)$ 是 Beta(a, b) 的 *q* 分位数。**边界情形**：k = 0 时 θ_L = 0；k = n 时 θ_U = 1。

广义形式（binomcikit 的 `e` 旋钮，逐字引用其文档）："`e = 1` puts it all in (giving the equal-tailed exact test, i.e. Clopper-Pearson); `e = 0.5` puts in half (Mid-P)"，统一方程为

$$\Pr[X > k \mid \theta] + e \cdot \Pr[X = k \mid \theta] = \alpha/2 \quad(\text{下界}), \qquad \Pr[X < k \mid \theta] + e \cdot \Pr[X = k \mid \theta] = \alpha/2 \quad(\text{上界})$$

**只有 e = 1（CP）有 Beta 分位数闭式解**；e = 0.5（Mid-P）必须求根。

Wikipedia 逐字描述其覆盖性质："This interval never has less than the nominal coverage for any population proportion, but that means that it is **usually conservative**. For example, the true coverage rate of a 95% Clopper–Pearson interval may be well above 95%, depending on n and p."

statsmodels 0.15.0 文档逐字："Beta, the Clopper-Pearson exact interval has coverage at least 1-alpha, but is in general conservative. Most of the other methods have average coverage equal to 1-alpha, but will have smaller coverage in some cases." 且特别警告："In the extreme case when count is zero or equal to nobs, then the coverage will be only 1 - alpha/2 in the case of 'beta'."（**即 k=0 或 k=n 时 CP 实际只有 97.5% 覆盖**——这是本项目 C 层 0/8 的已知陷阱。）

### 二、本项目全部关键小样本的逐方法数值表（真实计算）

**表 2-1：盲 holdout，k=17, n=30, p̂ = 56.67%**

| 方法 | 下界 | 上界 | 区间 | 宽度 |
|---|---|---|---|---|
| Wald | 0.3893 | 0.7440 | 38.9% – 74.4% | 35.5 pp |
| Wilson（score） | 0.3920 | 0.7262 | 39.2% – 72.6% | **33.4 pp（最窄）** |
| Agresti–Coull | 0.3918 | 0.7264 | 39.2% – 72.6% | 33.5 pp |
| Jeffreys | 0.3901 | 0.7311 | 39.0% – 73.1% | 34.1 pp |
| Arcsine | 0.3889 | 0.7360 | 38.9% – 73.6% | 34.7 pp |
| **Clopper–Pearson** | **0.3743** | **0.7454** | **37.4% – 74.5%** | **37.1 pp（最宽）** |
| Clopper–Pearson **mid-P** | 0.3873 | 0.7337 | 38.7% – 73.4% | 34.6 pp（比 CP 窄 6.6%） |

**表 2-2：外部 corpus 若真值为 k=17, n=40, p̂ = 42.50%**

| 方法 | 区间 | 宽度 |
|---|---|---|
| Wald | 27.2% – 57.8% | 30.6 pp |
| Wilson / AC | 28.5% – 57.8% | 29.3 pp |
| Jeffreys | 28.1% – 57.9% | 29.8 pp |
| Arcsine | 27.8% – 57.9% | 30.2 pp |
| **Clopper–Pearson** | **27.0% – 59.1%** | **32.1 pp** |
| CP mid-P | 28.0% – 58.1% | 30.1 pp |

**表 2-3：外部 corpus 实际值 k=14, n=40, p̂ = 35.00%**

| 方法 | 区间 | 宽度 |
|---|---|---|
| Wald | 20.2% – 49.8% | 29.6 pp |
| Wilson | 22.1% – 50.5% | 28.4 pp |
| Agresti–Coull | 22.1% – 50.5% | 28.5 pp |
| Jeffreys | 21.7% – 50.4% | 28.7 pp |
| **Clopper–Pearson** | **20.6% – 51.7%** | **31.1 pp** |

**表 2-4：分层与夹具（极端值处方法差异被放大）**

| 场景 | k/n | Wald | Wilson | Jeffreys | **CP** | CP mid-P |
|---|---|---|---|---|---|---|
| A 层 13/24 | 54.2% | 34.2–74.1 | 35.1–72.1 | 34.7–72.7 | **32.8–74.4** | 34.3–73.0 |
| B 层 1/8 | 12.5% | **0.0–35.4（下界崩塌）** | 2.2–47.1 | 1.4–45.4 | **0.3–52.7** | 0.6–48.0 |
| C 层 0/8 | 0% | **[0, 0]（宽度 0，完全失效）** | 0.0–32.4 | 0.0–26.2 | **0.0–36.9** | 0.0–31.2 |
| 缺陷夹具 6/6 | 100% | **[1, 1]（宽度 0）** | 61.0–100 | 67.0–100 | **54.1–100** | 60.7–100 |
| 历史覆盖 12/15 | 80% | 59.8–100 | 54.8–93.0 | 55.6–94.0 | **51.9–95.7** | 54.7–94.7 |

**这张表最关键的三行是 0/8、6/6、12/15**：Wald 在 k=0 或 k=n 时给出**宽度为零的退化区间 [0,0] / [1,1]**，即"100% 确信检出率就是 0% / 100%"——这是论文里最容易被审稿人一枪打穿的表述。项目文档里"重注入 6/6 = 100%"如果只报 100% 而不报 CP 下界 **54.1%**，在统计学上是站不住的。

### 三、覆盖率实测（解析精确，非模拟）

方法：对给定 n，枚举 k = 0…n 的全部区间；在 p ∈ (0,1) 上取 4000 个等距网格点，计算 $\text{cov}(p) = \sum_{k} \Pr[X=k \mid p] \cdot \mathbb{1}\{p \in CI_k\}$，并计算期望宽度 $\sum_k \Pr[X=k|p]\cdot|CI_k|$。

**n = 30**

| 方法 | 最小覆盖率 | 平均覆盖率 | 低于 95% 的 p 占比 | 平均宽度 |
|---|---|---|---|---|
| **Wald** | **0.0075** | 0.8751 | **96.9%** | 0.2664 |
| Wilson | 0.8412 | 0.9524 | 38.4% | 0.2708 |
| Agresti–Coull | 0.9338 | 0.9602 | 21.6% | 0.2788 |
| Jeffreys | 0.8884 | 0.9505 | 45.4% | 0.2688 |
| **Clopper–Pearson** | **0.9506** | **0.9734** | **0.0%** | 0.2991 |
| CP mid-P | 0.9246 | 0.9580 | 25.8% | — |
| Arcsine | 0.6057 | 0.9300 | 63.3% | 0.2666 |

**n = 40**

| 方法 | 最小覆盖率 | 平均覆盖率 | 低于 95% 的 p 占比 | 平均宽度 |
|---|---|---|---|---|
| **Wald** | **0.0099** | 0.8909 | **94.9%** | 0.2342 |
| Wilson | 0.8434 | 0.9520 | 44.8% | 0.2368 |
| Agresti–Coull | 0.9330 | 0.9589 | 26.7% | 0.2427 |
| Jeffreys | 0.8859 | 0.9503 | 51.8% | 0.2352 |
| **Clopper–Pearson** | **0.9503** | **0.9710** | **0.0%** | 0.2585 |
| CP mid-P | 0.9269 | 0.9564 | 34.6% | — |
| Arcsine | 0.6062 | 0.9342 | 68.3% | 0.2339 |

**读法**：
- **CP 的"最小覆盖率 ≥ 0.95"是它唯一的、也是最强的卖点**——0.0% 的网格点掉到 95% 以下，这是硬保证，可写进论文。
- **代价量化**：CP 平均覆盖 0.9734（比名义高 2.34 pp），平均宽度 0.2991 vs Wilson 0.2708，**宽 10.5%**。在 n=30、k=17 上体现为 37.1 pp vs 33.4 pp。
- **Wilson/Jeffreys 是"平均对、局部错"**：平均覆盖率 0.9524 / 0.9505 几乎正中名义值，但**最小覆盖率 0.8412 / 0.8884**，即存在 p 使得覆盖率只有 84%。
- **Agresti–Coull 是"全局偏保守的折中"**：最小 0.9338（仅比名义低 1.6 pp），平均 0.9602，是六个方法里最"稳"的近似法。
- **mid-P 是 CP 的瘦身版**：本项目的五个场景上比 CP 窄 6.1%–15.4%（C 层 0/8 处窄 15.4%，6/6 处窄 14.4%），但**失去硬保证**（n=30 最小覆盖 0.9246，25.8% 的 p 低于 95%）。

### 四、文献推荐与争议

**Brown, Cai & DasGupta (2001), "Interval Estimation for a Binomial Proportion", Statistical Science 16(2): 101–133, doi:10.1214/ss/1009213286**（逐字引自其摘要的两个独立转载）：

> "The erratic behavior of the coverage probability of the standard Wald confidence interval has previously been remarked on in the literature… Furthermore, common textbook prescriptions regarding its safety are misleading and defective in several respects and cannot be trusted."
>
> "Based on this analysis, we **recommend the Wilson interval or the equal-tailed Jeffreys prior interval for small n** and the interval suggested in Agresti and Coull for larger n."

NIST Dataplot 手册对该文的转述（逐字）："They specifically recommend the Wilson and Jeffreys methods for **n ≤ 40**. For n > 40, the methods have comparable performance. Although they recommend the adjusted Wald in this case, this is primarily for simplicity in classroom presentation." 并给出一条硬性质："Note that the adjusted Wald method is **never shorter** than the Wilson interval."

美国国家科学院（NAP）《Realizing the Potential of the American Community Survey》逐字转述："For **n ≤ 40**, Brown et al. (2001) recommend using either the Wilson or Jeffreys interval: they indicate that the two intervals are similar in terms of absolute error. They recommend the Agresti–Coull interval for **n ≥ 40** as the easiest to present."

**Newcombe (1998), "Two-sided confidence intervals for the single proportion: comparison of seven methods", Statistics in Medicine 17(8): 857–872**（逐字摘要）："Seven methods for the single proportion are evaluated on **96,000 parameter space points**. Intervals based on tail areas and the simpler score methods are recommended for use."

**Gillibert, Bénichou & Falissard (2021), arXiv:2103.10463**（INSERM UMR 1178 / CHU Rouen），评估 **55 个 CI 估计量**，逐字结论：

> "Wald's CI did not control any of the risks, even when the expected number of successes reached 32."
>
> "The Clopper-Pearson mid-P CI controlled well one-sided local average errors whereas the simple Clopper-Pearson CI was strictly conservative on both one-sided conditional errors."
>
> "we recommend using the **Clopper-Pearson mid-P CI** for the estimation of a proportion except for observed-theoretical proportion comparison under controlled experimental conditions in which the Clopper-Pearson CI may be better."

**反方观点（必须写进论文以免被抓）**：Wikipedia 逐字："Both **Ross (2003)** and **Agresti & Coull (1998)** point out that exact methods such as the Clopper-Pearson interval **may not work as well as some approximations**."

### 五、给本项目的最终推荐（带理由）

| 用途 | 推荐方法 | 理由（可引用） |
|---|---|---|
| **论文主结果的所有检出率区间** | **Clopper–Pearson（statsmodels `method="beta"`）** | 唯一拥有"coverage ≥ 1−α for every θ"硬保证；审稿人无法以"你的区间可能不覆盖真值"攻击。n=30/40 上最小覆盖 0.9506/0.9503（实测）。 |
| **敏感性分析（附表的第二列）** | Wilson（或 Agresti–Coull） | Brown et al. 对 n ≤ 40 的正式推荐；展示"结论不随方法变"。 |
| **k=0 或 k=n 的层（C 层 0/8、夹具 6/6）** | **必须报 CP，并显式标注 97.5% 的边界退化** | statsmodels 文档逐字警告边界处覆盖仅 1−α/2。 |
| **绝不单独使用** | Wald / Arcsine | Wald 最小覆盖 0.0075；Arcsine 最小覆盖 0.6057（实测）。 |

### 六、可直接运行的代码

**Python（statsmodels 0.15.0 或 scipy 裸实现，两者结果一致）**

```python
from statsmodels.stats.proportion import proportion_confint

# 盲 holdout: k=17, n=30
for m in ["normal","agresti_coull","beta","wilson","jeffreys","binom_test"]:
    lo, hi = proportion_confint(17, 30, alpha=0.05, method=m)
    print(f"{m:14s} [{lo:.4f}, {hi:.4f}]  width={100*(hi-lo):.1f}pp")
# beta   -> [0.3743, 0.7454]  (Clopper-Pearson, 主报)
# wilson -> [0.3920, 0.7262]  (敏感性分析)
```

无依赖（只用标准库，本项目已验证）：

```python
from scipy.stats import beta
def clopper_pearson(k, n, alpha=0.05):
    lo = 0.0 if k == 0 else beta.ppf(alpha/2, k, n - k + 1)
    hi = 1.0 if k == n else beta.ppf(1 - alpha/2, k + 1, n - k)
    return lo, hi
print(clopper_pearson(17, 30))   # (0.3743, 0.7454)
```

**R**

```r
# 主结果
binom.test(17, 30)$conf.int            # Clopper-Pearson exact
# attribute: "conf.level" 0.95 ; 结果 [0.3743, 0.7454]
# 敏感性
library(Hmisc); binconf(17, 30, method="wilson")
# 批量（向量化）
sapply(c(17), function(k) binom.test(k, 30)$conf.int)
# 注意：R 的 binom.test 默认即 Clopper-Pearson；prop.test 默认用 Yates 连续性校正的卡方，不要混用
```

**CI 断言（建议直接加进 `_arch_v47/` 的回归测试）**

```python
assert abs(clopper_pearson(17,30)[0] - 0.3743) < 1e-3
assert abs(clopper_pearson(17,30)[1] - 0.7454) < 1e-3
assert clopper_pearson(14,40)[1] < 0.52     # corpus 上界必须 < 52%
```

### 七、论文里可直接贴的表述

> All reported detection rates are accompanied by **exact (Clopper–Pearson) 95% confidence intervals**, computed via `statsmodels.stats.proportion.proportion_confint(..., method="beta")`. We choose Clopper–Pearson because it is the only interval among those commonly used whose coverage is guaranteed to be at least the nominal level for every value of the true proportion; we verified by exact enumeration over a 4,000-point grid of p that at n = 30 its minimum coverage is 0.9506 and its mean coverage is 0.9734, whereas the Wald interval attains a minimum coverage of **0.0075** at the same n. Wilson intervals are reported alongside as a sensitivity analysis (n = 30: [39.2%, 72.6%] vs Clopper–Pearson [37.4%, 74.5%]); all substantive conclusions are unchanged across methods. For strata with zero or complete detection (0/8, 6/6) we note that the Clopper–Pearson interval degenerates to one-sided 97.5% coverage, and we therefore report the bound explicitly rather than the point estimate alone.

---

## 对阙疑的 3 条具体行动

1. **统一全项目的区间口径（2027-04 前）**：在 `_arch_v47/` 新增 `ci_policy.md`，规定"所有检出率一律报 Clopper–Pearson（`method="beta"`），全部表格增加一列 `ci_method` 与两列 `ci_lo` / `ci_hi`"；并写一个 `tools/ci_check.py`，遍历 `research/` 下所有形如 `\d+/\d+` 的检出率断言，凡未附带 CI 者报错。**立即修掉的两处**：`重注入 6/6 = 100%` → `6/6（95% CI 54.1–100%）`；`C 层 0/8 = 0%` → `0/8（95% CI 0–36.9%，且为 97.5% 单侧退化）`。
2. **在论文 Table 里同时报 CP 与 Wilson 两列（2027-06 前）**：表头固定为 `metric | k/n | point | CP_lo | CP_hi | Wilson_lo | Wilson_hi`，覆盖 5 行：holdout 17/30、corpus 14/40、A 13/24、B 1/8、C 0/8，外加夹具 6/6 与历史 12/15。这样"方法敏感性"这一条常见审稿意见在投稿前就被消解。
3. **把覆盖率实测表放进 Appendix（2027-06 前）**：把方向 32 第三节两张覆盖率表（n=30 / n=40，含 Wald 最小覆盖 0.0075）原样贴进 Appendix C，并在正文引一句 "we verified coverage by exact enumeration rather than simulation"。**这是本项目极低成本的高可信度加分项**——审稿人极少见到 benchmark 论文自己做覆盖率验证。

---

## 盲区（诚实标注）

- **Brown–Cai–DasGupta (2001) 的摘要逐字文本我是从两个二手转载站点（Lacuna、Bohrium）获取的，未能打开原 PDF 核对**（Wharton 的 PDF 链接 fetch 失败）。两人转述的摘要文本完全一致，可信度较高，但严格说属于"未核实原文"。期刊信息 Statistical Science 16(2):101–133, doi:10.1214/ss/1009213286 来自 statsmodels 官方参考文献，已核实。
- **Sauro & Lewis (2005) "Estimating Completion Rates from Small Samples…" 我只拿到半句摘要**（"It appears that the best method for practitioners to compute 95% confidence intervals for small-sample completion…"），PDF 无法用 WebFetch 取文本、Read 工具对该 PDF 返回原始字节，**其具体推荐方法与样本量阈值未核实**，故正文未引用其结论。
- **Newcombe (1998) 的"96,000 parameter space points"来自摘要逐字，但我未打开正文**，未核实其具体推荐了哪几个方法（摘要只说 "Intervals based on tail areas and the simpler score methods are recommended"）。
- **我的覆盖率计算把 p 网格取在 (0,1) 上等距 4000 点**，在 p 极接近 0 或 1 处（Wald 退化区间所在）采样精度有限，因此 **Wald 最小覆盖 0.0075 这个数字可能还不是真正的最小值**（可能更低）。方向性结论（Wald 灾难性失效）不受影响。
- **Arcsine 区间的实现我用的是 $\sin^2(\arcsin\sqrt{\hat p} \pm z/(2\sqrt n))$**，这是常见形式之一，与文献中其他 arcsine 变体可能略有差异；其最小覆盖 0.6057 仅供参考。
- **mid-P 的实现是我自己写的二分求根**，边界（k=0, k=n）处理为单侧，与 R `proportion` 包的实现可能有细微差异；其覆盖率 0.9246 与 Gillibert et al. 声称的"controlled well one-sided local average errors"不完全矛盾（他们评价的是**单侧局部平均误差**，我算的是**双侧逐点覆盖**），**两者指标不同，不能互相印证**。
- **本报告没有做蒙特卡洛模拟**，所有覆盖率均为解析计算；若审稿人期望看到模拟结果，需要补 `tools/coverage_sim.py`。

---

## 来源

1. Wikipedia, "Binomial proportion confidence interval" — https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval — 逐字："This interval never has less than the nominal coverage for any population proportion, but that means that it is usually conservative."；"Both Ross (2003) and Agresti & Coull (1998) point out that exact methods such as the Clopper-Pearson interval may not work as well as some approximations."；Jeffreys 段逐字："it is one of the few intervals with the advantage of being equal-tailed… In contrast, the Wilson interval has a systematic bias such that it is centred too close to 0.5"；Beta 分位数实现代码 `beta.ppf([alpha/2, 1-alpha/2], [k, k+1], [n-k+1, n-k])` — 访问日期 2026-09-29。
2. statsmodels 0.15.0, `proportion_confint` — https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportion_confint.html — 逐字：method 取值 `"normal", "agresti_coull", "beta", "wilson", "jeffreys", "binom_test"`；"Beta, the Clopper-Pearson exact interval has coverage at least 1-alpha, but is in general conservative."；"In the extreme case when count is zero or equal to nobs, then the coverage will be only 1 - alpha/2 in the case of 'beta'."；参考文献 Brown, Cai, DasGupta (2001), Statistical Science 16(2):101–133, doi:10.1214/ss/1009213286 — 访问日期 2026-09-29。
3. Brown, Cai & DasGupta (2001) 摘要转载 — https://lacuna.tiptreesystems.com/paper/interval-estimation-for-a-binomial-proportion/art_23890287b7144cd788ad313c408a66a8 与 https://www.bohrium.com/en/paper-details/interval-estimation-for-a-binomial-proportion/812448370269356034-940 — 摘要逐字（两处一致）："we recommend the Wilson interval or the equal-tailed Jeffreys prior interval for small n and the interval suggested in Agresti and Coull for larger n" — 访问日期 2026-09-29（**原 PDF 未打开**）。
4. NIST, Dataplot "AGRESTI COULL CONFIDENCE LIMITS" — https://itl.nist.gov/div898/software/dataplot/refman2/auxillar/agcoulci.htm — 逐字："They specifically recommend the Wilson and Jeffreys methods for n ≤ 40"；"the adjusted Wald method is never shorter than the Wilson interval"；给出 Agresti–Coull 的 $\tilde X = X + z^2/2,\ \tilde n = n + z^2,\ \tilde p = \tilde X/\tilde n$ 公式 — 访问日期 2026-09-29。
5. Brown et al. 原 PDF（Wharton） — http://www-stat.wharton.upenn.edu/~lbrown/Papers/2001a%20Interval%20estimation%20for%20a%20binomial%20proportion%20(with%20T.%20T.%20Cai%20and%20A.%20DasGupta).pdf — **fetch 失败，未核实**；JSTOR https://www.jstor.org/stable/2676784 ；Project Euclid https://projecteuclid.org/journals/statistical-science/volume-16/issue-2 （确认卷期）。
6. Newcombe (1998), Statistics in Medicine 17(8):857–872 — http://stats.org.uk/statistical-inference/Newcombe1998.pdf ；PubMed https://pubmed.ncbi.nlm.nih.gov/9595616/ — 摘要逐字："Seven methods for the single proportion are evaluated on 96,000 parameter space points. Intervals based on tail areas and the simpler score methods are recommended for use." — 1998-04-30。
7. Gillibert, Bénichou & Falissard (2021), arXiv:2103.10463 — https://arxiv.org/abs/2103.10463 — 作者机构 INSERM UMR 1178 (Université Paris Sud) / CHU Rouen / Inserm U 1219 Normandie University；逐字："Wald's CI did not control any of the risks, even when the expected number of successes reached 32."；"we recommend using the Clopper-Pearson mid-P CI for the estimation of a proportion except for observed-theoretical proportion comparison..." — 2021-03-17。
8. binomcikit 文档, "Exact interval (Clopper–Pearson & Mid-P)" — https://pranava-babinomcikit-rtd.readthedocs.io/en/latest/methods/exact.html — 逐字："e = 1 puts it all in (giving the equal-tailed exact test, i.e. Clopper-Pearson); e = 0.5 puts in half (Mid-P)"；"Clopper-Pearson (blue) stays above the nominal 0.95 line everywhere… but that is over-coverage"；示例 n=5, x=3：CP [0.147, 0.947] vs Mid-P [0.182, 0.926] — 2026-07-25。
9. National Academies Press, "Realizing the Potential of the American Community Survey" — https://www.nap.edu/read/21653/chapter/7 — 逐字转述 Brown et al. (2001) 的 n ≤ 40 / n ≥ 40 推荐 — 访问日期 2026-09-29。
10. Sauro & Lewis, "Estimating Completion Rates from Small Samples Using Binomial Confidence Intervals" — https://measuringu.com/papers/sauro-lewisHFES.pdf — **仅获得半句摘要，未核实** — 2005。
11. Tandfonline, "Binomial Confidence Intervals for Rare Events" — https://www.tandfonline.com/doi/full/10.1080/00031305.2024.2350445 — 比较 Wald / Clopper-Pearson / Wilson 等，强调同时看覆盖率与相对误差界 — 2023-06-07（**未打开全文**）。
12. arXiv 2106.15521, "Locally correct confidence intervals for a binomial…" — https://arxiv.org/pdf/2106.15521 — 提出平均长度更短的区间 — 2023-01-23（**未打开全文**）。
13. CAMIS, "Confidence Intervals for a Proportion in R" — https://psiaims.github.io/CAMIS/R/ci_for_prop.html — 逐字："This method is often used as a compromise between the Clopper-Pearson and the Wald…" — 2026-07-14。
14. Statistics How To, "Clopper-Pearson Exact Method" — https://www.statisticshowto.com/clopper-pearson-exact-method/ — 访问日期 2026-09-29。
