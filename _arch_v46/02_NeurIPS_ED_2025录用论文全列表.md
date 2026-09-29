# 方向 02：NeurIPS 2025 Datasets & Benchmarks（D&B）录用论文全列表

## 核心结论

1. NeurIPS 2025 D&B track 收到 **1,995 篇投稿**（D&B chairs 官方博客原文："the track received 1,995 submissions this year"），是 2024 年 1,820 篇之后的**首次"增长放缓"**（2023→2024 是 987→1,820，2024→2025 只增 175 篇，官方定性为"the track has begun to stabilize"）。
2. **2025 年 D&B 最重大的制度变化是评分量表从 1–10 换成 1–6**，导致分数整体下移且分布收窄：录用论文篇均分 **4.65**、拒稿篇均分 **4.13**，而 D&B chairs 明确提到 track-wide average score 为 **4.25** 并被用作 SAC 追加排名的分界线。
3. **2025 年 D&B 首次允许 single-blind 投稿、首次强制数据集托管 + Croissant 元数据**，官方复盘显示 80% 以上录用论文把数据集放在 Hugging Face / Kaggle / Dataverse / OpenML 四个平台，**84% 的录用论文引入了新数据集**。

---

## 精确数字与案例

### 一、官方投稿数、评审规模与"稳定化"叙事

NeurIPS D&B chairs 在 2025-09-30 的官方复盘博客里给出了本年度**最权威的一段数字**，逐字摘录：

> "After three years of exponential growth, the track received **1,995 submissions** this year. While this is a large number, the increase from the **1,820 submissions** received last year is smaller than in previous years (for comparison, there were **987 submissions in 2023**), suggesting that the track has begun to stabilize."

同一段还给出 2024 年 D&B 的录用率与主赛道对照：

> "A first step in the direction of alignment with the main track began in 2024, when DB track saw an **acceptance rate of 25.3%** closely mirroring the main program's **25.8%** rate."

2025 年 D&B 的**评审资源规模**（来自 2025-12-05 的 D&B 年度复盘博客）：

> "This last year, the track operated with **41 senior area chairs, 281 area chairs and 2,680 reviewers**."

作为对照，主赛道 2025 年是 **20,518 reviewers、1,663 ACs、199 SACs**（PC chairs 博客原文），投稿 **21,575 篇**。也就是说 D&B 用**约占主赛道 13% 的审稿人**（2,680 / 20,518）处理了**约占主赛道 9.2% 的投稿**（1,995 / 21,575）。

### 二、录用数：三个口径

- **官方虚拟站**：`https://nips.cc/virtual/2025/events/datasets-benchmarks-2025` 页面顶部标注 **"494 Events"**。
- **Paper Copilot 统计**：`legacy.papercopilot.com` 的 NeurIPS 2025 D&B 行给出 **Total 591；Accept 497 (84.09%)；Poster 434 (73.43%)；Spotlight 56 (9.48%)；Oral 7 (1.18%)；Reject 94 (15.91%)**。
- **Paper Copilot 原始 JSON**（`nips/nips2025.json`，38,038,097 字节）：`track == "Datasets & Benchmarks"` 共 **591 条**，status 分布 Poster 434 / Reject 94 / Spotlight 56 / Oral 7，与统计页一致。

⚠️ **"84.09%"是典型的样本偏差陷阱**：591 只是"公开了评审记录（opt-in）"的样本，分母不是 1,995。用官方投稿数计算的真实录用率是 **497 / 1,995 = 24.91%**，或按虚拟站 494 计为 **494 / 1,995 = 24.76%**。**Paper Copilot 自己在页面上就写了这个警示**：

> "If rating scores are publicly available, the statistics are based on submissions that opted in for release. … If scores are collected from the community via the Google Form, the statistics reflect only those samples."

**这条"84% vs 25%"的对比，是阙疑论文 Threats to Validity 里"分母污染"的最佳实证。**

### 三、评分分布（2025 年 D&B，6 分制）

| 分组 | n | 均分（各篇均分的平均） | 中位数 | 最小 | 最大 | 平均 confidence | 平均审稿人数 |
|---|---|---|---|---|---|---|---|
| 全部录用 | 497 | **4.65** | 4.60 | 3.50 | 5.75 | 3.60 | 3.93 |
| Poster | 434 | 4.60 | 4.50 | 3.50 | 5.33 | 3.58 | 3.93 |
| Spotlight | 56 | **5.00** | 5.00 | 4.33 | 5.75 | 3.66 | 3.88 |
| Oral | 7 | **5.00** | 5.00 | 4.75 | 5.25 | 4.08 | 4.14 |
| Reject | 94 | **4.13** | 4.25 | 2.67 | 5.00 | 3.54 | 3.99 |

**单条评审分直方图**（D&B 全部 591 条）：2 分 15 条、3 分 59 条、**4 分 938 条、5 分 1,216 条**、6 分 100 条。也就是说 2025 年 D&B 的分数**高度集中在 4 与 5**，6 分（Strong Accept）全 track 只出现 100 次。

**篇均分桶（0.5 粒度）**：2.5→2 篇、3.0→3 篇、3.5→4 篇、4.0→102 篇、**4.5→265 篇、5.0→209 篇**、5.5→5 篇、6.0→1 篇。可见"4.5 分"是最大的单一桶（265 篇），**录用的实际分界线在篇均 4.0 附近**。

D&B chairs 对这个现象有**官方解释**（原文）：

> "1. **Increased average score:** Unlike papers in the main track, which one can expect to be more method and algorithm oriented, it is less common for a dataset submission to be fundamentally 'technically incorrect.' 2. **Subjective nature of contributions:** Evaluating the merit of a dataset or benchmark can be highly subjective. … We think that these factors can lead to reviewer scores that skew higher and have a tighter distribution compared to the papers in the main track. As a result, it can be difficult for the ACs to differentiate clearly between two papers that may have the same average score but vastly different merits and trade-offs."

以及他们的应对措施（**对阙疑极具参考价值**）：

> "we asked our SACs, based on their discussion with the ACs, to produce **a relative ranking of the papers within their stack of papers**. … For any paper ranked below the track-wide average score of **4.25**, SACs were required to provide a detailed description of its merits and motivation."

**这意味着 NeurIPS D&B 在 2025 年已经承认"分数不够用"，转向"相对排名 + 定性理由"**——这与阙疑主张的"四态判决 + 证据带 provenance"是同一类设计动机，可以直接引用作为相关工作。

### 四、录用论文清单（≥30 篇，含机构）

取自 `nips2025.json`（Paper Copilot 镜像 OpenReview 元数据）。2025 年 Paper Copilot 的 `author_site` 字段大量为空，故本清单以**机构字段**为主、作者以首作者为补。

**Oral（7 篇，全部列出）**

1. NOVA: A Benchmark for Rare Anomaly Localization and Clinical Reasoning in Brain MRI｜Technische Universität München; Munich Center for Machine Learning｜rating 5;5;5;5
2. Envisioning Beyond the Pixels: Benchmarking Reasoning-Informed Visual Editing｜Shanghai Jiao Tong University; Wuhan University; Tsinghua University｜5;5;5;5
3. OrthoLoC: UAV 6-DoF Localization and Calibration Using Orthographic Geodata｜Technische Universität München; DeepScenario GmbH; ETH Zurich｜5;5;5;5
4. CoralVQA: A Large-Scale Visual Question Answering Dataset for Coral Reef Image Understanding｜Beijing University of Posts and Telecommunications｜4;5;5;5;6
5. BEDLAM2.0: Synthetic humans and cameras in motion｜Max Planck Institute for Intelligent Systems; ETH Zurich; Meshcapade｜5;5;5;6
6. WebGen-Bench: Evaluating LLMs on Generating Interactive and Functional Websites from Scratch｜Chinese University of Hong Kong; Shanghai Jiao Tong University; SenseTime｜4;5;5;6
7. Artificial Hivemind: The Open-Ended Homogeneity of Language Models (and Beyond)｜University of Washington; Meta; Carnegie Mellon University; Stanford University｜4;4;5;6

**Spotlight（56 篇，列 30 篇）**

8. PatientSim: A Persona-Driven Simulator for Realistic Doctor-Patient Interactions｜KAIST; University of California｜4;4;5;5
9. Fixing It in Post: A Comparative Study of LLM Post-Training Data Quality and Model Performance｜Technische Universität München; IBM｜5;5;5
10. EuroSpeech: A Multilingual Speech Corpus｜ETH Zurich｜5;5;5
11. GUARD: Constructing Realistic Two-Player Matrix and Security Games for Benchmarking Game-Theoretic Algorithms｜Columbia University｜4;4;5;5
12. Whose View of Safety? A Deep DIVE Dataset for Pluralistic Alignment of Text-to-Image Models｜Google; Brown University; Princeton University｜5;5;5;5
13. Bubbleformer: Forecasting Boiling with Transformers｜University of California, Irvine; Argonne National Laboratory｜5;5;5;5
14. ResearchCodeBench: Benchmarking LLMs on Implementing Novel Machine Learning Research Code｜Stanford University｜5;5;5;5
15. InterMT: Multi-Turn Interleaved Preference Alignment with Human Feedback｜Peking University; Shandong University; University of Electronic Science and Technology of China｜4;4;5;5;5
16. MARS-VFL: A Unified Benchmark for Vertical Federated Learning with Realistic Evaluation｜Wuhan University｜4;4;6;6
17. Sheetpedia: A 300K-Spreadsheet Corpus for Spreadsheet Intelligence and LLM Fine-Tuning｜Peking University; Singapore Management University｜5;5;5
18. ConnectomeBench: Can LLMs proofread the connectome?｜Massachusetts Institute of Technology｜4;4;5;5
19. Open-Insect: Benchmarking Open-Set Recognition of Novel Species in Biodiversity Monitoring｜McGill University; University of Copenhagen; Agriculture and Agri-food Canada｜5;5;5
20. **SWE-smith: Scaling Data for Software Engineering Agents**｜Stanford University; Princeton University; Anthropic; Allen Institute for AI｜4;5;5;6
21. MedSG-Bench: A Benchmark for Medical Image Sequences Grounding｜Beijing University of Posts and Telecommunications; Tianjin University｜4;5;5
22. Embodied Web Agents: Bridging Physical-Digital Realms for Integrated Agent Intelligence｜University of California, Los Angeles; University of Illinois Urbana-Champaign｜5;5;5;5
23. The ML.ENERGY Benchmark: Toward Automated Inference Energy Measurement and Optimization｜University of Michigan; Jane Street; University of Illinois Urbana-Champaign｜4;4;5
24. Data-Juicer 2.0: Cloud-Scale Adaptive Data Processing for and with Foundation Models｜Alibaba Group｜4;5;6;6
25. MME: A Comprehensive Evaluation Benchmark for Multimodal Large Language Models｜Nanjing University; Tencent; Tencent Youtu Lab｜5;5;6;6
26. OS-Harm: A Benchmark for Measuring Safety of Computer Use Agents｜EPFL; ELLIS Institute｜5;5;5;5
27. MMLongBench: Benchmarking Long-Context Vision-Language Models Effectively and Thoroughly｜HKUST; University of Edinburgh｜5;5;6;6
28. AGENTIF: Benchmarking Large Language Models Instruction Following Ability in Agentic Scenarios｜Tsinghua University｜5;5;5;6
29. Scaling Computer-Use Grounding via User Interface Decomposition and Synthesis｜University of Hong Kong; Tsinghua University; University of California｜5;5;5;5;5
30. TIDMAD: Time Series Dataset for Discovering Dark Matter with AI Denoising｜MIT; Stanford University; Columbia University｜5;5;5;6
31. **Reasoning Gym: Reasoning Environments for Reinforcement Learning with Verifiable Rewards**｜Independent; Scale AI; Lloyds Banking Group; Saint Cloud State University｜4;5;5;6
32. Augmenting Biological Fitness Prediction Benchmarks with Landscapes Features from GraphFLA｜University of Electronic Science and Technology of China｜5;5;6;6
33. Robo2VLM: Improving Visual Question Answering using Large-Scale Robot Manipulation Data｜University of California, Berkeley; Google｜5;5;5;5
34. Fire360: A Benchmark for Robust Perception and Episodic Memory in Degraded 360° Firefighting Video｜University of Illinois Urbana-Champaign｜5;5;5;5
35. CausalVerse: Benchmarking Causal Representation Learning with Configurable High-Fidelity Simulations｜（机构字段缺失）｜5;5;5;5
36. Benchmarking Egocentric Multimodal Goal Inference for Assistive Wearable Agents｜Meta 等｜5;5;5;5
37. RoFt-Mol: Benchmarking Robust Fine-tuning with Molecular Graph Foundation Models｜（机构字段缺失）｜5;5;5;5
38. MLIP Arena: Advancing Fairness and Transparency in Machine Learning Interatomic Potentials via an Open, Accessible Benchmark Platform｜（机构字段缺失）｜5;5;5;6
39. HawkBench: Investigating Resilience of RAG Methods on Stratified Information-Seeking Tasks｜（机构字段缺失）｜4;5;5;6
40. CoRe: Benchmarking LLMs' Code Reasoning Capabilities through Static Analysis Tasks｜（机构字段缺失）｜5;5;5;5
41. **TabArena: A Living Benchmark for Machine Learning on Tabular Data**｜（机构字段缺失）｜4;5;5;6
42. **SciArena: An Open Evaluation Platform for Non-Verifiable Scientific Literature-Grounded Tasks**｜Yilun Zhao, Kaiyan Zhang, Tiansheng Hu 等（Yale / Allen Institute for AI 等）｜4;5;5;6
43. **Why Do Multi-Agent LLM Systems Fail?**｜（机构字段缺失）｜5;5;5;6
44. Torch-Uncertainty: Deep Learning Uncertainty Quantification｜（机构字段缺失）｜5;5;5;5
45. MONITRS: Multimodal Observations of Natural Incidents Through Remote Sensing｜（机构字段缺失）｜4;5;5;5
46. MedChain: Bridging the Gap Between LLM Agents and Clinical Practice with Interactive Sequence｜（机构字段缺失）｜4;5;6
47. Solving Inequality Proofs with Large Language Models｜（机构字段缺失）｜4;4;5;5;6
48. Nemotron-CLIMB: Clustering-based Iterative Data Mixture Bootstrapping for Language Model Pre-training｜NVIDIA 等｜4;5;5;5;6
49. A Controllable Examination for Long-Context Language Models｜（机构字段缺失）｜5;5;5;5
50. THUNDER: Tile-level Histopathology image UNDERstanding benchmark｜（机构字段缺失）｜5;5;5;5

**Poster（434 篇，示例 2 篇，均来自官方虚拟站事件页）**

51. TreeFinder: A US-Scale Benchmark Dataset for Individual Tree Mortality Monitoring Using High-Resolution Aerial Imagery｜Zhihao Wang, Cooper Li, Ruichen Wang, Lei Ma, George Hurtt, Xiaowei Jia, Gengchen Mai, Zhili Li, Yiqun Xie
52. Benchmarking Large Language Models with Integer Sequence Generation Tasks｜Daniel O'Malley, Manish Bhattarai, Nishath Ranasinghe, Erick Draayer, Javier E. Santos

### 五、机构分布（2025 D&B，按参与论文数）

| 排名 | 机构 | 参与论文数 |
|---|---|---|
| 1 | Tsinghua University | 41 |
| 2 | Stanford University | 38 |
| 3 | Hong Kong University of Science and Technology | 35 |
| 4 | Peking University | 34 |
| 5 | Meta | 32 |
| 6 | Chinese University of Hong Kong | 29 |
| 6 | Alibaba Group | 29 |
| 8 | Shanghai Jiao Tong University | 27 |
| 8 | Google | 27 |
| 10 | Amazon | 26 |
| 11 | Zhejiang University | 25 |
| 12 | Carnegie Mellon University | 24 |
| 13 | Microsoft | 23 |
| 14 | Shanghai AI Laboratory | 22 |
| 14 | University of California, Berkeley | 22 |

与 2024 年对比：**Tsinghua 仍是第 1（41 篇，两年不变）**；Stanford 35→38；**HKUST 从榜外升到第 3（35 篇）**；Alibaba Group 29 篇、Shanghai AI Lab 22 篇进入前列——**中国机构在 D&B 的占比明显上升**。

### 六、2025 年的制度变化与官方复盘数字

**投稿侧（2025-03-10 博客 + 2025 CFP 原文）**：

- **Single-blind 可选**："Authors can choose to submit either single-blind or double-blind."
- **强制托管**："New datasets should be hosted at one of the hosting sites dedicated to ML datasets (**Dataverse, Kaggle, Hugging Face, or OpenML**)."；"Datasets and code should be **available and accessible to all reviewers, ACs and SACs at the time of submission**. … **Non-compliance justifies the desk rejection of the paper.**"
- **强制 Croissant 元数据**："Authors should use the **Croissant machine-readable format** … and include the Croissant file with their paper submission in OpenReview."

**复盘侧（2025-12-05 博客，全部为原文数字）**：

| 指标 | 数值 |
|---|---|
| 使用四大托管平台的录用论文占比 | **over 80%** |
| 自建/定制托管占比 | **13%** |
| 录用论文中引入新数据集的占比 | **84%** |
| Croissant 缺失 license 字段 | **11.9%** |
| Croissant 缺失数据集描述 | **4.9%** |
| Croissant 缺失 URL | **3.5%** |
| 缺失数据集名称 | **less than one percent** |
| 作者问卷回收 | **851 authors** |
| 审稿人问卷回收 | **155 reviewers** |
| 作者认为托管流程顺利 | **82%** |
| 作者遇到困难 | **16%** |
| 作者认为新要求让评审更公平/更彻底 | **58%** |
| 作者认为评审质量需改进 | **25%** |
| 作者认为托管+元数据要求有效提升质量 | **63%** |
| 审稿人认为数据集易获取 | **77%** |
| 审稿人遇到困难 | **around 10%** |
| **审稿人未实际查看数据集、只看论文** | **11%** |
| 审稿人认为自动元数据报告有用 | **69%** |
| 审稿人认为合规 checklist 提升效率 | **70%** |

**"11% 的审稿人从未打开数据集"这一条对阙疑尤其重要**：它量化了"评审证据链断裂"的比例，可直接支撑阙疑"必须提供不依赖人工打开产物的独立对账器"的动机。

### 七、2025 年 D&B 相对 2024 年的五个结构性变化

把两年的数据并排看，可以提炼出五条可验证的变化：

**变化一：投稿增速从"翻倍"降到"个位数"。** 2023→2024 是 987→1,820（+84.4%），2024→2025 是 1,820→1,995（**+9.6%**）。官方原文用"stabilize"（稳定）来描述。**对阙疑的含义**：赛道不再"水涨船高"，投稿量趋于饱和意味着**录用难度不会因为赛道变热而进一步恶化**，但也意味着"蹭赛道增长红利"的策略失效。

**变化二：录用率维持在主赛道同量级。** 2024 年 D&B 25.3% vs 主赛道 25.8%；2025 年主赛道 24.52%（官方原文），D&B 按第三方可复算约 24.9%。**两年都在 24%–26% 区间**。这条数据否定了"该 track 更容易中"的假设。

**变化三：评分量表换代，分数整体下移且收窄。** 2024 年 D&B 录用篇均 **6.75**（10 分制，即 67.5%），2025 年 **4.65**（6 分制，即 77.5%）——**注意这不是"变难"，而是量表变了**。但**分布的收窄是真实的**：2024 年录用篇均的标准差 0.54（10 分制，相对标准差 8.0%），2025 年是 0.27（6 分制，相对标准差 5.8%）。用相对离散度衡量，**2025 年的分数确实更挤**。

**变化四：分档的分数区分度在下降。** 2024 年 Poster 6.64 / Spotlight 7.38 / Oral 7.62，三档之间有可见间隔（Poster→Spotlight 差 0.74）；2025 年 Poster 4.60 / Spotlight 5.00 / Oral 5.00，**Spotlight 与 Oral 完全同分**。这正是 D&B chairs 所说的"ACs 难以清晰区分"的量化体现，也是他们引入"相对排名 + 4.25 阈值定性理由"的直接原因。

**变化五：评审参与度上升，但审稿人未看产物的问题仍在。** 平均审稿人数从 2024 年的 3.64 升到 2025 年的 3.93；审稿人平均 confidence 从 3.77 降到 3.60。**审稿人变多了，但自评信心反而下降**——官方给出的解释是"submissions increasingly span specialized domains … The reviewer pool shows limitations in diversity and domain coverage"，并承认"Each paper requires review by experts in data-centric machine learning as well as domain-specific knowledge"。**这解释了为什么强制托管 + Croissant 元数据会被采纳**：当审稿人不懂领域时，可机器校验的元数据成了最低成本的信任替代物。

### 八、2025 年录用论文的主题分布（与 2024 年的对比）

2025 年的 497 篇录用论文，主题重心明显从"数据集构建"转向"**LLM / Agent 的行为评测**"。从 Oral 与 Spotlight 的标题即可看出：

- **Agent 与工具使用**：SWE-smith（软件工程 agent 数据）、Embodied Web Agents、AGENTIF（agentic 指令遵循）、Scaling Computer-Use Grounding、OS-Harm（计算机使用 agent 安全性）、WebGen-Bench（生成网站）、AgentRecBench、Why Do Multi-Agent LLM Systems Fail?（**多智能体失败原因**）。
- **可验证奖励与推理环境**：Reasoning Gym（"Reasoning Environments for Reinforcement Learning with **Verifiable Rewards**"）、Solving Inequality Proofs with Large Language Models、ResearchCodeBench、CoRe（代码推理）。
- **评测平台化**：SciArena（"An Open Evaluation Platform for Non-Verifiable Scientific Literature-Grounded Tasks"）、TabArena（"A Living Benchmark"）、MLIP Arena、MME、THUNDER。
- **AI for Science 延续**：TIDMAD（暗物质）、Bubbleformer（沸腾预测）、Augmenting Biological Fitness Prediction、Roft-Mol、MONITRS、STAR（天文超分）、ProteinConformers。
- **安全与对齐**：OS-Harm、CARES（医学 LLM 安全性）、DeceptionBench、Artificial Hivemind、Whose View of Safety?、Comprehensive Assessment and Analysis for NSFW Content Erasure。

**与 2024 年对比的两条关键变化**：

1. **"Agent 评测"取代"LLM 静态问答评测"成为主流**（2024 年的 AgentBoard / Embodied Agent Interface 是先行者，2025 年变成集群）。
2. **"可验证性"（verifiability）成为显式关键词**：Reasoning Gym 标题里直接写"with **Verifiable Rewards**"；SciArena 的定位是"**Non-Verifiable** Scientific Literature-Grounded Tasks"；AGENTIF 测的是"指令遵循的**可判定**程度"。**这说明 2025 年该 track 的评审已经在奖励"可判定 / 可验证"的设计**——阙疑的核心主张（可被独立验收）正落在这一趋势上。

### 九、从 2025 年数据看"单人 + 无机构背书"的可行性

D&B 2025 的机构分布（前 15）全部是头部高校与大厂，**没有任何"个人研究者"或"双非院校"进入前列**。但有两处反例值得注意：

1. **Reasoning Gym** 的机构列表里出现 "**Independent**"（独立研究者），该论文最终为 **Spotlight**。
2. 2025 年 D&B 的 **Oral 中有 2 篇的第一机构是 Technische Universität München（TUM）**，而非美国头部机构；Spotlight 中亦有 Wuhan University、Beijing University of Posts and Telecommunications 等非 Top-10 机构单篇出现。

**结论**：机构集中度高是事实，但**"Independent" 能进 Spotlight 说明该 track 不以机构为门槛**；真正的门槛是"贡献是否可被独立使用/验收"。这对阙疑是**利好信号**，但必须诚实地说：**该 track 没有任何"双非本科生单人论文"的公开先例可查**（我们未找到此类案例的报道），因此这条推断仍是**弱证据**。

### 十、2025 年 D&B 的 Best Paper：Artificial Hivemind（补上本方向盲区）

本方向初稿把"2025 年 D&B 的 Best Paper / Outstanding Paper 名单未核实"列为盲区。补检索后可确认：**NeurIPS 2025 于 2025-11-26 公布 7 篇获奖论文 = 4 篇 Best Paper + 3 篇 Runner-Up，其中 Best Paper 有 1 篇来自 Datasets & Benchmarks track**，官方原文为：

> "the best and runner-up paper awards this year go to seven groundbreaking papers, including **four best papers (one of which is from the datasets and benchmarks track)** and three runner-ups."

**该篇 D&B Best Paper 是**：*Artificial Hivemind: The Open-Ended Homogeneity of Language Models (and Beyond)*，作者为 Liwei Jiang、Yuanjun Chai、Margaret Li、Mickel Liu、Raymond Fok、Nouha Dziri、Yulia Tsvetkov、Maarten Sap、Yejin Choi。它的核心产出是 **Infinity-Chat 数据集：26,000 条真实世界开放式用户查询 + 31,250 条人类标注**（每例 25 个独立标注），并在 **70+ 个模型**上研究"mode collapse"，提出 Artificial Hivemind 效应（模型内重复 + 模型间同质化）。评奖委员会给该 D&B 论文的评语原文是：

> "Overall, this work **sets a new standard for datasets and benchmarks** that advance scientific understanding and address pressing societal challenges rather than solely improving technical performance."

**三条对本方向的校正**：
1. 该篇 Best Paper **正是本方向第四节的 Oral 第 7 条**（Artificial Hivemind，机构为 University of Washington / Meta / Carnegie Mellon / Stanford），说明**本文件的 Oral 清单与官方获奖名单可以互相印证**——本清单的口径得到了一次独立交叉验证。
2. **D&B 的 Best Paper 奖励的是"数据集/基准的方法学"，而不是"更高的技术指标"**（评语原文强调 "rather than solely improving technical performance"）。这与阙疑"把测量陷阱本身当作产出"的主张同构。
3. 2025 年 Best Paper 委员会（Main Track 与 D&B 共用一个委员会）成员包括 Jacob Andreas（MIT）、Doina Precup（McGill）、Luke Zettlemoyer（University of Washington/Meta）、Xing Xie（Microsoft）等 14 人，**其中 Xing Xie 同时出现在 2024 年 D&B 的评审委员会名单中**——**该 track 的评奖/评审委员会存在跨年连任**。

**再补一条与"该 track 评审趋势"呼应的证据**：该篇 D&B Best Paper 的获奖理由强调"数据集/基准应推进科学理解、回应社会挑战，而不仅是提升技术性能"——这与本方向第七节总结的"2025 年 D&B 从'数据集构建'转向'LLM/Agent 行为评测'"、第九节"可验证性成为显式关键词"是同一趋势的官方表述。也就是说，**2025 年该 track 的最高奖，颁给了一篇"评测方法学"论文**（Artificial Hivemind 研究的是模型输出的同质化，属评测而非建模），**而不是一篇"更高的 SOTA"论文**。对阙疑的含义：**该 track 的最高荣誉明确奖励"测量与评测的设计"，而不是"更强的系统"**——这正是阙疑应当对齐的价值取向。

---

## 对阙疑的 3 条具体行动

1. **把"11% 审稿人未查看产物"写进 Introduction 的动机段**：在 `research/paper_v0.3.md` 的 §1 加一句带引文的主张——"即使在被要求强制托管数据集的 NeurIPS 2025 D&B track，仍有 **11%** 的审稿人未实际检查数据集（来源：NeurIPS Blog, 2025-12-05）；这解释了为什么'可被独立验收'必须由机器而非人完成"。**同时**在 `research/02_hypotheses.md` 里加一条 H：*机器可对账的产物应能把"人工未核验"的缺口从 11% 降到接近 0*。时间点：2026-10 前。
2. **建立"分母纪律"检查脚本**：新增 `tools/check_denominator_<batch>.py`，扫描 `research/*.md` 与 `data/**/*.json` 中所有形如 `X / Y = Z%` 的断言，强制要求每条断言显式声明分母来源。**首个靶子就是本方向发现的"Paper Copilot 84.09% vs 官方口径 24.9%"**——把这两个数并列写进 `research/12_threats_to_validity.md` 的 `T2: Opt-in sampling inflates rates` 小节。这条规则对阙疑自身同样致命：**阙疑的"检出率 66.7%（10/15 可测）"分母是 15 而不是 17，必须像 NeurIPS 一样把"为什么分母变小"写在正文里**。
3. **对齐 D&B 的"相对排名 + 定性理由"机制**：D&B chairs 在 2025 年对篇均分低于 4.25 的论文强制要求 SAC 给出定性理由。阙疑应在 `research/08_metrics.md` 里引入同构机制：**对每条被判 `unknown`（四态之一）的卡，强制要求输出"为何无法判决"的机器可读理由字段**（而非静默跳过）。可用 `tools/gate_engine.py` 的 advice 层（现有 7 条 advice 规则）扩展，产出 `data/unknown_justifications_<batch>.json`，字段固定为 `{atom_id, rule_id, reason_code, evidence_ref}`。时间点：与下一批规则迭代同批。

---

## 盲区（诚实标注）

- **2025 年 D&B 的官方录用数未在任何官方文本中出现**。官方只给了投稿数（1,995）与评审规模，**没有给录用数或录用率**。本文件的 497 来自 Paper Copilot（opt-in 样本），494 来自官方虚拟站计数，**两者均非官方"录用数"**；24.91% / 24.76% 是本文件**自行计算**的结果，已在文中标注。
- **"84% 的录用论文引入新数据集"中的"84%"**：官方原文是"Eighty-four percent of accepted papers introduced new datasets as part of benchmark or evaluation contributions"，**未说明分母**是 494 还是 497，也未说明是否只统计了提交问卷的子集。
- **2025 年 D&B 的 Best Paper / Outstanding Paper 名单未核实**。我们检索到 NeurIPS 2025 有 4 篇主赛道最佳论文（含 Qwen 相关），但**未找到 D&B track 单独的获奖名单**；`neurips.cc/virtual/2025/awards_detail` 未逐条核对。**（补强后已复核：见第十节——NeurIPS 2025 官方 blog 2025-11-26 明确 D&B Best Paper 为 *Artificial Hivemind*；但"Outstanding Paper / Runner-Up 中是否另有 D&B 论文"仍未核实。）**
- **Paper Copilot 的 `author_site` 字段在 2025 数据中大量为空**，因此本清单第 35 条之后的"第一作者"多标注为"机构字段缺失"，**这不是论文没有作者，而是镜像数据缺字段**。
- 2025 年 D&B 的**拒稿论文只有 94 条进入 opt-in 样本**（占 1,995 的 4.7%），因此"录用 4.65 vs 拒稿 4.13"的对比**样本严重不平衡**，不能外推为全体投稿的分数分布。
- **本文件未逐篇打开 OpenReview 核对**（Cloudflare Turnstile 拦截本机自动化访问）。

---

## 来源

1. Reflecting on the 2025 Review Process from the Datasets and Benchmarks Chairs — https://blog.neurips.cc/2025/09/30/reflecting-on-the-2025-review-process-from-the-datasets-and-benchmarks-chairs/ — "1,995 submissions" / "1,820 submissions" / "987 submissions in 2023" / "25.3% … 25.8%" / "track-wide average score of 4.25" — NeurIPS Blog，2025-09-30
2. NeurIPS Datasets & Benchmarks Track: From Art to Science in AI Evaluations — https://blog.neurips.cc/2025/12/05/neurips-datasets-benchmarks-track-from-art-to-science-in-ai-evaluations/ — "1,995 in 2025" / "41 senior area chairs, 281 area chairs and 2,680 reviewers" / 80%、13%、84%、11.9%、4.9%、3.5% / 851 authors、155 reviewers / 82%、16%、58%、25%、63% / 77%、10%、11%、69%、70% — NeurIPS Blog，2025-12-05
3. Reflections on the 2025 Review Process from the Program Committee Chairs — https://blog.neurips.cc/2025/09/30/reflections-on-the-2025-review-process-from-the-program-committee-chairs/ — "21,575 valid paper submissions, of which 5,290 were accepted" / "24.52%" / "20,518 reviewers, 1,663 ACs and 199 SACs" / "11 unfortunate cases" — NeurIPS Blog，2025-09-30
4. NeurIPS 2025 Datasets & Benchmarks Track Call for Papers — https://neurips.cc/Conferences/2025/CallForDatasetsBenchmarks — single-blind / 强制托管 / Croissant / "Non-compliance justifies the desk rejection" — NeurIPS，2025
5. NeurIPS 2025 D&B 虚拟站事件页 — https://nips.cc/virtual/2025/events/datasets-benchmarks-2025 — "494 Events" + 52 篇可见标题与作者 — NeurIPS，2025
6. NeurIPS 2025 Reviewer Guidelines — https://neurips.cc/Conferences/2025/ReviewerGuidelines — Overall 1–6 / Quality·Clarity·Significance·Originality 各 1–4 / Confidence 1–5 — NeurIPS，2025
7. Paper Copilot，NeurIPS 2025 D&B 录用列表与统计 — https://legacy.papercopilot.com/paper-list/neurips-paper-list/neurips-2025-accepted-paper-list-datasets-benchmarks-track/ — Total 591 / Accept 497 (84.09%) / Poster 434 / Spotlight 56 / Oral 7 / Reject 94 — Paper Copilot，2026 访问
8. Paper Copilot 原始数据仓库 — https://github.com/papercopilot/paperlists （`nips/nips2025.json`，38,038,097 字节）— Paper Copilot，2026 访问
9. NeurIPS 2025 Datasets & Benchmarks Accepted Papers（模板页，含失效的"163"）— https://neurips.cc/Conferences/2025/DatasetsBenchmarks/AcceptedPapers — NeurIPS，2025
10. OpenReview，NeurIPS 2025 Datasets and Benchmarks Track — https://openreview.net/group?id=NeurIPS.cc/2025/Datasets_and_Benchmarks_Track — OpenReview，2025
11. NeurIPS Blog (2025-11-26). *Announcing the NeurIPS 2025 Best Paper Awards*（7 篇获奖 = 4 Best + 3 Runner-Up；"one of which is from the datasets and benchmarks track"；D&B Best Paper = Artificial Hivemind；Infinity-Chat 26K 查询 + 31,250 标注；70+ 模型；评奖委员会 14 人含 Xing Xie）。https://blog.neurips.cc/2025/11/26/announcing-the-neurips-2025-best-paper-awards/
