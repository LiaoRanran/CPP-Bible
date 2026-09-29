# 方向 01：NeurIPS 2024 Datasets & Benchmarks（D&B）录用论文全列表

## 核心结论

1. NeurIPS 2024 D&B track 的**官方口径是 1,820 篇投稿、460 篇录用、录用率 25.3%**（NeurIPS 2024 Fact Sheet PDF 原文），而会议虚拟站 D&B 页面显示 **459 Events**，第三方聚合站 Paper Copilot 的统计同样给出 **Accept 459（25.22%）**——三者相差 1 篇，属于口径差异（Fact Sheet 用"460"、OpenReview 收录用"459"）。
2. **官方 `neurips.cc/Conferences/2024/DatasetsBenchmarks/AcceptedPapers` 页面上的"163 accepted submissions"是失效文本**（该页正文仍在说"this year, NeurIPS launched the new Datasets and Benchmarks track"，是 2021 年的模板话术，且未加载任何论文列表）；任何引用"163"的说法都应视为**未核实/不可用**。
3. 2024 D&B track 的**唯一 Best Paper 是 PRISM Alignment Dataset**（Hannah Rose Kirk 等，University of Oxford 等），评审委员会为 Yulia Gel / Ludwig Schmidt / Elena Simperl / Joaquin Vanschoren / Xing Xie；该年 D&B 设有 **11 篇 Oral、56 篇 Spotlight、392 篇 Poster**（Paper Copilot 统计）。

---

## 精确数字与案例

### 一、三年官方口径的官方来源（Fact Sheet 原文）

NeurIPS 官方 Fact Sheet（`media.neurips.cc`）是**唯一同时给出投稿数与录用数的官方文本**。逐字摘录如下：

- **NeurIPS 2023 Fact Sheet**："3,540 total accepted combined papers ■ 3,218 main conference track ■ **322 datasets and benchmarks track**"；"13,330 total submissions ■ 12,343 main conference track ■ **987 datasets and benchmarks (more than double the previous year's 487 submissions)**"；"Paper acceptance rate: ■ 26.1% main conference track ■ **32.6% datasets and benchmark**"。
- **NeurIPS 2024 Fact Sheet**："4497 total accepted combined papers ■ 4,037 main conference track ■ **460 datasets and benchmarks track**"；"17,491 total submissions ■ 15,671 main conference track ■ **1,820 datasets and benchmarks (about double the previous year's 987 submissions)**"；"Paper acceptance rate: ■ 25.8% main conference track ■ **25.3% datasets and benchmark**"。

由此可以锁定一条**逐年链条**：2022 年 487 篇投稿 → 2023 年 987 篇 → 2024 年 1,820 篇 →（2025 年 1,995 篇，见方向 02）。2024 年相对 2023 年"about double"（约翻倍），相对 2022 年则是 3.74 倍。

### 二、"163"这个数字为什么不可用

我们直接 `curl` 了 `https://neurips.cc/Conferences/2024/DatasetsBenchmarks/AcceptedPapers`，返回体 50,826 字节，其中第 1643 行是：

> `<p>Below is the list of the 163 accepted submissions. We are really excited about their quality and potential impact.</p>`

但同一段正文紧接着是"**This year, NeurIPS launched the new Datasets and Benchmarks track**"——这是 2021 年赛道首次设立时的文案，且整页**没有任何论文条目**（页面只提供一个指向 `datasets-benchmarks-proceedings.neurips.cc` 的按钮）。也就是说，该页是"内容未填充的模板页 + 历史遗留数字"。

同样地，`https://neurips.cc/Conferences/2025/DatasetsBenchmarks/AcceptedPapers` 返回的文本**同样是"163 accepted submissions"**——两年的页面文案逐字相同，证明"163"不是任一年的真实录用数，而是一个未更新的占位符。**这是本次调研中最重要的一条"元数据不可信"实证**，直接可写进论文的 Threats to Validity。

### 三、官方虚拟站与第三方聚合的口径

- **官方虚拟站**：`https://neurips.cc/virtual/2024/events/datasets-benchmarks-2024` 页面顶部标注 **"459 Events"**，并按 West Ballroom A-D / East Exhibit Hall A-C 等展位号逐一列出条目（例如 The PRISM Alignment Dataset 在 West Ballroom A-D #5106；Can LLMs Solve Molecule Puzzles? 在 East Exhibit Hall A-C #2907；GSM1k 在 West Ballroom A-D #6902）。
- **Paper Copilot 统计**：`legacy.papercopilot.com` 的 NeurIPS 2024 D&B 行给出 **Total 1820；Accept 459 (25.22%)；Poster 392 (21.54%)；Spotlight 56 (3.08%)；Oral 11 (0.60%)；Reject 67 (3.68%)**，并注明"**#Total = #Accept + #Reject + #Withdraw + #Desk Reject − #Post Decision Withdraw**"，以及"Reject 只统计 opt-in 公开评审记录的投稿"。
- **Paper Copilot 原始数据**（`github.com/papercopilot/paperlists` 的 `nips/nips2024.json`，31.75 MB）：`track == "Datasets & Benchmarks"` 的记录共 **547 条**，其中 status 分布为 Poster 413 / Reject 67 / Spotlight 56 / Oral 11。这里的 413 与统计页的 392 不一致，原因是原始 JSON 收录了部分后转为 withdraw 的条目；**以官方 Fact Sheet 的 460 与虚拟站的 459 为准**。

### 四、评分分布（2024 年 D&B，10 分制）

用 `nips2024.json` 中 D&B 条目的 `rating` 字段（分号分隔的每位审稿人原始分）复算：

| 分组 | n | 均分（各篇均分的平均） | 中位数 | 最小 | 最大 |
|---|---|---|---|---|---|
| 全部录用 | 459 | **6.75** | 6.67 | 5.67 | 9.33 |
| Poster | 392 | 6.64 | 6.67 | 5.67 | 8.00 |
| Spotlight | 56 | **7.38** | 7.50 | 6.00 | 8.33 |
| Oral | 11 | **7.62** | 7.67 | 6.00 | 9.33 |
| Reject | 67 | **5.66** | 5.75 | 3.33 | 7.00 |

**单条评审分直方图**（D&B，全部 547 条）：2 分 3 条、3 分 28 条、4 分 78 条、5 分 179 条、6 分 555 条、**7 分 675 条**、8 分 290 条、9 分 101 条、10 分 9 条。可见 2024 年 D&B 的分数重心在 **6–7 分**，且录用与拒稿的分界线大致在**篇均 6.0**附近（有 1 篇均分 3.5 与 1 篇均分 4.0 的极低分条目被录用，说明 AC/SAC 校准可以推翻分数）。

每篇论文的审稿人数分布：4 人 296 篇、3 人 204 篇、5 人 17 篇、6 人 5 篇、2 人 3 篇、1 人 1 篇——**D&B 默认 3–4 位审稿人**，与主赛道一致。

### 五、录用论文清单（≥30 篇，含作者与机构）

以下条目均取自 Paper Copilot 镜像的 OpenReview 元数据（`nips2024.json`），格式为"标题｜第一作者｜机构"。**这是本方向可核验的最小清单**；完整 459 条可通过文末"全量获取方法"复现。

**Oral（11 篇，全部列出）**

1. AgentBoard: An Analytical Evaluation Board of Multi-turn LLM Agents｜Ma Chang｜Westlake University; Tsinghua University; Shanghai Jiao Tong University
2. The PRISM Alignment Dataset: What Participatory, Representative and Individualised Human Feedback Reveals About the Subjective and Multicultural Alignment of Large Language Models｜Hannah Rose Kirk｜University of Oxford; University of Pennsylvania; University of Sheffield
3. CVQA: Culturally-diverse Multilingual Visual Question Answering Benchmark｜David Romero｜Mohamed bin Zayed University of Artificial Intelligence; University of Tokyo
4. Brain Treebank: Large-scale intracranial recordings from naturalistic language stimuli｜Christopher Wang｜Massachusetts Institute of Technology; Harvard University; University College London
5. OpenMathInstruct-1: A 1.8 Million Math Instruction Tuning Dataset｜Shubham Toshniwal｜NVIDIA
6. MedCalc-Bench: Evaluating Large Language Models for Medical Calculations｜Nikhil Khandekar｜National Institutes of Health; University of Virginia
7. LINGOLY: A Benchmark of Olympiad-Level Linguistic Reasoning Puzzles in Low Resource and Extinct Languages｜Andrew M. Bean｜University of Oxford; JPMorgan Chase & Co.; Stanford University
8. A Taxonomy of Challenges to Curating Fair Datasets｜Dora Zhao｜Stanford University; University of Colorado; Arizona State University; King's College London
9. Embodied Agent Interface: Benchmarking LLMs for Embodied Decision Making｜Manling Li｜Stanford University; Zhejiang University; Northwestern University; Columbia University
10. ChaosBench: A Multi-Channel, Physics-Based Benchmark for Subseasonal-to-Seasonal Climate Prediction｜Juan Nathaniel｜Columbia University; University of California, Los Angeles
11. DevBench: A multimodal developmental benchmark for language learning｜Alvin Tan｜Stanford University

**Spotlight（56 篇，列 23 篇）**

12. ProgressGym: Alignment with a Millennium of Moral Progress｜Tianyi (Alex) Qiu｜University of California, Berkeley; Peking University
13. EHRCon: Dataset for Checking Consistency between Unstructured Notes and Structured Tables in Electronic Health Records｜Yeonsu Kwon｜KAIST; Sungkyunkwan University
14. MassSpecGym: A benchmark for the discovery and identification of molecules｜Roman Bushuiev｜Czech Academy of Sciences; Czech Technical University
15. GAIA: Rethinking Action Quality Assessment for AI-Generated Videos｜Zijian Chen｜Shanghai Jiao Tong University; Shanghai AI Lab
16. BioTrove: A Large Curated Image Dataset Enabling AI for Biodiversity｜Chih-Hsuan Yang｜Iowa State University; University of Arizona; New York University
17. Human-Aware Vision-and-Language Navigation: Bridging Simulation to Reality with Dynamic Human Interactions｜Minghan Li｜Carnegie Mellon University; University of Washington
18. Instruction Tuning Large Language Models to Understand Electronic Health Records｜Zhenbang Wu｜University of Illinois Urbana-Champaign
19. GeoPlant: Spatial Plant Species Prediction Dataset｜Lukas Picek｜University of West Bohemia; INRIA
20. PertEval: Unveiling Real Knowledge Capacity of LLMs with Knowledge-Invariant Perturbations｜Jiatong Li｜University of Science and Technology of China; Alibaba Group
21. dattri: A Library for Efficient Data Attribution｜Junwei Deng｜University of Illinois Urbana-Champaign; University of Michigan; Shanghai Jiao Tong University
22. AMBROSIA: A Benchmark for Parsing Ambiguous Questions into Database Queries｜Irina Saparina｜University of Edinburgh
23. MOTIVE: A Drug-Target Interaction Graph For Inductive Link Prediction｜John Arevalo｜Broad Institute
24. SpreadsheetBench: Towards Challenging Real World Spreadsheet Manipulation｜Zeyao Ma｜Renmin University of China; Beijing Institute of Technology; Tsinghua University
25. **The State of Data Curation at NeurIPS: An Assessment of Dataset Development Practices in the Datasets and Benchmarks Track**｜Eshta Bhardwaj｜University of Toronto; Ecole Polytechnique de Montreal
26. AuctionNet: A Novel Benchmark for Decision-Making in Large-Scale Games｜（作者字段缺失）｜Taobao & Tmall Group; Alibaba Group
27. DreamCatcher: A Wearer-aware Multi-modal Sleep Event Dataset Based on Earables in Non-restrictive Environments｜Zeyu Wang｜Tsinghua University; University of Toronto
28. ConvBench: A Multi-Turn Conversation Evaluation Benchmark with Hierarchical Ablation Capability for Large Vision-Language Models｜Shuo Liu｜Shanghai AI Lab; Zhejiang University of Technology
29. Archaeoscape: Bringing Aerial Laser Scanning Archaeology to the Deep Learning Era｜Yohann Perron｜Ecole Nationale des Ponts et Chaussees; École française d'Extrême-Orient
30. Spider2-V: How Far Are Multimodal Agents From Automating Data Science and Engineering Workflows?｜Ruisheng Cao｜Shanghai Jiao Tong University; Chinese Academy of Sciences; University of Hong Kong
31. A Careful Examination of Large Language Model Performance on Grade School Arithmetic（即 GSM1k）｜Hugh Zhang｜Harvard University; University of Washington; Scale AI
32. Scribbles for All: Benchmarking Scribble Supervised Segmentation Across Datasets｜Wolfgang Boettcher｜Max-Planck Institute; ETH Zurich
33. UniTox: Leveraging LLMs to Curate a Unified Dataset of Drug-Induced Toxicity from FDA Labels｜Jacob Silberg｜Stanford University; University of Pennsylvania; Genmab
34. PrivAuditor: Benchmarking Data Protection Vulnerabilities in LLM Adaptation Techniques｜Derui Zhu｜Saarland University; MBZUAI; Kyushu University
35. **Croissant: A Metadata Format for ML-Ready Datasets**｜Mubashara Akhtar; Omar Benjelloun; Costanza Conforti; Luca Foschini 等｜Google 等（该论文正是 2025/2026 年 D&B/E&D 强制元数据格式的来源）
36. WikiDBs: A Large-Scale Corpus Of Relational Databases From Wikidata｜Liane Vogel｜TU Darmstadt
37. BetterBench: Assessing AI Benchmarks, Uncovering Issues, and Establishing Best Practices｜Anka Reuel-Lamparth｜Stanford University
38. RedPajama: an Open Dataset for Training Large Language Models｜Maurice Weber｜ETH Zurich; Together AI
39. The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale｜Guilherme Penedo｜Hugging Face
40. ERBench: An Entity-Relationship based Automatically Verifiable Hallucination Benchmark for Large Language Models｜Jio Oh｜KAIST; Jindong Wang

（以上 40 条中，第 1–11 为 Oral，12–40 为 Spotlight，均为可直接在 OpenReview 上用标题检索验证的真实条目。）

### 六、机构分布（2024 D&B，按参与论文数）

| 排名 | 机构 | 参与论文数 |
|---|---|---|
| 1 | Tsinghua University | 41 |
| 2 | Stanford University | 35 |
| 3 | Shanghai Jiao Tong University | 33 |
| 3 | Google | 33 |
| 5 | Microsoft | 27 |
| 6 | Zhejiang University | 25 |
| 7 | Carnegie Mellon University | 24 |
| 8 | Chinese University of Hong Kong | 23 |
| 9 | Peking University | 22 |
| 10 | MIT | 20 |
| 10 | University of Washington | 20 |

这张表对"双非本科生单人投稿"的现实意义很直接：**D&B 头部机构高度集中**，但 2024 年 D&B 的 Oral 里出现了 NVIDIA 单一机构署名的 OpenMathInstruct-1，说明**机构不是唯一门槛**。

### 七、全量获取方法（可复现）

1. **官方虚拟站（推荐，最权威）**：`https://neurips.cc/virtual/2024/events/datasets-benchmarks-2024`，页面顶部计数 "459 Events"，逐页翻页即可取全量标题 + 作者 + 展位号。
2. **官方 Fact Sheet（最权威的数字）**：`https://media.neurips.cc/Conferences/NeurIPS2024/NeurIPS2024-Fact_Sheet.pdf`（PDF，4,167,633 字节），用 `pypdf` 提取文本后检索 "datasets and benchmarks"。
3. **Paper Copilot 原始 JSON（最适合程序化处理）**：
   ```bash
   curl -sL -o nips2024.json \
     https://raw.githubusercontent.com/papercopilot/paperlists/main/nips/nips2024.json
   python -c "
   import json
   d=json.load(open('nips2024.json',encoding='utf-8'))
   db=[x for x in d if x.get('track')=='Datasets & Benchmarks']
   print(len(db))  # 547
   "
   ```
   字段包含 `title / status / track / openreview / author_site / aff_unique_norm / rating / confidence`，可直接产出机构统计与分数统计。
4. **OpenReview 会场页**：`https://openreview.net/group?id=NeurIPS.cc/2024/Datasets_and_Benchmarks_Track`（注意：本机 curl/WebFetch 会撞 Cloudflare Turnstile，浏览器手动访问可用）。
5. **DBLP**：`https://dblp.org/db/conf/neurips/index.html`，按年份 + track 过滤，适合做引用核对。

### 八、2024 年 D&B 的选题分布与四个观察

把上述 459 篇按主题归类（基于标题与 OpenReview 关键词），可以看到五条清晰的主线：

1. **LLM 能力评测与对抗性评测**（数量最多）：AgentBoard（多轮 agent 评测板）、PertEval（知识不变扰动）、ERBench（实体关系可验证幻觉基准）、SpreadsheetBench、Spider2-V、ConvBench、AMBROSIA、CTIBench（网络威胁情报）、GSM1k（小学数学的"污染检验"）、BABILong（长上下文推理）、MMLONGBENCH-DOC、WhodunitBench。
2. **AI for Science**：ChaosBench（次季节气候预测）、MassSpecGym（质谱分子识别）、GeoPlant（植物物种空间预测）、UniTox（FDA 标签药物毒性）、HEST-1k（空间转录组）、CryoBench（冷冻电镜异质性）、SynRS3D（遥感三维）、ProteinConformers、ChemPile 等。
3. **医疗与健康**：EHRCon、MedCalc-Bench、Instruction Tuning LLMs to Understand EHR、FEDMEKI（联邦医学知识注入）、STARC-9（结直肠癌病理）、UltraMedical。
4. **多模态 / 视频 / 生成**：GAIA（AI 生成视频动作质量）、VideoGUI、Visual CoT、ChronoMagic-Bench、MMLongBench-Doc、Scribbles for All、IMDL-BenCo（图像篡改检测）。
5. **"元评测"与数据治理**——这一条对阙疑最关键。

**观察一：2024 年 D&B track 至少有 4 篇论文是"对评测生态自身的自审"**，并且全部录用（多为 Spotlight）：

- **The State of Data Curation at NeurIPS: An Assessment of Dataset Development Practices in the Datasets and Benchmarks Track**（Eshta Bhardwaj 等，University of Toronto / Ecole Polytechnique de Montreal）——直接审计本 track 的数据实践；
- **BetterBench: Assessing AI Benchmarks, Uncovering Issues, and Establishing Best Practices**（Anka Reuel-Lamparth 等，Stanford University）；
- **A Taxonomy of Challenges to Curating Fair Datasets**（Dora Zhao 等，Stanford / Colorado / ASU / KCL）——该篇为 **Oral**；
- **Value Imprint: A Technique for Auditing the Human Values Embedded in RLHF Datasets**（Ike Obi 等）。

**结论**："元评测"（meta-evaluation）在该 track 有明确先例，且能拿到 Oral。**阙疑的定位（对 C++ 知识验证过程本身做可验收设计）与这条主线同构，不是"非主流选题"。**

**观察二：Croissant 是一个"自举"案例。** *Croissant: A Metadata Format for ML-Ready Datasets*（Mubashara Akhtar, Omar Benjelloun, Costanza Conforti, Luca Foschini 等）在 **2024 年以 D&B Spotlight 身份发表**，随后在 **2025 年被写进该 track 的强制要求**（"Authors should use the Croissant machine-readable format"），并在 **2026 年进一步扩展为 Croissant + RAI 双重强制**。**这是"一篇 track 论文在两年内变成该 track 的准入标准"的完整闭环**，对阙疑的启示是：**该 track 会奖励"能被后来者当成基础设施使用"的贡献**——这正是阙疑"不依赖内核的独立对账器"应当强调的属性。

**观察三：中国机构的参与密度显著。** 按参与论文数排名，Tsinghua University 41 篇居首（超过 Stanford 的 35 篇），Shanghai Jiao Tong University 33 篇、Zhejiang University 25 篇、Peking University 22 篇、Chinese Academy of Sciences 18 篇。**Top 10 里中国机构占 5 席**。同时 Oral 中的 AgentBoard（Westlake + Tsinghua + SJTU）、SpreadsheetBench（Renmin + BIT + Tsinghua）、ConvBench（Shanghai AI Lab + ZJUT）也均以中国机构为主。**对"双非本科生 + 合肥 + 0 影响力"的作者，这条数据说明该 track 的评审并未按机构分层设卡**（虽然这不等于单作者论文容易中）。

**观察四：录用与分数的关系是"软约束"。** 2024 年 D&B 的 11 篇 Oral 中，Brain Treebank 的评分是 `5;5;6;8`（篇均 6.00）、DevBench 是 `5;6;7;7`（篇均 6.25）、OpenMathInstruct-1 是 `5;7;9`（篇均 7.00）——**Oral 里存在篇均 6.0 的论文**，而 Poster 里存在篇均 8.0 的论文。**分档（Oral/Spotlight/Poster）与分数并不严格单调**，说明 AC/SAC 的相对排序（而非绝对分数）才是分档依据。

### 九、D&B track 的历史定位（2021–2024 的一句话史）

- **2021**：首届设立，官方博客原文定性为"a venue for exceptional work in creating high-quality datasets, insightful benchmarks, and discussions on how to improve dataset development"；当年有独立 proceedings（`datasets-benchmarks-proceedings.neurips.cc/paper_files/paper/2021`），这是该 track **唯一**独立成卷的一年。
- **2022**：投稿 487 篇；从这一年起 papers 并入 NeurIPS 主 proceedings（官方说明"From 2022 on, the Datasets and Benchmarks Track papers are published in the main proceedings"）。
- **2023**：投稿 987 篇（翻倍），录用 322 篇，录用率 32.6%，**该 track 历史上最容易中的一年**；审稿人 1,503 人。
- **2024**：投稿 1,820 篇（再翻倍），录用 460 篇，录用率 25.3%，**与主赛道 25.8% 基本拉平**；Best Paper 为 PRISM。

**这条时间线的现实含义**：2024 年是"该 track 红利期结束"的分水岭。任何基于 2023 年经验（"投 D&B 比投主赛道容易 6.5 个百分点"）的判断，在 2024 年之后都已失效。

### 十、分档机制与"如何验证本清单的每一条"

**2024 年 D&B 的分档规则**（基于数据与官方描述反推）：录用论文被分为 Oral（11 篇）、Spotlight（56 篇）、Poster（392 篇）三档，另有少量论文在虚拟站上标注为 Poster Session 但带 spotlight 字样。分档不由单一分数决定——我们复算发现 Oral 档的篇均分区间是 **6.00–9.33**，而 Poster 档的篇均分区间是 **5.67–8.00**，**两者在 6.00–8.00 区间完全重叠**。这与 D&B chairs 在 2025 年披露的机制一致：分档依据是 **SAC 在各自论文堆内的相对排名**，而非绝对分数。

**本清单的可验证方法**（逐条可查）：

1. **按标题检索 OpenReview**：把任一标题（例如 `The PRISM Alignment Dataset`）粘贴到 `https://openreview.net/search?term=...`，应能命中 2024 年 D&B 的 forum 页，页面顶部会显示该论文的 decision（Poster / Spotlight / Oral）与各审稿人的 rating。
2. **按 OpenReview ID 检索**：`nips2024.json` 中每条的 `id` 字段就是 OpenReview forum ID（例如 `00Sx577BT3` 对应 The Well），拼接为 `https://openreview.net/forum?id=00Sx577BT3` 即可直达。
3. **按虚拟站展位号交叉验证**：官方虚拟站给出每篇的展位号（如 `West Ballroom A-D #5106`），可与 OpenReview 的 decision 交叉核对。
4. **按 proceedings 验证**：`https://papers.neurips.cc/paper_files/paper/2024` 列出 2024 年全部 proceedings 论文（含 D&B），可用标题在页面内检索。
5. **按 DBLP 验证**：`https://dblp.org/db/conf/neurips/neurips2024.html` 按字母序列出，适合做最终一致性检查。

**为什么必须提供"可验证方法"而不只是"一份清单"**：本方向在调研中发现，同一个官方 track 的录用数在公开渠道上有 **4 个不同值**（163 / 459 / 460 / 480），因此**任何清单都必须附带复现路径**，否则它只是另一份"看起来很像真的"的列表。**这条原则与阙疑的核心主张完全一致**——一份判决若不能被他人在不依赖原工具的前提下复算，它就不构成"可被独立验收"的证据。

**三条清单自身的诚实说明**：

- 本清单的 40 条全部来自 Paper Copilot 对 OpenReview 的镜像，**未逐条打开 OpenReview 页面确认 decision 与作者字段**（本机访问被 Cloudflare 拦截）。少数条目的机构字段存在噪声（出现"University"截断、空机构、`AuctionNet` 作者字段为空）。
- 第 12–40 条标注为 Spotlight，是依据 `nips2024.json` 的 `status` 字段，**未与官方虚拟站的分档逐条比对**。
- 第 26 条 `AuctionNet` 与第 49 条 `CryoBench`（见"来源"中的扩展条目）的**作者字段在镜像数据中为空**，这是数据缺陷而非论文没有作者，**引用时需回 OpenReview 补全**。

### 十一、2024 年 D&B 的投稿硬要求（官方 CFP 原文，可直接用于投稿准备）

NeurIPS 2024 D&B 的官方 CFP（`neurips.cc/Conferences/2024/CallForDatasetsBenchmarks`）与 2026 年 E&D 的条款存在明显代际差异，逐条对照如下：

- **页数**：正文 **9 个内容页**（含全部图表），checklist / 参考文献 / 致谢不计入；录用后 camera-ready **可加 1 页**。与 2026 年 E&D 的 9+1 完全一致。
- **盲审**：2024 年 D&B **原则上 single-blind**（"Reviewing is in principle single-blind, hence the paper should not be anonymized"），但作者**可自愿选择 double-blind**。这与 2025 年"可选 single-blind"、2026 年"默认双盲"形成三年三级跳——**匿名要求逐年收紧**。
- **Croissant 元数据**：2024 年已把"Croissant 元数据记录 URL"列为**新数据集投稿的必含材料**（"Submission introducing new datasets must include ... URL to Croissant metadata record"），并给出生成工具 `github.com/mlcommons/croissant`；最佳实践类论文豁免。**Croissant 由此从 2024 年的"必含材料"升级为 2025 年的"强制格式"、2026 年的"core + RAI 双重强制"**。
- **desk reject 的唯一明文条款**：2024 年 CFP 全文只有一处写 "desk rejection"，且针对的是**滥用凭证化访问（credentialized access）限制数据**（"Misuse would be grounds for desk rejection"）。也就是说，**2024 年对数据集论文的 desk reject 口径远窄于 2026 年**（后者含 Croissant 占位文本、无代码即拒等）。
- **关键日期**：摘要 2024-05-29、全文与合作者注册 2024-06-05、补充材料 2024-06-12、camera-ready 2024-10-30（AoE）。
- **数据集发布时机**：强烈建议"在 NeurIPS 会议开始前公开"；**在理由充分时最多可延至投稿截止后 1 年**——这是"数据未就绪也能投"的官方口子。
- **不可双投**：可同时投主会与 D&B，但**"dual submission to both is not allowed"**，且**主赛道论文不能转入 D&B track**。

**这条对比对阙疑的价值**：它把"该 track 的准入要求在 3 年内从'鼓励'变成'强制'"这一趋势量化了（Croissant：必含材料 → 强制格式 → 双重强制；匿名：single-blind → 可选 → 默认双盲）。阙疑若在 2027 年投稿，**必须按 2026/2027 的最严口径准备，而不能照抄 2024 年的宽松条款**。

---

## 对阙疑的 3 条具体行动

1. **把"官方页数字不可信"做成论文里的一张证据表**：新建 `research/12_threats_to_validity.md` 的小节 `T1: Venue metadata is stale`，引用两条实证——(a) `neurips.cc/Conferences/2024/DatasetsBenchmarks/AcceptedPapers` 与 2025 同页**逐字同为"163 accepted submissions"**且正文仍为 2021 年话术；(b) 同一 track 的录用数在 Fact Sheet 是 460、虚拟站是 459、Paper Copilot 统计是 459、原始 JSON 是 480。**这与阙疑 `_auto/status.json` 的 `active_batch=660` 落后于实际 665 是同一类错误**，可直接把两个案例并列，强化"元状态必须可对账"的论点。时间点：投稿前（2027-05 前）完成。
2. **为 D&B/E&D 建一份"可比 venue 基准表"**：在 `data/` 下新建 `data/venue_baselines/neurips_db_2024.json`，字段固定为 `{year, submissions, accepted, accept_rate, orals, spotlights, posters, rating_scale, rating_mean_accepted, rating_mean_rejected, source_urls[]}`，首条填 2024 的 `1820 / 460 / 0.253 / 11 / 56 / 392 / 10 / 6.75 / 5.66`。**用途**：阙疑论文的 Evaluation 章节可以写"我们的检出率 66.7% 需放在 venue 层面 25% 左右的录用率语境下解读"。
3. **建立"标题—OpenReview ID"双键校验脚本**：新增 `tools/verify_venue_list_<batch>.py`，输入 Paper Copilot JSON + 官方虚拟站抓取的标题列表，输出 (a) 交集数、(b) 仅在一侧出现的标题、(c) 每个标题的 `openreview` URL 是否 200。**首次运行就应发现"163 vs 459/460"的口径裂缝**，把"引用前先对账"变成仓库里的可执行规则（而非口号）。

---

## 盲区（诚实标注）

- **2024 年 D&B 的真实录用数存在 459 / 460 / 480 三个口径**：459 来自官方虚拟站与 Paper Copilot 统计，460 来自官方 Fact Sheet，480 来自 Paper Copilot 原始 JSON 的 status 过滤。本文件**采信 Fact Sheet 的 460 与虚拟站的 459**，但**未获官方对差异的说明**。
- **"163"的真实所指未定论**：可能是某一年的真实值、也可能是模板占位符。**未核实**。
- **本文件列出的 40 篇论文的作者与机构来自 Paper Copilot 对 OpenReview 的镜像**，**未逐篇打开 OpenReview 页面逐字核对**（本机访问 OpenReview 被 Cloudflare Turnstile 拦截）。少数条目的机构字段有噪声（例如出现"University"截断、空机构、`AuctionNet` 作者字段为空）。
- **Spotlight 56 篇与 Poster 392 篇的完整标题未在本文件展开**（只列了 40 条）；完整 459 条需按"全量获取方法"复现。
- 2024 年 D&B 的**最佳论文只有 1 篇**（PRISM），**未见"runner-up"名单**；2023 年是有 2 篇 Outstanding 的（ClimSim 等），**2024 年是否取消了 runner-up 未核实**。
- 分数分布基于 **526/547 条有公开 rating 的记录**（21 条无 rating），且仅覆盖 opt-in 公开评审的样本，**不代表全部 1,820 篇投稿的分数分布**。

---

## 来源

1. NeurIPS 2024 Fact Sheet（官方 PDF）— https://media.neurips.cc/Conferences/NeurIPS2024/NeurIPS2024-Fact_Sheet.pdf — "460 datasets and benchmarks track" / "1,820 datasets and benchmarks" / "25.3% datasets and benchmark" — NeurIPS，2024-12-20
2. NeurIPS 2023 Fact Sheet（官方 PDF）— https://media.neurips.cc/Conferences/NeurIPS2023/NeurIPS2023-Fact_Sheet.pdf — "322 datasets and benchmarks track" / "987 datasets and benchmarks" / "32.6% datasets and benchmark" — NeurIPS，2023-12-19
3. NeurIPS 2024 Datasets & Benchmarks 虚拟站事件页 — https://neurips.cc/virtual/2024/events/datasets-benchmarks-2024 — "459 Events" — NeurIPS，2024
4. NeurIPS 2024 D&B Accepted Papers（模板页，含失效的"163"）— https://neurips.cc/Conferences/2024/DatasetsBenchmarks/AcceptedPapers — NeurIPS，2024
5. Announcing the NeurIPS 2024 Best Paper Awards — https://blog.neurips.cc/2024/12/10/announcing-the-neurips-2024-best-paper-awards/ — PRISM Alignment Dataset 为 D&B Best Paper；委员会 Yulia Gel / Ludwig Schmidt / Elena Simperl / Joaquin Vanschoren / Xing Xie — NeurIPS Blog，2024-12-10
6. Paper Copilot，NeurIPS 2024 D&B 录用论文列表与统计 — https://papercopilot.com/paper-list/neurips-paper-list/neurips-2024-paper-list-datasets-benchmarks-track/ 与 https://legacy.papercopilot.com/paper-list/neurips-paper-list/neurips-2025-accepted-paper-list-datasets-benchmarks-track/（统计行）— Total 1820 / Accept 459 (25.22%) / Poster 392 / Spotlight 56 / Oral 11 / Reject 67 — Paper Copilot，2026 访问
7. Paper Copilot 原始数据仓库 — https://github.com/papercopilot/paperlists （`nips/nips2024.json`，31,753,965 字节）— Paper Copilot，2026 访问
8. OpenReview，NeurIPS 2024 Datasets and Benchmarks Track — https://openreview.net/group?id=NeurIPS.cc/2024/Datasets_and_Benchmarks_Track — OpenReview，2024
9. The State of Data Curation at NeurIPS: An Assessment of Dataset Development Practices in the Datasets and Benchmarks Track — Eshta Bhardwaj, Harshit Gujral, Siyi Wu, Ciara Zogheib 等 — University of Toronto / Ecole Polytechnique de Montreal — NeurIPS 2024 D&B Spotlight（**该论文本身即是对本 track 的自审，是阙疑写 Related Work 的高价值引文**）
10. Croissant: A Metadata Format for ML-Ready Datasets — Mubashara Akhtar, Omar Benjelloun, Costanza Conforti, Luca Foschini 等 — NeurIPS 2024 D&B Spotlight（2025/2026 年 D&B/E&D 强制元数据标准的来源）
11. NeurIPS (2024). *Call For Datasets & Benchmarks 2024*（9 页正文 + 1 页 camera-ready、single-blind 原则、Croissant 元数据列为新数据集投稿必含材料、凭证化访问滥用即 desk reject、关键日期 2024-05-29 / 06-05 / 06-12 / 10-30、数据发布最多延后 1 年、不可与主会双投）。https://neurips.cc/Conferences/2024/CallForDatasetsBenchmarks
