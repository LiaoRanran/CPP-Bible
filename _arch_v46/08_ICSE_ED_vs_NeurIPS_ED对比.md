# 方向 08：ICSE / FSE / ASE 的评估类 track 与 NeurIPS E&D 对比

> 调研时间：2026-09-29（GMT+8）
> 检索工具：WebSearch ×12 + WebFetch ×10（ICSE/FSE/ASE 官方 researchr 与 HotCRP、OpenAccept、NeurIPS 官方 CFP 与 reviewer guidelines）
> 锚点：阙疑（queyi）——单作者、双非本科、合肥、0 影响力；需要"单人能活下来"的 venue

## 核心结论

1. **NeurIPS E&D 的截稿窗口极短且只有一次机会**：abstract 2026-05-04、full paper 2026-05-06、rebuttal 只有 **5 天**（07-22 至 07-27）、decision 2026-09-24；而 ICSE 提供**两个独立投稿周期**（ICSE 2026：Cycle 1 截稿与 Cycle 2 截稿相隔约 4 个月），FSE/ASE 则是一年一次但配套 track 极多。
2. **录用率上，NeurIPS E&D 与 ICSE/ASE 主 track 处于同一量级（20–25%）**：ICSE 2026 总录用率 21.85%（321/1,469）、ICSE 2025 为 21.30%、ASE 2025 为 21.6%（245/1,136）、NeurIPS 2024 D&B track 为 25.3%（1,820 篇）、NeurIPS 2025 主 track 为 24.52%。
3. **对单人生存友好度，ICSE/FSE/ASE 明显优于 NeurIPS E&D**：三会都有 **Artifact Evaluation、Tool Demonstration、NIER/IVR（新想法与反思）等"低门槛但可引用"的通道**，且 ICSE 的评审标准明确把 **Verifiability and Transparency** 单列为五个维度之一并承诺"任何随论文提交或链接的工件会被至少一位审稿人检查"——这正好是阙疑"可被独立验收"主张的天然落点。

## 精确数字与案例

### 一、NeurIPS E&D track：时间线与硬约束

**Key dates（与主 track 完全一致，来自官方 E&D CFP）**
- Abstract submission deadline: **2026-05-04（AoE）**（所有作者此时必须有 OpenReview profile）
- Full paper submission deadline（含全部补充材料）: **2026-05-06（AoE）**
- Author notification: **2026-09-24（AoE）**
- 投稿门户开放：**2026-04-15**

**评审时间线（来自 E&D 2026 Reviewing Guidelines，逐日精确）**

| 阶段 | 日期 |
|---|---|
| Review period | 2026-05-29 ~ 06-25 |
| Emergency review period | 07-06 ~ 07-13 |
| AC initial meta-review | 07-13 ~ 07-22 |
| Paper Reviews released | 07-22 |
| **Authors rebuttal** | **07-22 ~ 07-27（5 天）** |
| Author + Reviewer + AC discussion | 07-27 ~ 08-03 |
| Reviewer + AC discussion | 08-03 ~ 08-10 |
| Meta-Review | 08-10 ~ 08-17 |
| Paper Decision notification | 09-24 |

即：**从出分到 rebuttal 截止只有 5 天**，而审稿意见在 rebuttal 结束时才对审稿人可见（见方向 06）。这是阙疑必须提前准备"弹药库"的根本原因。

**格式与政策（E&D 特有）**
- 页数：与主 track 相同，正文 **9 个内容页**（含全部图表），references / 可选技术附录 / 强制 checklist 不计入；camera-ready 可加 1 页。
- **评审模式：2026 年起 E&D 默认双盲**（"Unlike previous years, the default review mode for the E&D Track is now double-blind"）。只有"因科学或伦理原因无法完全匿名化"的数据集类投稿，才可在 submission form 中选择 single-blind。
- **code policy 是"按贡献类型而定"（contribution-dependent）**："code release is **required** at submission when the primary contribution is a reusable executable artifact, such as a benchmark suite, evaluation environment, data generator, or software tool, whose functionality must be inspected in order to evaluate the scientific claims." 对分析性/实证性/概念性/方法性贡献，代码**非强制**，但论文须含足够细节。
- **LLM 政策（严格）**："Our policy is strict: **reviewers may not use any LLMs or AI agents in the review process.**" "Unlike the Main Track, which is conducting a separate experiment involving sanctioned LLM support through OpenReview, **no such experiment applies to the ED track**." 制裁："possible **desk rejection of the reviewers' associated submissions**."
- **评审标准四维**：Quality / Clarity / Significance / **Originality**。E&D 对 Originality 的界定极其宽松且对阙疑有利：
  > "Originality does **not** necessarily require introducing an entirely new method. Providing novel insights, exposing failure modes, evaluating existing methods, or framing new metrics is equally valuable."
  > "**Beating a baseline is not required.**"（Benchmark 类）
  > "New framing is sufficient - no need to beat a baseline."（Evaluation Methodology 类）
- **唯一的不利条款**：数据集类 "**Datasets-as-endpoints don't meet the bar on their own.**"
- **2026 年 scope 的重大变化**：track 从 "Datasets & Benchmarks" 更名为 "Evaluations & Datasets"，官方定位是 **"evaluation becomes an object of scientific study in its own right"**。Scope 明确包含："rigorous reproduction, auditing, and stress-testing of prior evaluations"、"Present negative results, critical analyses, and use-case-inspired evaluations"、"Study benchmark saturation or overfitting and their impact on scientific conclusions"。

**E&D 的历史规模与录用率**
- NeurIPS 2024 D&B track：投稿 **1,820** 篇，录用率 **25.3%**。
- NeurIPS 2025 D&B track：投稿 **1,995** 篇；组织规模为 **41 名 SAC、281 名 AC、2,680 名审稿人**。
- NeurIPS 2025 主 track（对照）：投稿 **21,575** 篇，接收 **5,290** 篇，录用率 **24.52%**；**20,518 名审稿人、1,663 名 AC、199 名 SAC**。
- E&D 官方定位："We aim for an **equally stringent review** as the main conference track."
- **2025 年 E&D/D&B 的作者与审稿人调查**（851 名作者 + 155 名审稿人回应）：
  - 作者侧：**82%** 报告 hosting 过程顺利，**16%** 遇到困难（主因：≥1TB 超大数据集、平台限速、截止前不稳定）；
  - **58%** 作者同意新要求带来更公平或更彻底的评审，**25%** 认为评审质量需改进（抱怨集中在"审稿人在 rebuttal 中参与有限""依赖 AI 生成的反馈"）；
  - 审稿人侧：**77%** 认为数据集易于访问，**约 10%** 遇到困难（链接缺失/失效、超大文件），**11%** 根本没有直接检查数据集、只根据论文做评估；
  - **69%** 审稿人认为自动元数据报告有用，**70%** 认为合规 checklist 提升了评估效率。

### 二、ICSE：唯一提供"一年两次机会"的顶会

**ICSE 2026 Research Track 实际结果（来自官方 HotCRP 公告页）**
- Cycle 1：收到 **660** 篇投稿，**60** 篇直接录用 + **101** 篇大修后录用 = 161 篇，录用率 **24.4%**；
- Cycle 2：收到 **809** 篇投稿，**72** 篇直接录用 + **88** 篇大修后录用 = 160 篇，录用率 **19.8%**；
- **总计 1,469 篇投稿，321 篇录用 → 21.85%**。

**ICSE 近 13 年主 research track 录用率（OpenAccept 数据）**

| 年份 | 投稿数 | 接收数 | 录用率 |
|---|---|---|---|
| 2025 | 1,150 | 245 | 21.30% |
| 2024 | 1,051 | 234 | 22.26% |
| 2023 | 780 | 207 | 26.54% |
| 2022 | 691 | 197 | 28.51% |
| 2021 | 615 | 138 | 22.44% |
| 2020 | 617 | 129 | 20.91% |
| 2019 | 504 | 109 | 21.63% |
| 2018 | 502 | 105 | 20.92% |
| 2017 | 415 | 67 | 16.14% |
| 2016 | 530 | 101 | 19.06% |
| 2015 | 452 | 84 | 18.58% |
| 2014 | 496 | 99 | 19.96% |
| 2013 | 461 | 85 | 18.44% |

（注：2025/2026 因改为双周期，投稿数统计口径与其他年份不可直接比较；2026 的 1,469 是两周期合计。）

**ICSE 2025 的完整流程（这是理解 ICSE 的关键）**
- **双投稿周期**：Cycle 1 摘要 2024-03-15 / 投稿 2024-03-22 / author response 2024-06-11~13 / notification 2024-07-05 / revision due 2024-08-02；Cycle 2 摘要 2024-07-26 / 投稿 2024-08-02 / author response 2024-10-08~10 / notification 2024-11-01 / revision due 2024-11-29。所有时间均为 23:59:59 AoE。
- **结果类型三种：Accept / Revision / Reject**。Revision 需用 LaTeXdiff 等工具**以不同颜色标注修改**，并额外提交 "Author Response" 文档逐条回应审稿人意见；修改稿由**同一组审稿人**再审；给 **4 周**修改时间（比往年少 1 周，因为把时间重新分配给了 author rebuttal）。
- **页数：正文最多 10 页**（含所有图、表、附录），另有 **2 页仅限参考文献**，PDF 格式，camera-ready 加 1 页。模板必须 `\documentclass[10pt,conference]{IEEEtran}`，**不得**含 compsoc 或 compsocconf 选项。
- **双盲（double-anonymous）**：必须省略作者姓名；引用自己先前工作必须用第三人称；可在 arXiv 上传预印本但**不得声明投给了 ICSE 2025**。
- **Author Response 是 2025 年重新加入的**（"NEW THIS YEAR #2: We add back opportunities for 'Author Response' in addition to 'Major Revision'"）。
- **九个研究领域**（投稿时选一个）：AI for Software Engineering、Analytics、Architecture and Design（本年新增）、Dependability and Security、Evolution、Human and Social Aspects、Requirements and Modeling、**Software Engineering for AI**、Testing and Analysis。
- **五个评审标准**：Novelty、Rigor、Relevance、**Verifiability and Transparency**、Presentation。
  > "iv) Verifiability and Transparency: The extent to which the paper includes sufficient information to understand how an innovation works; to understand how data was obtained, analyzed, and interpreted; and **how the paper supports independent verification or replication of the paper's claimed contributions. Any artifacts attached to or linked from the paper will be checked by one reviewer.**"
- **开放科学政策**：鼓励披露匿名化、整理后的数据/工件以提高可复现性；**共享工件不是投稿或录用的必要条件**，但"sharing is expected to be the default, and non-sharing needs to be justified"。默认理解是"录用后数据/工件将公开可得"。对定性研究有豁免说明。
- **Desk reject 三类触发点**：格式不符（"Alterations of spacing, font size, and other changes that deviate from the instructions may result in desk rejection without further review"）；绕过被拒重投规则；并发投稿违规（"will lead to automatic rejection from ICSE 2025 as well as any other venue adhering to this policy"）。

### 三、ASE：早期拒绝 + 强制数据可用性声明

**ASE 2026 关键规则（来自官方 researchr 与投稿指南整理）**
- 截稿：**2026-03-26**；
- 页数：**10 页（不含参考文献）+ 2 页仅限参考文献**；
- 模板：`\documentclass[sigconf,review,anonymous]{acmart}`（ACM 双栏）；
- **早期拒绝阶段（early reject）**："为了让作者快速回复并减轻作者和审稿人在反驳阶段的负担，所有负面评分的论文将在反驳期前提前被拒。"
- **强制性数据可用性声明**（本年度新增强制）：须在 10 页限制内的正文结论后提交；数据或复制包须通过提供长期档案的 DOI 公开且匿名发布；所有导致论文结果的数据必须对审稿人和读者开放；不合适时须在声明中说明。
- **匿名要求**：省略作者姓名与机构；引用自己先前工作用第三人称；鼓励投稿标题与 arXiv 预印本标题不同；评审期间作者不应公开使用投稿标题。
- **ASE 2026 Tools and Datasets track** 单独截稿：**2026-07-22**。

**ASE 录用率（OpenAccept + 官方作者页交叉核对）**

| 年份 | 投稿数 | 接收数 | 录用率 |
|---|---|---|---|
| 2025 | 1,181 | 246 | 20.83% |
| 2024 | 587 | 155 | 26.41% |
| 2023 | 629 | 134 | 21.30% |
| 2022 | 531 | 116 | 21.85% |
| 2021 | 427 | 82 | 19.20% |
| 2020 | 408 | 93 | 22.79% |
| 2019 | 377 | 77 | 20.42% |
| 2018 | 315 | 64 | 20.32% |
| 2017 | 314 | 65 | 20.70% |
| 2016 | 284 | 53 | 18.66% |
| 2015 | 289 | 55 | 19.03% |
| 2014 | 276 | 55 | 19.93% |
| 2013 | 310 | 43 | 13.87% |

**ASE 2025 的官方口径（来自 ASE 2025 作者 Yi Li 的博客，2025-09-26）**：
> "This year, ASE received **1190 submissions** and **1136 were remaining after desk rejection**. Out of the 1136 submissions, **113 papers were directly accepted and 132 were accepted after major revisions**, which gives an overall acceptance rate of **21.6%**."

注意：这与 OpenAccept 的 1,181 / 246 / 20.83% 存在小幅差异（投稿数差 9，接收数差 1）。**本文同时给出两个口径**，不做取舍。

### 四、FSE：track 最多、双盲最严

**FSE 2026 的全部 track（官方 How to Submit 页面）**：Research Papers、Industry Papers、Student Research Competition、Software Engineering Education、**Journal-First**、Doctoral Symposium、**Artifacts**、**Tool Demonstrations**、**Workshops**、FSE-AIWare Joint Competition、**Ideas, Visions and Reflections（IVR）**。

**FSE 2026 关键政策**
- **"heavy" 双盲**：原文 "The double-anonymous process used this year is 'heavy', i.e., the paper anonymity will be maintained during all reviewing and discussion periods." 在 major revision 情况下，作者 response letter 也必须保持匿名。
- **建议推迟 arXiv**："we recommend the authors to postpone publishing their submitted work on arXiv or similar sites until after the notification"；若已上传，须避免说明投给 FSE 2026。
- **明确 desk reject**："Papers that do not comply with the double-anonymous review process (for the tracks that employ this process) **will be desk-rejected**."
- **并发/重复投稿**：不得已发表、不得在评审期内在别处评审；"The double submission restriction applies only to refereed journals and conferences, **not to unrefereed forums (e.g., arXiv.org)**."
- 格式：ACM Primary Article Template；research track 用 main proceedings，其他 track 用 companion proceedings（`\acmBooktitle{Companion Proceedings of the 34th ACM Symposium on the Foundations of Software Engineering (FSE '26), June 5--9, 2026, Montreal, Canada}`）。
- FSE 2026 会议地点/时间：**Montreal, Canada, 2026-06-05 ~ 06-09**。

**FSE 与 NeurIPS 的一个关键差异**：FSE 有 **Journal-First** track——已发表在期刊（TOSEM/TSE/EMSE 等）的论文可以到 FSE 做报告。这意味着 SE 社区有一条"期刊 → 会议曝光"的额外通道，而 NeurIPS 没有。

### 四之二、ISSTA：SE 顶会里被忽略的第四个选项

阙疑的候选 venue 清单通常只列 NeurIPS E&D / ICSE / FSE / ASE，但 **ISSTA（ACM SIGSOFT International Symposium on Software Testing and Analysis）是第四个 CCF-A 的 SE 顶会**，主题（测试与分析）与阙疑的"验证器"定位高度重合。OpenAccept 实测数据：

| 年份 | 投稿数 | 接收数 | 录用率 |
|---|---|---|---|
| 2025 | 550 | 107 | **19.45%** |
| 2024 | 694 | 143 | 20.61% |
| 2023 | 406 | 117 | 28.82% |
| 2022 | 250 | 61 | 24.40% |
| 2021 | 233 | 51 | 21.89% |
| 2020 | 162 | 43 | 26.54% |

**三条观察**：
1. **ISSTA 的投稿量在 2022→2024 两年内从 250 涨到 694（+177.6%）**，是四会里增速最快的，2025 年回落到 550；录用率随之从 2022 的 24.40% 降到 2025 的 **19.45%**——**比 ICSE（21.85%）、ASE（20.83%）、NeurIPS E&D（约 25%）都更严**。
2. **ISSTA 没有 ICSE 那样的"双周期"**，一年一次机会，但同样有 Artifact / 工具类通道（与 ICSE/FSE/ASE 同构）。
3. ISSTA 的录用率波动大（2023 年 28.82% 的"宽年"与 2025 年 19.45% 的"严年"相差 9.37 个百分点），**说明 SE 会议的年度难度不可预测，单年数据不能当作"难度基准"**。

**对阙疑的推论**：ISSTA 是"测试与分析"的专精会，对"验证器 / 规则引擎"的接受度天然高于泛 ML 会议；但其录用率是四会中最低的，**不应作为首选，而应作为 ICSE 被拒后的第二落点**。

**为什么 ISSTA 值得单独列出来**：ICSE/FSE/ASE 的截稿都在 3–8 月，而 **ISSTA 的 research track 通常在年初（1 月前后）截稿、年中开会**，是四会中**时间上最早的一次机会**。对阙疑的排期含义是：**若把 ISSTA 纳入候选，2027 年 1 月就会有一次投稿机会，早于 ICSE Cycle 1（3 月）与 NeurIPS E&D（5 月）**，可以当作"压力测试"——用一次真实评审检验稿件成熟度，且**不与后续投稿冲突**（ISSTA 的评审结果在 3–4 月公布，早于 ICSE 与 NeurIPS 的截稿）。

### 五、对"单人生存友好度"的六维打分

| 维度 | NeurIPS E&D | ICSE | ASE | FSE |
|---|---|---|---|---|
| 一年投稿次数 | 1 | **2（双周期）** | 1（+Tools/Datasets 另一次） | 1 |
| 从截稿到出分 | 4.6 个月 | 约 4 个月（Cycle 1）/ 2.7 个月（Cycle 2） | 约 6 个月 | 约 4 个月 |
| 是否有 rebuttal | 有（5 天） | 有（约 3 天窗口 + 4 周 revision） | 有（但负面评分提前拒） | 有 |
| 是否有"修改后录用" | 无 | **有（Revision）** | **有（major revision）** | 有 |
| 低门槛可引用通道 | Workshop（non-archival） | SEIP / NIER / SEIS / Journal-First / Tool Demo | Tools and Datasets / NIER / Industry Showcase | IVR / Tool Demo / Industry / Journal-First |
| 是否要求 artifact 检查 | 代码按贡献类型 | **有（Verifiability and Transparency 维度，至少一位审稿人检查工件）** | 强制数据可用性声明 | Artifact track 单独评审 |
| 对"评估/审计类"论文的态度 | 明确欢迎（2026 起 scope 中心就是 evaluation science） | 接受（Rigor 维度） | 接受 | 接受 |

**结论**：NeurIPS E&D 的"评估即科学对象"定位与阙疑最契合，但它**没有 revision 机制**、rebuttal 只有 5 天、且双盲下代码匿名化成本高。ICSE 的**双周期 + Revision + 至少一位审稿人检查工件**三点，对单作者、单仓库、无机构背书的项目是最友好的组合。

### 六、阙疑的可迁移资产盘点

阙疑现有可复算资产（来自 `00_仓库扫描.md` 实测，非 brief 旧值）：
- **67 条判决规则**（block 44 / warn 16 / advice 7），`data/_gate_rules.json`；
- **内核 `tools/gate_engine.py` = 3,826 行**；
- **盲 holdout 30 seeds**（真错 17 / 对照 9 / unknown 4），检出率 **66.7%**（10/15 可测）；
- **外部 corpus 40 条**（A/B/C 三层），检出率 **43.8%**（A 54.2% / B 12.5% / C 0%）；
- **真实缺陷夹具 15 条**，重注入检出 **6/6 = 100%**，历史覆盖 **12/15 = 80%**；
- **实卡 37 张**（verified 23 / red-team 3 / draft 11）+ draft650 草稿 10 张；
- **9 个保护器**、**452 条判决账本**（采信 README，未独立复算）。

对照 ICSE 的 "Verifiability and Transparency" 维度（"Any artifacts attached to or linked from the paper will be checked by one reviewer"），阙疑的**四态判决 + append-only 哈希链 + Merkle checkpoint + 不依赖内核的独立对账器**正是"可被独立验收"的具象化，与该维度是 1:1 对应关系。

## 对阙疑的 3 条具体行动

1. **把 ICSE 2026 Cycle 1 设为主目标、NeurIPS 2027 E&D 设为并行目标，并做时间线去冲突**：NeurIPS 2027 的 abstract 预计在 2027-05 上旬（按 2026 的 05-04 外推），ICSE 2027/2028 Cycle 1 通常在 3 月、Cycle 2 在 8 月。行动：在 `_arch_v46/` 建 `venue_timeline.md`，把两条时间线逐月对齐，明确"同一份稿件绝不双投"（NeurIPS handbook 明文：主 track 与 E&D 互投 = desk reject）。工具：纯 Markdown + 日历；时间点：2026-12-31 前完成。

2. **把 `data/` 与 `tools/` 打包成一个符合 ICSE "Verifiability and Transparency" 的匿名 artifact**：具体做三件事——(a) 一个 `reproduce.sh`，从零跑出 66.7% / 43.8% / 100% / 80% 四个数字；(b) 一份 `ARTIFACT.md` 说明每个数字对应的命令与预期输出；(c) 把 `tools/` 里 595 个 `.py` 收敛成一份**只含必要入口**的清单（595 个文件对审稿人是灾难）。命令：`bash reproduce.sh > out.txt 2>&1`，然后人工核对 out.txt。时间点：2027-02-28 前完成，直接对应 ICSE Cycle 1 的 artifact 检查。

3. **准备一个 ASE 2026 Tools and Datasets track 的备用投稿方案**（截稿 2026-07-22，或 2027 年对应日期）：ASE 的 Tools and Datasets track 专门收工具与数据，且 ASE 2026 强制"数据可用性声明 + 长期档案 DOI"。行动：在 `_arch_v46/` 记录一份 `ase_tools_submission_plan.md`，明确 (a) 页数 10+2 页的裁剪方案（把 3,826 行内核压成一张架构图 + 一段算法描述）；(b) 为 `data/holdout/holdout.json`、`data/external_corpus/external_corpus_665.json`、`data/defect_fixtures/defects.json` 各申请一个 Zenodo DOI（Zenodo 免费，提供长期档案 DOI）。时间点：2027-01-31 前完成方案，2027-06 前申请 DOI。

## 盲区（诚实标注）

- **NeurIPS 2026 E&D track 的实际投稿数与录用率未公布**（截至 2026-09-29，decision 日期为 2026-09-24，但官方 blog 尚未发布 E&D 统计）。本文用的是 **2024（1,820 / 25.3%）与 2025（1,995）** 的 D&B track 数字。
- **NeurIPS 2027 的 E&D CFP 尚未发布**；本文引用的全部日期来自 **NeurIPS 2026** 的 CFP 与 reviewer guidelines，2027 年可能变动（例如页数、rebuttal 时长、是否继续双盲）。
- **"NeurIPS E&D 2026 是否继续 single-blind 选项"未核实 FAQ 原文**，只读到 CFP 中"默认双盲 + 数据集类可申请 single-blind"的表述。
- **ASE 2025 的两个录用率口径不一致**：官方作者博客 1,190 / 1,136 / 245 / 21.6% vs OpenAccept 1,181 / 246 / 20.83%。**我未找到 ASE 官方公告页**来裁决，两个口径都已列出。
- **ASE 2026 的完整 research track CFP 原文我未读到**（`conf.researchr.org/track/ase-2026/ase-2026-research-track` 返回的是会议议程而非 CFP）；早期拒绝、强制数据可用性声明等条款来自**一篇中文博客（博客园 inertial-fish，2026-03-04）**的转述，**未与 ASE 官方原文逐字核对**。
- **FSE 2026 research track 的 CFP 原文我未读到**（同样返回议程页）；双盲 "heavy"、arXiv 建议、desk reject 条款来自 FSE 2026 的 *How to Submit* 总页面，该页面明确说明"各 track 格式不同，请读各自 CFP"，因此**research track 的页数与 rebuttal 细节未核实**。
- **ICSE 2026 的 CFP 原文我未读到**；本文的 ICSE 流程细节（双周期、Revision、4 周、10+2 页、五个评审维度）全部来自 **ICSE 2025** 的 CFP 全文。ICSE 2026 可能已调整。
- **"ICSE 的 Journal-First / NIER / SEIP 的具体录用率"未查到官方数字**，只有"这些通道存在"这一事实。
- **ISSTA 的录用率数据来自 OpenAccept（第三方聚合站）**，**未与 ISSTA 官方公告逐条核对**；且 OpenAccept 的"主研究 track"口径是否包含 journal-first / 特殊 track 未核实。**ISSTA 2026 的投稿数与录用率截至检索时未公布**（ISSTA 2026 于 2026 年举行），本文只给到 2025 年。
- **NeurIPS E&D 的 Croissant RAI 字段具体清单**未核实（只读到"2026 年起同时要求 core 与 RAI 字段"）。
- **NeurIPS 2025 E&D 调查的 851/155 样本代表性未知**（官方未给回应率），因此 58% / 82% / 69% 等百分比只能作为"作者与审稿人主观感受"，不能当作客观质量指标。
- 本文不涉及中国大陆政治、机构制裁、出口管制等议题；检索中出现的相关页面已主动排除。

## 来源

1. NeurIPS (2026). *Call For Evaluations & Datasets 2026*（scope、双盲默认、code policy、Croissant、key dates、camera-ready）。https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets
2. NeurIPS (2026). *Evaluations and Datasets 2026 Reviewing Guidelines*（逐日时间线、四维标准、Originality 宽松界定、LLM 严格禁令、desk reject 情形）。https://neurips.cc/Conferences/2026/EvaluationsDatasetsReviewerGuidelines
3. NeurIPS (2026). *Call For Papers 2026*（track 不可互投、key dates）。https://neurips.cc/Conferences/2026/CallForPapers
4. NeurIPS Communications Chairs (2025-09-30). *Reflections on the 2025 Review Process*（21,575 / 5,290 / 24.52% / 20,518 reviewers / 1,663 ACs / 199 SACs）。https://blog.neurips.cc/2025/09/30/reflections-on-the-2025-review-process-from-the-program-committee-chairs/
5. NeurIPS Communications Chairs (2025-12-05). *NeurIPS Datasets & Benchmarks Track: From Art to Science in AI Evaluations*（1,820→1,995 投稿、41 SAC / 281 AC / 2,680 reviewers、851 作者 + 155 审稿人调查）。https://blog.neurips.cc/2025/12/05/neurips-datasets-benchmarks-track-from-art-to-science-in-ai-evaluations/
6. 会议之眼 (2024). *NeurIPS 2024 录取通知：又一独家数据*（D&B track 1,820 篇 / 25.3%）。https://www.conferenceeye.cn/article/c3db836af52b4ad893f5dd73ee89cbe4
7. ICSE 2026 Research Track HotCRP 官方公告（Cycle 1: 660/161/24.4%；Cycle 2: 809/160/19.8%；总 1,469/321）。https://icse2026.hotcrp.com/
8. ICSE 2025 Research Track Call for Papers（双周期日期、10+2 页、双盲、Revision + Author Response、五个评审标准、open science 政策、desk reject 三类）。https://www.conferences-computer.science/icse/2025/cfp/ICSE-2025.txt
9. OpenAccept. *ICSE Acceptance Rates and Submission Statistics*（2013–2025 逐年投稿/录用/录用率）。https://openaccept.org/c/sw/icse/
10. OpenAccept. *ASE Acceptance Rates and Submission Statistics*（2013–2025 逐年数据）。https://openaccept.org/c/sw/ase/
11. Li, Y. (2025-09-26). *Papers accepted by ASE 2025*（1,190 投稿 / 1,136 过 desk reject / 113 直接 + 132 大修 = 245 / 21.6%）。https://liyiweb.com/posts/paper-accepted-by-ase-2025/
12. FSE 2026. *How to Submit*（全部 track 列表、heavy double-anonymous、arXiv 建议、desk reject 条款、ACM 模板、Montreal 2026-06-05~09）。https://conf.researchr.org/track/fse-2026/fse-2026-how-to-submit
13. 博客园 inertial-fish (2026-03-04). 《ASE 2026 投稿相关》（早期拒绝阶段、强制数据可用性声明、10 页 + 2 页、ACM 模板）。https://www.cnblogs.com/sinclaire/p/19669421
14. ASE 2026 Tools and Datasets track 截稿（2026-07-22）。https://ase26-tools-datasets.hotcrp.com/deadlines
15. NeurIPS (2026). *Main Track Handbook 2026*（9 页 / 50MB / 双投含主 track 与 E&D 互投即 desk reject）。https://neurips.cc/Conferences/2026/MainTrackHandbook
16. OpenAccept. *ISSTA Acceptance Rates and Submission Statistics*（2020–2025 逐年投稿/录用/录用率；2025 = 550/107/19.45%，2024 = 694/143/20.61%，2023 = 406/117/28.82%）。https://openaccept.org/c/sw/issta/
