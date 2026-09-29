# 方向 05：NeurIPS Datasets & Benchmarks / Evaluations & Datasets 审稿标准详解（从 OpenReview 看真实分数分布）

## 核心结论

1. **NeurIPS 2024 → 2025 发生了量表代际更替**：2024 年 Overall 是 **1–10 分制**（10=Award quality，1=Very Strong Reject），并配有 Soundness / Presentation / Contribution 三项 **1–4 分制**子分；2025 年 Overall 改为 **1–6 分制**（6=Strong Accept，1=Strong Reject），子分改为 Quality / Clarity / Significance / Originality 四项 **1–4 分制**，同时新增 Limitations 与 Responsible Reviewing 确认项。**这是所有"NeurIPS 分数解读"教程大面积过期的根因。**
2. **D&B track 的分数分布比主赛道更"高且窄"**：2025 年 D&B 录用论文篇均分 **4.65**（6 分制）、拒稿 **4.13**，单条评审分有 **938 条落在 4 分、1,216 条落在 5 分**，而 6 分全 track 只出现 **100 次**；官方明确解释这是"数据集论文很少'技术性错误'+ 贡献主观性高"导致，并因此**引入"篇均分 4.25"作为 SAC 强制补充定性理由的阈值**。
3. **分数不是决定性的**：2025 年 PC chairs 官方承认存在"高分被拒"（AC 在 rebuttal 后发现审稿人未发现的重大问题）与"低分被收"（AC 力挺）两类情形；我们复算的 2024 年 D&B 数据里，**录用论文最低篇均 3.5（10 分制）而拒稿论文最高篇均 7.00**，两者区间重叠。

---

## 精确数字与案例

### 一、2024 年审稿表单（11 个问题）与量表原文

NeurIPS 2024 Reviewer Guidelines 原文列出的表单字段：

| 序号 | 字段 | 类型 |
|---|---|---|
| 01 | Summary | 文本 |
| 02 | Strengths and Weaknesses（须覆盖 Originality / Quality / Clarity / Significance 四维） | 文本 |
| 03 | Questions | 文本 |
| 04 | Limitations | 文本 |
| 05 | Ethical concerns | 标记 |
| 06 | **Soundness** | **1–4** |
| 07 | **Presentation** | **1–4** |
| 08 | **Contribution** | **1–4** |
| 09 | **Overall** | **1–10** |
| 10 | **Confidence** | **1–5** |
| 11 | Code of conduct acknowledgement | 勾选 |

**2024 年 Overall 1–10 量表的完整原文定义**（逐字摘录）：

- **10 Award quality**：Technically flawless paper with groundbreaking impact on one or more areas of AI, with exceptionally strong evaluation, reproducibility, and resources, and no unaddressed ethical considerations.
- **9 Very Strong Accept**：Technically flawless paper with groundbreaking impact on at least one area of AI and excellent impact on multiple areas of AI, with flawless evaluation, resources, and reproducibility, and no unaddressed ethical considerations.
- **8 Strong Accept**：Technically strong paper with novel ideas, excellent impact on at least one area of AI or high-to-excellent impact on multiple areas of AI, with excellent evaluation, resources, and reproducibility, and no unaddressed ethical considerations.
- **7 Accept**：Technically solid paper, with high impact on at least one sub-area of AI or moderate-to-high impact on more than one area of AI, with good-to-excellent evaluation, resources, reproducibility, and no unaddressed ethical considerations.
- **6 Weak Accept**：Technically solid, moderate-to-high impact paper, with no major concerns with respect to evaluation, resources, reproducibility, ethical considerations.
- **5 Borderline accept**：Technically solid paper where reasons to accept outweigh reasons to reject, e.g., limited evaluation. **Please use sparingly.**
- **4 Borderline reject**：Technically solid paper where reasons to reject, e.g., limited evaluation, outweigh reasons to accept, e.g., good evaluation. **Please use sparingly.**
- **3 Reject** / **2 Strong Reject** / **1 Very Strong Reject**：依次为"技术缺陷 + 弱评测 + 复现不足 + 伦理未处理" → "重大技术缺陷 / 差评测 / 低影响 / 差复现 / 伦理基本未处理" → "trivial results or unaddressed ethical considerations"。

**Confidence 1–5**（2024/2025 两年一致）：5 = "absolutely certain … checked the math/other details carefully"；1 = "Your assessment is an educated guess. The submission is not in your area or the submission was difficult to understand."

### 二、2025 年审稿表单（13 个问题）与量表原文

NeurIPS 2025 Reviewer Guidelines 原文列出的字段（**新增了 Limitations 与 Responsible reviewing acknowledgement，并把四维度直接做成打分项**）：

| 序号 | 字段 | 类型 |
|---|---|---|
| 01 | Summary | 文本 |
| 02 | Strengths and Weaknesses（须覆盖 Quality / Clarity / Significance / Originality） | 文本 |
| 03 | **Quality** | **1–4**（4 excellent / 3 good / 2 fair / 1 poor） |
| 04 | **Clarity** | **1–4** |
| 05 | **Significance** | **1–4** |
| 06 | **Originality** | **1–4** |
| 07 | Questions（原文建议 "ideally around 3–5"） | 文本 |
| 08 | Limitations | 文本 |
| 09 | **Overall** | **1–6** |
| 10 | **Confidence** | **1–5** |
| 11 | Ethical concerns | 标记 |
| 12 | Code of conduct acknowledgement | 勾选 |
| 13 | Responsible reviewing acknowledgement | 勾选 |

**2025 年 Overall 1–6 量表的完整原文定义**（逐字摘录）：

- **6 Strong Accept**：Technically flawless paper with groundbreaking impact on one or more areas of AI, with exceptionally strong evaluation, reproducibility, and resources, and no unaddressed ethical considerations.
- **5 Accept**：Technically solid paper, with high impact on at least one sub-area of AI or moderate-to-high impact on more than one area of AI, with good-to-excellent evaluation, resources, reproducibility, and no unaddressed ethical considerations.
- **4 Borderline accept**：Technically solid paper where reasons to accept outweigh reasons to reject, e.g., limited evaluation. **Please use sparingly.**
- **3 Borderline reject**：Technically solid paper where reasons to reject, e.g., limited evaluation, outweigh reasons to accept, e.g., good evaluation. **Please use sparingly.**
- **2 Reject**：For instance, a paper with technical flaws, weak evaluation, inadequate reproducibility and incompletely addressed ethical considerations.
- **1 Strong Reject**：For instance, a paper with well-known results or unaddressed ethical considerations.

**2025 年 Questions 字段的一条重要指令**（对阙疑写 rebuttal 有用，原文）："You are strongly encouraged to **state the clear criteria under which your evaluation score could increase or decrease**. This can be very important for a productive rebuttal and discussion phase."

**2025 年 Limitations 字段的评分导向**（原文）："In general, **authors should be rewarded rather than punished for being up front about the limitations** of their work and any potential negative societal impact."

**⚠️ 关键提醒**：2025 年 1–6 分制**没有 "Weak Accept" 这一档**（2024 年的 6 分 Weak Accept 在 1–6 制下已不存在）；2024 年"7 分 = Accept"，2025 年"5 分 = Accept"。**任何把 2024 年的 6/7 分阈值直接套到 2025/2026 的做法都是错的。**

### 三、真实分数分布（我们从 OpenReview 镜像数据复算）

数据源：Paper Copilot 的 `nips/nips2024.json`（31.75 MB）与 `nips/nips2025.json`（38.04 MB），字段 `rating` 为分号分隔的每位审稿人原始分。**这是目前可公开获取的、最接近 OpenReview 全量的分数数据。**

**2024 年 D&B（1–10 制）**

| 分组 | n | 篇均分的平均 | 中位数 | 最小 | 最大 | 平均 confidence | 平均审稿人数 |
|---|---|---|---|---|---|---|---|
| 全部录用 | 459 | **6.75** | 6.67 | 5.67 | 9.33 | 3.77 | 3.64 |
| Poster | 392 | 6.64 | 6.67 | 5.67 | 8.00 | 3.76 | 3.64 |
| Spotlight | 56 | **7.38** | 7.50 | 6.00 | 8.33 | 3.83 | 3.66 |
| Oral | 11 | **7.62** | 7.67 | 6.00 | 9.33 | 3.91 | 3.64 |
| Reject | 67 | **5.66** | 5.75 | 3.33 | 7.00 | 3.71 | 3.67 |

单条评审分直方图：2→3、3→28、4→78、5→179、**6→555、7→675**、8→290、9→101、10→9。

**2025 年 D&B（1–6 制）**

| 分组 | n | 篇均分的平均 | 中位数 | 最小 | 最大 | 平均 confidence | 平均审稿人数 |
|---|---|---|---|---|---|---|---|
| 全部录用 | 497 | **4.65** | 4.60 | 3.50 | 5.75 | 3.60 | 3.93 |
| Poster | 434 | 4.60 | 4.50 | 3.50 | 5.33 | 3.58 | 3.93 |
| Spotlight | 56 | **5.00** | 5.00 | 4.33 | 5.75 | 3.66 | 3.88 |
| Oral | 7 | **5.00** | 5.00 | 4.75 | 5.25 | 4.08 | 4.14 |
| Reject | 94 | **4.13** | 4.25 | 2.67 | 5.00 | 3.54 | 3.99 |

单条评审分直方图：2→15、3→59、**4→938、5→1,216**、6→100。

**篇均分桶（0.5 粒度，全部 591 条）**：2.5→2、3.0→3、3.5→4、4.0→102、**4.5→265、5.0→209**、5.5→5、6.0→1。

**三条可直接引用的结论**：

1. **量表代际差异**：2024 年"录用门槛"大约在篇均 6.0（10 分制，即 60%），2025 年在篇均 4.0（6 分制，即 67%）。
2. **6 分极稀缺**：2025 年全 track（591 条 opt-in 样本）**只有 100 条单条评审给了 6 分**，而 7 篇 Oral 的篇均也只有 5.00——**在该 track，"5 分"就已经是 oral 级**。
3. **录用/拒稿区间重叠**：2024 年录用最低篇均 5.67、拒稿最高 7.00；2025 年录用最低 3.50、拒稿最高 5.00。**分数不能单独决定结果。**

### 四、D&B track 的官方"分数不够用"诊断与对策

D&B chairs 在 2025-09-30 官方复盘中给出了**该 track 分数分布异于主赛道的两条机制解释**（原文）：

> "1. **Increased average score:** Unlike papers in the main track, which one can expect to be more method and algorithm oriented, it is less common for a dataset submission to be fundamentally 'technically incorrect.' 2. **Subjective nature of contributions:** Evaluating the merit of a dataset or benchmark can be highly subjective. A dataset that fills a critical gap for a smaller, long-tail research area might be just as valuable or novel as one that targets a well-established 'head' problem. … We think that these factors can lead to reviewer scores that **skew higher and have a tighter distribution** compared to the papers in the main track. As a result, it can be difficult for the ACs to differentiate clearly between two papers that may have the same average score but vastly different merits and trade-offs."

**官方对策（对阙疑的设计有直接借鉴价值，原文）**：

> "we asked our SACs, based on their discussion with the ACs, to produce **a relative ranking of the papers within their stack of papers**. … **For any paper ranked below the track-wide average score of 4.25, SACs were required to provide a detailed description of its merits and motivation.** … This combination of relative ranking and qualitative justification provided a much richer signal."

**注意 4.25 这个数**：它恰好落在我们复算的 2025 年"4.0–4.5"分桶的密集区（4.0→102 篇、4.5→265 篇），验证了官方诊断。

### 五、2026 年 E&D 的评审标准（8 类贡献 × 4 维度 × 强制检查项）

2026 年 Reviewing Guidelines（2026-06-25 更新）**没有给出数值量表**（量表沿用主赛道的 1–6），而是给出了**按贡献类型细分的评审标准**。四个核心维度原文：

- **Quality**："Is the submission technically sound, and are the claims well-supported by empirical, analytical, or conceptual arguments? Is this a complete piece of work or work in progress? Are the authors careful and honest about evaluating both the strengths and weaknesses of their work?"
- **Clarity**："Is the submission clearly written, well-organized, and detailed enough to enable reproducibility?"
- **Significance**："Are the results impactful for the community? Does it advance our understanding of AI evaluation, provide unique data, or address a difficult task better than prior work? Are others (researchers or practitioners) likely to use the ideas or build on them?"
- **Originality**："Does the work provide new insights, deepen understanding, or highlight important properties of existing methods? **Originality does not necessarily require introducing an entirely new method.** Providing novel insights, exposing failure modes, evaluating existing methods, or framing new metrics is equally valuable."

**8 类贡献及其"强制检查项"**（对阙疑最相关的三类加粗）：

| 类别 | 强制检查项 |
|---|---|
| Benchmark Design and Benchmark Analysis | 双盲（或经论证单盲）；鼓励提供可复现代码；无代码须评估 code justification 字段 |
| Evaluation Methodology and Metrics | 双盲；鼓励提供指标实现代码 |
| **Evaluation Tools, Frameworks, and Infrastructure** | **代码强制**（"无代码 = 拒稿，除非提供有说服力的理由"）；Code URL 须可访问、可执行、已匿名化 |
| **Reproducibility, Auditing, and Stress-Testing of Evaluations** | 双盲；鼓励提供复现/审计代码；负结果须"deep and carefully controlled" |
| Human-Centered and Interaction-Based Evaluation | **须提供 IRB 认证或等效机构文件**；须确认参与者获公平报酬 |
| **Datasets and Data Resources** | **有效的 Croissant 文件**；**RAI 元数据完整**；**无需向 PI 请求即可访问**；论文须为双盲或经论证单盲；检查自动化审稿报告 |
| Dataset Documentation, Auditing, and Responsible Data | 双盲；自动化审计须提供代码/工具 |
| Data-Centric Methods and Empirical Analyses | 双盲；鼓励提供实验代码 |

**评审人禁止条款（原文）**："**reviewers may not use any LLMs or AI agents in the review process**."；"被识别为低质量的评审可能被进一步调查是否存在不当 LLM 使用"。

### 六、分数的"可推翻性"：官方承认的两类反常

2025 年 PC chairs 博客原文（前文已引）：

> "Many ACs fought for papers they thought were good even if reviewers disagreed, and often we followed their lead, ending in an **accept** decision for the paper. Conversely, sometimes ACs flagged significant negative issues with evidence after the rebuttal that reviewers did not catch … This then led to **reject decisions even when papers had high ratings**."

同年 PC chairs 还披露了一条**对"审稿疲劳"的量化观察**（原文）：

> "one new source of noise we observed this year was **reviewers increasing their scores just to end back-and-forth discussion with the authors**, but being silent or critical in private discussions with the AC, which leads us to believe that increasing levels of author engagement in rebutting their papers is now **leading to reviewer fatigue**."

以及**责任评审条款的硬后果**（原文）："we note in some cases decisions had to be reverted … This included situations like the **11 unfortunate cases** where one of the co-authors are confirmed to be grossly negligent in their reviews under our new responsible reviewing policies."

### 七、Rebuttal 对分数的真实影响（跨会议实证）

NeurIPS 未公开 rebuttal 前后分数的成对数据，但 ICLR 有（ICLR 与 NeurIPS 同为 OpenReview 体系、同为 1–6 制后的同构流程）。论文 **"Insights from the ICLR Peer Review and Rebuttal Process"**（Kargaran, Nikeghbal, Yang, Ousidhoum，arXiv:2511.15462，2025-11-20，含 LMU Munich / TUM / USC / Paper Copilot / Cardiff University）基于 ICLR 2024+2025 全量数据给出以下**具体数字**：

- "**Rebuttals primarily affect borderline papers**, with score changes concentrated in the mid-range (**5–6**), where even small shifts can change outcomes."
- "**approximately 20% of accepted submissions likely benefiting from rebuttal-driven score increases**."
- "**Reviewer disagreements decrease by roughly 9–10% after rebuttals**, with the strongest convergence observed for high-quality papers (oral/spotlight) and minimal effect for low-scoring or rejected papers."
- "in both years, **over 40% of papers in the top 5% before rebuttal are replaced after score updates**."
- "nearly **20% of papers lost their position in the top 30%** after rebuttal."
- "**rejected and withdrawn submissions show only small reductions (generally below 7%)**."
- "most reviews (**71% of cases**) reflect changes only in the overall score and do not update other aspects, such as soundness."
- "Rebuttals submitted **in the middle of the rebuttal period may be the most effective**, while very early or last-minute rebuttals have less impact."
- "**Reviewers 4, 3, 2, and 1, in order, tend to show increasing generosity**, which means that the reviewer who submits last (Reviewer 1) tends to submit higher scores."
- 该文的 **Table 6** 给出 ICLR 2025 全量分数变动：**Decrease 640 条、Increase 10,728 条、Keep 33,913 条**（按 overall rating 统计）。

**换算**：Increase 10,728 / (640+10,728+33,913) = **23.7%** 的评审在 rebuttal 后提分，Keep 占 **75.0%**，Decrease 只占 **1.4%**。**"提分"比"降分"常见约 17 倍。**

### 八、Desk reject：2026 年的自动化实践

NeurIPS 2026 Position Paper Track 用 **Pangram** 工具 desk-reject 了 **178 篇**（占该 track **18.4%**）（AI Weekly，2026-06-04，二手转述）。这说明 NeurIPS 已在用**机器判决**做初筛。阙疑的差异化不在"用机器判决"（这件事已经发生），而在**判决可被第三方独立复算**。

### 九、2024 → 2025 表单变化的逐条对照与影响分析

把两年的表单并排放，可以精确看到"NeurIPS 认为什么变得更重要了"：

| 维度 | 2024 | 2025 | 变化含义 |
|---|---|---|---|
| 子分维度名 | Soundness / Presentation / Contribution | **Quality / Clarity / Significance / Originality** | 从"技术可靠性 + 表达 + 贡献"改为与文本 Strengths/Weaknesses 的四维度**完全对齐** |
| 子分数量 | 3 个 | **4 个** | 多了一个独立维度 |
| Overall 量表 | **1–10** | **1–6** | 档位从 10 档压到 6 档 |
| Overall 的 "Accept" 档 | 7 分 | 5 分 | **档位位置从 70% 移到 83%** |
| "Weak Accept" | 存在（6 分） | **不存在** | 中间档位被删除 |
| Limitations 的位置 | 独立字段（第 4 题） | 独立字段（第 8 题）+ 明确"奖励诚实" | 位置后移但导向更明确 |
| Questions 的指令 | "list up and carefully describe any questions" | **"ideally around 3–5"** + "state the clear criteria under which your evaluation score could increase or decrease" | 从开放式改为**结构化 + 可反驳** |
| Responsible reviewing 确认 | 无 | **有（第 13 题）** | 与"责任评审倡议"配套 |
| 伦理标记 | 有 | 有 | 不变 |

**三条可推断的影响**：

**影响一：1–6 制把"中间地带"压缩了。** 2024 年的 1–10 制里有 5（Borderline accept）和 4（Borderline reject）两档，且 6（Weak Accept）与 7（Accept）明确分开；2025 年的 1–6 制里 4（Borderline accept）与 3（Borderline reject）**就是**中间地带，没有更细的过渡。我们复算的数据印证了这一点：2025 年 D&B 的 591 条里，**篇均分落在 4.0 与 4.5 两个桶的合计 367 条，占 62.1%**——**超过六成的论文挤在两个相邻桶里**。

**影响二："3–5 个问题 + 明确的升降分标准"改变了 rebuttal 的博弈结构。** 审稿人被要求写出"什么条件下我会改分"，这理论上让 rebuttal 变成**可定向攻击**的。但 2025 年 PC chairs 同时观察到相反现象："reviewers increasing their scores **just to end back-and-forth discussion** with the authors, but being silent or critical in private discussions with the AC"——**即审稿人可能"表面提分、私下否定"**。这意味着作者**不能只看公开分数的变化来判断成败**。

**影响三：子分维度改名意味着"Presentation"不再单独打分。** 2024 年有独立的 Presentation 分；2025 年 Clarity 覆盖了它，但**评审指引明确把"可复现性"塞进了 Clarity**："Is the submission clearly written, well-organized, and **detailed enough to enable reproducibility**?"（2026 年 E&D 的 Clarity 定义原文）。**这条对阙疑是直接约束**：论文的"可复现细节"不再只影响"表达分"，而是直接影响四个核心维度之一的 Clarity 分。

### 十、分数与结果的四种组合（含官方承认的反常）

把"分数"与"结果"做成 2×2，NeurIPS 官方文本与我们的数据可以填满四个格子：

| | 被录用 | 被拒 |
|---|---|---|
| **高分** | 主流情形（2024 D&B 录用篇均 6.75；2025 篇均 4.65） | **官方承认存在**："reject decisions even when papers had high ratings"（AC 在 rebuttal 后发现审稿人漏掉的重大问题）。2024 年 D&B 拒稿最高篇均 **7.00** |
| **低分** | **官方承认存在**："Many ACs fought for papers they thought were good even if reviewers disagreed … ending in an accept decision"。2024 年 D&B 录用最低篇均 **3.50** | 主流情形（2024 D&B 拒稿篇均 5.66；2025 篇均 4.13） |

**这张表的价值在于：它证明"分数—结果"不是确定性映射，而是"分数 + AC/SAC 相对排序 + 定性理由"的三元函数。** 这正是 D&B chairs 在 2025 年引入"**相对排名 + 4.25 阈值强制定性理由**"的制度动机。

**对阙疑的推论**：一个"四态判决（含 unknown）"的系统，其评价方式也应当是**三元的**——不能只用"检出率"一个数字，而应当同时报告（a）每态的数量分布，（b）每条判决的证据引用是否可复算，（c）无法判决（unknown）的原因分类。**阙疑的 `unknown` 态恰好对应 NeurIPS 的 "borderline" 地带**，而 NeurIPS 对这个地带的处理方式是"**强制要求定性理由**"——这为阙疑要求"每条 unknown 必须带机器可读的 reason_code"提供了直接的外部依据。

### 十一、给"单人作者"的审稿现实（从数据反推）

从 2025 年 D&B 的数据可以反推三条对单人作者不利/有利的机制：

**不利机制一：审稿人数上升但 confidence 下降。** 平均审稿人数 3.64→3.93，平均 confidence 3.77→3.60。**审稿人更多，但每个人更不确定**——这意味着"分歧"的概率上升，而分歧意味着**更需要 AC 校准**，也就意味着**AC 的主观判断权重上升**。

**不利机制二：11% 的审稿人根本没打开数据集。** 官方原文："Eleven percent did not directly inspect datasets and instead based their evaluations solely on the accompanying papers." **如果审稿人只看论文不看产物，那么"产物可验收"这个卖点在评审阶段几乎不被看到。** 这解释了为什么 2025 年要上"自动化元数据报告"（69% 审稿人认为有用）——**必须把"可验收性"做成审稿人不用打开产物也能看到的信号（checklist、自动报告）**。

**有利机制一：该 track 明确"不要求击败 baseline"。** 2026 年 E&D 的 CFP 原文："**Submissions need not introduce a new model or outperform prior work.** … A submission need not 'beat a baseline'; its primary contribution should be to deepen and refine our understanding of evaluation practices." 且 Originality 的定义明确"**Beating a baseline is not required**"（Benchmark Design 类原文）。**这条对"单人无算力、无法做大规模对比实验"的作者是决定性的利好。**

**有利机制二：负结果被明确欢迎。** CFP 原文："**Negative results, critical analyses, and use-case-inspired evaluations are welcome.**" 且 2026 Reviewing Guidelines 对 Reproducibility/Auditing 类的 Quality 项明确问："If a negative result: **is it deep and carefully controlled?**" **阙疑主动放弃把变异率 97.3% 当作缺陷检测率，并把三个测量陷阱（标签效度 / 检测器可用性 / 编译档）量化为可复算数字——这正是"deep and carefully controlled negative result"的标准形态。**

---

## 对阙疑的 3 条具体行动

1. **把"分数不是判决"写进论文的 Evaluation 设计**：在 `research/08_metrics.md` 加一节 `Why rates alone are insufficient`，引用三组数字——(a) 2024 D&B 录用最低篇均 **5.67** vs 拒稿最高 **7.00**（区间重叠）；(b) 2025 D&B chairs 官方承认"分数高且窄，AC 难以区分"并引入 **4.25** 阈值强制定性理由；(c) PC chairs 官方承认存在"高分被拒 / 低分被收"。**结论句**：既然连 NeurIPS 都承认纯数值分不足以支撑判决，阙疑的"四态判决 + 证据带 provenance"就不是过度设计。时间点：2026-12 前。
2. **按 2026 E&D 的"类 3 / 类 4 / 类 6"三类的强制检查项做一次逐项自检**：新建 `research/03c_review_readiness.md`，逐条勾选：
   - 类 3（Tools/Frameworks/Infrastructure）：**Code URL 可访问 + 可执行 + 已匿名化** → 用干净容器实测 `python tools/gate_engine.py --check`，把退出码与输出存成 `data/review_readiness/engine_smoke.json`；
   - 类 4（Auditing/Stress-Testing）：**负结果须"deep and carefully controlled"** → 阙疑已主动放弃把变异率 97.3% 当缺陷检测率，这正是"carefully controlled negative result"，应把它从"缺陷"改写为"贡献"（论文 v0.3 已放弃该口径，需在正文显式表述为"我们报告了一个负结果"）；
   - 类 6（Datasets）：**有效 Croissant 文件 + RAI 元数据完整 + 无需向 PI 请求即可访问** → 为 holdout 30 / corpus 40 / 缺陷夹具 15 三个数据集各生成一份 Croissant 文件（可先用官方校验器 `https://huggingface.co/spaces/JoaquinVanschoren/croissant-checker` 与 RAI 编辑器 `https://huggingface.co/spaces/JoaquinVanschoren/croissant-rai-checker` 验证）。时间点：2027-03 前完成（投稿前 2 个月）。
3. **把 rebuttal 策略前置到投稿前**：依据 ICLR 实证（**23.7% 的评审会提分、75.0% 不动、1.4% 降分；提分/降分 ≈ 17:1；中期提交的 rebuttal 最有效**），在 `research/` 下新建 `14_rebuttal_plan.md`，预先写好三类回复模板：(a) 对"评测规模小"（30 holdout / 40 corpus）的回应——直接给出分母定义与 Clopper-Pearson 区间；(b) 对"baseline 不足"的回应——把"独立对账器"本身作为 baseline（不依赖内核的第三方复算）；(c) 对"单作者"的回应——只谈可复现产物，不谈机构。**并且**在投稿前就准备好"code justification 字段"的文本（因为 2026 E&D 的类 3 是"无代码 = 拒稿"，阙疑有代码，但必须解释为何这是**可执行产物**而非 demo）。时间点：2027-06（若投 2027 届，rebuttal 期在 7 月）。

---

## 盲区（诚实标注）

- **本文件的所有分数分布均基于 Paper Copilot 的 opt-in 公开样本**（2024 D&B 有 rating 的 526 条、2025 D&B 591 条），**不是 OpenReview 全量**。2025 年只有 591 条进入样本，而官方投稿是 1,995 篇，**覆盖率约 29.6%**。
- **OpenReview 的 2024/2025/2026 会场页在本机被 Cloudflare Turnstile 拦截**（`api2.openreview.net` 返回 `ChallengeRequiredError`），因此**未能直接核验**表单字段、分项分（`quality` / `clarity` / `significance` / `originality` 字段在 2025 数据中**全部为 null**，即分项分未公开）与每篇的 decision。
- **2024 年表单的 11 个问题与 2025 年表单的 13 个问题**：来源于官方 Reviewer Guidelines 页面的文本提取，**未与 OpenReview 实际渲染的表单逐字段比对**。2025 年表单的 "Quality/Clarity/Significance/Originality 各 1–4" 在原文中只列了文字标签（excellent/good/fair/poor），**数字编号是我们按列表顺序对应**。
- **2026 E&D 的数值量表未在 E&D 专属文档中给出**；我们的结论"沿用主赛道 1–6"是基于 CFP 原文"will follow the Call for Papers of the NeurIPS 2026 Main Track"的**推断**，**未在 2026 主赛道 Reviewer Guidelines 中逐字核对**。
- **ICLR rebuttal 论文的数据是 ICLR 而非 NeurIPS**。两者同为 OpenReview、同为 1–6 制后的同构流程，但**审稿人池、AC 校准机制、track 结构均不同**，跨会议外推需谨慎。该论文的部分数字（如 "23.7% / 75.0% / 1.4%"）是**本文件从 Table 6 的绝对数自行换算**，非原文百分比。
- **"Reviewer 1 倾向于给更高分"** 是 ICLR 论文的结论，**未在 NeurIPS 数据上验证**。
- **Position Paper Track 的 "178 篇 / 18.4%"** 来自 AI Weekly 二手转述（2026-06-04），**未找到 NeurIPS 官方一手声明**，标为待核实。
- **NeurIPS 2026 E&D 的实际分数分布尚不存在**（作者通知 2026-09-24，评审分公开通常需等到会议前后）。**需在 2026-11 之后重新调研。**
- 2025 年 D&B 的 **`corr_rating_confidence`（分数-置信度相关系数）** 字段在数据中存在（例如某篇为 0.816），但我们**未做全量统计**，因此"置信度是否影响分数"在本文件中**无结论**。

---

## 来源

1. 2024 Reviewer Guidelines — NeurIPS — https://neurips.cc/Conferences/2024/ReviewerGuidelines — 11 个表单问题；Soundness/Presentation/Contribution 各 1–4；Overall 1–10（含 10 档完整定义）；Confidence 1–5 — NeurIPS，2024
2. 2025 Reviewer Guidelines — NeurIPS — https://neurips.cc/Conferences/2025/ReviewerGuidelines — 13 个表单问题；Quality/Clarity/Significance/Originality 各 1–4；Overall 1–6（含 6 档完整定义）；Confidence 1–5；"state the clear criteria under which your evaluation score could increase or decrease" — NeurIPS，2025
3. NeurIPS Evaluations & Datasets 2026 Reviewing Guidelines — https://neurips.cc/Conferences/2026/EvaluationsDatasetsReviewerGuidelines — 四维度定义；8 类贡献的强制检查项；"reviewers may not use any LLMs or AI agents in the review process" — NeurIPS，2026-06-25
4. Reflecting on the 2025 Review Process from the Datasets and Benchmarks Chairs — https://blog.neurips.cc/2025/09/30/reflecting-on-the-2025-review-process-from-the-datasets-and-benchmarks-chairs/ — "skew higher and have a tighter distribution" / "track-wide average score of 4.25" / relative ranking 机制 — NeurIPS Blog，2025-09-30
5. Reflections on the 2025 Review Process from the Program Committee Chairs — https://blog.neurips.cc/2025/09/30/reflections-on-the-2025-review-process-from-the-program-committee-chairs/ — "reject decisions even when papers had high ratings" / "reviewers increasing their scores just to end back-and-forth discussion" / "11 unfortunate cases" — NeurIPS Blog，2025-09-30
6. Paper Copilot 原始数据（分数分布复算来源）— https://github.com/papercopilot/paperlists — `nips/nips2024.json`（31,753,965 字节，D&B 547 条，526 条有 rating）、`nips/nips2025.json`（38,038,097 字节，D&B 591 条）— Paper Copilot，2026 访问
7. Paper Copilot，NeurIPS 2024 / 2025 D&B 统计行 — https://legacy.papercopilot.com/paper-list/neurips-paper-list/neurips-2025-accepted-paper-list-datasets-benchmarks-track/ — 2024: min 3.30 / max 9.30 / avg 6.58；2025: min 2.60 / max 5.70 / avg 4.55；并含 "opt-in" 免责说明 — Paper Copilot，2026 访问
8. Insights from the ICLR Peer Review and Rebuttal Process — Amir Hossein Kargaran, Nafiseh Nikeghbal, Jing Yang, Nedjma Ousidhoum — arXiv:2511.15462 — LMU Munich / TUM / Munich Center for Machine Learning / USC / Paper Copilot / Cardiff University — 2025-11-20 — "approximately 20% of accepted submissions likely benefiting from rebuttal-driven score increases" / "decrease by roughly 9–10%" / "over 40% of papers in the top 5%" / Table 6 分数变动绝对数
9. NeurIPS 2025 Datasets & Benchmarks Track Call for Papers — https://neurips.cc/Conferences/2025/CallForDatasetsBenchmarks — "reviewed according to a set of criteria and best practices specifically designed for datasets and benchmarks"；single-blind 可选；强制 Croissant — NeurIPS，2025
10. NeurIPS 2026 Evaluations & Datasets Track Call for Papers — https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets — 默认双盲；contribution-dependent code policy；"无代码 = 拒稿"（类 3）；>4GB 样本要求 — NeurIPS，2026
11. NeurIPS Rejects 18.4% of Position Papers via Pangram AI Tool — https://aiweekly.co/alerts/neurips-rejects-184-of-position-papers-via-pangram-ai-tool — 178 篇 desk-reject（二手转述，待核实）— AI Weekly，2026-06-04
12. NeurIPS review scores: what the numbers actually mean — https://phdflow.ai/guides/neurips-review-scores-explained — "The overall score is 1 to 6, not 1 to 10: it changed in 2025 and most guides still have the old scale." — PhD Flow，2026-08-11
