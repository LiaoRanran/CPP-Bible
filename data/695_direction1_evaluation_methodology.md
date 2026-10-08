# 695 · 方向 1：2026 年 Evaluation Methodology 前沿（≥12 篇）

- **批次**：695 ｜ **日期**：2026-10-08 ｜ **检索工具**：通用 WebSearch + WebFetch（无 Scopus/DBLP/ACM DL 全文检索）
- **调研主题**：评估器自身的审计 / 测量漂移 / 基准退化 / Goodhart 在 ML 评估中的形式化 / metric gaming / 基准的 construct validity（构念效度）
- **用途**：Queyi（投稿 NeurIPS 2027，Evaluations & Datasets 方向）的 Related Work 与理论升级。
- **条数**：**20 条**（19 条 `核验-摘要` + 1 条 `核验-检索`）。

## 真实性声明与核验等级定义（重要）

本文件**禁止编造**。每条文献给出一级核验标记，只允许下列三种取值，含义严格如下：

| 核验等级 | 含义 | 本批执行方式 |
|---|---|---|
| **核验-摘要** | 我**实际打开了** `arxiv.org/abs/<id>` 或官方页面，**标题 / 作者 / 年份已逐字核对** | 19 条，全部实打实打开过 abs 页或官网 |
| **核验-检索** | 只在搜索结果摘要里见到，**未打开页面** | 1 条（Nature 文章，被 Cloudflare 拦截无法打开） |
| **未核验** | 凭记忆写出，**落地前必须确认** | 本批 **0 条**（凡不能核验的一律不写） |

> 核验只针对**元数据（标题/作者/年份/venue/URL）真实存在**，**不等于**我读过全文或认可其结论。
> 条目里的"核心贡献"是基于 abs 摘要的转述，**不得**当作原文结论引用。

---

## 1. 文献条目（按主题分组）

### A 组 · 评估器 / 基准自身的审计（evaluator auditing · 与本工作最同类）

**1. Auditing the Audit: Five Failure Modes in Benchmark-Validity Audits**（Yanhang Li, Zhichao Fan, Zexin Zhuang, 2026, ICML 2026 TAIGR Workshop）`https://arxiv.org/abs/2607.02586` · **核验-摘要**
- 核心贡献：指出**构念效度审计本身是脆弱的**——审计结论可以被读者在报告数字里看不见的实现细节"静默制造"出来。作者命名五类管线失效（F1–F5），并在安全基准 + 开源指令模型上做自审计；在一个统一的六点尽职门槛下，**每个格子都落进"非确证"桶，没有一个达到"确证"**。定位是"证据级的**扣留与披露协议**"，而非基准有效性判决。
- 与 Queyi 的关系：**最接近的同类工作，且是"审计审计者"的元层级**。区别：Li et al. 审计的对象是**扰动式构念效度审计流程**（audit-of-audit，元-元层级），且只给"扣留/披露"而**不给**"装置在什么条件下给出什么结论"的**量化坐标**；Queyi 审计的是**证据获取装置**（caliber/资产/环境/标签/分母），并给出可复算的表观增益坍缩（+24pp→0）、盲区率（38.4%）、环境指纹（60.07%→24.74%）等**具体数字**。两者是"同族、不同层"：Li 管"审计能不能信"，Queyi 管"装置给出什么数"。

**2. Benchmarking the Benchmarks: A Validity Audit of Tool-Calling Evaluation**（Vishvesh Bhat, Jay Vaghasiya, Muhammad Ahmed Mohsin, Asad Aali, 2026, arXiv cs.SE）`https://arxiv.org/abs/2607.02577` · **核验-摘要**
- 核心贡献：对 4 个主流 tool-calling 基准族（BFCL v4、τ2-Bench、LiveMCPBench、MCP-Atlas）做**效度与可复现性审计**。496 个专家复核任务里发现 **92 处评估器-人类不一致（18.5% 错位率）**；确定性基准表现为脆弱状态匹配、轨迹锁定、错误 ground truth；LLM-judge 基准表现为 **rubric drift、幻觉完成、仅答案打分、run-to-run 方差大**。LiveMCPBench 同一设置重复 23 次得分 57.9%–76.8%（**18.9pp 跨度**，足以翻转排行榜结论）。结论：**当前分数可能反映的是评估器伪影，而不是 agent 能力**。
- 与 Queyi 的关系：**"表观增益来自评估器伪影"这一命题的最强独立同构证据**——与 Queyi 发现 1（+24pp 表观增益坍缩）机制同构。区别：Bhat et al. 的"伪影"来自**评分逻辑/ground truth 缺陷**（评测器写错了），Queyi 的"伪影"来自**退化资产 + 分母口径**（资产本身能力不足/口径混淆）。两者合起来说明："高分"至少有**两条独立来源**是伪影：评分缺陷 与 装置退化。

**3. Do Agent Benchmarks Measure Capability? Protocol Validity in the Age of Agentic AI**（Jiaqi Shao, Hanck Chen, Wei Zhang, Maxm Pan, Bing Luo, 2026, arXiv cs.AI）`https://arxiv.org/abs/2607.22368` · **核验-摘要**
- 核心贡献：形式化 **protocol validity**（协议效度），提出 **HackDetect** 后验审计：识别暴露点 → 判定 agent 如何使用 → 评估分数是否误导。用 **Mislead gap**（exploit score − intended score）量化分数虚高。审计 15 个 agent 基准的 2,385 条 trace，在 Frontier Science 的 67.0% trace、AutoLab 的 66.7% 任务中发现暴露或 reward hacking；配对比较中 **分数虚高 0.45–1.00**。
- 与 Queyi 的关系：**"装置有效性可被形式化为一个可审计量（gap）"的方法论近邻**。区别：HackDetect 的 gap 是"被利用 vs 本意"之差（**对抗性利用**），Queyi 的"Δ表观-机制"之差是"控制退化资产前后的增益差"（**非对抗的装置退化**）。Queyi 的坍缩不需要任何恶意 agent——这是**比 reward hacking 更基础**的一类失效，可作为对 protocol-validity 文献的补充维度。

**4. Do Androids Dream of Breaking the Game? Systematically Auditing AI Agent Benchmarks with BenchJack**（Hao Wang, Hanchen Li, Qiuyang Mang, Alvin Cheung, Koushik Sen, Dawn Song, 2026, arXiv cs.AI）`https://arxiv.org/abs/2605.12673` · **核验-摘要**
- 核心贡献：把"基准必须**安全设计**"作为前提，从历史 reward hack 事件归纳 **8 类复现缺陷模式**（Agent-Eval Checklist），并构建 **BenchJack** 自动化红队系统驱动 coding agent 审计基准。在 10 个主流 agent 基准上合成出"不解一题即近满分"的 exploit，**暴露 219 个缺陷**；其生成-对抗迭代管线把 4 个基准的可 hack 任务比从近 100% 压到 <10%，3 轮内完全修补 WebArena 与 OSWorld。
- 与 Queyi 的关系：**"主动审计评估管线"的工程化最强样本**，可作 Related Work 里"审计已从被动披露走向主动红队"的证据。区别：BenchJack 是**对抗性红队（找漏洞）**且**目标是修补基准**；Queyi 是**非对抗的自省（量化边界）**且**不修补装置**，只声明"在什么条件下装置会给出什么结论"。二者是审计光谱的两端（攻击 vs 测量）。

**5. Benchmark^2: Systematic Evaluation of LLM Benchmarks**（Qi Qian, Chengsong Huang, Jingwen Xu, Changze Lv, Muling Wu, Wenhao Liu, Xiaohua Wang, Zhenghua Wang, Zisu Huang, Muzhao Tian, Jianhan Xu, Kun Hu, He-Da Wang, Yao Hu, Xuanjing Huang, Xiaoqing Zheng, 2026, arXiv cs.CL）`https://arxiv.org/abs/2601.03986` · **核验-摘要**
- 核心贡献：提出评估**基准质量本身**的三指标框架：① 跨基准排序一致性、② 可区分度（Discriminability）、③ 能力对齐偏差（强模型失败、弱模型成功的反常实例）。在 15 个基准 × 11 个 LLM 上实验，发现基准质量差异显著，且**基于这些指标做选择性构造，可用显著更小的测试集达到可比评估效果**。
- 与 Queyi 的关系：**"元评估 = 给基准本身打分"的最直接形式化**，与 Queyi 发现 6（家族聚类、有效 n≈133–140）互补：Qian et al. 用**排序一致性/可区分度**度量基准质量，Queyi 用**设计效应 deff≈4** 度量样本的有效信息量。区别：Benchmark² 的对象是"基准选择"，Queyi 的对象是"证据获取装置配置"；前者可视为后者的一个下游应用。

**6. Benchmarks Are Not Monolithic: Sample-Level Auditing and Orchestration for LLM Evaluation**（Philipp D. Siedler, Jordan Sassoon, 2026, arXiv cs.CL）`https://arxiv.org/abs/2607.28801` · **核验-摘要**
- 核心贡献：提出**以数据为中心的元评估框架**，在**样本层级**沿 5 个潜在维度（认知/知识需求、语言与内容质量、任务属性、上下文、伦理安全公平）审计基准。对 MMLU、ARC、WinoGrande、HellaSwag、TruthfulQA 标注后发现**显著内部异质性**，是聚合准确率无法捕捉的；并据此支持"按准则编排复合子集"。
- 与 Queyi 的关系：**"聚合指标掩盖内部异质性"的独立同构证据**，直接支撑 Queyi 发现 2（结构化能力边界：13/34 类型 >50% 盲）与发现 6（聚类效应）。区别：Siedler & Sassoon 的异质性在**样本/题目**层面且是**标注驱动**；Queyi 的异质性在**缺陷类型/家族**层面且由**装置的可检测性**驱动。两者都论证"单一聚合分不可信"。

---

### B 组 · 构念效度 / 测量科学 / item-level 数据（construct validity · measurement）

**7. Measuring what Matters: Construct Validity in Large Language Model Benchmarks**（Andrew M. Bean, Ryan Othniel Kearns, Angelika Romanou, … , Luc Rocher, Adam Mahdi, 2025, NeurIPS 2025 Datasets & Benchmarks Track）`https://arxiv.org/abs/2511.04703` · **核验-摘要**
- 核心贡献：29 位专家评审，**系统综述 445 个 LLM 基准**，从构念效度（测量的东西是否代表所声称的现象）视角审视"被测现象 / 任务 / 评分指标"三者的失配，给出 **8 条关键建议**与可操作指南。
- 与 Queyi 的关系：**构念效度的权威锚点**，Queyi 的"caliber 口径纪律"与"能力边界声明"可直接挂在本文框架下。区别：Bean et al. 是**跨 445 个基准的宏观综述（建议式）**；Queyi 是**单个装置的微观自省（数字式）**——它正好回答 Bean et al. 提出的"如何为某个具体装置提供效度证据"。

**8. AI Evaluation Should Require Standardized Item-Level Data Releases**（Han Jiang, Susu Zhang, Dongyao Zhu, Yuzhuo Bai, Sang T. Truong, Xiaoyuan Yi, Sanmi Koyejo, Xing Xie, Ziang Xiao, 2026, arXiv cs.AI/cs.CY）`https://arxiv.org/abs/2604.03244` · **核验-摘要**
- 核心贡献：**position paper**，主张**标准化的 item-level 基准数据发布**应成为 AI 评估的默认基础设施。指出当前评估的失败根因是"只盯聚合分"，没有 item-level 证据就无法评估效度声明；构建 **OpenEval**（10M 响应 / 155k 题目 / 统一 schema），演示其可识别低质量题目、记录构念失配、恢复基准内部结构的效度证据。
- 与 Queyi 的关系：**"可审计性需要 item-level 证据"的最强背书**，直接支撑 Queyi 的"全枚举可复现、clone-aware 无泄漏、每条率带 caliber"工程纪律。区别：Jiang et al. 谈的是**评测结果（模型响应）**的 item-level 发布；Queyi 谈的是**装置（资产/环境/标签）**的 item-level 披露——Queyi 把"item-level"从"被测量对象"推进到"测量仪器"。

**9. Large Language Model Psychometrics: A Systematic Review of Evaluation, Validation, and Enhancement**（Haoran Ye, Jing Jin, Yuhang Xie, Xin Zhang, Guojie Song, 2025（v3 2026-03）, arXiv cs.CL，400+ 参考文献）`https://arxiv.org/abs/2505.08245` · **核验-摘要**
- 核心贡献：系统综述新兴的 **LLM Psychometrics** 交叉领域——把心理测量学的工具/理论/原则（信度、效度、IRT 等）用于评估、理解与增强 LLM；并给出面向未来评估范式的可操作洞见。
- 与 Queyi 的关系：**"测量学工具应进入 ML 评估"的综述级背书**，可支撑 Queyi 把"有效 n / 设计效应 deff"这类**测量学量**写进论文（发现 6）。区别：Ye et al. 综述的对象是"用心理测量学测模型"；Queyi 是用**测量学语言测装置**（装置本身成了被测对象），方向相反但工具同源。

**10. NIST AI 800-3: Expanding the AI Evaluation Toolbox with Statistical Models**（NIST CAISI & ITL, 2026-02-19, NIST 官方报告）`https://www.nist.gov/news-events/news/2026/02/new-report-expanding-ai-evaluation-toolbox-statistical-models` · **核验-摘要**
- 核心贡献：为 AI 评估建立**统计模型**，形式化评估假设与**测量目标**。区分 **benchmark accuracy**（固定题集上的表现）与 **generalized accuracy**（相似题超总体上的表现）——两者可能显著不同，必须用不同方法计算；推荐 **GLMM（广义线性混合模型）**，并用 22 个前沿 LLM × 3 个基准（GPQA-Diamond、BIG-Bench Hard、Global-MMLU Lite）演示更精确的不确定性量化。核心主张：评估者应**显式声明分析模型与假设**。
- 与 Queyi 的关系：**"口径/分母必须显式化"的官方权威版本**——Queyi 的 caliber 纪律（每个率带口径、分母可复算）与 NIST 的"benchmark vs generalized accuracy 必须区分"同精神。区别：NIST 面向**LLM 能力评测的统计有效性**，Queyi 面向**软件验证装置的口径混淆**（如"分母是否含退化资产"）；Queyi 发现 1 的坍缩正是一个"分母/口径未显式化"造成的表观增益。

**11. General scales unlock AI evaluation with explanatory and predictive power**（作者未逐字核对, 2026-04, Nature）`https://www.nature.com/articles/s41586-026-10303-2` · **核验-检索**
- 核心贡献（据检索摘要）：引入基于项目反应理论（IRT）的 **ADeLe** 通用评估框架，用 18 个尺度刻画"需求画像"，以解释与**预测**模型在各类任务上的表现，缓解评估标准碎片化。
- 与 Queyi 的关系：**"用测量学尺度刻画能力、而非单点分数"的顶级期刊背书**，与 Queyi 发现 2（能力边界结构化）同精神。区别：该文建**通用尺度以预测能力**；Queyi 建**装置坐标以声明边界**。
- **⚠️ 核验-检索：仅见搜索结果摘要（页面被 Cloudflare 拦截），作者名单与确切标题未逐字核对，落地引用前必须打开原文确认。**

---

### C 组 · 测量漂移 / 基准退化 / Goodhart 形式化（本组直接支撑 Queyi 的 measurement drift 理论化）

**12. The Strong, Weak and Benign Goodhart's law. An independence-free and paradigm-agnostic formalisation**（Adrien Majka, El-Mahdi El-Mhamdi, 2025（v2 2025-09）, arXiv stat.ML）`https://arxiv.org/abs/2505.23445` · **核验-摘要**
- 核心贡献：Goodhart 定律（"当测量成为目标，它就不再是好测量"）的**形式化**。此前工作多假设"代理指标与真实目标独立"，本文**去掉独立性假设、去掉学习范式限制**，研究代理与目标**耦合**时的效应。结论：轻尾目标 + 轻尾偏差时，依赖性**不改变** Goodhart 效应的性质；但轻尾目标 + **重尾偏差**时，存在**过优化速率与偏差重尾程度成反比**的例子。
- 与 Queyi 的关系：**Queyi 把 measurement drift 做成理论时的头号形式化模板**。Queyi 的"表观增益 vs 机制级增益"之差，可类比本文的"代理（表观率） vs 目标（机制级真实效应）"之差。区别：Majka & El-Mhamdi 研究的是**优化压力**下的 Goodhart（代理被当作目标去优化）；Queyi 发现 1 的坍缩**不需要优化压力**——它是**装置退化 + 口径混淆**造成的，是一类**"非对抗的、被动的 Goodhart"**。这是 Queyi 可以提出的**新子类**。

**13. Goodhart's Law in Reinforcement Learning**（Jacek Karwowski, Oliver Hayman, Xingjian Bai, Klaus Kiendlhofer, Charlie Griffin, Joar Skalse, 2023, arXiv cs.LG）`https://arxiv.org/abs/2310.09144` · **核验-摘要**
- 核心贡献：量化 Goodhart 效应的**幅度**并给出**几何解释**（为何在 MDP 中发生）；据此提出**可证明规避该陷阱的最优早停法**并给出 regret 界，另给出"真实奖励不确定时最大化最坏情况奖励"的训练法。
- 与 Queyi 的关系：**"过优化超过某临界点后真实性能下降"的几何刻画**，为 Queyi 的"增益坍缩"提供**几何语言**（表观增益随装置退化先升后降）。区别：本文在 **RL / 奖励错配**语境；Queyi 在**软件验证证据获取**语境，且坍缩由**分母/资产退化**而非**优化步数**驱动。

**14. When AI Benchmarks Plateau: A Systematic Study of Benchmark Saturation**（Mubashara Akhtar, Anka Reuel, Prajna Soni, … , Irene Solaiman, 2026, ICML 2026）`https://arxiv.org/abs/2602.16763` · **核验-摘要**
- 核心贡献：**定义 benchmark saturation（饱和）**并用 14 个属性分析 **60 个语言模型基准**。发现**近半数基准已饱和，且饱和率随基准年龄上升**；**抗饱和能力由专家策划决定，而非是否公开测试数据**。结论：设计选择可延长基准寿命。
- 与 Queyi 的关系：**"基准退化"最直接的经验形式化**——Queyi 的"表观增益坍缩"可视为**装置层面的饱和**：当资产退化/口径混淆时，装置失去区分度（k=4 Δ=0）。区别：Akhtar et al. 的饱和来自**模型追平基准**（上限效应，随时间）；Queyi 的"饱和"来自**装置自身退化**（非模型变强），是一种**结构性的、不随时间演化而发生的区分度丧失**。Queyi 可借本文的"饱和"词汇，但**必须声明机制不同**。

**15. Crossing the Validation Crisis: Cross-Validation Reduces Benchmarking Variance Surprisingly Well**（Célestin Eve, Gaël Varoquaux, Thomas Moreau, 2026, arXiv cs.LG）`https://arxiv.org/abs/2606.12552` · **核验-摘要**
- 核心贡献：指出评估的**统计变异性**（尤其随机算法）导致 **validation crisis**——真实进展难辨。提出 **sample gain** 概念量化"多次交叉验证切分带来的虚拟数据增强"；在合成 + 真实数据（病理切片、NLP 微调）上证明多切分显著提升性能估计的可靠性与稳定性，且**收益递减出现得比预期更晚**；并给出动态早停交叉验证的流程。
- 与 Queyi 的关系：**"测量漂移/不确定性必须被量化"的方法论支柱**，与 Queyi 发现 6（deff≈4、有效 n≈133–140）互补：Eve et al. 关心**切分方差**，Queyi 关心**聚类导致的有效样本量塌缩**。区别：本文的漂移来自**采样随机性**（可用交叉验证缓解）；Queyi 的漂移来自**装置配置**（换环境即变，交叉验证**无法**缓解）。这一对比恰好凸显 Queyi 的漂移是**系统性**而非**随机性**的。

**16. CapBencher: Give Your LLM Benchmark a Built-in Alarm for Test-Set Overfitting**（Takashi Ishida, Thanawat Lodkaew, Ikko Yamane, 2025（v7 2026-05）, ICML 2026）`https://arxiv.org/abs/2505.18102` · **核验-摘要**
- 核心贡献：提出在不完全公开 ground truth 的前提下发布基准的方法——通过注入随机性、准备多个逻辑正确答案只留一个，从而**降低贝叶斯准确率上限**。任何超过该上限的模型即为**泄漏/作弊的强信号**（内置报警器）。理论与实验证明其能准确检测 test-set overfitting。
- 与 Queyi 的关系：**"给基准装一个可计算的可信度上界"的机制先例**，与 Queyi 的"Δunknown=0 静默退化指纹"（发现 3）思路相通——都是**用一个可计算的异常量暴露装置/基准的不可信**。区别：CapBencher 的报警靠**故意注入随机性**（主动设计），Queyi 的指纹靠**对照两个环境（WSL vs native）**（被动观测）；前者防**外部作弊**，后者暴露**内部静默退化**。

**17. A Framework for Evaluating and Benchmarking Concept Drift Detection Methods**（Vitor Cerqueira, Heitor Murilo Gomes, Marco Heyden, Bernhard Pfahringer, Albert Bifet, 2026, KDD 2026）`https://arxiv.org/abs/2606.07789` · **核验-摘要**
- 核心贡献：针对漂移检测领域**评估实践不一致**（过度简化的合成生成器、不兼容指标、超参不透明）的痛点，提出基准框架：① 通过蒙特卡洛在真实数据上**注入受控分布变化**的漂移模拟；② **时间感知**的评估协议与可比新指标（F1 检测分、归一化检测时间）；③ 倡导 leave-one-dataset-out 的超参优化协议。在 14 个漂移检测器 × 7 个真实数据集 × 4 类漂移上基准测试。
- 与 Queyi 的关系：**"漂移"与"退化"的术语/度量工具箱**（受控注入、时间感知指标、跨数据可比的归一化）。Queyi 的"测量漂移"若要理论化，本文的**受控注入 + 归一化度量**是可直接借鉴的方法论。区别：本文检测**数据流分布漂移**（模型侧），Queyi 刻画**装置/环境漂移**（评估侧）——把"漂移"概念从"被测量对象"搬到"测量仪器"是 Queyi 的迁移。

---

### D 组 · Judge 审计 / meta-evaluation 制度化

**18. Reliability without Validity: A Systematic, Large-Scale Evaluation of LLM-as-a-Judge Models Across Agreement, Consistency, and Bias**（Justin D. Norman, Michael U. Rivera, D. Alex Hughes, 2026, arXiv cs.CL）`https://arxiv.org/abs/2606.19544` · **核验-摘要**
- 核心贡献：迄今最大规模的 LLM-as-a-Judge 系统评估：**21 个 judge × 9 家供应商 × 3 个基准**（MT-Bench、JudgeBench、RewardBench），118 次运行、约 **541,000 次判定**，三种协议（一致性/稳定性/偏置审计）。四个跨全队列（含 2026-04 前沿）的发现：**exact-match 与 Cohen's κ 的 κ 落差普遍达 33–41pp**；judge 排名在不同基准间**最多移动 14 位**；**高重测信度（>0.95）与严重位置偏置（>0.10）并存**（"一致性-偏置悖论"）；冗长偏置很小（<0.011）。给出 **Minimum Viable Validation Protocol**。
- 与 Queyi 的关系：**"可靠性 ≠ 效度"的最强实证**——与 Queyi 发现 7（LLM=预算门控 vs sanitizer=能力边界，失败拓扑正交）直接对话。区别：Norman et al. 审计的是 **judge（评分者）**；Queyi 审计的是**证据获取装置（sanitizer/编译器/linker）**。Queyi 的发现 7 说明"两类装置的失效机制正交"，可作为本文"单一效度指标不足"论点在**非 judge 装置**上的延伸。

**19. JUDGe 2026 — Can We Trust the Judge?（First Workshop on Reliable Evaluation for Language Models）**（Organizers: Shanu Sushmita, Jayash Koshal, Meghana Makhija, Hui Wan, Amjad Abu-Jbara；NeurIPS 2026, Atlanta, 2026-12-12/13）`https://judge2026.github.io/` · **核验-摘要**
- 核心贡献：**首个把"评估者可靠性/效度"当作系统问题**的 NeurIPS workshop。核心命题："**效度不是 judge 单独的性质，而是 judge 在系统中的性质**"——一个校准良好的评估器放进管线（门控安全决策、回灌训练）后会系统性失效。给出 **7 个失败 facet**（表面对语义敏感、criteria drift、位置偏置、谄媚/自我偏好、推理链效度、安全相关语义漂移、跨 judge 一致性），并产出 **Judge Deployment Disclosure Template**（类比 model card，但对象是**评估管线**）。
- 与 Queyi 的关系：**"评估者审计"作为独立议题制度化的最强信号**——可直接引用其"效度是系统性质"论点为 Queyi 的"装置第一性"背书；其 Disclosure Template 与 Queyi 的 caliber/口径披露**同构**。区别：JUDGe 的对象是 **LLM judge**，其"系统"指 RLHF/DPO 管线；Queyi 的对象是**软件验证证据获取装置**，其"系统"指编译器/sanitizer/linker 链 + 执行环境。**Queyi 可把 JUDGe 的 7 facet 框架当作"同类但不同对象"的对照**，并指出 JUDGe 未覆盖 Queyi 的"环境省略静默失效"（发现 3）这一维度。

**20. Learning to Evaluate: Cost-Effective Model Evaluation on Unlabeled Data with Meta-Learning（MetaEvaluator）**（Trinh Pham, Viet Huynh, Hongzhi Yin, Quoc Viet Hung Nguyen, Thanh Tam Nguyen, 2026, KDD 2026）`https://arxiv.org/abs/2605.23595` · **核验-摘要**
- 核心贡献：提出 **MetaEvaluator**——一个**模型无关、免标注**的评估框架，通过在一池参考模型上元学习得到有效初始化，从而对**未见模型**在无标注数据上快速给出评估。声称是**首个在无标注数据集上评估新模型的模型无关框架**，大幅降低评估成本。
- 与 Queyi 的关系：**"评估器本身也是可学习对象"的代表**，与 Queyi 的"评估器自身是科学对象"的立场同向。区别：MetaEvaluator 把评估器当作**要被优化的预测器**（成本/精度），Queyi 把评估器当作**要被审计的测量仪器**（边界/口径）。两者是"优化评估器"与"审计评估器"的分野——**可作 Related Work 里一句话的对照**。

---

## 2. 关键发现与趋势总结

1. **"评估器审计"在 2026 年已从个案升级为独立议题，但对象集中在三类：基准数据集、LLM judge、评估协议。** 20 条里有 6 条（#1–#6）明确做"审计评估装置"，但审计对象几乎全是 **benchmark / judge / protocol**。**没有一篇审计"软件验证的证据获取装置"**（sanitizer/编译器/linker + 执行环境）。这既是 Queyi 的空位，也是必须正视的"同类工作压力"。

2. **"表观分 ≠ 真实能力"已成为 2026 年的共识命题，且有两条独立证据链。** 一条是**评分缺陷链**（#2 的 18.5% 错位、18.9pp 方差；#3 的 Mislead gap 0.45–1.00；#4 的 219 个缺陷），一条是**测量学链**（#7 构念效度、#10 NIST 统计有效性、#8 item-level）。Queyi 的"+24pp 坍缩"应明确**归入第三条链：装置退化链**——这是三条链里目前**最少被形式化**的一条。

3. **Goodhart 的形式化正在快速成熟，但全部聚焦"优化压力"。** #12（去独立性的范式无关形式化）与 #13（几何 + 早停）都在刻画"**因为被当作目标去优化**"而失效。Queyi 发现 1 的坍缩**不需要优化压力**（退化资产 + 口径混淆即可），这是一个**可命名的新子类**（"被动/结构性 Goodhart"），有理论增量空间。

4. **"基准退化"被两条不同机制占据：饱和（模型追平）与漂移（分布/装置变化）。** #14 定义 saturation 为"失去统计上可靠的可区分性"，#15 把 variance 定义为 validation crisis，#17 把 drift 工具化。**Queyi 的坍缩与 #14 的饱和在"失去区分度"上同形（k=4 Δ=0），但机制完全不同**（非模型变强，而是装置退化）。这是最值得写进论文的"同形不同因"对照。

5. **测量学词汇（构念效度、信度、IRT、有效样本量、GLMM）正在大规模进入 ML 评估。** #7 #8 #9 #10 #11 五条构成一个清晰的"测量科学化"浪潮。**Queyi 的 deff≈4 / 有效 n≈133–140 正好可以借用这套词汇**，把"家族聚类"从工程观察升级为**测量学结论**。

6. **审计的方法论正在"攻击化 + 制度化"双轨推进。** 攻击化：#3 HackDetect、#4 BenchJack（主动红队）；制度化：#19 JUDGe（workshop + Disclosure Template）、#1 的"扣留/披露协议"。**Queyi 目前两头都不占**——既非红队，也无第三方裁判（与 693 的缺口一致）。论文应诚实声明定位为"**装置自省 + 量化坐标**"，而非"已审计"。

---

## 3. "评估器审计"这个概念的精确坐标（回答硬性要求 3）

### 3.1 有人做过吗？——做过，但**对象不同**

2025–2026 年确有大量工作在做"审计评估器"，且 2026 年已形成**三个明确子类**：

| 子类 | 审计对象 | 代表 | 审计产出 |
|---|---|---|---|
| **审计基准** | benchmark 数据集/题目 | #2（tool-calling 效度审计）、#5（Benchmark²）、#6（样本级审计）、#14（饱和） | 错位率、可区分度、饱和率 |
| **审计 judge** | LLM-as-a-Judge 评分器 | #18（541k 判定）、#19（JUDGe workshop） | κ 落差、位置偏置、7 失败 facet |
| **审计协议/管线** | evaluation protocol / 评分逻辑 | #3（protocol validity + HackDetect）、#4（BenchJack）、#1（audit-of-audit） | Mislead gap、缺陷分类、五类管线失效 |

**关键区分**：
- **审计"基准"** = 审计**被测量对象**（题目好不好）。
- **审计"judge"** = 审计**评分者**（打分准不准）。
- **审计"协议/管线"** = 审计**流程**（评分逻辑/执行链可不可信）。
- **#1「Auditing the Audit」** 是唯一的**元-元层级**：审计"审计流程"本身，指出**审计结论可被实现细节静默制造**。

### 3.2 Queyi 审计的是什么？——**"证据获取装置"，一个尚未被占据的位置**

Queyi 的对象既不是基准数据集，也不是 judge，也不是评分协议，而是**产生"缺陷是否存在"这一 ground truth 的装置集合**：
- **caliber（口径）**：分母/标签定义；
- **资产（asset）**：sanitizer / 编译器告警 / linker 等**证据生产工具**；
- **环境（environment）**：WSL vs native 等**执行坐标**；
- **标签（label）**：缺陷存在性判定；
- **分母（denominator）**：语料与有效样本量。

### 3.3 与既有"评估器审计"的三点本质区别

1. **审计对象从"测量结果"前移到"测量仪器"。** 所有既有工作审计的是"分数/评分/题目"（**输出侧**）；Queyi 审计的是"**产出 ground truth 的工具链**"（**输入侧/仪器侧**）。这是**测量学里"从测结果到测仪器"的位移**，目前**没有对应文献**。
2. **失效机制从"对抗性"扩展到"结构性/静默"。** #3/#4 的失效需要 **agent 主动利用**；Queyi 发现 3 的"环境省略静默失效"（WSL 60.07% → native 24.74%，**Δunknown=0**）是**无人恶意、无报警、无 unknown 增长**的**静默退化**——比 reward hacking 更隐蔽，现有文献**未刻画**。
3. **审计产出从"披露/修补"转向"量化坐标"。** #1 产出"扣留/披露协议"、#4 产出"修补补丁"、#19 产出"披露模板"；Queyi 产出的是**装置在什么条件下给出什么结论的坐标**（表观增益坍缩曲线、盲区率 38.4%、deff≈4）。**这是"审计 = 出结论"而非"审计 = 出建议"的路线**。

> **一句话定位**：现有"评估器审计"审计的是**测量结果**（benchmark/judge/protocol）；Queyi 审计的是**测量仪器**（软件验证证据获取装置）。Queyi 的空位在于**仪器侧的静默退化**，风险在于**需自证这不是"又一个基准审计"**——建议用 §4.2 的对照表把差异写死在论文里。

---

## 4. 对 Queyi 的启示

### 4.1 可以引用什么（具体到 claim）

| Queyi 的 claim | 引用 | 引用方式 |
|---|---|---|
| 发现 1（+24pp 表观增益坍缩、k=4 Δ=0） | #2（18.5% 错位、18.9pp 方差）、#3（Mislead gap 0.45–1.00）、#12（Goodhart 形式化） | "表观分可被装置/评分缺陷制造"已有独立证据；Queyi 补充**装置退化**这一条链 |
| 发现 2（38.4% 盲区、13/34 类型 >50% 盲） | #6（样本级异质性）、#11（ADeLe 尺度）、#7（构念效度） | "聚合分掩盖内部异质性"有同构证据；Queyi 的异质性在**缺陷类型**维度 |
| 发现 3（WSL 60.07%→native 24.74%，Δunknown=0） | #17（漂移的受控注入与归一化度量）、#15（validation crisis） | 借"漂移度量"工具箱；Queyi 的漂移是**环境坐标**而非数据分布 |
| 发现 4（operator ≡ greedy set-cover） | （684/685 已有子模文献） | 本批**不新增**，维持原引 |
| 发现 5（合成 vs 真实 −17.92pp） | #8（item-level 数据）、#10（NIST benchmark vs generalized accuracy） | "口径/总体不同则结论不同"的官方背书 |
| 发现 6（deff≈4、有效 n≈133–140） | #9（LLM Psychometrics）、#10（GLMM 方差分解）、#15（sample gain） | 把"家族聚类"用**测量学语言**重述 |
| 发现 7（LLM=预算门控 vs sanitizer=能力边界） | #18（可靠性≠效度、一致性-偏置悖论）、#19（JUDGe 7 facet） | "单一效度指标不足"；Queyi 补充**装置类型维度** |
| 整体立场（评估器自身是科学对象） | #1（audit-of-audit）、#4（安全设计）、#19（效度是系统性质）、#5（元评估） | 立场背书 + 说明 Queyi 处于"仪器侧"空位 |

### 4.2 可以对比什么（表格式定位区别）

| 维度 | #1 Auditing the Audit | #2 Benchmarking the Benchmarks | #3 HackDetect | #4 BenchJack | #19 JUDGe | **Queyi（本工作）** |
|---|---|---|---|---|---|---|
| **审计对象** | 审计流程（元-元） | tool-calling 基准的评估器 | agent 基准协议 | agent 基准漏洞 | LLM judge | **软件验证证据获取装置** |
| **对象层级** | 流程 | 结果/评分 | 协议 | 结果/漏洞 | 评分者 | **仪器（sanitizer/编译器/linker/环境）** |
| **失效机制** | 实现细节静默制造结论 | 评分逻辑缺陷 | 对抗性利用 | 对抗性 hack | judge 偏置/漂移 | **非对抗的装置退化 + 静默环境失效** |
| **是否需要恶意方** | 否 | 否 | **是** | **是** | 否 | **否** |
| **产出** | 扣留/披露协议 | 更正组件 | Mislead gap | 修补补丁 | Disclosure Template | **量化坐标（坍缩/盲区/deff）** |
| **领域** | LLM 安全基准 | tool-calling | agent | agent | LLM judge | **软件验证（C/C++）** |

### 4.3 可以升级什么（指向理论升级）

1. **measurement drift 的形式化（最高优先级）。** 模板取 #12（去独立性的 Goodhart 形式化）+ #13（几何刻画 + 临界点）。建议形式化：把 Queyi 的"装置配置 e（caliber/资产/环境/标签/分母）"作为自变量，报告率 $\hat R(e)$ 作为观测量，机制级率 $R^\*(e)$ 作为目标量，定义**测量漂移** $D(e) = \hat R(e) - R^\*(e)$。发现 1 即 $D$ 在退化资产下**不收敛到 0 却仍产生表观增益**；发现 3 即 $D$ 在换环境时**阶跃且无报警**。**可命名新子类："无优化压力的结构性 Goodhart"**——这是 #12/#13 均未覆盖的情形。

2. **把"静默退化"做成一个可判定的指纹。** 借 #16（CapBencher 的内置报警器）的思路：定义一个**不依赖外部裁判**的可计算异常量（如"换环境后 Δunknown=0 但主率大幅下降"），作为**静默退化的充要指纹**。这是 Queyi 对 #16"防外部作弊"的**镜像贡献**（防内部静默退化）。

3. **把 deff≈4 升级为测量学结论。** 用 #9（心理测量学）+ #10（GLMM 方差分解）的语言重写发现 6：把"缺陷家族"当作**聚类结构**，报告 **ICC / 设计效应 / 有效样本量**，并说明"基准的**名义 n** 与**有效 n** 的差距"如何使排行榜区分度被高估。这与 #15 的"sample gain"、#14 的"可区分性"形成**同一测量学谱系**。

4. **（可选）把"证据获取装置"提升为一个通用概念。** 若理论升级成功，Queyi 的"装置审计协议"可声明为**可迁移到其它"证据获取装置"**（如 fuzzing 装置、形式化验证器、静态分析器），把本工作从"一个案例"升级为"一个协议 + 一个案例"。**但须诚实标注：本批未找到同类先例，迁移性是**主张**而非**已验证**结论。**

---

## 5. 检索记录（可复核）

> 检索工具为通用 WebSearch（非学术数据库系统检索，无 Scopus/DBLP/ACM DL 全文）。核验用 WebFetch 打开 `arxiv.org/abs/<id>` 或官方页。日期均为 **2026-10-08**。

| # | 检索词 | 日期 | 命中的可用条目 |
|---|---|---|---|
| S1 | `evaluator auditing machine learning benchmark meta-evaluation 2026` | 2026-10-08 | #6、#20 |
| S2 | `measurement drift machine learning evaluation benchmark degradation formalization` | 2026-10-08 | #17 |
| S3 | `Goodhart's law machine learning evaluation formalization metric gaming 2025 2026` | 2026-10-08 | （多为博客）→ 转 S7/S9 |
| S4 | `construct validity benchmark NLP evaluation crisis 2025 2026` | 2026-10-08 | #7 |
| S5 | `benchmark contamination measurement evaluation pipeline stress testing 2026` | 2026-10-08 | （多为博客） |
| S6 | `auditing evaluation pipelines LLM judge reliability meta-evaluation NeurIPS 2025 2026` | 2026-10-08 | #19 |
| S7 | `"Goodhart" formalization geometric theory machine learning arXiv 2025` | 2026-10-08 | #13 |
| S8 | `evaluator reliability validity workshop NeurIPS 2026 JUDGe position paper` | 2026-10-08 | #19 |
| S9 | `arxiv Goodhart's law independence-free paradigm-agnostic formalisation strong weak benign` | 2026-10-08 | #12 |
| S10 | `benchmark saturation rot evaluation science LLM 2026 position paper` | 2026-10-08 | #14 |
| S11 | `negative results benchmark evaluation dataset audit NeurIPS datasets track 2025 2026` | 2026-10-08 | NeurIPS 官方 blog（背景，未列条目） |
| S12 | `"benchmark" audit construct validity measurement theory ML evaluation 2026 arXiv` | 2026-10-08 | #1、#7 |
| S13 | `auditing the evaluator benchmark itself measuring benchmark quality meta-benchmark 2025` | 2026-10-08 | #2、#5 |
| S14 | `"measurement drift" OR "metric drift" evaluation benchmark formal theory 2026 arXiv` | 2026-10-08 | #17 |
| S15 | `benchmark validity crisis measurement invariance ML evaluation statistical rigor 2026` | 2026-10-08 | #15、#10（NIST） |
| S16 | `metric gaming benchmark overfitting evaluation protocol flaws LLM 2026 arXiv` | 2026-10-08 | #16 |
| S17 | `LLM judge audit reliability validity position paper 2026 arXiv meta-evaluation judge` | 2026-10-08 | #18 |
| S18 | `software verification evaluation benchmark soundness auditing 2026 arXiv` | 2026-10-08 | （SoundnessBench，未列） |
| S19 | `"evaluator" audit "evidence" acquisition measurement instrument validity 2026 arXiv benchmark protocol` | 2026-10-08 | #3、#2 |
| S20 | `"evaluation science" OR "science of evaluation" AI benchmarks 2026 arXiv framing discipline` | 2026-10-08 | #8、#11 |
| S21 | `benchmark evaluation construct validity measurement invariance psychometrics LLM 2026 arXiv` | 2026-10-08 | #9 |
| S22 | `Nature "General scales unlock AI evaluation" 2026 authors` | 2026-10-08 | #11（核验-检索） |

**核验动作记录**：实际打开并核对元数据的页面共 **19 个**（`arxiv.org/abs/2607.02586`、`2511.04703`、`2602.16763`、`2607.28801`、`2606.19544`、`2505.23445`、`2607.02577`、`2601.03986`、`2606.12552`、`2505.18102`、`2606.07789`、`2310.09144`、`2605.23595`、`2605.12673`、`2607.22368`、`2604.03244`、`2505.08245`，外加 `judge2026.github.io` 与 `nist.gov` 官方页）；**1 个**页面（Nature，`s41586-026-10303-2`）因 Cloudflare 拦截**未能打开**，标为 `核验-检索`。

---

## 6. 与 684 / 685 / 693 已有调研的关系

### 6.1 已有基础（不重复登记）
- **684** `684_related_work_supplement.md`（18 篇）：子模优化、主动测试、**治理/Goodhart 的经典根**（Goodhart 1975、Strathern 1997、Gebru 2021、Mitchell 2019、Pineau 2021、Raji 2021）。
- **685** `685_literature_survey.md`（39 篇）：四领域（submodular 12 / eval 12 / active 9 / info 6），eval 领域含 HELM、Emergent Mirage、BIG-bench、Skalse 2022、Leaderboard Illusion。
- **693** `693_related_work_update.md`（5 条）：HOW2BENCH、fuzzer vs static analysis、SV-COMP 2026、NeurIPS 2026 track blog、LLM-Judge Validation（二手转述）。

### 6.2 本批（695）新增了什么

| 类别 | 内容 |
|---|---|
| **全新主题** | **"评估器审计"作为一个 2026 年独立议题**（#1–#6、#18–#19）；684/685/693 **完全没有**覆盖"审计基准/审计 judge/审计协议"这一簇。 |
| **全新主题** | **Goodhart 的形式化文献**（#12、#13）。685 只有 Goodhart 1975 的**经典根**与 Skalse 2022（reward hacking），**没有** 2025–2026 的**形式化**工作——这是 measurement drift 理论化的直接缺口，本批补上。 |
| **全新主题** | **基准饱和 / validation crisis / 漂移度量工具箱**（#14、#15、#16、#17）。685 的 eval 领域未含。 |
| **全新主题** | **测量科学化浪潮**（#7、#8、#9、#10、#11）：构念效度、item-level、心理测量学、NIST 统计模型。685 仅到 HELM/Model Cards 层面，**未进入测量学**。 |
| **补细节（非新增）** | #18（LLM-as-a-Judge 大规模审计）是 693 的 N5（二手转述）的**升级版**——从"未读原文的转述"升级为**已核验的原始文献**。 |

### 6.3 一句话总括
684/685/693 覆盖的是**方法学工具（子模/主动学习/信息论）+ 治理叙事（Goodhart 经典/Model Cards）+ 少量 2026 补漏**；**695 补上了"评估器审计 + 测量漂移形式化 + 基准退化/饱和"这条 2026 年最热的线**，且是本批唯一**逐条联网核验**的调研（693 的 N5 甚至标为"未读原文"）。**新增为主，补细节为辅。**

---

## 附：落地前必读的诚实边界

1. **本批核验只到"元数据真实"层面**，未精读全文；条目里的"核心贡献"是 abs 摘要的转述，**引用前须读原文**。
2. **#11（Nature）为 `核验-检索`**，作者与确切标题**未逐字核对**，落地前必须打开原文确认。
3. 本批**未找到**任何"审计软件验证证据获取装置"的同类先例——这是 Queyi 的空位，但也意味着**Queyi 需要自证不是"又一个基准审计"**（见 §4.2 对照表）。
4. 检索为**定向补漏**性质，**不是系统综述**（无数据库全文检索），可能漏掉未进入通用搜索索引的工作。
