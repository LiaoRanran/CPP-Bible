# 方向 21：Method section 怎么写

## 核心结论

1. **E&D / dataset 类论文的 Method 不是"解释给人看"，而是"复算给人跑"**——NeurIPS 2026 E&D FAQ 明确写死：数据集与代码必须与正文在 **2026-05-06 (AoE)** 同一天提交，且"数据集和代码在 ED 赛道不被视为补充材料"；Method 的可验收性由此从"写作问题"变成"提交物问题"。
2. **Method 的每一节都应能被 checklist 的某一项反向锚定**：NeurIPS Paper Checklist 共 **16 项**，其中第 4（实验可复现性）、5（代码/数据开放 + "精确命令与环境"）、6（实验设置）、7（误差棒与统计显著性）、8（算力资源）五项直接约束 Method 的写法；未附 checklist 的投稿会被 desk reject。
3. **provenance 不是自创概念，而是已有成熟模板的拼装**：Datasheets for Datasets（**7 节**）负责"动机—构成—采集—清洗—用途—分发—维护"，Model Cards 负责"预期用途 + 指标分解"，Croissant 负责"机器可读元数据"；阙疑的 append-only 哈希链 + Merkle checkpoint + 独立对账器应当写成这三者的混合体，而不是另造一套私有术语。

---

## 精确数字与案例

### 1. 赛道规则：Method 的边界由提交规则决定，不由写作偏好决定

NeurIPS 2026 Evaluations & Datasets（ED）赛道 FAQ（2026-04-07 更新）给出的可量化约束如下：

| 项目 | 精确要求 |
|---|---|
| 全文投稿截止 | **2026-05-06（AoE）**，含所有必需材料、数据集与代码的最终形式 |
| 数据/代码提交时机 | 必须与全文**同时**提交；"数据集和代码在 ED 赛道不被视为补充材料" |
| 大文件 | **> 4GB** 的数据集须提供较小的数据样本，并说明样本创建方式 |
| 数据集公开 | 须在 camera-ready 截止前公开，否则可能被移出会议与论文集 |
| LaTeX 模板 | 与主赛道一致，双盲默认 `\usepackage[eandd]{neurips_2026}` |
| 匿名化 | 默认双盲；数据集可用匿名账户 + Croissant 文件一并匿名；代码可用 `anonymous.4open.science` |
| 单盲例外 | 仅限数据集投稿，且仅在"数据收集会暴露机构身份"或"伦理原因需门控"时可选 |
| 门控访问 | 仅在为公共利益必要时允许，且须同时满足三条：对**大部分公众开放**、提供**快速响应与数据访问**、保证**多年持续维护**（范例：PhysioNet Credentialing） |
| 自动化检查 | 投稿截止后执行 **automated verification checks** |

对阙疑的直接含义：**holdout 的 30 个 seed 属于"私有留出集"**。FAQ 明确允许保留不公开的 hold-out（用于防污染），但"须在论文中说明"，且"论文主要贡献应为公开发布的部分，且该部分须符合托管指南"。也就是说，阙疑必须在 Method 里显式写一句"`data/holdout/holdout.json` 为私有 hold-out，理由为防污染；公开部分为 `data/external_corpus/external_corpus_665.json`（40 条）与 `data/defect_fixtures/defects.json`（15 条）"——否则会被判为不符合托管指南。

NeurIPS 2025 D&B 赛道的 Call for Papers 则把"必须提交"写得更硬：该赛道相对主赛道只有**三点**差异——(a) 允许 single-blind，(b) **强制提交数据集与基准代码**，(c) 收窄到 DMLR（data-centric machine learning research）范围。其日期锚点为：摘要 2025-05-11 AoE、全文 2025-05-15 AoE、技术附录 2025-05-22 AoE、通知 2025-09-18 AoE、camera-ready 2025-10-23 AoE。托管要求写得很具体：新数据集应托管在 **Dataverse / Kaggle / Hugging Face / OpenML** 之一（或自建站点），代码须以可执行形式托管在 GitHub/Bitbucket 等平台，且**必须对全体审稿人、AC、SAC 在投稿时刻即可访问**——"Non-compliance justifies the desk rejection of the paper."（不合规即构成 desk rejection 理由）。

### 2. 录取规模：这条赛道的竞争强度

| 年份 | D&B 赛道提交数 | 接收数 | 备注 |
|---|---|---|---|
| 2023 | **985** | 未核实 | Paper Copilot 统计行 |
| 2024 | **1820** | **163**（官方页面） | 接收率 ≈ **8.96%**（163/1820） |
| 2025 | 591（Paper Copilot，仅统计选择公开评分的记录） | **163**（官方页面） | 该行统计口径存疑，见盲区 |

2024 年 D&B 的评审分数分布（Paper Copilot）：全部提交 min 3.30 / max 9.30 / 平均 **6.58** / 标准差 **0.6745**；Accept 层平均 **6.72**（std 0.5439，区间 5.60–9.30）；Reject 层平均 **5.64**（std 0.71，区间 3.30–7.00）。也就是说，**接收与拒稿的平均分只差 1.08 分**。2025 年该行记录平均分 **4.55**（区间 2.60–5.70）。这些数字说明：Method 的清晰度与可复算性往往是 6.5 分与 5.6 分之间那条线的实际决定因素。

### 3. Paper Checklist：Method 的五根锚

NeurIPS 官方 Paper Checklist（`neurips.cc/public/guides/PaperChecklist`）共 **16 项**，与 Method 强相关的五项原文要点如下（保留英文原句以便直接对照）：

- **第 4 项 Experimental Result Reproducibility**：核心问句是 "If the contribution is a dataset or model, what steps did you take to make your results reproducible or verifiable?" 官方给出四种可接受路径：完整描述架构 / 让复现者能用同数据集复刻 / 提供模型访问 / 详细复刻指令 + hosted model + checkpoint。**"While NeurIPS does not require releasing code, we do require all submissions to provide some reasonable avenue for reproducibility."**
- **第 5 项 Open Access to Data and Code**："The instructions should contain the **exact command and environment** needed to run to reproduce the results."（原文强调）。另有一句对阙疑特别重要：**"Papers cannot be rejected simply for not including code, unless this is central to the contribution (e.g., for a new open-source benchmark)."**——阙疑的"可被独立验收"正是 central，所以代码不可省。
- **第 6 项 Experimental Setting/Details**：数据划分、超参及其选择方式必须在正文或附录给出；"The experimental setting should be presented in the core of the paper to a level of detail that is necessary to appreciate the results"。
- **第 7 项 Experiment Statistical Significance**：**"The authors should answer 'Yes' if the results are accompanied by error bars, confidence intervals, or statistical significance tests, at least for the experiments that support the main claims of the paper."** 并要求说明误差棒捕捉的是哪种变异来源、计算方法（closed form / library call / bootstrap）、假设（如正态）、以及是 std 还是 sem。
- **第 8 项 Experiments Compute Resource**：须给出计算单元类型（CPU/GPU/集群/云）、内存、存储、每次运行的算力与总算力估算；并**披露全项目是否比论文中报告的部分更耗算力**（"whether the full research project required more compute than the experiments reported in the paper (e.g., preliminary or failed experiments that didn't make it into the paper)"）。

清单的强制性条款：**"The papers not including the checklist will be desk rejected."** 且答案对审稿人、AC、SAC、伦理审稿人均可见并随最终版发布；答 "no" 或 "n/a" 本身不构成拒稿理由（"In general, answering 'no' or 'n/a' is not grounds for rejection"）。

对阙疑而言，第 8 项的"披露失败实验"条款是一个**免费的加分位**：阙疑已经有现成的诚实登记材料（`research/` 下 19 个文件里的验收报告、`_arch_v46/00_仓库扫描.md` §14 的盲区清单、以及"变异测试 97.3% 不可当缺陷检测率"的主动放弃声明）。把这些写进 Method 末尾的 "Compute and Effort Disclosure" 小节，等于直接命中 checklist 第 8 项。

### 4. provenance 的三套成熟模板与它们的字段

**(a) Datasheets for Datasets**（Gebru, Morgenstern, Vecchione, Vaughan, Wallach, Daumé III, Crawford；arXiv:1803.09010，v1 2018-03-23，v8 2021-12-01；正式发表于 **CACM 2021 年 12 月**）。论文主张"每个数据集都应附一份 datasheet，记录其动机、构成、采集过程、推荐用途等"，并按电子元件 datasheet 的类比组织。其七节结构为：**Motivation（动机）/ Composition（构成）/ Collection Process（采集过程）/ Preprocessing, Cleaning, and Labeling（预处理与标注）/ Uses（用途）/ Distribution（分发）/ Maintenance（维护）**。阙疑可对应改造为：Motivation（为什么要验证 C++ 知识而非生成）/ Composition（37 实卡 + 10 草稿 + 67 规则 + 452 判决账本）/ Collection（holdout 30 seed 的植入方式、corpus 40 条的三层来源）/ Preprocessing（标签人工复核记录：真错 7→17 的两次 reveal）/ Uses（可验收场景与不可用场景）/ Distribution（Croissant + Zenodo DOI）/ Maintenance（Merkle checkpoint 与对账器的维护承诺）。

**(b) Model Cards for Model Reporting**（Mitchell 等；arXiv:1810.03993；发表于 **FAT\* 2019**，DOI **10.1145/3287560.3287596**）。Model Cards 的核心是"透明化模型报告"，强调**按子群体分解指标**。阙疑可直接借用的写法是"按规则类别分解检出率"——即把 66.7% 的总体检出率拆成 44 条 block 规则 / 16 条 warn / 7 条 advice 三层的分层检出率，并像 Model Card 那样标注每层的适用域（cpp_standard / compiler / platform / input_domain，这正是 663 C1 批次为 26 张 verified 卡补的 semantic scope）。

**(c) Croissant**（arXiv:2403.19546；发表于 **NeurIPS 2024 Datasets & Benchmarks track**；代码在 `github.com/mlcommons/croissant`）。Croissant 是"用于 ML-ready 数据集的高层元数据格式，把元数据、资源文件描述与 ML 语义结合"。NeurIPS 2025/2026 把它**强制化**：Croissant 文件必须随投稿提交并通过校验（可用 Hugging Face Space `JoaquinVanschoren/croissant-checker` 在线验证；FAQ 提示 Hugging Face 数据集常因限流导致在线校验超时，建议本地运行校验代码）。若数据集托管在 Kaggle/OpenML/Hugging Face/Dataverse，Croissant 会自动生成；自建托管则须自己生成。FAQ 还允许在格式无法处理某些文件类型时"仅提供数据集级元数据与资源描述（FileObject、FileSet），可省略 RecordSets"。

**阙疑的关键适配点**：Croissant 面向"表格/记录型"数据集，而阙疑的核心提交物是**判决账本（452 条）+ 哈希链 + Merkle checkpoint**。这类"不可变追加日志"并不是 RecordSet，恰好对应 Croissant 允许的"省略 RecordSets、只给 FileObject/FileSet + 数据集级元数据"路径。这一点必须在 Method 里显式说明，否则会撞上自动化校验。

**(d) 补充参照：FAIR 原则**（Wilkinson 等，2016，*Scientific Data*）：Findable / Accessible / Interoperable / Reusable。它可作为 Method 里"数据可得性"一段的总纲句，但**不建议**把它当作技术贡献来写——FAIR 是 2016 年的既有共识，不是新颖性。

### 5. 独立验收的实证基线：artifact 的真实通过率

Method 里若声称"可被独立验收"，必须有同类系统的通过率作参照。目前可查到的两组硬数据：

**(a) ICSE artifacts 大规模评估（2015–2024）**：一项针对 **1372 篇 ICSE 研究轨道论文**（2015–2024 年，逐年 84/101/68/105/109/129/138/197/207/234 篇）的研究统计出：给出 artifact 链接的有 **1085 篇（79.08%）**；链接中 artifact 可访问的有 **941 篇（86.73%）**；其中**含可执行组件的仅 796 篇（84.59%）**。该研究明确指出："In both cases, the publicly shared artifacts were not executable due to undocumented issues, underscoring the gap between availability and practical reusability."（公开分享的 artifact 因未记录的依赖问题而不可执行，暴露了"可用"与"可实际复用"之间的鸿沟）。它还做了一个 **100 篇的分层抽样**。

**(b) EuroSys Artifact Evaluation（2021–2025）**：接收论文数 38 / 45 / 54 / 71 / 85；artifact 投稿率 58% / 73% / 59% / 47% / 53%；获得 Artifact Available 的比例（占接收论文）55% / 73% / 57% / 45% / **52%**；获得 Evaluated-Functional 的比例 47% / 60% / 44% / 35% / **49%**；而 **Results Reproduced 的比例从 2021 年的 37% 掉到 2025 年的 25%**（2022 年 44%、2023 年 15%、2024 年 17%）。

这两个数字组合起来给出一个非常有力的 Method 论证：**"我给出了 artifact 链接"的论文有 79%，但"别人真能跑出我的结果"的论文只有 25%**。阙疑把"不依赖内核的独立对账器"作为一等贡献，正是在补这个 79%→25% 的缺口。这句话可以直接写进 Method 的第一段。

**(c) ACM 三级徽章**（Artifact Review and Badging v1.0）：**Artifacts Available**（有 DOI、长期归档、不可变）、**Artifacts Evaluated – Functional**（Documented / Consistent / Complete / Exercisable 四项均达标）、**Artifacts Evaluated – Reusable**（超出最低功能要求）。SLE'24 的 artifact evaluation 页面给出了判定细则，例如 "Available" 要求用 DOI 指向**具体版本**（Zenodo 不要用 "always latest" DOI；FigShare 要用带版本后缀的 DOI），且**必须归档在长期保存的档案库**（"version repositories do not fulfill this requirement, as the hosting company could decide at any time to discontinue the service, as done by Google, for example: Google Code"）。

### 6. Method 的结构模板（针对"验证器/评估框架"这类贡献）

综合上述规则与模板，阙疑的 Method 建议按 **7 小节 + 2 附录** 组织，每节末尾用一行 "Recompute:" 给出可执行命令（这正是 checklist 第 5 项 "exact command and environment" 的直接落地）：

1. **§3.1 Problem Formalization**：把"知识验证"形式化为判定函数 `verdict: (artifact, claim, environment) -> {accept, reject, warn, unknown}`，显式写出四态判决的语义与偏序（哪两态互斥、哪一态是 fail-closed）。必须给出**输入域**定义（cpp_standard / compiler / platform / input_domain 四元组）。
2. **§3.2 Rule Engine**：67 条规则（block 44 / warn 16 / advice 7）的分类学、规则来源、以及规则的版本化方式。建议用一张三列表：规则 ID / 触发条件（一阶逻辑式）/ 证据字段。不要贴 3826 行代码，只贴规则 schema + 一个完整规则实例。
3. **§3.3 Four-State Verdict Semantics**：四态的真值表 + 冲突消解顺序（block 优先于 warn 优先于 advice）+ unknown 的产生条件。这一节要给出**反例**：什么情况下故意返回 unknown 而不是 reject。
4. **§3.4 Evidence and Provenance**：每条判决携带的证据结构（源位置、规则 ID、规则版本、引擎版本、输入哈希、时间戳）。这一节是 datasheet 的 "Composition + Collection" 的技术版。
5. **§3.5 Append-only Hash Chain**：链的定义（前驱哈希 + 记录体哈希）、写入协议、以及"为什么 append-only"（不可回改是独立验收的前提）。给出**一个真实的链头与链尾哈希前缀**（8–12 位即可）作为锚。
6. **§3.6 Merkle Checkpoint**：checkpoint 的构造（叶子排序规则、树的填充规则、根哈希计算）、checkpoint 发布节奏、以及"给定一条记录与一条 inclusion proof，验证者如何在不信任内核的前提下验证"。
7. **§3.7 Independent Reconciler**：**这一节是全文最重要的 Method 小节**。必须明确写出：对账器**不导入** `tools/gate_engine.py`；它只依赖账本文件 + 规则表 JSON + 哈希原语；它的输入、输出、以及它能检出而内核自己检不出的故障类（这是它存在的全部理由）。建议用伪代码（LaTeX `algorithm`/`algorithmic` 环境）给出 **≤ 25 行**的对账算法，并在附录给出完整实现的行数与文件路径。

附录 A：**Compute and Effort Disclosure**（checklist 第 8 项）；附录 B：**Reproducibility Instructions**（checklist 第 5 项，含逐条命令）。

伪代码写作的三条硬规则（来自 PLOS 与 MDPI 的方法学写作指南的一致建议）：(i) 伪代码只写**控制流与不变量**，不写语言细节；(ii) 每个 `return`/`raise` 分支都要能被正文的某一句引用；(iii) 伪代码里出现的每个符号都必须在 §3.1 定义过。

---

## 对阙疑的 3 条具体行动

**行动 1（2026-10-31 前，写 Method 骨架）**：在 `research/paper_v0.4.md` 中新增 §3 Method，严格按上面 §3.1–§3.7 + 附录 A/B 的 9 个小节落地；每小节末尾加一行 `Recompute: <命令>`。命令必须真实可跑，例如 `python tools/gate_engine.py --check --rules data/_gate_rules.json`（须先用 `--help` 核实真实参数名，`_arch_v46/00_仓库扫描.md` 未记录该脚本的 CLI）。验收标准：把 §3 单独交给一个没读过仓库的人，他能仅凭 §3 跑出 `--check 16/16` 的结果。

**行动 2（2026-11-15 前，写 provenance 混合元数据）**：新建 `research/14_datasheet_queyi.md`（Datasheet 七节）+ `data/croissant/queyi.jsonld`（Croissant，走"省略 RecordSets、只给 FileObject/FileSet + 数据集级元数据"的路径），并本地跑 Croissant 校验。同时把 hold-out 声明句写进论文：`data/holdout/holdout.json`（30 seeds）为防污染私有 hold-out，公开部分为 `data/external_corpus/external_corpus_665.json`（40 条）与 `data/defect_fixtures/defects.json`（15 条）。这一步直接对应 NeurIPS 2026 ED FAQ 的私有留出集条款。

**行动 3（2027-01-31 前，做 artifact 提交包）**：按 ACM 三级徽章标准准备提交包——Zenodo 上传带**版本号 DOI**（不要用 "always latest" DOI）+ 匿名 git 镜像（`anonymous.4open.science`）+ README 内的 "exact command and environment" 清单。目标是在论文里写出一句有实证支撑的主张："同类工作给出 artifact 链接的比例约 79%，但真正被复现出结果的比例只有 25%（EuroSys 2025：52% Available / 49% Functional / 25% Reproduced）；阙疑的独立对账器把这个缺口作为一等设计目标。"

---

## 盲区（诚实标注）

1. **NeurIPS 2027 的 ED CfP 在本次调研时点（2026-09-29）尚未发布**，本文所有日期与格式要求来自 **NeurIPS 2026 ED FAQ**（更新于 2026-04-07）与 **NeurIPS 2025 D&B CfP**。2027 的页数限制、deadline、Croissant 强制程度均可能在 2027 年调整，须在 2027 年 3–4 月刷新。
2. **NeurIPS 2024 D&B 的接收数（163）来自官方 Accepted Papers 页面的检索摘要**；本次 WebFetch 该 URL 时被重定向到 2025 年页面（返回内容标题为 "NeurIPS 2025"），因此 2024 与 2025 同为 163 这一"巧合"**未做二次独立核实**。
3. **NeurIPS 2025 D&B 的提交数 591 口径存疑**：Paper Copilot 自己说明 "Reject: refers only to submissions that opted in for public release"，且该行给出的百分比（84.09% / 73.43% / 9.48% / 1.18% / 15.91%）定义未在页面中说明。本文只采用其**提交数 591** 并标注为可疑，不采用其百分比。
4. **ICSE artifacts（2015–2024）那组数字（1372 / 1085 / 941 / 796）来自检索摘要文本**，未能下载全文核对表 1 的逐年数值；分层抽样 100 篇的具体方法未核实。
5. **EuroSys AE 的 2021–2025 逐年表格**来自 ACM DL 页面检索摘要，未逐格核对原 PDF。
6. **Croissant 对"不可变追加日志"这类非表格数据的适用性未验证**——FAQ 只说了"若格式无法处理某些文件类型，仍须提交 Croissant 文件，可仅提供数据集级元数据与资源描述，可省略 RecordSets"，但阙疑的哈希链是否真能被 `croissant-checker` 通过，**必须实测**，本文不能保证。
7. **FAIR 原则（Wilkinson 等 2016）的正式 DOI 未核实**，只核实到论文标题、作者姓氏与年份。
8. **`tools/gate_engine.py` 的 CLI 参数名未核实**（`_arch_v46/00_仓库扫描.md` 只记录了行数 3826，未记录 CLI），行动 1 中的命令写法是示意，须以 `--help` 实测为准。
9. 本文**未**逐字核对 PLOS / MDPI 方法学指南原文，只核对了其页面标题与定位。

---

## 来源

1. NeurIPS 2026 Evaluations & Datasets FAQ（2026-04-07 更新）— https://neurips.cc/Conferences/2026/EvaluationsDatasetsFAQ
2. NeurIPS 2025 Datasets & Benchmarks Track Call for Papers — https://neurips.cc/Conferences/2025/CallForDatasetsBenchmarks
3. NeurIPS Paper Checklist Guidelines — https://neurips.cc/public/guides/PaperChecklist
4. NeurIPS 2025 Data Hosting Guidelines — https://neurips.cc/Conferences/2025/DataHostingGuidelines
5. NeurIPS 2025 Datasets and Benchmarks Accepted Papers（163 篇）— https://neurips.cc/Conferences/2025/DatasetsBenchmarks/AcceptedPapers
6. NeurIPS 2024 Datasets and Benchmarks Accepted Papers — https://neurips.cc/Conferences/2024/DatasetsBenchmarks/AcceptedPapers
7. Paper Copilot, NeurIPS 2024 / 2025 Datasets & Benchmarks Track Statistics — https://legacy.papercopilot.com/statistics/neurips-statistics/neurips-2024-statistics-datasets-benchmarks-track/ ；https://legacy.papercopilot.com/paper-list/neurips-paper-list/neurips-2025-accepted-paper-list-datasets-benchmarks-track/
8. T. Gebru, J. Morgenstern, B. Vecchione, J. W. Vaughan, H. Wallach, H. Daumé III, K. Crawford, "Datasheets for Datasets", arXiv:1803.09010（v1 2018-03-23 / v8 2021-12-01），CACM, December 2021 — https://arxiv.org/abs/1803.09010
9. M. Mitchell, S. Wu, A. Zaldivar, P. Barnes, L. Vasserman, B. Hutchinson, E. Spitzer, I. D. Raji, T. Gebru, "Model Cards for Model Reporting", arXiv:1810.03993；FAT\* 2019，DOI 10.1145/3287560.3287596 — https://arxiv.org/abs/1810.03993
10. "Croissant: A Metadata Format for ML-Ready Datasets", arXiv:2403.19546；NeurIPS 2024 Datasets & Benchmarks Track — https://arxiv.org/abs/2403.19546 ；代码 https://github.com/mlcommons/croissant
11. "The State of Open Science in Software Engineering Research: A Case Study of ICSE Artifacts"（1372 篇 ICSE 论文 2015–2024 的 artifact 可得性与可执行性统计）— https://acm-stag.literatumonline.com/doi/10.1145/3744916.3787813
12. "Lessons Learned from Five Years of Artifact Evaluations at EuroSys"，ACM Reproducibility and Replicability 2025，DOI 10.1145/3736731.3746152 — https://dl.acm.org/doi/abs/10.1145/3736731.3746152
13. ACM, Artifact Review and Badging – Version 1.0 — https://www.acm.org/publications/policies/artifact-review-and-badging
14. SLE 2024 Artifact Evaluation（Available / Evaluated 徽章判定细则）— http://sleconf.org/2024/ArtifactEvaluation.html
15. M. D. Wilkinson et al., "The FAIR Guiding Principles for scientific data management and stewardship", Scientific Data, 2016 — https://agbeltran.github.io/publication/2016-03-15-fair-guiding-principles
16. PLOS Author Resources, "How to write a methods section" — https://explore.plos.org/author-resources/how-to-write-a-methods-section
17. "A step forward in tracing and documenting dataset provenance", Nature Machine Intelligence, 2024 — https://www.nature.com/articles/s42256-024-00884-w
18. Data Provenance Initiative, publications — https://www.dataprovenance.org/publications
