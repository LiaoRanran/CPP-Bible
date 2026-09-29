# 方向 05：prompt provenance log 怎么写

## 核心结论

1. **"prompt provenance log" 这个词有明确的制度出处：NLnet 基金会 2025-12-08 生效、2026-01-26 修订至 v1.1 的《Policy on the use of Generative Artificial Intelligence for NLnet-funded projects》。** 政策原文规定：*"If GenAI is used in the application process **a prompt provenance log must be maintained**. This log should list: **the model used, dates and times of prompts, the prompts themselves, the unedited output.**"* —— **只有 4 个字段，但"未编辑的原始输出"这一条是最苛刻的**，因为它要求你保留 AI 的原文，而不是只保留你改完的版本。违规后果写在政策里：*"Failure to comply with the above policy may result in **rejection of the proposal** or ultimately in the **termination of the running grant**."*

2. **NeurIPS 2026 PPT 把"版本历史"从"建议"升级为"申诉的唯一货币"，并明确预告它将成为未来默认要求。** 官方要求作者提供三个检查点：**(1) "pre-AI" checkpoint**（证明论文实质性内容在独立于 AI 的情况下开发）、**(2) "post-AI" checkpoint**（紧随最具实质性的 AI 撰写编辑之后）、**(3) 提交时的最终稿**，并额外提交一份分析证明"**(2) 的 AI 编辑没有引入 (1) 中不存在的新的实质性内容**，且 **(2) 之后的人工编辑证明 (3) 已被人类作者适当核实**"。官方原话：*"We expect that in **future years this kind of audit trail will become a default**."* 而阙疑的目标是 **NeurIPS 2027 E&D** —— **2027 年就是"future years"，所以这份 log 必须从 2026-10 就开始写，不能等投稿前补。**

3. **各大出版社的"放哪、写什么"已经高度收敛，可以一次写成多套可复用文本。** 三条最硬的规则：**Elsevier** —— 必须放在**参考文献列表之前**，标题固定为 *"Declaration of generative AI and AI-assisted technologies in the manuscript preparation process"*，且**基础语法/拼写检查被明确豁免**；**IEEE** —— 放在**致谢（acknowledgments）**里，必须点名 **AI 系统 + 具体哪几节用了 + 用到什么程度**，**编辑/语法用途"建议披露但不强制"**；**COPE / ICMJE** —— **AI 永远不能当作者**，且 **COPE 要求在 Materials and Methods（或类似章节）说明"如何用、用了哪个工具"**，ICMJE 进一步要求在**投稿信（cover letter）和正文两处都写**，并警告 *"Nondisclosure of AI use may require corrective action and may be construed as **misconduct** in some circumstances."*

---

## 精确数字与案例

### 一、NeurIPS PPT 2026 的三节点版本历史（逐字，本方向的最高优先级要求）

来源：NeurIPS 官方博客 *AI-Generated Papers in the NeurIPS 2026 Position Paper Track*，2026-06-02，署名 Alex Lu、Seth Lazar、David Rügamer（Position Paper Chairs）与 Stanley Hua、Kate Metcalf（Assistant Position Paper Chairs）。

**申诉流程原文（逐字）**：

> **Appeals Process**
> It is important to be clear **where the burden of proof should lie** when it comes to detecting improper use of AI in submissions to a peer-reviewed conference.
>
> Authors who use AI extensively but, in their belief, responsibly, are often **indistinguishable from those who have used AI in ways that are not consistent with policy**. We have used every available measure to distinguish between these two groups, but we acknowledge there will inevitably be borderline cases.
>
> We believe that it is inappropriate for the research community as a whole to bear the cost of making more fine-grained distinctions among these cases. **Authors who limit AI use in their final drafts help reduce burden on the review community. Authors who make more extensive use of AI should maintain clear documentation of their process, which can be shared if requested.**
>
> Authors given the opportunity to appeal will be able to provide evidence of responsible AI use in the following form. **Well-motivated equivalents may be considered.**
>
> - "Authors must supply the Track Chairs with a link to an online version of their paper that has a **version history** including the work **before and after the use of AI**"
> - "They must identify **(1)** a **'pre-AI' checkpoint** indicating that they developed the **substantive content** of the paper independent of AI, **(2)** a **'post-AI' checkpoint** immediately after their most substantive AI-written edits, and **(3)** the **final paper as submitted**."
> - "They must present analysis showing that **the AI edits in (2) did not introduce new substantive content that was not present in (1)**, and of **human edits after (2) which demonstrate that (3) was appropriately verified by human authors**."
>
> "This dossier will be reviewed by the PPT team. **Authors who do not wish to appeal may withdraw their paper.**"

**配套的硬截止与审计预告（逐字）**：

> "Where we have strong but not decisive evidence of non-compliance, we are asking authors to provide evidence supporting that their AI use complied with policy … **Submissions lacking such proof by June 15th, 2026 will also be desk-rejected.**"

> "But we are also introducing a new approach to auditing AI use by establishing appropriate provenance. Authors whose submissions show significant AI involvement must provide an **audit trail** that clearly demonstrates that they complied with the policy. **We expect that in future years this kind of audit trail will become a default.**"

**三个检查点的可操作解读（这是本方向最实用的部分）**：

| 检查点 | 官方定义 | 阙疑必须留存的东西 | 最低技术手段 |
|---|---|---|---|
| **(1) pre-AI** | "developed the substantive content of the paper independent of AI" | **机制设计、四态判决定义、67 条规则、数据集数字**这些"实质内容"的产生过程 | `gate_engine.py` 的 Git 提交历史 + 设计笔记（`research/` 下 md 的提交时间戳） |
| **(2) post-AI** | "immediately after their most substantive AI-written edits" | **AI 改写后的那一版完整快照**（且必须能看出"AI 只改了措辞，没加新内容"） | 单独的 Git tag（如 `post-ai-edit-v1`）+ 对应的 prompt 记录 |
| **(3) final** | "the final paper as submitted" | 投稿版 PDF/LaTeX 源码 + 其 SHA-256 | 投稿仓库的 `submission` tag |
| **附加分析** | "(2) 未引入 (1) 中没有的新实质内容；且 (2)→(3) 有人工核实" | **一份 diff 报告**：把 (1) 与 (2) 的**断言清单（claim list）**做对比 | 人工维护的 claim 表 + diff |

**⚠️ 关键提醒**：官方写的是 *"Well-motivated equivalents may be considered"* —— **这意味着"用 Git 提交历史替代 Google Docs 版本历史"是被允许的**，前提是你**能解释清楚这套等效物如何证明同一件事**。对阙疑（已有 Git 仓库、已有哈希链账本）来说，这是**把既有基础设施直接变成合规资产**的机会。

### 二、NLnet 的 prompt provenance log（4 个必填字段 + 一套 Git 提交规范）

来源：`nlnet.nl/foundation/policies/generativeAI/`。政策生效 **2025-12-08**（Version 1.0），当前版本 **2026-01-26（Version 1.1，基于 grantee 反馈调整）**。

**四项基本原则（逐字，这是整套 log 的正当性根据）**：

> 1. "**FLOS licence**: All projects must be free/libre/open source: all scientific outcomes must be published as open access…"
> 2. "**No misrepresentation**: Grantees and applicants should not claim work as their own, if it is not. **This has always been true and GenAI doesn't change that.**"
> 3. "**Project quality**: Grantees are expected to deliver project outcomes to the best of their ability. Tools may assist but **do not replace human responsibility** for correctness, clarity, and reproducibility."

**prompt provenance log 的逐字定义（全篇最关键的一段）**：

> "If GenAI is used in the application process **a prompt provenance log must be maintained. This log should list:**
> - **the model used,**
> - **dates and times of prompts,**
> - **the prompts themselves,**
> - **the unedited output.**"

> "Instructions about how to submit the prompt log for applications are provided on the **proposal form**。"（NLnet 的 `nlnet.nl/propose/` 表单里确实有一道题：*"AI disclosure — Did you use generative AI in writing this proposal? (See our GenAI policy.) -- Please choose an option -- No, …"*）

**项目开发阶段的要求（比申请阶段更细，且直接给出了 Git 提交规范）**：

> "Use of GenAI should be disclosed and transparent. For any **substantive** use of GenAI that materially affects outputs, **public disclosure is required**, making it available to both users and contributors."

> "Generated content should be marked as such. When adding (partially) generated code, make sure **the provenance is clear for each such contribution. Specify which model was used, (including version), and how it was used. Provide the used prompts/interactions and resulting output, or a summary thereof.**"

> "**Example**: When using git, **distinguish commits that add generated code and include the used model and prompts in the commit message.** Consider choosing a development tool that helps you create commits, and auto-fills the relevant information."

> "**Make sure to provide the information in a logical place where it can easily be found. Avoid hosting it on third-party platforms that require a log-in or may disappear over time.**"

**NLnet 官方给出的两条 Git 提交范例（逐字，这是"prompt provenance log 长什么样"的最具体答案）**：

```
Author: Harry Hacker <hh@example.org>
Date: Sun Jan 18 10:32:15 2026
    Fix compliance tests
    Fix several mistakes in generated code, make it compile;
    manually verify each test with RFC123 specification.
```

```
Author: Harry Hacker with CodeLLM-3.4 <hh@example.org>
Date: Sun Jan 18 10:52:08 2026
    Generate compliance tests
    Prompt: Generate tests for compliance with RFC123 messages.
    Output: (this commit)
```

**注意第二条例子的两个细节**：**(a)** 作者字段写成 `Harry Hacker with CodeLLM-3.4` —— **把模型写进作者行**，既保留人类问责又标明工具；**(b)** commit message 里明确分 `Prompt:` 与 `Output:` 两行。**这套格式可以直接照搬到阙疑的 `gate_engine.py` 与 `research/` 仓库。**

**"何时可以不那么细"的豁免条款（逐字）**：

> "If GenAI is not used for generating code but only for tasks like testing or creating documentation, it **suffices to provide a general description of the use in the 'readme'**. More detailed logging on a per commit basis is **preferred but not required**."

**"ongoing project" 的过渡条款（逐字，可能对阙疑有用）**：

> "Note that for ongoing projects, **logging is *not* required retroactively**. It applies to milestones which were **started after this policy came into force (December 8, 2025)**."

**关于 GenAI 本身的研究是允许的（逐字）**：

> "It is allowed to work on the topic of GenAI itself within the scope of a grant, but only if this is explicitly part of approved work."

**NLnet 引用的 EU 版权立场（逐字，对"AI 生成内容能否算作者产出"有直接意义）**：

> "purely AI-generated outputs—those created automatically by an AI system **without substantial human intervention**—are **not eligible for copyright protection in the EU**. Such outputs are considered to fall into the **public domain**…"（引自欧洲议会 JURI 委员会委托报告 IUST_STU(2025)774095，第 93 页）

### 三、ICLR 2027：把披露写进论文正文的强制章节（含官方 boilerplate）

来源：`iclr.cc/Conferences/2027/AIPolicyForAuthors`。

> "We ask that authors explicitly state how they used LLMs in their submission, **both in the paper's text as well as in the paper submission form**."

> "Additionally, we require authors to disclose AI use in a **mandatory section in their paper (this section will not be counted towards the page limit)**. The ICLR paper template includes a **boilerplate disclosure** to give authors a sense of the expected detail. You are not required to follow this format exactly—we believe these disclosures may be a source of useful information to the community about how AI is affecting research workflows, and we **encourage you to provide as much detail as you want!**"

> "Ultimately the paper's authors are **responsible** for the contents of their submissions. Consequently, **a substantial falsehood, instance of plagiarism, or misrepresentation produced by an LLM would be considered a Code of Ethics violation on the part of the paper's authors, and might lead to desk rejection of the paper.**"

**官方 boilerplate 逐字（可直接改写使用）**：

> "In this work, we used generative AI tools for **<tasks with required disclosure>**. We have not used generative AI tools for **<other tasks with required disclosure>**, and **<the rest of the required disclosure tasks>** are not applicable to this work. Additionally, we used generative AI tools for **<tasks with recommended disclosure>**. **We have reviewed all AI-assisted work.** [Elaborate. For example, "we checked LLM-generated research ideas for potential plagiarism through a manual literature survey", "LLM-generated code was verified and tested for correctness by 2 authors", etc.]. **We take responsibility for the final content of this work, including text, claims or artifacts produced with the aid of generative AI.**"

**ICLR 2027 的"必披露 / 建议披露"任务清单（逐字，这是"log 该记什么"的官方分类依据）**：

| 等级 | 任务（逐字） |
|---|---|
| **Required（必须披露）** | "Generate synthetic data sets, help develop theoretical models or conceptual frameworks, formulate mathematical claims, provide critical ingredients for proving mathematical claims, assist in the writing of proofs, propose or refine hypotheses, design or provide feedback on research methodology or experiments, implement methods, assist with translation, clean and reformat dataset, support qualitative and thematic data analysis, interpret results." |
| **Recommended（建议披露）** | "Formulate questions for surveys or interviews, create or modify scientific figures or images, suggest experimental parameters, **create or edit software code**, creation of artifacts, **draft parts of a research paper**, transcribe recordings of research material, summarize or analyse existing literature, discover research topics or identify gaps, brainstorming, sourcing/searching for information, **edit a research paper to improve readability**, identify relevant literature, format references, suggest a structure for a research paper, propose a title or keywords for a research paper." |

**对阙疑的直接映射（这条必须写进 log 的分类维度里）**：
- **"implement methods" + "create or edit software code"** → 阙疑的 `gate_engine.py`（3826 行）与 595 个 .py 工具**属于必披露 + 建议披露双重覆盖**；
- **"clean and reformat dataset" + "interpret results"** → 数据集的 30 盲 holdout / 40 外部 corpus 处理属于 **Required**；
- **"edit a research paper to improve readability" + "draft parts of a research paper"** → **Recommended**（相对宽松，但仍须披露）；
- **"assist with translation"** → 对非母语作者是 **Required**，阙疑必须把"翻译/润色"归到这一类。

### 四、五家机构"放哪、写什么"逐条对照表

| 机构 | 能否当作者 | 是否必须声明 | 声明放哪 | 关键豁免 | 逐字依据 |
|---|---|---|---|---|---|
| **NeurIPS PPT 2026** | 隐含不可（要求 substantially human-written） | **必须**（投稿时声明如何使用 AI，并 attest 未违反规则） | 投稿表单 + **申诉时提交三节点版本历史 dossier** | 允许 AI 用于 "copy-editing or similar peripheral changes" | "the final paper must itself be substantially written by human authors, meaning that AI is used only for copy-editing or similar peripheral changes to the main text" |
| **ICLR 2027** | 未在 AI 政策中单列 | **必须**（正文强制章节 + 投稿表单） | **论文正文的 mandatory section**（不计页数） | 无豁免；分 Required / Recommended 两档 | "we require authors to disclose AI use in a mandatory section in their paper (this section will not be counted towards the page limit)" |
| **Elsevier** | **明确不可** | **必须**（若使用） | **参考文献列表之前**，标题固定为 *"Declaration of generative AI and AI-assisted technologies in the manuscript preparation process"* | **基础语法、拼写、标点检查明确豁免** | "During the preparation of this work the author(s) used [NAME OF TOOL / SERVICE] in order to [REASON]. After using this tool/service, the author(s) reviewed and edited the content as needed and take(s) full responsibility for the content of the publication." |
| **IEEE** | 未明确（但要求作者是可识别的自然人，见 ACM 同源原则） | **必须**（若使用 AI 生成 text/figures/images/code） | **致谢（acknowledgments）章节** | **编辑与语法增强"generally outside the intent of the above policy"，披露仅为 recommended** | "The use of content generated by artificial intelligence (AI) in an article … shall be disclosed in the **acknowledgments section**… The AI system used shall be identified, and **specific sections of the article that use AI-generated content shall be identified and accompanied by a brief explanation regarding the level at which the AI system was used**." |
| **COPE** | **明确不可** | **必须** | **Materials and Methods（或类似章节）** | 未列豁免 | "AI tools cannot meet the requirements for authorship as they **cannot take responsibility** for the submitted work. As non-legal entities, they cannot assert the presence or absence of conflicts of interest nor manage copyright and license agreements." / "Authors who use AI tools in the writing of a manuscript, production of images or graphical elements of the paper, or in the collection and analysis of data, must be transparent in disclosing **in the Materials and Methods (or similar section) of the paper how the AI tool was used and which tool was used**." |
| **ICMJE** | **明确不可** | **必须** | **投稿信（cover letter）+ 正文相应章节，两处都写** | 无 | "Authors who use such technology should describe, in **both the cover letter and the submitted work in the appropriate section** if applicable, how they used it." / "**Nondisclosure of AI use may require corrective action and may be construed as misconduct in some circumstances.**" |

**Elsevier 的图片规则（额外的一条红线，逐字）**：

> 允许（须披露）："Explanatory images such as flowcharts, diagrams and decision trees — disclose in the figure caption and in the AI declaration"；"Data visualizations generated directly from the authors' own underlying data, described in the Methods section"
> **不允许**："**Primary research images: microscopy, western blots, radiology/imaging scans, patient photographs**"；"**Graphical abstracts created with general-purpose generative AI tools**"；"**Cover art generated with AI, without prior permission from the editor/publisher**"

**Elsevier 对审稿人的限制（逐字，阙疑未来审稿时也适用）**：

> "Reviewers must **not upload a manuscript, or any part of it, to a generative AI tool** — doing so is treated as a **breach of the confidentiality** of the peer-review process and of the authors' intellectual property… Reviewers may still use AI tools in a more limited way, such as **improving the language of their own review report** or running a background literature search."

**COPE 对"作者责任"的定性（逐字，这条比任何技术手段都重要）**：

> "Authors are **fully responsible** for the content of their manuscript, **even those parts produced by an AI tool**, and are thus **liable for any breach of publication ethics**."

### 五、日志字段设计：一份可直接抄的 12 字段模板

来源：ai-cards.org *AI tools for research: a disclosure log template for papers and [projects]*（2026-08-03）。原文核心原则（逐字）：

> "**Use one row per AI-assisted task.**"

> "一行记录应能让未来的读者回答四个问题：**What did you use? / What did you ask it to do? / What material did it process? / How did a human check the result?**"

> "**That last question matters most. A tool log without human review reads like a receipt. A good log shows responsibility.**"

**12 个字段（逐字）**：

| 字段 | 记录什么（逐字） |
|---|---|
| Date | The day you used the tool |
| Project stage | Search, design, data collection, analysis, writing, revision, submission |
| Tool name | Name of the AI tool or AI-assisted feature |
| Provider | Company, platform, or institution |
| **Version or model** | Model name, version, or **"unknown" if the tool did not show it** |
| Input material | What you uploaded, pasted, or described |
| Task | What you asked the tool to do |
| Output used | Whether you used text, code, labels, summaries, images, suggestions, or only ideas |
| **Human review** | Who checked the output and how |
| Changes made | What the author changed, rejected, corrected, or verified |
| **Disclosure relevance** | Manuscript, methods, acknowledgment, cover letter, figure caption, appendix, or **no disclosure likely** |
| Privacy note | Whether the input included unpublished data, personal data, confidential peer review material, or copyrighted text |
| Link to record | Prompt file, transcript, screenshot, notebook page, or repository path |

**原文给出的完整 Markdown 模板（逐字，可直接落地）**：

```
# AI tool log
 
Project:
Authors:
Last updated:
 
| Date | Stage | Tool and provider | Version or model | Input material | Task | Output used | Human review | Changes made | Disclosure location | Privacy note | Record link |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-08-03 | Writing | Tool name, provider | Model or version | Draft introduction, no data | Asked for sentence-level language edits | Accepted edited phrasing in two sentences | First author checked against original meaning | Rejected one suggested claim | Acknowledgment or AI disclosure statement | No personal or unpublished data uploaded | /records/2026-08-03-language-edit.md |
```

**原文的"逐条 prompt 记录"模板（仅在任务影响内容时使用，逐字）**：

```
# AI prompt record
 
Date:
Project:
Tool:
Version or model:
User:
Project stage:
 
## Input material
Describe what you pasted, uploaded, or linked.
 
## Prompt
Paste the prompt here.
 
## Output used
Describe the part used in the project.
 
## Human check
Describe how the author checked the output.
 
## Decision
Accepted:
Modified:
Rejected:
Needs follow-up:
```

**原文的"何时才需要存完整 prompt"判据（逐字，这条能大幅降低记录负担）**：

> "**Save prompts and outputs when the tool shaped research content.** That includes data labels, generated code, summaries of papers, interview coding suggestions, figure edits, or manuscript text that you copied into the draft."

> "**无需**归档每个拼写建议；仅当工具塑造了研究内容时才保存 prompt 与输出。"

**原文的"提交前整理四分组法（逐字，直接对应四家机构的四种放置位置）**"：

> 1. "entries that **do not need disclosure** because the tool had no effect on the research record."
> 2. "entries that belong in the **acknowledgment or AI declaration**."
> 3. "entries that belong in **methods** because they affected design, data handling, analysis, screening, coding, or synthesis."
> 4. "entries that **raise policy or ethics questions**. These may involve personal data, confidential peer review material, patient information, third party manuscripts, copyrighted corpora, or generated images."

**SciSpace 的补充要点（逐字，可作为 log 的"频率要求"）**：

> "The most effective disclosure practices are often the simplest ones: **document as you go rather than trying to reconstruct everything later.**"

> "**Review logs periodically rather than waiting until submission.**"

> "At a minimum, note **the prompts you used, the AI model and version, and any key outputs that influenced your writing or analysis**. If a prompt went through multiple revisions, it helps to **record those changes too**."

### 六、一个真实的 prompt provenance log 长什么样（开源实例）

来源：`github.com/ontola/atomic-plugins` 仓库的 `syncables/docs/ai-logs/sessions/2026-08-24-nlnet-genai-disclosure.md`。这是为了遵守 NLnet 政策而真实建立的目录结构：`docs/ai-logs/README.md`（政策说明与范围界定）+ `docs/ai-logs/sessions/<日期>-<主题>.md`（每次会话一份）。

**该会话日志的头部字段（逐字）**：

```markdown
# Session log — 2026-08-24

- **Session:** https://claude.ai/code/session_01TzsffxbQTzSPYqrpZ4rJ2M
- **Model:** Claude Sonnet 5 (`claude-sonnet-5`)
- **Repos touched:** `localthought/syncables` (this repo); the same session
  also worked on `localthought/reflector`, syncables' sibling project — see
  [reflector's own log for this session](...) for the parts of the conversation
  specific to that repo.
- **Redactions applied:** none needed for the syncables-relevant portion of
  this session; no secrets or personal information appeared in it.
```

**该日志的范围声明（逐字，这段值得整段借鉴）**：

> "This log records the **substantive human prompts and the assistant's substantive outputs**, per the scoping explained in `docs/ai-logs/README.md`. It **omits the coding assistant's internal system prompt, tool-call plumbing, and other harness scaffolding**. Only the turns relevant to `syncables` are included here."

**该日志的逐轮格式（逐字）**：

> "## Turn 1
> **User prompt:** > Clone the repository localthought/syncables into this session.
> **Assistant output:** Attached `localthought/syncables` to the session (read access; it's public, served via the session's anonymous git-read proxy) and shallow-cloned it for reference…"

**四个可复用的设计决策**：
1. **一个会话一份文件**，文件名带日期；
2. **头部固定四个字段**：Session URL / Model（含精确 model id）/ Repos touched / **Redactions applied**；
3. **正文按 Turn 编号**，每个 Turn 分 `User prompt` 与 `Assistant output`；
4. **显式声明省略了什么**（system prompt、tool-call plumbing、harness scaffolding）—— **这一条极其重要，因为它把"选择性记录"变成了一种被说明过的、可辩护的做法，而不是"藏证据"**。

---

## 对阙疑的 3 条具体行动

1. **在项目根目录建立 `provenance/` 目录，并写入 `provenance/ai-tool-log.md`，字段严格采用 ai-cards.org 的 12 字段表（加一列 `neurips_checkpoint`）。** 具体落地：新建 `provenance/ai-tool-log.md`，表头为 `Date | Stage | Tool and provider | Version or model | Input material | Task | Output used | Human review | Changes made | Disclosure location | Privacy note | Record link | neurips_checkpoint`；`neurips_checkpoint` 取值限定为 `pre-AI / post-AI / final / n-a`。**同时新建 `provenance/prompts/` 目录，只保存"塑造了研究内容"的 prompt（按 ai-cards.org 判据），不保存拼写建议类交互。** 每个 prompt 记录用 ai-cards.org 的 6 段模板（Input material / Prompt / Output used / Human check / Decision）。**时间点：2026-10 立即启动**（因 NeurIPS 2027 就是官方预告的"future years"，且 retroactive 补记不可信）。

2. **把 `gate_engine.py` 与 `research/` 的 Git 提交规范改成 NLnet 双行格式，让每一次 AI 辅助提交自带 provenance。** 具体做法：在仓库根加 `.gitmessage` 模板，要求所有涉及 AI 辅助的提交写成：
   ```
   <一句话动作>
   Prompt: <实际使用的 prompt 原文>
   Output: <生成的内容概要或 "this commit">
   ```
   作者行在有 AI 参与时写 `<人类名> with <模型名 版本>`（照抄 NLnet 的 `Harry Hacker with CodeLLM-3.4` 格式）。**同时增加一个 CI 检查（可用现有的 595 个 .py 工具之一）：若 commit message 含 `Prompt:` 但作者行未含 `with `，则告警。** 依据是 NLnet 政策原文 *"distinguish commits that add generated code and include the used model and prompts in the commit message"*。**对应文件：`.gitmessage` + `tools/check_provenance.py`。时间点：2026-11 前。**

3. **提前写好三份"声明文本"，存为 `provenance/disclosure/` 下的模板，并在 2027-05 前填好实际内容。** 具体三份：
   - **`neurips_2027_disclosure.md`** —— 按 ICLR 2027 官方 boilerplate 结构改写（*"In this work, we used generative AI tools for … We have not used generative AI tools for … We have reviewed all AI-assisted work … We take responsibility for the final content of this work…"*），并**按 ICLR 的 Required / Recommended 清单逐条勾选**（阙疑已知必填项：implement methods、create or edit software code、clean and reformat dataset、interpret results、assist with translation、edit a research paper to improve readability）；
   - **`elsevier_style_declaration.md`** —— 标题固定为 *"Declaration of generative AI and AI-assisted technologies in the manuscript preparation process"*，正文套用 Elsevier 逐字模板 `During the preparation of this work the author(s) used [TOOL] in order to [REASON]. After using this tool/service, the author(s) reviewed and edited the content as needed and take(s) full responsibility for the content of the publication.`；**注意放置位置是参考文献列表之前**；
   - **`three_checkpoint_dossier.md`** —— 按 NeurIPS 三节点要求，为 `pre-AI / post-AI / final` 各写一段说明，并附上**一份 (1) vs (2) 的 claim diff 表**（左列"pre-AI 已有的实质内容"、右列"post-AI 是否引入新内容"，逐行填 `no new content` / 具体新增项）。**这份 diff 表就是官方要求的 "analysis showing that the AI edits in (2) did not introduce new substantive content that was not present in (1)"。**
   **时间点：模板 2026-12 前建好，内容 2027-05 前填实。**

---

## 盲区（诚实标注）

- **NLnet 的"申请表单里怎么提交 prompt log"我没有看到具体操作说明**：政策原文只说 *"Instructions about how to submit the prompt log for applications are provided on the proposal form"*，我读到了表单里那道 AI disclosure 选择题的片段（`nlnet.nl/propose/`），但**没有看到"上传方式/格式/字数限制"的具体规则**。
- **"NeurIPS 2027 会不会强制要求 provenance log"是推断，不是事实**：官方 2026-06-02 博客只说 *"We expect that in future years this kind of audit trail will become a default"*。**这是一句预期表述，不是承诺**；且**那是 Position Paper Track 的政策，不是 E&D Track 的**。阙疑投的是 E&D，**E&D 的 AI 政策文本我没有逐字读到**（方向 02 的文件里也没有）。**这是本方向最大的不确定性。**
- **NeurIPS PPT 2026 与 Main Program 的 LLM 政策不同，且官方明确提醒过**：博客原文 *"Note that the Position Paper Track's LLM policy **differs from the Main Program's** LLM policy. Authors are responsible for understanding policy pertaining to the specific track they are submitting to, and abiding by it."* —— **所以不能把 PPT 的三节点要求直接外推到 E&D。**
- **Elsevier 的声明模板来自 CASRAI 的二次整理页（2026-08-24 更新，标注 "Last verified 2026-08-16 against Elsevier's own generative-AI policy page"），不是 Elsevier 官网原文**。CASRAI 页面自己提示：*"Publisher AI policies are an actively evolving area — check the live policy page for the current version before submission if this page is more than a few months old."* **我没有直接打开 `elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals`。**
- **Springer Nature 的具体条款未取到**：我搜到了官方入口（`group.springernature.com/gp/group/ai/ai-guidance-for-researchers-editors-reviewers`、`preview-www.nature.com/nature/editorial-policies/ai`）与 enago 的中文二次整理，但**没有打开官方页面逐字核实**。本文件因此**未给出 Springer Nature 的逐字条款**。
- **ACM 的具体 AI 政策文本未逐字取到**：我只读到了 *ACM Policy on Authorship* 的摘要片段（"Anyone listed as author on an ACM submission must meet all the following criteria: 1. They are an identifiable hum[an]…"）与 PKC 2026 的一句 *"We plan to generally follow the ACM Policy on the use of AI tools"*。**ACM 关于 AI 披露的具体条款（放在哪、写什么）未核实。**
- **ai-cards.org 与 scispace.com 的模板都是非官方、非同行评审的第三方建议**：ai-cards.org 未标注作者与机构；scispace.com 是商业产品（SciSpace AI Writer）的内容营销页，**其"模板"部分实质上在推销自家自动记录功能**。**模板结构可参考，但不具备任何合规效力**——真正有约束力的是各机构的官方政策。
- **ontola 的 `ai-logs` 是单个开源项目的实践，不是标准**：它提供了很好的格式参考，但**该项目的规模、语言、资助方都与阙疑不同**，且**该日志本身是 LLM 生成并整理出来的**（从 Turn 2 的 prompt 可以看出）。**它的价值在于"格式示范"，不在于"合规范本"。**
- **一个未被回答的关键问题**：**如果 (1) pre-AI checkpoint 本身就是用 LLM 辅助设计的（阙疑的 `_arch_v46/` 有 75+ 份 AI 生成文档、595 个 .py 工具），那么 (1) 还成立吗？** NeurIPS 官方要求 (1) 证明"developed the substantive content of the paper **independent of AI**"。**官方文本没有讨论"AI 辅助写代码/做设计"是否算"substantive content"**。这是一个真实的规范空白，**我建议阙疑在 `provenance/` 里对这条做显式声明，而不是回避**（例如声明"机制设计与规则判定逻辑由作者独立完成，AI 用于代码实现与文档整理"）。

---

## 来源

1. NLnet, *Policy on the use of Generative Artificial Intelligence for NLnet-funded projects* — https://nlnet.nl/foundation/policies/generativeAI/ — "If GenAI is used in the application process a **prompt provenance log must be maintained**. This log should list: the model used, dates and times of prompts, the prompts themselves, the unedited output."；"distinguish commits that add generated code and include the used model and prompts in the commit message"；"Avoid hosting it on third-party platforms that require a log-in or may disappear over time."；两条 Git 提交范例（`Harry Hacker with CodeLLM-3.4`）；"logging is *not* required retroactively"；"rejection of the proposal or ultimately in the termination of the running grant" — NLnet Foundation — 生效 2025-12-08（v1.0），当前 v1.1 **2026-01-26**
2. NLnet 资助申请表单（AI disclosure 字段） — https://nlnet.nl/propose/ — "AI disclosure — Did you use generative AI in writing this proposal? (See our GenAI policy.)" — NLnet
3. NLnet 政策归档与 grantee 反馈 — https://nlnet.nl/foundation/policies/generativeAI/archive/ — "Version 1.1 … Adjustments based on feedback from grantees" — 2026-01-26
4. NeurIPS 官方博客, *AI-Generated Papers in the NeurIPS 2026 Position Paper Track* — https://blog.neurips.cc/2026/06/02/ai-generated-papers-in-the-neurips-2026-position-paper-track/ — Appeals Process 全段逐字；"a link to an online version of their paper that has a **version history** including the work before and after the use of AI"；"**(1) a 'pre-AI' checkpoint** … **(2) a 'post-AI' checkpoint** … **(3) the final paper as submitted"；"**We expect that in future years this kind of audit trail will become a default.**"；"Submissions lacking such proof by **June 15th, 2026** will also be desk-rejected."；"Well-motivated equivalents may be considered." — Alex Lu, Seth Lazar, David Rügamer（Position Paper Chairs）；Stanley Hua, Kate Metcalf（Assistant PPC）— 2026-06-02
5. ICLR 2027, *AI Policy for Authors* — https://iclr.cc/Conferences/2027/AIPolicyForAuthors — "both in the paper's text as well as in the paper submission form"；"a **mandatory section in their paper (this section will not be counted towards the page limit)**"；官方 boilerplate 全文；Required / Recommended 任务清单全文；"might lead to desk rejection of the paper" — ICLR 2027
6. ICLR 2027 Author Guidelines — https://iclr.cc/Conferences/2027/AuthorGuidelines — ICLR 2027
7. CASRAI, *Elsevier AI Policy: What to Write & Where* — https://casrai.org/guides/elsevier-generative-ai-authorship-policy — 标题 "Declaration of generative AI and AI-assisted technologies in the manuscript preparation process"；Elsevier 逐字模板 "During the preparation of this work the author(s) used [NAME OF TOOL / SERVICE] in order to [REASON]. After using this tool/service, the author(s) reviewed and edited the content as needed and take(s) full responsibility for the content of the publication."；"immediately before the reference list"；"Basic grammar, spelling and punctuation checks … **No — explicitly exempted**"；图片允许/不允许清单；审稿人不得上传稿件 — CASRAI Editorial Board — last updated 2026-08-24，verified 2026-08-16 against elsevier.com
8. IEEE Open, *Author Guidelines for Artificial Intelligence (AI)-Generated Text* — https://open.ieee.org/author-guidelines-for-artificial-intelligence-ai-generated-text/ — "shall be disclosed in the **acknowledgments section**"；"The AI system used shall be identified, and **specific sections of the article that use AI-generated content shall be identified and accompanied by a brief explanation regarding the level at which the AI system was used**"；"The use of AI systems for editing and grammar enhancement is common practice and, as such, is generally outside the intent of the above policy. In this case, disclosure as noted above is **recommended**." — IEEE — 2024-04-16
9. COPE, *Authorship and AI tools*（COPE position）— https://publicationethics.org/guidance/cope-position/authorship-and-ai-tools — "AI tools cannot be listed as an author of a paper."；"must be transparent in disclosing **in the Materials and Methods (or similar section)** of the paper **how the AI tool was used and which tool was used**"；"Authors are **fully responsible** for the content of their manuscript, even those parts produced by an AI tool"；DOI `10.24318/cCVRZBms` — COPE Council — last reviewed 2023-02-13
10. ICMJE, *Recommendations … A. Use of AI by Authors* — https://www.icmje.org/recommendations/browse/artificial-intelligence/ai-use-by-authors.html — "the journal should require authors to disclose **at submission** whether they used AI-assisted technologies"；"should describe, **in both the cover letter and the submitted work in the appropriate section** if applicable, how they used it"；"Chatbots (such as ChatGPT) and other AI-assisted tools **should not be listed as authors**"；"**Nondisclosure of AI use may require corrective action and may be construed as misconduct in some circumstances**" — ICMJE
11. ICMJE, *Recommendations … Manuscript Preparation*（AI 总入口）— https://www.icmje.org/recommendations/browse/artificial-intelligence/ — "Editors/publishers, authors, and reviewers should be **transparent in their use of AI tools at any stage** of the editorial process" — ICMJE
12. COPE, *Artificial intelligence and authorship*（news-opinion）— https://publicationethics.org/news-opinion/artificial-intelligence-and-authorship — "Both the WAME guidance and COPE's own position statement concur: **AI bots should not be permitted as authors**" — 2023-02-27
13. CASRAI, *Can AI Be an Author? ICMJE & COPE Rules* — https://casrai.org/guides/can-ai-be-listed-as-an-author — "ICMJE, COPE, and major scholarly publishers hold a uniform position: AI tools cannot be listed as authors because [they cannot take responsibility]" — 2026-08-09
14. ai-cards.org, *AI tools for research: a disclosure log template for papers and [projects]* — https://ai-cards.org/ai-tools-for-research/ — "Use one row per AI-assisted task."；12 字段表全文；完整 Markdown 模板代码块；prompt record 模板；"Save prompts and outputs when the tool shaped research content."；提交前四分组法；"A tool log without human review reads like a receipt." — 2026-08-03
15. SciSpace, *Disclose with Confidence: Model, Prompt, and Source Logging for Scholarly AI Use* — https://scispace.com/resources/disclose-with-confidence-model-prompt-and-source-logging-for-scholarly-ai-use/ — "document as you go rather than trying to reconstruct everything later"；"Review logs periodically rather than waiting until submission."；"At a minimum, note the prompts you used, the AI model and version, and any key outputs that influenced your writing or analysis."；Final Checklist 10 条 — Tulika K（SciSpace）— 2026-06-16
16. ontola/atomic-plugins, NLnet GenAI disclosure session log — https://github.com/ontola/atomic-plugins/blob/main/syncables/docs/ai-logs/sessions/2026-08-24-nlnet-genai-disclosure.md — Session URL / Model（`claude-sonnet-5`）/ Repos touched / Redactions applied 四字段头；"It **omits the coding assistant's internal system prompt, tool-call plumbing, and other harness scaffolding**"；Turn 编号格式 — 2026-08-24
17. ACM, *Policy on Authorship* — https://www.acm.org/publications/policies/new-acm-policy-on-authorship — "Anyone listed as author on an ACM submission must meet all the following criteria: 1. They are an identifiable hum[an]…" — ACM
18. PKC 2026 AI Tool Policy — https://pkc.iacr.org/2026/aipolicy.php — "We plan to generally follow the ACM Policy on the use of AI tools." — IACR — 2026-05-25
19. *LLMPT: A Template for Prompt Documentation in Scientific [Work]* — https://link.springer.com/chapter/10.1007/978-3-032-29596-5_12 — "we introduce LLMPT, a standardized template for documenting prompts and model configurations" — Springer — 2026-07-07
20. paperpal, *用AI写了论文，到底要不要披露？投稿前AI使用声明实操指南* — https://paperpal.cn/zh/blog/academic-writing-guides/how-to-disclose-ai-use-academic-submission — 中文二次整理（未采信其中未在官方页面核实的数字）— 2026-07-06
