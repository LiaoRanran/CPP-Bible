# 方向 04：NeurIPS Datasets & Benchmarks / Evaluations & Datasets 录用率 · 投稿数 · 接收数（2021–2026 逐年）

## 核心结论

1. **2024 年是该 track 录用率的断崖年**：从 2023 年的 **32.6%**（987 投稿 / 322 录用）骤降到 **25.3%**（1,820 投稿 / 460 录用），跌幅 **7.3 个百分点**，官方定性为"向主赛道对齐（alignment with the main track）"——因为同年主赛道是 25.8%，两者只差 0.5 个百分点。
2. **2025 年投稿增速首次降到个位数**：1,995 篇，相对 2024 年的 1,820 篇只增 **9.6%**（而 2023→2024 是 +84.4%、2022→2023 是 +102.7%）；官方原文明确称"the track has begun to stabilize"。**2025 年官方没有公布录用数**，第三方可复算值为 **24.9%**（497/1,995）。
3. **2026 年 E&D track 的三项数字（投稿数 / 录用数 / 录用率）全部未公开**；可获得的只有主赛道数字 **30,709 / 7,900 / 25.73%**（第三方 OpenAccept）。**本文件对该 track 的 2026 年数据一律标注"未公开"，不做推测。**

---

## 精确数字与案例

### 一、主表：D&B / E&D track 逐年精确数字

| 年份 | track 名称 | 投稿数 | 录用数 | 录用率 | 数据性质 |
|---|---|---|---|---|---|
| 2021 | Datasets and Benchmarks | **未查到** | **未查到** | **未查到** | 首届，未找到官方 Fact Sheet |
| 2022 | Datasets and Benchmarks | **487** | **未查到** | **未查到** | 投稿数来自 2023 Fact Sheet 的对照句 |
| 2023 | Datasets and Benchmarks | **987** | **322** | **32.6%** | **官方 Fact Sheet 原文** |
| 2024 | Datasets and Benchmarks | **1,820** | **460** | **25.3%** | **官方 Fact Sheet 原文** |
| 2025 | Datasets and Benchmarks | **1,995** | **未公布**（第三方 497 / 虚拟站 494） | **未公布**（可复算 24.91% / 24.76%） | 投稿数为官方博客原文 |
| 2026 | Evaluations and Datasets | **未公开** | **未公开** | **未公开** | 作者通知 2026-09-24，列表未发布 |

### 二、逐年逐条溯源

**2022 年：487 篇投稿（唯一可得数字）**

NeurIPS 2023 Fact Sheet 的对照句原文："**987 datasets and benchmarks (more than double the previous year's 487 submissions)**"。因此 2022 年 = 487 篇。**2022 年的录用数官方未给**；Paper Copilot 的 2022 D&B 页面在本次调研中未取到有效统计行（返回的是 JS 壳页）。**标注为未核实。**

**2023 年：987 / 322 / 32.6%（官方 Fact Sheet）**

NeurIPS 2023 Fact Sheet 逐字原文（用 `pypdf` 从 PDF 提取）：

> "● Paper reviews ○ **3,540 total accepted combined papers** ■ 3,218 main conference track ■ **322 datasets and benchmarks track** ○ **13,330 total submissions** ■ 12,343 main conference track ■ **987 datasets and benchmarks (more than double the previous year's 487 submissions)** ○ Paper acceptance rate: ■ **26.1% main conference track** ■ **32.6% datasets and benchmark** ○ Reviewers ■ 968 Area Chairs ■ 98 Senior Area Chairs ■ 12,974 main conference reviewers ■ 1,503 datasets and benchmark reviewers"

**关键结构性事实**：2023 年 D&B 录用率（32.6%）**比主赛道（26.1%）高 6.5 个百分点**——这是该 track 最后一次"比主赛道好中"。同年的**审稿人规模**是 D&B **1,503 人 vs 主赛道 12,974 人**（D&B 占 10.4%），而投稿占比是 987/13,330 = **7.4%**——即 2023 年 D&B 的"审稿人/投稿比"反而**优于**主赛道。

**2024 年：1,820 / 460 / 25.3%（官方 Fact Sheet）**

NeurIPS 2024 Fact Sheet 逐字原文：

> "● Paper reviews ○ **4497 total accepted combined papers** ■ 4,037 main conference track ■ **460 datasets and benchmarks track** ○ **17,491 total submissions** ■ 15,671 main conference track ■ **1,820 datasets and benchmarks (about double the previous year's 987 submissions)** ○ Paper acceptance rate: ■ **25.8% main conference track** ■ **25.3% datasets and benchmark**"

**2024 年的三个关键比值**：
- D&B 录用率 25.3% vs 主赛道 25.8% → **差 0.5 个百分点**，官方在 2025 年复盘博客中明确把这一点当作"对齐成功"的证据："A first step in the direction of alignment with the main track began in 2024, when DB track saw an acceptance rate of 25.3% closely mirroring the main program's 25.8% rate."
- D&B 投稿占比：1,820 / 17,491 = **10.4%**。
- 与 2023 年对比：录用率 **32.6% → 25.3%（−7.3pp）**，投稿数 **987 → 1,820（+84.4%）**。**录用数只从 322 增到 460（+42.9%），远低于投稿增速**——这是录用率下滑的直接算术原因。

**2025 年：1,995 篇投稿（官方），录用数未公布**

投稿数的官方来源有两个，互相印证：

- D&B chairs 复盘博客（2025-09-30）："After three years of exponential growth, the track received **1,995 submissions** this year. While this is a large number, the increase from the **1,820 submissions** received last year is smaller than in previous years (for comparison, there were **987 submissions in 2023**), suggesting that the track has begun to stabilize."
- D&B 年度复盘博客（2025-12-05）："doubling submissions annually through 2024 and increasing further to **1,820 in 2024 and 1,995 in 2025**."

**录用数**：官方 Fact Sheet（`NeurIPS2025-Fact_Sheet.pdf`，154,675 字节）经 `pypdf` 全文提取后，**没有任何 "datasets and benchmarks" 或 E&D 相关数字**（该 PDF 的 Program Overview 只写"Tracks: 3 / Number of Orals: 87 / Number of Posters: 5,290"）。因此 **2025 年 D&B 录用数官方未公布**。

第三方可复算的两个口径：

| 口径 | 来源 | 录用数 | 除以 1,995 得 |
|---|---|---|---|
| Paper Copilot 原始 JSON + 统计页 | `nips/nips2025.json` 中 `status ∈ {Poster, Spotlight, Oral}` = 434+56+7 | **497** | **24.91%** |
| 官方虚拟站事件页 | `nips.cc/virtual/2025/events/datasets-benchmarks-2025` 顶部 "494 Events" | **494** | **24.76%** |

⚠️ **必须避免的错误引用**：Paper Copilot 统计页在 NeurIPS 2025 D&B 行显示 **"Accept 497 (84.09%)"**。这个 84.09% 的分母是 **591**（opt-in 公开评审的样本），**不是 1,995**。该站自己写明："If rating scores are publicly available, the statistics are based on submissions that opted in for release." **84.09% 是样本偏差产物，绝不可当作录用率引用。**

**2026 年：全部未公开**

- 官方 CFP 只给日期："Author notification: **September 24, 2026 (AoE)**"。
- `neurips.cc/Downloads/2026` 原文 "**Number of events: 9127**"——这是全部类别（Posters / Tutorials / Invited talks / Workshops / Demonstrations）的事件数，**不是 E&D 论文数**。
- 探测 `neurips.cc/Conferences/2026/EvaluationsDatasets/AcceptedPapers`、`.../EvaluationsDatasetsAcceptedPapers`、`neurips.cc/virtual/2026/events/evaluations-datasets-2026`、`.../datasets-benchmarks-2026` **全部 404**；`neurips.cc/Conferences/2026/DatasetsBenchmarks/AcceptedPapers` 返回 200 但**正文为空**。
- 第三方 NeurIPS 2026 主赛道数字（OpenAccept）：**Submitted 30,709 / Accepted 7,900 / Acceptance Rate 25.73%**。**未给 E&D 分轨数字。**

### 三、主赛道对照表（用于横向比较）

| 年份 | 主赛道投稿 | 主赛道录用 | 主赛道录用率 | D&B 投稿 | D&B 录用率 | 两者差 |
|---|---|---|---|---|---|---|
| 2023 | 12,343 | 3,218 | **26.1%** | 987 | **32.6%** | +6.5pp |
| 2024 | 15,671 | 4,037 | **25.8%** | 1,820 | **25.3%** | −0.5pp |
| 2025 | 21,575 | 5,290 | **24.52%** | 1,995 | 未公布（≈24.9%） | ≈+0.4pp |
| 2026 | 30,709 | 7,900 | **25.73%** | 未公开 | 未公开 | 未公开 |

主赛道数据来源：2023/2024 来自各自 Fact Sheet；2025 来自 PC chairs 官方博客原文"the main track this year received **21,575 valid paper submissions**, of which **5,290** were accepted. That is, the main track had an acceptance rate of **24.52%**"；2026 来自 OpenAccept（第三方）。

**由此得到一条对阙疑极有用的判断**：**该 track 在 2024 年之后已经"不再比主赛道好中"**。任何"投 D&B 比投主赛道容易"的经验判断，在 2024 年之后**都不成立**。

### 四、投稿量增长的"斜率"分析

D&B track 投稿数的逐年变化：

| 区间 | 投稿数变化 | 增长率 |
|---|---|---|
| 2022 → 2023 | 487 → 987 | **+102.7%** |
| 2023 → 2024 | 987 → 1,820 | **+84.4%** |
| 2024 → 2025 | 1,820 → 1,995 | **+9.6%** |
| 2025 → 2026 | 未公开 | 未公开 |

主赛道投稿数的长期趋势（PC chairs 原文）："growing from **9,467 submissions in 2020 to 21,575 in 2025**"——5 年 **2.28 倍**。而 D&B 从 2022 到 2025 是 487→1,995，3 年 **4.10 倍**。

**2025 年 D&B 增速掉到 9.6% 的官方解释**（D&B chairs 原文）："As the NeurIPS Datasets and Benchmarks (DB) track continues to mature, its growth in submissions is beginning to stabilize, as is also its establishment within the community."

**对阙疑的含义**：2027 年投稿时，E&D track 的竞争强度预计**仍将维持在主赛道同量级（约 25%）**，且随着 2026 年改名扩权（"evaluation becomes an object of scientific study"），**投稿量有可能重新加速**（因为原来投主赛道的评测类论文被明确引导到该 track）。

### 五、录用率的"可控性"证据：AC/PC 可以推翻分数

2025 年 PC chairs 官方博客披露了两类"分数与结果不一致"的情形，逐字摘录：

> "Many ACs fought for papers they thought were good even if reviewers disagreed, and often we followed their lead, ending in an accept decision for the paper. Conversely, sometimes ACs flagged significant negative issues with evidence after the rebuttal that reviewers did not catch, and we ask SACs to carefully discuss these issues with the ACs to ensure the evidence is convincing. **This then led to reject decisions even when papers had high ratings.**"

我们复算的数据也印证这一点：**2024 年 D&B 有 1 篇篇均 3.5 分、1 篇篇均 4.0 分的论文被录用**（10 分制下属于极低分），而**拒稿论文的篇均分上限达 7.00**——两者分数区间**重叠**。

### 六、录用率不是唯一约束：空间与容量

2025 年 PC chairs 原文：

> "In principle, space is a constraint we have to be mindful of, as our physical venues can only permit so many papers. … For the main track, however, as we put our attention on resolving boundary and outlier decisions using the consensus of ACs and SACs during calibration, we reached a **comfortably lower number of accepted papers than the capacity of our venue holds**. That is, **space ultimately played a negligible role** compared to scientific merit."

**这条对阙疑是重要的"止损信息"**：至少在 2025 年主赛道，**"场地不够"不是拒稿理由**；被拒的核心原因仍是"科学价值"与"边界判决"。

### 七、该 track 特有的"分母陷阱"清单（本方向最有价值的产出）

调研过程中我们实际撞到 **5 个不同的"录用数"或"录用率"**，它们互不相等：

| 数字 | 出处 | 实际含义 |
|---|---|---|
| **163** | `neurips.cc/Conferences/2024/DatasetsBenchmarks/AcceptedPapers` 与 **2025 同页逐字相同** | **失效模板占位符**，两年同文，正文仍是 2021 年话术，页面无任何论文条目 |
| **459** | 官方虚拟站 "459 Events"（2024） | 会议现场事件数（含 poster/spotlight/oral） |
| **460** | 官方 Fact Sheet（2024） | 官方录用数 |
| **480** | Paper Copilot 原始 JSON 按 status 过滤（2024） | 含已 withdraw 条目的宽口径 |
| **84.09%** | Paper Copilot 统计页（2025） | **opt-in 样本的录用率**，分母 591，非 1,995 |

**这张表本身就是阙疑论文"元数据必须可对账"论点的最强论据**：同一个官方 track、同一个年份，公开可得的录用数有 **4 个不同值**，录用率有 **2 个数量级不同**的说法。若一个人工研究者都会搞错，机器对账就不是"锦上添花"而是"必要条件"。

### 八、录用率下滑的算术分解（谁"吃掉了"名额）

把 2023→2024 的变化拆成三个可独立验证的量：

| 指标 | 2023 | 2024 | 变化 |
|---|---|---|---|
| D&B 投稿数 | 987 | 1,820 | **+833（+84.4%）** |
| D&B 录用数 | 322 | 460 | **+138（+42.9%）** |
| D&B 录用率 | 32.6% | 25.3% | **−7.3 个百分点** |
| **若维持 2023 年 32.6% 录用率，2024 年应录用** | — | **593** | **实际少录 133 篇** |
| D&B 录用数 / 全会议录用数 | 322 / 3,540 = **9.1%** | 460 / 4,497 = **10.2%** | +1.1pp |
| D&B 投稿数 / 全会议投稿数 | 987 / 13,330 = **7.4%** | 1,820 / 17,491 = **10.4%** | +3.0pp |

**这张表的核心结论**：**D&B 的投稿份额（7.4%→10.4%，+3.0pp）增长快于它的录用份额（9.1%→10.2%，+1.1pp）**。也就是说，2024 年 D&B 的录用率下滑**不是"名额被主赛道挤占"**（它的录用份额其实还上升了 1.1pp），而是**投稿涌入了 3.0pp 而录用只跟上 1.1pp**。**这否定了"该 track 被主赛道抢名额"的常见猜测。**

**2025 年的检验**：若按 2024 年的 25.3% 推算，1,995 篇应录用约 **505** 篇；第三方可复算的 497（或虚拟站 494）与之相差 8–11 篇，**在 1.6%–2.2% 的相对误差内**。这说明**2025 年的录用率基本是 2024 年水平的延续（约 24.8%–25.3%）**，官方说的"向主赛道对齐"在数字上是站得住的。

### 九、投稿量增长的"赛道生命周期"判断

把 D&B 与主赛道的投稿增长放在同一坐标系里，可以看到 D&B 走的是**一条压缩的"生命周期"曲线**：

| 阶段 | D&B 对应年份 | 增长率 |
|---|---|---|
| 起步（首届） | 2021 | — |
| 高速增长期 | 2022→2023 | +102.7% |
| 高速增长期 | 2023→2024 | +84.4% |
| **平台期** | **2024→2025** | **+9.6%** |
| 未知（改名扩权） | 2025→2026 | **未公开** |

对照主赛道：2020 年 9,467 篇 → 2025 年 21,575 篇，**5 年 2.28 倍**（年均约 17.9%）；而 D&B 从 2022 年的 487 篇到 2025 年的 1,995 篇，**3 年 4.10 倍**（年均约 60%）。**D&B 用 3 年走完了主赛道 5 年多的增长量**，然后迅速进入平台期。

**2026 年的不确定性来源**：官方把 track 改名为 Evaluations & Datasets，并明确"evaluation becomes an object of scientific study in its own right"，同时说这次改名"**broadens the scope** … allowing works that were previously submitted to the main track to be more clearly aligned with the ED Track's reframed focus"。**这句话的直白含义是：原本投主赛道的评测类论文会被引导过来。** 因此 2026 年 E&D 的投稿量**有可能重新加速**，而录用率**可能进一步下探**。

**对阙疑的可执行结论**：把"2027 年 E&D 录用率预期"设为 **22%–27%**，并在其中标注一个"上行风险"：若 2026 年投稿量跳增 30% 以上且录用数未同比扩张，则实际录用率可能落到 **20%–23%**。**这个区间应当在 2026-11（2026 年数字公开后）用实测值替换。**

### 十、"分母纪律"：本方向对阙疑最有价值的可迁移规则

本方向在调研中实际撞到 5 个互不相等的"录用数"，并在 2025 年撞到"84.09% vs 24.91%"这一对相差 3.4 倍的"录用率"。把这两件事抽象成一条规则：

> **任何百分数都必须附带三件套：(a) 分子的精确定义；(b) 分母的精确定义与规模；(c) 被排除项及其理由。**

用这条规则审查阙疑现有的三个数字，会发现**三处都需要补分母说明**：

| 阙疑数字 | 现状 | 按"分母三件套"应补充 |
|---|---|---|
| 盲 holdout 检出率 **66.7%** | 原文"10/15 可测" | 分母 15 的由来：30 seeds 中真错 17，**排除 2 条的理由是什么**？（未在扫描文件中找到） |
| 外部 corpus 检出率 **43.8%** | 原文 40 条三层，A 54.2% / B 12.5% / C 0% | 43.8% 的分子是 17.5 还是 17 或 18？**分层分母是 24/16/…？** 需逐层给数 |
| 缺陷夹具重注入检出 **100%** | 原文 6/6 | 分母 6 ≠ 夹具总数 15；**另 9 条为何未纳入重注入测试**？ |

**这三条不是"论文写法建议"，而是"如果不对齐就会被审稿人抓住"的硬伤**——因为 2026 年 E&D 的 CFP 明确要求"what claims it supports, **under what assumptions**, and what limitations apply"。**分母的定义就是最重要的 assumption。**

---

## 对阙疑的 3 条具体行动

1. **把"5 个录用数"做成论文里的一张实证表**：在 `research/12_threats_to_validity.md` 新建小节 `T3: Same venue, five different acceptance counts`，逐行列出 163 / 459 / 460 / 480 / 84.09% 及其出处 URL 与失效原因。**然后写一句关键论证**："如果一个官方会议 track 的录用数在公开渠道上有 4 个互不相等的值、录用率有 2 个数量级不同的说法，那么任何声称'XX% 检出率'的系统都必须同时发布**分母的定义与可复算脚本**。" 时间点：投稿前（2027-05 前）。
2. **给阙疑的每个百分数加上"分母三件套"**：修改 `research/08_metrics.md`，规定每个百分数必须同时给出 **(a) 分子、(b) 分母、(c) 分母被排除项的理由**。按此规则，阙疑现有的三个数字应改写为：
   - 盲 holdout 检出率 **66.7% = 10/15**，分母 15 = 30 seeds 中"可测"的 17 真错里排除 2 条（**必须写明这 2 条为何不可测**）；
   - 外部 corpus 检出率 **43.8% = 约 17.5/40**（原文为 40 条三层，A 54.2% / B 12.5% / C 0%，需核对分层分母）；
   - 缺陷夹具重注入检出 **100% = 6/6**，分母 6 **不等于**夹具总数 15（历史覆盖 12/15=80% 是另一个分母）。
   **这条规则直接源自本方向发现的"84.09% vs 24.91%"事故**。时间点：2026-10 前。
3. **为 2027 年的投稿做一次"E&D 竞争强度预测"并写入 ROADMAP**：用本文件的主表拟合一条简单趋势（D&B 录用率 32.6% → 25.3% → ≈24.9%），在 `_arch_v46/ROADMAP.md` 的第五组或 `research/16_venue_choice.md` 里写入结论：**2027 年 E&D 录用率的合理预期区间是 22%–27%**，并注明"若 2026 年 E&D 因改名扩权导致投稿量跳增，区间下限应下调"。**同时**标注一个监控动作：2026-10 至 2026-11 期间重新抓取 `neurips.cc/Conferences/2026/EvaluationsDatasets/AcceptedPapers` 与虚拟站事件页，把 2026 的三个数字补进本表。时间点：2026-11 前完成首轮刷新。

---

## 盲区（诚实标注）

- **2021 年 D&B 的投稿数、录用数、录用率全部未查到**。NeurIPS 2021 Fact Sheet 在 `media.neurips.cc/Conferences/NeurIPS2021/NeurIPS2021-Fact_Sheet.pdf` 返回 404；2021 年该 track 有独立 proceedings（`datasets-benchmarks-proceedings.neurips.cc/paper_files/paper/2021`），但**未逐条统计**。
- **2022 年 D&B 的录用数与录用率未查到**。仅有投稿数 487（来自 2023 Fact Sheet 的对照句，属间接来源）。
- **2025 年 D&B 的录用数官方未公布**；本文件的 497 与 494 分别是第三方与虚拟站口径，**24.91% / 24.76% 是本文件自行计算**，非官方数字。
- **2026 年 E&D track 的三项数字全部未公开**（撰写于 2026-09-29，距作者通知 5 天）。**必须重刷**。
- **2026 年主赛道 30,709 / 7,900 / 25.73% 来自 OpenAccept 第三方**，未在官方 Fact Sheet 中核对（2026 Fact Sheet 撰写时点未发布）。**2025 年 OpenAccept 给的是 21,575 / 5,290 / 24.52%**，与官方 PC chairs 博客逐字一致，故 OpenAccept 在主赛道上的可信度较高；但其**是否包含各分轨，未核实**。
- **2025 年主赛道"Number of Posters: 5,290"** 与"录用 5,290 篇"数值相同，官方 Fact Sheet 的字段定义（Poster 是否等价于 accepted）**未核实**。
- **Paper Copilot 的 `Total` 字段口径不稳定**：2024 D&B 行的 `Total = 1820` 与官方投稿数一致，但 2025 D&B 行的 `Total = 591` 显然只是 opt-in 样本。**该站未对 2025 行的 `Total` 做口径说明**，这是一个已知的、可复现的第三方数据缺陷。
- **"2024 年有 1 篇篇均 3.5 分被录用"** 来自本文件对 Paper Copilot 原始 JSON 的复算（`mean-rating buckets: (3.5, 1), (4.0, 1)`），**未逐篇打开 OpenReview 确认这两篇的最终 decision**。

---

## 来源

1. NeurIPS 2024 Fact Sheet（官方 PDF）— https://media.neurips.cc/Conferences/NeurIPS2024/NeurIPS2024-Fact_Sheet.pdf — "460 datasets and benchmarks track" / "1,820 datasets and benchmarks" / "25.3% datasets and benchmark" / "4,037 main conference track" / "15,671 main conference track" / "25.8% main conference track" — NeurIPS，2024-12-20
2. NeurIPS 2023 Fact Sheet（官方 PDF）— https://media.neurips.cc/Conferences/NeurIPS2023/NeurIPS2023-Fact_Sheet.pdf — "322 datasets and benchmarks track" / "987 datasets and benchmarks (more than double the previous year's 487 submissions)" / "32.6% datasets and benchmark" / "26.1% main conference track" / "1,503 datasets and benchmark reviewers" — NeurIPS，2023-12-19
3. NeurIPS 2022 Fact Sheet（官方 PDF）— https://media.neurips.cc/Conferences/NeurIPS2022/NeurIPS_2022_Fact_Sheet.pdf — "2,905 accepted papers / 9,634 full paper submissions / 20% paper acceptance percentage / 16 Datasets and Benchmark Orals"（**未拆分 D&B 投稿与录用**）— NeurIPS，2022-12-19
4. Reflecting on the 2025 Review Process from the Datasets and Benchmarks Chairs — https://blog.neurips.cc/2025/09/30/reflecting-on-the-2025-review-process-from-the-datasets-and-benchmarks-chairs/ — "1,995 submissions" / "1,820 submissions" / "987 submissions in 2023" / "25.3% … 25.8%" — NeurIPS Blog，2025-09-30
5. Reflections on the 2025 Review Process from the Program Committee Chairs — https://blog.neurips.cc/2025/09/30/reflections-on-the-2025-review-process-from-the-program-committee-chairs/ — "21,575 valid paper submissions, of which 5,290 were accepted" / "24.52%" / "9,467 submissions in 2020" / "space ultimately played a negligible role" / "reject decisions even when papers had high ratings" — NeurIPS Blog，2025-09-30
6. NeurIPS Datasets & Benchmarks Track: From Art to Science in AI Evaluations — https://blog.neurips.cc/2025/12/05/neurips-datasets-benchmarks-track-from-art-to-science-in-ai-evaluations/ — "1,820 in 2024 and 1,995 in 2025" / "41 senior area chairs, 281 area chairs and 2,680 reviewers" — NeurIPS Blog，2025-12-05
7. NeurIPS 2025 Fact Sheet（官方 PDF）— https://media.neurips.cc/Conferences/NeurIPS2025/press/NeurIPS2025-Fact_Sheet.pdf — 经 `pypdf` 全文提取后**无 D&B 数字**；仅 "Number of Posters: 5,290" / "Number of Orals: 87" — NeurIPS，2025-12-10
8. Paper Copilot 统计与原始数据 — https://legacy.papercopilot.com/paper-list/neurips-paper-list/neurips-2025-accepted-paper-list-datasets-benchmarks-track/ 与 https://github.com/papercopilot/paperlists（`nips/nips2024.json`、`nips/nips2025.json`）— 2024 D&B Total 1820 / Accept 459 (25.22%)；2025 D&B Total 591 / Accept 497 (84.09%) — Paper Copilot，2026 访问
9. NeurIPS 2026 Evaluations & Datasets Track Call for Papers — https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets — "Author notification: September 24, 2026 (AoE)" — NeurIPS，2026
10. OpenAccept，NeurIPS 2026 / 2025 / 2024 统计 — https://openaccept.org/c/ai/neurips/2026/ 、 https://openaccept.org/c/ai/neurips/2025/ 、 https://openaccept.org/c/ai/neurips/2024/ — 2026: 30,709 / 7,900 / 25.73%；2025: 21,575 / 5,290 / 24.52%；2024: 15,671 / 4,043 / 25.80% — OpenAccept，2026
11. NeurIPS 2024 / 2025 D&B Accepted Papers 模板页（含失效的"163"）— https://neurips.cc/Conferences/2024/DatasetsBenchmarks/AcceptedPapers 与 https://neurips.cc/Conferences/2025/DatasetsBenchmarks/AcceptedPapers — 两页逐字同为 "Below is the list of the 163 accepted submissions" — NeurIPS，2024/2025
12. NeurIPS 2024 / 2025 D&B 虚拟站事件页 — https://neurips.cc/virtual/2024/events/datasets-benchmarks-2024 （"459 Events"）与 https://nips.cc/virtual/2025/events/datasets-benchmarks-2025 （"494 Events"）— NeurIPS，2024/2025
