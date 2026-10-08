# 695 · 方向 4：可复现性与审计框架（≥12 篇）

- **批次**：695 ｜ **方向**：4（可复现性与审计框架）｜ **日期**：2026-10-08
- **用途**：支撑 Queyi（评估器审计协议，投稿 NeurIPS 2027 Evaluations & Datasets）的 Related Work 与差异化定位。
- **检索工具**：WebSearch（通用网络搜索）+ WebFetch（打开 arXiv abs 页 / 官方页核验）。
- **真实性声明（重要）**：本批所有条目均**联网核验**，未凭记忆编造。核验等级定义如下：
  - **`核验-摘要`**：已用 WebFetch 打开 `arxiv.org/abs/<id>` 或官方页，逐字核对**标题 / 作者 / 年份 / venue / arXiv 号 / 摘要**。
  - **`核验-检索`**：通过 WebSearch 命中官方页或权威索引（DOI / IEEE / NIST / ACM），确认条目**存在且元数据一致**，但**未成功抓取正文**（页面为 JS 渲染或付费墙）。
  - **`未核验`**：凭记忆列出、**未联网确认**——本批为 **0 条**；若后续新增，落地前必须二次确认。
- **不重复声明**：论文已引的 Datasheets (Gebru 2021)、Model Cards (Mitchell 2019)、Pineau 2021、Merkle 1988、
  kao2025constantsize、wang2026whoaudits、Atlas (spoczynski2025atlas)、PaperTrail (martinboyle2026papertrail)、
  Reproducibility Beyond Artifacts (li2026reprobeyond)、NeurIPS Dataset Review (wu2024neurips)、Raji 2021
  **不再作为"新增"列入**（仅在对比表中作对照出现）。

---

## 1. 文献条目（分组：可复现性 / 审计框架 / 溯源与防篡改）

> 共 **20 条新增**（可复现性 9 / 审计框架 8 / 溯源与防篡改 3）。
> 核验分布：`核验-摘要` **16** 条、`核验-检索` **4** 条、`未核验` **0** 条。

### A. 可复现性（Reproducibility）— 9 条

**A1. Croissant: A Metadata Format for ML-Ready Datasets** — `核验-摘要`
- 作者：Mubashara Akhtar, Omar Benjelloun, Costanza Conforti, … , Carole-Jean Wu, Luyao Zhang（共 30+ 位，Google/Meta/OpenML 等）
- 年份/venue：2024 ｜ NeurIPS 2024 **Datasets and Benchmarks Track**（早期短版见 ACM DEEM'24）
- URL：https://arxiv.org/abs/2403.19546 ｜ DOI:10.48550/arXiv.2403.19546
- 核心贡献：提出 **Croissant**——跨 ML 工具/框架/平台的**数据集元数据格式**，让数据集可发现、可移植、可互操作；已被多个主流数据集仓库（数十万数据集）支持；人评显示元数据可读、完整且简洁。
- 与 Queyi 的关系：**格式层对照**。Croissant 是"数据集**描述**的机器可读标准"，Queyi 的 `croissant.json` 是**采纳**它的实例；但 Croissant **不携带判定状态、不保证可复算、不防篡改**——它回答"数据长什么样"，Queyi 回答"结论是否幸存"。可引作"Queyi 的元数据层与社区标准对齐"的证据。

**A2. Data Cards: Purposeful and Transparent Dataset Documentation for Responsible AI** — `核验-摘要`
- 作者：Mahima Pushkarna, Andrew Zaldivar, Oddur Kjartansson（Google Research）
- 年份/venue：2022 ｜ ACM FAccT 2022 ｜ DOI:10.1145/3531146.3533231
- URL：https://arxiv.org/abs/2204.01075
- 核心贡献：提出 **Data Cards**——面向"负责任 AI"的**结构化数据集文档**（来源、采集/标注方法、意图、伦理、演化），并给出落地框架与 20+ 张已部署卡片的经验。
- 与 Queyi 的关系：**模板层对照**。Data Cards 是 Model Cards 在数据集上的延伸，仍是**静态文档**；Queyi 的 `DATASHEET.md` 与其同精神，但 Queyi 额外把"每个数字一行命令复算 + 四态判定"编进证据链。可引作"文档化实践的当前天花板 = 静态报告"。

**A3. Reproducibility of Machine Learning: Terminology, Recommendations and Open Issues** — `核验-摘要`
- 作者：Riccardo Albertoni, Sara Colantonio, Piotr Skrzypczyński, Jerzy Stefanowski
- 年份/venue：2023 ｜ arXiv 预印本（survey）
- URL：https://arxiv.org/abs/2302.12691
- 核心贡献：系统综述 ML 可复现性的**术语**（repeatability/reproducibility/replicability 的边界）、梳理现有建议，并指出被忽视的关键要素；特别针对生物医学与物理 AI 两域给出补充建议。
- 与 Queyi 的关系：**术语纪律来源**。Queyi 的"四态判定（survives/weakened/collapses/unresolved）"要精确，必须先厘清"复现 vs 复制"；本文是可引的术语权威之一（与 A5、A7 共同构成术语三角）。

**A4. Reproducibility in Machine Learning-based Research: Overview, Barriers and Drivers** — `核验-摘要`
- 作者：Harald Semmelrock, Tony Ross-Hellauer, Simone Kopeinik, Dieter Theiler, Armin Haberl, Stefan Thalmann, Dominik Kowald
- 年份/venue：2024（v1 2024-06，v3 2025-02）｜ **AI Magazine**（accepted）
- URL：https://arxiv.org/abs/2406.14325
- 核心贡献：把 ML 可复现性障碍分为**方法/代码/数据/实验**四层，构建 **Drivers–Barriers Matrix**，给出研究者可操作的缓解策略；论点：社区对该问题"过于轻视"。
- 与 Queyi 的关系：**危机量化框架**。其"很多论文原则上都不可复现"的判断，正是 Queyi "检测器不可用 ≠ 检测器说没问题"（unresolved 态）的宏观动机；可用于 Related Work 论证"为什么需要四态而非二元"。

**A5. What is Reproducibility in Artificial Intelligence and Machine Learning Research?** — `核验-摘要`
- 作者：Abhyuday Desai, Mohamed Abdelhamid, Nakul R. Padalkar
- 年份/venue：2024（v2 2025-03）｜ submitted to AI Magazine
- URL：https://arxiv.org/abs/2407.10239
- 核心贡献：给出**验证研究分类框架**：repeatability、dependent/independent reproducibility、direct/conceptual replicability，澄清各概念角色，指导验证研究的设计与解释。
- 与 Queyi 的关系：**判定代数的术语基座**。Queyi 的"四态"可映射到其分类（survives≈independent reproducibility；weakened≈partial；collapses≈fail；unresolved≈不可判定），引用它能把 Queyi 的四态锚定到既有术语体系。

**A6. Can citations tell us about a paper's reproducibility? A case study of machine learning papers** — `核验-摘要`
- 作者：Rochana R. Obadage, Sarah M. Rajtmajer, Jian Wu
- 年份/venue：2024 ｜ ACM/IEEE JCDL 2024（Related DOI:10.1145/3641525.3663628）
- URL：https://arxiv.org/abs/2405.03977
- 核心贡献：以 **ML Reproducibility Challenge** 参与论文为样本，构建"引用语境情感 → 复现结果"分析框架，训练分类器并检验引用情感与复现评分的相关性；发布数据与工件。
- 与 Queyi 的关系：**"可复现性可测量"的直接先例**。它用**外部信号（引用）**度量复现，Queyi 用**内部账本 + 一行命令复算**度量；可对比"间接信号 vs 直接证据链"两条路线。

**A7. Reproducibility, Replicability, and Repeatability: A survey of reproducible research with a focus on high performance computing** — `核验-摘要`
- 作者：Benjamin A. Antunes, David R.C. Hill
- 年份/venue：2024 ｜ **Computer Science Review** 53:100655 ｜ DOI:10.1016/j.cosrev.2024.100655
- URL：https://arxiv.org/abs/2402.07530
- 核心贡献：综述可复现性危机成因，聚焦"计算常沦为黑箱"；系统梳理 HPC 场景下的挑战与解法。
- 与 Queyi 的关系：**"环境/执行栈不可复现"的权威综述**。Queyi 的 Finding 3（环境省略静默失效：WSL 60.07% → native 24.74%，Δunknown=0）是其"计算黑箱"论断的一个**可执行、可量化**的实例。

**A8. Preregistration for Experiments with AI Agents** — `核验-摘要`
- 作者：Michelle Vaccaro
- 年份/venue：2026 ｜ **ICML 2026 Spotlight（Top 5%）Position Paper**
- URL：https://arxiv.org/abs/2606.11217
- 核心贡献：主张把社会科学的**预注册（preregistration）**扩展到"以 LLM/AI agent 为被试"的实验；系统列举研究者自由度（模型选择、提示措辞、设置、结果依赖式重设计），指出低成本迭代 + 缺乏报告规范使这些选择"易被利用、难以察觉"；给出预注册模板。
- 与 Queyi 的关系：**"预注册 ML"的最新权威**。Queyi 的 A5 `uninterpretable` 降级条款本质是**内部预注册**（686 C3 已指出其不可外部核验）；本文为"把预注册公开化、让降级标准可被外部核验"提供了 2026 年的直接文献支撑。

**A9. Artifact Review and Badging（ACM 政策，V1.1）** — `核验-检索`
- 作者/机构：ACM（Reproducibility Task Force）
- 年份/venue：2020（V1.1，2020-08-24）｜ ACM 官方政策
- URL：https://www.acm.org/publications/policies/artifact-review-and-badging-current
- 核心贡献：定义 artifact evaluation 的**徽章体系**：Artifacts Available（可用）、Artifacts Evaluated（Functional / Reusable）、Results Reproduced / Results Replicated，是 ACM 各会议复现赛道（如 SIGMOD、PADS）的评分基准。
- 与 Queyi 的关系：**"badging = 静态评级"的机制对照**。徽章是**一次性、人工、二元/离散等级**的判定；Queyi 的四态是**可复算、带账本、可演化**的判定。可引作"artifact evaluation 机制的天花板"。
- 说明：该页 WebFetch 两次返回空（JS 渲染），故标 `核验-检索`（官方 URL + 政策版本由检索结果确认，**徽章措辞未逐字抓取**，引用前建议人工复核页面正文）。

### B. 审计框架（Audit Frameworks）— 8 条

**B1. Who Audits the Auditors? Recommendations from a field scan of the algorithmic auditing ecosystem** — `核验-摘要` ｜ ⭐**audit-the-auditor**
- 作者：Sasha Costanza-Chock, Emma Harvey, Inioluwa Deborah Raji, Martha Czernuszenko, Joy Buolamwini
- 年份/venue：2022 ｜ ACM FAccT 2022 ｜ DOI:10.1145/3531146.3533213
- URL：https://arxiv.org/abs/2310.02521
- 核心贡献：**首个 AI 审计生态系统的实地扫描**（N=438 个人 / N=189 机构目录，N=152 问卷，N=10 深访）；指出"AI 审计"定义模糊、标准缺失，导致"已审计"声明难以核验，可能**加剧而非缓解**伤害；提出 6 条政策建议（含**强制披露审计发现的关键组件以供同行评审**、**对审计者本身做评估/认证**）。
- 与 Queyi 的关系：**"审计者本身也要被审计"的奠基文献**。其第 6 条建议"formalize evaluation and, potentially, accreditation of algorithmic auditors"正是 Queyi 递归问题（谁审计审计者）的制度化表述；Queyi 的 452 事件账本 + 四态，是把"审计结论可核验"从**政策呼吁**落到**技术装置**的一次尝试。

**B2. A Framework for Assurance Audits of Algorithmic Systems** — `核验-摘要`
- 作者：Khoa Lam, Benjamin Lange, Borhane Blili-Hamelin, Jovana Davidovic, Shea Brown, Ali Hasan
- 年份/venue：2024 ｜ **ACM FAccT 2024** ｜ DOI:10.1145/3630106.3658957
- URL：https://arxiv.org/abs/2401.14908
- 核心贡献：提出 **criterion audit**——面向合规与保证的**外部审计框架**，借鉴**财务审计**范式，给出必要条件与实操蓝图；以 NYC Local Law 144（招聘算法偏见审计）为例说明适配；讨论"把成熟财务审计实践移植到 AI 审计"的收益、固有局限与实施挑战。
- 与 Queyi 的关系：**"审计标准/程序"的制度层对照**。它回答"一次合规审计应当如何组织"，Queyi 回答"审计**结论**在口径/环境/资产变化下是否幸存"；二者互补——B2 管流程，Queyi 管结论的可复算与防篡改。

**B3. Outsider Oversight: Designing a Third Party Audit Ecosystem for AI Governance** — `核验-摘要`
- 作者：Inioluwa Deborah Raji, Peggy Xu, Colleen Honigsberg, Daniel E. Ho
- 年份/venue：2022 ｜ ACM/AAAI **AIES 2022** ｜ DOI:10.1145/3514094.3534181
- URL：https://arxiv.org/abs/2206.04737
- 核心贡献：综合金融/环境/健康等**非算法领域**的外部监督制度经验，论证"仅靠审计本身不足以实现算法问责，**制度设计**才是关键"；对第三方审计的组件给出证据综述与启示。
- 与 Queyi 的关系：**"独立复算"的制度论证**。Queyi 的"每个数字一行命令复算"是技术层的独立复核；B3 提供"为什么必须把锚放到系统外部"的制度理由（与 686 C3 的递归分析直接呼应）。注意：Raji 2021（Elephant in the Room，论文已引）与本条是**不同论文**。

**B4. Benchmarks Are Not Monolithic: Sample-Level Auditing and Orchestration for LLM Evaluation** — `核验-摘要` ｜ ⭐**meta-evaluation**
- 作者：Philipp D. Siedler, Jordan Sassoon
- 年份/venue：2026 ｜ arXiv 预印本
- URL：https://arxiv.org/abs/2607.28801
- 核心贡献：提出**数据集中心的元评估框架**，在**样本级**沿五个潜在维度（认知/知识需求、语言/内容质量、任务属性、上下文、伦理安全公平）审计基准；对 MMLU/ARC/WinoGrande/HellaSwag/TruthfulQA 标注，揭示"聚合准确率掩盖的内部异质性"，并支持按准则**重组**基准子集。
- 与 Queyi 的关系：**"审计基准本身"的最近邻之一**。它把"基准不是铁板一块"做成样本级元评估，与 Queyi 的"能力边界图（38.4% 结构化盲区）"同属"拆开聚合分数看内部结构"；差异：它审的是**LLM 基准的样本属性**，Queyi 审的是**软件验证证据获取装置的测量口径**，且 Queyi 带四态与防篡改账本。

**B5. Who Evaluates the Evaluators? A Study on Reflexive Meta-Evaluation Methods for Large Language Models** — `核验-检索` ｜ ⭐**audit-the-auditor**
- 作者：Shuhan Lv, Yong Li, Yuang Chen, Fang Lin, Guantong Cheng
- 年份/venue：2026 ｜ IEEE ICSIPC 2026（Nanchang, China, 2026-04-24~26）｜ DOI:10.1109/ICSIPC69751.2026.11583935
- URL：https://ieeexplore.ieee.org/abstract/document/11583935
- 核心贡献：构建**反身式元评估框架**（reflexive meta-evaluation），通过 Meta-Prompt Optimization、Self-Critique for Evaluation Design、**Uncertainty-Aware Rejection** 三方面提升 LLM 评估的可信度与公平性；用 Spearman 秩相关度量评估者与人类判断的一致性。
- 与 Queyi 的关系：**递归问题的第二个独立证据**。其"元评估即对评估系统的评估/反思/优化"与 Queyi "评估器审计协议"同题；尤其 **Uncertainty-Aware Rejection** 与 Queyi 的 **unresolved 态**同构——两者都主张"不确定时应拒绝给出结论"而非强行二判。
- 说明：正文经 WebFetch 抓到摘要与元数据（作者/会议/DOI 已核对），但完整正文需登录；标 `核验-检索`。

**B6. LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods** — `核验-摘要`
- 作者：Haitao Li, Qian Dong, Junjie Chen, Huixue Su, Yujia Zhou, Qingyao Ai, Ziyi Ye, Yiqun Liu
- 年份/venue：2024 ｜ arXiv 综述（60 页，持续更新）
- URL：https://arxiv.org/abs/2412.05579
- 核心贡献：从**功能/方法/应用/元评估/局限**五视角系统综述 LLM-as-Judge 范式，含"如何评估 LLM 裁判"（meta-evaluation）一章。
- 与 Queyi 的关系：**"评估者也是被评估对象"的综述锚点**。它为"评估器须被审计"提供全景；Queyi 的 693-A（AI 双标 κ=0.495 + 人类裁决材料包）可归入其 meta-evaluation 章节的一个实例。

**B7. Claim Verification in the Age of Large Language Models: A Survey** — `核验-摘要`
- 作者：Alphaeus Dmonte, Roland Oruche, Marcos Zampieri, Prasad Calyam, Isabelle Augenstein
- 年份/venue：2024（v2 2025-02）｜ arXiv 综述
- URL：https://arxiv.org/abs/2408.14317
- 核心贡献：系统综述 **LLM 时代的 claim verification 框架**，拆解检索/提示/微调组件与公开数据集。
- 与 Queyi 的关系：**"科学声明自动核验"的综述入口**。Queyi 的 claim–evidence 接口（每个 claim 声明 caliber Q=(D,A,E,Θ,P)、每个数字一行命令复算）是"**面向科研产物的 claim verification**"的一个受限但可执行的实例；本文可作为该方向的通用背景。

**B8. Artificial Intelligence Risk Management Framework (AI RMF 1.0)** — `核验-检索`
- 作者：Elham Tabassi（NIST）
- 年份/venue：2023 ｜ NIST AI 100-1 ｜ DOI:10.6028/NIST.AI.100-1
- URL：https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10
- 核心贡献：由《2020 国家 AI 倡议法案》授权，提供 AI 风险管理的**自愿性、跨行业、用例无关**框架（治理/映射/度量/管理四功能），是"AI 审计标准"的制度底座之一（与 ISO/IEC 42001 并列）。
- 与 Queyi 的关系：**"标准 ≠ 判定代数"的对照**。NIST AI RMF 给的是**组织流程与风险分类**，不含"结论是否幸存"的可复算判定；可引作"现行标准重流程、轻可复算证据链"的代表，衬托 Queyi 的差异化。

### C. 溯源与防篡改（Provenance & Tamper-evidence）— 3 条

**C1. Recording provenance of workflow runs with RO-Crate** — `核验-摘要`
- 作者：Simone Leo, Michael R. Crusoe, Laura Rodríguez-Navas, … , Stian Soiland-Reyes（共 18 位）
- 年份/venue：2024 ｜ **PLOS ONE** 19(9):1-35 ｜ DOI:10.1371/journal.pone.0309210
- URL：https://arxiv.org/abs/2312.07852
- 核心贡献：提出 **Workflow Run RO-Crate**——RO-Crate / Schema.org 的扩展，以不同粒度记录**计算工作流执行溯源**，打包输入/输出/代码等对象；**对齐 W3C PROV**；已在 6 个工作流系统实现；给出两个数字图像分析 ML 用例。
- 与 Queyi 的关系：**"内容寻址研究对象"的社区标准**。RO-Crate 是**打包与溯源表达**标准，Queyi 的"内容寻址证据 + 部分历史可复现"可与之对齐；差异：RO-Crate **不定义判定状态、不提供防篡改承诺**，Queyi 在此之上加了四态与 Merkle 锚。

**C2. Merkle Trees in Blockchain: A Study of Collision Probability and Security Implications** — `核验-摘要`
- 作者：Oleksandr Kuznetsov, Alex Rusnak, Anton Yezhov, Kateryna Kuznetsova, Dzianis Kanonik, Oleksandr Domin
- 年份/venue：2024 ｜ **Internet of Things** 26:101193 ｜ DOI:10.1016/j.iot.2024.101193
- URL：https://arxiv.org/abs/2402.04367
- 核心贡献：理论 + 实证研究 Merkle 树的**根碰撞概率**：路径越长根碰撞概率越高，哈希越长碰撞概率显著下降；为区块链数据完整性设计给出量化指引。
- 与 Queyi 的关系：**Merkle 锚定的安全性量化依据**。Queyi 用 Merkle 根锚定 452 事件哈希链（含 OpenTimestamps 外部锚）；本文为"树深/哈希长度如何影响防篡改强度"提供可引的定量支撑，可用于 Queyi 威胁模型中对 Merkle 安全边界的诚实声明。

**C3. OpenTimestamps** — `核验-检索`
- 作者/机构：Peter Todd 等（开源社区标准，opentimestamps.org）
- 年份/venue：2016 起 ｜ 开放时间戳标准
- URL：https://opentimestamps.org/
- 核心贡献：定义**可证明时间戳**的创建与**独立验证**操作；当前支持锚定到 **Bitcoin 区块链**；通过免费 calendar servers 聚合，格式可扩展。
- 与 Queyi 的关系：**外部锚定的机制来源**。Queyi 的 "Merkle 根 + OpenTimestamps 外部锚"即用本方案把"证据在某时刻已存在"钉到链外不可篡改的时钟上；本文是该机制的一手权威。
- 说明：官方页已抓取（How it Works / calendar servers / 多语言客户端均确认），但**非学术论文**，故标 `核验-检索`。

---

## 2. Queyi 审计机制 vs 现有框架（对比表，必须）

> 对比维度：① **审计对象**（审什么）｜ ② **是否有判定状态**（是否显式编码多元/不确定性判定）｜ ③ **是否可独立复算**（第三方能否一行命令重算）｜ ④ **是否防篡改**（证据/判定是否 tamper-evident）。
> 说明：本表基于公开文献的**已知属性**与 Queyi 已登记能力，属**架构层对比**，非逐个跑通代码的实证对比。

| 框架 | 审计对象 | 判定状态 | 可独立复算 | 防篡改 |
|---|---|---|---|---|
| **Queyi（本文）** | **软件验证的证据获取装置**（资产池/口径/环境/标签/分母） | ✅ **四态**：survives / weakened / collapses / unresolved（unresolved 为一等公民） | ✅ **claim–caliber 接口**：每个数字一行命令复算 | ✅ **452 事件 append-only 哈希链 + Merkle 根 + OpenTimestamps 外部锚** |
| Model Cards (Mitchell 2019) | 单个模型 | ❌ 静态文本 | ❌ | ❌ |
| Datasheets (Gebru 2021) | 数据集 | ❌ 静态文本 | ❌ | ❌ |
| **Data Cards (A2)** | 数据集 | ❌ 静态文档 | ❌ | ❌ |
| **Croissant (A1)** | 数据集元数据 | ❌ 描述格式 | ⚠️ 可加载数据，非复算结论 | ❌ |
| HELM (Liang 2023) | LLM 多场景表现 | ⚠️ 评分/二元 | ⚠️ 发布代码数据，非环境钉定 | ❌ |
| **NIST AI RMF (B8)** | 组织 AI 风险流程 | ⚠️ 风险分类（非结论判定） | ❌ | ❌ |
| **ACM Artifact Badging (A9)** | 论文工件/结果 | ⚠️ 离散徽章（Available/Evaluated/Reproduced/Replicated） | ⚠️ 人工评审，非一行复算 | ❌ |
| **criterion / assurance audit (B2)** | AI 系统的合规与保证 | ⚠️ 审计意见（流程性） | ❌ | ❌ |
| DeepFact (huang2026deepfact，已引) | 基准**标签**（事实性断言真值） | ⚠️ 审计后更新标签 | ⚠️ 版本化理由可审计 | ❌ |
| Who Grades the Grader (zhang2026whogrades，已引) | LLM agent 的**评分函数** | ❌（指标失败即弃用） | ✅ 可检查表达式 | ❌ |
| SV-COMP 2026 (beyer2026svcomp，已引) | 验证器在固定任务集上的表现 | ⚠️ 超时/未知≈未解答 | ✅ **独立 witness validation** | ⚠️ 竞赛基础设施记录 |
| **RO-Crate (C1)** | 计算工作流执行溯源 | ❌ 溯源表达 | ⚠️ 内容寻址可查，非判定复算 | ❌（无篡改承诺） |

### 关键差异（Queyi 的"判定代数"定位）

现有框架可归为三类，**Queyi 都不属于**：
1. **报告模板**（Model Cards / Datasheets / Data Cards）：产出**静态文档**，无判定状态、无复算、无防篡改。
2. **评分系统**（HELM / ACM 徽章 / 各类 benchmark）：产出**分数或离散等级**，本质是"给对象打分"，不回答"结论是否幸存"。
3. **制度/流程框架**（NIST AI RMF / criterion audit）：产出**流程与合规意见**，不做可复算的证据级判定。

Queyi 是第四类——**判定代数（verdict algebra）**：
- **四态判定**把"检测器不可用（unresolved）"与"检测器说没问题（survives）"**显式区分为两种知识状态**——这是所有模板/评分/流程框架都不具备的；
- **claim–caliber 接口**让每个数字绑定口径 Q=(D,A,E,Θ,P) 且**一行命令复算**，把"可复现"从"应该做"变成"可执行、可证伪"；
- **452 事件 append-only 哈希链 + Merkle 根 + OpenTimestamps**让判定演化**tamper-evident**，是现有框架中唯一把"判定历史"做成密码学锚定对象的。

一句话：现有框架多回答"**你该报告什么 / 我给它打几分**"，Queyi 回答"**在被审计之后，这个结论还成立吗——成立到什么程度、以什么口径、能否被独立复算、能否被篡改**"。

---

## 3. 可以引用的审计框架和方法论

按 Queyi 的论证需要，推荐直接引用的框架/方法（含建议引用的具体论点）：

1. **四态判定的术语合法性** → 引 **A5（Desai 2024）** + **A3（Albertoni 2023）** + **A7（Antunes 2024）**：
   论证"reproducibility / replicability / repeatability"须先分术语，Queyi 的四态是对这一术语体系的**可执行落地**。
2. **unresolved（不可用）是正当知识状态** → 引 **B5（Lv 2026，Uncertainty-Aware Rejection）** + **A4（Semmelrock 2024）**：
   两者都主张"不确定时应拒绝下结论"，为 Queyi "unresolved 一等公民"提供 2026 年外部背书。
3. **可复现性可被测量** → 引 **A6（Obadage 2024）**：其"引用情感→复现评分"是间接测量先例；Queyi 的"一行命令复算"是直接测量，可对比。
4. **审计程序与制度设计** → 引 **B2（Lam 2024, criterion audit）** + **B3（Raji 2022, Outsider Oversight）**：
   B2 给流程蓝图，B3 论证"制度设计 > 单次审计"；支撑 Queyi 的"协议"属性与"外部锚"必要性。
5. **审计者本身要被审计（递归）** → 引 **B1（Costanza-Chock 2022）** + **B5（Lv 2026）**：
   B1 第 6 条政策建议（审计者认证/评估）是递归问题的制度表述；B5 是技术实现。
6. **元评估/审计基准本身** → 引 **B4（Siedler 2026）** + **B6（Li 2024, LLMs-as-Judges survey）**：
   支撑"评估器须被评估"的合法性，并把 Queyi 置于"元评估"研究谱系。
7. **溯源与内容寻址标准** → 引 **C1（RO-Crate）**：把 Queyi 的证据打包对齐社区标准（W3C PROV）。
8. **防篡改的密码学依据** → 引 **C2（Merkle 碰撞概率）** + **C3（OpenTimestamps）**：为 Queyi 的 Merkle + 外部锚提供安全性与机制一手来源。
9. **预注册公开化** → 引 **A8（Vaccaro 2026）**：支撑 686 C3 提出的"把 A5 uninterpretable 条款公开预注册"的 revision 动作。
10. **元数据层对齐** → 引 **A1（Croissant）** + **A2（Data Cards）**：说明 Queyi 的 `croissant.json` / `DATASHEET.md` 与社区标准一致（NeurIPS E&D 友好）。

---

## 4. 关键发现与趋势总结

1. **可复现性研究已从"呼吁"走向"测量与制度"**（A3–A7）：2023–2025 年出现术语澄清（A3/A5/A7）、危机量化与障碍矩阵（A4）、复现信号的量化研究（A6）。趋势是**把可复现性当作可度量对象**——这正是 Queyi 的立足点。

2. **"审计"正在从 AI 治理域向评估域扩散**（B1–B8）：AI 审计从"政策倡导"（B1/B3）发展到"可操作框架"（B2）与"标准体系"（B8），2026 年进一步出现"审计基准/评估器本身"的元评估（B4/B5）。Queyi 站在这一波的最前端：把"审计"直接对准**证据获取装置**。

3. **"判定状态"是当前框架的普遍缺口**（对比表）：模板类无状态、评分类二元、流程类不做结论判定。**只有 Queyi 把 unresolved 与 survives 显式区分**——这是本批检索中最清晰的差异化信号（B5 的 Uncertainty-Aware Rejection 是唯一近似同构者，但作用于 LLM 评估而非执行级验证装置）。

4. **防篡改仍主要停留在"溯源表达"层**（C1/C2/C3）：RO-Crate 做**表达**，Merkle/OpenTimestamps 做**密码学锚定**，但**把二者与"判定状态"绑定**的框架未见。Queyi 的"452 事件哈希链 + Merkle 根 + 外部锚"是对这一空白的填补。

5. **"审计者被审计"的递归问题在文献里是"被提出但未被装置化"**：B1（2022）提出审计者认证的政策建议，B5（2026）给出 LLM 域的元评估实现；但**尚未见**把"审计协议本身"做成可复算、可证伪装置的完整工作——Queyi 的 452 事件账本（审计过程本身被记录）是朝此方向的尝试，但**尚无第三方执行**（见 §6 与 686 C3）。

6. **预注册正在 ML/AI 域回潮**（A8）：2026 年 ICML Spotlight 级别的主张，为 Queyi "把降级标准公开预注册"提供了及时的外部支撑，可把 686 C3 的路线图动作升级为**有文献依据的必做项**。

---

## 5. 检索记录（可复核表）

| # | 检索词 | 日期 | 工具 | 命中并采纳的条目 |
|---|---|---|---|---|
| S1 | `ML Reproducibility Challenge 2025 report reproducibility findings` | 2026-10-08 | WebSearch | A6（经二次定位）、reproml.org（背景） |
| S2 | `ACM artifact evaluation badging study reproducibility 2024 2025` | 2026-10-08 | WebSearch | **A9** |
| S3 | `reproducibility replicability terminology debate definitions machine learning` | 2026-10-08 | WebSearch | **A3**、A5、A7 |
| S4 | `Croissant dataset metadata format NeurIPS 2024` | 2026-10-08 | WebSearch | **A1** |
| S5 | `algorithmic auditing framework AI systems third-party audit practice 2025` | 2026-10-08 | WebSearch | **B2**、B3 |
| S6 | `Data Cards dataset documentation framework 2022 Google` | 2026-10-08 | WebSearch | **A2** |
| S7 | `RO-Crate W3C PROV content addressed research object provenance` | 2026-10-08 | WebSearch | **C1** |
| S8 | `transparency log tamper-evident research integrity scientific record` | 2026-10-08 | WebSearch | （背景，未采纳为独立条目） |
| S9 | `OpenTimestamps blockchain timestamp research reproducibility verifiable` | 2026-10-08 | WebSearch | **C3** |
| S10 | `preregistration machine learning experiments registered reports` | 2026-10-08 | WebSearch | **A8** |
| S11 | `quantifying reproducibility crisis machine learning empirical study survey` | 2026-10-08 | WebSearch | **A4**、A6 |
| S12 | `"who audits the auditor" AI accountability recursion meta-audit` | 2026-10-08 | WebSearch | **B1** |
| S13 | `NeurIPS reproducibility checklist effectiveness study authors artifact 2024` | 2026-10-08 | WebSearch | （背景，未采纳） |
| S14 | `automated scientific claim verification evidence extraction 2025 LLM` | 2026-10-08 | WebSearch | **B7** |
| S15 | `NIST AI Risk Management Framework audit ISO 42001 AI assurance standard` | 2026-10-08 | WebSearch | **B8** |
| S16 | `merkle tree blockchain science research data integrity timestamping` | 2026-10-08 | WebSearch | **C2** |
| S17 | `"auditing the auditors" LLM evaluation benchmark meta-evaluation 2025` | 2026-10-08 | WebSearch | **B4** |
| S18 | `accreditation certification algorithmic auditors evaluation governance` | 2026-10-08 | WebSearch | （背景，佐证 B1 建议 6） |
| S19 | `meta-evaluation auditing evaluators LLM judges who evaluates the evaluator` | 2026-10-08 | WebSearch | **B5**、B6 |
| S20 | `Outsider Oversight third party audit ecosystem AI governance Raji` | 2026-10-08 | WebSearch | **B3** |

| # | 核验抓取（WebFetch） | 日期 | 结果 |
|---|---|---|---|
| F1 | https://arxiv.org/abs/2403.19546（A1） | 2026-10-08 | ✅ 标题/作者/venue/摘要全对 |
| F2 | https://arxiv.org/abs/2204.01075（A2） | 2026-10-08 | ✅ |
| F3 | https://arxiv.org/abs/2302.12691（A3） | 2026-10-08 | ✅ |
| F4 | https://arxiv.org/abs/2310.02521（B1） | 2026-10-08 | ✅ |
| F5 | https://arxiv.org/abs/2401.14908（B2） | 2026-10-08 | ✅ |
| F6 | https://arxiv.org/abs/2312.07852（C1） | 2026-10-08 | ✅ |
| F7 | https://arxiv.org/abs/2606.11217（A8） | 2026-10-08 | ✅ |
| F8 | https://arxiv.org/abs/2405.03977（A6） | 2026-10-08 | ✅ |
| F9 | https://arxiv.org/abs/2406.14325（A4） | 2026-10-08 | ✅ |
| F10 | https://arxiv.org/abs/2407.10239（A5） | 2026-10-08 | ✅ |
| F11 | https://arxiv.org/abs/2408.14317（B7） | 2026-10-08 | ✅ |
| F12 | https://arxiv.org/abs/2607.28801（B4） | 2026-10-08 | ✅ |
| F13 | https://arxiv.org/abs/2402.07530（A7） | 2026-10-08 | ✅ |
| F14 | https://arxiv.org/abs/2206.04737（B3） | 2026-10-08 | ✅ |
| F15 | https://arxiv.org/abs/2412.05579（B6） | 2026-10-08 | ✅ |
| F16 | https://arxiv.org/abs/2402.04367（C2） | 2026-10-08 | ✅ |
| F17 | https://opentimestamps.org/（C3） | 2026-10-08 | ✅（官方页） |
| F18 | https://ieeexplore.ieee.org/abstract/document/11583935（B5） | 2026-10-08 | ⚠️ 摘要/元数据确认，正文付费墙 |
| F19 | https://www.nist.gov/publications/...ai-rmf-10（B8） | 2026-10-08 | ✅（官方页） |
| F20 | https://www.acm.org/publications/policies/artifact-review-and-badging-current（A9） | 2026-10-08 | ❌ 两次抓取返回空（JS 渲染）→ 标 `核验-检索` |

> 检索工具为**通用网络搜索 + 页面抓取**，**非**学术数据库系统检索（无 Scopus/DBLP/ACM DL 全文检索）。
> 因此本表**不能**声称是系统综述，而是"投稿前补漏"性质的定向检索。

---

## 6. 与 684/685/693 已有调研的关系（新增了什么）

| 批次 | 已有覆盖 | 695 方向 4 **新增**的部分 |
|---|---|---|
| **684**（Related Work 补充，18 篇） | 子模优化 / 主动测试 / 治理·Goodhart（Goodhart 1975、Strathern、Gebru、Mitchell、Pineau、Raji 2021） | 684 的治理条目是**哲学/规范层**；695 补上**可操作的审计框架**（B1–B3）与**可复现性的量化研究**（A3–A7） |
| **685**（前沿理论调研，39 篇） | 子模 12 / 主动 9 / 评估方法学 12（含 HELM、BIG-bench、Skalse、Shankar、Raji 2021）/ 信息论 6 | 685 的"评估方法学"聚焦**指标博弈与基准治理**；695 新增**可复现性术语与危机量化**（A3–A7）、**artifact evaluation/badging 机制**（A9）、**AI 审计制度**（B1–B3/B8）、**元评估**（B4–B6） |
| **693**（相关工作更新，2026 新条目） | HOW2BENCH（Cao 2026）、fuzzer/static 比较（Hassler 2026）、SV-COMP 2026、NeurIPS E&D track、LLM-Judge Validation | 693 新增的是**软件验证基准/竞赛**近邻；695 新增的是**审计与可复现性框架**族，二者互补：693 回答"有哪些近邻装置"，695 回答"审计/可复现的**方法论与制度**谱系长什么样" |
| **686**（元评估/反身性） | C2 框架对比表（Queyi vs HELM/Model Cards/Datasheets/Evals）、C3 反身性批判（递归、自欺、外部锚） | 695 为 686 的**论断补上文献支撑**：C3 的"外部锚是唯一出口"↔ B3（Outsider Oversight）；C3 的"递归问题"↔ B1（Who Audits the Auditors）+ B5（Who Evaluates the Evaluators）；C3 的"预注册公开化"↔ A8（Vaccaro 2026） |

**695 相对前三批的净新增（一句话）**：
> 前三批给了 Queyi **算法（子模/主动）**与**治理哲学（Goodhart）**的根；695 补上 **可复现性测量（A3–A7）、审计框架与制度（B1–B8）、溯源与防篡改标准（C1–C3）** 三条新线，
> 并把 **"审计者被审计"的递归问题**从 686 的内部批判，升级为**有 2022–2026 外部文献支撑**的可引主张。

**未重复**：HELM、DeepFact、Who Grades the Grader、SV-COMP 2026 等已见于 685/689/693，仅在 §2 对比表中作对照，不计入本批"新增"。

---

## 附：诚实边界与待办

1. **A9（ACM 徽章）正文未逐字抓取**：官方页 JS 渲染导致 WebFetch 返回空；徽章名称与版本（V1.1, 2020-08-24）来自检索摘要。**引用前建议人工打开页面核对措辞**。
2. **B5（Who Evaluates the Evaluators）为 IEEE 会议论文**（ICSIPC 2026），仅抓到摘要与元数据，**未读全文**；对其"三方面机制"的转述限于摘要范围，不得外推。
3. **C3（OpenTimestamps）非同行评审论文**，是开源标准；引用时按"标准/工具"而非"研究文献"处理。
4. **B4（Benchmarks Are Not Monolithic）与 B7（Claim Verification survey）为 arXiv 预印本**，会议接收状态未核验；bib 建议按 arXiv 记，注"接收状态待核验"。
5. **A8（Vaccaro 2026）**已核验为 ICML 2026 Spotlight（arXiv 页注明 "Accepted at ICML 2026 as a Spotlight (Top 5%)"），但**正式 proceedings 页码未核验**。
6. **术语一致性**：本批 A3/A5/A7 对 "reproducibility vs replicability" 的定义**互有细微差异**（NISO/ACM 2020 曾互换两词），引用时须**明确采用哪一家的定义**，不得混用（与 Queyi 的口径纪律一致）。
