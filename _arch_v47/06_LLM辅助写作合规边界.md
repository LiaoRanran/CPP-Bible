# 方向 06：LLM 辅助学术写作的合规边界

## 核心结论

1. **"AI 不能当作者"是唯一真正全球一致的一条，八家机构零例外；但"同一件事该不该声明、声明放哪"分歧极大，最极端的一组对比是"用 AI 润色语言"：** Elsevier **明确豁免**（*"Basic grammar, spelling and punctuation checks … No — explicitly exempted"*）；IEEE 说 *"disclosure … is **recommended**"*（建议而非强制）；NeurIPS **Main Track** 说 *"The use of spell checkers and grammar suggestions, aid for editing purposes, and basic code assistance **does not need to be documented**"*；**ACM 更激进**——*"When using Artificial Intelligence to assist with writing an ACM submission, **ACM no longer requires the disclosure of information regarding the use of AI**"*；**而 Springer Nature 把"extensive copy editing or writing support"划入 Amber（须披露）**、**ICLR 2027 完全没有豁免条款**、**NeurIPS PPT 2026 则只允许 "copy-editing or similar peripheral changes"**。**同一动作，五种处置。**

2. **NeurIPS PPT 2026 官方发布的 12 场景合规表（Table 4）是全领域唯一一份"逐场景判合规"的量化清单，而且官方做了实证验证：所有 permissible 场景 Pangram 一例都没判成 AI；所有 clearly impermissible 场景都被判成 AI。** 四档分类为：**Clearly permissible 2 个**（Proofreading、Light copyediting）、**Borderline permissible 4 个**（Heavy copyediting / line editing、Structural rewriting、Hybrid revision、Translation / backtranslation）、**Clearly impermissible 4 个**（Generation from a single-sentence human plan、Substantive AI rewriting、Original AI-authored passage、Human edits AI work）、**Diagnostic tests 2 个**（AI residue、Partial AI completion）。**最实用的一条数字**：*"In our experiment on partial AI completions, **Pangram never classified AI completions of 20% or less as AI-generated**."*

3. **对阙疑最致命的合规落差在"AI 用于实现方法"这一条上——而这恰好是阙疑的主战场。** NeurIPS **Main Track** Handbook 要求 *"The use of agents and/or LLMs **in implementing the method** should be described in the **experimental setup section** (or equivalent) **if it is an important, original, or non-standard component** of the approach"*；**ACM 要求更严**——凡涉及 *"coding, implementing models, running simulations, data analysis, testing, validating results, deploying software, archiving data and code for reproducibility"* 的 AI 使用，*"the specific use(s) of AI tools **must be described in detail in the methods section**"*。**阙疑的内核 `gate_engine.py` 有 3826 行、`_arch_v46/` 有 595 个 .py 工具、75+ 份 AI 生成文档——按 ACM 口径，这些 AI 参与的实现工作全部落在"必须详细披露在 Methods"的范围内。** 而按 NeurIPS 口径，只要"用 LLM 写代码"被判定为"important / original / non-standard"，也必须在 experimental setup 里写清。

---

## 精确数字与案例

### 一、NeurIPS PPT 2026 的 12 类 AI 使用场景合规表（Table 4 逐字）

来源：NeurIPS 官方博客 *AI-Generated Papers in the NeurIPS 2026 Position Paper Track*（2026-06-02）。表标题为 **"AI use cases and permissibility"**。

| 合规档位 | 场景（Use Case） | 该场景在测什么（What it tests，逐字） |
|---|---|---|
| **Clearly permissible** | **Proofreading** | "Request that an LLM edits only spelling, punctuation, grammar, and citation-format cleanup." |
| **Clearly permissible** | **Light copyediting** | "Request that an LLM edits only local clarity, concision, awkward phrasing, and sentence-level polish, with **no substantive change**." |
| **Borderline permissible** | **Heavy copyediting / line editing** | "Request that an LLM edits large wording changes and sentence restructuring, while **preserving the same claims and reasoning**." |
| **Borderline permissible** | **Structural rewriting** | "Request that an LLM reorganizes paragraph or argument presentation while **preserving the human's ideas**." |
| **Borderline permissible** | **Hybrid revision** | "Human and AI both materially shape the prose, including back-and-forth assistant use or human paraphrasing after AI edits. Tested with **Codex, and 5 editing turns (original, AI edits, human edits, AI edits, human edits)**." |
| **Borderline permissible** | **Translation / backtranslation** | "Request that an LLM translates between languages, so that meaning is preserved, but **surface wording may be extensively replaced**." |
| **Clearly impermissible** | **Generation from a single-sentence human plan** | "A human writes a **one-sentence plan/thesis**, then AI generates the **full passage** from it." |
| **Clearly impermissible** | **Substantive AI rewriting** | "Request that an LLM changes **claims, reasoning, framing, or argumentative structure**." |
| **Clearly impermissible** | **Original AI-authored passage** | "Request that an LLM writes a new position-paper-like passage from examples, topic, or instructions." |
| **Clearly impermissible** | **Human edits AI work** | "Human makes **minor edits** to an original AI-authored passage." |
| **Diagnostic tests** | **AI residue** | "Insert obvious chatbot artifacts or AI-styled residue into otherwise human text (e.g. 'sure, here is your paragraph:)')" |
| **Diagnostic tests** | **Partial AI completion** | "AI receives part of the original human text and completes the rest. Conditions: AI completes **5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95%**" |

**官方实证结论（逐字，本方向最值钱的一段）**：

> "For all of the permissible uses, **Pangram did not classify any as AI-generated**, despite a substantial change in the text (Figure 1A). Meanwhile, **clearly impermissible use cases were flagged by Pangram as AI-generated**. In our experiment on partial AI completions, **Pangram never classified AI completions of 20% or less as AI-generated** (Figure 1B). **While these experiments were conducted with only 10 text samples**, the findings suggest that **papers with very high Pangram AI scores were not compliant with our AI use policy**."

**配套的窗口敏感性数据（Table 2，10 篇 ChatGPT 生成的 "position paper"）**：

| 窗口策略 | 平均 Pangram AI score | Recall ≥0.5 | ≥0.7 | ≥0.9 | =1.0 |
|---|---|---|---|---|---|
| small（≈50 词） | **61.8%** | 70% | 30% | 0% | 0% |
| medium（≈100 词） | **91%** | 100% | 100% | 70% | 0% |
| **default（≈250–350 词）** | **100%** | 100% | 100% | 100% | 100% |

**⚠️ 三条必须同时说出的限制**：**(a)** 12 场景实验**只有 10 篇样本**（官方自己写 "only 10 text samples"）；**(b)** 逐场景的 Pangram 分数**官方没有给数值表**，只以 Figure 1A / 1B 图形呈现；**(c)** 这是 **Position Paper Track** 的政策，官方明确提醒 *"Note that the Position Paper Track's LLM policy **differs from the Main Program's** LLM policy."*

**对阙疑的映射（把 12 场景翻译成阙疑自己的动作）**：

| 阙疑的实际动作 | 落在哪一档 | 依据 |
|---|---|---|
| 用 LLM 检查拼写、标点、引用格式 | **Clearly permissible** | Proofreading |
| 让 LLM 只做"句子级清晰度/精简"改写，不改断言 | **Clearly permissible** | Light copyediting |
| 让 LLM 大幅重写措辞但保留全部 claim 与推理链 | **Borderline permissible** | Heavy copyediting / line editing |
| 让 LLM 重排段落/论证顺序，但观点是自己的 | **Borderline permissible** | Structural rewriting |
| 人写→AI 改→人改→AI 改→人改（5 轮） | **Borderline permissible** | Hybrid revision（官方用 Codex 测过） |
| 中译英（意思保留、表层措辞大量替换） | **Borderline permissible** | Translation / backtranslation |
| 只写一句 thesis，让 AI 生成整段 | **Clearly impermissible** | Generation from a single-sentence human plan |
| 让 LLM 改 claim / 推理 / 框架 / 论证结构 | **Clearly impermissible** | Substantive AI rewriting |
| 让 LLM 从零写一段"position-paper 风格"的文字 | **Clearly impermissible** | Original AI-authored passage |
| 对 AI 原文只做小幅人工编辑 | **Clearly impermissible** | Human edits AI work |

### 二、八家机构"是否算作者 / 是否要声明 / 声明放哪 / 豁免"逐条对照

| 机构 | AI 能否当作者 | 是否必须声明 | **声明放哪** | 豁免条款（逐字） |
|---|---|---|---|---|
| **COPE** | **不可** —— "AI tools cannot be listed as an author of a paper."；理由："they cannot take responsibility for the submitted work. As **non-legal entities**, they cannot assert the presence or absence of conflicts of interest nor manage copyright and license agreements." | 必须（写作、生成图像/图形元素、数据收集与分析三类都算） | **"in the Materials and Methods (or similar section) of the paper"** | 无 |
| **ICMJE** | **不可** —— "Chatbots (such as ChatGPT) and other AI-assisted tools should not be listed as authors because they **cannot be responsible for the accuracy, integrity, and originality** of the work" | 必须（**投稿时**即须声明） | **"in both the cover letter and the submitted work in the appropriate section"** ——**两处都写** | 无。且警告："**Nondisclosure of AI use may require corrective action and may be construed as misconduct** in some circumstances." |
| **Elsevier** | **明确不可** —— "generative AI tools … **cannot be credited as an author or co-author** under any circumstances" | 必须（若用于文稿准备） | **"at the end of the manuscript, immediately before the reference list"**，标题固定为 *"Declaration of generative AI and AI-assisted technologies in the manuscript preparation process"* | **"Basic grammar, spelling and punctuation checks (including standard spell-checkers) — No — explicitly exempted"** |
| **Springer Nature** | **不可** —— Red 档明确列 *"Assigning authorship or accountability to AI systems or tools"* 为 not permitted | **三档制**：Green **Permitted**（披露"enhances trust"）；Amber **Permitted with human oversight, verification, and transparency through disclosure**；Red **Not permitted** | 按 Springer Nature 的框架**不指定单一章节**，但要求"transparent declaration"；Nature 系列期刊此前明确 *"Use of an LLM should be properly documented in the **Methods section** (and if a Methods section is not available, in a suitable [alternative section])"* | **无普遍豁免**——"Using an LLM to polish or refine the language" 属 **Green（Permitted，仍须披露）** |
| **IEEE** | 未在 AI 指南中单列（但要求作者是可识别的自然人） | 必须（AI 生成的 text / figures / images / code） | **"in the acknowledgments section"** | **"The use of AI systems for editing and grammar enhancement is common practice and, as such, is generally outside the intent of the above policy. In this case, disclosure as noted above is recommended."** |
| **ACM** | **明确不可** —— "generative AI software tools **cannot be listed as authors on ACM Works under any conditions**." | **分裂式**：用于**研究**→必须；用于**写作**→**不再要求** | **研究用途**："**must be described in detail in the methods section**"；**写作用途**："ACM **no longer requires** the disclosure" | **写作辅助整体豁免披露**（2026-05-14 版政策的新变化） |
| **NeurIPS Main Track 2026** | **不可** —— "as you are the one taking responsibility for the work, **agents and LLMs cannot be authors**." | **有条件必须**：仅当 LLM 使用是方法的"**important, original, or non-standard**"组成部分 | **"the experimental setup section (or equivalent)"** | **"The use of spell checkers and grammar suggestions, aid for editing purposes, and basic code assistance **does not need to be documented**."** |
| **NeurIPS PPT 2026** | 隐含不可（要求 substantially human-written） | 必须（投稿时声明如何使用 AI，并 attest 未违规） | **投稿表单** + 申诉时提交三节点版本历史 dossier | **"AI is used only for copy-editing or similar peripheral changes to the main text"** —— 仅此一项 |
| **ICLR 2027** | 未在 AI 政策中单列 | 必须（**正文强制章节 + 投稿表单**） | **"a mandatory section in their paper (this section will not be counted towards the page limit)"** | **无任何豁免**；但分 **Required / Recommended** 两档，后者措辞更宽松 |

**四条可以直接引用的"权威理由"（各机构为什么说 AI 不能当作者，理由几乎完全相同）**：

> COPE: "AI tools cannot meet the requirements for authorship as they **cannot take responsibility** for the submitted work."
> ICMJE: "they cannot be responsible for the **accuracy, integrity, and originality** of the work."
> Elsevier: "authorship carries responsibilities and accountability … that **can only be attributed to and performed by a human**."
> ACM: "**They are an identifiable human being.** Anonymous authorship is not permitted…"
> NeurIPS Main Track: "as **you are the one taking responsibility** for the work, agents and LLMs cannot be authors."

### 三、Springer Nature 的 Green / Amber / Red 三档风险框架（最有操作价值的一份）

来源：`group.springernature.com/gp/group/ai/ai-guidance-for-researchers-editors-reviewers`。这是本方向唯一一份**按"风险等级"而非"任务类型"分类**的官方框架。

**框架的提问方式（逐字，这是它的方法论核心）**：

> "**Rather than focusing on whether AI has been used**, the policies ask each user to consider:
> - how AI has been used
> - the potential impact of that use
> - the level of risk introduced
> - whether appropriate human oversight has been maintained
> - whether transparency and accountability have been preserved"

**四条 Core expectations（逐字）**：

> 1. "**Human accountability is non-transferable**: Accountability for scholarly content, evaluation, and editorial decisions **cannot be delegated to AI systems**."
> 2. "**AI may support, but must not replace, scholarly judgement**: AI can assist clarity, efficiency, and exploration, but **must not determine conclusions, evaluations, or decisions**."
> 3. "**Transparency creates trust and confidence**"
> 4. "**Confidentiality and data protection are mandatory**"

**三档完整对照（逐字）**：

| 档位 | 定义 | 期望（Expectations） | 例子（Examples） | 合规与披露 |
|---|---|---|---|---|
| **Green — Permitted**（Assistive AI use） | "AI use that supports expression, organisation, or efficiency **without influencing scientific, scholarly or evaluative judgement**." | "AI use is likely to be **reversible and verifiable**"；"AI use **does not introduce new intellectual content**"；"Accountability … remains clearly human" | "Using an LLM to **polish or refine the language**"；"Suggesting structure or formatting of manuscript sections"；"Translation, structuring or clarifying reviewer comments"；"Comparing methodological options"；"Stress-testing research questions"；"**Data cleaning and deduplication**" | **Permitted**。"Disclosure enhances trust and transparency" |
| **Amber — Exercise caution**（Evaluative or interpretive AI use） | "AI use that **may influence interpretation, framing, emphasis, or evaluative judgement**, but remains under human control." | "AI contributes to reasoning or critique"；"AI **does introduce new intellectual content** and requires verification and oversight"；"Human judgement and accountability must be **demonstrable**" | "Suggesting analytical, experimental or methodological approaches"；"Drafting explanatory summaries"；"Comparing results to existing literature"；"**Extensive copy editing or writing support**"；"Pattern identification in exploratory data analysis"；"Explaining outputs from statistical models in plain language"；"**Recommending statistical tests or modelling approaches**" | **Permitted with human oversight, verification, and transparency through disclosure**。"If AI materially influences evaluative judgement, accountability must remain clearly human-led and defensible." |
| **Red — Not permitted** | "AI use that is **opaque** or **replaced accountable human contribution**, generates **unverifiable outputs**, compromises **confidentiality or integrity**, or **violates applicable laws**." | — | "**Generating hypotheses, analyses or conclusions and presenting them as human-derived**"；"**Fabricating data, citations or results**"；"**Using an LLM to generate core research reasoning without disclosure**"；"**Assigning authorship or accountability to AI systems or tools**"；"**Delegating peer review to an LLM**"；"**Creating photorealistic images (deepfakes)**" | **Not permitted** |

**对阙疑最直接的一条**：**"Data cleaning and deduplication" 在 Springer Nature 是 Green（可做，须披露）；"Recommending statistical tests or modelling approaches" 与 "Extensive copy editing or writing support" 是 Amber（须人工监督 + 披露）；"Generating hypotheses, analyses or conclusions and presenting them as human-derived" 与 "Fabricating data, citations or results" 是 Red（禁止）。** 阙疑的 452 条判决账本、67 条规则、四态判决逻辑属于"hypotheses / analyses / conclusions"——**如果用 LLM 生成这些内容再当作人类产出呈现，直接落入 Red。**

### 四、ICLR 2027 的 Required / Recommended 双清单（唯一"任务级"的官方分类）

来源：`iclr.cc/Conferences/2027/AIPolicyForAuthors`。这是所有机构里**唯一把"哪些任务必须披露、哪些只是建议披露"逐条列出**的官方清单。

**Required（必须披露，逐字）**：

> "Generate synthetic data sets, help develop theoretical models or conceptual frameworks, formulate mathematical claims, provide critical ingredients for proving mathematical claims, assist in the writing of proofs, propose or refine hypotheses, design or provide feedback on research methodology or experiments, **implement methods**, assist with translation, **clean and reformat dataset**, support qualitative and thematic data analysis, **interpret results**."

**Recommended（建议披露，逐字）**：

> "Formulate questions for surveys or interviews, create or modify scientific figures or images, suggest experimental parameters, **create or edit software code**, creation of artifacts, **draft parts of a research paper**, transcribe recordings of research material, summarize or analyse existing literature, discover research topics or identify gaps, brainstorming, sourcing/searching for information, **edit a research paper to improve readability**, identify relevant literature, format references, suggest a structure for a research paper, propose a title or keywords for a research paper."

**官方 boilerplate（逐字，可直接填用）**：

> "In this work, we used generative AI tools for **<tasks with required disclosure>**. We have not used generative AI tools for **<other tasks with required disclosure>**, and **<the rest of the required disclosure tasks>** are not applicable to this work. Additionally, we used generative AI tools for **<tasks with recommended disclosure>**. **We have reviewed all AI-assisted work.** [Elaborate…]. **We take responsibility for the final content of this work, including text, claims or artifacts produced with the aid of generative AI.**"

**ICLR 的责任定性（逐字，比处罚更值得注意）**：

> "**a substantial falsehood, instance of plagiarism, or misrepresentation produced by an LLM would be considered a Code of Ethics violation on the part of the paper's authors, and might lead to desk rejection of the paper.**"

### 五、一处显著的政策分歧：ACM 2026-05-14 版"写作辅助不再需要披露"

这是本方向**最反直觉、也最容易被误引用**的一条。ACM 在 **2026-05-14** 更新的 *Policy on Authorship* 里，把 AI 使用拆成两类，并对写作辅助**取消了披露要求**：

> 1. "When using Artificial Intelligence to **conduct research**, including the design and methodology of the research project, creation and selection of data sources, designing experiments, generation and collection of data, **coding, implementing models, running simulations, data analysis, testing, validating results, deploying software, archiving data and code for reproducibility**, or any other aspects of the research lifecycle that are **directly relevant to the conclusions** of the research underlying the Work, the specific use(s) of AI tools **must be described in detail in the methods section of the Work**. This includes the creation of artifacts that are directly relevant to the conclusions of the research, such as **code, datasets, and charts or figures** that rely on the AI tools."
> 2. "When using Artificial Intelligence to **assist with writing** an ACM submission, **ACM no longer requires the disclosure of information regarding the use of AI** (as distinct from AI used in the conduct of the research itself, addressed in item 1 above)."

**ACM 的政策理由（逐字，这段值得整段引用）**：

> "**Rather than attempt to limit the use of Artificial Intelligence (AI) to conduct research or report on the results of that research by placing expectations on authors to disclose all uses of large language models in their Works, this updated Policy attempts to set clear expectations for their responsible use**, as follows:"

**⚠️ 一个仍在流传的过时版本**：ACM RESPECT 2026 的政策页仍引用**旧版 ACM 口径**：

> "The use of generative AI tools and technologies to create content is permitted but **must be fully disclosed in the Work**. For example, the authors could include the following statement in the **Acknowledgements** section of the Work: **ChatGPT was utilized to generate sections of this Work, including text, tables, graphs, code, data, citations, etc.**). If you are uncertain about the need to disclose the use of a particular tool, **err on the side of caution**, and include a disclosure in the acknowledgements section of the Work."

**这说明 ACM 内部/会议层面的口径尚未完全同步**——**对阙疑的实务建议是：按"更严的那一版"执行（即写完整披露），因为遵循更严口径永远不会违反更松口径。**

**ACM 的两条附加硬规则（逐字）**：

> "**All named authors on an ACM submission will be held responsible and accountable for any problematic content contained in the submission regardless of the source** of that problematic content: … *prior to publication* … ACM reserves the right to **reject submissions in their entirety and impose additional penalties**. … *after publication* … ACM reserves the right to **retract the published Work in its entirety**."

> "**Anonymous Authorship** – when all or some authors are unnamed or listed as 'Anonymous' and do not provide full contact information to ACM." 属于不可接受的署名行为（**注意：ACM 允许笔名/化名，只要提供准确联系信息**）。

### 六、NeurIPS Main Track 与 PPT 的差异（同一年、同一会议、两套政策）

| 维度 | NeurIPS **Main Track** 2026 | NeurIPS **PPT** 2026 |
|---|---|---|
| 写作辅助豁免 | **有**：*"spell checkers and grammar suggestions, aid for editing purposes, and basic code assistance **does not need to be documented**"* | **无豁免**，只允许 *"copy-editing or similar peripheral changes"* |
| 披露位置 | **"experimental setup section (or equivalent)"** | **投稿表单** + 申诉 dossier |
| 触发条件 | 仅当 LLM 使用是方法的 *"important, original, or non-standard component"* | 一律须声明"如何使用 AI"并 attest |
| 检测手段 | 无公开的检测器筛查流程 | **Pangram 3.3.2 全量筛查 + 178 篇 desk reject** |
| 其他禁令 | *"attempts at **prompt injections** as well as other attempts to **manipulate reviewing** is strictly prohibited"*；*"There have been many cases of **hallucinated citations** in literature review, which **violates the NeurIPS Code of Conduct**"* | 同（Code of Conduct 适用于全会议） |

**官方对"两套政策并存"的提醒（逐字）**：

> "Note that the Position Paper Track's LLM policy **differs from the Main Program's** LLM policy. **Authors are responsible for understanding policy pertaining to the specific track they are submitting to, and abiding by it.**"

**⚠️ 对阙疑的关键提示**：阙疑投的是 **E&D（Evaluations & Datasets）Track**，属于 **Main Program 体系**（D&B 更名而来），**不是 PPT**。因此**最可能适用的是 Main Track 口径**（豁免 spell check / grammar / basic code assistance、披露放 experimental setup section）——**但 E&D 是否有自己的附加政策，我没有读到文本**（见盲区）。**"Main Track 政策"这个推断本身就是本方向最大的不确定点。**

### 七、跨机构"声明放置位置"的完全分歧图（最容易踩坑的一节）

| 放置位置 | 采用该位置的机构 |
|---|---|
| **参考文献列表之前**（专门小节） | **Elsevier** |
| **致谢（Acknowledgments）** | **IEEE**；ACM 旧版口径；ACM RESPECT 2026 页面 |
| **Materials and Methods（或类似章节）** | **COPE**；**ACM**（研究用途）；**Taylor & Francis**（有 Methods 时）；Nature 系列期刊 |
| **Acknowledgments（无 Methods 时）** | **Taylor & Francis**（无 Methods 时） |
| **投稿信 + 正文，两处** | **ICMJE** |
| **正文强制章节（不计页数）** | **ICLR 2027** |
| **experimental setup section** | **NeurIPS Main Track 2026** |
| **投稿表单 + 申诉 dossier** | **NeurIPS PPT 2026** |
| **不指定单一章节，按 Green/Amber/Red 分级披露** | **Springer Nature** |

**结论：不存在"一份声明通用所有机构"的可能。** Taylor & Francis 的披露规则提供了一个具体的反例：它要求**必须写明工具的具体版本号**——*"**The specific tool used, including its version number** (e.g. 'ChatGPT-4' rather than just 'ChatGPT', or 'Grammarly's generative AI feature' rather than just 'Grammarly') — **a generic reference to 'AI assistance' without naming the tool does not satisfy the requirement**."* **而 Elsevier 的模板只要求 `[NAME OF TOOL / SERVICE]`，未要求版本号。** 一份按 Elsevier 写的声明直接投 T&F，会因缺少版本号而不合规。

---

## 对阙疑的 3 条具体行动

1. **在 `paper/` 下建立 `compliance_matrix.md`，把上面"八家机构 × 四个问题"的对照表落成项目内的活文档，并在每一行标注"本项目适用/不适用 + 依据 URL + 读取日期"。** 具体四列为 `机构 | AI 能否当作者 | 是否必须声明 | 声明放哪 | 本项目处置`。**必须明确写下"阙疑投的是 E&D Track（Main Program 体系），不是 PPT"这一条，并注明该推断的依据与不确定性。** 另外必须单独列一行 **ICLR 2027**（作为备选投稿目标），因为它的 *"mandatory section … not counted towards the page limit"* 与 Required/Recommended 双清单**对页数预算有直接影响**。**对应文件：`paper/compliance_matrix.md`（新建）。时间点：2026-12 前。**

2. **把"哪些 AI 辅助动作属于 Required 披露"变成代码层的强制检查，而不是靠记忆。** 具体做法：在现有的 595 个 .py 工具中新增 `tools/check_ai_disclosure.py`，规则为——**扫描 `provenance/ai-tool-log.md` 的每一行，若 `Task` 字段命中 ICLR Required 清单的关键词（`implement methods` / `clean and reformat dataset` / `interpret results` / `assist with translation` / `propose or refine hypotheses` / `design … methodology`）或 ACM 研究用途清单（`coding` / `implementing models` / `running simulations` / `data analysis` / `testing` / `validating results` / `deploying software` / `archiving data and code`），则该行必须在 `paper/disclosure.md` 中有对应条目，否则脚本非零退出。** 依据是 ACM 的 *"must be described in detail in the methods section"* 与 ICLR 的 Required 清单。**对应文件：`tools/check_ai_disclosure.py`（新建）+ 接入 CI。时间点：2027-01 前。**

3. **按 Springer Nature 的 Green/Amber/Red 框架，为阙疑的每个工作流环节预先定档并写成 `research/14_ai_risk_tiers.md`。** 具体分档（基于本文件核实过的官方例子逐条映射）：
   - **Green（可做，须披露）**：用 LLM 润色论文语言；建议章节结构；**数据清洗与去重**（Springer Nature 原文列为 Green）；比较方法学选项；对研究问题做 stress-test。
   - **Amber（须人工监督 + 可证明的人类判断）**：用 LLM 建议分析/实验/方法学路线；**大范围 copy editing 或写作支持**；把结果与已有文献对比；解释统计模型输出；**推荐统计检验或建模方法**。
   - **Red（禁止）**：**用 LLM 生成 hypothesis / analysis / conclusion 并当作人类产出呈现**；伪造数据、引用或结果；**在未披露的情况下用 LLM 生成核心研究推理**；把作者身份或问责交给 AI；**把 peer review 委托给 LLM**。
   **关键判断（必须写进文件）**：**阙疑的四态判决逻辑、67 条规则、452 条判决账本属于 "hypotheses / analyses / conclusions"，若由 LLM 生成即为 Red。因此本项目必须把"机制与规则设计由作者独立完成、LLM 用于代码实现与文档整理"写成一条显式声明。** **对应文件：`research/14_ai_risk_tiers.md`（新建）。时间点：2026-12 前。**

---

## 盲区（诚实标注）

- **阙疑实际要投的 E&D Track 的 AI 政策文本，我没有读到。** 我核实的是 **NeurIPS Main Track 2026 Handbook** 与 **PPT 2026 博客**。E&D 属于 Main Program 体系，**但 Main Track Handbook 是否逐字适用于 E&D，官方文本没有明说**。**"适用 Main Track 口径"是本文件的推断，不是已核实事实。**
- **Springer Nature 的逐字条款只取到了"框架层"（Green/Amber/Red + 四条 Core expectations + 例子），未取到"具体条款层"。** 原因：`nature.com/nature/editorial-policies/ai`、`preview-www.nature.com/nature/editorial-policies/ai`、`preview-www.nature.com/natmachintell/editorial-policies/ai` 三次 WebFetch 全部被重定向到 `idp.nature.com` 的登录页；`nature.com/articles/s41592-026-03020-1`（*Using AI responsibly in scientific publishing*，Nature Methods，2026-02-11）与 `nature.com/natprogbrainhealth/editorial-policies/ai` 返回 **"Client Challenge"**（Cloudflare 拦截）。**因此"Nature 系列要求把 LLM 使用记录在 Methods section"这一条，我只从搜索引擎摘要读到了片段（`preview-www.nature.com/natmachintell/editorial-policies/ai` 的摘要句），未在官方页面逐字核实。**
- **Springer Nature 的 FAQ 全部未展开**：官方页面的 9 个 FAQ（包括 *"Can AI tools like ChatGPT be listed as authors?"*、*"Do I need to declare AI-assisted copy editing?"*、*"Are generative AI images allowed in publications?"*）**在抓取结果里只出现了问题标题，答案内容没有渲染出来**。因此**"Springer Nature 是否要求披露 AI 辅助的 copy editing"这一关键问题，我没有拿到官方答案**——本文件把它按 Amber 处理（依据是 Amber 档明确列了 *"Extensive copy editing or writing support"*），但**"extensive"与"light"的分界官方没有给出**。
- **Wiley 与 SAGE 的逐字条款未核实**：我只读到了 aje.cn（2026-06-15 更新）与知乎的中文二次整理，**未打开 Wiley / SAGE 的官方政策页**。本文件的对照表**因此不含 Wiley 与 SAGE**。
- **NeurIPS 的官方 LLM Policy 页面目前是空占位**：`neurips.cc/public/LLM` 抓取结果只有标题 "LLM Policy" 与正文 "**Coming Soon**"。**这意味着 NeurIPS 2026 的正式 LLM 政策文档尚未发布，我现在引用的 Main Track Handbook 段落是当前可得的最权威文本。**
- **NeurIPS PPT 的 12 场景实验只有 10 篇样本，官方自己承认**（*"While these experiments were conducted with only 10 text samples"*），且**逐场景的 Pangram 分数没有数值表**（只有 Figure 1A/1B 图）。**"所有 permissible 场景都未被判为 AI"这句话的统计强度很弱**，不能作为"只要做轻度润色就一定安全"的保证。
- **"Pangram never classified AI completions of 20% or less as AI-generated"这条有两个限定**：**(a)** 样本是 10 篇 position paper 风格文本；**(b)** 用的是 **Pangram 3.3.2 在 medium/default 窗口**下的配置。**不能外推到其他文体或其他检测器。** 而且这条**不是"允许 AI 补全 20%"的政策许可**——Table 4 把 "Partial AI completion" 归为 **Diagnostic tests**（诊断实验），**不是 permissible 档位**。**把"检测器没抓到"误读成"政策允许"是极易犯的错误。**
- **ACM 内部口径不一致**：`acm.org` 的 FAQ（我核实的最新版）说写作辅助**不再需要披露**，而 `respect.acm.org/2026` 的会议政策页仍在说**必须 fully disclosed in the Work**，并给出"写在 Acknowledgements"的示例。**我不知道哪个是 ACM 的当前统一口径**，本文件的建议是"按更严的执行"。
- **AI 幻觉引用（hallucinated citations）的具体处理后果，我没有取到权威一手数据**：NeurIPS Main Track Handbook 只说 *"There have been many cases of hallucinated citations in literature review, which violates the NeurIPS Code of Conduct"*，**没有给出处罚等级或案例数字**。中文搜索（CSDN / 搜狐）提到的"某次 AI 生成 26 条参考文献中 8 条为伪造"等数字**来自自媒体，未核实，未采信**。（ICLR 2026 的 779 篇 desk reject 与幻觉引用处理，是方向 07 的任务，本文件不重复。）
- **各机构政策的时效性风险**：Elsevier / Springer Nature / ACM / Taylor & Francis 的政策页都在 2026 年持续更新（ACM 最新版标注 **2026-05-14**；CASRAI 的整理页标注 "Last verified 2026-08-16" 并提醒 *"Publisher AI policies are an actively evolving area"*）。**本文件的所有条款应在 2027-05 投稿前重新核对一次官方页面。**

---

## 来源

1. NeurIPS 官方博客, *AI-Generated Papers in the NeurIPS 2026 Position Paper Track* — https://blog.neurips.cc/2026/06/02/ai-generated-papers-in-the-neurips-2026-position-paper-track/ — **Table 4 "AI use cases and permissibility"** 12 场景全文（2 clearly permissible / 4 borderline permissible / 4 clearly impermissible / 2 diagnostic tests）；"For all of the permissible uses, Pangram did not classify any as AI-generated"；"Pangram never classified AI completions of 20% or less as AI-generated"；"While these experiments were conducted with only 10 text samples"；Table 2 窗口表（small 61.8% / medium 91% / default 100%）；"Note that the Position Paper Track's LLM policy differs from the Main Program's LLM policy" — Alex Lu, Seth Lazar, David Rügamer（PPC）；Stanley Hua, Kate Metcalf（Assistant PPC）— 2026-06-02
2. NeurIPS 2026 Main Track Handbook, *Author Use of Agents and Large Language Models (LLMs)* — https://neurips.cc/Conferences/2026/MainTrackHandbook — "The use of agents and/or LLMs in implementing the method should be described in the **experimental setup section (or equivalent)** if it is an **important, original, or non-standard component** of the approach"；"The use of spell checkers and grammar suggestions, aid for editing purposes, and basic code assistance **does not need to be documented**."；"**agents and LLMs cannot be authors**"；"attempts at **prompt injections** as well as other attempts to **manipulate reviewing is strictly prohibited**"；"many cases of **hallucinated citations** in literature review, which **violates the NeurIPS Code of Conduct**" — NeurIPS 2026
3. NeurIPS LLM Policy 页面（空占位） — https://neurips.cc/public/LLM — 正文仅 "Coming Soon" — NeurIPS
4. NeurIPS 2026 Call For Position Papers — https://neurips.cc/Conferences/2026/CallForPositionPapers — "Note that the Position Paper Track's LLM policy differs from the Main Program's LLM policy. Authors are responsible for …" — NeurIPS 2026
5. COPE, *Authorship and AI tools*（COPE position）— https://publicationethics.org/guidance/cope-position/authorship-and-ai-tools — "AI tools cannot be listed as an author of a paper."；"cannot take responsibility for the submitted work. As **non-legal entities**, they cannot assert the presence or absence of conflicts of interest nor manage copyright and license agreements."；"must be transparent in disclosing **in the Materials and Methods (or similar section)** of the paper how the AI tool was used and which tool was used"；"Authors are **fully responsible** for the content of their manuscript, even those parts produced by an AI tool"；DOI `10.24318/cCVRZBms` — COPE Council — last reviewed 2023-02-13
6. ICMJE, *Recommendations … A. Use of AI by Authors* — https://www.icmje.org/recommendations/browse/artificial-intelligence/ai-use-by-authors.html — "should describe, **in both the cover letter and the submitted work in the appropriate section** if applicable, how they used it"；"Chatbots (such as ChatGPT) and other AI-assisted tools **should not be listed as authors because they cannot be responsible for the accuracy, integrity, and originality of the work**"；"**Nondisclosure of AI use may require corrective action and may be construed as misconduct in some circumstances.**" — ICMJE
7. CASRAI, *Elsevier AI Policy: What to Write & Where* — https://casrai.org/guides/elsevier-generative-ai-authorship-policy — 标题 "Declaration of generative AI and AI-assisted technologies in the manuscript preparation process"；"**immediately before the reference list**"；"Basic grammar, spelling and punctuation checks (including standard spell-checkers) — **No — explicitly exempted**"；"generative AI tools … **cannot be credited as an author or co-author**"；图片允许/不允许清单；审稿人不得上传稿件 — CASRAI Editorial Board — last updated 2026-08-24，verified 2026-08-16
8. Springer Nature, *AI guidance for researchers, editors and reviewers* — https://group.springernature.com/gp/group/ai/ai-guidance-for-researchers-editors-reviewers — Green / Amber / Red 三档全文（含 Permitted / Permitted with human oversight / Not permitted 与全部例子）；四条 Core expectations；"Rather than focusing on **whether** AI has been used, the policies ask each user to consider: how AI has been used / the potential impact / the level of risk / whether appropriate human oversight has been maintained / whether transparency and accountability have been preserved" — Springer Nature
9. IEEE Open, *Author Guidelines for Artificial Intelligence (AI)-Generated Text* — https://open.ieee.org/author-guidelines-for-artificial-intelligence-ai-generated-text/ — "shall be disclosed in the **acknowledgments section**"；"The AI system used shall be identified, and **specific sections of the article that use AI-generated content shall be identified and accompanied by a brief explanation regarding the level at which the AI system was used**"；"The use of AI systems for editing and grammar enhancement … disclosure as noted above is **recommended**" — IEEE — 2024-04-16
10. ACM, *Policy on Authorship* — https://www.acm.org/publications/policies/new-acm-policy-on-authorship — 更新于 **2026-05-14**；"Anyone listed as author on an ACM submission must meet all the following criteria: … **They are an identifiable human being.** Anonymous authorship is not permitted, although pseudonyms and/or pen names are permitted provided accurate contact information is given to ACM… ACM does not currently permit collective authorship."；第 1 项（研究用途）"**must be described in detail in the methods section of the Work**"；第 2 项（写作辅助）"**ACM no longer requires the disclosure of information regarding the use of AI**"；"Rather than attempt to limit the use of Artificial Intelligence (AI) … this updated Policy attempts to set clear expectations for their responsible use" — ACM
11. ACM, *Frequently Asked Questions*（Policy on Authorship 部分） — https://www.acm.org/publications/policies/frequently-asked-questions — "Can a generative AI tool be listed as an author? **No, generative AI software tools cannot be listed as authors on ACM Works under any conditions.**"；"In the event content integrity issues stemming from the use of AI during authorship are identified *after publication* … ACM reserves the right to **retract the published Work in its entirety**."；不可接受的署名行为清单（Anonymous / Collective / Gift / Guest / Ghost / Purchased Authorship、Paper Mills、Citation Manipulation） — ACM
12. ACM RESPECT 2026, *Policies on Generative AI, LLMs, and Related Tools* — https://respect.acm.org/2026/index.php/policies-on-generative-ai-llms-and-related-tools/ — 引用旧版 ACM 口径："The use of generative AI tools and technologies to create content is permitted but **must be fully disclosed in the Work** … **ChatGPT was utilized to generate sections of this Work, including text, tables, graphs, code, data, citations, etc.**"；"Reviewers may **not** submit papers to LLMs, plagiarism detectors, summarizers, or other such tools."；"we have seen the occasional '**hallucinatory reference**' in ACM RESPECT submissions" — ACM RESPECT 2026
13. ICLR 2027, *AI Policy for Authors* — https://iclr.cc/Conferences/2027/AIPolicyForAuthors — "a **mandatory section in their paper (this section will not be counted towards the page limit)**"；官方 boilerplate 全文；**Required** 清单（含 "implement methods"、"clean and reformat dataset"、"interpret results"、"assist with translation"）；**Recommended** 清单（含 "create or edit software code"、"draft parts of a research paper"、"edit a research paper to improve readability"）；"might lead to **desk rejection** of the paper" — ICLR 2027
14. CASRAI, *Taylor & Francis's Generative AI Policy: Authorship Rules and Disclosure Requirements* — https://casrai.org/guides/taylor-francis-generative-ai-authorship-policy — "**The specific tool used, including its version number** (e.g. 'ChatGPT-4' rather than just 'ChatGPT'…) — **a generic reference to 'AI assistance' without naming the tool does not satisfy the requirement**"；"belongs in the **Methods section** where the journal has one, or in the **Acknowledgments section** where it does not"；书籍作者的 **disclose-and-seek-approval** 模型；"**Past**ing a confidential manuscript into a consumer-facing AI chatbot for a quick summary is treated as a **confidentiality breach**" — CASRAI Editorial Board — last updated 2026-08-25
15. Taylor & Francis, *AI Policy* — https://taylorandfrancis.com/our-policies/ai-policy/ — "Generative AI tools **must not be listed as an author** because such tools are **unable to assume responsibility** for the [content]" — Taylor & Francis
16. CASRAI, *Can AI Be an Author? ICMJE & COPE Rules* — https://casrai.org/guides/can-ai-be-listed-as-an-author — "ICMJE, COPE, and major scholarly publishers hold a **uniform position**: AI tools cannot be listed as authors because [they cannot take responsibility]" — 2026-08-09
17. CASRAI, *MDPI's Generative-AI Authorship Policy* — https://casrai.org/guides/mdpi-generative-ai-authorship-policy — "MDPI's policy explicitly states that generative-AI tools **do not meet the criteria for authorship and cannot be** [listed]" — 2026-08-24
18. aje.cn, *Nature、Elsevier、Wiley 等五大出版商最新AI政策汇总（2026年）* — https://www.aje.cn/arc/publishers-ai-policy-2026 — 五家出版商逐家整理（**中文二次资料，未在官方页面逐字核实，本文件仅用于交叉参考**）— 更新于 2026-06-15
19. CASRAI, *Journal and Publisher Policies on Generative AI in Manuscripts: The Policy Landscape* — https://casrai.org/guides/ai-in-manuscripts-publisher-policy-landscape — "The detail that varies most across publishers … is exactly **where the disclosure statement must appear** (Methods vs. Acknowledgments vs. a dedicated AI-use declaration field in the submission system) and **how granular the 'how it was used' description needs to be**." — CASRAI
20. NeurIPS 2026 Position Paper Track（OpenReview） — https://openreview.net/group?id=NeurIPS.cc/2026/Position_Paper_Track — "Submission Start: Apr 15 2026 08:00AM UTC-0, Abstract Registration: May 05 [2026]" — OpenReview
