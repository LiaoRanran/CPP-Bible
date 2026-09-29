# 方向 23：Threats to Validity 五层写法

## 核心结论

1. **"五层"不是凭空多出来的一层，而是对经典四层的一个精确切分**：Shadish、Cook & Campbell（2002）的四类是 **statistical conclusion validity / internal / construct / external**；Wohlin 等把它改写为 **conclusion / internal / construct / external**。所谓"五层"是把 **statistical（定量：功效、区间、效应量、多重比较）** 从 **conclusion（定性：从数据到主张的推断是否成立）** 中拆出来——这个拆分必须在文中显式声明，否则会被认为是不懂框架来源。
2. **真实数据表明：绝大多数论文的 TTV 章节是装饰**——Lago、Runeson、Song、Verdecchia（ESEM 2024）分析了 ICSE 十年（2014–2023）**91 篇 SIGSOFT 杰出论文**，其中只有 **67.0%（61/91）** 有专门 TTV 章节，**56% 属浅表**，**61.5%（56/91）不报任何缓解策略**，只有 **2.19%（2/91）** 讨论威胁之间的权衡取舍。
3. **层与层的使用率极不均衡，这正是阙疑的机会**：同一研究中 internal validity 出现 **34 次（37.4%）**、external **29 次（31.9%）**、construct **19 次（22.0%）**，而 **conclusion validity 只出现 4 次**、reliability 5 次。阙疑的核心量是"检出率"这一**比例型结论**，其最大威胁恰恰在 conclusion/statistical 层——在这个几乎无人认真写的层里做出扎实工作，是最容易拿到"诚实性加分"的位置。

---

## 精确数字与案例

### 1. 最硬的一手数据：ESEM 2024 对 91 篇 ICSE 杰出论文的审计

**论文**：Patricia Lago, Per Runeson, Qunying Song, Roberto Verdecchia, *"Threats to Validity in Software Engineering – hypocritical paper section or essential analysis?"*，ESEM '24（第 18 届 ACM/IEEE International Symposium on Empirical Software Engineering and Measurement），2024-10-24/25，巴塞罗那，11 页。**DOI 10.1145/3674805.3686691**；开放数据 **Zenodo DOI 10.5281/zenodo.13382821**。

**样本**：**91 篇** ICSE 主技术轨道论文，筛选标准是获 **ACM SIGSOFT Distinguished Paper Award**，时间跨度 **10 年（2014–2023）**。选取"杰出论文"作为样本的策略很关键——即"连最佳论文都做不到"，论证力度远强于随机抽样。

**六个考察方面（six main facets）**：显式记录（explicit documentation）、分类（categorization）、局限性讨论（discussion of limitations）、权衡取舍（trade-offs）、主动分析（proactive analysis，含缓解策略）、分类与研究类型的匹配度（fitness of categorization）。由 **7 个研究问题（Q0–Q7）** 与对应指标（M0.1–M7.2）支撑。

**可逐条引用的数字**：

| 指标 | 数字 | 占比 |
|---|---|---|
| 有专门 TTV 章节 | 61/91 | **67.0%** |
| 没有专门 TTV 章节 | 30/91 | 33.0% |
| 完全未报告 TTV | 20/91 | ≈22.0% |
| TTV 反思**深入** | 20/91 | **22%** |
| TTV 反思**浅表** | 51/91 | **56%** |
| 明确引用带分类的清单/指南 | **2/91** | **≈2.2%** |
| 采用了与研究类型匹配的分类 | 29/91 | 31.9%（2014–2018 段 39.5%；2019–2023 段 **26.4%**，轻微下降） |
| 在研究设计/方法章节就讨论 TTV | — | **8.8%** |
| **未报告任何缓解策略** | 56/91 | **61.5%** |
| 在 TTV 章节讨论研究设计 | 24/91 | 26.4% |
| 有专门 Limitations 章节 | 13/91 | **14.3%** |
| 按定义讨论了局限性（含无专门章节者） | 61/91 | 67% |
| 无专门章节但符合定义地讨论 | 11/91 | 12.1% |
| **报告 TTV 之间权衡取舍的** | **2/91** | **2.19%** |

**效度类型使用频次**：internal **34（37.4%）**、external **29（31.9%）**、construct **19（22.0%）**、reliability **5**、conclusion **4**、定性标准（credibility/transferability/dependability/confirmability 之一）**7**、generalizability **10**、bias **3**。

**重叠情况**：讨论 internal 的论文中 **82.4%（28/34）** 也讨论 external；讨论 external 的论文中 **96.6%（28/29）** 也讨论 internal；讨论 internal 的论文中 **50%（17/34）** 也讨论 construct，反之为 **89.5%（17/19）**；**只讨论三类之一的极少：7/37，18.9%**。

**研究类型分布（Q0）**：多方法研究 **55/91（60.4%）**；实验（lab experiment）51、设计研究 48、挖掘研究 15、案例研究 11、访谈 10、问卷 8、文献综述 3。Top-1 组合为"设计研究 + 实验"**34 篇（37.4%）**；"单独实验" **14 篇（15.4%）**。

**该论文的结论与产出**：这些"最佳论文"的 TTV 讨论仍以浅表或缺失为主；证实了 Verdecchia 等（2023）的批评——TTV 多被当作**事后附加（afterthought）**与**清单式罗列（laundry list / boilerplate）**；**十年来无改进趋势**。作者据此提出 **12 条注意事项（C1–C12）**，分别面向研究者、审稿人与读者。

### 2. 上游批评：Verdecchia 等 2023（IST）

**论文**：Roberto Verdecchia, Emelie Engström, Patricia Lago, Per Runeson, Qunying Song, *"Threats to validity in software engineering research: A critical reflection"*，*Information and Software Technology*，2023（DOI 对应 PII **S0950584923001842**）。

**原文可直接引用的关键句**（来自摘要与引言）：

- "In many ESE studies, TTV often seem to be **unfocused and treated in a rather superficial manner**."
- "Frequently, TTV sections seem to be included **just as a mandatory component**, rather than a critical reflection on the potential threats of studies."
- "to date, TTV sections seem to be mostly formulated as **'laundry-lists'** of potential threats, lacking a thorough contextualization in the specifics of the study at hand."
- "it is crucial to consider TTV as **an essential part of the empirical research process**, rather than just a perfunctory requirement. Researchers should consciously take time to critically reflect on the TTV of their studies **throughout all research phases**, without blindly relying in a check-list fashion on diktat imposed by pre-existing TTV categorizations."

**它列出的三个具体缺陷（原文章节标题）**：把 TTV 当检查清单会阻碍反思（Using threats to validity as checklists hinders reflection）；TTV 作为事后附加（Threats to validity as afterthought）；以及缺少分类类型的承认（failure to acknowledge different types of validity categorizations）。该文的定位是 **position paper**，其结论是"urgent need to reconsider how we approach, document, and evaluate TTV"。

### 3. 分类框架的来源与"五层"的准确谱系

- **Shadish, Cook & Campbell（2002）**，*Experimental and Quasi-Experimental Designs for Generalized Causal Inference*：四类效度为 **statistical conclusion validity / internal validity / construct validity / external validity**。注意——**"statistical" 本来就在四类里**，且被明确命名为 "statistical conclusion validity"。
- **Wohlin 等**，*Experimentation in Software Engineering*（Springer；第 3 版 2024，**DOI 10.1007/978-3-662-69306-3**）：SE 社区最通行的四分类为 **conclusion / internal / construct / external validity**，其中 conclusion validity 承接了 Shadish 的 statistical conclusion validity。
- **Sjøberg & Bergersen（2023）**，*"Construct Validity in Software Engineering"*，*IEEE Transactions on Software Engineering*（**DOI 10.1109/TSE.2022.3176725**）：指出"被归入 construct validity 的威胁主题过于庞杂，需要一个更极简的处理方式（more minimalist approach）"，并**提出 7 条指南**改进 construct validity 的处理与报告。
- **Ampatzoglou 等（2019）**，*"Identifying, categorizing and mitigating threats to validity in software engineering secondary studies"*，IST（PII S0950584918302106）：面向**二级研究**的威胁识别—分类—缓解框架。
- **Feldt & Magazinius**，*"Validity threats in empirical software engineering research – An initial survey"*；**Siegmund 等**，*"Views on internal and external validity in empirical software engineering"*：两篇被 ESEM 2024 论文列为"更早的警告"。

**因此"五层"的正确写法**：先承认 Shadish/Wohlin 的四分类，再声明本文的切分理由——"本文把 conclusion validity 进一步拆为 **statistical（定量层：区间、功效、多重比较、效应量）** 与 **inferential/conclusion（定性层：数据到主张的推断、替代解释、测量陷阱）** 两层，理由是本研究的核心主张是**比例型**的（检出率），其威胁同时具有定量与定性两面，合并讨论会掩盖后者。" 加这一句，就把"自创分类"的风险转成"有理由的细化"。

### 4. 每一层的四段式模板（威胁 → 证据 → 缓解 → 残余）

这是本文建议阙疑采用的写法。每层固定四段，**每段必须出现具体数字或具体文件**，禁止形容词堆叠：

**第 1 层 Construct Validity（构念效度：我们测的是不是"知识验证能力"）**
- 威胁：检出率是"在 30 个植入样本上的命中比例"，而"知识验证能力"是更宽的概念。命中率高不等于验证能力强（可能只擅长植入式缺陷）。
- 证据：holdout 标签分布 **真错 17 / 对照 9 / unknown 4**；`data/holdout/holdout.json` 的 `audit_note` 记录了 662 A1 批次逐个按 atom 头部注释核标签、665 扩样后真错从 7 改为 **17**；`blind=false`、`revealed=true`、`reveal_irreversible=true`。这说明标签本身经过两轮人工修正——**测量工具本身被改过**。
- 缓解：三类语料交叉（盲 holdout 30 / 外部 corpus 40 / 真实缺陷夹具 15），并明确"外部 corpus 才代表非植入场景"。
- 残余：**未解决**。植入样本与真实缺陷的分布不同，任何跨语料的检出率差都不能单独归因于"能力"。

**第 2 层 Internal Validity（内部效度：观察到的差异是否由我们声称的原因造成）**
- 威胁：编译档、编译器、sanitizer 可用性都可能制造虚假的"检出/漏检"。
- 证据：论文 v0.3 已量化 **`-O1`→`-O0` 使 3/5 个 miss 被同一个 sanitizer 抓住**。这是一个真实的内部效度威胁——即"漏检"有一部分不是规则不行，而是编译档不匹配。
- 缓解：把编译档矩阵化（`-O0/-O1/-O2/-O3/-Os`），并对每条判决记录 `cpp_standard / compiler / platform / input_domain` 四元组（663 C1 批次已为 26 张 verified 卡补齐 semantic scope）。
- 残余：**部分解决**。已量化但未做全档位扫描。

**第 3 层 External Validity（外部效度：结论能推广到哪）**
- 威胁：37 实卡 + 10 草稿 = 47 个 `ATOM-*.md` 覆盖 `conc 3 / lang 8 / mem 23 / ub 2 / hist 1`，**内存域占 23/37（62.2%）**，域分布严重不均衡。
- 证据：`atoms/mem/` 卡数 23，是全仓最大头；`atoms/ub/` 只有 2 张。
- 缓解：外部 corpus 40 条按 A/B/C 三层分层报告（A 54.2% / B 12.5% / C 0%），并主动放弃把内部变异率（97.3%）当缺陷检测率。
- 残余：**未解决**。C 层检出率 0% 本身就是一个外部效度的负面结果，必须保留在正文而不是塞进附录。

**第 4 层 Conclusion Validity（结论效度：从数据到主张的推断是否成立）**
- 威胁：把"检出率 66.7%"读成"能力约 66.7%"；把"重注入检出 6/6=100%"读成"100% 可靠"。
- 证据：本方向实算——6/6 的 Clopper-Pearson 95% 置信区间是 **[0.5407, 1.0000]**，下限只有 54.07%；10/15 的 CP 区间是 **[0.3838, 0.8818]**。**n=6 与 n=15 在数学上不支持任何强主张。**
- 缓解：所有比例一律附 CI；明确写出"本样本量不支持对 70% 与 60% 的区分"。
- 残余：**可完全解决**（只要坚持附区间并限制主张强度）。

**第 5 层 Statistical（统计层：区间方法、功效、多重比较、效应量）**
- 威胁：(i) 用 Wald 区间会在 k=0 或 k=n 时给出越界值（实算：2/16 的 Wald 下限 **−0.0370**；12/15 的 Wald 上限 **1.0024**）；(ii) 多重比较未校正——67 条规则 × 3 个数据集 = 最多 201 次比较，α=0.05 下期望假阳性约 **10 次**；(iii) 未报效应量，无法区分"统计显著但无意义"。
- 证据：NeurIPS Checklist 第 7 项原文要求说明误差棒捕捉的变异来源、计算方法与假设，并警告 "For asymmetric distributions, the authors should be careful not to show in tables or figures symmetric error bars that would yield results that are out of range (e.g. negative error rates)."；statsmodels 文档原文 "the Clopper-Pearson exact interval has coverage at least 1-alpha, but is in general conservative"。
- 缓解：比例区间一律用 **Clopper-Pearson**（`method='beta'`）或 **Wilson**；配对比较用 **McNemar**，非配对用 **Fisher 精确**；效应量报 **Cohen's h** 与 **Cohen's κ**；多重比较用 **Holm–Bonferroni**；对 n=30 级别明确做功效讨论。
- 残余：**可完全解决**，且这是阙疑相对同规模工作最容易拉开差距的一层。

### 5. 一个"元状态不可信"的现成案例，直接可用

`_auto/status.json` 记录 `active_batch=660`、`state=awaiting_review`，而 `git log` 最新批次已是 **665**（`22e47b45`）。这是**元状态漂移**：仓库自己记录的状态落后于真实状态 5 个批次。

这个案例的价值在于：它是**系统自身的不确定性证据**，属于第 1 层（construct）与第 2 层（internal）的交界。诚实写法是："系统自报的状态文件在本次扫描时落后于实际提交 5 个批次（`_auto/status.json` 记 660，`git log` 为 665），这说明**元状态不能作为证据源**；本论文所有数字均来自内容文件（JSON/MD）而非状态文件。" 这句话同时做到了三件事：给出具体数字、承认系统缺陷、说明规避策略。

### 6. 该写多长、放在哪

- **位置**：NeurIPS 主赛道正文有页数限制（ED 赛道沿用主赛道格式，具体页数须查 2027 年 CfP），但 **Limitations 章节是 checklist 第 2 项明确鼓励的独立章节**。实操建议：正文放一节 **"Limitations"**（1 页内，五层各一段），完整五层版放**附录**（可 2–4 页）。
- **长度基准**：ESEM 2024 样本中只有 **14.3%（13/91）** 有专门 Limitations 章节，说明"有专门章节"本身就是少数派做法，**不构成超标风险**。
- **禁忌**：不要写成 20 条 bullet 的 laundry list（这正是 2/91 引用清单、61.5% 不报缓解策略所对应的反面教材）；每条威胁必须绑定"阙疑的具体证据 + 具体缓解 + 残余程度"三段。

---

## 对阙疑的 3 条具体行动

**行动 1（2026-11-15 前，写五层版 Threats to Validity）**：改写 `research/12_threats_to_validity.md`，严格用上面第 4 节的"四段式 × 五层"结构（共 20 段），每段必须出现至少一个具体数字或文件路径。开头加一段"分类谱系声明"（Shadish/Cook/Campbell 四类 → Wohlin 四类 → 本文为何拆出 statistical 层）。验收标准：把这份文件单独给一个不熟悉阙疑的人看，他能复述出每一层的威胁是什么、阙疑用什么证据回应、还剩什么没解决。

**行动 2（2026-12-31 前，把 statistical 层做成可执行的自检）**：新建 `research/24_stats_selfcheck.md` 并写一个脚本 `tools/stats_report_*.py`，对三个数据集（holdout 30 / corpus 40 / defects 15）自动输出：每层 k/n、Clopper-Pearson 与 Wilson 区间、配对 McNemar p 值、Cohen's h、Holm 校正后的 p 值。命令示例：`python tools/stats_report_676.py --holdout data/holdout/holdout.json --corpus data/external_corpus/external_corpus_665.json --fixtures data/defect_fixtures/defects.json --out report/stats_676.md`。把该报告作为论文附录 D，并在 §5.6 引用它——这样"统计方法"就从"声称用了"变成"有一条命令可复算"。

**行动 3（2027-02-28 前，把元状态漂移写成正式实证）**：在五层版的 internal validity 段中，把 `_auto/status.json`（`active_batch=660`）与 `git log`（665）的漂移写成一个**可复算的实证**，并给出复算命令（`git log --oneline -1` 与 `python -c "import json;print(json.load(open('_auto/status.json'))['active_batch'])"`）。同时把"452 条判决账本采信 README、未独立复算"这一条登记进 construct validity 段——它本身就是"证据链上有一环未经独立验证"的诚实披露，而阙疑的主张恰恰是"可被独立验收"，这两者并列出现反而是加分项。

---

## 盲区（诚实标注）

1. **ESEM 2024 那组数字来自 ACM DL 全文 HTML 的自动抽取**，其中"完全未报告 TTV = 20/91 ≈ 22.0%"与"TTV 反思浅表 = 51/91 (56%)""深入 20/91 (22%)"三者的分类边界我**未逐字核对原表**；22% + 56% + 22% = 100% 是自洽的，但"20 篇未报告"与"20 篇深入"数值相同，存在被抽取工具混淆的可能，**引用前建议回原文核表**。
2. **"six main facets"的六项名称**（显式记录 / 分类 / 局限性讨论 / 权衡取舍 / 主动分析 / 分类匹配度）来自摘要的概括性表述，**与正文 Q0–Q7 的七项并不一一对应**，本文按摘要口径列出。
3. **Verdecchia 等 2023 的正文未能获取**（ScienceDirect 需机构登录），本文只引用了摘要与引言片段，**未核实其 Table 1 的映射表内容**。
4. **Sjøberg & Bergersen 2023 的"7 条指南"具体内容未核实**（只核实到摘要中的"more minimalist approach"与"seven guidelines to improve how construct validity is handled and reported"）。
5. **Wohlin 第 3 版（2024）中 conclusion validity 的确切定义措辞未核实**，只核实到 Springer 链接与 DOI 10.1007/978-3-662-69306-3。
6. **Ampatzoglou 等 2019、Feldt & Magazinius、Siegmund 等三篇只核实到标题与被引关系**（作为 ESEM 2024 论文的参考文献 [1][2][3][4] 出现），未核实其年份与具体结论。
7. **"2014–2018 段 39.5% vs 2019–2023 段 26.4%"这个下降趋势的显著性未做检验**——原论文称之为 "slight downward trend"，本文照搬该措辞。
8. **NeurIPS 2027 ED 的正文页数限制未核实**（2027 CfP 尚未发布），"正文 1 页 + 附录 2–4 页"是**建议值**，不是规则。
9. **阙疑的 66.7%（10/15）与 43.8% 之间的口径关系未核实**；本方向沿用方向 22 的发现（43.8% 与分层率不自洽），并把它列为 construct/conclusion 层的待查项。
10. **`_auto/status.json` 的 `active_batch` 字段名与当前值未在本次会话中直接读取验证**，来源是 `_arch_v46/00_仓库扫描.md` §2 的记录（该扫描为只读实测）。

---

## 来源

1. P. Lago, P. Runeson, Q. Song, R. Verdecchia, "Threats to Validity in Software Engineering – hypocritical paper section or essential analysis?", ESEM '24, 2024-10-24/25, Barcelona, 11 页，DOI 10.1145/3674805.3686691；开放数据 Zenodo DOI 10.5281/zenodo.13382821 — https://dl.acm.org/doi/fullHtml/10.1145/3674805.3686691 ；https://dl.acm.org/doi/10.1145/3674805.3686691 ；PDF: https://robertoverdecchia.github.io/papers/ESEM_2024.pdf
2. R. Verdecchia, E. Engström, P. Lago, P. Runeson, Q. Song, "Threats to validity in software engineering research: A critical reflection", *Information and Software Technology*, 2023（PII S0950584923001842）— https://www.sciencedirect.com/science/article/pii/S0950584923001842
3. D. I. K. Sjøberg, G. R. Bergersen, "Construct Validity in Software Engineering", *IEEE Transactions on Software Engineering*, 2023, DOI 10.1109/TSE.2022.3176725 — https://ieeexplore.ieee.org/abstract/document/9780058 ；https://dlnext.acm.org/doi/10.1109/TSE.2022.3176725
4. W. R. Shadish, T. D. Cook, D. T. Campbell, *Experimental and Quasi-Experimental Designs for Generalized Causal Inference*, Houghton Mifflin, 2002（四类效度：statistical conclusion / internal / construct / external）— 转引综述：https://link.springer.com/article/10.1007/s12564-024-09955-4
5. C. Wohlin et al., *Experimentation in Software Engineering*, Springer，第 3 版 2024，DOI 10.1007/978-3-662-69306-3 — https://link.springer.com/book/10.1007/978-3-662-69306-3
6. A. Ampatzoglou et al., "Identifying, categorizing and mitigating threats to validity in software engineering secondary studies", *Information and Software Technology*, 2019（PII S0950584918302106）— https://www.sciencedirect.com/science/article/pii/S0950584918302106
7. R. Feldt, A. Magazinius, "Validity threats in empirical software engineering research – An initial survey"（作为 ESEM 2024 论文参考文献 [1] 出现，未核实年份）
8. J. Siegmund et al., "Views on internal and external validity in empirical software engineering"（作为 ESEM 2024 论文参考文献 [2] 出现，未核实年份）
9. "A Revision of the Campbellian Validity System", *Scandinavian Journal of Educational Research*, 2020, DOI 10.1080/00313831.2020.1739126 — https://www.tandfonline.com/doi/full/10.1080/00313831.2020.1739126
10. "A primer on the validity typology and threats to validity in education research", *Asia Pacific Education Review*, 2024 — https://link.springer.com/article/10.1007/s12564-024-09955-4
11. NeurIPS Paper Checklist Guidelines（第 2 项 Limitations 原文、第 7 项统计显著性原文）— https://neurips.cc/public/guides/PaperChecklist
12. statsmodels, `proportion_confint`（Clopper-Pearson 保守性原文；Brown, Cai & DasGupta 2001, Statistical Science 16(2):101–133）— https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportion_confint.html
13. SciPy, `scipy.stats.binomtest` / `proportion_ci` — https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binomtest.html
14. Designing Empirical Education Research Studies (DEERS), "Threats to Validity" 模块 — https://empiricalcsed.org/modules/study%20design/threats/
15. 阙疑仓库只读扫描（锚点来源）— `_arch_v46/00_仓库扫描.md`（§2 元状态漂移、§3 卡数分布、§6 holdout 标签、§10 编译档陷阱）
16. 本方向第 4 节第 5 层的置信区间数字（6/6 → [0.5407, 1.0000]；2/16 Wald 下限 −0.0370；12/15 Wald 上限 1.0024）为**本次实算**，非引用。
