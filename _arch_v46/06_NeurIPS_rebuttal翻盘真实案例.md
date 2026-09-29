# 方向 06：NeurIPS rebuttal 翻盘真实案例

> 调研时间：2026-09-29（GMT+8）
> 检索工具：WebSearch ×13 + WebFetch ×8（OpenReview / arXiv / NeurIPS 官方 blog / 一手论坛）
> 锚点：阙疑（queyi）——67 条判决规则（block 44）+ 四态判决 + append-only 哈希链；目标 NeurIPS 2027 E&D track

## 核心结论

1. **rebuttal 提分是统计上真实存在、且高度集中于 borderline 论文的现象**：ICLR 2024 有 17%、ICLR 2025 有 23% 的评审分数在 rebuttal 后上升，而下降仅 1%；分数上升论文的接收率（57.6% / 55.7%）是不变论文（12.4% / 7.8%）的 4.5–7 倍。
2. **提分的最强预测因子不是 rebuttal 写得多好，而是"初始分数"与"其他审稿人的评分"**：ICLR 大规模因果分析显示，"审稿人前序总分"对"提分"的系数为 −1.01、"其他审稿人均分"为 +0.55，均强于任何文本特征——这意味着单篇低分论文靠 rebuttal 翻盘的概率结构性地低。
3. **能稳定换分的 rebuttal 只有一种句式：「承认原稿缺了什么证据 → 立刻给新实验 → 用小表给结果 → 明确说出该实验排除了哪个替代解释」**，而"通用/模糊辩护"（generic/vague defense，系数 −0.29）与"回避"（evasion，−0.10）在统计上主要导致维持原分。

## 精确数字与案例

### 一、五个可核验的"rebuttal 改分"实例

以下五个案例来自一篇 2026-07-25 的知乎长文《从 OpenReview 上的低分转高分论文看如何 rebuttal》，该文逐个给出了 OpenReview forum id。我已直接核验了其中两个（NetHack、Qonvolution）的 OpenReview 页面。

**案例 1（已核验）：NetHack is Hard to Hack —— 4 → 7**
- 论文：*NetHack is Hard to Hack*，作者 Ulyana Piterbarg、Lerrel Pinto、Rob Fergus，NeurIPS 2023 poster，Submission Number 501，OpenReview id `tp2nEZ5zfP`（https://openreview.net/forum?id=tp2nEZ5zfP）。
- 知乎文引述审稿人原话：「作者的 rebuttal 回应了我的担忧，因此我将评分从 4 提高到 7，以表达接收支持。」
- 我在 OpenReview 页面上确认了论文标题、三位作者、NeurIPS 2023 poster 身份与 Submission Number 501；**审稿人原话与 4→7 的分数变化未能从公开页面直接读到**（OpenReview 默认只展示最终版本，初版分数会被覆盖——这正是下文 arxiv 2511.15462 论文需要专门爬取历史快照的原因）。
- 论文摘要给出的量化结果：SOTA 神经 agent 在 offline 设置下比此前全神经策略高 127%，online 设置高 25%，但仍无法逼近符号 agent。

**案例 2（已核验）：Qonvolution —— 两位审稿人 4 → 6**
- 论文：*Qonvolution: Towards Learning of High-Frequency Signals with Queried Convolution*，作者 Abhinav Kumar、Tristan Ty Aumentado-Armstrong、Lazar Valkov、Gopal Sharma、Alex Levinshtein、Radek Grzeszczuk、Suren Kumar，Submitted to ICLR 2026，Submission Number 14056，OpenReview id `j8Cz0jPvXW`（https://openreview.net/forum?id=j8Cz0jPvXW）。
- 我在 OpenReview 页面确认了标题、七位作者、ICLR 2026 投稿身份与 Submission Number 14056。
- **注意一个重要的口径问题**：知乎文写这篇文章时（2026-07）语境是 NeurIPS rebuttal 季，但该文的 OpenReview 页面显示它是 **ICLR 2026 投稿**，不是 NeurIPS 投稿。因此本文把"改分实例"作为**跨会议（ICLR/NeurIPS 同一套 OpenReview + rebuttal 机制）**的证据使用，而不声称它是 NeurIPS 案例。这一点必须写进阙疑的 Threats to Validity。
- 该案例对阙疑最有用的地方：reviewer 的主要质疑是"实验验证不足"，作者通过补充实验改变判断——这与阙疑当前的处境（holdout 30 样本、真错 17、检出率 66.7%）高度同构。

**案例 3：MOSAIC —— 两位审稿人 4 → 6**
- OpenReview id `7AH0y1OtnC`。知乎文描述：讨论记录显示两位 reviewer 在 rebuttal 后从 4 提到 6，reviewer 评价作者提供了强有力的 rebuttal 并解决了主要问题。**我未核验该页面**。

**案例 4：Large Language Models Suffer From Their Own Output —— 3 → 5**
- OpenReview id `SaOxhcDCM3`。知乎文引述：「感谢作者提供新实验；reviewer 将评分从 3 提高到 5。」**我未核验该页面**。

**案例 5：Mixtures of Subspaces for Bandwidth Efficient Context —— 两位审稿人提升到 solid accept**
- OpenReview id `x3qnrhfhX0`。知乎文描述：作者通过清晰 rebuttal 解决 reviewer 问题，其中包括补充对 warm-start duration 不敏感性的验证（sensitivity study），最终两位 reviewer 提升到 solid accept。**我未核验该页面**。

**案例 6（附加，非 NeurIPS）：SANA —— 所有审稿人 +2 分，排名跃升至第 9**
- 论文：*SANA: Efficient High-Resolution Image Synthesis with Linear Diffusion Transformers*，NVIDIA + MIT + 清华，ICLR 2025，arXiv 2410.10629，OpenReview id `N8Oj1XhtYZ`。
- 量化结果：4K 图像生成比 SOTA 的 FLUX 快 100 多倍；1K 分辨率快 40 倍；单张消费级 4090 上生成 1024×1024 只需 0.37 秒。
- rebuttal 结果：知乎文标题称"所有审稿人都加了 2 分"，论文排名跃升至第 9。第四位审稿人原本给 10 分（满分），在作者逐一回答其四个问题后表示「我再也看不到这篇论文中任何明显的缺点了。因此，我提高了我的评分」。
- **诚实标注**：知乎文正文只逐条佐证了第 1、2、3 位审稿人各加 2 分，第 4 位只给出"10 分最高分 + 后续提高评分"的表述。因此"所有审稿人都加 2 分"这一说法**未获逐条证实**。

### 二、ICLR 2024/2025 全量数据：rebuttal 到底能改变多少

这是本轮调研最有价值的一手量化来源：arXiv:2511.15462，*Insights from the ICLR Peer Review and Rebuttal Process*，作者 Amir Hossein Kargaran、Nafiseh Nikeghbal、Jing Yang、Nedjma Ousidhoum，2025-11-19 提交，代码与分数变化数据开源在 https://github.com/papercopilot/iclr-insights。

**语料规模（Table 1）**

| 年份 | 论文数 | 评审数 | 分数变化记录数 |
|---|---|---|---|
| ICLR 2025 | 11,672 | 46,748 | 46,353 |
| ICLR 2024 | 7,405 | 28,028 | 26,878 |

（因评审发布时的技术问题，不到 5% 的论文在 rebuttal 前无记录分数，故变化记录数少于评审数。）

**论文层面（Table 2）**

| 年份 | 类型 | 论文数 | 接收率 | 平均评级变化 |
|---|---|---|---|---|
| 2025 | 上升 | 5,807 | **55.7%** | 5.21 → 5.97 |
| 2025 | 下降 | 377 | 8.0% | 4.88 → 4.41 |
| 2025 | 不变 | 5,247 | 7.8% | 4.30 → 4.30 |
| 2025 | 总体 | 11,431 | 32.1% | 4.78 → 5.15 |
| 2024 | 上升 | 2,930 | **57.6%** | 5.31 → 6.01 |
| 2024 | 下降 | 251 | 6.4% | 4.91 → 4.44 |
| 2024 | 不变 | 3,792 | 12.4% | 4.51 → 4.51 |
| 2024 | 总体 | 6,973 | 31.2% | 4.86 → 5.14 |

**评审层面（Table 2）**

| 年份 | 类型 | 评审数 | 对话轮次 | 作者参与% | 审稿人参与% | 评分变化 |
|---|---|---|---|---|---|---|
| 2025 | 上升 | 10,728 | 2.21±0.83 | 95.65 | 86.88 | 4.64 → 6.34 |
| 2025 | 下降 | 640 | 2.04±1.13 | 83.75 | 66.41 | 5.95 → 4.10 |
| 2025 | 不变 | 34,985 | 1.47±0.68 | 65.92 | 39.07 | 4.81 → 4.81 |
| 2024 | 上升 | 4,666 | 2.04±0.75 | 99.79 | 80.73 | 4.58 → 6.30 |
| 2024 | 下降 | 359 | 1.71±0.89 | 90.25 | 50.7 | 6.28 → 4.49 |
| 2024 | 不变 | 21,853 | 1.35±0.57 | 75.26 | 30.65 | 4.91 → 4.91 |

**四个必须记住的数字**
1. 评审分数**保持不变**的比例：2024 年 **81%**，2025 年 **75%**。
2. **上升**：2024 年 **17%**，2025 年 **23%**。
3. **下降**：两年均仅 **1%**（最罕见）。
4. 分数上升的论文中，**42%（2024）/ 44%（2025）最终仍未被接收**——提分 ≠ 录用。

**改分集中在哪些分数段**：最频繁的变化序列是 **5 → 6、6 → 8、3 → 5**（Figure 3）。即 borderline（边界）区间。排名位移上：rebuttal 前排名前 5% 的论文有**超过 40%** 在分数更新后被替换；约 **20%** 的论文在 rebuttal 后失去前 30% 的位置。

**最佳 rebuttal 时间窗**：2025 年在 **11 月 18–24 日**期间发出的首条消息，有近 **三分之一（约 1/3）**后来导致评分上升；过早或临近/超过截止的首条消息与提分关联更弱。审稿人活动高峰为 2025 年 11 月 25–26 日。

### 三、什么写法真的换到分：系数表

同一篇论文（§4.2, Table 8）给出了"策略 → 分数变化"的系数方向。模型三分类（Decrease / Keep / Increase）macro F1 = **0.51（±0.02）**，二分类 macro F1 = **0.69（±0.02）**。

| 特征 | 平均\|系数\| | INC（提分） | KEEP（不变） |
|---|---|---|---|
| rebuttal 前总体评级分数 | 0.67 | **−1.01** | 0.08 |
| 其他审稿人平均评级（前） | 0.37 | **+0.55** | 0.01 |
| 审稿人参与度（note 数） | 0.25 | +0.20 | −0.37 |
| 通用/模糊辩护（策略） | 0.19 | **−0.29** | **+0.26** |
| 有证据支撑的澄清（策略） | 0.15 | **+0.23** | −0.20 |
| 单纯同意/不同意（策略子类） | 0.13 | +0.19 | −0.14 |
| 回避（立场子类） | 0.10 | **−0.10** | +0.15 |
| 不同意（立场） | 0.10 | **−0.15** | +0.13 |
| 未来承诺（策略子类） | 0.10 | +0.09 | −0.15 |

结论：**"有证据支撑的澄清"（+0.23）与"单纯同意/不同意"（+0.19）是唯一两个明确指向提分的文本策略**；"通用/模糊辩护"（−0.29）与"回避"（−0.10）明确指向维持原分。另一个反直觉发现：**71% 的分数变化只体现在总体评级（overall rating）上**，没有同步更新 soundness 等其他维度（Table 6）——说明 reviewer 的改分往往是"整体感觉变了"，而非"逐维度重估"。

论文明确声明：以上均为**相关性而非因果性**。

### 四、审稿人认知偏差：为什么"口头认可"不等于"改分"

一篇 2026-08-03 的中文解析（控场AI）记录了一个真实 Reddit 提问：作者分数为 4/4、3/2、3/2、2/4（前者评分、后者置信度），其中打 **2 分且置信度 4** 的审稿人在讨论期明确表示"疑虑已解决"，但**始终没有更新评分**。

该文给出的机制解释（均属社区经验，非官方统计，须标注）：审稿人惰性、保守心态、时间压力、锚定效应（anchoring bias）、确认偏误、现状偏见、从众/级联效应。同时给出 NeurIPS 官方**并未公布**审稿人改分的精确统计这一事实。

该文还引用了 2014 年 NIPS 一致性实验——我核验了原始记录（Computational Complexity 博客，Lance Fortnow，2014-12-18，引 Eric Price 分析）：
- NIPS 2014 把程序委员会劈成两组独立的 PC，**10%（166 篇）**投稿被两组同时评审；
- 其中约 **16 篇（约 10%）**被两组都接收，**43 篇（26%）**被恰好一组接收，**107 篇（64%）**被两组都拒；
- 换算：**被接收论文中超过一半（57%）**在换一组 PC 的情况下不会被接收；**被拒论文中 83%** 仍会被拒。

这是"审稿噪声 > 论文质量差异"的最强证据，也是阙疑 Threats to Validity 里"单一 venue 判决不可复现"的现成引用。

### 五、NeurIPS 自己的官方规则与规模

从 NeurIPS 官方来源（Call for Papers 2025 / FAQ 2025 / 2025 PC Chair 反思博客）可确认：
- **rebuttal 窗口 = 1 周**（"Authors will have one week to view and respond to initial reviews"）。
- **2025 年取消全局 rebuttal，改为 per-review rebuttal，上限 10,000 字符**；不能上传任何额外文件；不能用链接（唯一例外是 reviewer 索要代码时，可经 Official Comment 发给 AC 一个匿名链接）。
- **rebuttal 期间不允许提交论文或补充材料修订**。
- **rebuttal 不会立刻对审稿人可见**——"the rebuttals will be revealed to the reviewers/ACs at the end of the rebuttal period"。
- rebuttal **可以含新结果**，但"original submission will serve as the basis for the reviewers' (and ACs') acceptance recommendations"。
- 规模（2025 PC Chair 博客，2025-09-30）：主 track 收到 **21,575** 篇有效投稿，接收 **5,290** 篇，录用率 **24.52%**；参与的有 **20,518 名审稿人、1,663 名 AC、199 名 SAC**。
- 官方承认一个新噪声源：**"reviewers increasing their scores just to end back-and-forth discussion with the authors, but being silent or critical in private discussions with the AC"**（审稿人为结束来回讨论而提分，却在与 AC 的私下讨论中保持沉默或批评）——官方判断这与"作者 rebuttal 参与度上升导致审稿人疲劳"有关。
- 另有 **11 例**因共同作者"严重失职评审"（grossly negligent reviews）导致其关联投稿被 desk reject。

另一篇相关论文：*How Effective is Your Rebuttal? Identifying Causal Models from the OpenReview System*，作者 Loka Li、Ibrahim Aldarmaki、Minghao Fu、Wong Yu Kang、Yunlong Deng、Qiang Huang、Jing Yang、Jin Tian、Guangyi Chen、Kun Zhang，ICLR 2026 Conference **Withdrawn Submission**，Submission Number 9704，OpenReview id `tysOWd3RWm`。该文用弱监督因果表征学习（CRL）建模 rebuttal 文本，试图给出可识别的因果结构。**注意：该投稿已被撤稿（Withdrawn）**，引用时须标注这一状态。

### 六、可复用的 rebuttal 结构（综合上述案例的共性）

五个成功案例的共同骨架（来自知乎文的归纳，我逐条对照了可核验案例）：
1. **先承认原稿缺了什么证据**："We agree that the original submission did not sufficiently distinguish X."（而不是 "We respectfully disagree because Section 3 already explains X."）
2. **马上给新实验**，不要先重述 motivation。
3. **用小表先给结果**——"Rebuttal 里 table 比三段解释更有价值"。
4. **明确说出实验排除了哪个替代解释**："This rules out generic pretraining and model capacity as sufficient explanations."
5. **提炼一条原论文没讲清的新 insight**。
6. **对过强 claim 主动收窄**："We agree that the original wording was too broad and will revise..."

## 对阙疑的 3 条具体行动

1. **在 2026-10 至 2026-11 期间，为论文 v0.3 写一份"预 rebuttal 弹药库"文件 `research/14_rebuttal_arsenal.md`**，按上述 6 段骨架，针对阙疑最可能被攻击的 5 个点（holdout 仅 30 样本、外部 corpus 检出率 43.8%、C 层 0%、反事实算子 P=R=F1=0、单作者无 baseline）各写一条"承认缺口 + 已做的新实验 + 小表 + 排除了什么"的四段式。工具：直接用 Markdown 写；命令：`python tools/gate_engine.py --check` 复跑一遍，把结果贴进表里。时间点：2027-05 投稿前定稿。

2. **把"分数上升 ≠ 录用"这一条写进论文 §Threats to Validity 与 §Evaluation**：引用 ICLR 2024 的 42% / ICLR 2025 的 44%（分数上升但仍被拒），以及 2014 NIPS 实验的 57% / 83%。具体做法：在 `research/12_threats_to_validity.md` 新增一节 "Venue-level noise"，落点写明"阙疑的 66.7% 检出率是系统属性，不是录用概率的预测器"。时间点：2026-12 前完成。

3. **为 rebuttal 窗口做时间预算**：NeurIPS E&D 2026 的 rebuttal 只有 **5 天**（2026-07-22 至 07-27，见 `08_ICSE_ED_vs_NeurIPS_ED对比.md`），且 rebuttal 在窗口结束前对审稿人不可见。行动：在 2027-06 之前把 `data/holdout/`、`data/external_corpus/`、`data/defect_fixtures/` 三套数据各准备一条"一键复跑"命令，并预先算好"若审稿人要求扩样，需要多少算力/多少小时"。工具：`tools/` 下的 `--check` 自检脚本 + 一个新增的 `tools/rebuttal_snapshot_<batch>.py`（只在 `_arch_v46/` 记录设计，不改仓库其它文件）。

## 盲区（诚实标注）

- **5 个改分案例中我只直接核验了 2 个**（NetHack `tp2nEZ5zfP`、Qonvolution `j8Cz0jPvXW`）；MOSAIC `7AH0y1OtnC`、LLM Suffer From Their Own Output `SaOxhcDCM3`、Mixtures of Subspaces `x3qnrhfhX0` 三个 forum id **未核验**，其分数变化数字**采信知乎二手转述**。
- **NetHack 的"4 → 7"与审稿人原话未能从公开 OpenReview 页面读到**（页面只展示最终版本）。OpenReview 覆盖初版分数是 arxiv 2511.15462 需要专门存档快照的原因，也意味着任何"分数变化"引述都应标注"来自二手/快照"。
- **Qonvolution 是 ICLR 2026 投稿而非 NeurIPS 投稿**，知乎文在 NeurIPS rebuttal 语境下引用它，存在口径混淆。本文已标注。
- **SANA 的"所有审稿人都加 2 分"未被逐条证实**，仅第 1、2、3 位有佐证。
- **NeurIPS 官方从未公布审稿人改分的精确统计**；所有 NeurIPS 侧的改分比例数字（如"约 20% 会改分"）均为社区经验值，本文未采用。
- Paper Copilot 的 NeurIPS 2025 页面显示"5,526 投稿 / 95.46% 录用"，与官方 blog 的 21,575 / 24.52% 严重不符，判断为该页面抓取口径错误（可能只抓到某一子集），**本文一律以 NeurIPS 官方 blog 数字为准**。
- "rebuttal 策略系数表"来自 arxiv 2511.15462，该文自述为**相关性**分析；不得表述为因果。
- *How Effective is Your Rebuttal?* 一文状态为 **Withdrawn Submission**，其结论不可当作已发表结果引用。
- 所有 ICLR 数字来自 2024/2025 两届，**NeurIPS 的对应数字在 2027 时点需重新爬取**（OpenReview API + 快照存档）。
- 2014 NIPS 实验的 166 篇、57%、83% 已核验于 Computational Complexity 博客与 Eric Price 分析，但该实验是 2014 年的，**不能直接外推到 2027 年的评审规模**（当年投稿量约 1/10）。

## 来源

1. Kargaran, A. H., Nikeghbal, N., Yang, J., Ousidhoum, N. (2025). *Insights from the ICLR Peer Review and Rebuttal Process.* arXiv:2511.15462. https://arxiv.org/abs/2511.15462 ；数据与代码：https://github.com/papercopilot/iclr-insights
2. *NetHack is Hard to Hack*，Piterbarg, U., Pinto, L., Fergus, R.，NeurIPS 2023 poster，Submission Number 501。https://openreview.net/forum?id=tp2nEZ5zfP
3. *Qonvolution: Towards Learning of High-Frequency Signals with Queried Convolution*，Kumar, A. 等，Submitted to ICLR 2026，Submission Number 14056。https://openreview.net/forum?id=j8Cz0jPvXW
4. Li, L., Aldarmaki, I., Fu, M. 等 (2025). *How Effective is Your Rebuttal? Identifying Causal Models from the OpenReview System.* ICLR 2026 Withdrawn Submission，Submission Number 9704。https://openreview.net/forum?id=tysOWd3RWm
5. NeurIPS (2025). *Call For Papers 2025*（rebuttal 一周、双投与 collusion 条款）。https://neurips.cc/Conferences/2025/CallForPapers
6. NeurIPS (2025). *NeurIPS 2025 FAQ for Authors*（per-review rebuttal 10,000 字符上限、禁止链接、rebuttal 结束时才可见）。https://neurips.cc/Conferences/2025/PaperInformation/NeurIPS-FAQ
7. NeurIPS Communications Chairs (2025-09-30). *Reflections on the 2025 Review Process from the Program Committee Chairs*（21,575 / 5,290 / 24.52% / 20,518 reviewers / 11 例 desk reject）。https://blog.neurips.cc/2025/09/30/reflections-on-the-2025-review-process-from-the-program-committee-chairs/
8. Fortnow, L. (2014-12-18). *The NIPS Experiment.* Computational Complexity。https://blog.computationalcomplexity.org/2014/12/the-nips-experiment.html ；原始分析：http://blog.mrtz.org/2014/12/15/the-nips-experiment.html
9. 知乎 (2026-07-25). 《从 OpenReview 上的低分转高分论文看如何 rebuttal》。https://zhuanlan.zhihu.com/p/2064466275745653337
10. 知乎 (2024-11-28). 《rebuttal 真的有用！这篇 ICLR 论文，所有审稿人都加了 2 分》（SANA 案例）。https://zhuanlan.zhihu.com/p/9533078343
11. 控场AI (2026-08-03). 《NeurIPS 讨论期审稿人口头认可后会改分吗？经验解析》。https://www.kongchang.com/articles/neuripstao-lun-qi-shen-gao-ren-kou-tou-ren-ke-hou-hui-gai-fen-ma
12. NeurIPS (2025). *Reviewer Guidelines 2025.* https://neurips.cc/Conferences/2025/ReviewerGuidelines
