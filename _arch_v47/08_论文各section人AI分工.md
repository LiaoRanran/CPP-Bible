# 方向 08：论文各 section 的人/AI 分工

> 调研时间：2026-09-29。目标：为「阙疑」项目（NeurIPS 2027 E&D 投稿）给出**逐 section 的人/AI 分工红线**。核心参照物是 NeurIPS 2026 Position Paper Track 官方博客在 2026-06-02 发布的 **Table 4「AI 使用案例与合规性」**，它把 LLM 用途切成三类：**Clearly permissible（明确允许）/ Borderline permissible（边界允许）/ Clearly impermissible（明确禁止）**，并且**用 Pangram 3.3.2 对每一类做了实测**。

---

## 核心结论

1. **官方已经用检测器把「三类」跑成了实验结果，而不是原则口号。** NeurIPS 2026 Position Paper Track 对 969 篇投稿用 **Pangram v3.3.2** 筛查：**178 篇（18.4%）直接 desk reject**、**123 篇（12.7%）被要求补证据**、**668 篇（68.9%）通过**；其中 178 篇又分三档：**Pangram score ≥0.9 共 77 篇**、**≥0.8 且作者有多篇独著或另有一篇被拒共 79 篇**、**≥0.5 但作者声明「未使用 AI」或留空共 22 篇**。**22 篇这一档是最致命的**——它的触发条件不是分数高，而是**声明与实测不符**（官方原话：desk-rejected for scoring at or above *fifty percent* on an AI detector, where the author either declared no AI use or left the declaration blank）。
2. **Table 4 的实测结论可以浓缩成一句话：允许的用途 Pangram 一篇都没标；禁止的用途全部被标。** 官方原文：对于所有「允许」用途，Pangram **未将任何一篇分类为 AI 生成**；而「明确禁止」的用途**均被标记为 AI 生成**。在「部分 AI 补全」诊断实验中，Pangram **从未**把 AI 补全比例 **≤20%** 的文本判为 AI 生成。也就是说，**存在一个实测出来的、约 20% 文本量的「安全窗」**，但 Table 4 同时把「Hybrid revision（人机来回修订、人类转述 AI 编辑）」列入 **Borderline**，说明**窗宽不等于免责**。
3. **逐 section 分工的合理落点是：越靠「可核验事实」的 section，AI 介入应越低；越靠「语言表达」的 section，AI 介入可越高。** 按 Table 4 反推：Abstract / Introduction / Related Work 属"语言重、事实可核"→ 允许到 **Light copyediting** 为止；Method / Evaluation 属"逻辑与因果重"→ 只允许 **Proofreading**，一旦让 LLM「重组段落或论证呈现方式」即落入 **Structural rewriting（Borderline）**，若改动论点/推理/框架即 **Substantive AI rewriting（明确禁止）**；Threats to Validity / Limitations 属"作者自陈"，**必须人类亲写**，因为它是审稿人判断作者是否真正理解自己系统的唯一入口。真实数据佐证：Liang et al.（*Patterns* 2023 与 *Nature Human Behaviour* 2025）在 **1,121,912 篇**论文上估计，截至 2024-02，计算机科学领域**摘要**约 **17.5%** 句子被 LLM 改动、**引言**约 **15.3%**，而数学摘要仅 **4.9%**、引言 **3.5%**——**越靠"论证"的领域/章节，人类痕迹保留得越多**。

---

## 精确数字与案例

### 一、Table 4 全文（三类用途 + 诊断测试）

来源：NeurIPS Blog, *AI-Generated Papers in the NeurIPS 2026 Position Paper Track*, 2026-06-02。表中「测试内容」为原文描述。

| 类别 | 使用案例 | 测试内容（LLM 被要求做什么） |
|---|---|---|
| **Clearly permissible** | Proofreading | 只编辑拼写、标点、语法、引文格式 |
| **Clearly permissible** | Light copyediting | 只改局部清晰度、简洁性、别扭措辞、句子级润色，不做实质改动 |
| **Borderline permissible** | Heavy copyediting / line editing | 大量措辞改动与句子重构，但保留相同论点与推理 |
| **Borderline permissible** | Structural rewriting | 重新组织段落或论证呈现方式，但保留人类的想法 |
| **Borderline permissible** | Hybrid revision | 人类与 AI 都实质性塑造文本（来回助手使用 / 人类转述 AI 编辑）；官方用 Codex 测了 **5 轮编辑** |
| **Borderline permissible** | Translation / backtranslation | 跨语言翻译，保留含义但表层措辞可能被大量替换 |
| **Clearly impermissible** | Generation from a single-sentence human plan | 人写一句计划，AI 生成整段 |
| **Clearly impermissible** | Substantive AI rewriting | 要求 LLM 改论点、推理、框架或论证结构 |
| **Clearly impermissible** | Original AI-authored passage | LLM 按例子/主题/指示新写一段立场论文式段落 |
| **Clearly impermissible** | Human edits AI work | 人类对 AI 原创段落做细微修改 |
| **Diagnostic** | AI residue | 在人类文本里插明显聊天痕迹（如 "sure, here is your paragraph"） |
| **Diagnostic** | Partial AI completion | AI 接收部分人类原文并补全其余；条件为 AI 补全 **5/10/15/20/25/30/35/40/45/50/55/60/65/70/75/80/85/90/95%** |

**实测结果（逐字要点）**：所有「允许」用途 **0 篇**被判 AI 生成；所有「明确禁止」用途**全部**被判 AI 生成；部分补全实验中 **≤20% 从未**被判 AI 生成。

### 二、178 篇的三档阈值（Table 5）——「声明不符」比「分数高」更致命

| 结果 | Pangram AI Score | 附加条件 | 篇数 |
|---|---|---|---|
| Desk reject（无申诉） | ≥0.9 | 无 | **77** |
| Desk reject（无申诉） | ≥0.8 | 作者提交了多篇独著论文且至少一篇高于阈值，或至少一位作者另有一篇被拒 | **79** |
| Desk reject（无申诉） | ≥0.5 | 作者声明未使用 AI，或未作 AI 声明 | **22** |
| — | — | **合计（占全赛道 18.4%）** | **178** |
| Desk reject（可申诉） | ≥0.8 且 <0.9 | 需在 **2026-06-15** 前提交版本历史证据 | **123** |

**行动含义**：如果阙疑的某一段是 AI 生成但你在 AI 声明里写「未使用」，**Pangram 分数只要过 50% 就会被直接拒且无标准申诉通道**。这正是"分工"问题从"写得好不好"变成"声明与痕迹是否自洽"的地方。

### 三、分 section 的 AI 使用率实测（Liang et al.）

来源：*Mapping the Increasing Use of LLMs in Scientific Papers*（arXiv:2404.01268，Stanford，2024-04）；扩展版 *Quantifying large language model usage in scientific papers*（Liang et al., *Nature Human Behaviour*, 2025，覆盖 **1,121,912** 篇预印本与已发表论文，2020-01 至 2024-02）。

| 领域 | 摘要被 LLM 改动比例（截至 2024-02） | 引言被 LLM 改动比例 |
|---|---|---|
| Computer Science | **17.5%** | **15.3%** |
| Electrical Eng. & Systems Science | **14.4%** | **12.4%** |
| Mathematics | **4.9%** | **3.5%** |
| Nature portfolio（15 刊） | **6.3%** | **6.4%** |
| 发布前基线（2022-11） | cs 2.3% / eess 2.9% / math 2.4% / Nature 3.1% | — |

**分组差异**：第一作者预印本 ≥3 篇者摘要改动 **19.3%**（引言 16.9%），≤2 篇者 **15.6%**（13.7%）；与最近邻嵌入更相似的论文 **22.2%**，不相似的 **14.7%**；短论文（<5000 词）**17.7%**，长论文 **13.6%**。词频突增的四个词：**realm, intricate, showcasing, pivotal**（2023 年起骤增）。

**对阙疑的直接含义**：**Abstract 是全场 AI 痕迹最重的 section**。而 Abstract 恰好也是 Pangram 最先扫、权重最大的部分——所以"摘要必须人类亲写、且要能追溯到人写的那一版"是本方向最强的可执行结论。

### 四、可留下的人工痕迹（官方申诉清单是唯一权威模板）

NeurIPS 2026 PPT 给 123 篇有条件论文列的申诉证据要求（逐字）：

> - Authors must supply the Track Chairs with a link to an online version of their paper that has a version history including the work before and after the use of AI
> - They must identify (1) a "pre-AI" checkpoint indicating that they developed the substantive content of the paper independent of AI, (2) a "post-AI" checkpoint immediately after their most substantive AI-written edits, and (3) the final paper as submitted.
> - They must present analysis showing that the AI edits in (2) did not introduce new substantive content that was not present in (1), and of human edits after (2) which demonstrate that (3) was appropriately verified by human authors.

**这三点正好构成"可验证人工痕迹"的操作定义**：① 一个**人写基线版本**；② 一个**AI 编辑后版本**；③ 一段**人类复核后**的 diff。换句话说，**"留下可验证人工痕迹" = 留下三段式版本历史 + 能证明 AI 没引入新实质内容的 diff**。而**纯 git 仓库天然满足前两点**——这恰好是阙疑相对"Word 里改来改去"的作者的结构性优势。

### 五、其它 venue 的 section 级规范（作为下限参照）

| 机构 | 文件 | 逐字要点 |
|---|---|---|
| ICMJE | *Recommendations: Use of AI in Publishing* | "Authors should not list or cite AI and AI-assisted technologies as an author."；"When AI is used, users should disclose which tool was used, and for what purpose." |
| COPE | *Authorship and AI tools*（2023-02-13） | AI 工具不能作为作者；使用须在 Materials/Methods 或 Acknowledgements 中透明披露 |
| WAME | 2023-01-20 policy statement | "Chatbots cannot be authors because they cannot meet authorship requirements" |
| Nature Portfolio | *nr-editorial-policy-checklist*（2023-04） | "Large Language Models (LLMs), such as ChatGPT, do not currently satisfy our authorship criteria." |

**注意**：ICMJE 说披露位置可在 cover letter / acknowledgements；**NeurIPS PPT 则要求写进 submission 的 AI 声明字段**。两者不冲突，但**阙疑投稿时必须在 OpenReview 表单的 AI 声明里逐项列出**，因为 NeurIPS 是"以声明为判据"而非"以正文为判据"。

### 六、E&D 特有的"section 等价物"：README / Croissant / 复现清单

E&D 投稿里有一批**不是 section、但起 section 作用**的文本，它们的 AI 风险被严重低估：

| 文本载体 | 为什么它比正文更危险 | 建议档位 |
|---|---|---|
| **README / 复现说明** | 会被 reviewer 与 AC 逐行执行；措辞含糊=直接暴露"没跑过" | Proofreading 上限 |
| **Croissant core + RAI 字段** | 字段值可被机器校验（如 `citeAs`、`license`、`rai:dataCollection`），**AI 幻觉出一个不存在的 license 会被 checker 抓** | 人类填写，AI 仅做 JSON 格式校验 |
| **Threats to Validity / Limitations** | 是审稿人判断"作者是否理解自己系统"的唯一入口；也是官方 checklist 的必填项 | 人类亲写 |
| **Reproducibility Checklist 勾选项** | 勾选即承诺；与 Pangram 声明同理，**"勾了但做不到"= 22 篇那类风险** | 人类逐条勾 |
| **Response / Rebuttal** | NeurIPS 2026 Main Track 明文 "The per-review rebuttal limit is 10,000 characters"、"不能上传附件"、"Do not use links in any part of the response" | 人类亲写（详见方向 11） |

**关键机制**：正文里一句 AI 味的话，最多是"风格可疑"；**README 里一句 AI 味的话，是"可执行承诺"**——reviewer 会真的去跑它。所以 E&D 的实际分工原则应比 PPT 的 Table 4 更保守一档：**凡是被机器或人"执行"的文本，一律按 Proofreading 处理。**

### 七、把"人工痕迹"变成可审计产物的四种载体

官方申诉清单只给了抽象要求，落到阙疑的工程实践有四种具体载体，可靠性从高到低：

1. **git 提交历史（最强）**：提交时间戳、作者、diff 三者不可事后伪造（除非 rebase）。风险：**匿名化时若用 `git-filter-repo` 重写历史，时间戳可能被保留但作者信息被抹**——所以要在匿名化**之前**导出完整历史存档（见方向 19）。
2. **LaTeX 编辑器的 tracked changes / Overleaf 版本历史（较强）**：官方明确点名 "Use tracked changes in your word processor or keep Git commits if you write in LaTeX"。
3. **prompt provenance log（中）**：记录"哪一轮问了什么、输出被采纳了多少"。这是**唯一能证明"AI 没引入新实质内容"的正面证据**（见方向 05）。
4. **手写草稿照片 / 纸质笔记（弱但不可替代）**：对 Abstract 这类高风险 section 有特殊价值，因为它是**唯一的"非电子"人写证据**。

**反例警示**：官方披露有作者用 **Codex 做了 5 轮编辑**（即 Table 4 的 Hybrid revision 条件），最终落入 Borderline——**"多轮 AI 编辑"本身不构成加分，反而因为留痕过多而更难自证**。

---

## 对阙疑的 3 条具体行动

1. **建立 `docs/paper/AI_USAGE_MATRIX.md`，逐 section 写死"允许到哪一档"，并在 2027-01 前冻结。** 表格字段：`section | 允许档位（Proofreading / Light copyedit / Heavy copyedit / Structural rewrite / 禁止） | 谁写的初稿 | AI 工具与版本 | 人工复核人 | 对应 git tag`。建议初始赋值：Abstract=Light copyedit、Intro=Light copyedit、Related Work=Light copyedit、Method=Proofreading、Evaluation=Proofreading、Threats to Validity=**人类亲写（连 Light copyedit 都不做）**、Limitations=人类亲写、Appendix=Proofreading。理由：Table 4 把 "Structural rewriting" 归为 Borderline，而 Method/Evaluation 一旦被"重组论证"就接近 "Substantive AI rewriting"（明确禁止）。**时间点：2027-05 投稿前必须已冻结并逐条对照 git tag。**
2. **为每个 section 建"三段式版本证据链"，直接用 git tag 落地。** 具体命令序列：`git tag -a sec-method-human-baseline -m "Method 初稿，纯人写，无 LLM"` → 允许 LLM 做 Light copyedit 后再 `git tag -a sec-method-post-copyedit` → 人工复核后 `git tag -a sec-method-final`；随后生成逐 tag diff 存档到 `docs/paper/provenance/method_diff.txt`（`git diff sec-method-human-baseline sec-method-final -- paper/method.tex > docs/paper/provenance/method_diff.txt`）。**这就是官方要求的 (1)(2)(3) 三检查点的本地实现，且第三条能直接回答"AI 是否引入新实质内容"。**
3. **在 OpenReview AI 声明字段里做"逐 section 声明"，而不是一句"AI used for language polishing"。** 声明模板建议（写进 `docs/paper/AI_USAGE_MATRIX.md` 末尾）：`Sections proofread by an LLM: Abstract, Intro, Related Work (grammar/punctuation only). Sections with human-only authorship: Method, Evaluation, Threats to Validity, Limitations. No section was generated from a plan or rewritten substantively by an LLM. Tool: <name+version>. Provenance: git tags sec-*-human-baseline / -post-copyedit / -final in the anonymized repo.` **理由：178 篇里有 22 篇是因为"声明与实测不符"被拒的——把声明做细，是把风险从"分数"转到"可核验的自洽性"。**

---

## 盲区（诚实标注）

- **Table 4 的"三类"是 Position Paper Track 的官方口径，不是 E&D Track 的官方口径。** E&D 2026 CFP 只写了 "The Call for Papers of the NeurIPS 2026 Evaluations and Datasets will follow the Call for Papers of the NeurIPS 2026 Main Track"，**没有逐 section 表格**；而 `https://neurips.cc/public/LLM` 页面在本次抓取时内容为 **"Coming Soon"**，Main Track Handbook 的 LLM 条款原文**未取到逐字文本**。因此"E&D 2027 会沿用 PPT 的 Table 4"是**推断**，不是已核实事实。
- **Pangram 的 20% 安全窗来自官方自述，第三方未复现。** 官方称 "Pangram never classified 20% or below as AI-generated"，但该实验的语料、prompt、窗口设置均未公开，且 Pangram 版本从 3.3.2 迭代到 4（2026-07，官方报 AUROC **0.9916**、FPR **0.0041%**，v3.3.2 FPR 为 **0.0539%**）后阈值行为可能改变。**不要把这个 20% 当作可依赖的安全边际。**
- **"逐 section 允许档位"表是我按 Table 4 反推的，没有官方 section 映射。** Table 4 按"LLM 被要求做什么"分类，不按 section 分类；把它映射到 Abstract/Intro/Method/Threats 是本次调研的**解释性推断**，可能存在与官方意图不符之处。
- **Liang et al. 的百分比是"估计的 LLM 改动句子比例"，不是"AI 生成比例"。** 其方法为词频分布偏移的统计估计（验证误差 <3.5%），**不能**用来推断某篇具体论文的 AI 含量，也**不能**与 Pangram 的 score 直接换算。
- **COPE / WAME / Nature 的具体逐字日期与措辞**部分来自二次转载页面（如 pjohns.pso-hns.org 对 WAME 的转载），**原始 COPE 页面本次未逐字打开**（仅取得搜索结果摘要），细节以原文为准。

---

## 来源

1. AI-Generated Papers in the NeurIPS 2026 Position Paper Track — https://blog.neurips.cc/2026/06/02/ai-generated-papers-in-the-neurips-2026-position-paper-track/ — 含 Table 4（三类用途）、Table 5（77/79/22 阈值）、178/123/668、Pangram v3.3.2、FPR <0.1%、三段式申诉证据要求 — NeurIPS Communication Chairs — 2026-06-02
2. NeurIPS Desk-Rejected 178 Position Papers for Being "AI-Generated" — https://strictcite.com/blog/neurips-2026-position-paper-pangram-ai-detection — 969 篇 / 178（18.4%）/ 123（12.7%）/ 668（68.9%）；42.7% 落 90–100%；Pangram 4 AUROC 0.9916 / FPR 0.0041%；v3.3.2 FPR 0.0539%；TOEFL 89 篇 0 误报 — 2026-09-08（2026-09-26 更正）
3. What's new for the Position Paper Track at NeurIPS 2026 — https://blog.neurips.cc/2026/03/30/whats-new-for-the-position-paper-track-at-neurips-2026/ — "around 35% of reviewers were not responsive"；Responsible Reviewing 跨赛道 — NeurIPS Communication Chairs — 2026-03-30
4. NeurIPS 2026 Evaluations & Datasets Track Call for Papers — https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets — "evaluation becomes an object of scientific study in its own right"；双盲为默认；Croissant core + RAI；匿名化代码要求 — NeurIPS — 2026
5. NeurIPS LLM Policy — https://neurips.cc/public/LLM — 页面内容为 "Coming Soon"（**未取到正文**）— NeurIPS
6. ICMJE, Use of Artificial Intelligence in Publishing — https://www.icmje.org/recommendations/browse/artificial-intelligence/ — "Authors should not list or cite AI ... as an author"；"disclose which tool was used, and for what purpose" — ICMJE — 2023 起持续更新
7. COPE, Authorship and AI tools — https://publicationethics.org/guidance/cope-position/authorship-and-ai-tools — AI 工具不能作为作者 — COPE — 2023-02-13
8. Nature Portfolio editorial policy checklist — https://www.nature.com/documents/nr-editorial-policy-checklist-Apr-2023-flat.pdf — "LLMs, such as ChatGPT, do not currently satisfy our authorship criteria" — Nature Portfolio — 2023-04
9. Mapping the Increasing Use of LLMs in Scientific Papers — https://arxiv.org/html/2404.01268v1 — cs 摘要 17.5% / 引言 15.3%；math 4.9% / 3.5%；Nature 6.3% / 6.4%；realm/intricate/showcasing/pivotal — Liang et al.（Stanford）— 2024-04
10. Quantifying large language model usage in scientific papers — https://nlp.stanford.edu/~manning/papers/Liang_et_al-2025-Nature_Human_Behaviour.pdf — 1,121,912 篇，2020-01 至 2024-02 — Liang et al., *Nature Human Behaviour* — 2025
11. LLMs as Research Tools: A Large Scale Survey of Researchers' Usage — https://arxiv.org/html/2411.05025v1 — 816 名作者中 **80.88%** 在研究中使用 LLM；Information Seeking 49%、Editing 45% — 2024-11（OpenReview p0BwJk3R1p）
12. NeurIPS Paper Checklist Guidelines — https://neurips.cc/public/guides/PaperChecklist — checklist 项包含 code/data/instructions 与 limitations 讨论 — NeurIPS
13. NeurIPS 2026 AI-Assisted Reviewing Experiment — https://neurips.cc/Conferences/2026/ai-reviewing-experiment — 自愿参与的 AI 辅助评审实验（细节未逐字取全）— NeurIPS 2026
