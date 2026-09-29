# 方向 11：rebuttal 怎么写才不像 AI

> 调研时间：2026-09-29。目标：为「阙疑」项目 NeurIPS 2027 E&D 投稿的 **rebuttal 阶段** 提供可执行依据，并回答一个更尖锐的问题——在 Pangram 3.3.2 已经把 178 篇投稿直接 desk reject 的环境下，一份大量借助 LLM 完成的 rebuttal 如何既不触发检测、又真的有效。

---

## 核心结论

1. **rebuttal 的"分数杠杆"比想象中小得多，但"提升组"的录用率是"不变组"的 4–7 倍。** ICLR 2025 评审层面仅 **23%** 的评分在 rebuttal 后上升、75% 不变、1% 下降（2024 为 17%/81%/1%）；但论文层面，**分数上升的稿子录用率 55.7%（2025）/57.6%（2024）**，不变组只有 7.8%/12.4%，下降组 8.0%/6.4%。更严格的因果口径（Dershowitz & Verma, CACM 2023）下，ACL 2018 里只有 **24 份 rebuttal 真正"有效"，占 1.6%**，真正靠 rebuttal 逆袭录用的 **不到 1%**；CHI 2020/2021 为 **3.7% / 3.6%**。结论：**rebuttal 的价值不在于"翻盘"，而在于把已经在 borderline 的稿子推过线，并避免自己把它推下去。**
2. **唯一被回归系数确认"有效"的句式是"带证据的澄清"，唯一被确认"无效"的是"泛泛而谈的辩护"。** arXiv:2511.15462（ICLR 2024+2025，19,000+ 篇、74,000+ 条评审）的多分类模型中，`Evidence backed clarification` 对"分数上升"类的系数为 **+0.23(0.10)**，而 `Generic/vague defense` 为 **−0.29(0.15)**（对"分数不变"类为 **+0.26(0.12)**，即它只帮你维持原判）。`Evasion`（回避立场）对上升类 **−0.10(0.04)**、对不变类 **+0.15(0.07)**。这恰好是 LLM 默认 rebuttal 的两大通病：**空泛同意 + 回避**。
3. **形式约束本身就是最强的"人味"证据。** NeurIPS 2026 Main Track Handbook 明文规定 **"The per-review rebuttal limit is 10,000 characters"**、**不能上传附件**、**"Do not use links in any part of the response"**、禁止泄露身份；ICLR 2026 允许上传 rebuttal revision（正文 **10 页**）并用 **pdfdiff** 比对。也就是说：**"贴一张新跑出来的实验图 / 贴一段真实 diff"是规则允许且 LLM 做不到的事**——而 rebuttal 后分数上升的评审，作者参与率 **95.65%**、对话轮次 **2.21±0.83**（不变组仅 65.92% / 1.47±0.68），说明**多回合、带新产物的互动**才是涨分 correlated 的行为，而不是文本长度。

---

## 精确数字与案例

### 一、ICLR 2024–2025 大规模实测：rebuttal 到底能涨多少分

来源：*Insights from the ICLR Peer Review and Rebuttal Process*（arXiv:2511.15462，2025-11，作者含 Kargaran、Nikeghbal 等）。语料为 ICLR 2024 与 2025 的完整评审周期。

| 年份 | 论文数 | 评审数 | 分数变化记录 |
|---|---|---|---|
| 2025 | 11,672 | 46,748 | 46,353 |
| 2024 | 7,405 | 28,028 | 26,878 |

**评审层面（per review）：**

> "In both years, most review scores remained unchanged (2024: 81%, 2025: 75%), followed by increases (2024: 17%, 2025: 23%), with decreases being the least frequent outcome (2024: 1%, 2025: 1%)."

**论文层面（含录用率，原文表 2）：**

| 年份 | 分组 | 论文数 | 录用率 | 均分 before → after |
|---|---|---|---|---|
| 2025 | Increase | 5,807 | **55.7%** | 5.21 → 5.97 |
| 2025 | Decrease | 377 | 8.0% | 4.88 → 4.41 |
| 2025 | Keep | 5,247 | **7.8%** | 4.30 → 4.30 |
| 2025 | Total | 11,431 | 32.1% | 4.78 → 5.15 |
| 2024 | Increase | 2,930 | **57.6%** | 5.31 → 6.01 |
| 2024 | Decrease | 251 | 6.4% | 4.91 → 4.44 |
| 2024 | Keep | 3,792 | **12.4%** | 4.51 → 4.51 |
| 2024 | Total | 6,973 | 31.2% | 4.86 → 5.14 |

> "Among papers with increased scores, 42% in 2024 and 44% in 2025 were still not accepted despite improved reviewer assessments. However, papers with increased scores were far more likely to be accepted (57.6% and 55.7%) than those with unchanged (12.4% and 7.8%) or decreased (6.4% and 8.0%) scores."

**关键行为学差异（这是"像不像 AI"的实证抓手）：**

| 分组 | 对话轮次 ConvTurn | 作者参与率 AuthPart% | 评审参与率 RevPart% |
|---|---|---|---|
| Increase（2025） | **2.21 ± 0.83** | **95.65** | **86.88** |
| Decrease（2025） | 2.04 ± 1.13 | 83.75 | 66.41 |
| Keep（2025） | 1.47 ± 0.68 | 65.92 | 39.07 |
| Total（2025） | 1.65 ± 0.79 | 73.05 | 50.51 |

> "Reviews with increased scores show higher engagement, including more conversation turns and stronger author–reviewer participation than in the keep or decrease score cases, indicating that active round-trip rebuttal discussions are often correlated with positive score changes."

**时间窗口也有实测差异**（ICLR 2025，评审 11-12 日发布，官方 rebuttal 截止 11-26 前后）：

> "As expected, messages submitted late—after or near the original rebuttal deadline—are less often associated with score increases. Interestingly, messages submitted very early were also less successful... During the period November 18–24, nearly one-third of first messages later led to a review score increase."

即：**第一条回复发在讨论期的中段（而非首日、也非截止最后一刻），约 1/3 后续带来加分。** LLM 一次性生成的 rebuttal 通常在首日或最后一刻提交，正好落在两个低效区间。

**副作用参照：** rebuttal 后评审者之间的分歧整体下降约 **9–10%**（2025：0.1623 → 0.1478，相对 −8.92%；2024：0.1620 → 0.1456，相对 −10.12%），其中 Oral 类下降 **41.33%（2024）/ 48.16%（2025）**，Spotlight 下降 28.54% / 25.96%，而低分/被拒稿下降通常**低于 7%**。说明 rebuttal 主要是"收敛共识"，强稿收敛得最快，弱稿几乎收敛不动。

### 二、"有效 rebuttal"的严格定义下：只有 1%–4%

来源：Nachum Dershowitz（Tel Aviv University）与 Rakesh M. Verma（University of Houston），*Rebutting Rebuttals*，Communications of the ACM，2023（DOI 10.1145/3584664）。他们分析了 **ACL 2018、CHI 2020、CHI 2021、FSCD 2022、SAT 2022** 五个会议共 **7,643** 篇投稿（1,545 + 3,125 + 2,844 + 59 + 70，合计由原文各数字相加得出，原文未直接给总和）。

**ACL 2018（1,545 篇投稿，1,197 份 rebuttal = 77%）：**

> "493 score changes (13% of the reviews): 245 positive (50%) and 248 negative (50%)"

> "Only 24 rebuttals were effective in this sense, a mere 1.6%. Eight or nine of these would have been accepted anyway, so maybe 1% were accepted on account of an effective rebuttal."

> "We estimate that fewer than 1% of the ACL rebuttals achieved their presumed goal of leading to acceptance by clearing up misconceptions or clarifying matters. For the other conferences we examined, the percentage for which the rebuttal might have been a positive factor—but often not the sole factor—in acceptance appears higher (3%–4%)."

| 会议 | 投稿数 | 真正的"有效 rebuttal"占比 |
|---|---|---|
| ACL 2018 | 1,545 | **<1%（严格）/ 1.6%（宽松，24 份）** |
| CHI 2020 | 3,125 | **3.7%（115 篇）** |
| CHI 2021 | 2,844 | **3.6%（103 篇）** |
| FSCD 2022 | 59 | **约 3%–4%**（同时约 2%–3% 因糟糕 rebuttal 受损） |
| SAT 2022 | 70 | **1%–3%（1–2 篇）** |

**反例（rebuttal 会把稿子往下推）：**

> "The (sometimes dramatically) decreased post-rebuttal scores were mostly in reaction to unsatisfactory rebuttals, and a third of the time due to failings noted by other reviewers."

> "Of the 206 with increased scores, 104 were accepted. Of the 207 with lowered scores, almost all (186) were ultimately rejected."

Danfeng (Daphne) Yao 在 CACM 2024-01-08 的观点文章 *Rebuttal How-To* 中直接引用了这个区间：

> "Researchers show 1%–4.4% of papers were positively impacted by rebuttals in five recent conferences."

### 三、有效 vs 无效句式：回归系数给出的实测排序

arXiv:2511.15462 用多分类模型预测"分数上升 / 不变 / 下降"，下表为原文 Table 8 的逐字系数（括号内为标准误）。**这是目前最可核验的一份"句式有效性排序"。**

| 特征（Feature） | All | DEC | **INC（上升）** | KEEP（不变） |
|---|---|---|---|---|
| Overall rating score（rebuttal 前） | 0.67(0.03) | 0.92(0.04) | −1.01(0.03) | 0.08(0.02) |
| Mean overall rating of other reviewers（前） | 0.37(0.02) | −0.56(0.03) | 0.55(0.01) | 0.01(0.02) |
| Reviewer engagement（note 数） | 0.25(0.02) | 0.17(0.03) | 0.20(0.02) | −0.37(0.02) |
| **Generic/vague defense（策略）** | 0.19(0.15) | 0.03(0.17) | **−0.29(0.15)** | **+0.26(0.12)** |
| Contribution score（前） | 0.19(0.02) | −0.27(0.02) | 0.28(0.01) | −0.01(0.01) |
| **Evidence backed clarification（策略）** | 0.15(0.10) | −0.03(0.12) | **+0.23(0.10)** | −0.20(0.09) |
| Bare agreement/disagreement（策略子类） | 0.13(0.09) | −0.05(0.10) | **+0.19(0.09)** | −0.14(0.07) |
| **Evasion（立场子类）** | 0.10(0.04) | −0.06(0.03) | **−0.10(0.04)** | **+0.15(0.07)** |
| Disagree（立场） | 0.10(0.12) | 0.02(0.05) | −0.15(0.13) | 0.13(0.18) |
| Method details（策略子类） | 0.10(0.06) | 0.01(0.07) | −0.15(0.06) | 0.14(0.05) |
| Future promise（策略子类） | 0.10(0.08) | 0.05(0.09) | 0.09(0.08) | −0.15(0.07) |
| Soundness score（前） | 0.10(0.02) | −0.12(0.03) | 0.14(0.02) | −0.03(0.02) |

原文解读（逐字）：

> "Some of the most important features are aspects over which the author has limited control in the rebuttal phase, such as the initial overall rating, the contribution and soundness scores, and the average of other reviewers' scores."

> "Other important features are more strategy-based. For example, a clearly 'evasive stance' or a 'generic/vague defense' strategy tends to only help reviewers maintain their original scores, while 'Bare agreement/disagreement' and providing 'evidence-backed clarification' can help increase the scores."

**模型本身的可预测性上限**（说明"写作技巧"的解释力有限）：三分类 Macro F1 **0.52**，二分类 **0.71**（随机基线 0.33 / 0.50）；只用 word counts 时 macro-F1 降到 **0.43**，用全部特征为 **0.49**。

**评审意见自身的结构权重**（原文 Table 4，对总分的重要性）：`× Novelty & Contribution` **0.47(0.01)** > `× Experiments & Evaluation` **0.32(0.01)** > `× Word Count` **0.25(0.01)** > `✓ Writing & Presentation` **0.23(0.01)** > `× Methodology & Technical Soundness` **0.23(0.01)**。即：**"缺点"栏里写"创新性不足/实验不足"最致命；"写作"只排第 4**。所以把 rebuttal 的力气花在"润色得像人"上，收益远低于去补一个真实实验。

### 四、长度限制与平台硬约束（2026 年版，逐字）

**NeurIPS 2026 Main Track Handbook（`Authors` → `Author Responses`）：**

> "Authors will have the opportunity to view reviews and respond accordingly during the author response period. During this time, authors may not submit revisions of their paper or supplemental material, but may post their responses as a discussion in OpenReview."

> "Using the 'Rebuttal' buttons, authors should respond to each review. Make sure that the 'readers' of the message are those you intend to read it. **The per-review rebuttal limit is 10,000 characters.** You may use plain text with markdown formatting supported by OpenReview, but **you cannot upload any additional files**. These responses can include new results, however your original submission will serve as the basis for the reviewers' (and ACs') acceptance recommendations."

> "Author responses may not contain any identifying information that may violate the double-blind reviewing policy. **Do not use links in any part of the response.** The only exception is if the reviewers asked for code, in which case you can send an anonymized link to the AC in an Official Comment."

（手册 **没有** 对 rebuttal 设 page limit 或 word limit，只有 10,000 **字符/每条评审** 这一条。）

**ICLR 2026 Author Guide：**

> "Nov 11 – December 3 : Public discussion period. Once reviews have been posted, authors can post responses to the reviews as comments on OpenReview. Authors can also revise their paper until the end of the public discussion period (Dec 3)."

> "Q. For rebuttal revisions, how many pages are allowed? The page limit is identical with the submission version (10 pages)."

> "There is a word limit for each comment, but there is no limit on the number of comments."

> "If such a revision is made, a [pdfdiff] will be applied to compare new changes to the paper against the original submission. Area chairs and reviewers reserve the right to ignore changes that are significantly different from the original paper."

**两条 AI 相关硬规则：**

- NeurIPS 2026：`"while authors are welcome to use any tool they wish for preparing and writing the paper, they must ensure that all content is correct and original"`；`"attempts at prompt injections as well as other attempts to manipulate reviewing is strictly prohibited"`；`"agents and LLMs cannot be authors"`。手册的 **Author Responses 章节本身没有出现 LLM / AI-generated 字样**——即 rebuttal 没有被单独立规。
- ICLR 2026：`"if LLMs played a significant role in research ideation and/or writing to the extent that they could be regarded as a contributor, then authors should describe the precise role of the LLM in a separate section on LLM usage. This section can appear in the appendix, and will not be considered as part of the page limit. **Not disclosing significant LLM usage can lead to desk rejection of the paper.**"`

### 五、评审人视角：AI 味的识别与 2026 年的反制措施

**(a) 评审对 LLM 文本的态度（NeurIPS 2026 Handbook 的"灰色地带"条款，逐字）：**

> "Finally, we note that while the explicit use of prompt injections to sway reviewing is strictly prohibited to authors, **there is a gray zone in which authors may adjust their text such that it provides favorable outputs if given to an LLM to review.** Reviewers authorized to use the sanctioned LLM should be aware that authors may have optimized their text in this way, not only for the quality of that review, but also so that authors are not penalized who wrote their papers for people and not for machines."

这一条极其重要：**官方已经把"为了让 LLM 评审给好评而优化文本"写进了手册，并主动提醒评审注意**。这等同于官方承认"AI 友好写作"与"人读友好写作"已经分化。

**(b) 检测器的存在感。** NeurIPS 2026 Position Paper Track 用 **Pangram 3.3.2** 筛查全部 **969** 篇投稿：**273 篇（28.2%）在默认窗口下得到 100% AI 分**；最终 **178 篇（18.4%）标准 desk reject**（不接受申诉），另有 **123 篇** 需在 2026-06-15 前提交"人类实质性参与"的证据。官方称 Pangram 审计的误报率 **低于 0.1%**，并在已录用的 ICLR 2026 论文上只检出 **1%**。（见 startupfortune.com 与 casrai.org 的报道；该组数字与本项目共享上下文一致，但官方原始 blog 未直接抓取，标记为二手，见盲区。）

**(c) 评审实际在抱怨什么。** 二手报道引述 r/MachineLearning 上的评审原话：某稿子的 rebuttal "seems to be entirely LLM-generated"，且原文也 "clearly LLM-generated, with Claude-speak everywhere"，评审的定性是 **"syntactically perfect but semantically hollow defense statements"**（语法完美但语义空洞的辩解）。同时报道指出：NeurIPS 2026 讨论期（8 月 3 日冻结）里，**"authors discovered hidden prompt injections embedded inside several official reviewer comments"**，用于反查评审是否直接粘贴 LLM 输出。

**(d) 反制规模。** ICML 2026 在 Nihar Shah（CMU，scientific integrity chair）主导下向所有投稿注入隐藏提示，据其本人陈述识别出"数百名"违规使用 LLM 的评审，删除 **795 条评审**、desk-reject **497 篇**（约当年投稿量的 **2%**）。Shah 称该策略获得研究者"overwhelming support"，原话：*"People were really tired of reviewers copy-pasting AI-generated reviews without putting any effort."*（来源：The Transmitter 报道的转载；数字为二手，见盲区。）

**(e) 评审侧 LLM 的正面参照。** Thakkar, Yuksekgonul, Silberg, Garg, Peng, Sha, Yu, Vondrick, Zou（arXiv:2504.09737, 2025-04-13；后发表于 Nature Machine Intelligence 2026-02）在 ICLR 2025 做了 **20,000+ 条评审**的随机对照实验：Review Feedback Agent 使 **27%** 的评审修改了评审意见，累计 **12,000+ 条**建议被采纳，修改者的评审平均变长 **80 词**；且收到 AI 反馈的评审在 rebuttal 阶段**更活跃（讨论更长）**。

**(f) 因果建模的新工作。** NeurIPS 2025 CauScien Workshop 收录 *How Effective is Your Rebuttal? Identifying Causal Models from the OpenReview System*（Longkang Li, Ibrahim Aldarmaki, Minghao Fu, Wong Kang, Yunlong Deng, Qiang Huang, Jing Yang, Jin Tian, Guangyi Chen, Kun Zhang），用弱监督解耦因果表示学习，以评审子分数（openness / clarity / directness）作为概念级监督，建模 rebuttal 特征对评分变化的因果效应。**注意：该文摘要未给出可直接引用的具体系数**，本项目只能引用其存在与方法，不能引用数字。

### 六、可执行的"不像 AI"清单（由上述实测反推）

把 Section 三 的系数、Section 一 的行为差异、Section 五 的评审抱怨合起来，得到一份**有数据支撑**的行动清单：

| 做法 | 依据（数字） | 是否 LLM 可伪造 |
|---|---|---|
| 每条意见都挂一个**新跑出来的数**（新实验 / 新消融 / 新统计） | Evidence-backed clarification 对 INC **+0.23**；Yao: *"Virtually all my rebuttals include new numbers and new experimental data."* | **否**（需要真实算力与时间） |
| **转述**评审意见、按重要性**重排**、问题与回答用同一套术语 | Yao: *"You can reorder comments by importance. You can paraphrase the comments."* | 部分可，但重排顺序暴露真实阅读优先级 |
| 明确**承认真实局限**，并给出边界条件 | Yao 的 Tactic 4（"A is out of our threat model…"）；Evasion 对 INC **−0.10** | 部分可 |
| 在讨论期**中段**发第一条回复，之后**跟进 2 轮以上** | 11/18–24 期间 **近 1/3** 首条消息后续带来加分；Increase 组 ConvTurn **2.21±0.83** vs Keep 组 1.47±0.68 | **否**（需要跨多天的真实在场） |
| 删掉所有"泛泛辩护"句（"We thank the reviewer for the insightful comment. We will address this in the camera-ready."） | Generic/vague defense 对 INC **−0.29**，对 KEEP **+0.26** | 正是 LLM 默认输出 |
| ICLR 路线上**上传 rebuttal revision（≤10 页）+ pdfdiff** | ICLR 2026 明文允许；NeurIPS 明文禁止上传附件 | **否**（需要真实改稿） |
| 避免 em dash 堆叠、"delve / it is worth noting / Moreover / Furthermore"三段式等表面 tell | 博客类来源一致指出；但**无同行评议数字**，见盲区 | 可轻易洗掉，故不能当作主要防线 |

**最关键的推论**：真正的防线不是"洗掉 AI 的措辞痕迹"（因为检测器公司自称误报率 <0.1%，而洗词是低成本、对手也在做的军备竞赛），而是 **制造 LLM 无法伪造的时间戳证据链**——跨多天的提交记录、pdfdiff 可比对的版本差异、评审要求后现跑的实验数字。这与本项目"判决可复算 + 证据可追"的核心卖点是同构的。

---

## 对阙疑的 3 条具体行动

1. **在 `_arch_v47/` 下新建 `rebuttal_playbook.md`，把方向 11 的系数表固化成写作检查表，并绑定到具体文件。** 具体：2027-09（NeurIPS 2027 rebuttal 窗口，参照 ICLR 2025 的 11-12→11-26 与 NeurIPS 2026 的 7-27→8-03 节奏，按官方日历校准）之前完成；检查表至少含 5 条硬性门禁——(a) 每条 reviewer 意见必须挂至少一个**新跑数字**（对应 `Evidence backed clarification`，INC +0.23）；(b) 全文禁用 `Generic/vague defense` 句式（INC −0.29），用 grep 检查 "We thank the reviewer for" / "We will address this in the final version" 的零出现；(c) 第一条回复必须在讨论期**中段**发出，且**至少 2 轮**跟进（Increase 组 ConvTurn 2.21 vs Keep 组 1.47）；(d) NeurIPS 路线**每条评审 ≤10,000 字符**、零附件、零链接；(e) ICLR 路线上传 ≤10 页 rebuttal revision 并附 pdfdiff。

2. **把"可复算判决账本"直接变成 rebuttal 的弹药库，而不是事后编。** 具体：在 `research/` 下新增 `rebuttal_evidence_pack/`，预先生成三份可即时取用的产物——(i) `ledger_recompute_demo.md`：给一条 `452 条判决账本`中的具体判决（写明 card_id + 哈希）演示第三方不信任内核的复算；(ii) `holdout_30_breakdown.md`：把盲 holdout **30**（真错 17，检出 66.7%）逐条列出，供评审质疑"检出率是否 cherry-pick"时逐条回；(iii) `counterfactual_fix_log.md`：记录反事实算子 **P = R = F1 = 0** 的修复过程（当前待修）。**这三条正是评审最可能质疑的点，且都是 LLM 无法凭空生成的具体数字。**

3. **为"AI 参与度"准备一份与 Pangram 逻辑对齐的自证材料，时间点：投稿前（2027-05 前）完成初版，rebuttal 期可即时提交。** 具体：在 `_arch_v47/` 下维护 `human_provenance/`，包含 (i) `gate_engine.py`（现 3826 行）的 git 提交历史导出（`git log --format='%H %ad %s' --date=iso > provenance_gate_engine.txt`），证明代码是跨月增量写成而非一次性生成；(ii) `_arch_v46/` 595 个 .py 工具与 75+ 份 AI 生成文档的**明确标注清单**，对应 ICLR 2026 的"LLMs 若有重要贡献必须在附录专章声明，未披露可致 desk reject"与 NeurIPS 2026 的"authors must ensure that all content is correct and original"；(iii) 一旦被要求举证（参照 2026 年那 123 篇的申诉路径），可在 48 小时内提交"版本历史 + AI 使用前后检查点"。

---

## 盲区（诚实标注）

- **arXiv:2511.15462 的"策略"标签是自动标注还是人工标注、标注者一致率（kappa）多少，我没有核实。** 表 8 中 `Evidence backed clarification`、`Generic/vague defense` 等类别的判定标准与标注可靠性直接决定方向 11 的核心结论，但我只拿到了系数，没有拿到标注协议与一致性检验。若该文用 LLM 自动打标，则"AI 味句式扣分"这一结论存在循环论证风险。
- **"AI 写作 tell"（em dash、"delve"、"it is worth noting"、三段式）缺乏同行评议数字。** 我检索到的只有商业博客（explainx.ai 2026-08、blendin.ai 2026-06、aismells.com、bookmoth.app 声称分析了 61,608 篇故事、ransomnews.com 称 arXiv 摘要中 "delve" 在 2024 达峰后到 2026 下降 94%）。这些数字**未核实、不可写入论文**，且方向相反：ransomnews 的说法意味着这类 tell 会自然过期，靠洗词做长期防御无效。
- **NeurIPS 2026 官方 blog 原文我没有直接抓取。** 178 篇 desk reject / 969 篇 / 28.2% / Pangram 3.3.2 / 误报率 <0.1% 这组数字来自 casrai.org、strictcite.com、startupfortune.com 等二手报道；数值上与共享上下文一致，但**逐字引文应当回官方 blog 复核后再写入论文**。
- **ICML 2026 的 795 条评审删除 / 497 篇 desk reject / 约 2% 三个数字来自 The Transmitter 报道的转载（tempmail.ninja、yourai.pro、share.google），不是一手来源。** 其中"family-wise error rate 0.0001"的说法我只在转载中见到，未核实。
- **NeurIPS 2027 E&D 的 rebuttal 规则尚未发布。** 本文件引用的 NeurIPS 2026 Main Track Handbook（10,000 字符）与 ICLR 2026 Author Guide 是**当前最新版**，但 2027 年规则可能变更（ICLR 2027 的提交截止已提前到 9-16，与 NeurIPS 2026 出分 9-24 冲突，说明日程正在剧烈调整）。投稿前必须重新抓取当年手册。
- **样本偏差**：arXiv:2511.15462 只覆盖 ICLR 2024–2025，Dershowitz & Verma 只覆盖 ACL 2018 / CHI 2020–21 / FSCD 2022 / SAT 2022，**都不含 NeurIPS E&D Track**。E&D 的评审结构与 D&B 改名后的评审文化可能显著不同（E&D 强调可复现性而非常规 novelty），把 ICLR 的系数外推到 E&D 属于未经检验的迁移。
- **"评审参与率 RevPart% 86.88% vs 39.07%"是相关而非因果。** 完全可能是"评审本来就打算加分，所以才更愿意回复"，而非"回复导致加分"。因果方向未定。

---

## 来源

1. *Insights from the ICLR Peer Review and Rebuttal Process* — https://arxiv.org/html/2511.15462 — "In both years, most review scores remained unchanged (2024: 81%, 2025: 75%), followed by increases (2024: 17%, 2025: 23%)"；11,672 篇 / 46,748 条评审（2025）— Kargaran, Nikeghbal 等，arXiv:2511.15462 — 2025-11-19
2. 同上，Table 8 策略系数 — https://arxiv.org/html/2511.15462 — "Evidence backed clarification" INC +0.23(0.10)；"Generic/vague defense" INC −0.29(0.15)、KEEP +0.26(0.12)；"Evasion" INC −0.10(0.04) — 同上 — 2025-11-19
3. 同上，Table 2 参与率与对话轮次 — https://arxiv.org/html/2511.15462 — Increase 组 ConvTurn 2.21±0.83、AuthPart 95.65%、RevPart 86.88%；Keep 组 1.47±0.68 / 65.92% / 39.07% — 同上 — 2025-11-19
4. Nachum Dershowitz (Tel Aviv Univ.) & Rakesh M. Verma (Univ. of Houston), *Rebutting Rebuttals*, Communications of the ACM — https://cacm.acm.org/opinion/rebutting-rebuttals/ — "Only 24 rebuttals were effective in this sense, a mere 1.6%"；"fewer than 1% of the ACL rebuttals achieved their presumed goal"；CHI 2020 3.7% / CHI 2021 3.6% — DOI 10.1145/3584664 — 2023-09
5. Danfeng (Daphne) Yao, *Rebuttal How-To: Strategies, Tactics, and the Big Picture in Research*, Communications of the ACM — https://cacm.acm.org/opinion/rebuttal-how-to-strategies-tactics-and-the-big-picture-in-research/ — "Researchers show 1%–4.4% of papers were positively impacted by rebuttals in five recent conferences"；"Trivializing reviewers' critical comments is a common rebuttal pitfall" — 2024-01-08
6. NeurIPS 2026 Main Track Handbook — https://neurips.cc/Conferences/2026/MainTrackHandbook — "The per-review rebuttal limit is 10,000 characters."；"Do not use links in any part of the response."；"there is a gray zone in which authors may adjust their text such that it provides favorable outputs if given to an LLM to review" — NeurIPS 2026 组委会 — 2026
7. ICLR 2026 Author Guide — https://iclr.cc/Conferences/2026/AuthorGuide — "The page limit is identical with the submission version (10 pages)."；"There is a word limit for each comment, but there is no limit on the number of comments."；"Not disclosing significant LLM usage can lead to desk rejection of the paper." — ICLR 2026 组委会 — 2025-09-19
8. *Can LLM feedback enhance review quality? A randomized study of 20K reviews at ICLR 2025* — https://arxiv.org/abs/2504.09737 — 20,000+ 条评审随机对照；27% 评审更新意见；12,000+ 条建议被采纳；+80 词 — Thakkar, Yuksekgonul, Silberg, Garg, Peng, Sha, Yu, Vondrick, Zou（Stanford / CMU / Columbia 等）— 2025-04-13（Nature Machine Intelligence 2026-02 转载：https://www.nature.com/articles/s42256-026-01188-x）
9. *How Effective is Your Rebuttal? Identifying Causal Models from the OpenReview System* — https://neurips.cc/virtual/2025/124110 — NeurIPS 2025 CauScien Workshop；用弱监督解耦因果表示学习，以 openness/clarity/directness 子分数作概念级监督（**摘要未给具体系数，未引用数字**）— Longkang Li, Ibrahim Aldarmaki, …, Kun Zhang — 2025
10. *Detecting LLM-Written Peer Reviews* — https://arxiv.org/html/2503.15772v1 — 检测 LLM 生成评审的方法学背景（本项目未从中取数字，仅作领域定位）— arXiv 2503.15772 — 2025-03-20（v2 2025-05-19）
11. NeurIPS 2026 Pangram desk rejection 报道 — https://startupfortune.com/neurips-is-facing-backlash-over-ai-detector-desk-rejections/ 与 https://casrai.org/news/neurips-2026-pangram-ai-detector-desk-rejection-controversy — 969 篇筛查 / 273 篇(28.2%) 100% AI 分 / 178 篇(18.4%) desk reject / 123 篇举证 — 二手报道，**官方原始 blog 未直接抓取** — 2026-06
12. NeurIPS 2026 隐藏提示（canary）与 ICML 2026 先例报道 — https://www.yourai.pro/the-trap-of-using-ai-in-peer-review-creates-controversy （The Transmitter 转载）— ICML 2026 删除 795 条评审、desk-reject 497 篇（约 2%）；Nihar Shah (CMU) 原话 "People were really tired of reviewers copy-pasting AI-generated reviews without putting any effort." — **二手，未核实** — 2026
13. NeurIPS 2026 rebuttal 现场观察 — http://singularitymoments.com/content/neurips-2026-rebuttal-deadline-chaos-triggers-ai-reviewing-controversy — 评审抱怨 "entirely LLM-generated rebuttals"、"Claude-speak everywhere"、"syntactically perfect but semantically hollow defense statements"；讨论期 2026-08-03 冻结 — **单一二手来源，可信度低，仅作定性佐证** — 2026
14. AI 写作 tell 类博客（**不可引用数字，仅作方向性提示**）— https://www.explainx.ai/blog/top-10-signs-ai-generated-text-2026 、https://blendin.ai/blog/ai-writing-tells 、https://ransomnews.com/ai-writing-tells-expire-2026/ — 后者称 arXiv 摘要中 "delve" 2024 达峰、2026 下降 94% — **未核实** — 2026
