# 695 · 方向 3：LLM-as-Judge / LLM-as-Verifier 最新研究（≥12 篇）

- **批次**：695 ｜ **方向**：方向 3（LLM-as-Judge / LLM-as-Verifier）｜ **日期**：2026-10-08
- **检索工具**：通用网络搜索（WebSearch）+ 逐条打开 `arxiv.org/abs/<id>` 或官方会议/出版页核验（WebFetch）
- **核验等级定义**（本批**只使用前两级**，无一条为凭记忆）：
  - `核验-摘要`：**已打开** arXiv abs 页 / 官方页 / PDF，核对到标题、作者、年份、venue 与摘要原文。
  - `核验-检索`：仅在搜索结果摘要中见到，**未打开原页**。
  - `未核验`：凭记忆，**落地前必须确认**（本批无此级条目）。
- **真实性声明**：本批共 **22 篇**，**全部为 `核验-摘要`**（其中 1 篇为官方 PDF 全文首页抽取）。**未编造任何 arXiv 编号**；每条的 arXiv id 均可按 URL 复核。所有条目均为 2023–2026 年真实出版物，**2025–2026 占 16/22**。
- **与既有调研的关系**：684（子模/治理 18 篇）、685（四域 39 篇）、693-E6（2026 补漏 5 条）**均未系统覆盖 LLM judge**；本批是仓库内**首次**对 LLM-as-Judge/Verifier 方向的专门调研。

---

## 1. 文献条目

### A · Judge 偏差与校准（Bias & Calibration）

**A1. Large Language Models are not Fair Evaluators**
- 作者：Peiyi Wang, Lei Li, Liang Chen, Zefan Cai, Dawei Zhu, Binghuai Lin, Yunbo Cao, Qi Liu, Tianyu Liu, Zhifang Sui
- 年份/venue：2023（arXiv v2 2023-08）｜ arXiv:2305.17926 ｜ https://arxiv.org/abs/2305.17926
- 核心贡献：首次系统揭示 **position bias（顺序偏差）**——只改候选答案出现顺序即可把排名刷成"Vicuna-13B 胜过 ChatGPT"；提出 Multiple Evidence / Balanced Position / Human-in-the-Loop 三种校准。
- **与 Queyi 的关系**：Queyi 的"资产选择算子（operator ≡ greedy set-cover）"与本文的"顺序不改结论才可信"是同一可信度问题的两个面。可作为 Queyi **§Limitations 里"装置结论对呈现方式是否敏感"的经典引证**，也支撑发现 4（选择算子不改变结论=装置稳健）。

**A2. Self-Preference Bias in LLM-as-a-Judge**
- 作者：Koki Wataoka, Tsubasa Takahashi, Ryokan Ri
- 年份/venue：2024（v2 2025-06，NeurIPS 2024 Safe GenAI Workshop）｜ arXiv:2410.21819 ｜ https://arxiv.org/abs/2410.21819
- 核心贡献：提出量化 self-preference bias 的指标；发现 GPT-4 显著自偏好，且**本质是 perplexity 偏好**（偏好"更熟悉/更低困惑度"的输出）。
- **与 Queyi 的关系**：Queyi 审计的是**非生成式证据装置**，无"模型给自己打分"维度；但可类比——装置是否偏好"自己覆盖得好"的缺陷类型（发现 2 的结构化盲区）。作为"judge 偏差谱系"的对照条目。

**A3. LLM Evaluators Recognize and Favor Their Own Generations**
- 作者：Arjun Panickssery, Samuel R. Bowman, Shi Feng
- 年份/venue：2024（arXiv v1 2024-04）｜ arXiv:2404.13076 ｜ https://arxiv.org/abs/2404.13076
- 核心贡献：证明 self-recognition 能力与 self-preference 强度**线性相关**（微调实验），且抗混淆因子——自偏好有因果解释。
- **与 Queyi 的关系**：与 A2 互补，说明"自偏好不是巧合"。用于 Queyi 讨论"当评估者与被评估者同源时的系统性风险"，为治理框架提供机制性证据。

**A4. Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge (CALM)**
- 作者：Jiayi Ye, Yanbo Wang, Yue Huang, Dongping Chen, Qihui Zhang, Nuno Moniz, Tian Gao, Werner Geyer, Chao Huang, Pin-Yu Chen, Nitesh V. Chawla, Xiangliang Zhang
- 年份/venue：2024（v2 2024-10）｜ arXiv:2410.02736 ｜ https://arxiv.org/abs/2410.02736
- 核心贡献：识别 **12 类 judge 偏差**，提出自动化量化框架 **CALM**；发现先进模型仍有显著任务特定偏差。
- **与 Queyi 的关系**：提供**最全的 judge 偏差清单**，是 Queyi §failure-modes 汇总表的"外部偏差分类学"来源；可对照 Queyi 的"环境省略/盲区"是否属于其 12 类之一（结论：Queyi 的失败更多是**能力/装置**层面，非偏好层面）。

**A5. Overconfidence in LLM-as-a-Judge: Diagnosis and Confidence-Driven Solution**
- 作者：Zailong Tian, Zhuoheng Han, Yanzhe Chen, Haozhe Xu, Xi Yang, Richeng Xuan, Houfeng Wang, Lizi Liao
- 年份/venue：2025（v1 2025-08-08，v3 2025-08-18）｜ arXiv:2508.06225 ｜ https://arxiv.org/abs/2508.06225
- 核心贡献：系统诊断 **Overconfidence Phenomenon**（置信度显著高估正确率）；给出跨模型 **ECE/ACE 表**（GPT-4o ECE 39.25、Mistral-Nemo 74.22 等）；提出 **TH-Score**（面向高/低置信区间的校准指标）与 **LLM-as-a-Fuser** 集成。
- **与 Queyi 的关系**：⭐ 直接支撑 Queyi 的**"环境省略静默失效"（发现 3）**——装置把"没观测到"当作"确定没问题"，正是 overconfidence 的装置版本（WSL 60.07% → native 24.74%，Δunknown=0）。Queyi 的"unknown 第三态"是本文 overconfidence 在**非 LLM 证据装置**上的同构现象。

**A6. Calibrating LLM Judges: Linear Probes for Fast and Reliable Uncertainty Estimation**
- 作者：Bhaktipriya Radharapu, Eshika Saxena, Kenneth Li, Chenxi Whitehouse, Adina Williams, Nicola Cancedda
- 年份/venue：2025（2025-12-23）｜ arXiv:2512.22245 ｜ https://arxiv.org/abs/2512.22245
- 核心贡献：用 **Brier-score 损失训练的线性探针**从 judge 隐藏态读出校准不确定度；在 JudgeBench / RewardBench 上 OOD 泛化，校准优于 verbalized confidence 且省 ~10× 算力。
- **与 Queyi 的关系**：Queyi 的"能力边界"要求装置能**报出不确定**；本文提供"如何低成本获得校准置信"的工程路线，可作 Queyi 未来把 8 资产从"三态（pass/fail/unknown）"升级为"带置信度"的参照。

**A7. Calibration as a First-Class Criterion in LLM Evaluation**
- 作者：Mario Sanz-Guerrero, Katharina von der Wense
- 年份/venue：2026（2026-09-22，UncertaiNLP @ EMNLP 2026）｜ arXiv:2609.26489 ｜ https://arxiv.org/abs/2609.26489
- 核心贡献：立场论文——主张把**校准作为一等评估标准**；指出 instruction tuning/RLHF **损害校准**；点明 LLM-as-a-judge、合成数据、主动学习都**默认置信度有意义却从不验证**。
- **与 Queyi 的关系**：⭐ 为 Queyi 的元评估立场提供**纲领级背书**——"评估装置依赖未经检验的置信度"正是 Queyi 要审计的对象。可直接引为 Queyi §motivation 的近期同类呼吁。

**A8. Judging the Judges: A Systematic Evaluation of Bias Mitigation Strategies in LLM-as-a-Judge Pipelines**
- 作者：Sadman Kabir Soumik
- 年份/venue：2026（v1 2026-04-25，v2 2026-06-24；**TMLR 2026**）｜ arXiv:2604.23178 ｜ https://arxiv.org/abs/2604.23178
- 核心贡献：跨 5 judge × 3 benchmark × 4 偏差类型比较 **9 种去偏策略**；关键发现：**Style bias 是主导偏差**（0.10–0.76，远超 position bias ≤0.04 且罕被研究）；verbosity bias 在长度感知下**异质**（Pro/Flash/Llama 偏好长，Claude 偏好简，GPT-4o 中性）；mid-tier 模型+正确去偏可**以约 1/15 成本超越前沿 judge**。
- **与 Queyi 的关系**：⭐ Queyi 的"表观增益坍缩"（发现 1）与本文"去偏后排名大变"同构——**评估配置选择本身改变结论**。本文的"style/verbosity 偏差常被忽略"支持 Queyi 把**装置配置**（E1/E2 环境坐标）提升为一等审计对象。

**A9. Diagnosing LLM Judge Reliability: Conformal Prediction Sets and Transitivity Violations**
- 作者：Manan Gupta, Dhruv Kumar
- 年份/venue：2026（2026-04-16，under review；亦见 ICML 2026）｜ arXiv:2604.15302 ｜ https://arxiv.org/abs/2604.15302
- 核心贡献：在 SummEval 上用**共形预测集 + 传递性分析**做 per-instance 诊断：整体 3-cycle 率仅 0.8–4.1%，但 **33–67% 文档至少含一个有向 3-cycle**；预测集宽度是 per-instance 可靠度指标（rₛ=+0.576）。
- **与 Queyi 的关系**：⭐ "**低聚合误差掩盖 per-instance 不可靠**"与 Queyi 的"**表观增益坍缩**"是同一种统计假象；Queyi 的"聚合覆盖率 ≫ 逐样本一致"可直接对标本条。可引为 Queyi"必须报告 per-instance 而非仅聚合指标"的方法论依据。

**A10. LLMs Cannot Reliably Judge (Yet?): A Comprehensive Assessment on the Robustness of LLM-as-a-Judge（RobustJudge）**
- 作者：Songze Li, Chuokun Xu, Jiaying Wang, Xueluan Gong, Chen Chen, Jirui Zhang, Jun Wang, Kwok-Yan Lam, Shouling Ji
- 年份/venue：2025（v1 2025-06-11，v3 2026-08-06）｜ arXiv:2506.09443 ｜ https://arxiv.org/abs/2506.09443
- 核心贡献：RobustJudge 框架，覆盖 **15 攻击 × 8 防御 × 13 模型**；发现 judge 对 **prompt 模板与模型选择高度敏感**，无单一防御在鲁棒性/效用/成本上全面占优。
- **与 Queyi 的关系**：Queyi 的"**prompt/环境敏感性**"（发现 3）在此有 LLM 侧对应物；本文"无普适防御"支持 Queyi"**无单一资产可覆盖全部缺陷**"（发现 2 盲区）的结构性判断。

---

### B · Judge Benchmark

**B1. JudgeBench: A Benchmark for Evaluating LLM-based Judges**
- 作者：Sijun Tan, Siyuan Zhuang, Kyle Montgomery, William Y. Tang, Alejandro Cuadron, Chenguang Wang, Raluca Ada Popa, Ion Stoica
- 年份/venue：2024（v1 2024-10-16，v2 2025-04；**ICLR 2025**）｜ arXiv:2410.12784 ｜ https://arxiv.org/abs/2410.12784
- 核心贡献：把困难数据集转成"**偏好标签=客观正确性**"的 response pair，覆盖知识/推理/数学/编码；发现强模型（如 GPT-4o）**仅略高于随机**。
- **与 Queyi 的关系**：⭐ "客观正确性标签"与 Queyi 的"真实缺陷存在性"同构——都是**用客观 ground truth 而非人类偏好**评判评估器。Queyi 可对标 JudgeBench，主张自己把"客观性"从 QA 正确性推到**代码缺陷证据**。

**B2. RewardBench: Evaluating Reward Models for Language Modeling**
- 作者：Nathan Lambert, Valentina Pyatkin, Jacob Morrison, LJ Miranda, Bill Yuchen Lin, Khyathi Chandu, Nouha Dziri, Sachin Kumar, Tom Zick, Yejin Choi, Noah A. Smith, Hannaneh Hajishirzi
- 年份/venue：2024（v1 2024-03-20，v2 2024-06）｜ arXiv:2403.13787 ｜ https://arxiv.org/abs/2403.13787
- 核心贡献：prompt-chosen-rejected 三元组基准，含"**可验证的微妙理由**（如 bug、错误事实）"；发现 RM 在拒答、推理、指令遵循上的系统性缺陷。
- **与 Queyi 的关系**：RewardBench 用"可验证理由"构造 hard case，与 Queyi 的"**真实 CVE 重构样本**"思路一致（拒绝合成易例）。可引为"真实/可验证标签优于偏好标签"的先例。

**B3. CodeJudgeBench: Benchmarking LLM-as-a-Judge for Coding Tasks**
- 作者：Hongchao Jiang, Yiming Chen, Yushi Cao, Hung-yi Lee, Robby T. Tan
- 年份/venue：2025（v1 2025-07-14，v2 2025-08；**ACL 2026 long**）｜ arXiv:2507.10535 ｜ https://arxiv.org/abs/2507.10535
- 核心贡献：面向**代码生成/修复/单测**三类任务的 judge 基准，评测 26 个 judge；发现 thinking 模型显著更好（Qwen3-8B 可胜 70B 专用 judge）；但**所有模型对顺序/作者身份高度敏感**，随机性大。
- **与 Queyi 的关系**：⭐ 最接近 Queyi 的"**用 LLM 判代码**"场景；其"顺序一改准确率就变"正是 Queyi"配置改变结论"的代码域证据。Queyi 可对比：CodeJudgeBench 判的是**生成的代码质量**，Queyi 审计的是**检测装置的证据能力**——两者互补。

**B4. BabelJudge: Measuring LLM-as-a-Judge Reliability Across Languages and Agent Trajectories**
- 作者：Shreyas KC
- 年份/venue：2026（2026-06-21）｜ arXiv:2606.22329 ｜ https://arxiv.org/abs/2606.22329
- 核心贡献：无人工标签的可靠性审计框架（**gold-labelling by degradation**），同时测 **position bias / verbosity bias / order inconsistency / 跨语言退化**四类失败；扩展到 agent 轨迹（工具调用幻觉等）。
- **与 Queyi 的关系**：⭐ "**由构造得到 gold 标签**"（扰动已知正确参考）与 Queyi"自撰样本 + 已知缺陷"方法论同源。其"order consistency 崩到 0.480=判词近乎随机"是 Queyi 强调"必须报告稳定性而非仅准确率"的强证据。

**B5. JudgeSense: A Benchmark for Prompt Sensitivity in LLM-as-a-Judge Systems**
- 作者：Rohith Reddy Bellibatlu, Edward Raff, Wenbin Zhang
- 年份/venue：2026（v1 2026-04-26，v3 2026-09-18）｜ arXiv:2604.23478 ｜ https://arxiv.org/abs/2604.23478
- 核心贡献：880 条人工标注样本 × 两条**仅措辞不同**的指令 × 25 judge；每个分数都对**同一 prompt 的自一致**归一（不把解码噪声算到措辞头上）；发现**改写会降低一致性**，序数任务最不稳，参数规模不预测稳定性。
- **与 Queyi 的关系**：⭐ **prompt sensitivity 的标杆**。Queyi 的"环境坐标 E1/E2（WSL vs native）"是**执行环境**层面的敏感性，与本文**指令措辞**层面的敏感性**正交**；Queyi 可主张自己补齐了"环境敏感"这一维。

**B6. Judge's Verdict: A Comprehensive Analysis of LLM Judge Capability Through Human Agreement**
- 作者：Steve Han, Gilberto Titericz Junior, Tom Balough, Wenfei Zhou
- 年份/venue：2025（2025-10-10，under review @ ICLR 2026）｜ arXiv:2510.09738 ｜ https://arxiv.org/abs/2510.09738
- 核心贡献：54 个 LLM 对 RAG/Agent 回答打分与人类一致性；用 z-score 区分 **human-like（|z|<1）** 与 **super-consistent（z>1）** 两种判词模式；提出"judge 的图灵测试"。
- **与 Queyi 的关系**：⭐ **judge–人类一致性的边界**的直接证据：**过度一致（super-consistent）可能是"过度简化"而非更可靠**。这与 Queyi"合成 vs 真实构成抵消（发现 5，标准化后 −17.92pp）"呼应——**一致性高 ≠ 有效**。Queyi 的 AI 双标 κ=0.495 可在此框架下定位为"低于 human-like 阈值"。

---

### C · LLM 代码缺陷检测 / 静态分析

**C1. LLM-based Vulnerability Detection at Project Scale: An Empirical Study**
- 作者：Fengjie Li, Jiajun Jiang, Dongchi Chen, Yingfei Xiong
- 年份/venue：2026（v1 2026-01-27，v2 2026-09-25）｜ arXiv:2601.19239 ｜ https://arxiv.org/abs/2601.19239
- 核心贡献：**首次**在项目规模上把 5 个专用 LLM 检测器 + 2 个通用 agent + 4 个传统静态分析器，作用在 265 个已知 C/C++/Java 漏洞、24 个真实项目上；分类 5,896 个误报。三大发现：通用 agent 召回最高但难处理复杂代码；**LLM 与传统方法都受"API 建模不全"拖累**，而 LLM 工具**另有推理与 prompt 遵循失败**；LLM 方法成本极高（单项目 $1000+）。
- **与 Queyi 的关系**：⭐⭐ **failure topology 问题最接近的实证工作之一**。它明确指出 LLM 检测器**额外**存在传统工具没有的失败原因（reasoning/prompt-compliance），暗示二者失败集合**不完全重叠**；但**未做集合正交性的形式化检验**，也未区分"预算门控 vs 能力边界"。Queyi 可主张自己把这一观察**提升为可检验的拓扑命题**。

**C2. Reducing False Positives in Static Bug Detection with LLMs: An Empirical Study in Industry**
- 作者：Xueying Du, Jiayi Feng, Yi Zou, Wei Xu, Jie Ma, Wei Zhang, Sisi Liu, Xin Peng, Yiling Lou
- 年份/venue：2026（2026-01-26）｜ arXiv:2601.18844 ｜ https://arxiv.org/abs/2601.18844
- 核心贡献：腾讯工业环境 433 条告警（328 FP / 105 TP）；**LLM+静态分析混合可消除 94–98% 误报且高召回**；单告警成本低至 2.1–109.5 秒。
- **与 Queyi 的关系**：⭐ 与 Queyi 的"**八资产并集 ≫ 单资产**（94.21%/99.22%）"数值高度呼应——独立工作也报告了 ~94–98% 的混合增益。区别：本文优化的是**误报消除（precision）**，Queyi 审计的是**覆盖/盲区（recall + unknown）**与**资产选择算子**。可作为"LLM 提升静态分析"的正向对照锚点。

**C3. LLM vs. SAST: A Technical Analysis on Detecting Coding Bugs of GPT4-Advanced Data Analysis**
- 作者：Madjid G. Tehrani, Eldar Sultanow, William J. Buchanan, Mahkame Houmani, Christel H. Djaha Fodja
- 年份/venue：2025（v1 2025-06-18，v2 2026-07-14）｜ arXiv:2506.15212 ｜ https://arxiv.org/abs/2506.15212
- 核心贡献：GPT-4(ADA) 对 32 个精选安全场景检出 **30/32（93.75%）**，SAST OR 基线 **11/32（34.4%）**，McNemar 检验显著。
- **与 Queyi 的关系**：⭐ 直接的 **LLM vs 传统工具对比**。其"LLM 检出率远高于 SAST"与 Queyi 中"LLM 臂在给足预算时能抓"（预算门控）一致；但样本量小（32），且**未分析两者失败集合是否互补**。Queyi 用 1147 样本 + 正交性框架做更严格版本。

**C4. LLM-Driven SAST-Genius: A Hybrid Static Analysis Framework**
- 作者：Vaibhav Agrawal, Kiarash Ahi
- 年份/venue：2025（v1 2025-09-18，v3 2025-11-04；IEEE S&P 2025 report）｜ arXiv:2509.15433 ｜ https://arxiv.org/abs/2509.15433
- 核心贡献：SAST + 微调 LLM 混合；**误报从 225 降到 20（约 −91%）**；主张"LLM 补 SAST 的上下文盲、SAST 补 LLM 的幻觉"。
- **与 Queyi 的关系**：⭐ 明确表述"**两者缺陷互补**"（LLM 幻觉 ↔ SAST 缺上下文），是 Queyi"failure topology 正交"的**定性最接近**陈述；但仍是**工程集成**而非**失败集合的拓扑刻画**。

**C5. Friends or Foes? Combining Static Analysis Tools and LLMs for Vulnerability Detection**
- 作者：Rafael Ramires, Sarmad Bashir, Abbas Khan, Mehrdad Saadatmand, Ibéria Medeiros
- 年份/venue：2026（ITEQS @ **ICSTW 2026**，IEEE）｜ 官方 PDF：https://www.es.mdh.se/pdf_publications/7373.pdf ｜ IEEE: https://ieeexplore.ieee.org/abstract/document/11600417
- 核心贡献：2 个 SAST + 2 个 LLM × 7 个 SQLi 数据集；发现 **SAST 倾向漏报（false negative）、prompt-engineered LLM 倾向误报（false positive）**，二者组合把 F1 从 6% 提到 ≈100%，平均 **+17–60%**。
- **与 Queyi 的关系**：⭐⭐ **failure topology 问题最接近的实证工作**。它给出"SAST=漏报型 / LLM=误报型"的**互补失败画像**，正是 Queyi"正交失败拓扑"的**经验近邻**；但它是**二分类（报/不报）**、单漏洞类型（SQLi）、**未形式化"正交"**，也未涉及"预算门控 vs 能力边界"。（本条目已用官方 PDF 全文首页抽取核验。）

---

### D · LLM 验证器 / Test-Time Verification

**D1. Variation in Verification: Understanding Verification Dynamics in Large Language Models**
- 作者：Yefan Zhou, Austin Xu, Yilun Zhou, Janvijay Singh, Jiang Gui, Shafiq Joty
- 年份/venue：2025（v1 2025-09-22，v2 2026-04-14；**ICLR 2026**）｜ arXiv:2509.17995 ｜ https://arxiv.org/abs/2509.17995
- 核心贡献：生成式 verifier（CoT + 二元判词）在 12 benchmark × 14 模型上的验证动力学：**易题更易被可靠认证**；**弱生成器的错误更易被检出**；验证力与 verifier 自身解题力相关但随难度变化；**"verifier scaling alone cannot overcome fundamental verification challenges"**。
- **与 Queyi 的关系**：⭐⭐ Queyi 的"**能力边界**"（sanitizer 臂：再多预算也抓不到）在 LLM 侧的**直接对应物**——本文的"强 verifier 也提供不了验证增益"正是"能力有界"的 LLM 版本。**Queyi 的独特贡献在于把"预算门控"与"能力边界"这一对区分明确归因到两类装置**，本文只观察 verifier 侧的上限、未做该二元对比。

---

## 2. LLM judge 已知 failure modes 汇总表

| # | Failure mode | 证据来源论文（本批） | 在 Queyi 里对应什么 |
|---|---|---|---|
| 1 | **Position / order bias**（顺序改结论就变） | A1 (2305.17926)、B3 (CodeJudgeBench)、B4 (BabelJudge) | Queyi 无"呈现顺序"维度，但对应 **选择算子稳健性**（发现 4：operator≡greedy，换算子不改结论=不敏感）；对照说明 Queyi 装置在顺序维度上**更稳** |
| 2 | **Verbosity bias**（偏好长输出） | A4 (CALM)、A8 (Judging the Judges)、B4 (BabelJudge) | 类比 Queyi 的"**告警量≠覆盖力**"：sanitizer 输出长/噪声多≠抓到更多缺陷类型；支撑"资产数量线性叠加"证伪（发现 1） |
| 3 | **Self-preference bias**（偏好自己/熟悉输出） | A2 (2410.21819)、A3 (2404.13076) | Queyi 审计非生成装置，无同源对打；但类比"装置偏好自己覆盖良好的缺陷类型"→ 发现 2 的结构化盲区 |
| 4 | **Overconfidence / miscalibration（ECE）** | A5 (2508.06225)、A6 (2512.22245)、A7 (2609.26489)、A9 (2604.15302) | ⭐ **Queyi 的"unknown 第三态 + 环境省略静默失效"（发现 3）**：装置把"未观测"当"确定无误"（WSL 60.07%→native 24.74%，Δunknown=0） |
| 5 | **Prompt / instruction sensitivity** | B5 (JudgeSense)、A10 (RobustJudge)、B3 (CodeJudgeBench) | ⭐ **Queyi 的环境坐标 E1/E2**：同一装置换执行环境即换结论；与"指令措辞敏感"**正交**，Queyi 补的是"执行环境敏感" |
| 6 | **Order/transitivity inconsistency**（per-instance 不可靠） | A9 (2604.15302)、B4 (BabelJudge) | ⭐ **Queyi 的表观增益坍缩（发现 1）**：低聚合误差掩盖 per-instance 不一致（k=4 Δ=0） |
| 7 | **Adversarial robustness collapse**（模板/模型选择敏感、无普适防御） | A10 (RobustJudge) | Queyi 的 **Goodhart / 目标博弈风险**（治理框架动机）；支撑"无单一资产覆盖全部缺陷"（发现 2） |
| 8 | **Verifier scaling ceiling**（强 verifier 也无增益） | D1 (2509.17995) | ⭐⭐ **Queyi 的"能力边界"（sanitizer 臂）**：预算加满也抓不到 = capability-bounded |
| 9 | **Style bias**（格式/文风主导，罕被研究） | A8 (2604.23178) | 类比 Queyi"**装置配置选择本身改变结论**"：E1/E2、去偏策略的效应量 > 常规偏差 |
| 10 | **Budget-gated failure**（给足预算即可修） | （本批**无直接文献**；Queyi 自创区分） | ⭐⭐ **Queyi 的 LLM 臂**：失败是 budget-gated，与 #8 的 capability-bounded 构成**正交对**——这是本论文相对本批文献的**净新增** |

---

## 3. Queyi 的"failure topology 正交"在文献中的定位（回答硬性要求 3）

**结论：未检索到直接对应工作。**

- 截至 2026-10-08，本批 22 篇 + 定向补搜中，**没有任何论文**把"**LLM judge / LLM verifier 与传统（非 LLM）检测器的失败集合**"做成**正交性 / 互补性的形式化检验**，也**没有**工作提出或检验"**预算门控（budget-gated）vs 能力边界（capability-bounded）**"这一对失败类型区分。
- 更精确地说，Queyi 的命题有三个要素，文献**最多各自命中一个**、**无一篇同时命中**：
  1. **同一对象**（软件验证的证据获取装置）；
  2. **两类装置对比**（LLM 臂 vs sanitizer/编译器/链接器臂）；
  3. **失败集合的拓扑刻画**（正交/互补）+ **失败类型的二元归因**（预算门控 vs 能力边界）。
- 因此，Queyi 的发现 7 应表述为**"据我们所知，首次"（to our knowledge, first）**，并在 Related Work 明确写"**最接近的是若干'互补性'实证工作，但均未做拓扑刻画或失败类型二分**"。

### 最接近的 3 篇（按接近度排序）

1. **C5 · Friends or Foes?（ICSTW 2026）** —— **最近邻**。给出"**SAST=漏报型失败 / LLM=误报型失败**"的互补画像，组合后 F1 +17–60%（6%→≈100%）。**差距**：二分类、单一漏洞类型（SQLi）、未形式化"正交"、无预算/能力二分。
2. **C1 · LLM-based Vulnerability Detection at Project Scale（arXiv:2601.19239, 2026）** —— 唯一在**项目规模**上把 LLM 检测器与传统静态分析器并列评测并**分类误报成因**的工作，明确指出 **LLM 工具有传统工具没有的额外失败原因**（reasoning / prompt-compliance failures）。**差距**：停在"失败成因不同"，未检验失败集合是否正交，也未涉及预算维度。
3. **C3 · LLM vs. SAST（arXiv:2506.15212, 2025）** —— 直接的 LLM vs SAST 对比（GPT-4 93.75% vs SAST 34.4%）。**差距**：样本仅 32、未分析失败集合关系、无互补性/正交性结论。

**补充锚点（非 LLM-vs-传统，但为"工具家族失败不重叠"提供旁证）**：
- **684/693-E6 已收录的 N2（Hassler et al., arXiv:2505.22052）** 报告"**全部 fuzzer 的并集与全部静态分析器的并集几乎不相交**"——这是"**两个工具家族失败集合正交**"的最强外部证据，但对象是 **fuzzer vs 静态分析**，**不含 LLM**。Queyi 可引其作为"家族间失败正交并非孤例"，同时强调自己是**首次把 LLM 臂纳入该对比并给出二元归因**。
- **D1（2509.17995）** 提供"能力边界"的 LLM 侧机制证据（verifier scaling 有上限），是 Queyi 归因"capability-bounded"的理论近邻。

---

## 4. 对 Queyi 的启示

### 4.1 可直接引用（引文与定位）
- **§motivation / 元评估立场**：A7（2609.26489，把校准列为一等标准）、A9（2604.15302，低聚合误差掩盖 per-instance 不可靠）、A5（2508.06225，overconfidence 诊断）。→ 支撑"评估装置本身须被审计"。
- **§failure modes**：A4（CALM 12 类偏差）作为**外部偏差分类学**，A8（style/verbosity 主导且被忽视）作为**配置敏感性**证据。
- **§related（代码域）**：B3（CodeJudgeBench）、B4（BabelJudge）、B5（JudgeSense）作为"LLM 判代码/判词的基准与偏差"；C1、C2、C3、C5 作为"LLM vs 传统静态分析"对照。
- **§Limitations / 诚实边界**：B6（Judge's Verdict）"过度一致≠更可靠"→ 为 Queyi 的 κ=0.495 与"AI 双标"提供解释框架。

### 4.2 可对比（把 Queyi 与文献区分开）
- **vs CodeJudgeBench / BabelJudge**：它们判的是"**生成的代码质量**"或"**判词稳定性**"；Queyi 审计的是"**检测装置的证据能力**"（能否发现缺陷、盲区在哪）。→ Queyi 是**装置审计**而非**输出评判**。
- **vs C5 / C1 / C3（互补性）**：它们观察"两家族互补"，Queyi **形式化**为 failure topology 并**归因**为 budget-gated vs capability-bounded。→ 这是净新增。
- **vs A9 / A5（校准）**：它们做 **LLM judge** 的 ECE；Queyi 把"overconfidence/unknown 静默"移到**非 LLM 证据装置**（sanitizer 在 WSL 下的静默失效）。→ 同构现象的跨装置迁移。

### 4.3 可升级（方法论）
1. **把三态升级为带置信度**：借鉴 A6（线性探针）与 A5（TH-Score），让 8 资产输出"pass / fail / **unknown(置信度)**"，把"环境省略静默失效"从定性升级为可校准量。
2. **per-instance 报告**：采纳 A9 / B4 的 per-instance 诊断（传递性、预测集宽度、自一致），补强 Queyi 对"表观增益坍缩"的呈现。
3. **正交性的形式化**：把发现 7 写成可检验命题（例如定义两臂失败集合的 Jaccard/条件熵、并给出"预算轴"上的 Δ 曲线），用 C5/C1 的互补观察做**外部锚点**。
4. **配置敏感性清单**：对标 A8/A10/B5，把 E1/E2、prompt、去偏策略统一为"装置配置坐标"，报告"配置×结论"敏感性矩阵。

---

## 5. 检索记录（可复核表）

| # | 检索词 | 日期 | 命中并采用的条目 |
|---|---|---|---|
| S1 | `LLM-as-a-judge bias position bias verbosity self-preference 2025 2026 arxiv` | 2026-10-08 | A8 (2604.23178)、A5 (2508.06225) |
| S2 | `judge calibration ECE LLM evaluator reliability 2026 arxiv` | 2026-10-08 | A7 (2609.26489)、A6 (2512.22245) |
| S3 | `JudgeBench RewardBench CodeJudgeBench LLM judge benchmark 2025 arxiv` | 2026-10-08 | B1 (2410.12784)、B3 (2507.10535) |
| S4 | `LLM static analysis limitations bug detection benchmark 2025 2026 arxiv` | 2026-10-08 | C2 (2601.18844) |
| S5 | `LLM verifier scaling test-time compute hallucination 2025 2026 arxiv` | 2026-10-08 | D1 (2509.17995，经 S12 复核) |
| S6 | `CodeJudgeBench evaluating LLM code judging benchmark 2025 arxiv` | 2026-10-08 | B3 (2507.10535) |
| S7 | `self-preference bias LLM judge own outputs 2024 2025 arxiv Panickssery` | 2026-10-08 | A2 (2410.21819)、A3 (2404.13076) |
| S8 | `BabelJudge JudgeSense LLM judge benchmark 2025 2026 arxiv` | 2026-10-08 | B4 (2606.22329) |
| S9 | `RewardBench evaluating reward models benchmark arxiv 2403` | 2026-10-08 | B2 (2403.13787) |
| S10 | `prompt sensitivity LLM judge evaluation robustness arxiv 2025` | 2026-10-08 | A10 (2506.09443)、B5 (2604.23478) |
| S11 | `LLM judge vs traditional tool complementarity bug detection agreement 2026` | 2026-10-08 | （无直接命中；引出 S13/S14） |
| S12 | `LLM verifier cannot self-verify generator scaling laws verification limits arxiv 2025` | 2026-10-08 | D1 (2509.17995) |
| S13 | `LLM vulnerability detection false negatives limitations empirical study C C++ 2025 arxiv` | 2026-10-08 | C1 (2601.19239) |
| S14 | `complementary strengths LLM static analysis tool ensemble hybrid detection 2026 arxiv` | 2026-10-08 | C4 (2509.15433)、C5 (Friends or Foes) |
| S15 | `LLM judge human agreement ceiling reliability reproducibility limits arxiv 2025 2026` | 2026-10-08 | B6 (2510.09738) |
| S16 | `Large Language Models are not Fair Evaluators position bias arxiv 2305.17926` | 2026-10-08 | A1 (2305.17926) |
| S17 | `Justice or Prejudice Quantifying Biases LLM-as-a-Judge arxiv 2410.02736` | 2026-10-08 | A4 (2410.02736) |
| S18 | `"Friends or Foes" combining static analysis tools LLMs vulnerability ICSTW 2026` | 2026-10-08 | C5（官方 PDF + IEEE + 会议页） |
| S19 | `Diagnosing LLM Judge Reliability Conformal Prediction Sets Transitivity Violations arxiv` | 2026-10-08 | A9 (2604.15302) |
| S20 | `do LLM detectors find different bugs than static analyzers overlap complementary evaluation 2026 arxiv` | 2026-10-08 | C3 (2506.15212)、C1 (2601.19239) |
| S21 | `LLM judge failure modes orthogonal to traditional detector complementary error sets 2026` | 2026-10-08 | **无直接命中**（用于确认硬性要求 3 的"未检索到"结论） |

**核验动作记录**（打开 abs 页逐条核对标题/作者/年份，`核验-摘要`）：
2508.06225、2410.12784、2601.18844、2604.23178、2512.22245、2609.26489、2507.10535、2410.21819、2404.13076、2606.22329、2506.09443、2604.23478、2403.13787、2601.19239、2510.09738、2509.15433、2305.17926、2410.02736、2509.17995、2604.15302、2506.15212 —— 共 **21 条**；另有 **C5（Friends or Foes）经官方 PDF 首页全文抽取核验**（第 22 条）。

> **检索口径诚实说明**：检索工具为通用网络搜索（WebSearch）+ 定向页面核验（WebFetch），**非**学术数据库系统检索（无 Scopus / DBLP / ACM DL 全文检索）。因此本表**不能**声称是系统综述，属"投稿前补漏 + 定向核验"性质。**本批无一条为凭记忆的 `未核验` 条目。**

---

## 6. 与 684 / 685 / 693 已有调研的关系（新增了什么）

| 批次 | 覆盖 | 是否含 LLM judge | 695 的新增 |
|---|---|---|---|
| **684** | 子模优化 / 主动测试 / 治理-Goodhart（18 篇） | ❌ 无 | 695 把"评估者自欺"从治理叙事**落到 LLM judge 的具体偏差与校准文献** |
| **685** | 四域 39 篇（子模 12 / eval 12 / active 9 / info 6） | ❌ 无（eval 域止于 HELM、Leaderboard Illusion 等元评估） | 695 **首次**引入 judge 偏差（position/verbosity/self-preference）、校准（ECE/TH-Score/共形）、judge benchmark（JudgeBench/RewardBench/CodeJudgeBench/BabelJudge/JudgeSense） |
| **693-E6** | 2026 补漏 5 条；其中 **N2**（fuzzer vs 静态分析"几乎不相交"）、**N5**（LLM-Judge Validation，二手转述） | ⚠️ 仅触及（N5 为最低证据级转述） | 695 把 N5 升级为**一批一手核验文献**，并把 N2 的"家族互补"扩展为 **LLM 臂 vs 传统臂**的 failure topology 问题 |

**695 相对既有材料的净新增**：
1. **22 篇一手核验文献**（684/685/693 均无 LLM judge 专项）。
2. **failure modes 汇总表**（10 行），把 Queyi 七发现逐一映射到外部证据。
3. **对硬性要求 3 的明确结论**：**未检索到直接对应工作**；给出最接近的 3 篇（C5 / C1 / C3）与旁证（N2、D1）。
4. **"budget-gated vs capability-bounded"二元区分**被确认为**本批文献空白**，即 Queyi 发现 7 的**净新增性得到外部确认**。
5. **可升级清单**（置信度三态、per-instance 报告、正交性形式化、配置敏感性矩阵）。

---

*文件生成：2026-10-08 ｜ 批次 695 ｜ 共 22 篇，核验等级：核验-摘要 22 / 核验-检索 0 / 未核验 0 ｜ 未修改仓库其他文件。*
