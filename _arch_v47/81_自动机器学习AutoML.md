# 方向 81：自动机器学习（AutoML）

> 本组贯穿问题：**"验证器能否自己发现新的验证规则 / 新的知识卡缺陷？"**
> AutoML 给出的答案是最冷静的一层：**"能自动调的东西，和能自动发明的东西，不是一回事。"**
> AutoML 二十年最强证据都集中在**在一个人工预先定义的搜索空间里做搜索与组合**；它从来没有证据表明系统能自己**扩展搜索空间的维度**（即"发明一条新规则"）。这个区分对阙疑是决定性的：阙疑的 67 条规则里 44 条是 block、16 条 warn、7 条 advice——**AutomML 可以直接帮的是"这 67 条的阈值/权重/组合方式"，不能直接帮的是"第 68 条规则从哪来"**。

---

## 核心结论

1. **AutoML 相对人工调参的提升是真实的，但幅度远小于宣传，且高度依赖"人工先把搜索空间写对"**：AutoGluon-Tabular（Erickson 等，arXiv:2003.06505，2020）在 50 个数据集（39 OpenML + 11 Kaggle）、4 小时预算下，Champion（优于全部 5 个对比框架）**23/39 与 7/11**；在两个 Kaggle 竞赛上以 4h 训练取得 **42/3505（≈98.8%）** 与 **39/2920（≈98.6%）**。但这是"框架 A vs 框架 B"，**不是"AutoML vs 资深人类"**。目前唯一直接对标的公开研究（Hanussek、Blohm、Kintz，AIRC 2020，arXiv:2009.01564）在 12 个 OpenML 数据集上的结论是：自动化框架**在 7/12（≈58%）任务上优于或持平于 ML 社区的历史人工结果**——即**约 42% 的任务自动化不如人**。
2. **AutoML 的"自动"= 搜索 + 组合 + 预算分配，不是"发明新算子"**：auto-sklearn 2.0（Feurer、Eggensperger、Falkner、Lindauer、Hutter，**JMLR 23(261), 2022**）相对于 auto-sklearn 1.0 与其他框架**最多把相对误差降低 4.5 倍**，并做到"**10 分钟的结果显著优于 auto-sklearn 1.0 一小时的结果**"——但它的两把武器是（a）PoSH（successive halving 式 bandit 预算分配）和（b）一种 **meta-feature-free 的元学习**，两者都在**既有的 110 个超参数/15 个分类器/14 个预处理器空间**内工作。AutoGluon 自己的消融实验更直白：去掉多层 stacking（NoMultiStack）后 rescaled loss 从 **0.1660 恶化到 0.5237**，**4 小时的无 stacking 版本通常打不过 1 小时的完整版**——说明收益主要来自**集成组合策略**，而非"搜到了神奇的单模型"。
3. **对阙疑"自动调验证器阈值"是直接可用的，但要走"算法配置（algorithm configuration）"这条支线，不是 AutoML 主线**：SMAC3 / irace / ParamILS 这一支明确面向**任意算法的参数**，包括非机器学习程序。ParamILS（Hutter、Stützle、Leyton-Brown、Hoos，*JAIR* 36:267–306, 2009）配置 SAT 求解器与 CPLEX 的结果是：即便这些算法"**默认参数是人工投入大量精力调出来的**"，自动配置仍能取得"substantial and consistent performance improvements"。**这才是阙疑 44 条 block 规则阈值该用的工具**，因为它不需要"损失函数可微"，只需要"目标可度量"。

---

## 精确数字与案例

### 一、AutoGluon-Tabular：AutoML 最强实证（以及它的边界）

论文：*AutoGluon-Tabular: Robust and Accurate AutoML for Structured Data*，arXiv:2003.06505（2020-03-14），AWS/亚马逊团队。

**实验构成（逐字取自 ar5iv 全文）**：
- **50 个**分类与回归任务：来自 OpenML AutoML Benchmark 的 **39 个**（每数据集 10 个训练/测试划分 ⇒ 共 **390** 个预测问题）+ 来自 Kaggle 的 **11 个**竞赛。
- 主预算 **4h**；OpenML 部分另跑 1h，Kaggle 部分另跑 8h；otto 竞赛另跑 24h。
- 对比框架：**TPOT、H2O AutoML、auto-sklearn、Auto-WEKA、GCP-Tables（Google AutoML Tables）**。

**Table 2（39 个 AutoML Benchmark 数据集，4h）逐字数字**：

| Framework | Wins vs AutoGluon | Losses | Failures | Champion | Avg. Rank | Avg. Rescaled Loss | Avg. Time (min) |
|---|---:|---:|---:|---:|---:|---:|---:|
| **AutoGluon** | – | – | **1** | **23** | **1.8438** | **0.1385** | 201 |
| H2O AutoML | 4 | 26 | 8 | 2 | 3.1250 | 0.2447 | 220 |
| TPOT | 6 | 27 | 5 | 5 | 3.3750 | 0.2034 | 235 |
| GCP-Tables | 5 | 20 | 14 | 4 | 3.7500 | 0.3336 | 195 |
| auto-sklearn | 6 | 27 | 6 | 3 | 3.8125 | 0.3197 | 240 |
| Auto-WEKA | 4 | 28 | 6 | 1 | 5.0938 | 0.8001 | 244 |

**Table 3（11 个 Kaggle 竞赛，4h；均值只在 7 个"全部框架都跑成功"的竞赛上计算）**：AutoGluon Champion **7**、Failures **0**、Avg. Rank **1.7143**、Avg. Percentile **0.7041**；第二名为 GCP-Tables 0.6281，最差 Auto-WEKA 0.2056。

**具体排行榜数字（逐字引文）**：
> "Even just the 4h training used in our benchmark sufficed for AutoGluon to perform very well in some competitions, placing **42 / 3505** and **39 / 2920** on the official leaderboards of the otto and bnp-paribas competitions, respectively."

24h 延长版：otto **23/3505**，*"AutoGluon managed to outperform **99.3%** of the participating data scientists."*

**消融（Table 5，4h AutoML Benchmark）——这条最关键**：

| 变体 | Avg. Rank | Avg. Rescaled Loss |
|---|---:|---:|
| **AutoGluon（完整）** | **1.9324** | **0.1660** |
| NoRepeat（只跑单轮 k-fold bagging） | 2.1216 | 0.2199 |
| **NoMultiStack（去掉多层堆叠）** | 2.8514 | **0.5237** |
| NoBag | 3.9054 | 0.7199 |
| NoNetwork | 4.1892 | 0.8171 |

> "Even after 4h of training, the *NoMultiStack* variant could usually not outperform the full version of AutoGluon trained for only 1h."

**对阙疑的直接读法**：AutoGluon 的胜利是**"多层 stacking + 重复 bagging + 神经网络底座"这套组合策略**的胜利。如果把搜索空间里的 stacking 拿掉，多给 4 倍的时间也补不回来。**这说明"时间/算力"不能替代"搜索空间的结构设计"**——映射到阙疑：给验证器更多 CPU 去搜阈值，不能替代"规则集合本身是否覆盖了正确的缺陷维度"。

### 二、auto-sklearn 2.0：元学习与 warm start 的真实形态

论文：*Auto-Sklearn 2.0: Hands-free AutoML via Meta-Learning*，Matthias Feurer、Katharina Eggensperger、Stefan Falkner、Marius Lindauer、Frank Hutter（均属弗莱堡大学 ML 组）。arXiv:2007.04074（v1 2020-07-08，v3 2022-10-04），**Journal of Machine Learning Research 23(261), 2022**。

**摘要逐字关键句**：
> "We develop PoSH Auto-sklearn, which enables AutoML systems to work well on large datasets under rigid time limits by using a new, simple and **meta-feature-free meta-learning** technique and by employing a successful **bandit strategy for budget allocation**."
> "...reducing the relative error by **up to a factor of 4.5**, and yielding a **performance in 10 minutes that is substantially better than what Auto-sklearn 1.0 achieves within an hour**."

**这里必须诚实拆穿一个常见误解**：auto-sklearn 2.0 明确宣称自己是 **meta-feature-free** 的元学习——它**不再**用"数据集元特征 → 相似数据集 → 迁移最优配置"这条经典路线，而是改成"用一组在历史数据集上表现良好的**配置集合（portfolio）**作为初始设计 + 用 bandit 分配预算"。也就是说，**2022 年 SOTA 的 AutoML 元学习，恰恰放弃了"从数据特征泛化出新配置"这条路**，退回到"记住过去好用的配置清单"。

**对"验证器能否自己发现新规则"的含义**：连 AutoML 这个把元学习当核心卖点的领域，其最强工程实现都**不敢**做"模型自己提出新的超参数维度"。它做的是"在 39 个历史数据集上预先跑出的 portfolio 里挑"。**这恰恰给了阙疑一个诚实可行的中间路线**：不是让 gate_engine.py 发明第 68 条规则，而是让它**在 37 张实卡上维护一个"哪些规则组合曾抓到过缺陷"的 portfolio**，新卡进来时按 portfolio warm start。

**前代**：auto-sklearn 1.0 = *Efficient and Robust Automated Machine Learning*，NeurIPS 2015（papers.neurips.cc/paper/5872），同样是 Feurer 等，卖点是 **Bayesian optimization + meta-learning + ensemble construction** 三件套。

### 三、CASH 问题、FLAML、TPOT、H2O：工具谱系与预算敏感性

- **CASH（Combined Algorithm Selection and Hyperparameter optimization）**：把"选算法"和"调超参"合成一个联合优化问题。它是 AutoML 的形式化核心。注意：CASH 的**形式化本身假设搜索空间（算法集合 + 每个算法的超参数及其取值范围）由人给定**。这是 AutoML 无法自我扩展搜索空间的**结构性根源**——形式上，CASH 优化的是 θ ∈ Θ，而 Θ 是外生给定的。
- **TPOT**：*TPOT: A Tree-based Pipeline Optimization Tool for Automating Machine Learning*，Olson & Moore，PMLR 64（AutoML Workshop @ ICML 2016）。用**遗传编程**演化 sklearn pipeline 树——这是 AutoML 里最"像自动发明"的一支（它能长出新的 pipeline 拓扑），但**算子集合仍是人工设定的 sklearn 原语**。在 AutoGluon 的 4h 对照中 TPOT 为 Champion 5/39，Avg. Rank 3.3750（第三名）。
- **FLAML**：*FLAML: A Fast and Lightweight AutoML Library*，Chi Wang、Qingyun Wu、Markus Weimer、Erkang Zhu（Microsoft），**MLSys 2021**。摘要逐字：*"It significantly outperforms top-ranked AutoML libraries on a large open source AutoML benchmark under equal, or sometimes **orders of magnitude smaller** budget constraints."* 注意摘要**没有给出具体倍数**，只给了"orders of magnitude"这种定性表述——**引用时不要替它补数字**。
- **H2O AutoML**：*H2O AutoML: Scalable Automatic Machine Learning*，ICML 2020 AutoML Workshop（H2O.ai，Erin LeDell 等）。实验规模值得记录：在 Airlines 数据集（**~150M 行**）上做 10k / 100k / 1M / 10M / 100M 行五个量级子集，测试集 100k，硬件 **c5.metal（96 vCPU / 192G RAM）**，H2O **3.30.0.3**。它是 AutoML 里唯一明确把**规模可扩展性**当卖点的分支。

### 四、AMLB：唯一诚实的跨框架基准，以及它对自己结论的封杀

论文：*AMLB: an AutoML Benchmark*，Pieter Gijsbers 等，arXiv:2207.12560（2022），JMLR 25（22-0493）。规模：**9 个 AutoML 框架、71 个分类任务 + 33 个回归任务 = 104 个任务**。

**但 AMLB 官方结果页（openml.github.io/automlbenchmark/results.html）自己挂出的警示，逐字如下**：
> "We use AutoML framework versions from **September 2021**, many frameworks have since seen major updates."
> "We use the 'benchmark' modes of the frameworks, which generally *only* optimize for performance."
> "**Results can not be used to make conclusions about which algorithm is best**, as all frameworks differ in multiple ways."
> "Performance statistics are often independent from many qualitative differences, such as ease of use or interpretability."

**这是本方向最该被阙疑吸收的一条方法论**：一个做了 104 个任务的基准，官方第一句话是"别用它来下结论"。**阙疑论文里的 30 盲 holdout / 40 外部 corpus 数字（66.7%、43.8%）必须同样挂出这种自限声明**，否则在 NeurIPS E&D 的"evaluation itself becomes an object of scientific study"定位下会被当成天真。

### 五、NAS 与 AutoML 的关系：搜索空间换来的确实是真的

**EfficientNet**（Tan & Le，ICML 2019，arXiv:1905.11946）是 NAS 支线最硬的证据。摘要逐字：
> "To go even further, we use neural architecture search to design a new baseline network and scale it up to obtain a family of models, called EfficientNets... our EfficientNet-B7 achieves state-of-the-art **84.3% top-1 accuracy** on ImageNet, while being **8.4x smaller and 6.1x faster on inference** than the best existing ConvNet."

（注：arXiv v5 摘要与部分镜像站写 84.3%，ICML 论文集页面写作 **84.4% top-1 / 97.1% top-5**；**两个数字都存在，引用时须注明版本**。迁移学习：CIFAR-100 **91.7%**、Flowers **98.8%**。B0 由 NAS 搜出，B1–B7 由复合缩放系数 φ 放大。）

**诚实评价**：EfficientNet 的增益来自"**NAS 搜出 B0 基线 + 人工设计的复合缩放规则**"。**复合缩放公式是人的贡献，不是 NAS 的贡献**。这是 AutoML 类工作最典型的真实结构：**机器搜局部，人给骨架**。

### 六、AutoML vs 人工：唯一直接对标的公开数字

*Can AutoML outperform humans? An evaluation on popular OpenML datasets using AutoML Benchmark*，Marc Hanussek、Matthias Blohm、Maximilien Kintz，AIRC 2020 Conference Proceedings（arXiv:2009.01564，v2 2020-12-15）。

**摘要逐字**：
> "This paper compares four AutoML frameworks on 12 different popular datasets from OpenML; six of them supervised classification tasks and the other six supervised regression ones. Additionally, we consider a real-life dataset from one of our recent projects. The results show that the automated frameworks **perform better or equal than the machine learning community in 7 out of 12 OpenML tasks**."

**即 7/12 ≈ 58% 优于或持平，5/12 ≈ 42% 不如人。**这是一个 12 数据集的小样本、来自非顶会（AIRC）会议的研究，**不能当作定论**，但它是目前能找到的、直接回答"AutoML 相对人工调参真实提升幅度"的**唯一**公开量化证据，而且它给出的答案是**克制的**。相比之下，网上大量博客（如 johal.in、CSDN、华为云社区等）给出的"H2O 提升 15% AUC""AutoGluon 提升 12%"等数字**均无论文出处、无数据集协议、疑似 AI 生成内容，本文件一律不予采信**，并在盲区中标记。

### 七、算法配置（Algorithm Configuration）：真正对阙疑有用的那一支

- **ParamILS**：Hutter、Stützle、Leyton-Brown、Hoos，*Journal of Artificial Intelligence Research* 36:267–306, **2009**（arXiv:1401.3492 为 JAIR 存档版）。摘要逐字：
> "We describe the results of a comprehensive experimental evaluation of our methods, based on the configuration of prominent complete and incomplete algorithms for SAT. We also present what is, to our knowledge, the first published work on automatically configuring the **CPLEX mixed integer programming** solver. All the algorithms we considered had default parameter settings that were **manually identified with considerable effort**. Nevertheless, using our automated algorithm configuration procedures, we achieved **substantial and consistent performance improvements**."

**这段是本方向对阙疑最重要的一句话**：被配置的算法（SAT 求解器、CPLEX）**已经是人类专家精心调过的**——自动配置**仍然**能稳定提升。这说明"人工阈值已经调过"**不构成**"不需要再自动调"的理由。
- **SMAC3**（automl/SMAC3，弗莱堡组）：官方定位逐字为"a tool for **algorithm configuration** to optimize the parameters of **arbitrary algorithms**"——明确**不限于 ML**。
- **irace**（Manuel López-Ibáñez 等，R 包，ORP 2016 论文）：*"an automatic configuration tool for tuning optimization algorithms"*，同样面向通用算法。

**这三者与 AutoML 主线（auto-sklearn / AutoGluon / FLAML）的关键区别**：后者要求"训练一个模型 + 用验证集打分"；前者只要"给一组配置 → 跑一遍 → 返回一个标量代价"。**阙疑的 gate_engine.py 是确定性程序、无梯度、无训练集，只能走前者。**

---

## 对阙疑的 3 条具体行动

1. **把"自动调阈值"从 AutoML 主线切到算法配置支线，并给出明确的字段与工具（时间点：2027-03 前完成第一版，2027-06 前出论文用数据）**。具体做法：在 `gate_engine.py`（当前 3826 行）中把 67 条规则的**可量化旋钮**抽成一个显式配置向量 θ（建议字段：`rules/<id>/threshold`、`rules/<id>/weight`、`rules/<id>/severity∈{block,warn,advice}`，先在 block 44 条上做），写成一个 JSON schema 文件 `_arch_v47/rule_config_space.json`。然后用 **SMAC3**（`pip install smac`，弗莱堡 automl 组，`https://github.com/automl/SMAC3`）或 **irace** 配置。目标函数必须**明确写成标量**：建议 `cost(θ) = -(检出率) + λ·(误报率)`，其中检出率在**真实缺陷夹具 15（当前重注入 6/6，历史覆盖 12/15 = 80%）**与**盲 holdout 30（真错 17，当前检出 66.7%）**上测，λ 先用 1.0 并做 λ∈{0.5,1,2,4} 敏感性扫描。**绝不能**用变异分数（core 97.3% / all 81.5%）当目标——该指标已被本项目判定作废。
2. **建立"规则 portfolio"而不是"规则发明器"（时间点：2027-05 前，对应论文 Method 一节）**。直接照抄 auto-sklearn 2.0 的 **meta-feature-free meta-learning**：在 37 张实卡上离线枚举"规则子集 → 抓到哪些缺陷"的历史记录，沉淀成一个 portfolio 文件 `_arch_v47/rule_portfolio.json`（格式建议：`{"card_features": {...}, "top_k_configs": [θ1, θ2, ...]}`）。新卡进来时按 portfolio 做 warm start，**只从 portfolio 里挑组合，不允许生成新规则**。论文里必须明写一句"our search space is fixed at 67 rules; we make no claim of rule invention"——这既符合事实，也正是 E&D Track 欣赏的克制。同时把 AMLB 的自我封杀式警示（"Results can not be used to make conclusions about which algorithm is best"）**逐字风格**复刻进 `research/12_threats_to_validity.md` 新增小节 **T-AutoML**，说明 30/40 样本量与框架版本冻结问题。
3. **补一个"AutoML 是否真的比人强"的对照实验，作为论文的 negative result 卖点（时间点：2027-08 前）**。仿 Hanussek 等（2020）的 12 数据集协议，做一个**人 vs 机器**的极小对照：让作者本人（阙疑，嵌入式方向）手工为 37 张实卡调一遍规则阈值，记录耗时与最终检出率；再让 SMAC3 在同一搜索空间跑 **4 小时**与 **10 分钟**两档（对应 auto-sklearn 2.0 的"10 min vs 1 hour"叙事框架），报告两者在盲 holdout 30 与夹具 15 上的差。**如果机器没赢，就照实写**——NeurIPS E&D 明确欢迎 negative results 且明确 "Submissions need not introduce a new model or outperform prior work"。这个实验同时直接对冲本项目最大风险（Pangram 3.3.2 对 AI 生成内容的 desk reject）：一手人工对照数据是 AI 检测器最不容易判为生成的材料。

---

## 盲区（诚实标注）

- **"AutoML vs 人工调参"的真实提升幅度，缺乏高质量大样本证据**。唯一的直接对标研究（Hanussek 等 2020）只有 **12 个 OpenML 数据集**、发表于 AIRC（非顶会）、且未报告效应量与置信区间。网上流传的"提升 15%""提升 12%""提升 25%"等数字来自 johal.in、CSDN、华为云社区、milvus blog 等**疑似 AI 生成的 SEO 页面**，本文件**全部拒绝采信**，也未找到可替代的顶会级证据。**论文中若需此数字，只能引用 7/12 并明确标注其样本量与会议层级。**
- **FLAML 摘要未给出具体倍数**（只有 "orders of magnitude smaller budget"）。我未能核实 MLSys 2021 正文中的量化对照表（未能打开正文 PDF 的 Table）。**引用 FLAML 时不得补数字。**
- **AMLB 的框架排名数据未取得**：ar5iv 对 2207.12560 的镜像返回 "no healthy upstream"，我只取得了规模（9 框架 / 71 分类 + 33 回归 = 104 任务）与官方结果页的自我限制声明，**未取得各框架的具体排名数字**。因此本文件**不做**"哪个 AutoML 框架最好"的判断。
- **auto-sklearn 2.0 的 "factor of 4.5" 是"up to"（上限）**，是与 auto-sklearn 1.0 及"other popular AutoML frameworks"比较下的最大相对误差降低倍数，**不是平均提升**。我在正文中已按"up to"表述；若论文引用需保留"最多"二字。
- **EfficientNet 的 84.3% vs 84.4% 存在版本差异**：arXiv v5 摘要（2020-09-11）写 **84.3%**，ICML 2019 论文集页面写 **84.4% top-1 / 97.1% top-5**。**未确认哪个是最终 camera-ready**，引用时必须双注。
- **"AutoML 用于规则系统 / 静态分析阈值自动调"这一具体交叉领域，我没有找到成熟文献**。搜索"AutoML + rule mining / static analysis / threshold"只返回了 2023–2026 年的 LLM 生成规则工作（如 arXiv:2410.04715 的 rule-based data selection、RuleMaster+ 的 IDS 规则生成），**均为 LLM 路线而非 AutoML 路线**，与阙疑的确定性内核不直接可比。这是一个真实的研究空白，也意味着**第 1 条行动若要发表， novelty 论证要靠"确定性验证器 + 算法配置"的组合，而非靠 AutoML 本身**。
- **样本偏差**：本方向引用的所有量化结论都来自**表格数据 / 图像分类 / SAT 求解**领域，**没有一个是"知识断言判定"领域**。从 CASH 到阙疑规则的迁移是**类比**，不是已验证的迁移。

---

## 来源

1. *AutoGluon-Tabular: Robust and Accurate AutoML for Structured Data*（Erickson 等，AWS，2020-03-14）— https://arxiv.org/abs/2003.06505 与全文 https://ar5iv.labs.arxiv.org/html/2003.06505 — 50 数据集（39 OpenML + 11 Kaggle）、4h 预算、Champion 23/39 与 7/11、otto 42/3505、bnp 39/2920、24h 23/3505 = 99.3%、NoMultiStack loss 0.5237 vs full 0.1660、Avg. Rank 1.8438/1.7143 — 2020
2. *Auto-Sklearn 2.0: Hands-free AutoML via Meta-Learning*（Feurer、Eggensperger、Falkner、Lindauer、Hutter，弗莱堡大学，JMLR 23(261) 2022）— https://arxiv.org/abs/2007.04074 — "meta-feature-free meta-learning"、"bandit strategy for budget allocation"、"reducing the relative error by up to a factor of 4.5"、"performance in 10 minutes... better than Auto-sklearn 1.0 within an hour"、39 AutoML benchmark datasets — 2022
3. *Efficient and Robust Automated Machine Learning*（Feurer 等， NeurIPS 2015）— https://papers.neurips.cc/paper/5872-efficient-and-robust-automated-machine-learning.pdf — "AUTO-SKLEARN performs favorably against the previous state of the art in AutoML"、Bayesian optimization + meta-learning + ensemble construction — 2015
4. *FLAML: A Fast and Lightweight AutoML Library*（Chi Wang、Qingyun Wu、Markus Weimer、Erkang Zhu，Microsoft，MLSys 2021）— https://proceedings.mlsys.org/paper_files/paper/2021/hash/1ccc3bfa05cb37b917068778f3c4523a-Abstract.html — "orders of magnitude smaller budget constraints"（摘要无具体倍数）— 2021
5. *TPOT: A Tree-based Pipeline Optimization Tool for Automating Machine Learning*（Olson & Moore，PMLR 64，AutoML Workshop @ ICML 2016）— https://proceedings.mlr.press/v64/olson_tpot_2016 — 遗传编程 pipeline 优化 — 2016
6. *AMLB: an AutoML Benchmark*（Gijsbers 等，arXiv:2207.12560，JMLR 25:22-0493）— https://arxiv.org/abs/2207.12560 与结果页 https://openml.github.io/automlbenchmark/results.html — 9 框架 / 71 分类 + 33 回归 = 104 任务；官方自限声明"Results can not be used to make conclusions about which algorithm is best"、框架版本冻结于 2021-09 — 2022 / 2024 页面更新
7. *Can AutoML outperform humans? An evaluation on popular OpenML datasets using AutoML Benchmark*（Hanussek、Blohm、Kintz，AIRC 2020）— https://arxiv.org/abs/2009.01564 — "perform better or equal than the machine learning community in 7 out of 12 OpenML tasks"、4 个框架、12 个 OpenML 数据集 + 1 个真实项目数据集 — 2020
8. *ParamILS: An Automatic Algorithm Configuration Framework*（Hutter、Stützle、Leyton-Brown、Hoos，JAIR 36:267–306, 2009）— https://arxiv.org/abs/1401.3492 — "default parameter settings that were manually identified with considerable effort"、"substantial and consistent performance improvements"、SAT 求解器与 CPLEX 配置 — 2009
9. *EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks*（Tan & Le，Google Brain，ICML 2019）— https://arxiv.org/abs/1905.11946 — "84.3% top-1"（arXiv v5）/"84.4% top-1 / 97.1% top-5"（ICML 论文集）、"8.4x smaller and 6.1x faster on inference"、CIFAR-100 91.7%、Flowers 98.8% — 2019
10. *H2O AutoML: Scalable Automatic Machine Learning*（H2O.ai / Erin LeDell 等，ICML 2020 AutoML Workshop）— https://github.com/h2oai/h2o-automl-paper 与 https://www.automl.org/wp-content/uploads/2020/07/AutoML_2020_paper_61.pdf — Airlines ~150M 行、10k/100k/1M/10M/100M 子集、H2O 3.30.0.3、c5.metal 96 vCPU / 192G RAM — 2020
11. SMAC3 官方文档 — https://automl.github.io/SMAC3/main/ — "a tool for algorithm configuration to optimize the parameters of arbitrary algorithms"（明确面向任意算法，不限于 ML）— 2026 页面
12. irace: Iterated Racing for Automatic Algorithm Configuration（López-Ibáñez、Dubois-Lacoste、Pérez Cáceres，曼彻斯特大学）— https://github.com/MLopez-Ibanez/irace — "an automatic configuration tool for tuning optimization algorithms" — 2016 论文 / 持续维护
13. Meta-learning and AutoML Tutorial（IJCAI 2020，王鑫等）— https://mn.cs.tsinghua.edu.cn/xinwang/ijcai2020Tutorial.htm — meta-learning 与 AutoML 的"learning to learn"同构关系 — 2020
