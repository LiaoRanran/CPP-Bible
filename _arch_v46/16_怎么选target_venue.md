# 方向 16：怎么选 target venue（决策框架）

> 调研时间：2026-09-29
> 对象项目：阙疑 / queyi（C++ 知识验证器，67 条判决规则内嵌引擎 + 四态判决 + append-only 哈希链 + 独立对账器）
> 数据集锚点（采信 `00_仓库扫描.md`）：盲 holdout 30 seeds（真错 17 / 对照 9 / unknown 4）、外部 corpus 40 条（A/B/C 三层）、真实缺陷夹具 15 条；内核 `tools/gate_engine.py` = 3826 行；实卡 37 张。

---

## 核心结论

1. 阙疑的贡献形态（**评估工具 + 审计方法 + 主动登记的负结果**）与 NeurIPS 自 2026 年起改名后的 **Evaluations & Datasets (E&D) Track** 的定义几乎逐条命中——该 track 官方 CFP 明文写「evaluation becomes an object of scientific study」，并把「Contribute tools, analyses, or frameworks that improve how evaluative claims are constructed or interpreted」「Present negative results, critical analyses」「Submissions need not introduce a new model or outperform prior work」列为 in-scope；这是 NeurIPS 正赛里**唯一不要求打败 baseline** 的轨道。

2. 但对「0 影响力 + 单作者 + 无导师背书」的画像，**TMLR 的单人生存友好度显著高于任何会议**：它把「novelty 不够」「没打赢 SOTA」「贡献太小」三条会议拒稿理由**在成文规则里判为 out of bounds**，允许用「降低 claim」替代补实验，2025 年录用率 70.6%（若计入撤回与 desk reject 则 46.3%）；代价是决策中位数 91 天（短稿）/104 天（长稿）、且**没有会议曝光与口头报告机会**。

3. 单作者最优解不是「单选」而是**三窗口错峰**：ICLR 2027（截稿 2026-09-25，已过）→ ICML 2027（约 2027-01-22~28）→ NeurIPS 2027（约 2027-05-20~21）。三者截稿间隔 4 个月与 4 个月，正好把「一次失败的沉没成本」摊到 12 个月里，且每一轮都能拿回公开评审意见做下一轮的修改依据。

---

## 精确数字与案例

### 一、先把「NeurIPS E&D」是什么讲清楚（2026 改名事件）

NeurIPS 官方博客 2026-03-23 发布《Introducing the Evaluations & Datasets Track at NeurIPS 2026》，宣布 **Datasets & Benchmarks Track 正式改名为 Evaluations & Datasets (ED) Track**。改名的理由原文是：「**evaluation becomes an object of scientific study**」——评估本身成为科学研究的对象，而不再只是数据集/基准的附属品。ED Track chairs 列名为：Konstantina Palla、Jessica Schrouff、Alexandre Drouin、Lijun Wu、Joaquin Vanschoren。

对阙疑最重要的三条 scope 变化（均为官方 CFP 原文，非转述）：

- 「Analyze strengths, limitations, or failure modes of existing benchmarks or evaluation practices」——**审计既有评估实践**。阙疑的「独立对账器 + 四态判决」正属于此类。
- 「Contribute tools, analyses, or frameworks that improve how evaluative claims are constructed or interpreted」——**改进评估性论断的工具/框架**。阙疑的 67 条规则内嵌引擎 + append-only 哈希链（可独立复算的证据链）逐条命中。
- 「Submissions need not introduce a new model or outperform prior work」——**不要求新模型、不要求打败前人**。这一条对阙疑是决定性的：它的反事实算子 P=R=F1=0（论文 v0.3 已主动放弃该口径），在任何「比性能」的轨道上都会被一票否决。

同时 CFP 对**数据集类**投稿新增了硬约束：「dataset submissions should also clarify how they should be meaningfully used in evaluative practices rather than being endpoints in themselves」「Papers that present data without clarifying the intended problem formulation, evaluation setup, or interpretive boundaries are unlikely to provide sufficient context for review」。这句话的实践含义是：**「我只是放了一个大数据集」不再够**。阙疑如果走 ED track，必须把「30 seeds / 40 corpus / 15 fixtures」讲成「评估性论断的证据集」，而不是「我收集了一个数据集」。

### 二、ED Track 的关键时间与格式硬约束（2026 版，可外推 2027）

2026 ED Track 与主赛道**同 timeline**（官方 CFP 原文「The dates are identical to the main track」）：

| 节点 | 2026 日期 |
|---|---|
| 投稿系统开放 | 2026-04-15 |
| Abstract 截止 | 2026-05-04 (AoE) |
| Full paper 截止（含全部补充材料） | 2026-05-06 (AoE) |
| 评审期 | 2026-05-29 ~ 2026-06-25 |
| 紧急评审期 | 2026-07-06 ~ 2026-07-13 |
| AC 初始 meta-review | 2026-07-13 ~ 2026-07-22 |
| 评审放出 | 2026-07-22 |
| 作者 rebuttal | 2026-07-22 ~ 2026-07-27 |
| 作者+评审+AC 讨论期 | 2026-07-27 ~ 2026-08-03 |
| 评审+AC 讨论期 | 2026-08-03 ~ 2026-08-10 |
| Meta-review 期 | 2026-08-10 ~ 2026-08-17 |
| 通知 | 2026-09-24 (AoE) |

（以上来自 NeurIPS 2026 ED Track Reviewing Guidelines 的 Timeline 段落。）

**格式硬约束**（来自 ED Track Reviewer Guidelines 与 Main Track Handbook）：

- 正文 **9 页**（含 Introduction 到 Conclusion / Discussion / Limitations / Future Work），参考文献不限页，附录不限页；评审明确写「We allow page excess of the paper limit **up to 5 lines**」。
- **超页或改 style file = desk reject**，且是自动检查。官方原文：「Submissions that violate these requirements are subject to desk rejection」。
- **2026 起 ED Track 默认双盲**（这是新变化：「Unlike previous years, the default review mode for the E&D Track is now **double-blind**」）。只有「数据集无法为科学或伦理原因完整匿名」时才在投稿表里选 single-blind。
- **代码政策改为 contribution-dependent**：若主要贡献是「reusable executable artifact, such as a benchmark suite, evaluation environment, data generator, or software tool, whose functionality must be inspected」，则**投稿时代码发布是强制的**；分析/概念/方法类则可选，但必须填 `code_submission_justification`。
- **数据集必须挂 Croissant 元数据**，且 2026 年新增要求同时提供 core 字段与 **Responsible AI (RAI) 字段**。数据须托管在 Dataverse / Kaggle / Hugging Face / OpenML 等持久平台，且**投稿时对所有评审/AC/SAC 可访问、无需向 PI 单独申请**；>4GB 须附小样本。
- **ED Track 评审不得使用任何 LLM/AI agent**（与主赛道不同，ED track「没有经 OpenReview 的 LLM 实验」）；严重违规可能连带 desk reject 评审者关联的投稿。
- **评审量表**：ED Track Reviewing Guidelines 用的是四个维度——**Quality / Clarity / Significance / Originality**，且明确写「Originality does not necessarily require introducing an entirely new method」。注意：ED Track 指南**没有公布数字打分区间**（1–6 或 1–10），这一点与主赛道 reviewer form 不同，属未核实项。

### 三、录用率：三年真实数字（可查证）

**NeurIPS Datasets & Benchmarks Track 投稿与录用**（Paper Copilot 从 OpenReview 抓取，2026-09-29 复核）：

| 年份 | 投稿数 | 录用数 | 录用率 | 备注 |
|---|---|---|---|---|
| 2022 | 447 | 163 | **36.47%** | 首年（track 2021 年设立） |
| 2023 | 985 | 322 | **32.69%** | Poster 290 / Spotlight 22 / Oral 10 |
| 2024 | 1,820 | 459 | **25.22%** | Poster 392 / Spotlight 56 / Oral 11 |
| 2025 | **1,995** | 未核实 | 未核实 | 投稿数来自 NeurIPS 官方博客 2025-12-05 |

**关键趋势**：2022→2024 投稿量从 447 涨到 1,820（**4.07 倍**），录用率从 36.47% 掉到 25.22%（**下降 11.25 个百分点**）。官方 2024 Fact Sheet 也确认：「1,820 datasets and benchmarks (about double the previous year's 987 submissions)」，主赛道 2024 录用率 25.8%，D&B 25.3%——**D&B 录用率与主赛道已基本持平**。这直接否证了「D&B 是水 track」的旧印象。

**2025 的数字要注意口径陷阱**：NeurIPS 官方博客 2025-12-05 明写「increasing further to 1,820 in 2024 and **1,995 in 2025**」，并给出该年 track 的组织规模：「**41 senior area chairs, 281 area chairs and 2,680 reviewers**」。但 Paper Copilot 抓到的 2025 D&B 记录只有 **591 条**（其中 Accept 497 / Reject 94），据此算出的「84.09% 录用率」是**样本偏差产物**（公开评分 opt-in 严重偏向录用者），不可当真实录用率。我在本方向把 2025 的录用率列为**未核实**。

**NeurIPS 主赛道对照**（OpenAccept，2026-09-29 读取）：

| 年份 | 投稿 | 录用 | 录用率 |
|---|---|---|---|
| 2023 | 12,343 | 3,218 | 26.07% |
| 2024 | 15,671 | 4,043 | 25.80% |
| 2025 | 21,575 | 5,290 | 24.52% |
| 2026 | 30,709 | 7,900 | 25.73% |

注意 2026 主赛道投稿 30,709 是 2025（21,575）的 **1.42 倍**——一年涨 42%。若 2027 ED track 跟随同比例增长，**投稿量可能从 1,995 涨到 2,800 量级**，录用率大概率继续下滑。这是阙疑必须在 2027 前算进去的风险。

**ICLR 对照**：ICLR 2025 主赛道投稿 11,565、录用 3,710、录用率 **32.08%**（OpenAccept）。ICLR 2027 的截稿日是 **abstract 2026-09-18、full paper 2026-09-25（AoE）**（OpenCurious 与 mldeadlines 均记 2026-09-25；iclr.cc 官方 Dates 页当时仍写「location and dates to be announced」）。⚠️ **这意味着以 2026-09-29 为「今天」，ICLR 2027 已经截稿 4 天，本周期不可投。**

### 四、TMLR：单人生存友好度的天花板

TMLR（Transactions on Machine Learning Research，JMLR 旗下）是**期刊**而非会议，规则与会议相反。2026-08-14 读取 TMLR FAQ + 2025 年度报告得到：

- **录用率两个数**：**70.6%**（不计撤回与 desk reject）/ **46.3%**（计入全部投稿）。2024 年的第二口径是 50.6%，官方解释是「much higher desk-rejection rate after an influx of weak submissions」。
- **明文取消的拒稿理由**（TMLR acceptance criteria 原文）：novelty「Not a necessary criteria for acceptance」；「The interest criterion cannot be used to reject work for not reaching a new state of the art」；「Accept papers that meet the criteria, even if the contribution is modest」。**这三条恰好覆盖了阙疑最可能被杀的三把刀。**
- **两条判据**：①claims are supported by accurate, convincing and clear evidence（官方称「the most important criterion」）；②would some individuals in its audience be interested（且「an unsure reviewer must assume they would be」）。**第二条对阙疑极有利——只要有一个小圈子（C++ 工具链/编译器测试/形式化方法社区）会感兴趣即可。**
- **claim/evidence gap 有两条出口**：「more experiments are not the only way: another is for the authors to **reduce their claims**」。这是会议 rebuttal 里不存在的动作——会议论文正文已冻结，只能承诺 camera-ready 改；TMLR 允许直接把 claim 写小。**阙疑论文 v0.3 已经主动放弃变异率 97.3% 与扩样样本盲态证据两个口径，这正是 TMLR 鼓励的动作。**
- **决策时长（实测，非官方承诺）**：Zachary Robertson 抓取 OpenReview API 全部 5,844 份 TMLR 投稿（截至 2026-02-06），筛出 4,865 份有三份评审且有决定的样本，测得「第三份评审 → 最终决定」的**中位数 45.2 天**、75 分位 57.0 天、90 分位 72.5 天、99 分位 116.2 天；**82.5% 的论文超过官方 35 天（5 周）窗口**，只有 4.3% 在 28 天内拿到决定。TMLR 2025 年度报告自报的中位数是**短稿 91 天 / 长稿 104 天**（官方目标约 9 周），2024 年分别是 97 / 113 天。
- **重要副产品**：Robertson 的分桶分析发现「等待时长与拒稿率无关」——15–35 天窗口拒稿率 26.9%，75–100 天窗口 30.5%，**基本持平**。即「等得久 = 论文有争议」是错觉，纯粹是流程延迟。
- **TMLR 的硬坑**（会直接吃掉一次投稿机会）：①**不接受会议论文的扩展版**（text/figures/results 任一复用即不合格，JMLR 才收扩展版）；②**泄露身份会永久失去改投 TMLR 的资格**（rejected submission 保持公开且作者可被 unmask）；③**有年度投稿配额**（Generalized Harmonic Quota Rule，N1=2 / N9=9，评审和 AE 翻倍）；④**动 style file 即可能无评审拒稿**；⑤**2025 年识别出 20+ 例 LLM 不当使用**，每例调查，最重可 1 年投稿禁令。

### 五、第三档：JOSS 与 SE 会议（阙疑的「安全垫」）

- **JOSS（Journal of Open Source Software）**：审稿标准明写在 review_criteria 页，核心是「A clear statement of need that illustrates the purpose of the software」「A description of how this software compares to other commonly used packages」——**明确允许「实现已被别处解决的功能」的软件被接收**，只要文档、测试、可安装性达标。对阙疑这种「3826 行内核 + 595 个 .py 工具 + 640 条目目录」的项目，JOSS 是最低摩擦的「可引用凭证」。⚠️ 我**未查到 JOSS 的官方录用率数字**，列为未核实。
- **ICSE 2027 / ASE 2026 / FSE 2027**：SE 社区与阙疑的「编译器/工具链测试」主题更近。ICSE 2027 Research Track 有独立 OpenReview（icse2027.hotcrp.com），社区截止日跟踪站 se-deadlines.github.io 记「ICSE 2027：April 25 – May 1, 2027，Dublin, Ireland」。⚠️ **具体投稿截稿日我未逐条核实**（SE 会议多为双轮/多 deadline 制）。
- **MLSys 2026**：deadline 2025-10-30（AoE），系统向。对阙疑偏「ML 系统」，匹配度低于 ED track。

### 六、真实决策案例（三个可查证的 venue 选择）

**案例 A：SWE-bench（ICLR 2024，非主赛道之外的「评测框架」）。** 论文 `SWE-bench: Can Language Models Resolve Real-world Github Issues?`，作者 Carlos E Jimenez、John Yang、Alexander Wettig、Shunyu Yao、Kexin Pei、Ofir Press、Karthik Narasimhan。它把一个「评测框架 + 2,294 个 GitHub issue 任务 + 19,000 训练实例 + 两个微调模型」打包投 ICLR 主赛道并被接收。**关键决策点**：它的最强结果是**负结果**——「表现最好的模型 Claude 2 只能解决 **1.96%** 的 issue」。这告诉我们：**「SOTA 全线崩盘」本身就是可发表的结论**，前提是你把 benchmark 建得足够可信（执行式验证、仓库自带测试作 oracle）。阙疑的「holdout 真错 17 检出率 66.7%」和「外部 corpus 43.8%」是同类结论，但**样本量小 2~3 个数量级**，这是它必须先在 ED track 而不是主赛道出场的根本原因。

**案例 B：DataComp（NeurIPS 2023 Datasets and Benchmarks Track）。** 作者 33 人（Samir Yitzhak Gadre 等），投稿量级是「12.8B image-text pairs」。它的贡献枚举是 5 条（我们会在方向 19 逐条拆解），其中第 5 条是「DataComp-1B，新 SOTA 数据集」，并在同算力下超过 OpenAI CLIP ViT-L/14 **3.7 个百分点**。**它选 D&B 而非主赛道的理由**：贡献主体是「数据集 + 评测 testbed + 300+ 基线实验」，不是新算法。**对阙疑的映射**：阙疑的贡献主体是「判决引擎 + 证据链 + 三套评估数据」，同理应选评测向轨道。

**案例 C：Csmith（PLDI 2011，非 NeurIPS 路线）。** 作者 Xuejun Yang、Yang Chen、Eric Eide、John Regehr，University of Utah。论文 `Finding and Understanding Bugs in C Compilers` 摘要原文：「we created Csmith, a randomized test-case generation tool, and spent **three years** using it to find compiler bugs. During this period we reported **more than 325** previously unknown bugs to compiler developers. **Every compiler we tested was found to crash and also to silently generate wrong code** when presented with valid input.」——它明确把贡献写成两条：①推进编译器测试 SOTA（生成覆盖大 C 子集且**避开 UB/unspecified behavior** 的程序）；②一组关于真实编译器 bug 的定性与定量结果。**注意 Csmith 的「避开 UB」正是阙疑的镜像问题**：阙疑做的是「识别 UB 类知识错误」，Csmith 做的是「生成不含 UB 的测试程序」。两者互为参照系，这也是阙疑在 Related Work 里必须处理的一条线（见方向 20）。Csmith 投 PLDI 而非 NeurIPS，因为 2011 年 NeurIPS 没有 D&B track，而 PLDI 是编程语言/编译器测试的主场。

### 七、给阙疑的打分表（五维，1–5 分，权重按「单作者 + 0 影响力」画像设）

| 维度 | 权重 | NeurIPS E&D 2027 | ICML 2027 | TMLR | JOSS | ASE 2026 / ICSE 2027 |
|---|---|---|---|---|---|---|
| **主题匹配度**（评估工具/审计/负结果） | ×3 | **5**（CFP 逐条命中） | 3（无 E&D track，需走主赛道或 Position track） | **5**（claims+evidence 判据） | 4（软件论文） | **5**（工具与测试） |
| **截稿可行性**（以 2026-10-08 为 W30 起点） | ×3 | **5**（2027-05-06，210 天） | 3（约 2027-01-22，约 106 天，紧） | **5**（滚动，无 deadline） | **5**（滚动） | 2（未核实，可能已在窗口外） |
| **录用率**（越高越好） | ×2 | 2（D&B 2024 已 25.22%） | 2（ICML 2025 主赛道 26.9%） | **5**（70.6% / 46.3%） | 4（未核实但门槛低） | 2（SE 顶会通常 20% 上下） |
| **审稿周期**（越短越好） | ×1 | 3（投稿→通知约 4.6 个月） | 3（约 3.3 个月） | 2（中位 91–104 天，但**无 deadline 压力**） | 3（未核实） | 3（未核实） |
| **单人生存友好度**（无导师/无背书/无算力） | ×3 | 3（双盲 + 匿名代码，弱化机构；但 9 页压缩 + Croissant + RAI 字段对单人工作量大） | 2（主赛道拼 SOTA，阙疑无胜算） | **5**（明文不看 novelty、可降 claim、可无 deadline） | 4（只看软件工程质量） | 4（工具论文对单人友好） |

**加权总分**（满分 5）：NeurIPS E&D 2027 = (5×3 + 5×3 + 2×2 + 3×1 + 3×3)/13 = (15+15+4+3+9)/13 = **3.54**；ICML 2027 = (3×3 + 3×3 + 2×2 + 3×1 + 2×3)/13 = (9+9+4+3+6)/13 = **2.38**；TMLR = (5×3 + 5×3 + 5×2 + 2×1 + 5×3)/13 = (15+15+10+2+15)/13 = **4.38**；JOSS = (4×3 + 5×3 + 4×2 + 3×1 + 4×3)/13 = (12+15+8+3+12)/13 = **3.85**；ASE/ICSE = (5×3 + 2×3 + 2×2 + 3×1 + 4×3)/13 = (15+6+4+3+12)/13 = **3.08**。

**结论**：**TMLR 是保底首选，NeurIPS E&D 2027 是曝光首选，JOSS 是凭证首选**。三者不互斥——JOSS 先拿（滚动投稿，无冲突）、TMLR 与 NeurIPS 并行（TMLR 接受「已投会议被拒的论文」不构成 overlap；但反过来，**NeurIPS 的 dual submission 政策禁止同期投归档 venue**，所以顺序必须是「NeurIPS 被拒 → 改投 TMLR」，不能同时）。

---

## 对阙疑的 3 条具体行动

1. **立刻（2026-10-08 前）建立 `_arch_v46/venue_scores.json`，把上面五维打分表落成可复算数据**：字段 `venue / match / deadline_feasibility / accept_rate / review_duration / solo_friendliness / weight / weighted_score / verified(bool) / source_url`。对每个数字标注 `verified: true/false`——**2025 D&B 录用率、JOSS 录用率、ICSE 2027 截稿日三项必须标 false**。命令：`python tools/gate_engine.py --check venue_scores.json`（沿用仓库既有的 `--check` 自检惯例，不新增文件到 `tools/`，只读校验）。这一步的作用是把「选 venue」从感觉变成可审计的判决，与阙疑自身「可被独立验收」的方法论同构。

2. **2026-10-08（W30 第一天）起，把 Croissant 元数据与 RAI 字段当作一等交付物来做**，而不是投稿前一周补。理由：ED Track 2026 CFP 明文「Datasets and code must be properly hosted, accessible, and clearly documented **upon submission**; these are essential submission requirements」，且官方 2025 年复盘披露**投稿首轮缺失字段的真实比例**：license 缺失 11.9%、dataset description 缺失 4.9%、URL 缺失 3.5%，**RAI 扩展采用率极低**。具体做法：在 `data/holdout/`、`data/external_corpus/`、`data/defect_fixtures/` 三个目录各写一份 `croissant.json`，字段至少含 `@type: Dataset / name / description / license / url / citeAs / crs` + RAI 的 `dataCollection / dataBiases / personalSensitiveInformation / dataUseCases`，用 Hugging Face 的 croissant-checker 在线校验（`https://huggingface.co/spaces/JoaquinVanschoren/croissant-checker`）。**这一步现在做，是因为它同时也是方向 17 时间线里 W6–W3 的关键路径项，提前做完等于给最后 3 周腾出缓冲。**

3. **把「三窗口错峰」写进 `_arch_v46/17_单人论文写作时间线.md` 的倒排表，并在 2027-01-22（ICML 2027 预估截稿）前完成一次「零成本试投」**：即用同一份 9 页稿投 ICML 2027 主赛道（哪怕明知录用率 26.9% 且主题匹配度只有 3），目的是**在 NeurIPS 2027 截稿前 4 个月拿到一轮真实评审意见**。若 ICML 拒稿，其 reviews 直接作为 NeurIPS 版本的修改依据；若 ICML 接收，则 NeurIPS 版本改投 ED track 的**另一篇**（如把「独立对账器」单独拆成一篇 tools/frameworks 投稿），避免 dual submission。时间点硬约束：**ICML 2027 投稿必须在 2027-01-20 前完成**（预留 2 天应对时区/系统故障）。

---

## 盲区（诚实标注）

- **NeurIPS 2025 D&B 的真实投稿-录用率未核实**。官方博客只给「1,995 submissions」与组织规模（41 SAC / 281 AC / 2,680 reviewers），未给录用数；Paper Copilot 抓到的 591 条是严重偏采样的子集（Accept 497 / Reject 94），据此算出的 84.09% 不可用。2026 ED Track 的录用率同理**尚未公布**（通知日为 2026-09-24，但我在 2026-09-29 未检索到官方统计）。
- **ED Track 的数字评分量表未核实**。ED Track Reviewing Guidelines 只用 Quality/Clarity/Significance/Originality 四维文字判据，**未列出 1–6 或 1–10 的分数定义**；主赛道 2026 Reviewer Guidelines 也未见分数区间。任何「ED track 几分能中」的说法都缺乏一手依据。
- **NeurIPS 2027 / ICML 2027 的截稿日是社区跟踪站估值，非官方**。researchtheta.com 记 NeurIPS 2027 为 2027-05-20（通知 2027-09-25，会期 2027-12-06~12，欧洲），OpenCurious 记 2027-05-21；ICML 2027 记 2027-01-22（OpenCurious）或 2027-01-28（researchtheta）。**截至 2026-09-29，NeurIPS 2027 与 ICML 2027 的官方 CFP 均未发布**，上述日期须在 2026-11 后重新核对。
- **ICSE 2027 / ASE 2026 / FSE 2027 的具体截稿日未核实**。se-deadlines.github.io 只给出会期（ICSE 2027：2027-04-25~05-01，都柏林），未逐条确认 research track 的 deadline。
- **JOSS 的录用率、审稿中位数未核实**。JOSS 官方只公布 review criteria 与流程，未见统计页。
- **「TMLR 不接受会议扩展版」与「NeurIPS 禁 dual submission」的组合规则未逐字核对 TMLR FAQ 与 NeurIPS CFP 的交叉条款**。我的推断是「NeurIPS 被拒后可投 TMLR」，依据是 phdflow 对 TMLR 编辑政策的解读「A paper a conference rejected — Not overlap, on our reading: the ban covers published, accepted or parallel work」，但**未在 jmlr.org 一手页面逐字确认**。
- **投稿量增长外推（2027 ED track 约 2,800）是线性外推，非预测**。依据仅为 NeurIPS 主赛道 2025→2026 的 1.42 倍增长；ED track 的实际增长可能被「改名后 scope 扩大吸引主赛道投稿」进一步推高，也可能被「Croissant/RAI 门槛提高」压低。

---

## 来源

1. NeurIPS 2026 Evaluations & Datasets Track Call for Papers — https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets （2026 年读取；含 scope、timeline、Croissant/RAI、代码政策、双盲变更）
2. Introducing the Evaluations & Datasets Track at NeurIPS 2026 — NeurIPS Blog，2026-03-23，https://blog.neurips.cc/2026/03/23/introducing-the-evaluations-datasets-track-at-neurips-2026/ （改名理由与 scope 定义）
3. NeurIPS Evaluations & Datasets 2026 Reviewing Guidelines — https://neurips.cc/Conferences/2026/EvaluationsDatasetsReviewerGuidelines （四维判据、9 页+5 行、desk reject 条款、LLM 禁用、完整 timeline）
4. NeurIPS 2026 Main Track Handbook — https://neurips.cc/Conferences/2026/MainTrackHandbook （9 页正文、50MB、双盲、contribution type 五选一）
5. NeurIPS Datasets & Benchmarks Track: From Art to Science in AI Evaluations — NeurIPS Blog，2025-12-05，https://blog.neurips.cc/2025/12/05/neurips-datasets-benchmarks-track-from-art-to-science-in-ai-evaluations/ （2025 投稿 1,995；41 SAC/281 AC/2,680 reviewers；Croissant 缺字段比例 11.9%/4.9%/3.5%；851 作者 + 155 评审问卷）
6. NeurIPS 2024 Fact Sheet（Longterm Wiki 转载） — https://www.longtermwiki.com/resources/3590e18cc6687057 （1,820 D&B 投稿、459 录用、25.3% D&B / 25.8% main；17,491 总投稿）
7. Paper Copilot — NeurIPS 2024/2025 Datasets & Benchmarks 统计 — https://papercopilot.com/paper-list/neurips-paper-list/neurips-2024-paper-list-datasets-benchmarks-track/ 与 https://legacy.papercopilot.com/paper-list/neurips-paper-list/neurips-2025-accepted-paper-list-datasets-benchmarks-track/ （2022/2023/2024 投稿与录用分 tier 明细）
8. OpenAccept — NeurIPS 主赛道历史统计 — https://openaccept.org/c/ai/neurips/ （2023–2026 投稿/录用/录用率）
9. OpenAccept — ICLR 2025 统计 — https://openaccept.org/c/ai/iclr/2025/ （11,565 投稿 / 3,710 录用 / 32.08%）
10. How Long Do TMLR Decisions Actually Take? An OpenReview Audit — Zachary Robertson, Stanford University, 2025（2026-02-06 发布），https://zrobertson466920.github.io/TMLRAudit/ （4,865 份样本；第三评审→决定中位 45.2 天、P75 57.0、P90 72.5、P99 116.2；82.5% 超 5 周；等时与拒稿率无关）
11. TMLR explained: 70.6% accepted — phdflow.ai，2026-08-14，https://phdflow.ai/guides/tmlr-explained （70.6%/46.3% 双口径；91/104 天中位；acceptance criteria 三条 out of bounds；配额规则；LLM 违规 20+ 例）
12. JOSS Review Criteria — https://joss.readthedocs.io/en/latest/review_criteria.html （「clear statement of need」「how this software compares to other commonly used packages」）
13. ICSE 2027 Research Track — https://conf.researchr.org/track/icse-2027/icse-2027-research-track ；SE 会议 deadline 跟踪 — https://se-deadlines.github.io/ （ICSE 2027 会期 2027-04-25~05-01，都柏林）
14. MLSys 2026 Dates and Deadlines — https://mlsys.org/Conferences/2026/Dates ；https://mldeadlines.com/conference/mlsys-2026/ （截稿 2025-10-30 AoE）
15. SWE-bench: Can Language Models Resolve Real-world Github Issues? — Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, Karthik Narasimhan，ICLR 2024，https://proceedings.iclr.cc/paper_files/paper/2024/hash/edac78c3e300629acfe6cbe9ca88fb84-Abstract.html （2,294 问题 / 12 仓库 / Claude 2 仅 1.96%）
16. DataComp: In search of the next generation of multimodal datasets — Samir Yitzhak Gadre 等 33 人，NeurIPS 2023 Datasets and Benchmarks Track，https://proceedings.neurips.cc/paper_files/paper/2023/hash/56332d41d55ad7ad8024aac625881be7-Abstract-Datasets_and_Benchmarks.html （12.8B pool / 38 下游 / 79.2% / +3.7pp）
17. Finding and Understanding Bugs in C Compilers — Xuejun Yang, Yang Chen, Eric Eide, John Regehr，PLDI 2011（Award paper），DOI 10.1145/1993498.1993532，https://www.flux.utah.edu/paper/yang-pldi11 （三年 / 325+ bug / 每个被测编译器都 crash 且静默产生错误代码）
18. ICML 2027 / NeurIPS 2027 / ICLR 2027 社区 deadline 跟踪 — https://www.opencurious.com/ai-conference-deadlines/icml-2027 、https://researchtheta.com/conferences/neurips-2027/ 、https://www.opencurious.com/ai-conference-deadlines/iclr-2027 （均为社区估值，非官方）
