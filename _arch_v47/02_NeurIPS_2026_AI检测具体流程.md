# 方向 02：NeurIPS 2026 AI 检测具体流程

## 核心结论

1. **NeurIPS 2026 Position Paper Track（PPT）的 AI 检测流程已在官方博客（2026-06-02）完整公开，可逐步复现**：与 Pangram 合作 → 用 **Pangram v3.3.2** 把每篇论文切成**默认 250–350 词的窗口** → 每个窗口给出"含 AI 生成文本"的概率 → **概率 > 0.75 即该窗口被标记** → 论文的 **Pangram AI Score = 被标记窗口占全部窗口的百分比**。原文特别声明：*"A Pangram AI score of 100% should not be interpreted as '100% of the text is AI-generated', rather that there is substantive use of AI in many parts of the text."*
2. **最终处置不是单一阈值，而是"分数 × 附加条件"的三条判据**：**≥0.9 单独即拒（77 篇）**；**≥0.8 且作者有多篇单人署名论文（至少一篇超阈值）或另有一篇已被拒（79 篇）**；**≥0.5 且作者声明"未使用 AI"或干脆没声明（22 篇）**——合计 **178 篇（18.4%）不予申诉地拒稿**；另有 **123 篇（12.7%）**落在 [0.8, 0.9) 区间，被要求**在 2026-06-15 前**提交版本历史证据，否则同样拒稿。
3. **官方自己承认这套流程是"分布外推断"，并给出了最关键的元数据**：Pangram 内部与外部审计报出的假阳性率 **< 0.1%**，且此前在 **ICLR 2026 已录用论文**上只检出 **1%** 为 AI 生成；但同一台机器在 NeurIPS PPT 2026 上给出 **42.7% 的论文分数落在 90–100%**。官方在实验（10 篇样本）中发现**缩小窗口到约 100 词后，90–100% 的比例从 42.7% 降到 12.7%**，于是改用 medium 窗口——**这是一次用"牺牲召回换更细粒度主张"的显式校准操作**。对阙疑而言，这直接说明：**AI 检测的阈值是可调的、可谈判的、且官方知道自己在做分布外推断**——因此"provenance audit trail"会成为未来默认要求。

---

## 精确数字与案例

### 一、官方流程的完整链条（逐字）

来源：NeurIPS 官方博客 *AI-Generated Papers in the NeurIPS 2026 Position Paper Track*（2026-06-02），署名 **Alex Lu、Seth Lazar、David Rügamer**（Position Paper Chairs）与 **Stanley Hua、Kate Metcalf**（Assistant Position Paper Chairs）。

**政策原文（Use of AI 小节）**：

> "While AI tools may be used in the research that leads to the final paper, **the final paper must itself be substantially written by human authors, meaning that AI is used only for copy-editing or similar peripheral changes to the main text.**"
> "At submission time, authors will be required to state how AI tools were used in the preparation of the paper, if at all, and to attest that they have not used AI in ways contrary to the above rule."
> "Note that the Position Paper Track's LLM policy differs from the Main Program's LLM policy. Authors are responsible for understanding policy pertaining to the specific track they are submitting to, and abiding by it."

**检测机制原文（这是全篇最有操作价值的一段）**：

> "Given a full text document, Pangram first uses a windowing algorithm to break up the text into text windows, where by default, each window is around **250 to 350 words**. Next, Pangram assigns each text window a probability that it contains AI-generated text. If the model's assigned probability exceeds **0.75**, then that window is flagged as AI-generated. From these predictions, each paper receives a **Pangram AI score**, which is the percentage of windows that are classified as AI-generated."

**数据保密**：

> "We worked closely with Pangram to ensure, as per their enterprise-level data agreement, that **zero data would be retained** through the usage of their model."

**决策表（Table 5 原文数据）**：

| 类别 | Pangram AI Score | 附加条件 | 篇数 |
|---|---|---|---|
| **不予申诉的 desk reject** | ≥0.9 | 无 | **77** |
| | ≥0.8 | 作者提交多篇独立作者论文（其中至少一篇高于该阈值），或至少一位作者另有一篇 desk reject | **79** |
| | ≥0.5 | 作者声明未使用 AI，或未作 AI 使用声明 | **22** |
| | | **合计** | **178（18.4%）** |
| **可申诉的 desk reject** | ≥0.8 且 <0.9 | 无 | **123（12.7%）** |

> "Submissions lacking such proof by **June 15th, 2026** will also be desk-rejected."

**申诉时作者必须提交的三项证据（原文）**：

> - "Authors must supply the Track Chairs with a link to an online version of their paper that has a version history including the work before and after the use of AI"
> - "They must identify **(1)** a 'pre-AI' checkpoint indicating that they developed the substantive content of the paper independent of AI, **(2)** a 'post-AI' checkpoint immediately after their most substantive AI-written edits, and **(3)** the final paper as submitted."
> - "They must present analysis showing that the AI edits in (2) did not introduce new substantive content that was not present in (1), and of human edits after (2) which demonstrate that (3) was appropriately verified by human authors."

**主席给出的核心理由（逐字，值得整段引用）**：

> "AI-generated text is often slick, but can depart significantly from the authors' original intention. In this case, submitting AI-generated text for peer review **externalises the cost of verifying that work, imposing it on reviewers**."
> "We are also introducing a new approach to **auditing AI use by establishing appropriate provenance**. Authors whose submissions show significant AI involvement must provide an **audit trail** that clearly demonstrates that they complied with the policy. **We expect that in future years this kind of audit trail will become a default.**"
> "It is important to be clear where the burden of proof should lie when it comes to detecting improper use of AI in submissions to a peer-reviewed conference."

### 二、官方公布的跨会议对比表（Table 1，这是最硬的元数据）

| 会议 / 赛道 | 论文数 | Pangram AI Score ≥50% | ≥90% | =100% |
|---|---|---|---|---|
| NeurIPS PPT **2025** | 536 | 28.5% | 11.9% | 8.2% |
| NeurIPS PPT **2026** | 971 | **70.5%** | **42.7%** | **28.2%** |
| NeurIPS **D&B 2025** | 996 | 5.6% | 0.8% | 0.4% |
| NeurIPS **E&D 2026** | 996 | **43.7%** | **9.3%** | 2.1% |
| FAccT **2022**（ChatGPT 发布前，负对照） | 159 | **0.0%** | 0.0% | 0.0% |
| FAccT **2025** | 204 | 1.0% | 1.0% | 0.0% |

> "in the Evaluations and Datasets track, papers with a Pangram AI score ≥90% have increased **more than tenfold** from 2025 to 2026."

**注意两处内部不一致**（对阙疑写"元数据必须可对账"是极好的案例）：正文说送检 **969** 篇、28.2%（273/969），而 Table 1 里 PPT 2026 的论文数写的是 **971**。同一篇官方博客里 969 与 971 并存。

**⚠️ 这张表对阙疑的直接影响**：**E&D 2026 有 43.7% 的论文 Pangram 分数 ≥50%，9.3% ≥90%**。也就是说，**阙疑要投的那个赛道，接近一半的投稿在 AI 检测器眼里是"有实质 AI 参与写作"的**。这是一个极高风险的入口。

### 三、窗口大小的校准实验（官方自己做的"降误报"操作）

官方从 FAccT 2022 中选了 **10 篇**风格接近 position paper 的论文，用 **OpenAI GPT-5.5**（经 OpenRouter）测试 **12 种 AI 使用场景**，并做了部分补全（5%–95%）与 **5 轮编辑**（原始 → AI 编辑 → 人类编辑 → AI 编辑 → 人类编辑）实验。

**Table 2：窗口大小对召回的影响（10 篇 AI 生成的"position paper"）**：

| 窗口策略 | 平均 Pangram AI score | Recall ≥0.5 | ≥0.7 | ≥0.9 | =1.0 |
|---|---|---|---|---|---|
| small（约 50 词） | 61.8% | 70% | 30% | 0% | 0% |
| medium（约 100 词） | 91% | 100% | 100% | 70% | 0% |
| default（250–350 词） | 100% | 100% | 100% | 100% | 100% |

**Table 3：改用 medium 窗口后 NeurIPS PPT 2026 的整体分布变化**：

| 窗口大小 | ≥50% | ≥90% | =100% |
|---|---|---|---|
| medium | 62.3% | **12.7%** | 2.16% |
| default | 70.5% | **42.7%** | 28.2% |

> "Using smaller window sizes reduces the chances of over-claiming AI use, but it may also worsen the ability of Pangram to truly identify AI-generated text… we decided to move forward with medium-sized windows, **trading off recall for finer-grained claims on AI use**."

**关键实验结论（对阙疑的合规策略是决定性的）**：

> "For all of the permissible uses, **Pangram did not classify any as AI-generated**, despite a substantial change in the text."
> "In our experiment on partial AI completions, **Pangram never classified AI completions of 20% or less as AI-generated**."

### 四、官方给出的"允许 / 边界 / 不允许"清单（Table 4）

| 类别 | 具体情形 |
|---|---|
| **明确允许** | Proofreading（仅拼写、标点、语法、引用格式清理）；Light copyediting（仅局部清晰度、简洁性、措辞与句级润色，**无实质改动**） |
| **边界允许** | Heavy copyediting / line editing（大幅措辞改动与句子重构，但**保留相同论点与推理**）；Structural rewriting（重组段落或论证呈现，**保留人类的想法**）；Hybrid revision（人机共同实质塑造行文）；Translation / backtranslation（翻译/回译） |
| **明确不允许** | Generation from a single-sentence human plan（人写一句计划，AI 生成整段）；Substantive AI rewriting（AI 改变论点、推理、框架或论证结构）；Original AI-authored passage（AI 原创段落）；Human edits AI work（人只对 AI 原创段落做轻微编辑） |
| **诊断测试** | AI residue（在人类文本里插入"Sure, here is your paragraph :)"这类聊天痕迹）；Partial AI completion（AI 补全人类原文的 5%–95%） |

**官方对假阳性率的自我陈述（逐字）**：

> "We found this number surprisingly high, given internal and external audits of Pangram reported a **false positive rate of less than 0.1%**, and in previous applications to **ICLR 2026 accepted papers, the model only detected that 1% of papers were AI-generated**."
> "In recognition of the fact that norms in this area are emerging, and these terms are inherently ambiguous, we have adopted **conservative decision thresholds designed to minimize false positives**."

### 五、对照案例：ICLR 2026 的做法（同一问题，不同流程）

来源：ICLR 官方博客 *A Retrospective on the ICLR 2026 Review Process*（2026-03-31）。

**ICLR 2026 整体数字**：收到 **19,525** 篇合规投稿，**779 篇**因程序/内容违规被 desk reject，**5,042 篇**撤稿，最终 **13,763 篇**进入决定，基于 **18,054** 位审稿人提供的 **76,139** 条评审；录用 **5,355** 篇、拒 **8,408** 篇，**录用率 27.4%**。

**与 NeurIPS 的关键差异（对阙疑极其重要）**：

| 维度 | NeurIPS 2026 PPT | ICLR 2026 |
|---|---|---|
| 检测对象 | **投稿论文正文** | **评审意见 + 投稿论文** |
| 检测器数量 | 1 个（Pangram 3.3.2） | **2 个**（"flagged as being entirely LLM generated by **both** detectors"） |
| 触发动作 | **自动 desk reject**（178 篇） | **先交给 AC 人工复核** |
| 人工介入 | 无（除申诉通道） | "we will only take action if an AC or SAC identifies **concrete evidence**" |
| 幻觉引用 | 未提及 | 系统化检测；"This system had a **significant false positive rate**"；AC 一轮 → PC 全部手工复核 → **每篇至少 3 个人类**看过；确认后 desk reject，**并设申诉通道** |
| 申诉 | **标准情况下不接受** | 有 |

ICLR 原文最值得引用的一句：

> "While systems exist for detecting LLM-generated content, **their accuracy is far from perfect**, and we did not want to penalize cases where an LLM was used to assist with writing but the judgements made in the review were reasonable and valid."

ICLR 还提到把 **Google 的 Paper Assistant Tool (PAT)** 开放给 ICLR 投稿人使用——**即：一边用检测器筛稿，一边提供官方写作助手**。这是一个鲜明的政策矛盾，可作为阙疑论文 Discussion 的一处引用。

### 六、NeurIPS 2026 E&D 的投稿硬要求（直接决定阙疑能不能投）

来源：NeurIPS 2026 E&D Call for Papers 原文。

- **更名与定位**：*"evaluation becomes an object of scientific study in its own right"*。
- **默认双盲**（新变化）：*"Unlike previous years, the default review mode for the E&D Track is now **double-blind**"*。
- **数据集与代码在投稿时就必须可用**：*"Datasets and code must be properly hosted, accessible, and clearly documented **upon submission**; these are essential submission requirements."*
- **代码要求是"取决于贡献类型"的**：当主要贡献是**可复用的可执行产物**（benchmark suite、evaluation environment、data generator、**software tool**）时，**代码发布是强制的**：*"code release is **required** at submission when the primary contribution is a reusable executable artifact… whose functionality must be inspected in order to evaluate the scientific claims."*
- **不合规直接 desk reject**：*"Code should be **documented and executable**. **Non-compliance justifies the desk rejection of the paper.**"*
- **Croissant 元数据**：必须使用 Croissant 机器可读格式，**且今年要求同时提供 core 与 Responsible AI (RAI) 字段**。
- **关键日期**：摘要 **2026-05-04**、全文 **2026-05-06**（AoE）、作者通知 **2026-09-24**、投稿系统 **2026-04-15** 开放。
- **E&D Track Chairs**：Konstantina Palla、Jessica Schrouff、Alexandre Drouin、Lijun Wu、Joaquin Vanschoren。

### 七、出版界的检测部署现状（2026 年中）

来源：CASRAI *AI Detection Tools Adoption in Academic Publishing: 2026 Trends*（2026-07-23）。

CASRAI 把"AI 检测"拆成**三类不同实践**，这个拆分对阙疑的 Related Work 很有用：

1. **Text-origin screening**（判断文本是否由 LLM 生成）——"the one with the most documented accuracy problems"；
2. **AI-assisted integrity screening**（图像操纵、统计异常、未披露的作者变更、论文工厂签名）——**不回答"是不是 AI 写的"**；
3. **Disclosure compliance checks**（检查稿件是否含规定的 AI 使用披露声明）。

**已核实的大规模部署**：

- **Elsevier — Check Integrity**：2026-03 新闻稿宣布在**近 2,000 本期刊**推广，筛查出版伦理违规（未授权作者变更、未披露的编辑利益冲突），**把被标记的稿件转给专门的诚信分析员人工复核，而不是自动拒稿**。
- **Springer Nature — Geppetto**：自研工具，逐节检查内部一致性，估计稿件各节是否含 AI 生成的"tortured phrase"或无意义文本；内部推广后（约 2024 年）**在投稿后不久识别出数百篇伪造论文**；2025-04 捐给 **STM Integrity Hub**。配套工具 **SnappShot** 用于识别问题图像。
- **STM Integrity Hub**：行业共享筛查基础设施（图像筛查、文本相似度、AI 内容信号）。
- **COPE 立场**："Authorship and AI tools"（**2023-02** 发布，至今无实质变化）：**AI 工具不能列为作者**。ICMJE、COPE、WAME 自 2023 年起一致持此立场。
- **在研标准**：COPE + WCRIF + 国际科学理事会（ISC）+ STM + 全球青年科学院（GYA）正在制定联合的 **"Global Reporting Standard for AI Disclosure in Research"**（俗称 **"Vancouver Standard"**，关联 2026-05 在温哥华举行的世界科研诚信大会）。**截至 2026 年中仍在公开征询阶段，尚未生效——不可当作已强制标准引用。**
- CASRAI 明确：**ICMJE 与 COPE 都不背书任何具体商用检测工具**。

### 八、被拒稿作者的第一手叙述

来源：机器之心 / 发现 AI 转载的 Reddit 原帖（2026-06-04）。

作者的核心指控（逐字）：

> "我被告知，作出拒稿判断时参考的材料包括：**检测器输出结果和作者提交的 AI 使用声明**。"
> "如果一个较高的检测分数被用来判断作者的声明「不一致」，而这种「不一致」又被用来证明拒稿合理，那么检测器就不只是一个辅助工具了。**它实际上成了裁决过程中的决定性因素。**"
> "真正的目标群体是 NeurIPS 2026 Position Paper 的投稿，而这些投稿的**真实写作过程并没有已知的 ground truth**。"
> "**在一个分布上测得的假阳性率，并不会自动迁移到另一个分布上。**"
> "我用 Pangram 跑了几篇 2026 年近期的论文，作者包括 NeurIPS Position Paper Track 的几位主席。Pangram 给出的结果包括：**69% AI、45% AI、36% AI 和 24% AI**。"

**这条论证与阙疑的论点同构**：阙疑的核心主张是"判决必须可复算、证据可追"；而 NeurIPS 这套流程的致命弱点恰恰是**把概率估计当作了 ground truth，且没有可复算的中间证据**。

---

## 对阙疑的 3 条具体行动

1. **把"provenance audit trail"变成仓库里的一等公民，因为 NeurIPS 官方已经预告它会成为默认要求。** 具体做法：新建 `_provenance/` 目录（与 `_arch_v47/` 同级），实现 `tools/provenance_log.py`，每条记录固定五个字段 `{timestamp_iso, artifact_path, artifact_sha256, ai_involvement: none|proofread|copyedit|structural|generated, human_edit_note}`，并生成 `_provenance/INDEX.md`（按时间排序、可直接导出为投稿附录）。**依据**：NeurIPS PPT 官方原文 *"Authors whose submissions show significant AI involvement must provide an audit trail that clearly demonstrates that they complied with the policy. **We expect that in future years this kind of audit trail will become a default.**"*；以及官方要求的三个版本节点（pre-AI / post-AI / final）。**阙疑应当直接按这三个节点组织自己的版本历史**，时间点：**2026-10 底前把工具写完并回溯补齐 `_arch_v47/` 之后的记录**（`_arch_v47/` 本身不必补，但从此之后的每一份论文相关产物必须留痕）。
2. **立刻做"赛道风险体检"，并据此决定 E&D 还是改投。** 已知硬数据：**E&D 2026 有 43.7% 的投稿 Pangram 分数 ≥50%，9.3% ≥90%**——这意味着 E&D 赛道本身处在官方重点监控范围内。具体做法：用 Pangram 免费额度（2,000 词/日）对阙疑的 Abstract + Intro + Method 分三次实测，记录 `{日期, 版本, 分数, 窗口策略}` 到 `_provenance/detector_selfcheck.md`；**同时把论文正文的写作方式从"LLM 起草"改成"人写骨架 + AI 只做 proofreading/light copyediting"**（官方 Table 4 明确：这两类在实验中 **Pangram 从未判为 AI**）。**触发条件**：若自测分数 ≥0.5，暂停投稿并重写正文；若 ≥0.9，必须整篇重写。时间点：**2027-03 前完成首轮体检**（留出重写时间），2027-05-06 投稿前复测。
3. **把"检测器的循环论证"写成阙疑论文的核心 motivation 段落，并引用官方原文。** 在 Introduction 第 2 段加入：NeurIPS PPT 2026 的流程是"检测器输出被当作 ground truth，与作者声明冲突时声明失效"（Reddit 作者的指控 + 官方 *"externalises the cost of verifying that work, imposing it on reviewers"*）；而**官方自己承认"分数是窗口被标记的比例"而非"文本的 AI 占比"**，且**换窗口大小就能把 ≥90% 的比例从 42.7% 压到 12.7%**——**同一批论文、同一个模型，只改一个超参数，18.4% 的拒稿率就会大幅改变**。这正是"判决不可复算"的教科书案例。然后接上阙疑的反命题：**判决必须绑定到可公开复算的规则与证据，且账本 append-only 不可回改**。时间点：**2026-11 前写完这段**（它是 Introduction 的骨架，越早定越好）。

---

## 盲区（诚实标注）

- **NeurIPS 官方博客里 969 与 971 两个论文数并存**（正文 969、Table 1 写 971），官方**未说明原因**；我采用正文的 969 作分母。
- **Table 1 中 "NeurIPS E&D 2026 = 996 篇"这个数字与本文件另一处"E&D 2026 三项数字全未公开"的说法需要核对**——该表是官方博客给出的 AI 检测统计（996 篇送检），不等于 E&D 的投稿总数；**E&D 2026 的总投稿数与录用数至今未公开**。
- **窗口实验只有 10 篇样本**，官方自己也写明 *"While these experiments were conducted with only 10 text samples…"*，因此 Table 2/Table 3 的结论**样本量极小**，不能当作稳定估计。
- **"Pangram 假阳性率 < 0.1%"是官方转述的"内部与外部审计"结果，我未找到该审计的公开报告**；**"ICLR 2026 已录用论文中只有 1% 被判 AI 生成"这一数字也未找到原始出处**。
- **ICLR 2026 用的两个检测器名称未公开**（原文只说 "two LLM content detectors"），因此无法评估其阈值与版本。
- **Reddit 原帖我只读到机器之心的中文转述**，未打开 Reddit 原文核对；且该帖作者的"主席论文 69%/45%/36%/24%"是**说明性检查**，作者自己也说 *"我并不是说这些论文就是 AI 写的"*。
- **CASRAI 页面含联盟营销链接**（affiliate links），其推荐部分需打折看待；但其中关于 Elsevier/Springer Nature/COPE 的事实性陈述有明确出处。
- **"Vancouver Standard"尚未生效**，若引用需标注"在研"。
- 本文件**未实测阙疑任何文本**，其 Pangram 分数未知。

---

## 来源

1. NeurIPS Blog, *AI-Generated Papers in the NeurIPS 2026 Position Paper Track* — https://blog.neurips.cc/2026/06/02/ai-generated-papers-in-the-neurips-2026-position-paper-track/ — 政策原文、Pangram v3.3.2、250–350 词窗口、概率 >0.75 标记、28.2%（273/969）、178 篇（18.4%）不予申诉拒稿、123 篇（12.7%）需 6-15 前举证、Table 1 跨会议对比、Table 2/3 窗口实验、Table 4 允许/边界/不允许清单、Table 5 决策阈值、audit trail 将成为默认 — Alex Lu / Seth Lazar / David Rügamer / Stanley Hua / Kate Metcalf — 2026-06-02
2. NeurIPS Blog, *Introducing the Evaluations & Datasets Track at NeurIPS 2026* — https://blog.neurips.cc/2026/03/23/introducing-the-evaluations-datasets-track-at-neurips-2026/ — "evaluation itself becomes an object of scientific study"；"Submissions need not introduce a new model or outperform prior work"；ED Track Chairs 名单 — 2026-03-23
3. NeurIPS 2026, *Call For Evaluations & Datasets 2026* — https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets — 默认双盲、代码在投稿时即可执行、Croissant core+RAI 字段、不合规即 desk reject、关键日期 2026-05-04 / 05-06 / 09-24 — NeurIPS，2026
4. ICLR Blog, *A Retrospective on the ICLR 2026 Review Process* — https://blog.iclr.cc/2026/03/31/a-retrospective-on-the-iclr-2026-review-process/ — 19,525 投稿 / 779 desk reject / 5,042 撤稿 / 13,763 决定 / 76,139 评审 / 18,054 审稿人 / 5,355 录用 / 27.4%；两个检测器且需"两个都判 LLM"才标记；幻觉引用检测的显著误报率；每篇至少 3 人复核；设申诉通道 — ICLR 2026 Program Chairs — 2026-03-31
5. ICLR Blog, *ICLR 2026 Response to LLM-Generated Papers and Reviews* — https://blog.iclr.cc/?p=1055/ — "Papers that make extensive usage of LLMs and do not disclose this usage will be desk rejected"；"we will only take action if an AC or SAC identifies concrete evidence" — 2025-11-19
6. ICLR Blog, *Making Google's Paper Assistant Tool (PAT) available to ICLR submitters* — https://blog.iclr.cc/2026 — 一边用检测器筛稿、一边提供官方写作助手 — ICLR 2026
7. CASRAI, *AI Detection Tools Adoption in Academic Publishing: 2026 Trends* — https://casrai.org/guides/ai-detection-tools-adoption-academic-publishing-2026-trends — Elsevier Check Integrity 覆盖近 2,000 本期刊（2026-03）、Springer Nature Geppetto 识别数百篇伪造论文并捐赠给 STM Integrity Hub（2025-04）、SnappShot、COPE "Authorship and AI tools"（2023-02）、Vancouver Standard 仍在征询 — 2026-07-23
8. 机器之心 / 发现 AI，*NeurIPS 用 AI 检测，说我的论文是 AI 生成的* — https://www.faxai.cn/archives/9784（另见 https://news.qq.com/rain/a/20260604A03YVD00）— Reddit 被拒稿作者第一手叙述；"检测器成了裁决过程中的决定性因素"；主席论文得分 69%/45%/36%/24% — 2026-06-04
9. CASRAI, *NeurIPS 2026 Pangram AI-Detector Desk Rejections* — https://casrai.org/news/neurips-2026-pangram-ai-detector-desk-rejection-controversy — "automated desk-reject gate with no appeal" — 2026-07-23
10. StrictCite, *NeurIPS Desk-Rejected 178 Position Papers for Being "AI-Generated"* — https://strictcite.com/blog/neurips-2026-position-paper-pangram-ai-detection — 三组判据 77/79/22；负对照 FAccT 2022 得 0.0%；"One is an audit; the other is an opinion with a confidence interval." — 2026-09-08
11. aiweekly.co, *NeurIPS Rejects 18.4% of Position Papers via Pangram AI Tool* — https://aiweekly.co/alerts/neurips-rejects-184-of-position-papers-via-pangram-ai-tool — 主席姓名 Alex Lu / Seth Lazar / David Rugamer — 2026-06-04
12. Paper Checker Hub, *AI Detection for Academic Conferences: Paper and Presentation Verification 2026* — https://hub.paper-checker.com/blog/ai-detection-academic-conferences-paper-presentation-verification-2026/ — 会议已把 AI 检测当作评审前的一轮筛查 — 2026-09
13. ACL Admin Wiki, *ACL Policy on Publication Ethics* — https://www.aclweb.org/adminwiki/index.php/ACL_Policy_on_Publication_Ethics — 综合 IEEE/ACM/ACL 2023/COLM 的出版伦理政策 — 2026-08-17
14. NeurIPS 2026, *Evaluations & Datasets FAQ* — https://neurips.cc/Conferences/2026/EvaluationsDatasetsFAQ — 赛道选择的官方说明 — 2026-04-07
