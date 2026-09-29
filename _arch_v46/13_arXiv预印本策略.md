# 方向 13：arXiv 预印本策略

## 核心结论

1. **arXiv 对五大目标会场（NeurIPS/ICLR/ICML/ACL/ICSE）都不构成"双投"或"破坏双盲"，是唯一可以合法拿时间戳的通道**；但时间戳必须在投稿**之前**或**同期**拿到，事后补挂会失去"抢优先权"的意义。
2. **预印本的引用优势有实测数字：+20.2%**（Colavizza 等，2024，约 122,000 篇 PLOS 论文 + PMC 对照组），但同一研究显示"共享代码"**没有**显著引用优势（+4.3% 只出现在共享数据上）；因此 arXiv 的收益来自"早可见"，不来自"附代码"。
3. **2025-10-31 起 arXiv CS 新增体裁闸门**：review/survey 与 position paper 必须先在期刊/会议完成同行评审才能上 arXiv——这直接决定了阙疑论文的体裁写法，写错体裁会在 arXiv 门口被拦而不是在会场被拒。

## 精确数字与案例

### 一、什么时候发：三家会场的原文边界

| 会场 | 原文 | 允许投稿前挂？ | 允许审稿期挂？ |
|---|---|---|---|
| NeurIPS 2026 | "The existence of non-anonymous preprints (on arXiv or other online repositories, personal websites, social media) will not result in rejection." | 是 | 是 |
| ICML 2025/2026 | "Authors are allowed to post versions of their work on preprint servers such as arXiv." | 是 | 是 |
| ICLR 2026 | "Submission of the paper to archival repositories such as arXiv is allowed during the review period." | 是 | 是 |
| ACL/ARR | 自 2024-02-15 取消匿名期，"no anonymity period or limitation on posting or discussing non-anonymous preprints" | 是 | 是 |
| ICSE 2027 | "可在 arXiv 等平台上传预印本，但不得说明该稿已投稿 ICSE 2027；**建议作者推迟到通知后再发布**" | 是 | 是（但不建议） |

四条硬性红线（全部为原文）：

1. **NeurIPS 2026**：预印本若用 NeurIPS 样式，必须选"preprint"选项而非"final"；公开版本**不得**写"Under review at NeurIPS"或类似表述。
2. **NeurIPS 2026**："aggressive advertising of papers under submission may be deemed a violation"——挂着可以，天天宣传不行。
3. **ICML 2025/2026**："under no circumstances should the work be advertised as an ICML submission at any time during the review period"；若在出结果前挂了非匿名版本，提交版本**不得引用它**。
4. **ARR**：提交表单里若勾选具有约束力的"no non-anonymous preprint"，则承诺在 meta-review 发布前不挂预印本，**违反会被 desk reject**。

**结论性配方**：投稿前 1–3 天挂 arXiv v1（拿时间戳），正文与摘要里绝不出现目标会场名称，社媒宣传只用"新预印本"而不用"投稿中"。

### 二、怎么发：endorsement（背书）是第一道门槛

arXiv 官方帮助页原文："arXiv requires that users be endorsed before submitting their first paper to arXiv or a new category." 关键规则：

- **自动背书条件**：需同时满足（a）已**认领**（claimed ownership）合作者提交的论文，（b）邮箱符合机构邮箱标准。arXiv 明确"automatic endorsement is given to authors from known academic institutions and research facilities"，并"encouraged to associate an institutional email address"。
- **若无机构邮箱或未认领论文**，只能找**个人背书**：启动一次投稿 → 收到含 6 位字母数字**背书码**的邮件 → 在摘要页点"Which authors of this paper are endorsers?"找到该领域的合格背书人 → 发背书请求邮件。官方提醒"inappropriate to email large numbers of potential endorsers at once, or to repeatedly email the same endorser"。
- **背书人资格**："Endorsers must have authored a certain number of papers within the *endorsement domain*"，且**只计 3 个月至 5 年前之间提交的论文**；背书人本人须在该领域已获正向背书。
- **最少 1 个正向背书**才能在该类别被认定为已背书；arXiv 保留撤销背书的权利。
- **背书不等于同行评审**：官方原文"The endorsement process is not peer review"，但背书人"should know the person that you endorse or you should see the paper"，且被发来审阅的稿件须**保密**。

**对阙疑的直接影响**：作者是双非本科生、0 影响力、无 arXiv 提交历史 → 极可能触发背书要求。可用的两条路：（a）用学校邮箱（`.edu.cn`）注册并认领已有论文；（b）找一位该领域活跃的 arXiv 作者（例如引用过的 C++/验证方向论文作者）请求背书。**这一步必须在计划挂 v1 的至少 2 周前启动**，因为背书请求可能无人响应。

### 三、发出去要多久：公告时间表（精确到小时）

arXiv 的公告不是即时生效。官方公告时间表（**美东时间**）：

| 投稿收到时间（美东） | 公告时间（美东） | 订阅邮件送达 |
|---|---|---|
| 周一 14:00 – 周二 14:00 | 周二 20:00 | 周二夜 / 周三早 |
| 周二 14:00 – 周三 14:00 | 周三 20:00 | 周三夜 / 周四早 |
| 周三 14:00 – 周四 14:00 | 周四 20:00 | 周四夜 / 周五早 |
| 周四 14:00 – 周五 14:00 | **周日 20:00** | 周日夜 / 周一早 |
| 周五 14:00 – 周一 14:00 | 周一 20:00 | 周一夜 / 周二早 |

另有三条硬事实：

- **周五、周六不公告**："Submissions to arXiv are typically posted publicly Sunday through Thursday, with no announcements Friday or Saturday."
- **质量检查耗时**："Quality assurance checks can take between one to four days to resolve, sometimes longer."
- **arXiv ID 无法提前获得、无法倒填**："It is not possible to generate or to be provided with the arXiv identifier or DOI in advance... The arXiv identifier cannot be back-dated, so identifiers will be assigned in the month of first announcement." 这意味着**投稿月份可能不等于首次公告月份**，引用年份会漂。

实操推论：如果目标是 2027-05-04（NeurIPS 2027 E&D 摘要截稿，按 2026 节奏外推）拿时间戳，最晚应在 **2027-04-28（周三）14:00 ET 前**提交，以确保 4 月内公告；若拖到周四 14:00 之后，会直接滑到周日甚至下周一公告。

### 四、许可证：选错不可改

arXiv 提供 6 种许可证，官方原文明确"**The license chosen is irrevocable and cannot be changed**"（不同版本可以不同）。选项与后果：

| 许可证 | 允许商业使用 | 允许改作 | 备注 |
|---|---|---|---|
| CC BY 4.0 | 是 | 是 | "Many publishers allow preprints to be deposited with a CC BY license" |
| CC BY-SA 4.0 | 是 | 是（须同许可） | — |
| CC BY-NC-SA 4.0 | 否 | 是（须同许可） | — |
| CC BY-NC-ND 4.0 | 否 | 否 | "Many publishers allow 'accepted manuscripts' to be deposited with a CC BY-NC-ND license, but there may be an embargo period" |
| **arXiv perpetual, non-exclusive license 1.0** | — | — | "gives limited rights to arXiv to distribute the article, and also limits re-use of any type from other entities or individuals" |
| CC Zero | 是 | 是 | "you will no longer control the article's copyright... conflicts with many publishers' requirements" |

**元数据许可证**：所有 arXiv 元数据适用 CC0 1.0 公共领域贡献。
**版权声明**：带出版商版权声明、禁止或妨碍 arXiv 再分发的 PDF 会被拒收。

**给阙疑的建议**：若不确定未来投哪个期刊/会议，选**最保守**的 arXiv perpetual non-exclusive license（这也是中文社区常见的"不影响后续投稿"建议）；若确定走 NeurIPS（非开放获取期刊），CC BY 4.0 也可接受。**不要选 CC Zero**（丧失版权控制）。

### 五、版本管理：每次替换都产生一个永久版本

官方原文："arXiv is intended as a historical collection of research works. Once made public, each version of a work is considered a permanent part of the scientific record and **may not be removed**." 每次 replace 或 withdraw 都会**版本号 +1**。

arXiv 明确列出"**要求用版本号而非新建 ID**"的情形：

- **出版流程各阶段**（submitted / revised / accepted / published version）——包括期刊、会议各自的版本记录与 DOI；
- 相关工作的不同内容（补充材料、勘误、扩展版、短版、完整版）；
- **著名猜想的多次尝试**（即使内容完全不同）；
- **拆分与合并**（长文拆两篇：用其中一篇 replace 旧长文，另一篇新建 ID；两篇短文合并：用其中一篇 replace 成长文，另一篇 withdraw 并注明被长文取代）；
- **翻译**（同一 ID 的不同语言版本）；
- **Living review / 年度更新**；
- **Comment 与 Reply to Comment**（arXiv 为每个 Comment 和 Reply 分配一个 ID，后续讨论只能通过 replace 产生版本）。

**引用规范**：可用带版本号的完整标识符 `arXiv:YYMM.NNNNNvX`；也可在 Comments 元数据里描述各版本（官方示例："For the longer conference version see: arXiv:YYMM.NNNNNvv1. For the shortened summary see arXiv:YYMM.NNNNNvv2, for the journal version that includes extended data in the appendix see arXiv:YYMM.NNNNNv3"）。

**撤稿的代价**：withdrawal 会产生一个**不含全文链接**的新版本，"Previous versions are still accessible in the version history"。即"撤了"也删不掉——Academia StackExchange 上有一条 2024-02-13 的提问"Found significant flaw in my arXiv version paper: what should I do?"，回答直指"Anyone following up on the citations or linkbacks to your paper's arXiv page will see that your paper was withdrawn"。**结论：发之前必须自审到"能承受被永久引用"，而不是"发出去再说"。**

### 六、预印本的真实收益：+20.2%

Colavizza、Cadwallader、LaFlamme、Dozot、Lecorney、Rappo、Hrynaszkiewicz（2024，"An analysis of the effects of sharing research data, code, and preprints on citations"，arXiv:2404.16171，正式版发表于 PLOS ONE，DOI 10.1371/journal.pone.0311493，2024-12-10）：

- 数据：PLOS 与 DataSeer 合作生产的 Open Science Indicators 数据集，覆盖 **PLOS 2018–2023 全部出版物** + 从 PMC Open Access Subset 抽样的对照组，**合计约 122,000 篇**。
- 方法：计算论文级与作者级引用指标，用一组宽泛的控制变量隔离 Open Science 实践对引用数的效应。
- 结果：
  - **早期以预印本形式发布 → 平均 +20.2% 引用优势**（"a significant positive citation advantage of about 20.2% on average"）；
  - **在在线仓库共享数据 → +4.3%**（"smaller yet still positive"）；
  - **共享代码 → 未发现显著引用优势**（"we do not find a significant citation advantage for sharing code"）。
- 作者自述局限："Further research is needed on additional or alternative measures of impact beyond citations."

**对阙疑的解读**：这条数字支持"先挂 arXiv"（+20.2%），但**不支持**"把代码开源就能涨引用"。代码开源对阙疑的价值在别处——NeurIPS E&D 的**提交门槛**（不公开代码直接 desk reject）和 ICSE 的 artifact 徽章，不在引用。

### 七、预印本的真实风险

1. **被抢（scooping）**：arXiv 博客与年度报告都记录 2025 年投稿激增；2025 年度报告称"arXiv now hosts more than 2.9 million scholarly articles in eight subject areas"，并直言"arXiv has seen a surge in lower-quality submissions"。中文二手来源（知乎 2025-12-20）称 2024 年新增投稿 24.4 万篇、2025 年新增 28.4 万篇，同比 +17%——**该数字未核实官方报告原文**（arXiv 官网首页另一处写"nearly 2.4 million scholarly articles"，与 2.9 million 冲突，属不同时点口径）。
2. **"同期工作"规则会削弱优先权主张**：NeurIPS 2026 Handbook 原文"For the purpose of the reviewing process, papers that appeared online after **March 1st, 2026** will generally be considered 'contemporaneous'"，即**不会**因与同期工作比较而被拒；但"Submissions that are very similar to contemporaneous work will undergo additional scrutiny to prevent cases of plagiarism and missing credit to prior work"。**这意味着：早挂 arXiv 能保护你不被指控抄袭，但不能阻止别人在同一年做同样的事。**
3. **索引延迟会低估早期引用**：一项被称作"lag state"的分析（The Neural Feed 转述，2026-03-28）指出，新发表且正在被引用的论文，其**自身参考文献**尚未被 Semantic Scholar / AI2 等索引摄入并连接，导致这些论文在引用图里表现为"孤立或低连通节点"；该偏差**恰好集中在最新、被引最快的 frontier 研究**上，会扭曲图嵌入、基于图的检索与 RAG 系统。原文称该研究记录在一份含 **16 条以上条目**的 live research journal 中。**该来源为二手转述，未核实原始论文。**
4. **索引时延的具体量级**：第三方博客（citepal，2025-12-21）称 Google Scholar 收录引用需 **24–48 小时**，Scopus 最长约 **1 个月**。**二手来源，未核实。**
5. **体裁闸门**：arXiv CS 自 2025-10-31 起要求 review/survey 与 position paper 必须先在期刊/会议过同行评审并附 DOI 证据，否则"likely to be rejected and not appear on arXiv"；workshop 评审**不算数**。

### 八、把策略压成一句话

**投稿前 1–3 天挂 arXiv v1 拿时间戳；用机构邮箱提前解决背书；许可证选最保守的 arXiv perpetual non-exclusive；正文和社媒绝不提目标会场名；把"是否会被永久引用"当作发帖前的自检标准。**

### 九、背书环节的三个易踩坑点

1. **背书域（endorsement domain）不等于学科分类**。官方原文："most high-level subject areas (e.g., hep-th, cond-mat, q-bio) are currently endorsement domains, with the notable exception of physics, in which individual subject classes are endorsement domains"。即背书按"域"计，找背书人应找**同一背书域**内的作者，而不是"方向看起来相近"的任何人。
2. **背书人只算 3 个月至 5 年前提交的论文**。官方原文："we only count papers that have been submitted between three months and five years ago"。这意味着刚毕业、5 年以上没发过 arXiv 的作者**可能已丧失背书资格**；反过来，找"最近 5 年内活跃"的人更稳。
3. **背书结果对双方是隐私，但作者可推断**。官方原文："The fact that you have personally endorsed or not endorsed a person... is private between you and the arXiv administrators"，"although under certain circumstances an author might be able to infer your action"。官方明确禁止一次给大量人发请求，也禁止反复骚扰同一人。

### 十、公告时间表的边界情形（决定"抢时间戳"的成败）

除周一至周五的常规档，还有四条边界规则必须知道：

- **周四 14:00 ET 之后提交 = 周日 20:00 公告**。这是最容易被忽视的"3 天空档"：周四 14:00–周五 14:00 提交的论文要等到**周日**才公开。对抢优先权而言，周四下午是最坏的提交时点。
- **周五 14:00 – 周一 14:00 提交 = 周一 20:00 公告**。周末提交反而只等约 3 天，比周四下午提交更划算。
- **质量检查可能延长 1–4 天甚至更久**。官方原文："Quality assurance checks can take between one to four days to resolve, sometimes longer"。若检查出问题会邮件通知、公告顺延，而 arXiv ID **不能倒填**，因此"投稿月份"与"公告月份"可能不同，引用年份会漂。
- **延期邮件（deferred mailing）**：arXiv 会因本地节日或临时原因推迟公告。2026 年的节日清单为 1/1、1/19、6/19、7/3、9/7、11/26、12/25、12/29、12/31——**跨年提交要特别小心**，12/25 至 12/31 之间有 4 个延期日，公告可能整体后移到次年 1 月，arXiv ID 的月份随之改变。

### 十一、Colavizza 研究的边界：能推广到什么程度

该研究样本是 **PLOS 2018–2023 全部出版物 + PMC Open Access Subset 抽样**，约 **122,000 篇**，领域以生命科学与医学为主。推广到计算机科学/软件工程需要谨慎：

- **可推广的部分**：预印本效应（+20.2%）的机制是"提前可见 → 更早被引用"，这在 CS 里同样成立，且 CS 的 arXiv 使用率极高（ICLR/NeurIPS 论文绝大多数有 arXiv 版本）。
- **需谨慎的部分**：该研究**未发现共享代码的引用优势**，但 CS 领域 GitHub 仓库的效应另有独立研究支持（Kang 等 2023，+20% 月引用率，样本 19,109 篇 ML 论文，见方向 14）。两者不矛盾——PLOS 语境下的"共享代码"是作为论文附件上传，CS 语境下的"GitHub 仓库"是可运行、可被 fork 的独立工程。
- **对阙疑的正确解读**：arXiv 的 +20.2% 与 GitHub 仓库的 +20%/月 是**两条独立红利**，不能用"共享代码无效"去否定建仓库的价值；但也不能拿 PLOS 的数字去承诺 CS 场景下的确切涨幅。

## 对阙疑的 3 条具体行动

1. **立刻（2026-10 内）解决 arXiv 背书资格，别等到投稿前。** 行动：用学校邮箱注册 arXiv，执行官方"claim ownership"流程（需 paper password 或 request ownership），把已投/已发表的任何论文认领；若无法获得机构邮箱自动背书，按官方流程走"启动投稿 → 拿 6 位背书码 → 在摘要页找'Which authors of this paper are endorsers?'"的路径，联系 2–3 位引用过的 C++/程序验证方向作者。验收标准：arXiv 账号状态显示 cs.SE（或 cs.PL）类别已获背书。记录到 `_arch_v46/arxiv_checklist.md`。
2. **写死"arXiv v1 发布 SOP"并做一次 dry-run。** 在 `_arch_v46/arxiv_checklist.md` 固化 6 步：①体裁自检（非 survey/position，依据 arXiv 2025-10-31 政策）；②许可证选择（默认 arXiv perpetual non-exclusive 1.0，禁用 CC Zero）；③提交时间（**周三 14:00 ET 前**，避开周四 14:00 后的周日公告空档）；④正文扫描 `grep -niE "under review|submitted to|neurips|iclr|icml" paper_v0.3.tex` 必须 0 命中；⑤Comments 元数据写清版本计划；⑥发布后 24 小时内核对是否已公告。**时间点：2027-04-20 前完成 dry-run，2027-04-28 前实发。**
3. **为"撤稿不可逆"准备一份预发布自审清单。** 依据 arXiv 原文"each version... may not be removed"，在 `_arch_v46/arxiv_checklist.md` 增加"发前 12 项自审"：四态判决定义无歧义、holdout 30 样本标签（真错 17 / 对照 9 / unknown 4）与检出率 66.7%（10/15 可测）口径一致、外部 corpus 40 条分层（A 54.2% / B 12.5% / C 0%）与 43.8% 总检出率可复算、缺陷夹具 15 条与重注入 6/6=100% 可复算、变异测试 97.3%/81.5% 已标注"不可当缺陷检测率"、反事实算子 P=R=F1=0 已登记为待修。每项需在仓库里有对应文件路径。**时间点：2027-04-15 前逐项签字。**

## 盲区（诚实标注）

- **arXiv 官方 2025 年报的精确投稿数与下载数**：官方 PDF（https://info.arxiv.org/about/reports/2025_arXiv_annual_report.pdf ）未能以文本方式读取（PDF 抓取工具在本环境下不可用），正文只采信了检索摘要中的"more than 2.9 million scholarly articles"与"a surge in lower-quality submissions"两句，**具体年度投稿数、下载数未核实**。
- **"2024 年 24.4 万篇、2025 年 28.4 万篇、+17%"**：仅见知乎二手转述，**未核实**。
- **arXiv 总文章数 2.4M vs 2.9M**：官网首页写"nearly 2.4 million"，2025 年报摘要写"more than 2.9 million"，**两处口径冲突，未核实**（可能是不同时点或不同统计范围）。
- **Colavizza 等论文的 PDF 正文**：本环境无法读取 PDF，正文数字（+20.2% / +4.3%）来自 arXiv 摘要页 verbatim 引用，**未逐字核对正文表格**。
- **"lag state" 分析**：仅见 The Neural Feed（2026-03-28）二手转述，**未找到原始论文或作者**，故未写入"来源"清单。
- **Google Scholar 24–48 小时 / Scopus 1 个月**：来自 citepal 博客，**二手，未核实**。
- **endorsement 2026-01-21 更新的具体改动内容**：只读到博客标题与"Authors who were previously endorsed to submit to a particular category will still be endorsed in that category"，**完整改动条款未核实**。
- **NeurIPS 2027 的 contemporaneous 截止日**：2026 是 3 月 1 日，2027 未公布，正文按"每年 3 月 1 日"外推，**须在 2026-12 核实**。

## 来源

1. arXiv info, "The arXiv endorsement system" — https://info.arxiv.org/help/endorsement.html （2026）
2. arXiv blog, "Attention Authors: updated endorsement policy" — https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy/ （2026-01-21）
3. arXiv info, "Availability of submissions"（公告时间表、质量检查 1–4 天、ID 不可倒填） — https://info.arxiv.org/help/availability.html （2026）
4. arXiv info, "Submission Version Availability"（版本永久、拆分合并、翻译、Comment 规则） — https://info.arxiv.org/help/versions.html （2026）
5. arXiv info, "arXiv License Information"（6 种许可证、不可更改、元数据 CC0） — https://info.arxiv.org/help/license/index.html （2026）
6. Giovanni Colavizza, Lauren Cadwallader, Marcel LaFlamme, Grégory Dozot, Stéphane Lecorney, Daniel Rappo, Iain Hrynaszkiewicz, "An analysis of the effects of sharing research data, code, and preprints on citations" — arXiv:2404.16171（v2, 2024-09-03）；正式版 PLOS ONE, DOI 10.1371/journal.pone.0311493（2024-12-10）
7. NeurIPS 2026 Main Track Handbook（Preprints 段与 Contemporaneous Work 段） — https://neurips.cc/Conferences/2026/MainTrackHandbook （2026）
8. ICML 2025 Call For Papers（arXiv 允许 + 宣传禁令） — https://icml.cc/Conferences/2025/CallForPapers （2025）
9. ICML 2026 Peer Review FAQ — https://icml.cc/Conferences/2026/PeerReviewFAQ （2026）
10. ICLR 2026 Author Guide（arXiv 不破坏双盲、引用须第三人称） — https://iclr.cc/Conferences/2026/AuthorGuide （2025）
11. ACL Rolling Review Call for Papers（2024-02-15 起无匿名期；binding "no non-anonymous preprint" 选项） — https://aclrollingreview.org/cfp （2024–2025）
12. ACL Admin Wiki, "Update to Anonymity Policy" — https://aclrollingreview.org/anonymity/ （2024-01-15）
13. arXiv blog, "Attention Authors: Updated Practice for Review Articles and Position Papers in arXiv CS Category" — https://blog.arxiv.org/2025/10/31/attention-authors-updated-practice-for-review-articles-and-position-papers-in-arxiv-cs-category/ （2025-10-31）
14. arXiv 2025 Annual Report（封面摘要） — https://info.arxiv.org/about/reports/2025_arXiv_annual_report.pdf （2026-08-21）
15. Academia StackExchange, "Found significant flaw in my arXiv version paper: what should I do?" — https://academia.stackexchange.com/questions/206703/ （2024-02-13）
16. ICSE 2027 Research Track（预印本建议推迟至通知后） — https://conf.researchr.org/track/icse-2027/icse-2027-research-track （2026）
17. arXiv info, "Withdrawing a submission" — https://info.arxiv.org/help/withdraw.html （2026）
