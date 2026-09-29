# 方向 07：NeurIPS desk reject 常见原因

> 调研时间：2026-09-29（GMT+8）
> 检索工具：WebSearch ×11 + WebFetch ×8（NeurIPS 官方 Handbook / CFP / Checklist / Reviewer Guidelines / 官方 blog / 第三方审计）
> 锚点：阙疑（queyi）——单作者、无机构背书、0 影响力，desk reject 是**最不可承受的失败模式**（连评审反馈都拿不到）

## 核心结论

1. **NeurIPS 主 track handbook 里明确写出"desk reject / 直接拒稿"的只有四类：格式或页数违规、匿名性违规、重复投稿、OpenReview 作者档案未更新**；checklist 缺失、作者变更、LLM 使用、arXiv 预印本这四类**没有**被 handbook 单独写成 desk reject 条款（arXiv 预印本反而被明确写成"不会导致拒稿"）。
2. **2026 周期新增了两个真实存在、但条款文字尚未完全落进 handbook 的 desk reject 通道**：一是"幻觉引用"（≥2 条即可能被拒，NeurIPS 2026 一位 AC 公开说 8 篇里 5 篇命中），二是 E&D track 的 **Croissant 元数据缺失/占位文本**（"Non-compliance justifies the desk rejection of the paper"）。
3. **最极端的执行案例是 NeurIPS 2026 Position Paper Track 用 Pangram AI 检测器一次性 desk reject 178 篇（18.4%），且无申诉通道**——这条对"单作者、非英语母语、由 LLM 辅助润色"的阙疑构成直接风险。

## 精确数字与案例

### 一、handbook 原文逐条：四类明确写出的 desk reject

以下全部摘自 *NeurIPS 2026 Main Track Handbook*（https://neurips.cc/Conferences/2026/MainTrackHandbook）。

**（1）页数与格式**
> "The main text of a submitted paper is limited to **nine content pages**, including all figures and tables. Additional pages containing references, optional technical appendices and mandatory paper checklist do not count as content pages. If your submission is accepted, you will be allowed an additional content page for the camera-ready version. The maximum file size is **50MB**."

> "Submissions that violate the NeurIPS style (e.g., by decreasing margins or font sizes) or page limits **may be desk rejected**. Papers may also be rejected without consideration of their merits if they fail to meet the submission requirements."

模板方面：**"This is the only template we will accept (note: Microsoft Word template has been discontinued)"**。也就是说 2026 年起 Word 模板已停用，必须用指定 LaTeX style file。

对"轻微 vs 重大"的官方口径（审稿人 FAQ）：
> "Do not worry about minor violations of the required format e.g., papers that exceed the page limit by a few lines or have an incorrect order of the checklist, references, and supplementary materials, but **report any major violations to your AC**."

**（2）匿名性**
> "All submissions must be anonymized and may not contain any identifying information that may violate the double-blind reviewing policy. This policy applies to any supplementary or linked material as well, **including code**... Please do not include acknowledgments at submission time... **Papers violating this policy will be desk rejected.**"

对阙疑的直接含义：`web/verify.html`、`tools/gate_engine.py`、`README.md` 里若出现"合肥""ASUS""个人 GitHub 账号"等，都属匿名性违规。

**（3）重复投稿（Dual Submissions）**
> "The reviewing process will treat any other archival submission by an overlapping set of authors as prior work (dual submissions to **nonarchival workshops** are permitted)... This includes '**thin slicing**' by submitting two or more very similar papers to NeurIPS in hopes one will be accepted, as well as **dual submissions of the same paper to both the main and E&D track**... **Failure to comply with the dual submission policy is grounds for desk rejection during any point of the reviewing and program building process.**"

关键点：**主 track 与 E&D track 之间互投同一篇 = 直接 desk reject**。阙疑只能选一个。

**（4）作者档案未更新**
> "Because profiles are used to inform conflicts of interest, a profile that has not been appropriately updated **risks desk rejection (for authors)** and sanctions (for reviewers)."

另外（作者变更条款，**未写 desk reject**）：
> "All author names must be entered into the submission form by the **abstract submission deadline**. After this, no changes can be made, except to the author order. If/when your paper is accepted, but we will not allow additions nor removal of authors."

### 二、checklist：16 条，缺失即 desk reject

*NeurIPS Paper Checklist Guidelines*（https://neurips.cc/public/guides/PaperChecklist）给出**逐字条款**：

1. **Claims**："Do the main claims made in the abstract and introduction accurately reflect the paper's contributions and scope?"
2. **Limitations**："The authors are encouraged to create a separate 'Limitations' section..."（**NA = 论文没有局限性；No = 有局限性但未讨论**）
3. **Theory, Assumptions and Proofs**："If you are including theoretical results, did you state the full set of assumptions of all theoretical results, and did you include complete proofs of all theoretical results?"
4. **Experimental Result Reproducibility**："If the contribution is a dataset or model, what steps did you take to make your results reproducible or verifiable?"
5. **Open Access to Data and Code**："If you ran experiments, did you include the code, data, and instructions needed to reproduce the main experimental results (either in the supplemental material or as a URL)?"
6. **Experimental Setting/Details**："If you ran experiments, did you specify all the training details (e.g., data splits, hyperparameters, how they were chosen)?"
7. **Experiment Statistical Significance**："Does the paper report error bars suitably and correctly defined or other appropriate information about the statistical significance of the experiments?"
8. **Experiments Compute Resource**："For each experiment, does the paper provide sufficient information on the computer resources (type of compute workers, memory, time of execution) needed to reproduce the experiments?"
9. **Code Of Ethics**："Have you read the NeurIPS Code of Ethics and ensured that your research conforms to it?"
10. **Broader Impacts**："If appropriate for the scope and focus of your paper, did you discuss potential negative societal impacts of your work?"
11. **Safeguards**："Do you have safeguards in place for responsible release of models with a high risk for misuse (e.g., pretrained language models)?"
12. **Licenses**："If you are using existing assets (e.g., code, data, models), did you cite the creators and respect the license and terms of use?"
13. **Assets**："If you are releasing new assets, did you document them and provide these details alongside the assets?"
14. **Crowdsourcing and Research with Human Subjects**：必须附上给参与者的完整指示文本与截图、报酬细节；**报酬不得低于其所在国最低工资**。
15. **IRB Approvals**："Did you describe any potential participant risks and obtain Institutional Review Board (IRB) approvals...?"
16. **Declaration of LLM usage**："Does the paper describe the usage of LLMs if it is an important, original, or non-standard component of the core methods in this research?"

**四条硬规则**：
- checklist 已内嵌在 LaTeX 样式文件中，**不要删除**；
- 原文：**"The papers not including the checklist will be desk rejected."**
- checklist **不计入页数限制**（"The checklist does NOT count towards the page limit."）；
- **"In general, answering 'no' or 'n/a' is not grounds for rejection."**——回答"no"不是拒稿理由，但缺失 checklist 本身是。
- 提交 PDF 的顺序必须是：**论文 → 可选技术附录 → checklist**（即 checklist 在参考文献之后）。

### 三、伦理与 Code of Conduct 通道

Handbook 原文：
> "Reviewers and ACs may flag submissions for potential violations to the NeurIPS Code of Ethics... **in extreme cases papers may be rejected by the program chairs on ethical grounds, regardless of scientific quality or contribution.**"

> "NeurIPS reserves the right to reject the presentation of scientific works that violate the Code of Ethics... The penalty for violations may include immediate removal from the reviewing system, revoking the paper's publication status, sharing of identities with sister conferences, informing the colluding parties home institutions, and/or sanctions to future NeurIPS."

注意用词：这里是 "rejected by the program chairs on ethical grounds"，**没有**用 "desk reject" 字样，但性质上是不经科学评审的直接拒稿。

LLM 相关（**未写 desk reject**，但操纵审稿被定性为严格禁止）：
> "agents and LLMs cannot be authors."
> "attempts at prompt injections as well as other attempts to manipulate reviewing is strictly prohibited."

审稿人侧制裁条款（*NeurIPS 2025 Reviewer Guidelines* 与 GitHub 镜像的官方口径）：
> "**Desk Rejection Sanction: Grossly negligent reviews can result in desk rejection of reviewer's own papers.**"

**2025 年实际执行了 11 例**——NeurIPS 2025 PC Chair 博客原文：
> "This included situations like the **11 unfortunate cases** where one of the co-authors are confirmed to be grossly negligent in their reviews under our new responsible reviewing policies."

### 四、arXiv 预印本：官方明确"不拒稿"

Handbook 原文：
> "The existence of non-anonymous preprints (on arXiv or other online repositories, personal websites, social media) **will not result in rejection**... Authors may submit anonymized work to NeurIPS that is already available as a preprint (e.g., on arXiv) **without citing it**."

> "Note: While having a nonanonymized preprint alone is not a violation of the double-blind reviewing policy, **aggressive advertising of papers under submission may be deemed a violation.**"

即：**发 arXiv 安全，但在社交媒体上"激进推广在投论文"可能被判违规**。对阙疑的推论：不要在 2027-05 投稿后于小红书/知乎宣传"我正在投 NeurIPS"。

### 五、2026 新增通道 ①：幻觉引用（hallucinated citations）

NeurIPS 2026 Handbook 唯一一句相关表述：
> "there have been many cases of hallucinated citations in literature review, which **violates the NeurIPS Code of Conduct**."

实际执行门槛来自 NeurIPS 2026 一位 Area Chair **Danish Pruthi** 的公开说明（属非正式记录）：
> "**5 out of 8 submissions have 2+ hallucinated references and will likely be desk rejected**"
> "NeurIPS is quite liberal in how they define hallucinations. One of the remaining three papers has a fabricated citation, but that's not enough for desk-rejection"

即 **"≥2 条幻觉引用"触发 desk reject**；1 条编造引用不足以致命。

四家会议的对比（第三方审计整理）：
- **ICLR 2026**：程序主席说明系统"automatically extracted references from a given submission and checked them against multiple standard bibliographic databases and a standard web search"；被标记的引用需经**三轮人工复核**（先 AC、后 PC 主席本人）才真正 desk reject，并设申诉渠道。官方承认该系统 **"had a significant false positive rate"**（例如会把作者自行翻译成英文的非英语标题论文标记出来），并称这"partially explains the relatively high desk rejection rate at this year's ICLR"。
- **ACL 2026**：程序主席声明**超过 100 篇已录用论文**因引用不存在的文献被 desk reject；每条标记须经 PC 主席与 SAC 复核；**政策中途撤回**，受影响论文改为走正常重新投稿流程。
- **ICML 2026**：Peer Review Ethics 页面将 "hallucinated references" 明确列为单篇投稿 desk reject 的理由。

量化审计（arXiv:2607.00738，48,095 篇已录用论文、260 万条提取引用，覆盖 ICLR/ICML/NeurIPS/USENIX Security，2021–2026）：

| 会议（2025） | ≥1 条幻觉引用 | ≥2 条幻觉引用 |
|---|---|---|
| ICLR | 18.7% | 1.9% |
| ICML | 23.3% | 3.4% |
| **NeurIPS** | **26.2%** | **5.1%** |
| USENIX Security | 34.9% | 4.8% |

即按"≥2 条即拒"门槛，**约每 20 篇已录用 NeurIPS 论文中就有 1 篇（5.1%）**在本周期会被 desk reject。

**最关键的发现：同行评审几乎抓不到**。受影响论文与干净论文的评审得分差异——ICLR **+0.02**、ICML **+0.005**、NeurIPS **+0.04**，统计上等于零噪音；且 Poster / Spotlight / Oral 各层级受影响比例几乎相同。**这意味着唯一有效的防线是作者自查，不是"评审会帮我兜住"。**

具名案例（GPTZero 对 ICLR 2026 约 20,000 篇投稿中的 300 篇运行检测，发现 50+ 条幻觉引用）：
- **"MixtureVitae"**：一条引用的前三位作者与真实论文吻合，但其余 7 位作者根本不在真实论文上；
- **"TamperTok"**：引用指向真实存在的论文，但整个作者列表全错；
- **AI 辅助医疗分诊投稿**：一条参考文献完整内容为 "[3] K. Arnold, J. Smith, and A. Doe"——虚构作者列表配虚构期刊（查询 Crossref API 作者组合 "K. Arnold J. Smith A. Doe" 返回 1,095,080 条兜底结果，最高匹配是一条标题为 "Sample thing"、作者为 "Jane Smith" 与 "John Doe" 的测试/占位预印本）。

三篇被标记的论文**评审得分均为 8.0 分**——再次说明 desk reject 与论文质量无关。

### 六、2026 新增通道 ②：E&D track 的 Croissant 元数据

*NeurIPS 2026 E&D Track Call for Papers*（https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets）与 *E&D 2026 Reviewing Guidelines* 给出：
- **Accessibility**："Datasets and code should be available and accessible to all reviewers, ACs, and SACs at the time of submission, and without a personal request to the PI. Code should be documented and executable. **Non-compliance justifies the desk rejection of the paper.**"
- **Croissant 强制**：数据集作者必须用 Croissant machine-readable format 记录数据集，并在 OpenReview 提交时附上 Croissant 文件；2026 年起**同时要求 core 字段与 Responsible AI (RAI) 字段**。
- 审稿人指引中明确：**"Empty or placeholder text should be flagged to your AC and may be desk-rejected."**
- **工具类无代码**："No code = reject unless a convincing justification is provided"（属强制性检查）。
- 格式违规："are subject to desk rejection and we ask that you report to your AC."

注意：**阙疑不是数据集论文**，这条对阙疑的直接影响较小，但间接影响大——如果阙疑把 `data/holdout/`、`data/external_corpus/`、`data/defect_fixtures/` 作为"release 的新资产"声明，就会被拉进 Croissant 的强制要求。**最安全的做法是不要在投稿中声明"释放新数据集"，而只声明"提供可复现的评估协议与夹具"。**

### 七、2026 最极端的执行案例：Pangram AI 检测器

*NeurIPS 2026 Position Paper Track* 的实际执行（来自 CASRAI 2026-07-23 的整理，数据源为 track chairs 在 NeurIPS 官方 blog 的公开说明）：
- Track 收到约 **969–971** 篇投稿，**全部**跑 Pangram（版本 3.3.2）；
- 基于得分 **desk reject 178 篇（18.4%），无申诉通道**；
- 另有 **123 篇（12.7%）** 进入有条件审查（须在 2026-06-15 前提交版本历史/文档检查点证明人类写作）；
- Pangram 默认窗口（每段约 250–350 词）在首轮把 **42.7%** 的投稿标为 90–100% AI 概率，其中 **273 篇（约 28.2%）** 拿到满分 100%；换用更窄的 **100 词 "medium" 窗口**后，该比例降到 **12.7%**；
- Track chairs 为 Alex Lu、Seth Lazar、David Rugamer，assistant chairs 为 Stanley Hua、Kate Metcalf；
- 争议点：**窗口大小一个参数造成约 30 个百分点的波动**；Pangram 自报假阳性率低于 0.1%，但未独立同行评审；
- 相关背景：2023 年 Stanford 研究（Liang et al., *Patterns*）发现 GPT 检测器在非英语母语者写的 TOEFL 作文上平均假阳性率 **61.3%**。

对阙疑的含义极其直接：**阙疑作者是中文母语者、论文若经 LLM 润色，处于该检测器的最高风险区**。且该通道**无申诉**。

### 八、其他会议的 desk reject 条款（可迁移参考）

- **FSE 2026**："Papers that do not comply with the double-anonymous review process (for the tracks that employ this process) will be **desk-rejected**." FSE 2026 的双盲是 "heavy" 模式——**匿名性在全部评审与讨论期间维持**，包括 major revision 的 response letter。
- **ICSE 2025 Research Track**：格式不符（"Alterations of spacing, font size, and other changes that deviate from the instructions may result in desk rejection without further review"）；绕过被拒论文重投规则（"will have their papers desk-rejected by the PC chairs without further consideration"）；并发投稿违规（"will lead to automatic rejection from ICSE 2025 as well as any other venue adhering to this policy"）。
- **ASE 2026**：新增强制性**数据可用性声明**（data availability statement），须在 10 页限制内的正文结论后提交；数据/复制包须通过提供长期档案的 DOI 公开且匿名发布。
- **ML4PS @ NeurIPS 2025**："Submissions flagged as coincidentally submitted to multiple NeurIPS workshops will be **desk rejected**."（workshop 之间互投也会被拒）
- **NeurIPS 2025 D&B track 的实际合规缺口**（官方 blog 2025-12-05）：缺 license 信息 **11.9%**、缺数据集描述 **4.9%**、缺 URL **3.5%**、缺数据集名称 **<1%**。这些是"提交时合规检查漏网但被审稿人 flag"的比例。

### 八之二、2026 年 ICML 的 desk reject 条款与"水印连坐"执法

ICML 2026 的官方 *Peer Review Ethics* 页面（2026-01-24 修订）给出了目前**结构最清晰的 desk reject 分类**，比 NeurIPS handbook 更细，值得阙疑逐条对照：

**单篇 desk reject 的理由（原文列举）**：
> "Placeholder abstracts at abstract submission. / Large differences between abstracts at abstract submission and at full paper submission. / Exceeding page limit. / Violations of paper formatting. / Violations of author anonymity. / Violations of the dual submission policy ... / **Hallucinated references.**"

注意两条 NeurIPS 没有明写的：**①"占位摘要"（placeholder abstract）本身就是 desk reject 理由**——即"先交个空摘要占位、全文再改"是明确违规；**②"摘要与全文差异过大"也是理由**。

**"全稿连坐"（desk rejection of all the submissions by the same author）的理由**：
> "Prompt injection (regardless whether all authors knew about it). / Violation of the concurrent submission policy ... / Neglect of reviewer or meta-reviewer duties (this is not limited to reciprocal reviewers). / Interference with integrity of peer-review process, including collusion, declaration of unsubstantiated conflicts, submission of low-quality AI-generated content (AI slop), and attempts to uncover the identities of reviewers or meta-reviewers."

也就是说，**审稿人/AC 若同时是作者却怠工或违规用 LLM，其本人名下所有投稿都可能被 desk reject**。

**该规则的执行案例（2026-03，二手来源，未核实）**：ICML 2026 在送审 PDF 中嵌入隐形水印，用于检测"审稿意见由 AI 代写"。据中文报道（知乎 / 智源社区 / 新智元，2026-03-19），共检出 **795 处违规审稿意见、涉及 506 名审稿人**（约占审稿意见总数 **1%**），并对"违规审稿人本人作为作者的投稿"执行连坐，**497 篇论文被 desk reject，约占总投稿量的 2%**。

**对阙疑的含义**：阙疑作者是稿件的唯一作者，**不存在"审稿怠工连坐"风险**（单作者若未接受审稿任务即无此暴露面），但"占位摘要"与"摘要—全文不一致"这两条是**新的、低成本的 desk reject 触发点**——2027 年投稿时，abstract deadline（预计 5 月上旬）当天必须提交**与全文一致的完整摘要**，不能先交占位。

### 九、把风险映射到阙疑的具体文件

| 风险条款 | 阙疑的具体暴露点 | 严重度 |
|---|---|---|
| 匿名性（含代码/补充材料） | `tools/gate_engine.py` 头部注释、`README.md` 里的机构/城市、`web/` 里的部署域名、`.git` 历史 | 极高（明文 "will be desk rejected"） |
| 幻觉引用 | `research/paper_v0.3.md` 的 Related Work 与 99_来源清单中的引用 | 极高（≥2 条即拒） |
| 页数/格式 | 9 页正文 + checklist 顺序 | 中（明文 may be desk rejected） |
| 主 track 与 E&D 双投 | 若同时投两个 portal | 极高（明文 grounds for desk rejection） |
| checklist 缺失 | LaTeX 模板中删除 checklist | 极高（明文 will be desk rejected） |
| 作者档案 | 2027-05-04 abstract deadline 前未建 OpenReview profile | 中（明文 risks desk rejection） |
| AI 检测 | 中文母语者 + LLM 润色 | 高（178 篇实证，无申诉） |
| 占位摘要 / 摘要—全文差异过大（ICML 2026 明文） | abstract deadline 当天先交空摘要占位 | 中（若投 ICML 类会议则高；NeurIPS 未明写但同源） |
| 审稿怠工连坐（ICML 2026 明文） | 单作者、未接受审稿任务 → **暴露面为零** | 无（阙疑的有利项） |
| LLM 使用声明 | 若 LLM 是方法核心组件（阙疑的规则引擎本身不是 LLM，风险低） | 低 |

## 对阙疑的 3 条具体行动

1. **在 2027-04-01 之前跑一遍"匿名性 + 引用"双查脚本**：新建 `tools/anonymity_scan_<batch>.py`（只登记在 `_arch_v46/`，不动仓库其它文件），扫描 `tools/*.py`、`web/*.html`、`README.md`、`research/*.md` 中的城市名、机构名、个人域名、邮箱、GitHub 账号；同时用 Crossref API（`https://api.crossref.org/works?query.bibliographic=...`）逐条核对 `research/` 与 99_来源清单里的每一条引用是否真实存在。命令示例：`python tools/anonymity_scan_<batch>.py --strict --json`。时间点：2027-04-01 前必须跑完并修完。

2. **把"≥2 条幻觉引用即 desk reject"写成硬约束并接入 CI**：在 `_arch_v46/` 记录一份 `desk_reject_checklist.md`（本文已提供全部条款），并在 `tools/` 的 `--check` 自检流程里加一条"引用真实性校验"步骤。工具：Crossref REST API + 人工复核（官方要求人复核，ICLR 三轮复核制可照搬）。时间点：2026-12-31 前完成设计，2027-03-31 前跑通。

3. **明确放弃"释放新数据集"的表述，改为"释放评估协议 + 夹具"**：E&D track 对数据集类有 Croissant 强制 + 无代码即拒的硬条款；阙疑的 `data/holdout/holdout.json`（30 seeds）、`data/external_corpus/external_corpus_665.json`（40 条）、`data/defect_fixtures/defects.json`（15 条）规模都太小，若声明为"新数据集"反而会触发更严的合规要求。行动：在 `research/06_datasets.md` 与 `research/paper_v0.3.md` 中统一措辞为 "evaluation protocol and fixtures"，并在 checklist 第 13 条（Assets）填 **NA**，第 4 条（Reproducibility）填 yes 并指向 GitHub 匿名仓库。时间点：2027-04-15 投稿门户开放前定稿。

## 盲区（诚实标注）

- **NeurIPS 2026 主 track 尚未真正投稿/评审**（截至 2026-09-29 只有 2026 年 5 月的 CFP 与 handbook），因此"2026 周期幻觉引用实际拒了多少篇主 track 论文"**未查到官方数字**；本文引用的 ACL 2026 ">100 篇"是 ACL 的数字，NeurIPS 侧的"5 out of 8"来自一位 AC 的个人公开表述，**非官方统计**。
- **arXiv:2607.00738 的审计数字（48,095 篇 / 260 万条引用 / 5.1%）我未直接读取原文**，采信第三方整理（strictcite.com，2026-09-05）。该审计对"幻觉"的定义较窄（仅算 non-existent works 与 substantial author-list mismatches），**排除了常规书目漂移**（如会议名变更、年份差 1），因此真实违规率可能更高。
- **Danish Pruthi 的引述**（"5 out of 8 submissions have 2+ hallucinated references"）来自社交媒体/二手整理，**我未核验其原始出处**。
- **"2020 年 NeurIPS desk reject 11%"** 这一数字出现在一篇 2020 年知乎文中，**我未核验其官方出处**，因此本文未采用。
- **Pangram 的 178 篇 / 18.4% / 42.7% / 273 篇 / 12.7%** 均转引自 CASRAI（2026-07-23），其自述来源为 NeurIPS 官方 blog 的 track chairs 说明；**我未直接读取该 blog 原文**。CASRAI 自己也在文末注明"任何具体百分比应视为该 2026 年 6 月博文所记录的状态"。
- **2026-06-15 有条件审查的最终结果（123 篇里多少人证明成功、多少人最终被拒）截至检索时未公布**。
- **NeurIPS 2026 E&D 的 FAQ 页面（`EvaluationsDatasetsFAQ`）与 hosting 指引（`EvaluationsDatasetsHosting`）我未逐字读取**，Croissant 的具体字段清单未核实。
- **ICSE 2026 的 desk reject 条款我未读取其独立 CFP 原文**（只读了 ICSE 2025 CFP 全文），ICSE 2026 可能有变化。
- **ICML 2026 的 "795 处违规 / 506 名审稿人 / 1% / 497 篇 desk reject / 2%" 全部来自中文二手报道**（知乎专栏 2026-03-21，其自述来源为智源社区 / 新智元 2026-03-19），**我未读取 ICML 官方公告或邮件原文核实**；但同页的 desk reject 条款（含 "Hallucinated references"、"Placeholder abstracts"、"desk rejection of all the submissions by the same author"）**已从 ICML 官方 Peer Review Ethics 页面（2026-01-24 修订）逐字核实**，条款本身可信，只有执法数字未核实。
- 本方向不涉及任何中国大陆政治、机构制裁相关内容；检索中出现的相关页面已主动排除。

## 来源

1. NeurIPS (2026). *Main Track Handbook 2026*（9 页 / 50MB / 格式 / 匿名 / 双投 / 作者档案 / 幻觉引用 / LLM / 伦理 / arXiv 条款原文）。https://neurips.cc/Conferences/2026/MainTrackHandbook
2. NeurIPS (2026). *Call For Papers 2026*（track 不可互投、"Irrelevant or duplicate papers risk desk rejection from all tracks"）。https://neurips.cc/Conferences/2026/CallForPapers
3. NeurIPS (2026). *Call For Evaluations & Datasets 2026*（Croissant 强制、code policy、accessibility desk reject 原文）。https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets
4. NeurIPS (2026). *Evaluations and Datasets 2026 Reviewing Guidelines*（LLM 严格禁令、desk reject 情形清单、reviewer 制裁条款）。https://neurips.cc/Conferences/2026/EvaluationsDatasetsReviewerGuidelines
5. NeurIPS. *Paper Checklist Guidelines*（16 条逐字条款、"papers not including the checklist will be desk rejected"、PDF 顺序）。https://neurips.cc/public/guides/PaperChecklist
6. NeurIPS (2025). *Reviewer Guidelines 2025*（"Desk Rejection Sanction: Grossly negligent reviews can result in desk rejection of reviewer's own papers"）。https://neurips.cc/Conferences/2025/ReviewerGuidelines
7. NeurIPS Communications Chairs (2025-09-30). *Reflections on the 2025 Review Process from the Program Committee Chairs*（21,575 / 5,290 / 24.52%；11 例 co-author desk reject）。https://blog.neurips.cc/2025/09/30/reflections-on-the-2025-review-process-from-the-program-committee-chairs/
8. CASRAI Editorial Board (2026-07-23). *NeurIPS 2026: Pangram AI-Detector Desk Rejections*（969–971 / 178 / 18.4% / 123 / 12.7% / 42.7% / 273 / 100 词窗口）。https://casrai.org/news/neurips-2026-pangram-ai-detector-desk-rejection-controversy
9. StrictCite (2026-09-05). *NeurIPS Started Desk-Rejecting Papers Over References That Don't Exist*（ACL >100 篇、Pruthi 引述、arXiv:2607.00738 审计表、GPTZero 三案例）。https://strictcite.com/blog/neurips-2026-hallucinated-citations-desk-reject
10. NeurIPS Communications Chairs (2025-12-05). *NeurIPS Datasets & Benchmarks Track: From Art to Science in AI Evaluations*（1,820→1,995 投稿、元数据缺口 11.9%/4.9%/3.5%、851 作者 + 155 审稿人调查）。https://blog.neurips.cc/2025/12/05/neurips-datasets-benchmarks-track-from-art-to-science-in-ai-evaluations/
11. ICSE 2025 Research Track Call for Papers（desk reject 三类触发点、并发投稿、格式违规原文）。https://www.conferences-computer.science/icse/2025/cfp/ICSE-2025.txt
12. FSE 2026 *How to Submit*（"Papers that do not comply with the double-anonymous review process... will be desk-rejected"、heavy double-anonymous）。https://conf.researchr.org/track/fse-2026/fse-2026-how-to-submit
13. ASE 2026 投稿相关（博客园，inertial-fish，2026-03-04）：早期拒绝、强制性数据可用性声明、10 页限制。https://www.cnblogs.com/sinclaire/p/19669421
14. ML4PS @ NeurIPS 2025 Guidelines（"Submissions flagged as coincidentally submitted to multiple NeurIPS workshops will be desk rejected"）。https://ml4physicalsciences.github.io/2025/guidelines.html
15. NeurIPS (2025). *NeurIPS 2025 FAQ for Authors*（rebuttal 期间不允许提交修订）。https://neurips.cc/Conferences/2025/PaperInformation/NeurIPS-FAQ
16. ICML (2026). *Peer Review Ethics 2026*（单篇 desk reject 理由含 "Placeholder abstracts at abstract submission"、"Large differences between abstracts at abstract submission and at full paper submission"、"Hallucinated references"；"desk rejection of all the submissions by the same author" 的四种触发；2026-01-24 修订）。https://icml.cc/Conferences/2026/PeerReviewEthics
17. 知乎专栏（2026-03-21）《ICML用"隐形水印"抓AI审稿：497篇论文被"连坐"冤不冤？》（795 处违规审稿意见 / 506 名审稿人 / 约占 1% / 497 篇 desk reject / 约占 2%；自述来源为智源社区、新智元 2026-03-19）——**二手来源，数字未核实**。https://zhuanlan.zhihu.com/p/2018740893985810067
