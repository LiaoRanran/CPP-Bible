# 方向 44：序贯检验与 e-process / e-value / anytime-valid inference

## 核心结论

1. **e-process 是"可以边补数据边看"的检验对象，而 p 值不是。** 形式定义：非负过程 $(E_t)$ 是关于零假设集合 $\mathbf P$ 的 e-process，当且仅当存在一族测试鞅 $(M^P)_{P\in\mathbf P}$ 使 $E_t\le M^P_t$（对所有 $P,t$）；等价地，对**任意**停时 $\tau$ 都有 $\mathbb E_P[E_\tau]\le 1$。Ramdas–Grünwald–Vovk–Shafer 在 *Game-theoretic statistics and safe anytime-valid inference*（arXiv:2210.01948，2022-10-04 提交、v2 2023-06-17，25 页；后发表于 *Statistical Science* 38(4)，DOI 10.1214/23-STS894）里证明了这两种定义等价。这一条性质叫 **anytime-valid**：停时不需要预先指定，看到数据想停就停，Type-I 保证不破。阙疑的盲 holdout 从 30 涨到 100、200 时**不需要重新校正 $\alpha$**，这正是单人项目最需要的性质。

2. **判决门槛有确定的数值换算：e-value $\ge 1/\alpha$。** 由 Ville 不等式 $P(\sup_t M_t\ge\alpha)\le 1/\alpha$，取 $\alpha=0.05$ 则门槛是 **20**；取 $\alpha=0.01$ 则门槛是 **100**。对比之下，同水平的一次性 Neyman–Pearson 检验在 z 检验上的似然比门槛约为 **3.14**（Koning & van Meer, *Sequentializing a Test: Anytime Validity is Free*, arXiv:2501.03982，Erasmus University Rotterdam，2025-01-08，原文：*"for a one-sided z-test at level 0.05 this threshold is roughly 3.14, which is much smaller than 1/0.05 = 20"*）。**代价是明确的**：anytime-valid 的代价是功效，约 20/3.14 ≈ 6.4 倍的似然比门槛。这是必须在论文里明说的 trade-off，不能藏。

3. **e-value 可乘、可平均、可跨批次合并，是"证据账本"的天然数据结构。** Vovk & Wang（*E-values: Calibration, combination and applications*，arXiv:1912.06116，Annals of Statistics 49(3)，2021，DOI 10.1214/20-AOS2020）指出 e-value 在"合并多项研究"上比 p 值可操作得多；Grünwald–de Heide–Koolen 的 *Safe Testing*（arXiv:1906.07801，v1 2019-06-18、v5 2023-03-10，被 JRSS-B 接收为 discussion paper）把这一性质叫 **safe under optional continuation**。对阙疑而言：每新增一批 red-team 卡/盲样本产出一个 e-value，**乘积仍是 e-value**，可以 append 进 452 条判决账本而无需重跑全量统计。这直接补上"算术不自洽"那一块的统计地基。

---

## 精确数字与案例

### 一、四篇奠基文献的精确元数据

| 文献 | arXiv / 发表 | 时间 | 关键原句 |
|---|---|---|---|
| Ramdas, Grünwald, Vovk, Shafer — *Game-theoretic statistics and safe anytime-valid inference* | arXiv:2210.01948；*Statistical Science* 38(4)，DOI 10.1214/23-STS894 | v1 2022-10-04，v2 2023-06-17；25 页 | *"Safe anytime-valid inference (SAVI) provides measures of statistical evidence and certainty -- e-processes for testing and confidence sequences for estimation -- that remain valid at all stopping times, accommodating continuous monitoring and analysis of accumulating data and optional stopping or continuation for any reason."* |
| Grünwald, de Heide, Koolen — *Safe Testing* | arXiv:1906.07801 | v1 2019-06-18，v5 2023-03-10 | *"Tests based on e-values are safe, i.e. they preserve Type-I error guarantees, under such optional continuation. We define growth-rate optimality (GRO) as an analogue of power in an optional continuation context… GRO e-values take the form of Bayes factors with special priors."* |
| Shafer — *Testing by Betting: A Strategy for Statistical and Scientific Communication* | JRSS-A **184(2): 407–431** | 2021 | 主张"报告对零假设下注的结果"替代报告 p 值；原文 *"The most widely used concept of statistical inference—the p‐value—is too complicated for effective communication to a wide audience."* |
| Howard, Ramdas, McAuliffe, Sekhon — *Time-uniform, nonparametric, nonasymptotic confidence sequences* | arXiv:1810.08240；Annals of Statistics **49(2)**，DOI 10.1214/20-AOS1991 | 2021 | 置信序列（CS）在**无界时间**上一致有效；这是"边看边估"的估计版本。 |

另有工具书：Ramdas & Wang, *Hypothesis Testing with E-values*（arXiv:2410.23614，v1 2024-10-31，2025-09-11 更新；配套站点 alrw.net/e/），这是目前最系统的 e-value 教材式综述，含第 2 章定义体系（2.1 e-values / 2.2 test (super)martingale / 2.4 e-process / 2.5 Ville 不等式 / 2.7 anytime-valid p-value / 2.8 confidence sequence / 2.9 平均 / 2.10 相乘）。

### 二、Ville 不等式与门槛的逐字陈述

SAVI 综述（arXiv:2210.01948 正文）给出的形式：

- 对测试鞅 $M$：$\displaystyle P\!\left(\sup_{t}M_t\ge\alpha\right)\le\frac{1}{\alpha}$，文中称之为 *"theorem of gamblers' ruin"*，并解释为 *"a gambler who begins with unit capital and keeps betting until he wins the casino's entire capital α has little chance of succeeding."*
- 对 e-process $E$：$\displaystyle\sup_{P\in\mathbf P}P(\exists t\ge 1: E_t\ge 1/\alpha)\le\alpha$，等价停时形式 $P(E_\tau\ge 1/\alpha)\le\alpha$ 对每个 $\tau\in\mathcal T$ 成立。
- 可容许（admissible）e-process 的刻画：当 $\mathbf P$ 局部支配时 $E_t=\inf_{P\in\mathbf P}M^P_t$（本质下确界）。博弈论解读：*"关于 P 的 e-process 报告的是许多同时进行的博弈（每一局对抗一个 P，共享同样结果）中的最小财富。"*

**可直接写进论文的换算表**：

| 名义水平 $\alpha$ | e-value 拒绝门槛 $1/\alpha$ | 等价"赔率"表述 |
|---|---|---|
| 0.10 | 10 | 10:1 |
| 0.05 | 20 | 20:1 |
| 0.01 | 100 | 100:1 |
| 0.001 | 1000 | 1000:1 |

对阙疑：盲 holdout 30 例、检出 66.7%（20/30 中 20 例？——实际是 30 例中检出 66.7%，即 20 例检出，17 例真错）这个点估计，用 e-process 表达比用百分比表达更抗"你又加了数据"的质疑。

### 三、为什么"边补数据边检验"对单人项目是刚需（有据可查的危害）

SAVI 综述在引言里给出两个**具体案例**，用来论证"偷看数据"（peeking）不是小事：

1. **56%**：John, Loewenstein & Prelec (2012) 对**2000 多名心理学家**的匿名调查显示，**56%** 承认"在查看结果是否显著之后才决定是否收集更多数据"（原文口径：*"56% 承认…"*）。
2. **power posing（权力姿势）**：Carney 自述的样本分块为 *"something like 25 subjects run, then 10, then 7, then 5"* —— 即边跑边看，最终效应不可复现。
3. 综述强调：针对**复合零假设**的一般理论在 **2017 年之前并不存在**，2017 年前后兴趣爆发。

这三条可以直接作为阙疑论文"威胁到有效性"一节的外部证据：单人项目不可能不 peeking，因此**必须**用 anytime-valid 框架，否则"检出率 66.7%"这个数字在评审眼里就是 peeking 后的选择性报告。

### 四、已有的"用 e-process 做 LLM 评测"直接竞品/参照（2026 年最新）

这是本方向对阙疑最要紧的发现——**"用 e-process 做模型/基准评测"已经有人在做**，因此阙疑必须差异化，不能把"引入 e-process"本身当卖点。

| 论文 | arXiv | 时间 | 逐字结果 |
|---|---|---|---|
| **CELEUS: Certifiable and Efficient LLM Evaluation via E-Processes**（Zhijian Zhou, Zesheng Ye, Zhaorun Chen, Bo Li, Feng Liu） | arXiv:2606.20820 | v1 2026-06-18，v2 2026-06-26 | *"Experiments show that Celeus reaches the target precision using 54-62% fewer evaluated samples than baselines, while preserving anytime-valid coverage."* 方法要点：(i) uncertainty-guided sampling 选信息量大的样本，(ii) surrogate-assisted 近似未评样本；证明信号对评测分数**条件无偏**，从而得到 anytime-valid e-process CI；并证明 CI 可"以近参数速率收缩到对数因子以内"。 |
| **Anytime-Valid LLM Leaderboards via Benchmark-weighted e-processes (BB-EDGE)** | arXiv:2609.32248 | 2026-09（检索时标注"10 小时前"，即 2026-09-29 前后） | 提出 Benchmark-Weighted and Block-Factorized e-processes 用于有向图式排行榜。**细节未核实**（未打开全文）。 |
| **SERPANT: Sequential E-value Ranking and Pruning via Adaptive Null Testing** | OpenReview PDF（ID 见来源） | 未核实 | 在线 LLM 排序/剪枝的 e-value 框架。**未核实**。 |
| **e-RT: Sequential Randomization Tests Using e-values**（Fernando G. Zampieri, University of Alberta） | arXiv:2512.04366 | v6 2026-02-18 / v9 2026-05-10 | 用 betting martingale 做临床试验序列监测；*"An e-value is a measure of evidence against a null hypothesis with a specific property: its expected value under the null is at most 1."* 提到配套开源包 **evalinger**（Sokolova & Sokolov 2026a）——**该包未核实**。 |
| **Anytime-valid testing with e-values and confirmatory adaptive designs**（Werner Brannath, Lasse Fischer, University of Bremen） | arXiv:2606.00878 | 2026 | 证明**适应性设计中的 combination tests / conditional error functions 与基于 e-value 的 anytime-valid 序列检验在形式上等价**；差别在"前者追求耗尽 Type-I 水平，后者追求 optional continuation / 水平可选的灵活性"。 |

**结论**：E&D track 的评审很可能已经见过 CELEUS 一类工作。阙疑的差异化不能是"我们用了 e-process"，而必须是"**我们用 e-process 对'知识断言'而非'模型分数'做 anytime-valid 判决，且判决可被第三方离线复算**"——即把 e-process 与哈希链账本、独立对账器绑定。这个组合在检索到的文献里**没有出现**。

### 五、算法与代码：可落地的具体实现

**（1）库**

| 库 | 语言 | 说明 |
|---|---|---|
| **confseq** | C++ 核心 + Python/R 接口，`github.com/gostevehoward/confseq` | 实现 uniform boundaries、confidence sequences、always-valid p-values；SAVI 综述正文点名推荐（*"numerous CSs 已在 C++ 包 confseq 中实现"*）。仓库 README 标注在 Python 3.7/3.8/3.9/3.10 + Ubuntu/macOS 上跑自动化测试。 |
| **safestats** | R（CRAN） | 实现 safe t-test、2×2 列联表等经典场景。 |
| **EValue**（R，CRAN，2025-08-28 页更新） | R | ⚠️ **注意同名混淆**：CRAN 上的 `EValue`（作者 Maya Mathur / Louisa Smith）算的是**流行病学里的 E-value（未测混杂的稳健性指标）**，与本文的 e-value（e-process 的取值）**完全不是一回事**。检索时极易踩坑。 |

**（2）最小可用算法（可直接写进 `gate_engine.py` 的配套模块）**

对"这批 $n$ 个知识卡里有多少个被正确判为不成立"这类二值结果，最简做法是 **betting / 赌博式 e-process**：

```
初始化财富 W_0 = 1
对第 t 张卡（t = 1..n）：
    先根据 F_{t-1} 选一个下注比例 λ_t ∈ [0,1)   # 可预测（predictable）
    观测结果 Y_t ∈ {0,1}                        # 是否检出
    财富更新：W_t = W_{t-1} · (1 + λ_t · (Y_t - μ_0) / (1 - μ_0))   # μ_0 为零假设下的检出率
输出：e-value = W_n
若 W_n ≥ 20（α = 0.05）则拒绝零假设
```

关键性质（可写进论文命题）：$\mathbb E[W_t\mid F_{t-1}] = W_{t-1}$，故 $(W_t)$ 是非负鞅、$W_0=1$，即**测试鞅**，从而 $W_\tau$ 对任意停时都是 e-value，$P(W_\tau\ge 1/\alpha)\le\alpha$。这个更新式在 Grünwald–de Heide–Koolen 的 "GRO"（growth-rate optimal）框架下可进一步优化：**GRO e-value 就是取特殊先验的 Bayes factor**，下注比例 $\lambda_t$ 取"期望对数增长率最大"的值。

**（3）复合零假设的落地方法**（SAVI 综述第 3 章给了五条路，按代价从低到高）：插件法（plug-in）、混合法（mixture）、Bayes factor、最坏情况最小化（minimizing the worst）、以及复合零+复合备择下的 Universal Inference (UI) 与 Reverse Information Projection (RIPr)。阙疑的场景（"检出率 ≥ 某阈值"是复合零）**首选混合法**：在零假设参数上放一个先验，得到 Bayes factor 形式，计算代价是若干次加权平均，不需要重新推导。

### 六、什么时候不要用 e-process（批判）

1. **功效损失是实打实的**：同水平下门槛从 ~3.14 抬到 20（z 检验例子，Koning & van Meer 2025）。若阙疑的目标是"给定 30 例盲样本，最大化检出率"，e-process **更弱**，不是更强。
2. **e-value 不可解释成"错误概率"**：$E=20$ 不等于"5% 概率错"。JRSS-B 的讨论稿里 Christine P. Chai 的评论（JRSS-B 86(5):1146，2024-07-08）即指出该点争议；Glenn Shafer 本人在同卷 86(5):1137 的讨论中回应，称 e-value 的价值要等学界"不再坚持"某类惯例后才显现。
3. **文献仍在高速变动**：2026 年上半年 arXiv 上就有 CELEUS、BB-EDGE、Brannath–Fischer 等多篇新作。**任何 2026 年写的"e-process 用于 LLM 评测"的 novelty 声明，到 2027 年投稿时都可能已被覆盖。**

---

## 对阙疑的 3 条具体行动

1. **在 `research/12_threats_to_validity.md` 增加小节 "T1: 非 anytime-valid 的检出率报告"，时间点 2027-05 前。** 内容必须写死：盲 holdout 30 例（真错 17，检出 66.7%）是**单次快照**，而 452 条判决账本是**逐条累加**的；两者混用构成 peeking。给出外部证据：John/Loewenstein/Prelec 2012 的 56% 偷看率、Carney power-posing 的 *"25 subjects run, then 10, then 7, then 5"*。并声明论文中所有"检出率"数字同时给 p 值（Clopper–Pearson，已在 `32_Clopper-Pearson精确计算.md` 覆盖）与 e-value 两种口径。

2. **新建 `eval/eprocess.py`（与 `gate_engine.py` 同层，不改内核），实现上述 betting e-process，并把 e-value 写进账本字段，时间点 2027-03 前。** 具体字段建议：`ledger_entry` 增加 `e_value_cum`（累计 e-value）与 `wager_lambda`（当步下注比例）；拒绝门槛固定为 **20**（$\alpha=0.05$）并同时输出 **10 / 100** 两档以便敏感性分析。用 `confseq`（`github.com/gostevehoward/confseq`，C++ 核心带 Python 接口）对二值序列做交叉验证；若安装受阻（注意本项目 sanitizer 已全缺），退化为纯 Python 实现并在盲区标注。**必须先做仿真校验**：在零假设下跑 10,000 条长度为 100 的合成序列，确认 $\sup_t W_t\ge 20$ 的经验频率 $\le 0.05$（这是 e-process 实现的唯一验收标准）。

3. **在论文 Related Work 中显式引用并差异化 CELEUS（arXiv:2606.20820），时间点 2027-06 前（NeurIPS 2027 摘要截止前）。** 差异化必须写成一句话可检验的对比：CELEUS 用 e-process 得到 *"anytime-valid CIs"* 并报告 *"54-62% fewer evaluated samples"*，其目标是**减少评测样本量**；阙疑用 e-process 的目标是**让 452 条已判决记录在"边补数据"下仍保持 Type-I 有效，且判决可被不信任内核的第三方离线复算**。**禁止**在论文里声称"首次将 e-process 用于 LLM/知识评测"——已有至少 3 篇（CELEUS、BB-EDGE、SERPANT）。

---

## 盲区（诚实标注）

- **BB-EDGE（arXiv:2609.32248）与 SERPANT（OpenReview）我未打开全文**，只见到检索摘要。两者的具体数据集、数字、是否涉及"知识断言"级别的判定，**均未核实**；引用前必须重新核对，否则有编造风险。
- **`evalinger` 包**（e-RT 论文提到，Sokolova & Sokolov 2026a）我未在 GitHub/CRAN 上核实其存在与版本号，**标为未核实**。
- **`Safe Testing` 在 JRSS-B 的精确页码未核实**。我只确认了同卷（86 卷 5 期，2024）存在 Shafer 的讨论评论（86(5):1137）与 Chai 的讨论评论（86(5):1146），据此推断正文在该期，但**未打开 OUP 页面确认起止页**。
- **Ville 不等式"在离散时间中相当紧、overshoot 是二阶效应"这一表述来自 SAVI 综述的中文提取**（通过 WebFetch 的模型摘要，而非我逐字读 PDF），存在转述误差风险。
- **样本偏差**：本方向检索到的 2026 年新论文（CELEUS / BB-EDGE / SERPANT / e-RT）全部集中在**临床统计 + LLM 评测**两个应用域，没有一篇是"代码/知识断言验证"。这既说明阙疑有空间，也说明**没有同类工作可对照**，阙疑将是自己领域里的第一例，缺乏可比基线。
- **检索工具自身的风险**：本次检索结果中出现大量 2026 年 6–9 月的 arXiv 编号（2606.*、2609.*），其编号与提交日期的一致性我无法逐一核验；上表所有 2026 年条目在写入论文前需重新访问 URL 确认。

---

## 来源

1. Game-theoretic statistics and safe anytime-valid inference — https://arxiv.org/abs/2210.01948 — *"e-processes for testing and confidence sequences for estimation -- that remain valid at all stopping times"*；25 页；Aaditya Ramdas, Peter Grünwald, Vladimir Vovk, Glenn Shafer — 2022-10-04（v2 2023-06-17）
2. 同上（期刊版） — https://projecteuclid.org/journals/statistical-science/volume-38/issue-4/Game-Theoretic-Statistics-and-Safe-Anytime-Valid-Inference/10.1214/23-STS894.full — *Statistical Science* 38(4)，DOI 10.1214/23-STS894 — 2023
3. 同上（全文，Ville 不等式逐字） — https://ar5iv.labs.arxiv.org/html/2210.01948 — $P(\sup_t M_t\ge\alpha)\le 1/\alpha$；e-process 定义 $E_t\le M^P_t$；56% 偷看率；*"25 subjects run, then 10, then 7, then 5"* — 2023
4. Safe Testing — https://arxiv.org/abs/1906.07801 — *"Tests based on e-values are safe… under such optional continuation"*；GRO = growth-rate optimality；GRO e-values 是特殊先验的 Bayes factor — Grünwald, de Heide, Koolen — v1 2019-06-18 / v5 2023-03-10
5. E-values: Calibration, combination and applications — https://arxiv.org/abs/1912.06116 — 期刊版 *Annals of Statistics* 49(3)，DOI 10.1214/20-AOS2020 — Vovk & Wang — 2021
6. Testing by Betting: A Strategy for Statistical and Scientific Communication — https://academic.oup.com/jrsssa/article/184/2/407/7056412 — JRSS-A 184(2): 407–431 — Glenn Shafer — 2021
7. Time-uniform, nonparametric, nonasymptotic confidence sequences — https://arxiv.org/abs/1810.08240 — Annals of Statistics 49(2)，DOI 10.1214/20-AOS1991 — Howard, Ramdas, McAuliffe, Sekhon — 2021
8. Sequentializing a Test: Anytime Validity is Free — https://arxiv.org/pdf/2501.03982v1 — *"for a one-sided z-test at level 0.05 this threshold is roughly 3.14, which is much smaller than 1/0.05 = 20"* — Nick W. Koning & Sam van Meer，Erasmus University Rotterdam — 2025-01-08
9. CELEUS: Certifiable and Efficient LLM Evaluation via E-Processes — https://arxiv.org/abs/2606.20820 — *"reaches the target precision using 54-62% fewer evaluated samples than baselines, while preserving anytime-valid coverage"* — Zhijian Zhou, Zesheng Ye, Zhaorun Chen, Bo Li, Feng Liu — v1 2026-06-18 / v2 2026-06-26
10. Hypothesis Testing with E-values（教材） — https://arxiv.org/abs/2410.23614 — 第 2 章定义体系（2.1–2.10）；配套站点 https://www.alrw.net/e/ — Ramdas & Wang — v1 2024-10-31，2025-09-11 更新
11. confseq（C++/Python/R 实现） — https://github.com/gostevehoward/confseq — *"Confidence sequences and uniform boundaries"*；Python 3.7–3.10 自动化测试 — Steve Howard 等 — 仓库 2026-01-24 仍有活动
12. Anytime-valid testing with e-values and confirmatory adaptive designs — https://arxiv.org/html/2606.00878 — *"concepts of adaptive designs, like combination tests and conditional error functions, are formally equivalent to anytime-valid test based on sequential e-values"* — Werner Brannath, Lasse Fischer，University of Bremen — 2026
13. Sequential Randomization Tests Using e-values — https://arxiv.org/pdf/2512.04366 — *"An e-value is a measure of evidence against a null hypothesis with a specific property: its expected value under the null is at most 1."* — Fernando G. Zampieri，University of Alberta — v6 2026-02-18 / v9 2026-05-10
14. Anytime-Valid LLM Leaderboards via Benchmark-weighted e-processes — https://arxiv.org/pdf/2609.32248 — BB-EDGE，细节未核实 — 2026-09
15. Shafer 对 *Safe Testing* 的讨论评论 — https://academic.oup.com/jrsssb/article/86/5/1137/7708228 — JRSS-B 86(5) — 2024-07-05
16. E-values Instead of P-values in Clinical Trials: What Happens? — https://ercim-news.ercim.eu/en145/special/3073-e-values-instead-of-p-values-in-clinical-trials-what-happens — ERCIM News 145 — 2026-07-02
