# 695 · 方向 2：Software Verification Evaluation 最新进展（≥12 篇）

- **批次**：695 ｜ **方向**：2 — Software Verification Evaluation ｜ **日期**：2026-10-08
- **用途**：为 Queyi（投稿 NeurIPS 2027，Evaluations & Datasets）补 Related Work 与"SV-COMP 定位"论证。
- **检索工具**：`WebSearch`（通用网络检索）+ `WebFetch`（打开 arXiv abs / 官方页 / 报告 PDF）。
  **非** Scopus/DBLP/ACM DL 全文系统检索 ⇒ 本文件**不是**系统综述，是投稿前定向补漏。
- **真实性声明**：全部条目均实际联网检索；核验等级定义如下，**只允许**这三种：

| 等级 | 含义 |
|---|---|
| `核验-摘要` | 实际用 WebFetch 打开了页面（arXiv abs / 官方页 / PDF 全文），标题·作者·年份·关键数字已逐项核对 |
| `核验-检索` | 只在搜索结果的标题/摘要里见到，**未**打开原页 |
| `未核验` | 凭记忆，**落地前必须确认** |

> 本批**未编造**任何标题、编号、DOI、arXiv id 或数字。凡数字均标注来源页；SV-COMP 2026 的关键数字来自**逐页读过的报告 PDF**（`sosy-lab.org/research/pub/2026-TACAS.*.pdf`，42 页，含 `%%EOF` 完整）。
> 凡标 `核验-检索` 的条目，引用前请再开一次原文。

---

## 1. 文献条目（按主题分组）

### A. SV-COMP 系（竞赛报告 / witness 机制 / witness 校验独立研究）

**A1. Evaluating Software Verifiers for C, Java, and SV-LIB (Report on SV-COMP 2026)**
- 作者：Dirk Beyer（LMU Munich）、Jan Strejček（Masaryk University, Brno）
- 年份：2026 ｜ venue：TACAS 2026，LNCS 16506，pp. 461–502 ｜ DOI：`10.1007/978-3-032-22749-2_23`
- URL：https://sv-comp.sosy-lab.org/2026/index.php ｜ PDF：https://www.sosy-lab.org/research/pub/2026-TACAS.Evaluating_Software_Verifiers_for_C_Java_and_SV-LIB_Report_on_SV-COMP_2026.pdf
- **核验等级**：`核验-摘要`（下载 PDF 后逐页读取）
- 核心贡献（报告原文数字）：
  - **第 15 届** SV-COMP，TACAS 2026（Torino, Italy）。
  - 评估 **61 个 C 验证器 + 16 个 C witness 校验器**；**11 个 Java 验证器 + 3 个 Java 校验器**；**43 个验证器 + 13 个校验器**以活跃团队支持参赛，由 **12 个国家的 44 位代表**带领。
  - 任务集：**36 402 个 C 任务（6 类性质）** + **1 731 个 Java 任务（2 类性质）**；校验轨分析了 **229 118 个 C witness** + **135 个手工 witness**；另有 **254 个 SV-LIB 任务（3 验证器 + 1 校验器）**；Huawei 赞助 demo 类 `C.Huawei-Concurrency-Challenges`。
  - **2026 变更**（本报告 §1 "Quick Summary of Changes"，本批核验的新增事实）：
    1. 工具注册/资格审查流程简化；
    2. **jury 由"注册工具"代表组成**（2025 及以前为"合格工具"代表），职责略减；
    3. **类别系统化命名**：一律以语言前缀开头（`C.` / `Java.` / `SV-LIB.`）；`assert_java`→`valid-assert`、`runtime-exception`→`no-runtime-exception`；
    4. `FalsificationOverall` 更名 **`C.FalseOverall`**（并入 termination），**新增对偶元类 `C.TrueOverall`**（只计 True 得分）；
    5. C 任务从 33 353（2025）增至 **36 402**；Java 任务从 1 345 增至 **1 731**；
    6. **witness 格式升级到 2.1**，**停止支持 C 正确性 witness 的 1.0 格式**（仅"非活跃验证器"与 Java 例外）；
    7. 新增类别 **`C.termination.ViolationWitnesses`（17 个手工校验任务，非终止 witness，格式 2.1）**；
    8. **正确性 witness 校验 CPU 时限由 15 min 下调至 5 min**（动机：迫使验证器产出"比原任务更易校验"的 witness）；
    9. 后处理脚本重写（中间数据由 XML 改为 CSV）；2025-04 Frauenchiemsee 与 2026-03 Munich 两次 SV-COMP/Test-Comp Workshop。
  - **scoring（自 SV-COMP 2021 沿用，报告 Table 2）**：True correct **+2**、True incorrect **−32**、False correct **+1**、False incorrect **−16**；"witness 需校验但无校验器确认"称为 **correct-unconfirmed**。
  - **校验轨 scoring（自 2024 沿用，Table 3）**：True correct +2 / True incorrect −32 / False correct +1 / False incorrect −16；
    **无 expected result 的任务用"投票"定 expected**：≥2 个校验器给出结果且 **≥75% 一致**才采纳，否则该任务 **void**。
  - **void 口径变更**：自 **SV-COMP 2025** 起，元类别归一化时 $n_i$ **不再计入 void 任务**（此前计入）。
- 与 Queyi 的关系：**定位对照的主锚点**（见 §2）。SV-COMP 是"验证器排行榜"，Queyi 是"评估装置审计"。报告原文自陈目标是"precision 与 performance 的快照"，且把"可复现"列为教育目标之一——与 Queyi 的"评估器自省"是**不同对象**。Queyi 不得声称"首个做 witness 校验/可复现"。

**A2. Improvements in Software Verification and Witness Validation: SV-COMP 2025**
- 作者：Dirk Beyer、Jan Strejček ｜ 年份：2025 ｜ venue：TACAS 2025（ETAPS 2025, Hamilton, ON, Canada），Springer，pp. 151–186 ｜ DOI：`10.1007/978-3-031-90660-2_9`
- URL：https://www.phil.muni.cz/vyzkum/publikace/prehled/2549737 ｜ https://sv-comp.sosy-lab.org/2025/
- **核验等级**：`核验-摘要`（打开 muni.cz 出版页，读到官方摘要；报告 PDF 本次下载被截断，未读全文）
- 核心贡献（官方摘要原文数字）：
  - **第 14 届**；评估 **62 个验证器 + 18 个 witness 校验器**（自陈"迄今最大规模"）；
  - **35 个验证器 + 13 个校验器**活跃参赛，由 **12 个国家 33 位代表**带领；
  - **33 353 个 C 任务（6 类性质：reachability / memory safety / memory cleanup / overflows / termination / data races）**；
  - **674 个 Java 断言有效性任务**；另有 **673 个 Java 运行时异常任务（demo 类）**；
  - 校验轨**首次纳入 103 个手工 witness**；
  - **设立组织委员会（organization committee）**以应对竞赛复杂度增长。
- 与 Queyi 的关系：提供 2025→2026 的**逐年可比口径**（工具数、任务数、手工 witness 数），可支撑"竞赛规模在膨胀、但赛道结构在收敛"的叙述；也是 Queyi 表 2 中"SV-COMP 已具备独立复核"的证据。

**A3. Software Verification Witnesses 2.0**
- 作者：Dirk Beyer、Matthias Dangl 等 ｜ 年份：2024 ｜ venue：SPIN 2024（Model Checking Software）｜ DOI：`10.1007/978-3-031-66149-5_11`
- URL：https://link.springer.com/chapter/10.1007/978-3-031-66149-5_11 ｜ PDF：https://www.sosy-lab.org/research/pub/2024-SPIN.Software_Verification_Witnesses_2.0.pdf
- **核验等级**：`核验-检索`
- 核心贡献：提出基于 **YAML** 的 witness 格式 **2.0**（取代 1.0 的 GraphML），并给出新旧格式的实验对比。SV-COMP 2026 报告确认 2.0/2.1 为现行格式。
- 与 Queyi 的关系：Queyi 的"证据资产"（asan/ubsan 等）**不产出形式化 witness**；此条说明"验证器生态有机器可检验的证据标准"，而 Queyi 的 sanitizer 证据是**运行时报告**，二者证据范式不同 ⇒ 可写进 Limitations。

**A4. Correctness Witness Validation by Abstract Interpretation（Goblint Validator）**
- 作者：Simmo Saan、Michael Schwarz、Julian Erhard、Helmut Seidl、Sarah Tilscher、Vesal Vojdani
- 年份：2024 ｜ venue：VMCAI 2024（扩展版 arXiv 2023）｜ DOI：`10.1007/978-3-031-50524-9_4` ｜ arXiv：`2310.16572`
- URL：https://arxiv.org/abs/2310.16572
- **核验等级**：`核验-摘要`（打开 arXiv abs）
- 核心贡献：提出抽象解释算子 **`unassume`**，把 witness 不变式注入抽象状态以加速不动点收敛、提升精度；手工 witness 可将多线程程序校验 CPU 时间**降低 7%–47%**，并发现**模型检查器产出的 witness 能引导分析器证明其独立无法证明的性质**。
- 与 Queyi 的关系：**witness 校验器的独立研究**——证明"校验器本身也可能因 witness 而变强/变弱"。Queyi 的 Finding 7（LLM 与 sanitizer failure topology 正交）与此同调：**证据提供者会改变审计者行为**。

**A5. Non-termination Witnesses and Their Validation**
- 作者：Zsófia Ádám、Paulína Ayaziová、Levente Bajczi、Dirk Beyer、Marek Jankola、Marian Lingsch-Rosenfeld、Jan Strejček
- 年份：2025 ｜ venue：ASE 2025，pp. 1969–1981 ｜ DOI：`10.1109/ASE63991.2025.00164`
- URL：https://ieeexplore.ieee.org/document/11334721
- **核验等级**：`核验-检索`
- 核心贡献：把 witness 格式 2.0 扩展到**非终止（termination violation）**，给出生成与校验方法；正是 SV-COMP 2026 新增 `C.termination.ViolationWitnesses` 类的技术依据。
- 与 Queyi 的关系：说明 witness 机制**仍在扩张边界**（termination 刚被覆盖，correctness witness 在多类任务仍缺校验器）。可作为"SV-COMP 也承认自己能力边界"的例证，弱化 Queyi 与它的对立叙事。

**A6. SV-COMP 2026 官方站（index / participants / benchmarks 页）**
- 年份：2026 ｜ URL：https://sv-comp.sosy-lab.org/2026/index.php
- **核验等级**：`核验-摘要`（WebFetch 打开 index 页）
- 核心贡献：官方声明"witness format **2.0/2.1**（YAML）已发布，格式在 GitLab 维护"；给出竞赛目标（precision/performance 快照、建立基准集、**教育与可复现**）。results 页给出 validated 结果入口（`.../2026/results/results-validated/`）。
- 与 Queyi 的关系：Queyi §7/附录对比表的一手引用页；说明 SV-COMP 已把"reproducibility"写进目标（第 5 条），Queyi **不能**把"可复现"当成独有贡献。

### B. 基准构建方法论与"基准本身不可靠"批评

**B1. SWE-bench Goes Live!（SWE-bench-Live）**
- 作者：Linghao Zhang、Shilin He、Chaoyun Zhang 等（Microsoft）｜ 年份：2025 ｜ venue：**NeurIPS 2025 Datasets & Benchmarks** ｜ arXiv：`2505.23419`
- URL：https://arxiv.org/abs/2505.23419 ｜ 主页：https://swe-bench-live.github.io/
- **核验等级**：`核验-摘要`（打开 arXiv abs）
- 核心贡献：指出现有 SWE-bench 系**未持续更新、仓库覆盖窄、依赖人工构建**，带来**过拟合与数据污染**风险；提出**可实时更新**的基准：初版 **1 319 个任务 / 93 个仓库**（源自 2024 后真实 GitHub issue），**每个任务配 Docker 镜像**保证可复现执行；自动化流水线取代人工瓶颈；在受控条件下报告与静态 SWE-bench 存在**显著性能落差**。
- 与 Queyi 的关系：⭐ **与 Finding 5（合成 vs 真实）直接呼应**——静态/合成基准与"活的真实分布"之间系统性偏移。Queyi 的"标准化后 −17.92pp"是同一现象在验证器资产上的实例。

**B2. Reproducible Automated Program Repair Is Hard — Experiences With the Defects4J Dataset**
- 作者：Adam Krafczyk、Klaus Schmid ｜ 年份：2026 ｜ venue：EASE 2026（30th Int'l Conf. on Evaluation and Assessment in SE）｜ arXiv：`2604.26674`
- URL：https://arxiv.org/abs/2604.26674
- **核验等级**：`核验-摘要`（打开 arXiv abs）
- 核心贡献：对广泛使用的 **Defects4J**（**835 个缺陷 / 17 个 Java 项目**，Google Scholar 引用 >1 800）施加**比"用测试用例复现缺陷"更严**的可复现要求后发现：
  - **180 个（21.6%）缺陷不适合用于评估实验**；
  - 另有 **59 个（7.1%）测试套件明显欠约束**——删掉一条语句即可让所有测试通过，而人工补丁并非仅删代码；
  - 提出缺陷数据集的系统化需求清单 + 面向 Java APR 的评估框架（含 flaky test 检查）。
- 与 Queyi 的关系：⭐⭐ **与 Finding 3（环境省略静默失效）和 Finding 5（合成 vs 真实）双重呼应**。Defects4J 是"被 1800+ 论文当作 ground truth 的基准"，其 21.6% 不可用率说明**基准的可靠性从未被独立审计**——正是 Queyi 主张的"评估装置是第一类科学对象"的最强外部证据。

**B3. BugSwarm: Mining and Continuously Growing a Dataset of Reproducible Failures and Fixes**
- 作者：David A. Tomassi、Naji Dmeiri、Yichen Wang、Antara Bhowmick、Yen-Chuan Liu、Premkumar Devanbu、Bogdan Vasilescu、Cindy Rubio-González
- 年份：2019 ｜ venue：ICSE 2019 ｜ arXiv：`1903.06725`
- URL：https://arxiv.org/abs/1903.06725
- **核验等级**：`核验-摘要`（打开 arXiv abs）
- 核心贡献：用 CI 容器（Travis-CI）归档 fail→pass 运行对，构造**持续增长**的可复现缺陷集；已收集 **3 091 对 fail-pass（Java + Python）**，全部打包在可复现容器中。
- 与 Queyi 的关系：**"环境即测量装置"的先例**——BugSwarm 用容器固化环境以保可复现；Queyi 的 Finding 3 反过来证明**环境被省略时会静默改变结论**（WSL 60.07% → native 24.74%）。二者是同一枚硬币的两面。

**B4. Measuring what Matters: Construct Validity in Large Language Model Benchmarks**
- 作者：Andrew M. Bean、Ryan Othniel Kearns、…、Inioluwa Deborah Raji、Adam Mahdi 等（**29 位专家**）｜ 年份：2025 ｜ venue：**NeurIPS 2025 Datasets & Benchmarks** ｜ arXiv：`2511.04703`
- URL：https://arxiv.org/abs/2511.04703
- **核验等级**：`核验-摘要`（打开 arXiv abs）
- 核心贡献：系统评述 **445 个 LLM 基准**，指出在"被测现象 / 任务 / 打分指标"上的模式会**削弱构念效度（construct validity）**；给出 **8 条建议**与可操作指引。
- 与 Queyi 的关系：⭐ 把"评估是否测到了它声称的东西"提升为**方法论一级问题**。Queyi 的 Finding 1（+24pp 坍缩为 0）正是构念效度失败的一个实例：**分数变化测的不是能力，而是资产构成**。

**B5. The Benchmarking Epistemology: Validity Theory for Evaluating Machine Learning Models**
- 作者：Timo Freiesleben、Sebastian Zezulka ｜ 年份：2025/2026 ｜ venue：*Philosophy of Science*（2026 在线），arXiv `2510.23191`（v2 2026-10）
- URL：https://arxiv.org/abs/2510.23191
- **核验等级**：`核验-摘要`（打开 arXiv abs）
- 核心贡献：借心理测量学的**效度理论**，把"基准分数能支撑什么科学推断"所需的**隐含假设显式化**；用 ImageNet 与 Fragile Families Challenge 两个案例说明"分数 ≠ 能力/进度"的边界条件。
- 与 Queyi 的关系：为 Queyi 的"评估器审计协议"提供**认识论骨架**：Queyi 的 claim/证伪/四态审计，本质是把"分数→结论"的隐含假设写下来并逐一压力测试。

**B6. Why SWE-bench Verified no longer measures frontier coding capabilities（OpenAI 官方分析）**
- 作者：OpenAI ｜ 年份：2026-02 ｜ venue：OpenAI 官方博客
- URL（由二手来源给出）：https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/
- **核验等级**：`核验-检索`（**仅通过二手中文精读页 https://sherconan.github.io/ai-frontiers-cn/openai/swe-bench-verified 见到；OpenAI 原页 WebFetch 未取到正文 ⇒ 落地前必须确认原页可访问**）
- 核心贡献（二手转述，**数字需二次核实**）：审计 o3 未能解决的 **138 个问题（占数据集 27.6%）**，发现 **59.4% 含实质缺陷**——**35.5% 测试过严**（强制特定实现细节）、**18.8% 测试过宽**（超出 issue 描述）、**5.1% 其他**；并报告**跨厂商训练数据污染**（GPT-5.2 / Claude Opus 4.5 / Gemini 3 Flash 均可复现 gold patch）；**建议停用 SWE-bench Verified，改用 SWE-bench Pro**。
- 与 Queyi 的关系：⭐⭐ **基准退化的教科书案例**，与 Finding 5（合成 vs 真实构成抵消）同构：**基准的"难度/能力"信号被测试设计与污染双重污染**。Queyi 的"退化资产"实验是同类现象在验证器侧的受控版本。

**B7. Recent Advances in LLM Benchmarks against Data Contamination: From Static to Dynamic Evaluation**
- 作者：Simin Chen、Yiming Chen、Zexin Li、…、Tao Xie、Baishakhi Ray ｜ 年份：2025 ｜ venue：综述（arXiv）｜ arXiv：`2502.17521`
- URL：https://arxiv.org/abs/2502.17521
- **核验等级**：`核验-摘要`（打开 arXiv abs）
- 核心贡献：系统梳理"静态→动态"基准的演进，指出**动态基准缺乏标准化评估准则**这一关键空白，并提出动态基准的最优设计原则。
- 与 Queyi 的关系：Queyi 的"资产池演化"（Finding 4：operator ≡ greedy set-cover）也是一种"动态评估"；此文提醒：**动态化本身会引入新的不可比性**——正对应 Queyi 的"+24pp 构成效应"。

**B8. Test of Time: Rethinking Temporal Signal of Benchmark Contamination**
- 作者：Terry Jingchen Zhang、Gopal Dev、Ning Wang、…、Bernhard Schölkopf、Mrinmaya Sachan、Zhijing Jin
- 年份：2025/2026 ｜ venue：ACL 2026 ｜ arXiv：`2509.00072`
- URL：https://arxiv.org/abs/2509.00072
- **核验等级**：`核验-摘要`（打开 arXiv abs）
- 核心贡献：证明"训练截止后性能衰减"这一**污染信号高度依赖题目构造方式**——对同一份源材料，LLM 改写题与 cloze 题会给出**截然不同的时间模式**；在 LiveCodeBench 上验证：简单 LLM 改写即可**抹掉**该信号。
- 与 Queyi 的关系：**"测量装置的形式决定结论"** 的又一独立证据，与 Finding 1（口径/构成变化导致结论坍缩）同源。可用于强化"阴性/敏感性问题不是 Queyi 独有"。

**B9. Defects4J: A Database of Existing Faults to Enable Controlled Testing Studies for Java Programs（原始基准）**
- 作者：René Just、Darioush Jalali、Michael D. Ernst ｜ 年份：2014 ｜ venue：ISSTA 2014 ｜ DOI：`10.1145/2610384.2628055`
- URL：https://github.com/rjust/defects4j ｜ https://defects4j.org/
- **核验等级**：`核验-检索`（仅从 GitHub/搜索摘要见到；当前 release **2.0.1**，README 记 **854 bugs + 10 deprecated**；另有镜像记 835 bugs）
- 核心贡献：手工构建的 Java 缺陷库（缺陷 + 触发测试 + 人工补丁），成为 APR/FL 领域事实标准。
- 与 Queyi 的关系：作为 B2 的"被审计对象"引用；Queyi 无需重复其内容，只需指出"Defects4J 系（v1/v2）已被 B2 证明有 ~29% 的可靠性问题"。**注意**：任务卡提到 "v2/v3"，本批**未能核验到独立的 v2/v3 论文**——落地前需确认版本对应关系。

### C. 静态分析的误报/漏报与"评估陷阱"

**C1. An Empirical Study of False Negatives and Positives of Static Code Analyzers From the Perspective of Historical Issues**
- 作者：Han Cui、Menglei Xie、Ting Su、Chengyu Zhang、Shin Hwei Tan ｜ 年份：2024（arXiv）/ 2026（ACM TOSEM）｜ venue：ACM TOSEM ｜ DOI：`10.1145/3849701` ｜ arXiv：`2408.13855`
- URL：https://arxiv.org/abs/2408.13855
- **核验等级**：`核验-摘要`（打开 arXiv abs）
- 核心贡献：**首个**从"维护者/用户/研究者已确认并修复的历史 issue"角度系统研究 FP/FN：**350 个历史 issue × 3 个分析器（PMD、SpotBugs、SonarQube）**；分析根因与触发程序特征；提出变质测试策略，**新发现 14 个 FP/FN（11 个被确认、9 个已修复）**。（注：ACM 版摘要称 **1257 个 issue × 4 个分析器**，口径与 arXiv v1 不同——引用时须选一个版本并注明。）
- 与 Queyi 的关系：⭐ Queyi 的 Finding 2（38.4% 盲区、13/34 类型 >50% 盲）与 Finding 6（家族聚类 deff≈4）是同一问题在"sanitizer/编译器/链接器"资产族上的量化：**工具族的 FP/FN 有结构，不是独立同分布**。

**C2. Reducing False Positives in Static Bug Detection with LLMs: An Empirical Study in Industry**
- 作者：Xueying Du、Jiayi Feng、Yi Zou、Wei Xu、Jie Ma、Wei Zhang、Sisi Liu、Xin Peng、Yiling Lou（腾讯）
- 年份：2026 ｜ venue：arXiv（另有 ACM DOI `10.1145/3786583.3786910`）｜ arXiv：`2601.18844`
- URL：https://arxiv.org/abs/2601.18844
- **核验等级**：`核验-摘要`（打开 arXiv abs）
- 核心贡献：在腾讯广告业务的大型企业代码上，对**企业定制静态分析器**构建 **433 个告警（328 FP / 105 TP，3 类缺陷）**数据集；**每个告警人工排查需 10–20 分钟**；LLM+静态分析混合可将 **94–98% 的 FP 消除**且保持高召回；单告警成本低至 2.1–109.5 秒。
- 与 Queyi 的关系：**工业级 FP 实证**，支撑"误报是静态分析评估的核心痛点"；也为 Queyi 的"证据资产组合"提供动机——若单资产 FP 率高，组合选择（FD/E 算子）的价值就更高。

**C3. UBfuzz: Finding Bugs in Sanitizer Implementations**
- 作者：Shaohua Li、Zhendong Su ｜ 年份：2024 ｜ venue：ASPLOS 2024 ｜ arXiv：`2401.04538`
- URL：https://arxiv.org/abs/2401.04538
- **核验等级**：`核验-摘要`（打开 arXiv abs）
- 核心贡献：用 UB 程序生成器 + **crash-site mapping** oracle 对 GCC/LLVM 的 sanitizer 实现做差分测试，**五个月发现 31 个 bug**，揭示 sanitizer 存在**严重漏报（false negative）**。
- 与 Queyi 的关系：⭐⭐ **直接支撑 Finding 2 与 Finding 3**：sanitizer 本身不可靠（漏报），且**同一程序在不同编译器/优化下的 UB 报告会不同**——这正是 Queyi"环境省略静默失效"的机制性解释：**换环境 = 换证据装置**。

**C4. Threats to Validity in Software Engineering — hypocritical paper section?**
- 作者：Roberto Verdecchia 等 ｜ 年份：2024 ｜ venue：ESEM 2024 ｜ DOI：`10.1145/3674805.3686691`
- URL：https://dl.acm.org/doi/10.1145/3674805.3686691 ｜ PDF：https://robertoverdecchia.github.io/papers/ESEM_2024.pdf
- **核验等级**：`核验-检索`
- 核心贡献：从**六个方面**分析 SE 论文中的 threats-to-validity 如何被撰写，指出"威胁声明"常被形式化/模板化（标题即暗示"是否沦为走过场"）。
- 与 Queyi 的关系：Queyi 的 Limitations 若只写模板化威胁，会被此类批评命中；应把"环境/口径/构成"写成**可执行的审计结果**而非声明。

### D. 可复现性

**D1. Large Language Models for Software Engineering: A Reproducibility Crisis**
- 作者：Mohammed Latif Siddiq、Arvin Islam-Gomes、Natalie Sekerak、Joanna C. S. Santos
- 年份：2025 ｜ venue：arXiv（投 EMSE）｜ arXiv：`2512.00651`
- URL：https://arxiv.org/abs/2512.00651
- **核验等级**：`核验-摘要`（打开 arXiv abs）
- 核心贡献：**首个大规模** LLM-for-SE 可复现性实证：系统挖掘并分析 **2017–2025 年间 640 篇论文**；提出**七类 reproducibility smell**（Code/Execution、Data、Documentation、**Environment & Tooling**、Versioning、Model、Access & Legal）；关键发现：**artifact badge 常只证明"有制品"，不保证可执行保真度与长期可复现**；提出 **Reproducibility Maturity Model (RMM)**。
- 与 Queyi 的关系：⭐ 与 Finding 3 强相关——**"Environment & Tooling"被单列为一类 smell**，与 Queyi"环境是 measurement tuple 的正式组件"一致；同时"badge ≠ 可复现"提醒 Queyi 不得把"可复现"写成"已被独立复现"（与 693-E6 N3 结论一致）。

---

## 2. SV-COMP vs Queyi 定位区别表（必须）

> 一句话：**SV-COMP 回答"哪个验证器在给定任务上表现好"；Queyi 回答"评估结果在评估器被审计后还成立吗"。**

| 维度 | **SV-COMP 2026**（verifier leaderboard） | **Queyi**（evaluator audit） |
|---|---|---|
| **比较对象** | **验证器 / 校验器**（在固定任务集上排名） | **评估装置本身**（资产池 + 口径 + 环境 + 标签 + 分母） |
| **判定来源** | 任务自带 expected result + **独立 witness 校验器复核**（confirm/refute）；无 expected 时用 **≥2 校验器、≥75% 投票** | 由**被审计装置自身**产出，再经 **Evaluator-Audit Protocol**（claim / 8 类失败模式 / 证伪 / 四态结果）反查 |
| **分母口径** | 元类别分数 $(\sum s_i/n_i)\cdot(\sum n_i)/k$；**void 任务自 2025 起不计入 $n_i$** | **unknown 与 miss 严格分离**；分母"含/不含 unknown"逐处显式声明；报告 $\Delta_{\text{unknown}}$ |
| **是否审计"未知"状态** | **不单列**：超时/未解算作"未解答/未确认"，四态语义不存在（只有 correct / incorrect / correct-unconfirmed） | **unknown 是一等公民**：Finding 3 的核心量就是 $\Delta_{\text{unknown}}=0$ 下的静默退化 |
| **是否审计环境** | 环境被**规范化**（统一容器/资源限制），是控制变量而**非审计对象** | 环境是 **measurement tuple 的正式组件**；跨 profile 报告三组件指标（Finding 3：WSL 60.07% → native 24.74%） |
| **是否有第三方裁判** | **有**：竞赛基础设施 + 组织委员会 + jury + 独立校验器 + Zenodo 复现包 | **暂无外部裁判**（693-A 人类裁决材料包已备齐但**未执行**；AI 双标 κ=0.495）⇒ 论文不得声称"已被独立复现" |
| 演化/时间轴 | 15 届年度快照，跨届可比 | 资产池演化 → 主张"看起来的改进可能是构成效应"（Finding 1/4） |
| 阴性结果的地位 | 排名即结果（弱者自然落后） | **阴性发现是一级产物**（+24pp 坍缩、演化假设失败、正交性） |
| 证据范式 | 形式化 **witness**（YAML/GraphML，机器可检） | **运行时报告**（asan/ubsan/告警/链接器），非形式化 witness |

**诚实边界（不得稻草人化）**：SV-COMP **已经**有 witness 校验、统一环境、复现包与第三方裁判——Queyi 的差异**不是**"第一个做可审计性"，而是**审计对象换了**：把"评估装置"当作对象，给出可执行协议 + 能力边界图 + 阴性发现实证。SV-COMP 不回答的问题（Queyi 的贡献区）：**同一批数据在口径/环境/资产构成变化下结论是否幸存**，以及**评估器自身迭代时如何防止"表观改进"实为构成效应**。

---

## 3. 可以引用的基准和方法论

| 用途 | 建议引用 | 说明 |
|---|---|---|
| 定位对照（必引） | **A1**（SV-COMP 2026 报告）+ **A2**（SV-COMP 2025 报告）+ **A6**（官网） | 用已核验口径：15 届 / 61+16 C 工具 / 36 402 C 任务；**不要**引未核验的任务数 |
| witness 机制与校验（诚实边界） | **A3**（Witnesses 2.0）、**A4**（Goblint unassume）、**A5**（Non-termination witnesses） | 证明"SV-COMP 已具备独立复核与格式标准" |
| 基准退化/不可靠（Finding 3 & 5） | **B2**（Defects4J 21.6% 不可用）、**B6**（SWE-bench Verified 59.4% 有缺陷）、**B1**（SWE-bench-Live）、**B3**（BugSwarm） | ≥2 篇要求已满足，实为 4 篇 |
| 构念效度/认识论（评估方法论） | **B4**（445 基准 / 29 专家 / 8 建议）、**B5**（效度理论） | 把 Queyi 的"口径纪律"升格为方法论 |
| 动态评估/污染 | **B7**（静态→动态）、**B8**（时间信号） | 支撑"资产池演化会引入不可比性" |
| 静态分析 FP/FN（Finding 2/6） | **C1**（350 issue × 3 工具）、**C2**（433 告警工业实证）、**C3**（UBfuzz 31 bugs） | 证明工具族漏报/误报有结构 |
| 可复现性（Finding 3） | **D1**（640 论文 / 7 类 smell / RMM）、**C4**（threats to validity） | Environment & Tooling 被单列；badge ≠ 可复现 |

**不建议引用**：B6 的**具体数字**（59.4% / 35.5% / 18.8%）——仅 `核验-检索` 级，且原始 OpenAI 页本次未取到正文；如需引用，先打开 OpenAI 原页并注明抓取日期。

---

## 4. 关键发现与趋势总结

1. **"评估装置"正在被系统性质疑（2024→2026 趋势）**。B2/B4/B6/D1 都在做同一件事：**审计被广泛信任的基准/工具**。Queyi 的"评估器审计协议"不是孤例，而是这一趋势在**软件验证证据装置**上的实例——这既降低 Queyi 的"新颖性叙事"，也**强化其合法性**（有方法论谱系）。

2. **"未知/环境/口径"三件事，主流基准仍未系统处理**。
   - SV-COMP：环境被规范化、unknown 不单列；
   - SWE-bench 系：环境靠 Docker 固化，但**测试设计缺陷（过严/过宽）**成为主要失效源（B6）；
   - Defects4J：环境可复现，但**测试套件欠约束（7.1%）与不可用缺陷（21.6%）**仍存在（B2）。
   ⇒ Queyi 的差异化点应精确表述为"**把 unknown 与环境作为被审计变量，而非控制变量**"。

3. **"基准退化"是跨领域共性**：合成→真实偏移（B1/B2）、污染（B6/B7/B8）、测试设计缺陷（B6/B2）。Queyi 的 Finding 5（标准化后 −17.92pp）与 Finding 1（+24pp 坍缩）是**同一现象在验证器资产上的受控再现**。

4. **witness 生态在扩张但仍有大片空缺**：A5 显示 termination 才刚被 witness 覆盖；A1 的 Table 1 显示大量类别 correctness witness "不支持"或"仅 demo"。⇒ "SV-COMP 有第三方裁判"是真的，但**裁判覆盖率有限**——Queyi 可在诚实边界里指出这一点。

5. **可复现 ≠ 可信**：D1 明确指出 artifact badge 只证明"有制品"，不保证执行保真度。Queyi 必须避免把"可复现"写成"已被独立复现"（与 693-E6 §3.3 一致）。

6. **对 Queyi 的 3 条直接动作**：
   - Related Work 增补 §2 定位表（本文件），并把 A1/A2 作为一手引用；
   - Limitations 增补"无第三方裁判"（引 A1 的 jury/validator 机制作对照）+ "witness 覆盖有限"（引 A1 Table 1）；
   - Finding 5 增补外部锚点 **B2**（21.6%）与 **B6**（59.4%），把"合成 vs 真实"从孤立观察升格为领域共识。

---

## 5. 检索记录（可复核表）

| # | 检索词 | 日期 | 工具 | 命中的可用条目 |
|---:|---|---|---|---|
| 1 | `SV-COMP 2025 International Competition on Software Verification report TACAS 2025` | 2026-10-08 | WebSearch | A2（+ A1 线索） |
| 2 | `SV-COMP 2026 witness validation benchmark 15th competition` | 2026-10-08 | WebSearch | A1、A6 |
| 3 | `SWE-bench Verified critique benchmark contamination validity 2025` | 2026-10-08 | WebSearch | B6 线索 |
| 4 | `static analysis false positives empirical study C++ 2024 2025` | 2026-10-08 | WebSearch | C1 |
| 5 | `Defects4J version 2.0 3.0 benchmark Java faults empirical study 2024 2025` | 2026-10-08 | WebSearch | B2、B9 |
| 6 | `"benchmark" validity threat software engineering flaky tests reproducibility study 2024 2025` | 2026-10-08 | WebSearch | C4、D1 |
| 7 | `ManyBugs BugSwarm benchmark real world bugs reproducibility study` | 2026-10-08 | WebSearch | B3 |
| 8 | `witness validation independent research soundness correctness witness SV-COMP criticism` | 2026-10-08 | WebSearch | A4、A5、A3 |
| 9 | `SWE-bench Multimodal SWE-bench Live SWE-bench Pro benchmark 2025 2026` | 2026-10-08 | WebSearch | B1 |
| 10 | `Defects4J benchmark overfitting automated program repair reproducibility critique` | 2026-10-08 | WebSearch | B2 |
| 11 | `static analysis false positive classification taxonomy empirical study industrial` | 2026-10-08 | WebSearch | C2 |
| 12 | `benchmark construct validity machine learning evaluation leaderboard gaming degenerate benchmark` | 2026-10-08 | WebSearch | B4、B5 |
| 13 | `reproducibility crisis software engineering experiments empirical study 2024 2025` | 2026-10-08 | WebSearch | D1 |
| 14 | `sanitizer false negatives undefined behavior environment compiler optimization silent failure study` | 2026-10-08 | WebSearch | C3 |
| 15 | `"Measuring What Matters" construct validity large language model benchmarks NeurIPS 2025 arXiv` | 2026-10-08 | WebSearch | B4 |
| 16 | `openai.com SWE-bench Verified no longer measures frontier coding capabilities analysis` | 2026-10-08 | WebSearch | B6 |
| 17 | `"Correctness Witness Validation by Abstract Interpretation" Saan TACAS 2024` | 2026-10-08 | WebSearch | A4 |
| 18 | `"Threats to Validity" software engineering ESEM 2024 paper Verdecchia` | 2026-10-08 | WebSearch | C4 |
| 19 | `"Software Verification Witnesses 2.0" SPIN 2024 Beyer Dangl` | 2026-10-08 | WebSearch | A3 |
| 20 | `"Non-termination witnesses and their validation" ASE 2025 Adam Beyer Strejcek` | 2026-10-08 | WebSearch | A5 |

**WebFetch 打开过的页面（= 核验-摘要 依据）**：
`fi.muni.cz/~xstrejc/publications/tacas2026.pdf`（失败，转 sosy-lab PDF）· `sosy-lab.org/research/pub/2026-TACAS.*.pdf`（**42 页，完整读取**）·
`sv-comp.sosy-lab.org/2026/index.php` · `phil.muni.cz/.../2549737`（SV-COMP 2025 摘要）·
`arxiv.org/abs/2408.13855` · `arxiv.org/abs/2601.18844` · `arxiv.org/abs/2401.04538` · `arxiv.org/abs/2505.23419` ·
`arxiv.org/abs/2604.26674` · `arxiv.org/abs/1903.06725` · `arxiv.org/abs/2511.04703` · `arxiv.org/abs/2510.23191` ·
`arxiv.org/abs/2512.00651` · `arxiv.org/abs/2502.17521` · `arxiv.org/abs/2509.00072` · `arxiv.org/abs/2310.16572`

**未能核验/受限说明**：
- SV-COMP 2025 与 2026 的 **muni.cz 镜像 PDF 被截断**（无 `%%EOF`，0 页可解析）；SV-COMP 2026 改用 sosy-lab 完整 PDF 成功。
- **OpenAI 原页** `openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/` 本次 WebFetch 未取到正文 ⇒ B6 降级为 `核验-检索`。
- 任务卡提到的 **Defects4J "v3"** 本批**未检索到对应论文**；"v2/v3" 与 release 版本（2.0.1）的对应关系**未核验**。

---

## 6. 与 684 / 685 / 693 已有调研的关系（新增了什么）

| 既有批次 | 已覆盖 | 本批（695-D2）**新增** |
|---|---|---|
| **684**（D Related Work 18 篇） | 子模优化、主动测试、评估治理/Goodhart（Datasheets/Model Cards/Pineau/Raji） | **软件验证领域的一手竞赛报告**（A1/A2）与 **witness 机制**（A3/A4/A5）——684 完全没有 SV-COMP 侧材料 |
| **685**（A1 前沿理论 39 篇） | 子模、主动学习、评估方法论（HELM/Leaderboard Illusion 等）、信息论 | **基准构建与批评的实证文献**（B1–B9：SWE-bench-Live / Defects4J / SWE-bench Verified / 构念效度）——685 的 eval 领域以 LLM 榜为主，**无软件验证/APR 基准** |
| **693-E6**（新增 N1–N5） | N1 HOW2BENCH 检查单、N2 fuzzer vs 静态分析互补、N3 SV-COMP 2026（摘要级）、N4 NeurIPS track、N5 LLM-Judge | **把 N3 从"摘要级"升级为"全文级"**（本批 A1 逐页核验，给出 2026 全部变更与 scoring）；**新增 witness 校验的独立研究**（A4/A5）；**新增 4 篇基准退化/批评**（B2/B4/B6/B1）；**新增静态分析 FP/FN 实证**（C1/C2/C3）；**新增可复现性**（D1/C4）。N2 仍保留为"跨工具族互补"锚点，本批 C1/C3 补充其机制解释 |

**去重声明**：本文件**不重复登记** 684 的 18 篇、685 的 39 篇、693-E6 的 N1–N5。SV-COMP 2026 报告（693-E6 的 N3）在本批**升级核验等级并大幅扩充事实**，属"同一文献的深度化"，非新增篇目。
