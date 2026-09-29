# 方向 78：程序合成（SyGuS、FlashFill、DreamCoder、AlphaCode/Codex、LLM 时代代码生成）

> 调研时间：2026-09-29｜调研员：方向 68–79 组｜真实检索 **13 次**（9 次 WebSearch + 4 次 WebFetch 逐字取数）
> 面向问题：**程序合成能否用来"自动生成验证规则 / 测试夹具"？** 以及：**阙疑的 595 个 .py 工具与这个领域是什么关系？**

---

## 核心结论

1. **FlashFill 证明了一件事：只要把目标语言限制在一个足够小的 DSL 里，"从示例合成程序"是可以在几分之一秒内完成的。** Sumit Gulwani（微软研究院），*Automating String Processing in Spreadsheets using Input-Output Examples*，**POPL 2011**（获 **Most Influential POPL Paper Award**）。论文逐字：*"We describe the design of a **string programming/expression language that supports restricted forms of regular expressions, conditionals and loops**."* 且 *"The synthesis algorithm is **very efficient taking fraction of a second for various benchmark examples**."* 还提到一个著名的"黄金测试"：*"The prototype tool has met the golden test – it **has synthesized part of itself**."* **对阙疑的直接意义：67 条规则本身就是一个小型 DSL（对 C++ 代码结构的谓词语言）。因此"用 PBE 合成新规则"在原理上不是幻想——但前提是必须先把规则语言形式化。**
2. **AlphaCode 是"大规模采样 + 廉价过滤 + 聚类选优"的最强工程范例，而它的数字恰好揭示了这条路线的天花板与代价。** DeepMind（arXiv:2203.07814, 2022；*Science* 378:1092）：在 **10 场** Codeforces 比赛（每场 **>5,000** 人）上平均排名 **top 54.3%**，估计 Codeforces 评分 **1238**（近 6 个月用户的前 **28%**）。**关键工程数字**：每题最多生成 **1,000,000 个样本**；用题目自带的样例测试过滤**去掉约 99%**；再按程序行为聚类，**最终只提交最多 10 个**；平均每题实际提交 **2.4 次**。**诚实的天花板**：约 **10% 的题目连一个能通过样例测试的程序都找不到**；动态规划与构造性算法明显更差；论文自己承认 *"**Loss is a poor proxy for solve rate**"*。**top 54.3% 的含义是"略高于中位数"——这是"大规模搜索 + 廉价 oracle"在开放问题上的真实水平，不是超人。**
3. **2026 年 ISSTA 的一篇复现研究给了阙疑一个"已发表的方法学背书"：覆盖率与变异分数并不能可靠预测测试套件的真实缺陷检测能力。** Zhao, Zhou, Cohen（University of Toronto），*Do Coverage and Mutation Scores of LLM-Generated Test Suites Correlate with Their Effectiveness?*，**ISSTA 2026**（PACMSE vol. 3, DOI `10.1145/3832093`）。规模：**11 个 SOTA LLM**（13 个配置）、**8,268 个生成测试套件 / 101,123 个测试用例**、基于 **Defects4J v3.0**（854 个缺陷、17 个项目、精选 **318 个 buggy 焦点方法**）。结论逐字：当被测代码**本身可能有 bug** 时，*"覆盖率作为缺陷检测有效性的指标变得不可靠"*（三种视图下相关性**一律为弱**），且**变异分析不适用**。**这与阙疑已经做出的判断完全一致**——项目上下文记录 *"变异 core 97.3% / all 81.5%（**已放弃当作缺陷检测率**）"*。**这不是阙疑的失败，而是一个与顶会复现研究同向的方法学发现。**

---

## 精确数字与案例

### 一、FlashFill / PBE（POPL 2011）：DSL 是可行的前提

**来源**：微软研究院官方页面（标注 *"Most Influential POPL Paper Award"*，PoPL'11, January 26-28, 2011, Austin, Texas）；ACM DL `10.1145/1926385.1926423`。

**论文摘要逐字**：
> *"We describe the design of a **string programming/expression language** that supports restricted forms of regular expressions, conditionals and loops. The language is expressive enough to represent a wide variety of string manipulation tasks that end-users struggle with. We describe an algorithm based on several novel concepts for synthesizing a desired program in this language from **input-output examples**. The synthesis algorithm is **very efficient taking fraction of a second for various benchmark examples**."*

**算法特性（逐字）**：
- *"it can **rank multiple solutions** and has **fast convergence**"*
- *"it can **detect noise in the user input**"*
- *"it supports an **active interaction model** wherein the user is prompted to provide outputs on inputs that may have multiple computational interpretations"*

**落地**：*"The algorithm has been implemented as an interactive add-in for Microsoft Excel spreadsheet system."* → 即 Excel 2013 起的 **Flash Fill** 功能（第三方中文资料，CSDN 2026-06-02 / 2026-06-03 均记载）。

**"黄金测试"逐字**：*"The prototype tool has met the golden test – it has **synthesized part of itself**, and has been used to solve problems **beyond authors' imagination**."*

**对阙疑最关键的三条可迁移设计**：
1. **必须限制在 DSL 内**：论文明确说语言"supports **restricted forms** of regular expressions"。**没有 DSL，就没有可判定的搜索空间。** 阙疑的 67 条规则（block 44 / warn 16 / advice 7）在形式上是一个"对 C++ 代码结构的谓词语言"，**但据我所知它没有形式化语法定义**——这是一个必须补上的前置工作。
2. **必须能排序多个解**：*"rank multiple solutions"*。PBE 天然是**一对多**的（一组示例可以被无穷多个程序满足）。**阙疑在自动生成规则时也会遇到同样问题**：多条候选规则可能都能通过 30 条 holdout。**必须有排序准则**（与方向 76 的"格值适应度"问题直接相连）。
3. **必须有主动交互**：*"active interaction model wherein the user is prompted to provide outputs on inputs that may have multiple computational interpretations"*。**这直接反驳了"全自动"的幻想**：FlashFill 这个被数十亿人使用的功能，其设计**显式包含向用户追问**的环节。**阙疑的"人工确认新规则"不是缺陷，而是 PBE 的标准组成部分。**

### 二、SyGuS：把合成问题标准化，然后发现它很难

**SyGuS**（Syntax-Guided Synthesis）把合成问题标准化为：给定一个语法（grammar）+ 一个正确性规格（spec），合成一个满足规格的表达式。**SyGuS-Comp** 是其竞赛。

**SyGuS-Comp 2018（第 5 届）的关键数字（arXiv:1904.07146, 2019-04-13，标题 *SyGuS-Comp 2018: Results and Analysis*）逐字**：
> *"In the 5th SyGuS-Comp, **five solvers** competed on **over 1600 benchmarks** across various tracks."*

**赛事历史（sygus-org.github.io/comp/ 逐字）**：*"The 5th SyGuS Competition, **SyGuS-Comp 2018** was held at the FLoC Olympic games at the 2018 Federated [Logic Conference]"*。搜索结果显示 **2018 年是第 5 届**，此后**我没有找到 SyGuS-Comp 2019 及以后的记录**。

**对阙疑的三条启示**：
1. **只有 5 个求解器参赛**——这是一个**小而窄的研究领域**，不是工程主流。**不要指望"用 SyGuS 求解器自动生成规则"这条路线有成熟的工具链。**
2. **1600+ 个 benchmark**——说明该领域的进展是**以 benchmark 驱动的**。**这与阙疑的 37 实卡 / 67 规则在方法论上是同一种东西**：一个小规模、人工构造的、可核查的测试集。**这是阙疑可以正面自我定位的地方**：它做的不是"通用合成"，而是"领域 benchmark + 可复算判决"。
3. **赛事在 2018 年后似乎停办**（**未核实**，见盲区）——一个曾经活跃的竞赛领域停办，通常意味着**问题比预期难、或工业界不关心**。**这是对"自动生成验证规则"路线的一个冷静提醒。**

### 三、DreamCoder（2020/2021）：库学习 = "自动扩展知识库"的学术原型

**来源**：Kevin Ellis, Catherine Wong, Maxwell Nye, Mathias Sablé-Meyer, Luc Cary, Lucas Morales, Luke Hewitt, Armando Solar-Lezama, Joshua B. Tenenbaum（MIT），arXiv:2006.08381（v1 **2020-06-15**）；发表于 **PLDI 2021**（DOI `10.1145/3453483.3454080`）。

**摘要逐字（这是本方向最贴近"自动扩展 37 实卡"的一段）**：
> *"We present DreamCoder, a system that learns to solve problems by writing programs. It **builds expertise by creating programming languages for expressing domain concepts**, together with neural networks to guide the search for programs within these languages. A **'wake-sleep' learning algorithm alternately extends the language with new symbolic abstractions** and trains the neural network on imagined and replayed problems. DreamCoder solves both classic inductive programming tasks and creative tasks such as drawing pictures and building scenes. **It rediscovers the basics of modern functional programming, vector algebra and classical physics, including Newton's and Coulomb's laws.** Concepts are built compositionally from those learned earlier, yielding **multi-layered symbolic representations that are interpretable and transferrable to new tasks**, while still growing scalably and flexibly with experience."*

**必须点破的两点**：
1. **"rediscovers ... Newton's and Coulomb's laws" 与方向 76 中 AI Feynman 的问题是同一个**：它**恢复的是人类已知的定律**，不是发现新定律。**DreamCoder 的贡献是"学会了表达这些定律的语言"，不是"发现了这些定律"。**
2. **"wake-sleep 交替扩展语言 + 训练网络"就是阙疑设想的"自动扩展 37 实卡"的学术原型**：DreamCoder 的"库"（library）对应阙疑的"知识卡集"，DreamCoder 的"新符号抽象"对应"新规则/新卡"。**关键差别**：DreamCoder 的抽象是从**合成成功的问题**中抽取的（**有明确的成功信号**）；阙疑的"新规则"必须从**判决账本**中抽取（**信号来自 30 条 holdout，噪声大得多**）。

**DreamCoder 的量化结果**：摘要中**没有给出任何具体数字**（如"解决了多少问题""提升多少倍"）。**第三方来源（simons.berkeley.edu 的 Kevin Ellis 讲稿，2022-12-13）逐字**：*"Library learning interacts synergistically with neural synthesis: **bootstrapping, more than sum of parts**"*——这是定性表述。**因此我无法给出 DreamCoder 的具体改进数字（见盲区）。**

### 四、AlphaCode（2022）：大规模采样路线的完整工程数字

**来源**：AlphaCode 团队（13 位共同第一作者：Yujia Li, David Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser, Rémi Leblond, Tom Eccles, James Keeling, Felix Gimeno, Agustin Dal Lago, Thomas Hubert, Peter Choy, Cyprien de Masson d'Autume；另有 Pushmeet Kohli, Nando de Freitas, Koray Kavukcuoglu, Oriol Vinyals 等），arXiv:2203.07814（2022-03），*Science* 378:1092。

**核心结果（逐字）**：
> *"In simulated evaluations on recent programming competitions on the Codeforces platform, AlphaCode achieved on average a ranking of **top 54.3%** in competitions with **more than 5,000 participants**."*

**完整数字表**：

| 项 | 数值（逐字） |
|---|---|
| 平均排名 | **top 54.3%**（10 场比赛，2021-12-01 至 2021-12-28） |
| 参赛规模 | 每场 **> 5,000** 人（Codeforces 平台活跃用户 > 500,000） |
| 估计 Codeforces 评分 | **1238**，近 6 个月用户的前 **28%** |
| 每题采样上限 | **1,000,000** 个样本 |
| 采样多样性 | 一半 Python、一半 C++ |
| **过滤去除比例** | *"Filtering removes approximately **99%** of model samples"* |
| 过滤后仍剩余 | *"thousands of samples per problem"*，甚至 *"tens of thousands of candidate samples"* |
| 聚类后最终提交 | **最多 10 个** |
| 每题平均实际提交 | **2.4 次** |
| 验证集求解率 | **34.2%**（10@1M） |
| 测试集求解率 | **29.6%**（10@100k） |
| 预训练数据 | **715.1 GB** GitHub 代码 |
| CodeContests 假阳性率 | **4%**（原始 **62%**） |
| 对照：APPS / HumanEval 假阳性率 | **60%** / **30%** |

**论文自己承认的局限（逐字要点，全部对阙疑有直接警示）**：
- *"**Loss is a poor proxy for solve rate**"*（验证损失是求解率的糟糕代理指标）
- **约 10% 的问题上，模型无法找到哪怕一个通过样例测试的程序**
- **更擅长**：位运算（bitmasks）、排序、数学、贪心算法；**明显更差**：**动态规划（DP）** 与**构造性算法（constructive algorithms）**
- **"慢解正例"（slow positives）率高达 46%**——即正确但算法复杂度不达标的解仍可能通过测试。**这是一个"测试通过 ≠ 正确"的精确案例**
- 对问题描述质量高度敏感：*"简化描述会使求解率从 3.0% 升至 15.7%"*
- **C++ 语法正确率低于 Python**（*"C++ syntax is harder to master than Python"*）

**对阙疑最有价值的三条**：
1. **"过滤去掉 99%"是整条路线能工作的关键。** 1,000,000 → 约 10,000 → 聚类 → 10。**过滤用的是题目自带的样例测试，即一个廉价、精确的 oracle。** 这与方向 76 的 FunSearch、方向 77 的 AlphaProof 是同一个公式：**没有廉价 oracle，就没有可用的采样路线。** 阙疑的 oracle 是**盲 holdout 30 + 真实缺陷夹具 15**，规模远小于 Codeforces 的样例测试——**这意味着阙疑能承受的候选数量级要低得多（可能只有几十个，而不是百万个）**。
2. **"慢解正例率 46%"直接对应阙疑的"变异分数不可靠"。** AlphaCode 发现：**通过测试的程序里，有近一半在复杂度上是错的**。这与 ISSTA 2026 的发现（覆盖率/变异分数不可靠）是同一类问题的两个侧面：**代理指标会系统性高估质量。**
3. **"top 54.3%"这个数字必须被正确解读。** 它**不是**"超过 54.3% 的人"吗？是。但**中位数是 50%**——所以它的真实水平是"**略高于中位数的参赛者**"。**在引用 AlphaCode 时把 54.3% 说成"接近人类顶尖"是严重的误读。**

### 五、ISSTA 2026：覆盖率与变异分数不可靠（对阙疑的直接背书）

**来源**：Junda Zhao, Shurui Zhou, Eldan Cohen（University of Toronto），*Do Coverage and Mutation Scores of LLM-Generated Test Suites Correlate with Their Effectiveness?*，**ISSTA 2026**（PACMSE vol. 3, DOI `10.1145/3832093`，论文 ID `issta26main-p17-p`，收稿 2026-06-25）；复现包 GitHub `drixs2050/Cov_mut_bug_detect_correlation` + Zenodo DOI `10.5281/zenodo.21429528`；NSERC 资助（RGPIN-2022-04154）。

**规模（逐字）**：
- **11 个 SOTA LLM / 13 个配置**：Gemini 2.5 Pro、Gemini 2.5 Flash、Claude 4 Sonnet、Grok-4、Grok-3、GPT-4.1、GPT-O4-mini、DeepSeek-V3、DeepSeek-R1、Qwen3-Coder-Plus、Qwen3-Plus
- *"**8,268 generated test suites** comprising **101,123 individual test cases**"*
- 基准：**Defects4J v3.0**（**854** 个缺陷，**17** 个项目）；精选 **318 个 buggy 焦点方法**；每次抽取 100 个焦点方法，共 **1,000 次独立抽取**
- 套件大小固定为 **k ∈ {3, 5, 10}**

**关键相关系数（论文用 Guilford 量表：|r| < 0.4 = weak）**：

| 场景 | 指标 | 相关性 |
|---|---|---|
| **代码可能有 bug（buggy）** | 覆盖率 vs 缺陷检测率（全部三种视图） | **一律为弱** |
| **代码可能有 bug** | 变异分析 | **不适用**（变异测试需假设套件在代码上是"绿色"通过的） |
| 代码无 bug（回归场景） | 模型**间**比较：Branch 覆盖率 vs 缺陷检测率 | **r = 0.861**（p = 1.6×10⁻⁴） |
| 代码无 bug | 模型**间**：Raw 变异分数 vs 缺陷检测率 | **r = 0.863**（p = 1.44×10⁻⁴） |
| 代码无 bug | 模型**内**与**合并**视图 | **普遍弱**（多低于 0.4，模型内常低于 0.2） |
| 套件大小作为混淆因素 | 套件大小 vs 变异分数 / 缺陷检测率 | **弱**（r ≈ **0.03–0.10**）——**与前人研究结论相反** |

**论文的核心担忧（逐字要点）**：
- *"if coverage and mutation score do not reliably [track defect detection]... relying primarily on these proxies to evaluate LLM-generated tests may be **misleading**"*
- *"除 Huang 等人外，**此前没有研究考虑输入代码本身可能是 buggy 的场景**。而恰恰在这一实际场景中，覆盖率失去预测能力、变异分析又不适用"*
- **测试正确性度量（编译成功数、通过率）应视为"成本效益（cost-effectiveness）"度量，而不应与缺陷检测有效性混为一谈**
- 建议：**同时报告多种指标（raw 与 normalized）且在 average 和 accumulated 两种聚合下报告**

**对阙疑的价值（这是本方向最重要的一条）**：阙疑的项目上下文里写着 *"变异 core 97.3% / all 81.5%（**已放弃当作缺陷检测率**）"*。**过去这看起来像是"自己的指标不好用"，现在它有了顶会复现研究的支持：变异分数与覆盖率在"被测代码可能有 bug"的场景下不可靠，是 2026 年的研究结论。** 论文中应当这样写：*"Our decision to abandon mutation score as a defect-detection proxy is consistent with the findings of Zhao et al. (ISSTA 2026), who report that in the buggy-code setting — precisely our setting — coverage-based and mutation-based proxies show weak correlation with actual defect detection."* **这句话把阙疑的一个"硬伤"转化为一个"有文献支持的方法学判断"。**

### 六、阙疑的 595 个 .py 工具与程序合成的关系（诚实评估）

项目上下文记录：**595 个 .py 工具**（`_arch_v46/` 有 75+ 份 AI 生成文档）。这些工具与程序合成的关系，必须分三类说清：

| 类别 | 例子（推测） | 与程序合成的关系 | 诚实评估 |
|---|---|---|---|
| **基础设施脚本** | 账本读写、哈希链校验、Merkle 计算、CI 脚本 | **无关**。这些是普通工程代码 | **不应把它们算作"合成的产物"。** 数量大不代表方法先进 |
| **分析/绘图脚本** | 统计计算、Clopper-Pearson 区间、绘图 | **无关**。一次性脚本 | 同上。**595 这个数字在论文里出现会被审稿人视为"AI 生成代码堆量"的证据**（结合 Pangram 风险），**建议不要在论文中强调这个数字** |
| **验证规则 / 变异算子 / 测试夹具** | `gate_engine.py` 的 67 条规则、变异算子、缺陷夹具 | **相关**。这才是程序合成的目标域 | **这是唯一值得用程序合成方法改进的部分** |

**结论（三条，必须写进论文）**：
1. **595 个 .py 工具的绝大多数与程序合成无关**，它们是普通工程产出。**用数量暗示"我们做了自动程序合成"是站不住的。**
2. **真正可以尝试合成的是三样东西**：(a) **新的验证规则**（谓词）；(b) **新的变异算子**（对应方向 79）；(c) **新的测试夹具**（对应 PBE 的天然场景）。**其中 (c) 最可行**——因为它天然是"给定输入-输出示例合成变换程序"的 FlashFill 形式。
3. **可合成性的判据是"oracle 是否廉价且精确"**。三条路线按可行性排序：**(c) 测试夹具 > (b) 变异算子 > (a) 验证规则**。理由是：夹具的 oracle 是"编译通过 + 运行时行为可观测"（精确）；变异算子的 oracle 是"是否产生与原始程序不同的行为"（精确但目标模糊）；**验证规则的 oracle 是 30 条 holdout（不精确、样本小、有 33.3% 的已知漏检）——最难**。

---

## 对阙疑的 3 条具体行动

1. **【2026-12 前】为 67 条规则写一份形式化 DSL 定义，这是"自动生成规则"的前置条件（没有它，后续全部免谈）。** 具体交付物：`docs/rule_dsl.md` + `rules/grammar.py`（用 Python 的 EBNF 或 `lark` 语法定义）。要求：
   - **定义基本谓词**：例如 `iter_invalidated_after(call)`, `ub_if_empty(container)`, `complexity_worse_than(op, baseline)` 等（**具体名称以现有 67 条规则的实际语义为准，我未阅读 `gate_engine.py`，因此这里只给形式**）；
   - **定义组合子**：`AND`, `OR`, `NOT`, `IMPLIES`, `WITHIN_SCOPE(scope, predicate)`；
   - **定义语法约束**：例如"每条规则最多 5 个谓词节点""不允许嵌套超过 3 层"——**这是为了把搜索空间限制在可枚举范围**，直接借鉴 FlashFill 的 *"restricted forms"*；
   - **验收**：用 `rules/grammar.py` 解析现有 67 条规则，**必须 100% 可解析**（若某条规则无法解析，说明它超出了 DSL 表达能力，需在文档中单列）；
   - **理由引用**：Gulwani 论文逐字 *"a string programming/expression language that supports **restricted forms**"*——**限制是特性，不是妥协**。
   - **时间点**：2026-12 完成；2027-01 前用该 DSL 重述全部 67 条规则。

2. **【2027-01 前】按"oracle 质量"排序实现三条合成路线的可行性验证，并如实报告哪条不可行。** 具体做法（**每条都要给出可执行的最小实验与预期失败的判据**）：
   - **路线 (c) 测试夹具合成（最可行）**：用 PBE 形式，输入是"若干 (C++ 代码片段, 期望判决) 示例"，输出是一个**能生成该夹具的 Python 函数**。**成功判据**：合成的夹具在**未参与合成的 10 条保留示例**上仍给出正确判决。**预期**：这条最可能成功，因为 oracle 是精确的（编译 + 运行）。
   - **路线 (b) 变异算子合成**：输入是"原始代码片段 + 期望的变异类型描述"，输出一个变异函数。**成功判据**：合成的变异算子产生的变异体**不被 67 条规则检出**（即"存活"）——这直接对应方向 79 的变异测试目标。**预期**：中等可行。**注意**：若变异算子合成的目标是"提高变异分数"，则**根据 ISSTA 2026 的结论，这个目标本身不可靠**，必须把目标改为"产生能通过 holdout 验证的、人类可读的变异体"。
   - **路线 (a) 验证规则合成（最难，可能不可行）**：**成功判据**：合成的候选规则在**盲 holdout 30** 上的检出数**严格增加**，且**不降低**真实缺陷夹具 15 的通过率（12/15）。**预期**：这条很可能失败，因为 oracle 只有 30 条、且已知检出率 66.7%（意味着真错 17 条中约 5–6 条是系统性漏检，**任何只靠这 30 条优化的规则都学不到这 5–6 条的规律**）。
   - **必须报告的 negative result**：如果路线 (a) 失败，**把它写成一个正式的 negative result 小节**。**理由引用**：NeurIPS E&D 的 CFP 明确欢迎 *"negative results"*，且方向 76 的证据表明"AI 生成候选容易、自我验证极难"。
   - **时间点**：2027-01 完成三条路线的最小实验；2027-02 写结论。

3. **【2027-03 前】把"我们放弃了变异分数"这件事从"硬伤"改写为"有文献支持的方法学判断"，并在论文的 Threats to Validity 里主动陈述。** 具体措辞建议：
   - **在 Metrics 小节**：*"We initially used mutation score as a defect-detection proxy and obtained core 97.3% / all 81.5%. We subsequently abandoned it as a defect-detection metric."*
   - **紧接着给出文献支持**：*"This decision is consistent with Zhao, Zhou & Cohen (ISSTA 2026), who evaluated 8,268 LLM-generated test suites (101,123 test cases) over Defects4J v3.0 and report that in the buggy-code setting — our setting — coverage and mutation-score correlations with actual defect detection are uniformly weak, and that mutation analysis is not applicable because it presupposes a green suite."*
   - **在 Threats to Validity 里补一句自我限制**：*"We note that mutation score and coverage remain meaningful as cost-effectiveness metrics; we do not claim they are useless, only that they do not track defect-detection effectiveness in our setting."*（**这一句直接抄自 ISSTA 论文的措辞精神，能让审稿人看到你读过文献**）
   - **同时在 README 中删去任何把 595 个 .py 工具当作成果的表述**，改为分三类列出（基础设施 / 分析 / 验证），并明确只有第三类与合成相关。
   - **时间点**：2027-03 前完成论文改写；2027-05 前更新 README。

---

## 盲区（诚实标注）

- **SyGuS-Comp 是否在 2018 年之后停办，我没有核实。** 我只确认 **SyGuS-Comp 2018 是第 5 届**（sygus-org.github.io/comp/），且搜索结果中**未出现 2019 年及以后的赛事页面**。**"停办"是我的推测，不是事实**，正文中已标注。
- **SyGuS-Comp 2018 的具体求解器名称、各 track 的解题数、以及"5 个求解器中谁赢"我都没有核实。** 只有 arXiv:1904.07146 摘要中的 *"five solvers competed on over 1600 benchmarks"*。
- **DreamCoder 没有任何具体量化结果被我核实。** 摘要**不含数字**；第三方讲稿（simons.berkeley.edu）只有定性表述 *"bootstrapping, more than sum of parts"*。**论文中若引用 DreamCoder 的改进倍数，必须先打开 PLDI 2021 原文（DOI `10.1145/3453483.3454080`）。**
- **DreamCoder 的"rediscovers Newton's and Coulomb's laws"是摘要原文，但"恢复"与"发现"的界线我未在原文中核实。** 从摘要措辞（*"rediscovers"*）看，作者的表述是诚实的（用词是"重新发现"），这一点比很多二手报道更准确。
- **FlashFill 的"在真实用户场景的准确率/成功率"我未核实。** 论文只说 *"fraction of a second for various benchmark examples"*，**没有给出成功率百分比**。搜索到的第三方中文资料（CSDN 2026-06-02/03）多为科普性描述，**不构成可引用的量化证据**。
- **FlashFill 的"Most Influential POPL Paper Award"我确认了微软官方页面上的标注，但未核实是 10 年还是 20 年奖，也未核实获奖年份。**
- **AlphaCode 的"机构归属"在其 arXiv HTML 中未直接标注**（抓取结果明确说明 *"原文中未直接标注机构归属"*）。我据公开信息归为 DeepMind，但**这不是从该页面逐字得到的**。
- **AlphaCode 的"slow positives 率 46%"这一数字来自对论文第 6 节的抓取，我未打开 PDF 逐字核对上下文。** 该数字的具体定义（分母是什么、如何判定"慢"）**未核实**。
- **ISSTA 2026 论文的"318 个 buggy 焦点方法"与"8,268 个测试套件"等数字来自 arXiv HTML 抓取（arXiv:2607.22880）。** 该论文的 DOI（`10.1145/3832093`）与 PACMSE 卷号来自同一抓取结果，**我未在 ACM DL 独立核实**。此外，**"ISSTA 2026"这个会议届次与论文的最终发表状态（是否已正式出版）我未核实**。
- **我对阙疑的 595 个 .py 工具的"三类划分"是推测性的**——我**没有读取这些文件的目录结构**，因此无法确认基础设施/分析/验证三类各占多少。**行动 3 中"删去 README 中把 595 当作成果的表述"这一条，需要先实际统计分类后再执行。**
- **我没有阅读 `gate_engine.py`（3826 行）或任何现有规则代码**，因此行动 1 中关于 DSL 的具体谓词名称（`iter_invalidated_after` 等）是**形式示例，不是现有代码的还原**。实施时必须按实际规则语义重写。
- **"验证规则合成会失败"这一预期是我基于 oracle 质量的推理**（30 条 holdout、检出率 66.7%），**不是实测**。**这正是行动 2 要验证的东西，在验证之前不能写进论文结论。**
- **样本偏差**：本文引用的所有合成系统（FlashFill / SyGuS / DreamCoder / AlphaCode）都有**大规模、精确、自动化的 oracle**（Excel 的示例、SyGuS 的形式规格、DreamCoder 的题目、Codeforces 的样例测试）。**没有任何工作覆盖"oracle 是一个 30 条样本、已知漏检 33% 的 holdout"这一场景。** 因此本文对阙疑的可行性排序是**结构性推理**，不是实测。

---

## 来源

1. Gulwani, S.（Microsoft Research） — *Automating String Processing in Spreadsheets using Input-Output Examples* — **POPL 2011**（PoPL'11, January 26-28, 2011, Austin, Texas, USA），DOI `10.1145/1926385.1926423` — https://www.microsoft.com/en-us/research/publication/automating-string-processing-spreadsheets-using-input-output-examples/ — 逐字：*"a string programming/expression language that supports restricted forms of regular expressions, conditionals and loops"*、*"very efficient taking fraction of a second for various benchmark examples"*、*"it can rank multiple solutions and has fast convergence"*、*"it can detect noise in the user input"*、*"supports an active interaction model"*、*"The prototype tool has met the golden test – it has synthesized part of itself"*；微软页面标注 **Most Influential POPL Paper Award**
2. Alur, R. 等 — *SyGuS-Comp 2018: Results and Analysis* — arXiv:1904.07146（2019-04-13） — https://arxiv.org/abs/1904.07146 — 逐字：*"In the 5th SyGuS-Comp, five solvers competed on over 1600 benchmarks across various tracks."*
3. SyGuS 官方赛事页 — https://sygus-org.github.io/comp/（2023-10-25） — 逐字：*"The 5th SyGuS Competition, SyGuS-Comp 2018 was held at the FLoC Olympic games at the 2018 Federated [Logic Conference]"*；另见 https://sygus.org/ 与 benchmark 仓库 https://github.com/SyGuS-Org/benchmarks（2026-01-25）
4. Ellis, K.; Wong, C.; Nye, M.; Sablé-Meyer, M.; Cary, L.; Morales, L.; Hewitt, L.; Solar-Lezama, A.; Tenenbaum, J. B.（MIT） — *DreamCoder: Growing generalizable, interpretable knowledge with wake-sleep Bayesian program learning* — https://arxiv.org/abs/2006.08381 — arXiv:2006.08381v1, **2020-06-15**；**PLDI 2021**, DOI `10.1145/3453483.3454080` — 逐字：*"builds expertise by creating programming languages for expressing domain concepts"*、*"A 'wake-sleep' learning algorithm alternately extends the language with new symbolic abstractions"*、*"It rediscovers the basics of modern functional programming, vector algebra and classical physics, including Newton's and Coulomb's laws"*、*"multi-layered symbolic representations that are interpretable and transferrable"*
5. Kevin Ellis 讲稿（simons.berkeley.edu, 2022-12-13） — https://simons.berkeley.edu/sites/default/files/docs/17406/kevinellistfcsjointslides.pdf — 逐字：*"Library learning interacts synergistically with neural synthesis: bootstrapping, more than sum of parts"*（**定性，无数字**）
6. AlphaCode 团队（13 位共同第一作者；含 Pushmeet Kohli, Nando de Freitas, Koray Kavukcuoglu, Oriol Vinyals） — *Competition-Level Code Generation with AlphaCode* — arXiv:2203.07814（2022-03）；*Science* 378:1092 — https://ar5iv.labs.arxiv.org/html/2203.07814 — 逐字：*"top 54.3%"*、*"more than 5,000 participants"*、估计评分 **1238**（前 28%）、每题最多 **1,000,000** 样本、*"Filtering removes approximately 99% of model samples"*、最多 **10** 次提交、平均 **2.4** 次/题、验证集 **34.2%**（10@1M）/ 测试集 **29.6%**（10@100k）、预训练 **715.1 GB**、CodeContests 假阳性 **4%**（原始 **62%**）、APPS **60%** / HumanEval **30%**、*"Loss is a poor proxy for solve rate"*、约 **10%** 题目无解、DP 与构造性算法更差、慢解率 **46%**、*"C++ syntax is harder to master than Python"*
7. Zhao, J.; Zhou, S.; Cohen, E.（University of Toronto） — *Do Coverage and Mutation Scores of LLM-Generated Test Suites Correlate with Their Effectiveness?* — **ISSTA 2026**，PACMSE vol. 3，DOI `10.1145/3832093`，论文 ID `issta26main-p17-p`（收稿 2026-06-25） — https://arxiv.org/html/2607.22880 — 逐字：*"8,268 generated test suites comprising 101,123 individual test cases"*、**11 个 SOTA LLM / 13 个配置**（Gemini 2.5 Pro/Flash、Claude 4 Sonnet、Grok-4/3、GPT-4.1、GPT-O4-mini、DeepSeek-V3/R1、Qwen3-Coder-Plus、Qwen3-Plus）、Defects4J v3.0（**854** 缺陷 / **17** 项目 / **318** buggy 焦点方法 / 1,000 次抽取）、k ∈ {3,5,10}、buggy 场景下覆盖率 vs 缺陷检测**一律为弱**、变异分析**不适用**、模型间 Branch 覆盖率 vs 缺陷检测 **r = 0.861**（p = 1.6×10⁻⁴）、Raw 变异分数 vs 缺陷检测 **r = 0.863**（p = 1.44×10⁻⁴）、套件大小相关性**弱**（r ≈ 0.03–0.10）、*"may be misleading"*、测试正确性度量应视为**成本效益**而非缺陷检测有效性；复现包 https://github.com/drixs2050/Cov_mut_bug_detect_correlation + Zenodo DOI `10.5281/zenodo.21429528`
8. *Correctness assessment of code generated by Large Language Models* — *Journal of Systems and Software*（2025-12-01），DOI `10.1016/j.jss.2025.112...`（S0164121225002390） — https://www.sciencedirect.com/science/article/pii/S0164121225002390（**仅标题与摘要层面，未深入**）
9. *Is LLM-Generated Code More Maintainable & Reliable than Human-Written Code?* — arXiv:2508.00700v1（2025-08-01） — https://arxiv.org/html/2508.00700v1（**二手，本文未深入使用**）
10. *Unseen Horizons: Unveiling the Real Capability of LLM Code Generation* — ICSE 2025 — https://zhouyangjia.github.io/assets/papers/2025%20ICSE.pdf（**仅标题层面，未深入**）
11. 中文科普资料（**仅作交叉参考，不构成证据**） — CSDN *程序合成技术解析：从 FlashFill 到自动化编程的未来*（2026-06-02） https://blog.csdn.net/weixin_33501543/article/details/161641396 ；CSDN *Excel Flash Fill：从程序合成到智能数据清洗的实战指南*（2026-06-03）
12. Zhao, J. 等复现包 — https://github.com/drixs2050/Cov_mut_bug_detect_correlation（2026-07-18）
