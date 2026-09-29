# 方向 10：Workshop 论文对求职 / 申研有用吗

> 调研时间：2026-09-29（GMT+8）
> 检索工具：WebSearch ×13 + WebFetch ×7（NeurIPS 官方 workshop guidance、workshop 官网、admissions 分析文、CVPR workshop 统计、期刊扩展政策）
> 锚点：阙疑（queyi）——双非本科生、0 影响力、考研初试约 2027-12；本文回答"阙疑应该先投 workshop 还是等主会"

## 核心结论

1. **workshop 论文的价值高度依赖"是否 archival + 是否被索引"，而不是"是否挂了大会议名"**：NeurIPS 官方明文规定 **"All NeurIPS workshop papers are non-archival and therefore do not appear in proceedings"**（不索引、无正式论文集）；而 ICSE 的 LLM4Code、FSE 的 LLMTrust 2026 则**默认 archival 并进入 IEEE Xplore / ACM DL + DBLP**——后者的可引用价值是前者的数量级差异。
2. **对申研，workshop 论文是"信号放大器（signal amplifier）而不是信号本身"**：它放大申请材料里已有的东西（强推荐信、真实研究经历、清晰 SOP），但救不了薄弱的申请；且**虚假陈述（把 workshop 写成主会）的破坏力远大于不列论文**——招生委员"约三秒"就能分辨，且"30 秒搜索"能查到你的论文是否曾从主 track 掉进 workshop。
3. **对阙疑这类"无机构、无导师、单作者"的项目，archival workshop 的边际价值最高**：因为它是唯一一个"低门槛 + 可引用 + 有外部同行评审背书"的通道，能把"我自学做了个东西"升级为"我的工作被同行评审接受并进入 IEEE/ACM 索引"。已有可核实的先例：FVAPPS 的两位作者署名均为 "Unaffiliated"（无机构），论文进入 IEEE 索引。

## 精确数字与案例

### 一、先分清两类 workshop：archival vs non-archival

**（A）NeurIPS 系 workshop：一律 non-archival**

*NeurIPS 2026 Workshops Guidance*（https://neurips.cc/Conferences/2026/WorkshopsGuidance）原文：
> "**All NeurIPS workshop papers are non-archival and therefore do not appear in proceedings.**"

其他硬性条款（均来自该文件）：
- workshop 接收投稿**必须使用 OpenReview** 管理；
- 每篇论文**必须获得 3 份审稿**，每位审稿人**不超过 3 篇**；
- **不允许评审员使用 LLM**（"NeurIPS workshop chairs opted out of the main-track reviewer-LLM experiment"）；
- 组织者及其有个人 COI 的人（如组织者的博士生/博后）**不能向该 workshop 投稿**；
- 提案正文 ≤3 页、组织者信息 ≤2 页、参考文献不限；组织者**超过 8 人**的提案不予接收，任何组织者**最多出现在 2 个**提案中；
- 关键日期：workshop 申请 2026-04-21 开放、2026-06-06 截止、2026-07-11 通知；**建议**的 workshop 论文投稿截止 2026-08-29；**强制**录用/拒稿通知截止 **2026-09-29（不可延长）**；workshop 举办日 **2026-12-11~12（悉尼）、12-12~13（巴黎、亚特兰大）**。

一个具体 workshop 的完整规则可以说明"NeurIPS workshop 到底是什么形态"——*FMTS @ NeurIPS 2026*（https://fmts-workshop.github.io/cfp.html）：
- 投稿**最多 4 页**（不含参考文献与附录），double-blind；
- **3 份审稿**，OpenReview 管理，**审稿人不得使用 LLM**；
- **非 archival**："Per the NeurIPS 2026 workshop guidance, all workshop papers are non-archival and do not appear in proceedings. Accepted papers will be posted on OpenReview and listed on this site. **Presenting here does not preclude later publication at an archival venue.**"
- **并发投稿被允许**："Concurrent submission is permitted. The NeurIPS 2026 main-track handbook permits dual submissions to non-archival workshops."
- **已发表的工作不合格**："Work already published at an ML or related conference, or accepted to the NeurIPS 2026 main conference, should not appear in the workshop."
- **预印本没问题**："Posting to arXiv or a similar server does not affect eligibility."
- **超页或匿名不合规会被 desk-reject without review**。
- **关键一句（对阙疑最有利）**："We will prioritise junior and early-career contributions in spotlight selection."
- 日期：投稿 2026-09-16、通知 2026-09-29（固定不可延）、camera-ready 2026-11-06（暂定）、workshop 2026-12-11~12。

另一个 NeurIPS 2026 workshop（Long Context Foundation Models）写得更直白：
> "**No submission will be indexed nor have archival proceedings.**"

**（B）SE 系 workshop：默认 archival 并进入正式索引**

- **LLM4Code 2025（ICSE 2025 合办）** 的 CFP 原文："All accepted papers by default will appear in the **ICSE 2025 workshop proceedings (i.e., the archival option)**." 同时提供 non-archival 选项（camera-ready 只挂 workshop 网站，**不上 DBLP**）。已确认被 **DBLP 收录**（dblp.org/db/conf/llm4code/llm4code2025）与 **IEEE Xplore 收录**（2025 IEEE/ACM International Workshop on Large Language Models for Code，IEEE 会议论文集编号 11027903）。投稿类型：Research papers **4–8 页含参考文献**、Position papers **1–4 页含参考文献**；double-blind；IEEE 格式；**Best paper awards 最多 10%**。
- **LLMTrust 2026（FSE 2026 合办，2026-07-05/06，Montreal）**：Full papers **8 页含参考文献**（最多 2 页参考文献）；Short papers **5 页**（最多 1 页参考文献）；Extended abstracts **1–5 页**（**APC-free**）。**Proceedings 进入 ACM Digital Library，作为 FSE 2026 Companion Proceedings 的一部分**。日期：投稿 2026-02-19、通知 2026-03-24、camera-ready 2026-04-02。

**（C）CVPR 系 workshop：archival 与 non-archival 混杂，须逐个查**

根据 aiworkshoptracker.com 的统计：**2024–2026 三年共 179 个 CVPR workshop 版次、803 篇录用论文**；CVPR 2024 有 24 个 workshop，CVPR 2025 有 56 个。同一届内部就同时存在 **Proceedings Track / Archival Track** 与 **Non Proceedings / Non Archival Track**，例如 CVPR 2026 的 DriveX（Archival Track）、HOW（Proceedings Track）与 VideoWorldModel（同时有 Proceedings Track 3 篇与 Non Proceedings Track 24 篇）。CVPR 2025 的 workshop 论文可通过 openaccess.thecvf.com 公开下载。**该站点未提供任何 workshop 的投稿数或录用率**。

对照：CVPR 2024 主会收到 **11,532 篇**有效投稿、接收 **2,719 篇**，录用率 **23.6%**。

**（D）ICLR Tiny Papers：已并入 workshop**

ICLR 2025 的官方说明："This year, the Tiny Papers Track has been **integrated into the workshops**!" 其原始目标群体是"under-represented, under-resourced, and budding researchers"。**页数限制、是否 archival、审稿标准、录用率全部下放给各 workshop 自定**（官方原文："These may vary by workshop according to the needs and standards of subcommunities"）。作者可单独申请 ICLR 的参会资助（Financial Assistance），申请 2 月初开放、**2026-03-02 截止**，由 DEI Chairs 评定。

### 二、workshop 录用率：40%–60% vs 主会 20–26%

多方来源给出的量级（均属经验/整理值，非官方统计）：
- NeurIPS workshop 录用率一般落在 **40%–60%**；主会 **20–26%**；Extended abstracts **>60%**（sensazioni.org，2026-05-17）。
- 主赛道 25–30%（3–4 位审稿人 + AC + 多轮 rebuttal）vs 热门 workshop 历史上 **40%–60%+**；有竞争力的 workshop 录用率 **25%** 值得写进 CV（dev.to，2026-05-02）。

**这些数字必须标注为"社区经验值"**——NeurIPS 官方从未公布 workshop 的投稿数与录用率；上述来源也未给出一手统计口径。

**补充：workshop 通道的绝对规模（2025 年 NeurIPS）。** 第三方追踪站 aiworkshoptracker.com 记录：**NeurIPS 2025 共 62 个 workshop、4,401 篇录用论文**（同期主会录用 5,290 篇）。也就是说，**workshop 的录用总量已达主会的 83%**——它不是"边角料"，而是**与主会同一数量级的出版通道**。这对阙疑的含义是：**"workshop 论文不值钱"的判断在绝对数量层面不成立**，真正的差别在于"是否 archival / 是否被索引"（见第一节 A vs B）。但必须诚实标注：**该 62 / 4,401 来自第三方聚合站，未与 NeurIPS 官方核对**，且"4,401 篇"是该站"追踪到的录用论文数"，可能混入 extended abstracts 与 non-archival 条目。

**为什么"62 个 workshop / 4,401 篇"这个数字对阙疑重要**：它意味着**即使主会投稿连续被拒，workshop 通道的容量也远大于单作者能产出的稿件量**——"投不出去"从来不是供给端的问题，而是"选错了通道（non-archival）"或"写不到 4 页的清晰度"的问题。对阙疑这种单作者项目，**真正稀缺的不是投稿机会，而是"值得被同行评审一次"的完整工作**；把 62 个 workshop 当成"简历刷量池"是错误用法，把它当成"用低成本换一次外部评审反馈"才是正确用法。

### 三、申研视角：workshop 论文的真实分量

一篇 2026-05-02 的招生视角分析文（dev.to，作者自称长期与招生委员会教师交流）给出了几个可直接使用的判断：

**判断 1：workshop 论文是"信号放大器，不是信号本身"**
> "a workshop paper is a **signal amplifier, not a signal by itself**. It amplifies whatever else is in your application."

**判断 2：教师约三秒就能分辨主会与 workshop**
> "Faculty can tell the difference between a NeurIPS main track paper and a NeurIPS workshop paper in about **three seconds**."
> "admissions committee members at top programs often **know the workshop organizers personally**. They've attended that workshop."

**判断 3：索引差异是结构性的**
> "Papers in main proceedings get indexed in **Semantic Scholar, ACL Anthology, DBLP**... Workshop papers are often just a PDF on a workshop website or OpenReview. They may not appear in your Semantic Scholar profile at all, or they'll show up with **zero citation count and no venue metadata**."

**两个正面个案（均为一手访谈式转述，非统计数据）**
- **arXiv 引用压倒 workshop**："A preprint you posted in June that has **15 citations by November**... **The workshop paper from the same project... contributed almost nothing to the decision.**"
- **workshop 打开冷邮件**："I've talked to PhD students who said a NeurIPS workshop paper **opened cold emails that had been going unanswered for months**. The work didn't change. The venue did."

**五个反例（这一节对阙疑最有价值）**

1. **虚假陈述陷阱（最致命）**：
   > "A **30-second search** shows acceptance type, scores, reviewer comments, and **whether your paper got desk-rejected from the main track before landing in a workshop**."
   > "I've heard this from multiple faculty members who sit on admissions committees: a misrepresented credential raises a flag that **colors everything else they read about you**."

2. **"唯一论文"问题**：
   > "A workshop paper you genuinely can't defend in depth is worse than listing no paper at all, because it creates an expectation the interview will immediately violate."
   具体表现：被问 "walk me through your methodology choices" 时答不上来（因为只是跑了些实验没主导论证框架）。

3. **付费出版型 workshop（Pay-to-Publish）**，四条同时满足即可剔除：① 没有列出程序委员会（PC）；② 没有公开的录用论文列表；③ 除标准注册费外还收投稿费；④ 论文集不出现在 DBLP 或 Semantic Scholar。
   > "Including it signals you haven't learned to read the terrain of your own field yet, which is a harder deficit to explain away than just having fewer publications."

4. **方向错配**：SOP 说想做语言模型机制可解释性，列的却是工业物联网时序异常检测的 workshop 论文，读起来像"有什么就列什么"。

5. **主题对齐错误导致中性偏负**：一篇 NeurIPS 图神经网络 workshop 论文，对做图结构数据的组是强信号，对 CV 组**几乎中性**。

**"挂靠品牌陷阱"（Co-Located Branding Trap）**：有些 workshop 自称"NeurIPS 2025 Workshop on X"，实际不在官方名单上。验证入口（原文给出）：
- NeurIPS: `neurips.cc/virtual/[year]/workshops`
- ICML: `icml.cc/virtual/[year]/workshops`
- ICLR: `iclr.cc/virtual/[year]/workshops`
- CVPR: `cvpr[year].thecvf.com/WORKSHOPS`
- ACL Anthology: `aclanthology.org`

**正确的 CV 写法（原文建议）**
```
Author Names. "Paper Title." Workshop on Efficient Methods for Large Language Models
at NeurIPS 2025. Non-archival.
```
```
Author Names. "Paper Title." arXiv:2501.XXXXX, 2025.
Accepted to the Workshop on X at ICML 2025 (non-archival).
```
> "Do not write 'ICML 2025 Workshop' without specifying whether it's in PMLR proceedings or not."

**SOP 的弱写法 vs 强写法**
- ❌ "I published a workshop paper on contrastive learning at NeurIPS 2025."（以资历开头）
- ✅ "While exploring cross-modal contrastive representations in a workshop paper at NeurIPS 2025, I ran into a **consistent failure mode on long-tail distributions that existing loss formulations couldn't explain cleanly**. That gap is what pushed me toward the theoretical direction I'm proposing here."（展示一个发现真实问题的大脑）

### 四、引用价值：workshop 论文的长期引用劣势

- *Do conference-journal articles receive more citations? A case study*（ScienceDirect, S1751157724001020, 2024-11）结论：**conference-journal 文章获得的引用显著多于 conference proceedings 文章**——即"先会议后期刊扩展"的版本引用更高。
- 这与 dev.to 的判断一致：non-archival workshop 论文常显示"零引用、无 venue 元数据"。

**但有补救路径：workshop → 期刊扩展**。IOPScience 的官方政策原文：
> "The expectation is that the submission includes **at least 30% new and original material** beyond what has previously been published."

IEEE 会议投稿政策要求作者只投原创、未在他处发表的工作；会议论文扩展为期刊版本时必须（1）恰当引用会议版本；（2）在 cover letter 中清楚声明关系；（3）说明差异。对于 **non-archival** workshop 论文，扩展约束更松（因为原稿本身未进入正式 proceedings）。

### 五、可核实的"独立研究者"先例：FVAPPS

这是本轮调研中找到的**最直接支持阙疑的证据**（已在方向 09 详述，此处从"申研/求职价值"角度重述）：

- 论文：*Proving the Coding Interview: A Benchmark for Formally Verified Code Generation (FVAPPS)*；
- 作者：**Quinn Dougherty、Ronak Mehta**，两人在 ICSE 2025 官方 program 页上的署名单位均为 **"Unaffiliated"（无机构）**；
- 发表：**LLM4Code 2025 workshop（ICSE 2025 合办）**，2025-05-03 14:10–14:20，10 分钟 talk，session chair 为 Chao Peng（ByteDance）；
- **DOI：10.1109/LLM4Code66737.2025.00017** → 进入 IEEE 索引；
- 内容规模：**4,712 个样本**，自称 "the largest formal verification benchmark"，把 APPS 的 Python 单元测试泛化为 **Lean 4 定理**；在 100 个随机样本的 **406 条定理**上，**Sonnet 30%、Gemini 18%**。

这条证据的意义：**"无机构署名"不等于"不能被顶会 workshop 接受并索引"**。它是阙疑"双非本科、无导师、单作者"处境的最强先例。

### 六、对阙疑的四条路径成本/收益对照

| 路径 | 门槛 | 是否 archival/索引 | 对申研/求职价值 | 对阙疑的可行性 |
|---|---|---|---|---|
| NeurIPS workshop（non-archival） | 低（40–60%） | ❌ 不索引、无 proceedings | 中低：能"打开冷邮件"，但简历上必须标 "Non-archival" | 高（4 页即可） |
| LLM4Code @ ICSE（archival 默认） | 中（4–8 页，double-blind，IEEE 格式） | ✅ IEEE Xplore + DBLP | **高**：可写成正式 publication | 高（阙疑的 C++ 验证正对该 workshop 主题） |
| LLMTrust @ FSE（archival） | 中（8 页 full / 5 页 short） | ✅ ACM DL + FSE 2026 Companion | **高** | 高（verification + provenance + auditable 三关键词完全匹配） |
| ICSE / FSE / ASE 主 track | 高（20–25%） | ✅ | 最高 | 中（需 10 页 + artifact） |
| NeurIPS E&D 主 track | 高（约 25%） | ✅ | 最高 | 中高（scope 最匹配，但无 revision 机制） |

## 对阙疑的 3 条具体行动

1. **2026-11 至 2026-12 期间，把阙疑做成一个 8 页 LLMTrust-style Full Paper 投 2027 年的 LLMTrust（FSE 2027 合办）**：理由是该 workshop 的 two-axis 主题（verification + provenance + auditable）与阙疑的"append-only 哈希链 + Merkle checkpoint + 独立对账器"完全同构，且 proceedings 进 ACM DL。行动：(a) 在 `_arch_v46/` 写 `llmtrust_2027_plan.md`，含 8 页大纲（含最多 2 页参考文献）；(b) 用 `data/defect_fixtures/defects.json`（15 条，重注入检出 6/6=100%）作核心结果；(c) 在 `research/13_ai_use_and_authorship.md` 中按 LLMTrust 要求声明 LLM 使用。时间点：2027-01-31 前完成稿件，按 2027-02 中旬的投稿截止（参照 2026 的 02-19）投出。

2. **同时准备一份 4 页 non-archival 版投 NeurIPS 2027 的 workshop，作为"低风险试水"**：NeurIPS workshop 投稿截止建议在 8 月底（2026 年是 08-29），通知强制在 9 月底（2026 年是 09-29），且**允许并发投稿**（"Concurrent submission is permitted"）。行动：把 8 页 LLMTrust 版压成 4 页，删掉全部实现细节只留 claim + 数字 + 一张架构图。**关键纪律**：CV 与 SOP 上一律写全称并明确标注 "Non-archival"（参照上文正确格式），绝不写"NeurIPS 2025 Workshop"这种模糊表述。时间点：2027-07-31 前完成压缩版。

3. **在 2026-12-31 前建一个"venue 真伪核验"流程并落成文件 `_arch_v46/venue_verification.md`**：核验清单四条——① 该 workshop 是否出现在 `neurips.cc/virtual/[year]/workshops`（或 ICML/ICLR/CVPR 对应入口）的官方名单上；② 是否有公开的 Program Committee 名单；③ 是否除注册费外还收投稿费；④ 论文集是否出现在 DBLP 或 Semantic Scholar（可用 `https://dblp.org/search?q=<workshop名>` 直接查）。四条中任何一条不满足就放弃。理由：dev.to 明确指出"把 pay-to-publish workshop 写进简历，表明你还没学会读懂自己领域的地形"。时间点：每次投稿前执行。

## 盲区（诚实标注）

- **Academia StackExchange 的"workshop 论文有什么意义"高赞回答我未能读取**（页面被 Cloudflare 人机验证拦截，返回 "Just a moment..."），因此该问题下的教授/招生委员一手观点**完全没有纳入**。这是本方向最大的信息缺口。
- **NeurIPS 官方从未公布 workshop 的投稿数与录用率**；"40%–60%"来自 sensazioni.org（一个内容农场风格站点，2026-05-17），**无一手统计来源**，只能当作量级参考。dev.to 的"主赛道 25–30% vs 热门 workshop 40–60%+"同样是经验值。
- **dev.to 那篇文章的案例全部是作者自述的访谈式转述**（"I've talked to PhD students..."），**无一个可核验的具名案例**。其中一处表述不严谨——称 workshop 论文可能 "potentially self-submitted"（可能自我提交），这不符合 workshop 仍需经 PC 评审的事实。该文作者身份与招生经验**未核实**。
- **"招生委员约三秒分辨主会 vs workshop"** 是修辞性表述，**不是测量结果**。
- **"15 次引用的预印本压倒同项目 workshop 论文"** 是单一转述，无论文标题、无作者、无时间，**不可作为统计数据使用**。
- **ScienceDirect S1751157724001020 我只读到摘要级结论**（"conference-journal articles receive significantly more citations than conference proceedings articles"），**具体倍数未读取**；且该研究对象是"conference-journal"（会议+期刊联合发表模式），与"workshop vs 主会"并非同一比较。
- **"30% 新内容"规则来自 IOPScience 的期刊政策页**，**不代表 IEEE/ACM 全部期刊**；不同期刊门槛不同（有的要求 30%，有的只要求"substantial new material"并附差异说明）。**我未逐家核对**。
- **CVPR workshop 的 179 个版次 / 803 篇录用论文来自 aiworkshoptracker.com（第三方聚合站）**，**未与 CVF 官方核对**；且该站点未提供任何投稿数或录用率。
- **LLM4Code 2025 与 LLMTrust 2026 的录用率均未公布**（官方页面只有日期与规则）。
- **FVAPPS 的"the largest formal verification benchmark"是论文自述**；"4,712 样本 / 406 定理 / Sonnet 30% / Gemini 18%"来自 ICSE 2025 官方 program 页的摘要，**未读论文全文核实样本构成**。
- **ICLR Tiny Papers 2025 并入 workshop 后的页数/archival/录用率全部"因 workshop 而异"**，官方未给统一值；本方向未逐 workshop 核对。
- **"考研复试 / 国内求职对 workshop 论文的认可度"未查到任何一手数据**（本方向只覆盖了海外申研视角）。这是对阙疑最相关却最缺失的一块：**阙疑作者的主战场是国内考研与国内嵌入式求职，而检索到的全部实证材料都来自海外 ML 申研语境**。
- 本文未涉及中国大陆政治、机构制裁、出口管制等议题；检索中出现的相关页面已主动排除。

## 来源

1. NeurIPS (2026). *Workshops Guidance*（"All NeurIPS workshop papers are non-archival and therefore do not appear in proceedings"、3 份审稿、审稿人禁用 LLM、组织者 COI、关键日期）。https://neurips.cc/Conferences/2026/WorkshopsGuidance
2. FMTS @ NeurIPS 2026. *Call for Papers*（4 页、double-blind、non-archival、3 审稿、允许并发投稿、"Presenting here does not preclude later publication at an archival venue"、优先 junior/early-career）。https://fmts-workshop.github.io/cfp.html
3. Long Context Foundation Models @ NeurIPS 2026（"No submission will be indexed nor have archival proceedings"）。https://longcontextfm.github.io/
4. LLM4Code 2025. *Call for Papers*（默认 archival、4–8 页 research / 1–4 页 position、double-blind、IEEE 格式、best paper ≤10%、non-archival 选项）。https://llm4code.github.io/2025/call/
5. DBLP: LLM4CODE@ICSE 2025（确认索引）。https://dblp.org/db/conf/llm4code/llm4code2025
6. LLMTrust 2026. 官网与 Submission & Proceedings（8 页 full / 5 页 short / 1–5 页 extended abstract；ACM DL FSE 2026 Companion Proceedings；2026-02-19 投稿、2026-03-24 通知）。https://llmtrust2026.github.io/
7. Dougherty, Q., Mehta, R. (2025). *Proving the Coding Interview: A Benchmark for Formally Verified Code Generation (FVAPPS).* LLM4Code 2025 @ ICSE 2025，DOI 10.1109/LLM4Code66737.2025.00017（两位作者署名 Unaffiliated；4,712 样本；406 定理上 Sonnet 30% / Gemini 18%）。https://conf.researchr.org/details/icse-2025/llm4code-2025-papers/21/Proving-the-Coding-Interview-A-Benchmark-for-Formally-Verified-Code-Generation
8. dev.to (2026-05-02). *Do Workshop Papers at NeurIPS/ICML Actually Help Your PhD Application? Here's What Admissions Committees Think.*（signal amplifier、三秒分辨、五个反例、CV/SOP 写法、品牌陷阱核验入口）。https://dev.to/ericwoooo_kr/do-workshop-papers-at-neuripsicml-actually-help-your-phd-application-heres-what-admissions-9dc
9. Sensazioni.org (2026-05-17). *NeurIPS Workshop Acceptance Probability (2024 Rates & Tips)*（workshop 40–60% vs 主会 20–26%、extended abstract >60%、non-archival 为主）。https://sensazioni.org/neurips-workshop-acceptance-probability
10. ICLR (2025). *Call for Tiny Papers 2025*（Tiny Papers 并入 workshop、目标群体、Financial Assistance 3 月 2 日截止、细则因 workshop 而异）。https://iclr.cc/Conferences/2025/CallForTinyPapers
11. AI Workshop Tracker. *CVPR Workshops, Deadlines & Acceptance Rate*（2024–2026 共 179 个 workshop 版次、803 篇录用论文；CVPR 2024 24 个、CVPR 2025 56 个；archival / non-archival track 标注）。https://aiworkshoptracker.com/conference/cvpr/
12. CVPR 2025 Open Access Repository — Workshops（workshop 论文公开下载入口）。https://openaccess.thecvf.com/CVPR2025_workshops/menu
13. ScienceDirect (2024-11). *Do conference-journal articles receive more citations? A case study.* S1751157724001020（会议+期刊版本引用显著高于纯会议版本）。https://www.sciencedirect.com/science/article/abs/pii/S1751157724001020
14. IOPScience Publishing Support. *Expanding a conference proceedings paper for journal publication*（"at least 30% new and original material"）。https://publishingsupport.iopscience.iop.org/questions/expanding-a-cs-proceedings-article-for-journal-publication/
15. NeurIPS (2023-09-12). *Your NeurIPS Workshop was Accepted – Now What?*（full-length papers 进 proceedings、extended abstracts（≤4 页）进 non-proceedings）。https://blog.neurips.cc/2023/09/12/your-neurips-workshop-was-accepted-now-what/
16. AI Workshop Tracker. *NeurIPS 2025 Deadline, Dates & Workshops*（NeurIPS 2025 共 62 个 workshop、4,401 篇录用论文；主会 5,290/21,575 = 24.5%）——**第三方聚合站，未与官方核对**。https://aiworkshoptracker.com/conference/neurips/2025/
