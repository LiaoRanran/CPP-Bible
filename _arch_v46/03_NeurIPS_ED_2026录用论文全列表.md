# 方向 03：NeurIPS 2026 Evaluations & Datasets（E&D）录用论文全列表

## 核心结论

1. **2026 年该 track 已正式改名**：Datasets & Benchmarks → **Evaluations & Datasets（E&D）**，官方博客（2026-03-23）原文为"the Datasets & Benchmarks Track at NeurIPS 2026 has been officially renamed the **Evaluations & Datasets (ED) Track**"，并把"evaluation 本身成为科学研究的对象"写成赛道新定位。
2. **截至本文件撰写日（2026-09-29），NeurIPS 2026 E&D track 的官方录用论文列表尚未发布**：作者通知日是 2026-09-24（官方 CFP 原文"Author notification: September 24, 2026 (AoE)"），但 `neurips.cc` 上的 E&D/D&B 录用页仍为 2021 年遗留模板页（无任何论文条目），OpenReview 会场页被 Cloudflare 拦截，官方虚拟站尚无 `evaluations-datasets-2026` 或 `datasets-benchmarks-2026` 事件页（均返回 404）。
3. **2026 年 9 月出现了一起与本项目高度相关的"提前泄露论文列表"事件**：一个 GitHub 仓库被发现包含约 **7,000 篇**论文的 HTML 列表，社区猜测是 NeurIPS 2026 录用名单泄露；但公开证据**只能证明"有人整理了一份庞大的论文集合"，不能证明"录用决定被泄露"**——这是一次教科书级的"provenance 缺失"案例，可直接作为阙疑论文的问题动机。

---

## 精确数字与案例

### 一、改名与赛道定位（官方原文）

**官方博客（2026-03-23）** 的核心段落逐字摘录：

> "We are excited to announce that the Datasets & Benchmarks Track at NeurIPS 2026 has been officially renamed the **Evaluations & Datasets (ED) Track**. … The new name places evaluation first, while datasets remain central and receive renewed focus within broader evaluative practices rather than as endpoints in themselves."

> "We explicitly define evaluation as: ***Processes, practices, tools, and resources for making evaluative claims about AI/ML systems, including – but not limited to – datasets, benchmarks, user studies, simulators, auditing, red-teaming methods, interaction protocols, metrics, and experimental or qualitative study designs.***"

> "**Benchmarks remain in scope**. They are a subset of evaluations, standardized, reusable setups that serve as shared comparison points. Removing 'benchmarks' from the title does not signal exclusion."

**E&D Track chairs 2026（官方署名）**：Konstantina Palla、Jessica Schrouff、Alexandre Drouin、Lijun Wu、Joaquin Vanschoren。联系邮箱 `evaluationsdatasets@neurips.cc`。

**CFP 的赛道定位原文**：

> "Formerly the Datasets & Benchmarks Track, the E&D Track reflects a shift and broadening in scope: **evaluation becomes an object of scientific study in its own right**. … Submissions are expected to clearly articulate the evaluative role their contribution plays: what claims it supports, under what assumptions, and what limitations apply."

### 二、时间线与关键日期（官方 CFP 原文）

| 事项 | 日期 | 原文 |
|---|---|---|
| 投稿系统开放 | 2026-04-15 | "The submission portal opens on April 15, 2026" |
| Abstract 截止 | 2026-05-04 (AoE) | "Abstract submission deadline: May 4, 2026 (AoE)" |
| 全文 + 全部补充材料截止 | 2026-05-06 (AoE) | "Full paper submission deadline (including all supplementary materials): May 6, 2026 (AoE)" |
| 作者通知 | **2026-09-24 (AoE)** | "Author notification: September 24, 2026 (AoE)" |
| 会议 | 2026-12-06 至 12-13 | Sydney 12-06～12-12；Atlanta / Paris 12-09～12-13 |

**注意**：本文件撰写于 2026-09-29，距作者通知仅 5 天，距投稿截止约 4.7 个月。

### 三、2026 年 E&D 的三项硬性制度变化

**变化 1：评审模式从"默认单盲"改为"默认双盲"**

2025 年 D&B 的官方 CFP 原文是"Authors can choose to submit either single-blind or double-blind"；而 **2026 年 E&D 的 CFP 原文是**：

> "Unlike previous years, the default review mode for the E&D Track is now **double-blind**, reflecting the track's broader scope beyond dataset submissions. Authors whose submission centers on datasets that cannot be fully anonymized for scientific or ethical reasons … should indicate this in the submission form by selecting **single-blind** review."

FAQ 进一步给出匿名化操作细节："On hosting platforms, create an **anonymous account** (e.g. using the name of your project) and ensure there is no information leaked (**including in the Croissant file**)."

**变化 2：新增 Responsible AI（RAI）元数据强制要求**

2026-05-04 官方博客原文：

> "we are introducing a new requirement for dataset submissions in the NeurIPS 2026 Evaluations and Datasets Track: **all dataset submissions must now include Responsible AI (RAI) metadata as part of the dataset's Croissant file**."

> "dataset submissions **missing RAI metadata from their Croissant file will be flagged during review**."

配套工具两个：在线 RAI 编辑器 `https://huggingface.co/spaces/JoaquinVanschoren/croissant-rai-checker`、Croissant 校验器 `https://huggingface.co/spaces/JoaquinVanschoren/croissant-checker`。

**变化 3：代码提交从"一律要求"改为"按贡献类型要求"**

CFP 原文：

> "our code policy is **contribution-dependent**. … code release is ***required*** at submission when the primary contribution is a reusable executable artifact, such as a **benchmark suite, evaluation environment, data generator, or software tool**, whose functionality must be inspected in order to evaluate the scientific claims."

**这条对阙疑是直接利好**：阙疑的形态（可执行工具 + 数据生成器 + 评测环境）恰好落在"代码强制公开"的类别里，且评审人**必须实际检查可执行性**——这正是"可被独立验收"的用武之地。

**其他量化门槛**：CFP 原文"for large datasets (larger than **4GB**), authors are required to include a small sample of the data"；FAQ 原文"We also generally require large datasets (**> 4GB**) to provide a smaller data sample"。

### 四、2026 年 E&D 的 8 类贡献与"强制检查项"

2026 Reviewing Guidelines（2026-06-25 更新）把投稿分为 **8 类贡献**，每类给出 Quality / Clarity / Significance / Originality 四维度的具体解读 + 强制检查项。这是目前 NeurIPS 对该 track **最细颗粒度的评审标准文本**。逐字摘录关键项：

**评测类**

1. **Benchmark Design and Benchmark Analysis** — 强制检查：必须双盲（或经论证的单盲）；**强烈鼓励**提供可复现 benchmark 的代码；若无代码，评估 OpenReview 的 code justification 字段是否有说服力；若引入新数据集，须遵守 Datasets 类要求。
2. **Evaluation Methodology and Metrics** — 强制检查：必须双盲；**鼓励**提供指标实现代码。原文："New framing is sufficient - no need to beat a baseline."
3. **Evaluation Tools, Frameworks, and Infrastructure** — 强制检查："**无代码 = 拒稿**，除非提供有说服力的理由"；Code URL 应可访问、可执行、已匿名化。
4. **Reproducibility, Auditing, and Stress-Testing of Evaluations** — 强制检查：必须双盲；鼓励提供复现/审计代码；"If a negative result: is it deep and carefully controlled?"
5. **Human-Centered and Interaction-Based Evaluation** — 强制检查：**须提供 IRB 认证或等效机构文件**；须确认所有参与者获得公平报酬。

**数据集类**

6. **Datasets and Data Resources** — 强制检查：是否存在**有效的 Croissant 文件**？**RAI 元数据是否完整**（偏见、局限、预期用途、敏感信息）？数据集是否**无需向 PI 请求即可访问**？原文："Datasets-as-endpoints don't meet the bar on their own."
7. **Dataset Documentation, Auditing, and Responsible Data** — 强制检查：必须双盲；若审计为自动化，须提供代码/工具。
8. **Data-Centric Methods and Empirical Analyses** — 强制检查：必须双盲；鼓励提供实验代码。

**评审人禁止条款**（同一文档原文）："**reviewers may not use any LLMs or AI agents in the review process**"。这与 2025 年 D&B 的"responsible reviewing initiative"（对评审敷衍的作者，其共同署名论文被 desk-reject）是同一路线的加码。

### 五、2026 年录用名单：为什么现在拿不到

我们做了以下**穷举式探测**，全部失败或返回无效内容：

| 探测的 URL | HTTP 状态 | 结果 |
|---|---|---|
| `neurips.cc/Conferences/2026/EvaluationsDatasets/AcceptedPapers` | 404 | 不存在 |
| `neurips.cc/Conferences/2026/EvaluationsDatasetsAcceptedPapers` | 404 | 不存在 |
| `neurips.cc/Conferences/2026/DatasetsBenchmarks/AcceptedPapers` | **200** | 但正文为空（仅 footer 脚本），**无任何论文条目** |
| `neurips.cc/virtual/2026/events/evaluations-datasets-2026` | 404 | 不存在 |
| `neurips.cc/virtual/2026/events/evaluations-and-datasets-2026` | 404 | 不存在 |
| `neurips.cc/virtual/2026/events/datasets-benchmarks-2026` | 404 | 不存在 |
| `neurips.cc/virtual/2026/papers.html` | **403** | 被拒（需浏览器） |
| `openreview.net/group?id=NeurIPS.cc/2026/Evaluations_and_Datasets_Track` | 200 | 返回 Cloudflare Turnstile 人机验证页，无内容 |
| `api2.openreview.net/notes?invitation=NeurIPS.cc/2026/Evaluations_and_Datasets_Track/-/Submission` | **403** | `ChallengeRequiredError`："Challenge verification required (2026-09-29-3700847)" |

**唯一可用的 2026 全局计数**：`neurips.cc/Downloads/2026` 页面原文 "**Number of events: 9127**"（该数覆盖 Posters / Tutorials / Invited talks / Workshops / Demonstrations 全部类别，**不是** E&D 论文数）。

**第三方对 NeurIPS 2026 主赛道的统计**（OpenAccept）：**Submitted 30,709 / Accepted 7,900 / Acceptance Rate 25.73%**。**未提供任何 E&D track 的分轨数字**。

**GitHub 上的社区文档**（`LiudengZhang/conference-vaults`，2026-05-11 快照）原文亦确认："Paper notifications go out Sep 24, 2026; workshop accept/reject Sep 29, 2026; **accepted-paper list and workshop roster are not yet public**."

**结论：截至 2026-09-29，"NeurIPS 2026 E&D 录用论文全列表"在公开渠道上不存在。本文件不做任何推测性列举。**

### 六、一起与阙疑同构的"未核实列表"事件（2026-09）

2026 年 9 月，Reddit r/MachineLearning 出现帖子 **"NeurIPS accepted papers leaked"**，指向 GitHub 仓库（争议 HTML 文件），声称包含约 **7,000 篇**论文；部分条目带详细元数据，部分已匿名化。多家媒体转述，但后续分析（`everdent.cn`，2026-09-01）给出的结论是：

> "该仓库证明的是**有人整理出了一份庞大的论文列表**，而不是 NeurIPS 已发布录用决定。"

> "真实的录用数据集应包含与决定直接相关的证据，例如**官方决定标签、报告展示安排、终稿状态，或与官方议程的直接匹配**。就公开描述而言，该主张并未证明存在任何这些信号。"

> "**'论文列表'与'已接收论文列表'是不同的产物，即使两者共享数千个标题。**"

该分析还给出了**三条可操作的溯源判据**（对阙疑的证据链设计有直接借鉴价值）：

1. 文件是否包含**明确的决定信息**（decision label）？
2. 收集时这些信息**是否属于私密信息**？
3. 其来源能否**追溯到权威系统**（可复现的采集脚本）？

**这三条判据几乎可以直接改写成阙疑"可被独立验收"的形式化定义**：一份判决要可验收，必须（1）带明确的四态判决标签，（2）带时间戳与当时可见性状态，（3）带可复现的证据引用（provenance）。阙疑的 append-only 哈希链 + Merkle checkpoint + 独立对账器，正是对这三条的工程化回答。

### 七、2026 年 E&D 的赛道边界示例（官方 FAQ 给出）

官方 FAQ 用真实论文举例界定"何时该投 E&D、何时该投主赛道"，这是**最具体的选题判断依据**：

| 例子 | 官方判定 | 理由（原文摘要） |
|---|---|---|
| ImageNet（Deng et al., 2009） | **ED** | "The primary contribution relates to the dataset → ED." |
| Kleinberg et al., 2016 | **主赛道 / negative result** | "its main contribution is that of a negative, rigorously demonstrated and surprising result that is **not demonstrated via empirical evaluations** → main track / negative result." |
| Gu et al., 2025《The Illusion of Readiness in Health AI》 | **ED** | "the primary focus of this paper is on **experimental evaluations** → ED." |
| Dwork et al., 2011（差分隐私公平性度量） | **ED** | "the main contribution is about the **definition of a new fairness metric** → ED." |
| Lam et al., 2023 | **主赛道 / use-case inspired** | 评测只是手段而非核心贡献 |

FAQ 还明确："**there will be no possibility to switch tracks or types** and that papers cannot be submitted to multiple tracks or types simultaneously. Irrelevant or duplicate papers risk desk rejection from all tracks."

**对阙疑的直接含义**：阙疑的核心贡献是"一套评测 C++ 知识正确性的方法论 + 可执行工具 + 数据集（30 holdout / 40 corpus / 15 缺陷夹具）"，且主张落在"可被独立验收"的**评测协议**上——按 FAQ 的判据，**属于 ED 赛道**（"Propose new evaluation protocols, practices, or methodologies" 明确在 in-scope 列表中）。

### 八、2026 年 9 月的一起"AI 检测 desk-reject"事件（旁证）

NeurIPS 2026 Position Paper Track 的 chairs（Alex Lu、Seth Lazar、David Rugamer）**用 Pangram AI 工具 desk-reject 了 178 篇投稿，占该 track 的 18.4%**（AI Weekly，2026-06-04 转述）。这件事的意义在于：**NeurIPS 已经在用自动化工具做"机器判决 + 人工确认"的流程**。阙疑的"67 条规则内嵌引擎（44 条 block）+ 四态判决"在设计上与这类实践同构，但阙疑的差异化在于**判决可被第三方独立对账**，而 Pangram 的判决是黑箱。

### 九、赛道边界的实操判断（写给阙疑自己的"投稿体检"）

官方 FAQ 的判据可以归纳成一句话：**"评测本身是不是核心智力贡献"**。把它展开成可操作的三问：

**第一问：如果删掉所有"被评测的系统"，论文还剩什么？**
如果剩下的是"一套如何做评测的方法论 / 协议 / 工具 / 审计结论"，则属于 ED；如果剩下的是"一个新模型 / 新算法"，则属于主赛道。官方原文的边界句是："The boundary shifts when **evaluation is the core intellectual contribution** versus when it **serves as evidence for a domain-driven modeling advance**."

**第二问：贡献的产物是"可执行物"还是"分析结论"？**
2026 年 E&D 的代码政策把两者分开处理：前者（benchmark suite / evaluation environment / data generator / software tool）**代码强制公开**；后者（analytical / empirical / conceptual / methodological）**代码非强制**，但"须有足够细节支撑有意义的评审"。阙疑的产物同时包含"可执行工具（`tools/gate_engine.py` 3826 行 + 独立对账器）"与"分析结论（检出率、测量陷阱）"，因此**大概率落在"代码强制"一类**。

**第三问：主张是否带"假设 + 局限"的显式声明？**
2026 年 CFP 原文反复强调："**Submissions are expected to clearly articulate the evaluative role their contribution plays: what claims it supports, under what assumptions, and what limitations apply.**" 并且明确警告："Papers that present data without clarifying the intended problem formulation, evaluation setup, or interpretive boundaries are unlikely to provide sufficient context for review and **may therefore not fall within the intended scope of the track**."

**第三问是 2026 年相对 2024 年的最大新增要求。** 2024/2025 年的 CFP 只要求"数据集要可用、可访问、有 Croissant"，2026 年则要求**论文正文本身必须回答"你支持什么主张、在什么假设下、有什么局限"**。这对阙疑是**优势而非负担**：阙疑的 v0.3 论文已经主动写了 semantic scope（cpp_standard / compiler / platform / input_domain 四字段）与 claim 边界，并在 26 张 verified 卡上补齐了 semantic scope（对应仓库 663 C1 批次）。**这些原本是"额外的诚实"，在 2026 年的评审标准下变成了硬性准入条件。**

### 十、2026 年 E&D 的"评审人视角"清单（给作者的反向检查）

把 2026 Reviewing Guidelines 的强制检查项反向读一遍，就是作者的提交清单：

| 检查项 | 阙疑当前状态（基于 `00_仓库扫描.md`） | 待办 |
|---|---|---|
| 是否双盲（默认） | 仓库为本地路径 `C:/CodeLearnling/...`，README 含作者信息 | **需做匿名化分支** |
| 代码是否可执行、可访问 | `tools/` 有 640 条目 / 595 个 `.py`，`gate_engine.py` 3826 行 | 需在干净环境实测 |
| 代码是否已匿名化 | 未知（未检查 git remote / 提交者信息） | **需检查并清理** |
| 数据集是否在四大平台托管 | 数据集在本地 `data/` 下 | **需上传 HF/Kaggle/Dataverse/OpenML** |
| 是否有有效 Croissant 文件 | 无 | **需生成（含 core + RAI）** |
| RAI 元数据是否完整 | 无 | **需填写偏见 / 局限 / 预期用途 / 敏感信息** |
| 数据集是否无需向 PI 请求即可访问 | 本地文件，无需请求 | ✅ 结构上满足 |
| 大数据集（>4GB）是否提供样本 | 数据集规模远小于 4GB | 不适用 |
| 是否声明了"支持什么主张 / 什么假设 / 什么局限" | v0.3 论文已有 semantic scope 与 claim 边界 | ✅ 部分满足，需强化 |

**这张表是本方向对阙疑最直接的产出**：它把"2026 年 E&D 的评审标准"翻译成了仓库里的 9 条待办。

---

## 对阙疑的 3 条具体行动

1. **把"评测即科学对象"写进标题与摘要的第一句**：2026 年 E&D 的官方定义原文是"evaluation becomes an object of scientific study in its own right"。建议把 `research/paper_v0.3.md` 的标题从"一个'可被独立验收'的 C++ 知识验证器"改为更贴赛道的表述，例如："**Auditable by Construction: An Independently Verifiable Evaluation Protocol for C++ Knowledge Claims**"，并在摘要第一句直接对齐官方定义（"we treat evaluation itself as the object of study"）。**注意**：不要在正文声称"我们是第一个"，只做定位对齐。时间点：2026-10 至 2026-12 之间完成标题定稿。
2. **按 E&D 的 8 类贡献给阙疑做"自归类体检"**：新建 `research/03b_track_fit.md`，逐条对照 2026 Reviewing Guidelines 的 8 类，标注阙疑属于哪一类（预判：**类 4 Reproducibility/Auditing/Stress-Testing + 类 3 Tools/Frameworks/Infrastructure + 类 6 Datasets**），并为每类填写其**强制检查项**的当前状态。**类 3 的"无代码 = 拒稿"必须逐字核对**——阙疑有 `tools/gate_engine.py`（3826 行）与 595 个 `.py`，但**是否已匿名化、是否可在无凭证环境一键执行**需实测（建议在干净容器里跑一次 `python tools/gate_engine.py --check`）。时间点：2026-11 前。
3. **把"7,000 篇未核实列表"事件写成论文的动机案例**：在 `research/00_problem.md` 增加一节 "Motivating Case: The Unverifiable List"，引用 2026-09 的这次事件，并列出该事件的三条溯源判据（决定标签 / 时间点私密性 / 权威溯源），然后**逐一说明阙疑如何满足**：(1) 四态判决标签显式落盘；(2) 每条判决带 append-only 哈希链时间戳；(3) Merkle checkpoint + 不依赖内核的独立对账器可复算。**这是本项目最有力的"问题—方案"闭环**，且来源是 2026-09 的新事件，时效性极强。

---

## 盲区（诚实标注）

- **2026 年 E&D 的录用论文列表、投稿数、录用数、录用率全部未公开**。本文件**不做任何推测**。**需要在 2026-10 之后重新调研**（预计 2026-10～11 官方会放出 accepted papers 页与虚拟站事件页）。
- **`neurips.cc/Downloads/2026` 的 "Number of events: 9127"** 是全部类别的事件数，**不能当作 E&D 论文数**；该页的下载表单只有 Posters / Tutorials / Invited talks / Workshops / Demonstrations 五类，**没有 E&D 独立分类**。
- **OpenReview 的 2026 E&D 会场数据无法通过 API 获取**（403 `ChallengeRequiredError`），因此无法统计投稿数、评审分分布或决策分布。**这是本方向最大的数据缺口**，建议在 2026-10 用浏览器手动导出。
- **"7,000 篇"这个数字来自 Reddit 帖子的转述**，我们**未直接打开该 GitHub 仓库核对**（仓库名在部分报道中写作 `xll0328/NIPS26-`、另一处写作 `YuanDaoze/NIPS26-`，**两者是否为同一仓库未核实**）。该仓库的原始 URL 与其 HTML 文件我们也**未逐条解析**。
- **Position Paper Track 的 "178 篇 / 18.4%"** 来自 AI Weekly 的二手转述（2026-06-04），**未在 NeurIPS 官方博客中找到对应的一手声明**，标为待核实。
- **2026 年 E&D 的 page limit 未在 FAQ 或 CFP 中给出**（官方只说"It's the same as the main track template"），**需查 NeurIPS 2026 Main Track Handbook**。
- **2026 年 NeurIPS 主赛道的 30,709 / 7,900 / 25.73%** 来自 OpenAccept 第三方统计，**未在 NeurIPS 官方 Fact Sheet 中核对**（2026 Fact Sheet 在撰写时点尚未发布）。

---

## 来源

1. NeurIPS 2026 Evaluations & Datasets Track Call for Papers — https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets — 赛道定义、8 类贡献、日期、双盲政策、代码政策、4GB 阈值 — NeurIPS，2026
2. Introducing the Evaluations & Datasets Track at NeurIPS 2026 — https://blog.neurips.cc/2026/03/23/introducing-the-evaluations-datasets-track-at-neurips-2026/ — 改名声明、evaluation 定义、5 位 track chairs — NeurIPS Blog，2026-03-23
3. Responsible AI metadata requirements for the Evaluations and Datasets Track NeurIPS 2026 — https://blog.neurips.cc/2026/05/04/responsible-ai-metadata-requirements-for-the-evaluations-and-datasets-track-neurips-2026/ — RAI 元数据强制要求 + 两个校验工具 — NeurIPS Blog，2026-05-04
4. NeurIPS Evaluations & Datasets 2026 Reviewing Guidelines — https://neurips.cc/Conferences/2026/EvaluationsDatasetsReviewerGuidelines — 四维度、8 类贡献的强制检查项、"reviewers may not use any LLMs or AI agents" — NeurIPS，2026-06-25
5. NeurIPS 2026 Evaluations & Datasets FAQ — https://neurips.cc/Conferences/2026/EvaluationsDatasetsFAQ — 赛道边界 5 个真实论文示例、双盲/单盲规则、>4GB 样本要求 — NeurIPS，更新于 2026-04-07
6. NeurIPS 论文列表提前出现，但这并不能证明录用结果已泄露 — https://www.everdent.cn/zh/post/neurips-paper-list-appeared-early-it-does-not-prove-acceptances-leaked-zh — 约 7,000 篇论文的 GitHub 列表事件 + 三条溯源判据 — Everdent，2026-09-01
7. NeurIPS 2026 Downloads — https://neurips.cc/Downloads/2026 — "Number of events: 9127" — NeurIPS，2026
8. OpenAccept，NeurIPS 2026 统计 — https://openaccept.org/c/ai/neurips/2026/ — Submitted 30,709 / Accepted 7,900 / 25.73% — OpenAccept，2026
9. conference-vaults，NeurIPS 2026 index — https://github.com/LiudengZhang/conference-vaults/blob/main/docs/conferences/neurips-2026/index.md — "accepted-paper list and workshop roster are not yet public"（2026-05-11 快照）— LiudengZhang，2026
10. NeurIPS Rejects 18.4% of Position Papers via Pangram AI Tool — https://aiweekly.co/alerts/neurips-rejects-184-of-position-papers-via-pangram-ai-tool — 178 篇 desk-reject（二手转述，待核实）— AI Weekly，2026-06-04
