# 方向 22：Evaluation section 怎么写

## 核心结论

1. **指标表的第一性原则不是"我的数最高"，而是"我的数和 baseline 的数是在同一测试集、同一指标、同一预算下算出来的"**——Dodge 等（2019）证明只报测试集分数不足以判断谁更好，Musgrave 等（2020）在统一设置后让过去四年度量学习论文声称的提升**全部消失**。
2. **小样本评测（n=30 量级）的误差棒不是装饰，而是唯一能防止过度解读的装置**：NeurIPS Paper Checklist 第 7 项明确要求"至少对支持主要主张的实验"报告误差棒 / 置信区间 / 显著性检验，并说明它捕捉的变异来源、计算方法与假设。
3. **消融必须报"移除后掉了多少 + 这个掉幅是否超过噪声"，而不是只报"加了它更好"**——Bouthillier 等（2021）指出增加变异源比精调估计器更划算（**算力成本降低 51 倍**），这意味着消融的对照组设计比统计方法选择更关键。

---

## 精确数字与案例

### 1. 真实好例之一：Dodge 等 2019 —— 把"最好分数"换成"预算—性能曲线"

**论文**：Jesse Dodge, Suchin Gururangan, Dallas Card, Roy Schwartz, Noah A. Smith, *"Show Your Work: Improved Reporting of Experimental Results"*，arXiv:1909.03004（2019-09-06 提交），发表于 ACL 2019（Anthology ID **D19-1224**）。

**核心论证**：仅凭测试集分数不足以得出"哪个模型最好"的结论；作者主张报告开发过程中的验证集表现，并提出一个新指标——**expected validation performance of the best-found model as a function of computation budget**（即"在给定超参搜索次数/训练时间预算下，最优模型的期望验证性能"，常缩写为 EMP）。原文给出两个可直接引用的量化结论：

- "We find multiple recent model comparisons where authors would have reached a **different conclusion** if they had used more (or less) computation."（多项近期模型对比中，若作者用更多或更少的算力，会得出**不同结论**。）
- "Our approach also allows us to estimate the amount of computation required to obtain a given accuracy; applying it to several recently published results yields **massive variation across papers, from hours to weeks**."（达到给定精度所需算力在不同论文之间差异巨大，**从数小时到数周**。）

**对阙疑的直接启发**：阙疑的核心数字是"检出率 66.7%（10/15 可测）"。按 Dodge 的口径，这个数字必须绑定一个**预算**——例如"在 67 条规则全部启用、编译档固定为 `-O1`、单条样本判定时间 ≤ T 秒"的预算下。否则读者无法判断 66.7% 是"规则够用"还是"预算不够"。

### 2. 真实好例之二：Bouthillier 等 2021 —— 变异源比估计器更重要

**论文**：Xavier Bouthillier, Pierre Delaunay, Mirko Bronzi, Assya Trofimov, Brennan Nichyporuk, Justin Szeto, Naz Sepah, Edward Raff, Kanika Madan, Vikram Voleti, Samira Ebrahimi Kahou, Vincent Michalski, Dmitriy Serdyuk, Tal Arbel, Chris Pal, Gaël Varoquaux, Pascal Vincent，*"Accounting for Variance in Machine Learning Benchmarks"*，arXiv:2103.03098（2021-03-02），发表于 **MLSys 2021**。

**可引用的精确数字**：论文摘要原文——"We show a counter-intuitive result that adding more sources of variation to an imperfect estimator approaches better the ideal estimator at a **51 times reduction in compute cost**."（向一个不完美估计器加入更多变异源，能更接近理想估计器，且**算力成本降低 51 倍**。）论文建模了完整基准测试过程，揭示"数据采样、参数初始化、超参选择"三类变异都会显著影响结果，并在 **5 个不同的深度学习任务/架构**上研究了"检测到改进的错误率"。

**对阙疑的直接启发**：阙疑的"变异源"不是随机种子，而是**编译档（-O0/-O1/-O2/-O3/-Os）、编译器（GCC/Clang/MSVC）、平台、输入域**。论文 v0.3 已经量化了其中一个：**`-O1`→`-O0` 使 3/5 个 miss 被同一个 sanitizer 抓住**。这就是一个教科书级的"变异源"实证。Evaluation 里应当把这条提升为一个正式的**多档位矩阵**，而不是一句附注。

### 3. 真实好例之三：Musgrave 等 2020 —— "统一设置后提升消失"

**论文**：Kevin Musgrave, Serge Belongie, Ser-Nam Lim，*"A Metric Learning Reality Check"*，arXiv:2003.08505，发表于 **ECCV 2020**（DOI 10.1007/978-3-030-58595-2_41）。

**核心论证**：过去四年的深度度量学习论文"consistently claimed great advances in accuracy, often more than…"（持续声称精度大幅提升），但在统一训练协议、统一 backbone、统一评估设置下重跑后，这些提升大部分不成立。

**这是阙疑 Evaluation 最该抄的一段论证结构**：不要写"我的检出率 66.7% 优于 cppcheck 的 X%"，而要先写"现有 C++ 静态/动态检测工具的报告口径互不相同（规则集不同、编译档不同、语料不同），因此我先把它们统一到同一语料、同一编译档、同一判定粒度上重跑，再比较"。统一之后的数字才叫 baseline。

### 4. 真实好例之四：Melis 等 2018 —— "单个 tuned 基线打败复杂模型"

**论文**：Gábor Melis, Chris Dyer, Phil Blunsom，*"On the State of the Art of Evaluation in Neural Language Models"*，arXiv:1707.05589，发表于 **ICLR 2018**。

**核心论证**：用大规模自动黑箱超参搜索（black-box hyperparameter search）重新评估若干流行架构与正则化方法，发现**一个被充分调参的标准 LSTM 基线**就足以超越许多声称新颖的架构。该论文的贡献不是新模型，而是"把评估标准拉回可比"。

**对阙疑的启发**：阙疑最强的 baseline 很可能不是另一个 C++ 检测器，而是**"充分调参后的 grep + 正则"**或**"把所有规则一律降级为 warn 的哑版本"**。Melis 这一例说明：把一个"愚蠢但被调到最好"的 baseline 认真跑出来，其说服力远高于列举三个弱 baseline。

### 5. 真实好例之五：弱 baseline 的系统性危害（2024）

**论文**：Nathan Wolfrath, Joel Wolfrath, Hengrui Hu, Anjishnu Banerjee, Anai N. Kothari，*"Stronger Baseline Models — A Key Requirement for Aligning Machine Learning Research with Clinical Utility"*，arXiv:2409.12116（2024-09-18），18 页 6 图。摘要原文：通过一系列案例研究，"we find that the common practice of **omitting baselines or comparing against a weak baseline model (e.g. a linear model with no optimization)** obscures the value of ML methods proposed in the research literature."（省略 baseline 或与弱 baseline——如**未经优化的线性模型**——比较，会掩盖文献中所述 ML 方法的真实价值。）

### 6. 人类基线的样本量门槛（ICML 2025 Spotlight）

**论文**：*"Recommendations and Reporting Checklist for Rigorous & Transparent Human Baselines in Model Evaluations"*，arXiv:**2506.13776**，**ICML 2025 Spotlight**，代码 `github.com/kevinlwei/human-baselines`。该论文系统审查了 **115 项**现有人类基线研究，发现的关键缺陷与建议门槛：

- **测试集一致性**：相当比例的 AI 评估在人机**不同测试子集**上比较；若因预算只能用子集，**AI 的分数也必须在该子集上重算**，且子集须随机采样或按难度/主题分层。
- **样本量**：许多研究只用 **3–5 个标注者**，远不足以代表"人类水平"；对一般人群基线建议做**统计功效分析**，经验法则是**约 1000 名参与者**才能代表美国成年人口；专家基线可用便利样本，但**必须显式定义专家资格标准**。
- **不确定性**：大量研究只报点估计，不报置信区间。
- **方法效应控制**：人机须使用**完全相同的任务说明、示例与上下文**，并随机化题目与选项顺序。
- **努力程度控制**：公平比较应在相似的资源投入下进行（相同时间限制或可比成本）。

**对阙疑的直接启发**：阙疑若想做"人类基线"，**绝对不能只找 1 个同学**。诚实的写法是：把 3 名同学的独立判决作为"便利样本专家基线"，明确标注它**不代表人类水平**，并按该论文的建议报告一致性与不确定性（κ + CI），而不是报告一个"人类准确率"。

### 7. 评估设计的既有标准：ACM SIGSOFT Empirical Standards — Benchmarking

这是目前对"基准/评估类论文"最细的一份可操作清单（`github.com/acmsigsoft/EmpiricalStandards/blob/master/docs/standards/Benchmarking.md`）。它对阙疑有三处特别有用：

**（a）Essential Attributes（必备项）**原文要点：
- 要么论证所选既有基准的合理性，要么定义新基准并给出四要素：**(i) 被基准的质量（如性能、可用性、可扩展性、安全性）、(ii) 量化该质量的指标、(iii) 指标的测量方法、(iv) 被测系统所承受的工作负载/使用画像/任务样本**；
- "describes the experimental setup for the benchmark in sufficient detail to support independent replication"；
- "specifies the workload or usage profile in sufficient detail to support independent replication"；
- "allows different configurations of a system under test to compete on their merits without artificial limitations"；
- "assesses stability or reliability using sufficient experiment repetitions and execution duration"；
- "discusses the **construct validity** of the benchmark; that is, does the benchmark measure what it is supposed to measure?"

**（b）Antipatterns（反模式）**原文四条：
- "Tailoring the benchmark for a specific method, technique or tool, which is evaluated with the benchmark."（把基准**裁剪**成有利于被评方法的样子）
- "Using benchmarking experiments that are irrelevant for the problem studied to obfuscate weaknesses in the proposed approach"
- "Insufficient repetitions or duration to assess stability of results"
- "Collecting aggregated measurements instead of persisting all raw results and running an offline analysis"（**只存聚合结果而不存原始结果**）

**（c）Invalid Criticisms（无效批评）—— 这一条对阙疑极其有利**，原文三条：
- "**The benchmark is not widely used.** It is sufficient to start developing a new benchmark with a small group of researchers as an offer to a larger scientific community. Such a proto-benchmark (Sim et al. 2003) can act as a template…"
- "**No independent replication of the benchmark results is reported.**"
- "**There is no independent organization that maintains the benchmark.**"

也就是说：**"你的 benchmark 没人用""没人独立复现过""没有组织维护"这三条在 ACM SIGSOFT 的标准里被明确列为无效批评**。阙疑作为单人 proto-benchmark，可以在 Evaluation 或 Threats to Validity 里直接引用这三条，把"37 实卡 / 30 样本太小"这类质疑前置回应掉。另外标准还给出 "Examples of Acceptable Deviations" 两条对阙疑有利：需要特殊硬件而难以复现、以及"**the study only employs one (or a few) runs because prior work has shown that a single run is sufficient**"。

### 8. 阙疑 Evaluation 的指标表：把数字算准（本次实算）

下面这张表是**本次调研用 Clopper-Pearson / Wilson 两种方法实算**的结果（纯 Python 实现正则化不完全 Beta 函数 + 二分求逆，`z=1.959963985`，α=0.05）。它可以直接作为 Evaluation 的 Table 1 底稿：

| 数据集 | 命中/总数 | 点估计 | Wilson 95% CI | Clopper-Pearson 95% CI | CI 宽度 |
|---|---|---|---|---|---|
| 盲 holdout（可测子集） | 10/15 | 0.6667 | [0.4171, 0.8482] | [0.3838, 0.8818] | 0.498 |
| 盲 holdout（全部真错） | 17/30 | 0.5667 | [0.3920, 0.7262] | [0.3743, 0.7454] | 0.371 |
| 外部 corpus（若为 7/16） | 7/16 | 0.4375 | [0.2310, 0.6682] | [0.1975, 0.7012] | 0.504 |
| 外部 corpus（若为 14/32） | 14/32 | 0.4375 | — | [0.2636, 0.6234] | 0.360 |
| A 层（若为 13/24） | 13/24 | 0.5417 | [0.3507, 0.7211] | [0.3282, 0.7445] | 0.416 |
| B 层（若为 2/16） | 2/16 | 0.1250 | [0.0350, 0.3602] | [0.0155, 0.3835] | 0.368 |
| C 层（若为 0/6） | 0/6 | 0.0000 | [0.0000, 0.3903] | [0.0000, 0.4593] | 0.459 |
| 重注入检出 | 6/6 | 1.0000 | [0.6097, 1.0000] | [0.5407, 1.0000] | 0.459 |
| 历史覆盖 | 12/15 | 0.8000 | [0.5481, 0.9295] | [0.5191, 0.9567] | 0.438 |

**这张表暴露了三个必须在投稿前解决的具体问题**：

**问题 A（算术不一致，必须查）**：论文 v0.3 记"外部 corpus 40 条，检出率 43.8%（分层 A 54.2% / B 12.5% / C 0%）"。但 **43.8% × 40 = 17.52，不是整数**，所以 43.8% 的分母不是 40。43.75% 的两个整数表示为 **7/16** 与 **14/32**。而 54.2% ≈ 13/24、12.5% = 2/16 也都是精确可表示的分数。若 A 层 = 24 条、B 层 = 16 条，则 A+B = 40 已用尽全部样本，且 (13+2)/40 = **15/40 = 37.5%**，与 43.8% 相差 6.3 个百分点。**这三个数字（43.8% / 54.2% / 12.5%）在当前口径下无法同时成立**，必须在投稿前把三层样本量、每层命中数、以及总检出率的分母写清楚。这是 Evaluation 最容易被审稿人一击致命的点。

**问题 B（Wald 区间不可用）**：若用 Wald 区间，B 层 2/16 的下限是 **−0.0370**（负数），12/15 的上限是 **1.0024**（超过 1）。这正是 Checklist 第 7 项原文警告的："For asymmetric distributions, the authors should be careful not to show in tables or figures symmetric error bars that would yield results that are out of range (e.g. negative error rates)." **结论：阙疑一律用 Clopper-Pearson（保守、覆盖度 ≥ 1−α）或 Wilson（平均覆盖度 = 1−α），永不使用 Wald。**

**问题 C（样本量的硬天花板）**：在 p≈0.7 的假设下，要把 Wald 半宽压到 ±0.15 需要 **约 36 个样本**；±0.10 需要 **约 81 个**；±0.05 需要 **约 323 个**。也就是说：**30 个样本的 holdout 在数学上最多支撑 ±0.16 左右的精度**。因此阙疑**不应**在 Evaluation 里主张"检出率约 66.7%"之外的更强结论（例如"达到 70% 以上"）。诚实的写法是给出 CI 并明确写"本样本量不支持对 70% 与 60% 的区分"。同一条约束也适用于 6/6 = 100% 的重注入检出：其 Clopper-Pearson 95% 下限只有 **0.5407**，即"重注入检出 100%"在 n=6 时**不能**被读作"真实检出率高于 54%"以外的任何更强主张。

### 9. Evaluation section 的结构模板

建议按 **6 小节 + 1 附录** 组织：

1. **§5.1 Evaluation Questions（EQ1–EQ5）**：先列问题，后列表。例如 EQ1 检出率、EQ2 假阳性率、EQ3 分层一致性（A/B/C 层是否同源）、EQ4 消融、EQ5 独立对账器能检出什么。
2. **§5.2 Datasets and Splits**：三张表——holdout（30 seeds，真错 17 / 对照 9 / unknown 4）、external corpus（40 条，A/B/C 三层，**必须写清每层 n 与命中数**）、defect fixtures（15 条，7 个来源 commit）。每张表给"是否公开 / 是否可复算 / 是否 blind"三列。
3. **§5.3 Baselines and Alignment Protocol**：明确写"对齐协议"三件事——同一语料、同一编译档矩阵、同一判定粒度（规则级 vs 文件级 vs 行级）。**引用 Empirical Standards 的 "allows different configurations of a system under test to compete on their merits without artificial limitations"** 作为协议设计依据。
4. **§5.4 Main Results（指标表）**：即上面的 Table 1。每个比例后**必须**带 CI 并标注方法（Clopper-Pearson / Wilson）。
5. **§5.5 Ablations**：至少三组——(a) 移除 44 条 block 中的 `-HC` 高复杂度组（661 A2 批次把规则口径从 63 修正到 67，正是因为补上了 4 条 `-HC` block 规则，所以这组消融有明确的历史锚点）；(b) 关闭 Merkle checkpoint；(c) 关闭独立对账器。每组报 Δ 检出率 + Δ 假阳性 + CI，并明确"Δ 是否超过噪声带"。
6. **§5.6 Statistical Analysis**：方法学小节，写清每处检验的选择理由（配对用 McNemar、非配对用 Fisher 精确、比例区间用 Clopper-Pearson、效应量用 Cohen's h、多重比较用 Holm）。细节见方向 24。
7. **附录 C：Raw Per-Sample Results**：逐样本一行（sample_id / layer / planted / detected / rule_ids / exit_code / 编译档）。这一条直接命中 Empirical Standards 的反模式第 4 条（"Collecting aggregated measurements instead of persisting all raw results"）——**必须存原始结果**。

---

## 对阙疑的 3 条具体行动

**行动 1（2026-10-15 前，修算术不一致）**：打开 `data/external_corpus/external_corpus_665.json`，逐条统计 A/B/C 三层的 `n`、每层命中数、以及总检出率的分母，把 43.8% / 54.2% / 12.5% 三个数复算到自洽。命令示例：`python -c "import json,collections; d=json.load(open('data/external_corpus/external_corpus_665.json',encoding='utf-8')); c=collections.Counter((s.get('layer'),bool(s.get('detected'))) for s in d['samples']); print(sorted(c.items()))"`（字段名须以实际 JSON 为准）。**这是最高优先级**——三个数不自洽会被直接判为"数据不可信"。

**行动 2（2026-11-30 前，重写指标表）**：把论文 v0.4 的 §5.4 换成上面第 8 节的表格结构，每个比例后加 Clopper-Pearson 95% CI 与计算脚本路径；在表注里写一句 "CIs computed with Clopper-Pearson exact method (Brown, Cai & DasGupta, 2001); Wald intervals are not used because they are undefined/out-of-range for k=0 and k=n at this sample size." 同时新增 §5.6 统计方法小节。工具：`statsmodels.stats.proportion.proportion_confint(count, nobs, alpha=0.05, method='beta')`（`'beta'` 即 Clopper-Pearson）或 `scipy.stats.binomtest(k, n).proportion_ci(confidence_level=0.95, method='exact')`。

**行动 3（2027-01-15 前，补消融与原始结果附录）**：跑三组消融（block 全开 / 去掉 `-HC` 组 / 全规则降级为 warn），输出逐样本原始表进附录 C；每组报 Δ + CI。同时把 `-O1`→`-O0` 的"3/5 miss 被同一 sanitizer 抓住"提升为一张正式的**编译档 × 命中矩阵**（行=编译档 `-O0/-O1/-O2/-O3/-Os`，列=sanitizer 组合），这直接对应 Bouthillier 等 2021 的"变异源"论点，也是最容易被审稿人认可的新增实证。

---

## 盲区（诚实标注）

1. **外部 corpus 三层样本量未知**，本文的 A=24 / B=16 / C=6 是**反推的假设**，不是实测。43.8% 与 54.2%/12.5% 的算术不一致是**基于论文 v0.3 摘要数字的推论**，也可能是 v0.3 摘要有笔误（而非数据有问题），必须回到 JSON 复算才能定论。
2. **A/B/C 三层的"层"定义（按检测器可用性分层）的具体判定规则未核实**，只知道论文 v0.3 记为"按检测器可用性分层"。
3. **Musgrave 等 2020 的具体提升幅度数字未核实**（只核实到"过去四年持续声称大幅提升、统一设置后不成立"的论点与 arXiv 号 2003.08505）。
4. **Henderson 等 2018 "Deep RL that Matters" 的具体变异数字未核实**（只核实到 arXiv:1709.06560、AAAI 2018 与"illustrate the variability in reported metrics"的摘要句）。
5. **Melis 等 2018 的具体性能数字未核实**（只核实到 arXiv:1707.05589、ICLR 2018 与"用大规模自动黑箱超参搜索重评估"的方法描述）。
6. **ICML 2025 human baselines 论文的"约 1000 名参与者"是经验法则（rule of thumb）而非统计功效分析的确定结果**，本文转引自论文解读页面，**未逐字核对 arXiv:2506.13776 原文**（PDF 无法通过 WebFetch 读取）。
7. **Bouthillier 等 2021 的"51 倍"来自 arXiv 摘要原文**，但该数字的推导条件（在哪个任务、哪个估计器上）未核实。
8. **Nature Scientific Reports 2024 的 "Evaluation metrics and statistical tests for machine learning"（s41598-024-56706-x）未能取到正文**（Nature 站点重定向到身份验证页），本文未引用其任何具体数字。
9. **ACM SIGSOFT Empirical Standards 的 Benchmarking 标准当前版本号为未知**（GitHub master 分支快照），引用时建议标注"as of 2026-09"。
10. **NeurIPS 2024 D&B 的平均分 6.58 / Accept 6.72 / Reject 5.64 来自 Paper Copilot 社区采集**，非官方公布，且该站自述"仅统计选择公开评分的提交"，存在选择偏差。

---

## 来源

1. J. Dodge, S. Gururangan, D. Card, R. Schwartz, N. A. Smith, "Show Your Work: Improved Reporting of Experimental Results", arXiv:1909.03004（2019）；ACL 2019, D19-1224 — https://arxiv.org/abs/1909.03004 ；https://aclanthology.org/D19-1224/
2. X. Bouthillier et al., "Accounting for Variance in Machine Learning Benchmarks", arXiv:2103.03098（2021）；MLSys 2021 — https://arxiv.org/abs/2103.03098 ；https://proceedings.mlsys.org/paper_files/paper/2021/hash/0184b0cd3cfb185989f858a1d9f5c1eb-Abstract.html
3. K. Musgrave, S. Belongie, S.-N. Lim, "A Metric Learning Reality Check", arXiv:2003.08505；ECCV 2020，DOI 10.1007/978-3-030-58595-2_41 — https://arxiv.org/pdf/2003.08505
4. G. Melis, C. Dyer, P. Blunsom, "On the State of the Art of Evaluation in Neural Language Models", arXiv:1707.05589；ICLR 2018 — https://arxiv.org/abs/1707.05589 ；https://iclr.cc/virtual/2018/poster/214
5. P. Henderson et al., "Deep Reinforcement Learning that Matters", arXiv:1709.06560；AAAI 2018 — https://arxiv.org/abs/1709.06560 ；https://ojs.aaai.org/index.php/AAAI/article/view/11694
6. N. Wolfrath, J. Wolfrath, H. Hu, A. Banerjee, A. N. Kothari, "Stronger Baseline Models — A Key Requirement for Aligning Machine Learning Research with Clinical Utility", arXiv:2409.12116（2024）— https://arxiv.org/abs/2409.12116
7. "Recommendations and Reporting Checklist for Rigorous & Transparent Human Baselines in Model Evaluations", arXiv:2506.13776；ICML 2025 Spotlight — https://en.papernotes.org/ICML2025/recommender/recommendations_and_reporting_checklist_for_rigorous_transparent_human_baselines/ ；代码 https://github.com/kevinlwei/human-baselines
8. ACM SIGSOFT Empirical Standards, "Benchmarking (of Software Systems)" — https://github.com/acmsigsoft/EmpiricalStandards/blob/master/docs/standards/Benchmarking.md ；总入口 https://www2.sigsoft.org/EmpiricalStandards/
9. NeurIPS Paper Checklist Guidelines（第 7 项原文）— https://neurips.cc/public/guides/PaperChecklist
10. L. D. Brown, T. T. Cai, A. DasGupta, "Interval Estimation for a Binomial Proportion", Statistical Science 16(2): 101–133, 2001, doi:10.1214/ss/1009213286 — https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportion_confint.html
11. SciPy, `scipy.stats.binomtest` / `BinomTestResult.proportion_ci` — https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binomtest.html
12. Paper Copilot, NeurIPS 2024 Datasets & Benchmarks Track 评分分布 — https://legacy.papercopilot.com/statistics/neurips-statistics/neurips-2024-statistics-datasets-benchmarks-track/
13. NeurIPS 2024 / 2025 Datasets and Benchmarks Accepted Papers（163 篇）— https://neurips.cc/Conferences/2025/DatasetsBenchmarks/AcceptedPapers
14. 本方向第 8 节的置信区间为**本次实算**（纯 Python 实现正则化不完全 Beta 函数 + 二分求逆；Wilson 解析式），非引用。
