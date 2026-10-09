# 698-E · 定向深度文献调研（针对 697 新概念）

- **批次**：698 ｜ **任务**：E ｜ **日期**：2026-10-09
- **目标**：针对 697 提出的新概念（结构性 Goodhart / 测量漂移代数 / 可检测性上限 / 评估器审计）
  做**定向**深度调研，而不是重复 695 的 82 篇通用调研。
- **红线**：`detect_calls = 0`；**0 处**论文正文/bib 修改。

---

## 0. 核验状态图例（**先读这个，再看任何一篇**）

| 标记 | 含义 |
|:--:|---|
| ✅**本批** | **本批（698）联网检索/抓取核验**：标题、作者、年份、arXiv id / DOI 已核对 |
| ✅**695** | 695 批次联网核验过（82 篇全部核验）；本批**未重新抓取**，沿用其结论 |
| 📕**经典** | 书籍 / 期刊经典文献，无 arXiv；给出出版信息，**未联网核验** |
| ⚠️**待确认** | **无法联网核验**（未找到可访问入口）⇒ 引用前**必须**自行核对 |

**统计**：共 **46 篇**（去重后）。其中 ✅本批 **14** 篇、✅695 **9** 篇、📕经典 **14** 篇、⚠️待确认 **9** 篇。

---

## 方向 1 · 结构性 Goodhart 的相关文献（13 篇）

### 1.1 核心问题

697 提出「结构性（被动）Goodhart」：**不需要任何优化压力**，仅口径变化就使报告值偏移。
本方向要回答：**有没有人提出过类似概念？**

### 1.2 文献

| # | 标题 | 作者 | 年 | Venue | URL | 核心贡献 | 与 697 的关系 | 核验 |
|:--:|---|---|---:|---|---|---|---|:--:|
| 1 | Categorizing Variants of Goodhart's Law | Manheim & Garrabrant | 2018 | arXiv | https://arxiv.org/abs/1803.04585 | 把 Goodhart 分为 **4 个变体**：Extremal / Causal / Adversarial / Regressional | **最重要的对照**：4 个变体**全部以"过度优化"为前提**（"a metric which can be used to improve a system is used to such an extent that further optimization is ineffective or harmful"）⇒ 与 697 的"无优化压力"**正交** | ✅本批 |
| 2 | The Strong, Weak and Benign Goodhart's law: An independence-free and paradigm-agnostic formalisation | Majka & El-Mhamdi | 2025 | arXiv | https://arxiv.org/abs/2505.23445 | 去掉独立性假设与学习范式限制，研究代理-目标**耦合**时的 Goodhart 效应 | 697 的**头号形式化模板**；但**仍以优化压力为前提**（过优化速率、重尾偏差）⇒ 697 的 SG-3 排除的正是这个前提 | ✅695 |
| 3 | Goodhart's Law in Reinforcement Learning | Karwowski, Hayman, Bai, Kiendlhofer, Griffin, Skalse | 2023 | arXiv | https://arxiv.org/abs/2310.09144 | 量化 Goodhart 幅度 + **几何刻画** + **可证明规避的最优早停法** | 697 §4.2 的反例基础：**早停需要"优化轨迹"**，而结构性子类没有轨迹 ⇒ 处方不适用 | ✅695 |
| 4 | Scaling Laws for Reward Model Overoptimization | Gao, Schulman, Hilton | 2022 | arXiv | https://arxiv.org/abs/2210.10760 | 奖励模型作为不完美代理，**过度优化**会损害真实性能 | 经典"优化压力"范式；697 明确切分 | ✅本批 |
| 5 | Reward Hacking in the Era of Large Models: Mechanisms, … | （未逐字核验作者） | 2026 | arXiv | https://arxiv.org/html/2604.13602v1 | 综述大模型时代的 reward hacking 机制 | 最新综述，说明该范式仍活跃；**仍以优化者存在为前提** | ✅本批（摘要级） |
| 6 | Concrete Problems in AI Safety | Amodei, Olah, Steinhardt, Christiano, Schulman, Mané | 2016 | arXiv | https://arxiv.org/abs/1606.06565 | 提出 reward hacking 等 5 类安全问题 | reward hacking 的源头定义；697 SG-3 说明 Queyi 场景**无优化者** | ⚠️待确认（id 凭记忆） |
| 7 | The Coin Flip Judge? Reliability and Bias in LLM-as-a-Judge Evaluation | （未逐字核验作者） | 2026 | arXiv | https://arxiv.org/abs/2606.13685 | 29 个任务、2 个 OpenAI judge、50 次成对比较，考察 judge 可靠性 | 说明"高一致性 ≠ 有效"；属**评估器不可靠**（≠ 口径漂移），但同属"测量出问题" | ✅本批 |
| 8 | Reliability without Validity: A Systematic, Large-Scale Evaluation | （未逐字核验作者） | 2026 | arXiv | https://arxiv.org/abs/2606.19544v1 | 系统评估 LLMaJ 的可靠性失效模式 | **标题就是 697 的核心论点**："可靠性 ≠ 有效性" —— 与 697 的"报告值 ≠ 机制量"同构 | ✅本批 |
| 9 | Goodhart's Law（原始表述） | Charles Goodhart | 1975 | 论文（货币政策） | — | "任何被观测到的规律，一旦被用于控制，就会失效" | 经典根；697 的命名来源 | 📕经典 |
| 10 | Improving Ratings: Audit in the British University System | Marilyn Strathern | 1997 | European Review 5(3) | https://doi.org/10.1002/(SICI)1234-981X(199707)5:3<305::AID-EURO184>3.0.CO;2-4 | "当测量成为目标，它就不再是好测量" | 经典表述；**同样预设"成为目标"** | 📕经典 |
| 11 | The Tyranny of Metrics | Jerry Z. Muller | 2018 | 书（Princeton UP） | — | 指标崇拜的制度性批判 | 治理叙事，非形式化；697 需要的是**数学对象** | 📕经典 |
| 12 | HackDetect / protocol validity（695 方向 1 #3） | （695 已核验） | 2026 | arXiv | （695 已登记，本批未取回 id） | 形式化 **protocol validity** + **Mislead gap**（exploit − intended） | **方法论最近邻**；区别：它的 gap 是**对抗性利用**，697 是**非对抗装置退化** | ✅695 |
| 13 | Leaderboard Illusion | （685 已收录） | 2025 | arXiv | （本批未核验 id） | 榜单生态的失真机制 | 榜单层面的 Goodhart；**仍含优化者**（刷榜） | ⚠️待确认 |

### 1.3 关键发现

> ### 结论 E1：**没有找到「结构性 / 被动 Goodhart」的直接对应概念。**
>
> 检索到的**全部** Goodhart 形式化工作（#1 Manheim-Garrabrant 的 4 变体、
> #2 Majka-El-Mhamdi、#3 Karwowski、#4 Gao、#5 综述）**都以"被优化"或"被利用"为前提**。
> #1 的原文措辞最明确："a metric **which can be used to improve a system** is used to such an extent…"
> —— 无优化者时，该定义不适用。
>
> ⇒ **697 的 SG-3（无优化者）是一个真实的概念空位**。
> 但**必须诚实标注**：本批**没有做文献计量学意义上的穷尽检索**
> （只做了 4 组关键词检索 + 若干抓取），因此**只能说"在本次检索范围内未发现"**，
> **不能**说"无人提出过"。
>
> **对外措辞建议**：`"a subclass we name and formalise"`，并引用 #1/#2/#3 作对照
> （与 697-A §6、697-E 红线 16 一致）。

---

## 方向 2 · 测量理论在 CS 中的应用（11 篇）

### 2.1 核心问题

心理学/社会学的**测量理论**（构念效度、测量不变性）如何迁移到 CS / ML 评估？

### 2.2 文献

| # | 标题 | 作者 | 年 | Venue | URL | 核心贡献 | 与 697/698 的关系 | 核验 |
|:--:|---|---|---:|---|---|---|---|:--:|
| 14 | **A Judge Should Know What Changed: Construct Validity for LLM-as-a-Judge Evaluation** | Jianlin Chen, Wenhui Chen, Ziyao Lin, Chi Man Vong | 2026 | arXiv (cs.AI) | https://arxiv.org/abs/2608.24419 | 把 judge 的**构念效度**形式化为**二维剖面**：**不变性 $S$**（构念保持编辑下裁决不变的概率）+ **构念敏感性 $R$**（最小构念改变编辑下裁决改变的概率）；证明 $S,R$ **相互独立**、**不存在保留全部比较的标量汇总**；7 judge × 4 领域 × 7 干预 + 5 控制实测：$S{=}0.945$ 但 $R{=}0.319$；并审计 5 个公开标签集（表面特征可复现 55–67% 标签，含 MT-Bench 人类投票的 67.4%） | **本批找到的最重要一篇**。它的 $S$/$R$ 二维剖面与本框架的 Step 1（声明口径）+ Step 4（量化漂移）**高度同构**；"不存在标量汇总"直接支持 697 的"单一 recall 数不足以描述一次测量"（692 §4）；"审计验证集本身"= 698-D 的审计对象 | ✅本批（**抓取原文摘要**） |
| 15 | Measuring What Matters: Construct Validity in Large Language Model Benchmarks | （29 位作者） | 2025 | NeurIPS 2025 | https://papernotes.org/NeurIPS2025/recommender/measuring_what_matters_construct_validity_in_large_language_model_benchmarks/ | 29 位专家系统综述 **445 篇 LLM benchmark 论文**，从构念效度角度审视 | 说明"benchmark 的构念效度"已是热点；697/698 的增量在**漂移的代数化**（不是效度分类） | ✅本批 |
| 16 | The Benchmarking Epistemology: Construct Validity for Predictive Benchmarking | （未逐字核验作者） | 2025 | arXiv | https://arxiv.org/pdf/2510.23191 | 预测式基准的构念效度框架 | 与 #15 同族；提供"效度"的标准词汇表 | ✅本批 |
| 17 | AI Measurement Science（教科书第 1 章：Validity） | Stanford AIMS Lab | 2026 | 在线教科书 | https://aimslab.stanford.edu/textbook/src/chap1.html | 区分 content / criterion / **construct** / external / consequential 五类效度 | **词汇来源**：本框架用"构念"时应引此；也说明 CS 正在**主动吸收心理测量学** | ✅本批 |
| 18 | Convergent and Discriminant Validation by the Multitrait-Multimethod Matrix | Campbell & Fiske | 1959 | Psychological Bulletin 56(2) | — | **MTMM 矩阵**：用多方法多特质矩阵分离方法方差与特质方差 | **与 698-B 的转移矩阵同构**！MTMM 分离"方法效应"vs"特质效应"，本批的 $T$ 分离"口径效应"vs"机制效应" ⇒ 可引为**方法论先例** | 📕经典 |
| 19 | Validity of Psychological Assessment | Samuel Messick | 1995 | American Psychologist 50(9) | — | 把效度统一为**构念效度的推论链**（内容/实质/结构/概化/外部/后果六面） | 提供"效度不是分数属性，而是**推论属性**"的论点 ⇒ 支持"数字必须随附口径" | 📕经典 |
| 20 | The Attack of the Psychometricians | Denny Borsboom | 2006 | Psychometrika 71(3) | — | 批判"把构念等同于测量模型"的循环 | **反身性警告**：不要用测量模型定义构念 ⇒ 与 697 定理 A1（不可识别）呼应 | 📕经典 |
| 21 | Measurement Invariance, Factor Analysis and Factorial Invariance | William Meredith | 1993 | Psychometrika 58(4) | — | 测量不变性的形式化（弱/强/严格不变性） | **"不变性"概念的直接来源**；697 的"对哪些口径承诺不变"（公理 A4）可视为其 CS 版 | 📕经典 |
| 22 | AI and the Everything in the Whole Wide World Benchmark | Raji, Bender, Paullada, Denton, Hanna | 2021 | NeurIPS Datasets & Benchmarks | https://arxiv.org/abs/2111.15366 | 批判"通用能力"基准的构念有效性 | 说明"基准测的不是它声称的东西"；与 697 的"报告值 ≠ 机制量"同源 | ⚠️待确认（id 凭记忆） |
| 23 | Pervasive Label Errors in Test Sets Destabilize Machine Learning Benchmarks | Northcutt, Athalye, Mueller | 2021 | NeurIPS Datasets & Benchmarks | https://arxiv.org/abs/2103.14749 | 用 confident learning 发现测试集标签错误普遍存在 | 与 697/698 的**标签漂移（Type III）**相关；但它是"标签错"，不是"标签口径变" ⇒ **必须区分** | ⚠️待确认（id 凭记忆） |
| 24 | Evaluation Gaps in Machine Learning Practice | Hutchinson, Smart, Hanna, Denton, Greer, Kjartansson, Barnes, Mitchell | 2022 | ACM FAccT | https://arxiv.org/abs/2202.02211 | 实证研究 ML 实践者如何评估、哪里出问题 | 提供"评估失效"的**实证**清单；与 698-D 的 8 类失效模式可对照 | ⚠️待确认 |

### 2.3 关键发现

> ### 结论 E2：**测量理论已被 CS 主动吸收，但"漂移"尚未被代数化。**
>
> - #14 已把**构念效度**形式化为 $S/R$ 二维剖面，并证明**不存在标量汇总** —— 这是本方向最接近的工作。
> - #15/#16/#17 说明"效度"词汇已进入 ML 评估主流。
> - #18（MTMM）提供**分离方法方差与特质方差**的经典工具 —— 与 698-B 的转移矩阵同构。
> - **空位仍在**：#14 的 $S/R$ 是**概率剖面**（回答"judge 稳不稳"），
>   而 697/698 的漂移代数是**代数对象**（回答"哪些口径操作可以后处理纠正、哪些必须重测"）
>   —— 后者（可纠错边界，定理 T6）在本次检索范围内**未见对应**。

---

## 方向 3 · 不可判定性在软件验证中的最新进展（10 篇）

### 3.1 核心问题

有没有人**系统分类过**"哪些 bug 不可检测"？

### 3.2 文献

| # | 标题 | 作者 | 年 | Venue | URL | 核心贡献 | 与 698-C 的关系 | 核验 |
|:--:|---|---|---:|---|---|---|---|:--:|
| 25 | Undecidability of Static Analysis | William Landi | 1992 | ACM LOPLAS 1(4) | https://dl.acm.org/doi/10.1145/161494.161501 | 证明**两个基本静态分析问题**（含 may-alias / must-alias 的若干变体）**不可判定** | 698-C 的"∃-执行 vs 需规约"分类的**理论支柱之一**：说明"存在通用的静态分析器"不可达 | ✅本批 |
| 26 | The Undecidability of Aliasing | G. Ramalingam | 1994 | ACM TOPLAS 16(5) | https://dl.acm.org/doi/abs/10.1145/186025.186041 | **过程内** must-alias 在含 if/循环/动态存储/指针的语言中**不可判定** | 直接支撑 698-C 的 `strict_aliasing` / `type_punning` 分类（本数据中 `strict_aliasing` 检出率 **0%**） | ✅本批 |
| 27 | The Evaluation of Program-Based Software Test Data Adequacy Criteria | Elaine J. Weyuker | 1988 | CACM 31(6) | https://cacm.acm.org/research/the-evaluation-of-program-based-software-test-data-adequacy-criteria/ | 提出**充分性准则的公理集**，并证明**不存在同时满足全部公理的准则** | **与 698-C 最同构的一篇**：用公理排除"完美准则"的存在 ⇒ 698-C 用判据排除"完美检测器"的存在 | ✅本批 |
| 28 | Rice's Theorem | Henry Gordon Rice | 1953 | Transactions of the AMS 74 | — | 非平凡语义属性的判定不可解 | 698-C §1.4 的理论基础；**必须区分"判定不可解"与"检测允许错误率"** | 📕经典 |
| 29 | On Computable Numbers, with an Application to the Entscheidungsproblem | Alan Turing | 1936 | Proc. LMS | — | 停机问题不可判定 | 最根本的源头 | 📕经典 |
| 30 | Social Processes and Proofs of Theorems and Programs | DeMillo, Lipton, Perlis | 1979 | CACM 22(5) | — | 论证"程序验证不能替代测试" | 支持"检测（∃-执行）与证明（∀-执行）性质不同" | 📕经典 |
| 31 | Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs | Cousot & Cousot | 1977 | POPL | — | 抽象解释框架：**可靠性 vs 完备性**的权衡 | 698-C 的 S 类（"阳性可靠、阴性不完备"）正是抽象解释意义下的**可靠但完备**分析 | 📕经典 |
| 32 | SV-COMP: State of the Art in Software Verification（竞赛报告） | Dirk Beyer 等 | 2024–2026 | TACAS / 报告 | （695-D 已提示 SV-COMP 2026 工具数需口径对齐，见 L2077） | 验证器竞赛：排名 + 正确性见证 | **"verifier leaderboard"** = 698-D 对比表中的一行；提供"验证器自身如何被评估"的现实案例 | ⚠️待确认 |
| 33 | Grammar-based Whitebox Fuzzing / 符号执行的可达性 | Godefroid, Kiezun, Levin | 2008 | PLDI | — | 用文法指导白盒 fuzzing 提高可达性 | 说明"∃-执行"在实践中靠**搜索**而非判定 ⇒ 支撑 S 类的"RE 但不可判定" | ⚠️待确认 |
| 34 | 漂移的受控注入（695 方向 1 #17） | （695 已核验） | 2026 | arXiv | （695 已登记） | 受控注入漂移以研究其可检测性 | 与 698-B 的检测预算策略同族 | ✅695 |

### 3.3 关键发现

> ### 结论 E3：**"不可判定"在软件验证里是常识，但"系统分类哪些 bug 不可检测"未见现成工作。**
>
> - #25/#26 给出**具体分析问题**的不可判定性（alias 等），但**不是**"缺陷类型的分类表"。
> - #27（Weyuker）是**方法论上的最近邻**：用公理排除"完美准则"的存在。
> - **空位**：本批的 **D/S/U 三分 + 34 类逐类归类 + L1/L2/L3 操作化**在本次检索范围内**未见对应**。
> - **必须诚实标注的两点**：
>   1. 本批的分类是**论证性**的（判据是属性的逻辑形式），**不是逐类证明**；
>   2. **"0 类 D"依赖"程序规模无界 + 存在指针/动态内存"这一前提**，对有界程序不成立。

---

## 方向 4 · 评估器审计的通用方法论（12 篇）

### 4.1 核心问题

除了 Queyi，还有谁在做"**审计评估器本身**"？

### 4.2 文献

| # | 标题 | 作者 | 年 | Venue | URL | 核心贡献 | 与 697/698 的关系 | 核验 |
|:--:|---|---|---:|---|---|---|---|:--:|
| 35 | **On Meta-Evaluation** | Hongxiao Li, Chenxi Wang, Fanda Fan, Zihan Wang, Wanling Gao, Lei Wang, Jianfeng Zhan | 2025 | arXiv (stat.ME) | https://arxiv.org/abs/2601.14262 | 给出 meta-evaluation 的**形式框架**：定义 **evaluation space** 与其结构化表示 + 基准 **AxiaBench**；首次大规模定量比较 **10 种评估方法 × 8 个应用域**；结论：**没有一种方法同时兼顾准确与高效**（DoE 与观察性设计偏离真实 ground truth 最严重）；整空间分层采样一致优于既有方法 | **本方向的头号工作**：把"评估的评估"确立为**独立科学对象**。与本框架的区别：它比较**评估方法**，本框架审计**口径漂移** —— 两者正交、可叠加 | ✅本批（**抓取原文摘要**） |
| 36 | Holistic Evaluation of Language Models (HELM) | Liang, Bommasani, Lee, Tsipras, Soylu, Yasunaga, … (Stanford CRFM) | 2022 | arXiv / TMLR | https://arxiv.org/abs/2211.09110 | 多场景 × 多指标的统一 LLM 评估，**taxonomy of desiderata** + 标准化 prompt | **定位对照**：HELM 审计**模型**（广度远超 Queyi）；本框架审计**评估器**。**绝不能说"比 HELM 更全面"**（红线 15） | ✅本批 |
| 37 | Audit-of-Audits for the Web: Bayesian Meta-Evaluation | （未逐字核验作者） | 2026 | ACM（DOI 10.1145/3774904.3792974） | https://dl.acm.org/doi/10.1145/3774904.3792974 | **Bayesian audit-of-audits**：把异质审计（count-based 与 metric-only）汇入统一后验 | "审计审计"的直接先例；**Bayesian 汇总 vs 本框架的代数化**是两条不同路线 | ✅本批 |
| 38 | A Dual-Perspective NLG Meta-Evaluation Framework | （未逐字核验作者） | 2025 | ACL 2025 (Long) | https://aclanthology.org/2025.acl-long.1327.pdf | NLG 元评估的双视角框架（不同评估器 vs 不同评估维度） | 与 #35 同族；说明 meta-evaluation 在 NLP 已是常规议题 | ✅本批 |
| 39 | A Survey on LLM-as-a-Judge | Gu, Jiang, Shi, Tan, Zhai, Xu, Li, Ma, Wang, et al. | 2024 | arXiv | https://arxiv.org/abs/2411.15594 | LLM-as-a-Judge 系统综述：可靠性、偏置、缓解策略 | 提供 judge 失效的**分类学**（位置/长度偏置、校准漂移）⇒ 698-D 领域 1 的输入 | ✅本批 |
| 40 | JudgeBench: A Benchmark for Evaluating LLM-based Judges | Tan, Zhuang, Chu, He, Wang, et al. | 2024 | arXiv / **ICLR 2025** | https://arxiv.org/abs/2410.12784 | 客观评估 LLM judge 的基准 | 说明"judge 也需要被基准化"；**审计对象是 judge 能力**，不是口径漂移 | ✅本批 |
| 41 | RewardBench: Evaluating Reward Models for Language Modeling | Lambert, Pyatkin, Morrison, Miranda, Lin, et al. | 2024 | arXiv / NAACL 2025 Findings | https://arxiv.org/abs/2403.13787 | 首个奖励模型评估基准 + 榜单 | 提供**可用的公开数据源**（698-F 实验 3 的候选数据） | ✅本批 |
| 42 | DeepFact: audit-then-score（695 方向 1） | （695 已核验） | 2026 | arXiv | （695 已登记） | 先审计事实性再打分 | **审计对象不同**（模型输出 vs 评估器口径）；是 698-D 对比表的一行 | ✅695 |
| 43 | Who Grades the Grader?（695 方向 1） | （695 已核验） | 2026 | arXiv | （695 已登记） | 对评分系统做制度审计 | **问题同构**（"谁来审计审计者"）；**方法不同**（制度 vs 代数） | ✅695 |
| 44 | HackDetect（= #12，跨列） | （695 已核验） | 2026 | arXiv | （695 已登记） | protocol validity + Mislead gap | 见方向 1 | ✅695 |
| 45 | Model Cards for Model Reporting | Mitchell, Wu, Zaldivar, Barnes, Vasserman, et al. | 2019 | ACM FAT* | https://arxiv.org/abs/1810.03993 | 模型文档模板 | **报告模板类**框架（698-D 对比表的第三类）；提供"随数字附声明"的制度先例 | ⚠️待确认（id 凭记忆） |
| 46 | Datasheets for Datasets | Gebru, Morgenstern, Vecchione, Vaughan, Wallach, et al. | 2018/2021 | CACM 64(12) | https://arxiv.org/abs/1803.09010 | 数据集文档模板 | 同上；也是 695 提到的"治理叙事" | ⚠️待确认（id 凭记忆） |

### 4.3 关键发现

> ### 结论 E4：**"审计评估器"已有多条独立路线，但"口径漂移的代数化"未见对应。**
>
> 现有工作可分为 5 条路线：
> 1. **元评估的方法比较**（#35 On Meta-Evaluation、#37 Audit-of-Audits、#38 Dual-Perspective）
>    —— 回答"哪种评估方法更可信"；
> 2. **judge 可靠性审计**（#14、#39、#40、#41、#7、#8）
>    —— 回答"judge 稳不稳 / 偏不偏"；
> 3. **报告模板**（#45 Model Cards、#46 Datasheets）—— 回答"该披露什么"；
> 4. **对抗性利用审计**（#12/#44 HackDetect）—— 回答"分数被利用了多少"；
> 5. **制度审计**（#43 Who Grades the Grader?）—— 回答"谁监督监督者"。
>
> **697/698 的位置**：**第 6 条路线 —— 口径漂移的代数化**：
> 不比较方法、不测 judge 偏差、不填模板、不找恶意利用，
> 而是问"**报告值有多少来自口径而非机制，以及这些漂移能否事后纠正**"。
> 在本次检索范围内，**"可纠错边界"（698 定理 T6）未见对应**。

---

## 5. 总括：哪些概念已被提出？哪些是真正的创新？

| 概念 | 是否已有对应 | 最接近的工作 | Queyi 的增量 |
|---|:--:|---|---|
| Goodhart 定律的分类 | ✅ 已有 | #1 Manheim-Garrabrant（4 变体） | **无**（我们是引用者） |
| Goodhart 的形式化 | ✅ 已有 | #2 Majka-El-Mhamdi、#3 Karwowski | **SG-3：去掉优化压力**（本次检索范围内未见） |
| 构念效度 / 不变性 | ✅ 已有 | #14 $S/R$ 二维剖面、#21 Meredith | 增量在**代数化 + 可纠错性**，不在"不变性"概念本身 |
| 测量漂移 | ⚠ 部分 | 统计过程控制的 concept drift（**未在本批检索范围内找到 CS 评估版本**） | **漂移算子族 + 7 公理 + 转移矩阵** |
| 不可判定性 | ✅ 已有 | #25 Landi、#26 Ramalingam、#28 Rice | **D/S/U 三分 + 34 类逐类归类 + L1/L2/L3** |
| "完美准则不存在" | ✅ 已有 | #27 Weyuker 1988 | 方法同构（公理排除法），**对象不同**（测试准则 vs 检测器） |
| 元评估 | ✅ 已有 | #35 On Meta-Evaluation | **对象不同**（方法比较 vs 口径漂移） |
| **可纠错边界** | ❌ **未见** | — | **698 定理 T6**（后处理层可纠正 / 获取层不可纠正 + 可计算残留误差） |
| **Chapman-Kolmogorov 条件** | ❌ **未见** | — | **698 定理 T5**（漂移链 CK 成立的充要条件） |
| **超可加性闭式残差** | ❌ **未见** | — | **697 定理 T1** |

### 5.1 三条必须写进论文的诚实结论

1. **不声称"首次提出 Goodhart 的变形"** —— #1 已有 4 变体分类，#2/#3 已形式化。
   我们的说法是"**去掉优化压力这一前提后，得到一个新的子类**"。
2. **不声称"首次形式化测量漂移"** —— #14 的 $S/R$ 剖面、#21 的测量不变性都是近邻。
   我们的说法是"**把漂移做成代数对象并给出可纠错边界**"。
3. **不声称"首次系统分类不可检测的缺陷"** —— #25/#26/#27/#28 是理论支柱。
   我们的说法是"**在 34 类具体缺陷上给出 D/S/U 归类与 L1/L2/L3 操作化，并做预测效度检验（未通过）**"。

---

## 6. 诚实边界

1. **本批检索不是穷尽检索**。4 组关键词、约 8 次检索 + 4 次抓取。
   ⇒ 所有"未见对应"只能读作"**在本次检索范围内未发现**"，**不是**"不存在"。
2. **9 篇标 ⚠️待确认**（多为凭记忆的 arXiv id / 经典期刊文献）。
   **引用前必须自行核对**；本批**没有**把它们当作论据使用（只作背景）。
3. **#5/#7/#8/#16/#32/#37/#38** 只核验到**标题与摘要级别**，未读全文。
4. **"✅695"的 9 篇**沿用 695 的核验结论，本批**未重新抓取**；若 695 有误则本批继承其误。
5. **文献计量学意义上的空白**：本批**未做**系统检索（如 arXiv 全库查询 + PRISMA 流程），
   因此"概念空位"的强度是**中等**（多组关键词交叉未命中），不是**强**。
6. **经典文献（📕）无 URL**：Goodhart 1975、Strathern 1997、Muller 2018、Campbell-Fiske 1959、
   Messick 1995、Borsboom 2006、Meredith 1993、Rice 1953、Turing 1936、DeMillo 1979、Cousot 1977
   —— 这些**未联网核验**，出版信息凭领域常识给出。

---

*文件生成：2026-10-09 ｜ 批次 698 任务 E ｜ 共 46 篇（✅本批 14 / ✅695 9 / 📕经典 14 / ⚠️待确认 9）｜ `detect_calls` = 0*
