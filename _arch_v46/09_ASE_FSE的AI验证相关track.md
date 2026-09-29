# 方向 09：ASE / FSE / ICSE 里与 AI 生成代码验证、LLM 评测、软件可靠性相关的 track 与近期论文

> 调研时间：2026-09-29（GMT+8）
> 检索工具：WebSearch ×14 + WebFetch ×8（researchr 官方 track 页、arXiv、ACM DL、IEEE Xplore、workshop 官网）
> 锚点：阙疑（queyi）——C++ 知识验证器；本文回答"阙疑应当把稿子投进 SE 社区的哪条通道，以及有哪些现成的对标物"

## 核心结论

1. **SE 三会（ICSE/FSE/ASE）在过去三年已经形成了一个完整的"AI 生成代码验证"生态**：既有主 track 的常设 session（AI4SE / Software Engineering for AI / LLM for SE），也有专门的数据/工具 track（ASE Tools and Datasets、FSE Artifacts）与专门 workshop（ICSE 的 LLM4Code、FSE 的 LLMTrust 2026），其中**LLM4Code 与 LLMTrust 都是 archival + IEEE/ACM 索引**，不是"边缘会议"。
2. **C/C++ 是这套生态里最薄弱、也最被明确点名的缺口**：ASE 2025 的 *Defects4C* 论文开篇即指出"Java-based APR 因 Defects4J 而进展显著，但 C/C++ 程序修复研究存在显著空白，主要原因是缺乏高质量开源基准"——这与阙疑"C++ 知识验证"的定位形成直接的、被顶会承认的空白。
3. **"LLM 自评不可靠"已经被 SE 社区量化到可以引用**：ASE 2025 的 *SE-Jury* 发现现有自动指标与人类判断的相关性不足，其集成判官方案把相关性提升了 **29.6%–140.8%**；NeurIPS 2026 E&D 的 LLM 禁令与审稿人调查中"25% 作者抱怨依赖 AI 生成反馈"是同一问题的另一面。

## 精确数字与案例

### 一、track 地图：SE 三会里"AI 生成代码验证"的落点

**ICSE 的九个研究领域**（2025 年起）：AI for Software Engineering、Analytics、Architecture and Design、Dependability and Security、Evolution、Human and Social Aspects、Requirements and Modeling、**Software Engineering for AI**、Testing and Analysis。其中 2025 年做了一次关键拆分（"NEW THIS YEAR #1: it is now split into two: 'AI for Software Engineering' and 'Software Engineering for AI'"）。阙疑的定位属于**后者**（用 SE 方法服务 AI/验证 AI 产出）叠加 **Dependability and Security**。

**ASE 2025 的 session 分布**（来自官方议程）：AI4SE、Autonomous and Self-Adapting Systems、Security and Privacy、Regression and Model-Based Testing、Refactoring and Reengineering、Program Comprehension and Visualization、Specification Languages、API Design and Management、Automated Program Repair and Synthesis。

**FSE 2026 的 session 分布**（来自官方议程）：**LLM for SE 1/2/3**（三个并行分会场，共约 15 篇）、**Agents**（RocketMQ-A2A 多智能体协作、AgentBound 智能体执行边界安全、LLM Agent 轨迹压缩降本）、**Verification 1**（Precondition Synthesis for Deep Neural Networks with Statistical Guarantees、Compiler Optimization-Based SMT Simplifications）、**Bug Detection and Localization**（Reflex 事件驱动自动故障定位、GraphLocator 图引导因果推理、Typestate-based Fault Localization）、**Benchmarking**（CrypFormBench：LLM 密码方案形式化分析能力基准）、**Testing 1**（Clotho：LLM 输入的预生成测试充分性度量；Towards Automated Crowdsourced Testing via Personified-LLM）、**Program Analysis 1**（LLMs for Opaque Predicate Resolution）、**Program Repair**（TLR：代码库级 C 内存管理错误修复）、**Synthesis**（Event-B Agent：LLM Agent 做形式模型合成与修复；Fun2spec：规模化代码契约合成）、**Dependency**（面向可靠软件定义汽车 OTA 更新的依赖感知框架）。

**FSE 2026 中与阙疑最接近的三篇**（可作为 Related Work 的直接锚点）：
1. *Validating LLM-Generated SQL Queries Through Metamorphic Prompting*（Research）——用蜕变关系（metamorphic）验证 LLM 生成的 SQL，与阙疑"用规则/性质验证 LLM 产出"同构；
2. *Galápagos: Automated N-Version Programming with LLMs*（Journal-First）——N 版本编程 + LLM，与阙疑"独立对账器"（不依赖内核的第二个实现）思路一致；
3. *CrypFormBench*（Benchmarking）——LLM 形式化分析能力基准，与阙疑"知识验证"的评测设计同层。

### 二、五个可直接对标的近期论文（含精确数字）

**（1）Defects4C —— C/C++ 修复能力的首个大型基准（ASE 2025 main research paper）**
- 作者：Jian Wang、Xiaofei Xie、Qiang Hu、Shangqing Liu、Jiongchi Yu、Jiaolong Kong、Yi Li；arXiv:2510.11059（v1 2025-10-13，v2 2025-12-02）；DOI 10.1109/ASE63991.2025.00029。
- **数据集规模（精确）**：来自真实 C/C++ 仓库，含 **9M（900 万）条** bug 相关提交、**248 个高质量 buggy 函数**、**102 个 vulnerable 函数**，每个都配有可复现的测试用例。
- **评测规模**：用 Defects4C 系统评测了 **24 个** SOTA LLM 在 C/C++ 故障修复上的能力。
- 论文动机原文（对阙疑极其重要）：
  > "While substantial progress has been made in Java-based APR, largely facilitated by benchmarks like Defects4J, **there remains a significant gap in research on C/C++ program repair**... This gap is primarily due to the lack of high-quality, open-source benchmarks tailored for C/C++."
- 对阙疑的含义：**"C/C++ 缺基准"是 2025 年 ASE 顶会论文的官方论断**，可以直接引用，且阙疑的 15 条真实缺陷夹具 + 6/6 重注入检出正好是这个空白里的一块砖。但要注意规模差距：Defects4C 是 248+102，阙疑是 15。

**（2）SE-Jury —— LLM-as-Ensemble-Judge（ASE 2025，DOI 10.1109/ASE63991.2025.00214）**
- 作者：Xin Zhou、Kisub Kim、Ting Zhang、Martin Weyssow、Luis F. Gomes、Guang Yang、Kui Liu、Xin Xia、David Lo；arXiv:2505.20854（v1 2025-05-27，v2 2025-10-10）。
- **机制**：定义 5 种独立评估策略，每种由一个独立 judge 实现；再用动态团队选择机制挑出最合适的 judge 子集，通过 ensembling 产出最终正确性分数。
- **精确结果**：跨三类 SE 任务（代码生成、自动程序修复、代码摘要）的多个 benchmark 上，SE-Jury 与人类判断的相关性**比现有自动指标提升 29.6% 到 140.8%**；在代码生成与程序修复上，其与人类标注者的一致度**接近标注者间一致度（inter-annotator agreement）**。
- 论文动机原文：
  > "On one hand, human evaluation provides high accuracy but is labor-intensive and lacks scalability. On the other hand, many automatic evaluation metrics are scalable and require minimal human effort, but **they often fail to accurately reflect the actual correctness of generated software artifacts**."
- 对阙疑的含义：阙疑的"四态判决"（pass / fail / warn / advice 之类的分级）本质上是一种**非 LLM 的判定器**；SE-Jury 提供了"判定器与人类判断的相关性"这一评测范式，阙疑可以照抄其方法论框架（但要诚实说明阙疑没有人类标注预算）。

**（3）CWEval —— 同时评功能与安全（LLM4Code 2025 @ ICSE 2025）**
- 作者：Jinjun Peng、Leyi Cui、Kele Huang、Junfeng Yang、Baishakhi Ray（Columbia University）；arXiv:2501.08200（2025-01-14）。
- 定位："the **first** evaluation method to our knowledge that simultaneously evaluates both functionality and security"，配套 **CWEval-bench**（multilingual, security-critical coding benchmark）。
- 对阙疑的含义：**"同时评两个正交维度"**（CWEval 是功能 + 安全，阙疑是"知识正确性 + 证据可验收性"）是一个已被顶会 workshop 接受的设计模式。

**（4）A.S.E / AICGSecEval —— 仓库级 AI 生成代码安全评测（腾讯，2025）**
- arXiv:2508.18106（v1 2025-08-25，v2 2025-09-11）；OpenReview id `OJbIlRcaVR`；开源在 https://github.com/Tencent/AICGSecEval 。
- 定位："A.S.E (AI Code Generation Security Evaluation), a **repository-level** evaluation benchmark"——把评测从函数级提升到仓库级。
- 对阙疑的含义：**"仓库级 vs 函数级"是 2025 年评测设计的一个显式维度**；阙疑的 `tools/` 640 条目 / 595 个 `.py` 是仓库级资产，可以主张自己是"仓库级知识一致性验证"，但要给出与 A.S.E 的明确边界差异。

**（5）FVAPPS —— 形式化验证代码生成的基准（LLM4Code 2025 @ ICSE 2025，DOI 10.1109/LLM4Code66737.2025.00017）**
- 作者：Quinn Dougherty、Ronak Mehta，**两人署名均为 "Unaffiliated"（无机构）**；2025-05-03 于 ICSE 2025 的 LLM4Code workshop 报告（10 分钟 talk）。
- **精确数字**：**4,712 个样本**，论文自称 "the largest formal verification benchmark"；把 APPS 的 Python 单元测试泛化为 **Lean 4 定理**（用 `sorry` 关键字给出无证明的定理）；在 100 个随机样本的 **406 条定理**上，**Sonnet 完成 30%，Gemini 完成 18%**。
- **对阙疑的直接价值**：这是"**无机构署名的独立研究者**在 ICSE 的 archival workshop 上发表被 IEEE 索引的论文"的**已核实案例**（见方向 10）。

### 三、LLM 评测方向的两篇综述与一篇立场论文

- *LLM-as-a-Judge for Software Engineering: A Survey*（SE 2030 forward-looking paper），arXiv:2510.24367，2025-10-28。定位是"steer the community toward advancing LLM-as-a-Judge for evaluating SE artifacts"。
- *Large Language Models for Code Generation: A Comprehensive Survey*，arXiv:2503.01245（2025-03-04），覆盖 LLM 在自动代码生成中的局限与挑战。
- *LLM Hallucinations in Practical Code Generation: Phenomena, Mechanism, and Mitigation*（2025）——指出 CoderEval、EvoCodeBench 等基准"measure the functional correctness"，但幻觉问题另有一层。
- *Verifying LLM-Generated Code in the Context of Software Verification*，arXiv:2502.07728（2025-02-11）——探索用 **SPARK（Ada 的形式化验证框架）** 验证 LLM 生成代码的可行性。**这是与阙疑最同构的一篇**：都是"用一套非 LLM 的严格规则去验收 LLM/人类产出的代码"。阙疑的差异点是 **C++ 而非 Ada**，且是"知识卡一致性"而非"内存安全证明"。
- 另有 2025 年 5 月由浙江大学、新加坡管理大学、渥太华大学等机构发布的 **291 个软件工程 benchmark 全览**（arXiv 综述），是梳理 Related Work 的高效入口。

### 四、workshop 通道：两条与阙疑高度匹配的线

**（1）LLM4Code（ICSE 的常设 workshop，2025 已是第二届/第三届）**
- 投稿类型：**Research papers 4–8 页**（含参考文献）、**Position papers 1–4 页**（含参考文献）。
- **默认 archival**："All accepted papers by default will appear in the ICSE 2025 workshop proceedings (i.e., the archival option)." 同时提供 **non-archival** 选项（camera-ready 只挂在 workshop 网站，不上 DBLP）。
- 评审：HotCRP 提交，**double-blind**，IEEE 格式（与 ICSE 2025 一致）。
- **Best paper awards：最多 10% 的论文**。
- 主题明确包含 "Datasets and Evaluation"（LLM4Code 的评测数据集、自动化数据集生成/增强、LLM4Code 的实证研究）与 "LLM-based code comprehension / program analysis / fault localization / vulnerability detection"。
- **已被 DBLP 收录**（dblp.org/db/conf/llm4code/llm4code2025）与 **IEEE Xplore 收录**（2025 IEEE/ACM International Workshop on Large Language Models for Code）。

**（2）LLMTrust 2026（首届，co-located with FSE 2026）**
- 全称：*The 1st International Workshop on Software Engineering for and with Trustworthy LLMs*，FSE 2026 合办，**2026-07-05 或 07-06，Montreal, Canada**。
- 组织者：Sumon Biswas（Case Western Reserve University）、Shibbir Ahmed（Texas State University）、Sayem Mohammad Imtiaz（Meta）、Hridesh Rajan（Tulane University）；TPC 含 Akond Rahman（Auburn）、Giang Nguyen（Meta）、Hong Jin Kang（University of Sydney）、Saikat Dutta（Cornell）、Mohammad Wardat（Oakland University）等 13 人。
- **投稿类型与页数（精确）**：Full papers **8 页含参考文献**（其中最多 2 页可为参考文献）；Short papers **5 页含参考文献**（最多 1 页参考文献）；Extended abstracts **1–5 页含参考文献**（**APC-free**）。
- **出版**：Proceedings 进入 **ACM Digital Library，作为 FSE 2026 Companion Proceedings 的一部分**——即 **archival 且被 ACM DL 索引**。
- 评审：Double-Anonymous，遵循 FSE 2026 方法。
- **关键日期**：投稿 **2026-02-19**；通知 **2026-03-24**；camera-ready **2026-04-02**；workshop **2026-07-05**。
- 两条主轴：①"Software Engineering **for** Trustworthy LLM-Based Systems"（principled architecture, testing, **verification**, monitoring, governance）；②"Software Engineering **with** Trustworthy LLM Integration"（rigorous, auditable use of LLM assistance，含 **provenance**、privacy、safety）。
- **对阙疑的匹配度极高**：阙疑的 "append-only 哈希链 + Merkle checkpoint + 独立对账器" 就是 **provenance + verification + auditable** 三个关键词的具象实现。

**（3）SEE-AIT 2026**（另一条 FSE 2026 的 workshop 线）：主题含 "LLM-Driven Workflows and Agentic Integration"，program 中出现 *JavaOracle: a specification-driven approach that leverages large language models*（specification-driven + LLM 的组合）。

### 四之二、ISSTA 2026：AI for SE 类别已成规模（54 篇）

本方向初稿只覆盖了 ICSE/FSE/ASE，遗漏了第四个 CCF-A 的 SE 会 **ISSTA**。补检索后确认：**ISSTA 2026 research track 的 "AI for Software Engineering" 类别共收录 54 篇论文**，其中与阙疑最相关的四篇是：

- **LLMutantKiller: Using Large Language Models to Generate Tests that Kill Mutants**（Farideh Khalili、Aidan Domondon、Harshit Garg、Frank Tip）——用 LLM 生成能"杀死变异体"的测试。**这与阙疑的变异测试口径（core 97.3% / all 81.5%）正面撞车**：阙疑已主动放弃把变异率当缺陷检测率，而 LLMutantKiller 恰恰在做"如何提高变异杀死率"。阙疑的 Related Work 必须引用它，并说明"我们不做变异杀死率，我们做的是知识卡判决的独立可验收性"。
- **KaPilot: LLM-Assisted Generation of Kani Specifications for Unsafe Rust Verification**（Minghua Wang、Yuxi Ling、Mingzhi Gao、Yuwei Liu、Lin Huang）——用 LLM 生成 Kani（Rust 的有界模型检查器）规格。**这是"用 LLM 生成形式化规格、再用非 LLM 工具验证"的又一条路线**，与阙疑"用 67 条规则验证知识卡"同构，且语言是 Rust 而非 C++。
- **DocPrism: Multi-Lingual Detection of Incorrectness Inconsistencies Between Code and Documentation**（Xiaomeng Xu、Zahin Wahab、Reid Holmes、Caroline Lemieux，University of British Columbia）——检测"代码与文档不一致"。**阙疑的"知识卡 vs C++ 语义一致性"本质上就是"文档 vs 代码一致性检测"的一个特例**，DocPrism 可作为最直接的邻居工作。
- **RICE: Harnessing LLMs and Historical Issues to Discover Internal Rust Compiler Errors**（Langyi Lu、Wei You、Bin Liang、Jianjun Huang）——用 LLM + 历史 issue 发现 Rust 编译器内部错误。

**新增的结论**：ISSTA 2026 的 54 篇 AI for SE 论文里，**"测试生成/演化"是最大子方向（约 10 篇）**，而"验证/正确性"约 5 篇——**"用非 LLM 的严格规则验收代码"这条路线在 ISSTA 里仍属少数派**。这对阙疑既是"空白仍在"的证据，也意味着**邻居工作的引用池足够小，可以逐篇读完全部相关工作**。

**为什么这一节要补 ISSTA**：ICSE/FSE/ASE 的 AI 验证生态已被本方向第一至四节覆盖，但 **ISSTA（International Symposium on Software Testing and Analysis）的主题是"测试与分析"，与"验证器"的语义距离比 FSE/ASE 更近**。ISSTA 2026 的 54 篇 AI for SE 论文说明：**该会的 AI 化程度已经不亚于 FSE**，且因为主题专精，**"用规则/性质验收代码"的论文在这里比在泛 ML 会议上更容易找到对口审稿人**。阙疑若在 ICSE 被拒，ISSTA 应排在转投清单的前列。

### 五、与阙疑的差距分析（诚实版）

| 维度 | SE 社区的现状 | 阙疑的现状 | 差距 |
|---|---|---|---|
| 基准规模 | Defects4C：248 buggy + 102 vulnerable 函数；FVAPPS：4,712 样本 | 15 条真实缺陷夹具；holdout 30 seeds；外部 corpus 40 条 | 数量差 1–2 个数量级 |
| 评测对象 | 24 个 SOTA LLM（Defects4C） | 0 个 LLM（阙疑验证的是"知识卡"，不是 LLM 输出） | **定位差异，不是缺陷**，但须在 Related Work 中说清 |
| 人类标注 | SE-Jury 与人类判断相关性对比；标注者间一致度 | 无人类标注预算 | 硬缺口，需在 Threats to Validity 中承认 |
| 形式化程度 | SPARK/Ada 形式化验证；Lean 4 定理；SMT 简化 | 67 条规则（44 block）+ 四态判决 + 哈希链 | 阙疑是"规则化"而非"形式化"，须避免 overclaim |
| 工件可复现 | ASE 2026 强制数据可用性声明 + 长期档案 DOI | 未申请 DOI | 可低成本补齐（Zenodo 免费） |
| 语言 | Java / Python / Ada / 多语言 | **C++（且是 C/C++ 这个被 ASE 2025 点名的空白）** | **这是阙疑唯一的、被顶会背书的差异化优势** |

## 对阙疑的 3 条具体行动

1. **在 2026-12-31 前把 *Defects4C* 与 *Verifying LLM-Generated Code in the Context of Software Verification* 读完全文并写进 Related Work**：前者用来论证"C/C++ 基准空白"（引用其原文 "there remains a significant gap in research on C/C++ program repair"），后者用来做最同构的对比项（SPARK/Ada vs 阙疑的规则引擎）。行动：在 `research/paper_v0.3.md` 的 Related Work 新增两段，并在 `_arch_v46/` 记录 `related_work_notes.md`。工具：arXiv HTML 版（arxiv.org/html/2510.11059v1、arxiv.org/html/2502.07728）便于精读。

2. **把阙疑包装成 LLMTrust 2026 风格的三关键词（verification + provenance + auditable）并准备一份 8 页 Full Paper 方案**：LLMTrust 的 Full paper 是 8 页含参考文献（最多 2 页参考文献），投稿截止 **2026-02-19**（已过，因此目标是 **2027 年对应的那一届**）。行动：在 `_arch_v46/` 写 `llmtrust_2027_plan.md`，含 (a) 8 页大纲；(b) 把 `tools/gate_engine.py` 3,826 行压成一张架构图 + 一段 67 条规则的分类表；(c) 用 `data/defect_fixtures/defects.json`（15 条）的 6/6 重注入检出作为核心结果。时间点：2027-01-31 前完成方案。

3. **把"证据可验收性"从模糊主张升级为可对照 SE-Jury 的可测量指标**：SE-Jury 用"与人类判断的相关性提升 29.6%–140.8%"作为核心量化。阙疑的对应物应是"独立对账器与内嵌引擎判决的一致率"。行动：新增一个脚本 `tools/reconcile_agreement_<batch>.py`（设计只登记在 `_arch_v46/`），跑出"内嵌引擎 67 条规则判决 vs 不依赖内核的独立对账器判决"的一致率（预期接近 100%，因为对账器是同一套规则的第二实现；若不为 100%，每个不一致点都是真 bug）。命令：`python tools/reconcile_agreement_<batch>.py --json > out.json`。时间点：2026-12-31 前跑通并写进论文 §Evaluation。

## 盲区（诚实标注）

- **我没有读到 ASE 2026 research track 的 CFP 原文**（researchr 的 research-track 链接返回的是会议议程页），因此"ASE 2026 的 early reject 与强制数据可用性声明"来自一篇中文博客转述，未与官方逐字核对。
- **FSE 2026 research track 的 CFP 原文同样未读到**；FSE 2026 的 session 与论文清单来自议程页（可信），但页数、rebuttal 机制未核实。
- **Defects4C 的"9M 提交"含义未完全核实**：摘要写 "a large collection of bug-relevant commits (9M in total), 248 high-quality buggy functions, and 102 vulnerable functions"，但"9M"是否指全部候选提交（而非最终入选缺陷）**未读全文确认**。
- **SE-Jury 的 "29.6%–140.8%" 是"相对提升"还是"绝对百分点"未核实**（摘要原文为 "improvements ranging from 29.6% to 140.8% over existing automatic metrics"，未说明口径）；引用时须标注为"相对提升，口径未核实"。
- **CWEval 的 "first" 自称**是论文自述，**我未独立检索是否存在更早的同时评功能与安全的基准**。
- **A.S.E 的具体评测数字（覆盖多少仓库、多少个 CWE、模型得分）未读取**，只确认了其定位与开源地址。
- **ICSE 2025 LLM4Code 的录用率未查到**（官方页面未公布）；"Best paper awards 最多 10%"是官方规则，不是录用率。
- **LLMTrust 2026 的投稿数与录用率未公布**（首届，截至检索时只有 2026-02-19 的投稿截止与 2026-03-24 的通知日期）。
- **"291 个软件工程 benchmark 全览"的具体 arXiv 编号与作者列表未核实**（只在中文二手报道中见到"浙江大学、新加坡管理大学、渥太华大学，2025 年 5 月"的描述），因此未在正文中给出引用格式。
- **FSE 2026 的 session 论文清单来自议程页**，其中部分标注为 Journal-First（即已在期刊发表），**不能当作 FSE 2026 的新论文引用**。
- **ISSTA 2026 的 "54 篇 AI for SE 论文"来自 GitHub 上的第三方归档（breezesway/SE-papers）**，**未与 ISSTA 2026 官方 program 逐条核对**；该归档页面在 #40 处被截断（41–54 号未显示），因此"54 篇"的完整性**未核实**。四篇论文的作者列表来自该归档，**未回 ACM DL / arXiv 核对**。
- 本文未涉及中国大陆政治、机构制裁、出口管制等议题；检索中出现的相关页面已主动排除。

## 来源

1. Wang, J., Xie, X., Hu, Q., Liu, S., Yu, J., Kong, J., Li, Y. (2025). *Defects4C: Benchmarking Large Language Model Repair Capability with C/C++ Bugs.* ASE 2025 main research paper. arXiv:2510.11059；DOI 10.1109/ASE63991.2025.00029。https://arxiv.org/abs/2510.11059 ；https://defects4c.github.io/
2. Zhou, X., Kim, K., Zhang, T., Weyssow, M., Gomes, L. F., Yang, G., Liu, K., Xia, X., Lo, D. (2025). *SE-Jury: An LLM-as-Ensemble-Judge Metric for Narrowing the Gap with Human Evaluation in SE.* ASE 2025，DOI 10.1109/ASE63991.2025.00214。arXiv:2505.20854。https://arxiv.org/abs/2505.20854
3. Peng, J., Cui, L., Huang, K., Yang, J., Ray, B. (2025). *CWEval: Outcome-driven Evaluation on Functionality and Security of LLM Code Generation.* LLM4Code 2025 @ ICSE 2025。arXiv:2501.08200。https://arxiv.org/abs/2501.08200
4. *A.S.E: A Repository-Level Benchmark for Evaluating Security in AI-Generated Code*（Tencent, 2025）。arXiv:2508.18106；OpenReview id `OJbIlRcaVR`；代码 https://github.com/Tencent/AICGSecEval ；https://arxiv.org/pdf/2508.18106v2
5. Dougherty, Q., Mehta, R. (2025). *Proving the Coding Interview: A Benchmark for Formally Verified Code Generation (FVAPPS).* LLM4Code 2025 @ ICSE 2025，DOI 10.1109/LLM4Code66737.2025.00017。https://conf.researchr.org/details/icse-2025/llm4code-2025-papers/21/Proving-the-Coding-Interview-A-Benchmark-for-Formally-Verified-Code-Generation
6. *Verifying LLM-Generated Code in the Context of Software Verification*（2025）。arXiv:2502.07728。https://arxiv.org/html/2502.07728
7. *LLM-as-a-Judge for Software Engineering: A Survey*（SE 2030, 2025-10-28）。arXiv:2510.24367。https://arxiv.org/abs/2510.24367
8. *Large Language Models for Code Generation: A Comprehensive Survey*（2025-03-04）。arXiv:2503.01245。https://arxiv.org/abs/2503.01245
9. LLM4Code 2025 Call for Papers（4–8 页 research / 1–4 页 position、默认 archival、double-blind、best paper ≤10%、非 archival 选项）。https://llm4code.github.io/2025/call/
10. DBLP: LLM4CODE@ICSE 2025（确认被 DBLP 收录）。https://dblp.org/db/conf/llm4code/llm4code2025
11. LLMTrust 2026 官网（FSE 2026 合办；8 页 full / 5 页 short / 1–5 页 extended abstract；ACM DL FSE 2026 Companion Proceedings；投稿 2026-02-19、通知 2026-03-24）。https://llmtrust2026.github.io/
12. FSE 2026 会议议程（LLM for SE 1/2/3、Agents、Verification 1、Benchmarking、Program Repair、Synthesis 等 session 与论文清单）。https://conf.researchr.org/track/fse-2026/fse-2026-research-papers
13. FSE 2026 *How to Submit*（全部 track 列表含 Artifacts / Tool Demonstrations / IVR / Journal-First）。https://conf.researchr.org/track/fse-2026/fse-2026-how-to-submit
14. ICSE 2025 Research Track Call for Papers（九个研究领域、"AI for Software Engineering" 与 "Software Engineering for AI" 的拆分）。https://www.conferences-computer.science/icse/2025/cfp/ICSE-2025.txt
15. *From Prompts to Properties: Rethinking LLM Code Generation with Property-Based Testing.* FSE 2025，DOI 10.1145/3696630.3728702。https://dl.acm.org/doi/10.1145/3696630.3728702
16. Li, Y. (2025-09-26). *Papers accepted by ASE 2025*（含 Defects4C 的一句话定位与 ASE 2025 统计）。https://liyiweb.com/posts/paper-accepted-by-ase-2025/
17. SEE-AIT 2026 Workshop (co-located with FSE 2026) 官网与 program。https://seeait.github.io/ ；https://seeait.github.io/program.html
18. ISSTA 2026 Research Papers（research track 页）与 ISSTA 2026 "AI for Software Engineering" 类别论文归档（54 篇；含 LLMutantKiller / KaPilot / DocPrism / RICE）。https://conf.researchr.org/track/issta-2026/issta-2026-research-papers ；https://github.com/breezesway/SE-papers/blob/main/2026/issta2026_research_track/category_AI_for_Software_Engineering.md
