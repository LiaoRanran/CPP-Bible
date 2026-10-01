# 阙疑（Queyi）：让**验证能力**可被独立验收
## —— 面向 LLM 生成技术知识的失败驱动验证系统（v0.5 初稿）

> **本稿的三条硬纪律（写在最前面，因为后面每一章都受它约束）**
>
> 1. **数字分两类**：① *已落盘可复算*（有产物与复算命令，本稿直接引用并标注来源命令）；
>    ② *等待 669 批次实验*（一律写成 `{{TODO_669: …}}` 占位符，**不填任何编造值**）。
> 2. **Claim 分三档**：能支撑 / 不能支撑 / 不可复现（后者是新增栏，对应 667 规划 A25）。
>    凡"能支撑"的，必须能答出"复算命令是什么"。
> 3. **AI 参与留痕**：本稿由 LLM 辅助起草，**逐处登记在 `research/AI_USAGE_shturl`**；
>    未登记的 AI 贡献按本项目纪律视为未声明作者（`research/13_ai_use_and_authorship.md`）。
>
> **上游**：`research/paper_v0.4.md`（v0.4.1 数字修订）、`docs/669_调研消化/06_论文章节映射.md`（章节缺口）、
> `docs/669_调研消化/02_可落地行动清单.md`（P0 行动）、`data/668_acceptance_report.md`（最新真实数字）、
> `docs/667_究极大规划.md`（实验设计）、`docs/669_独立审计.md`（本次同步完成的第三方只读审计）。
>
> **⚠ 引用前必读（审计结论前置）**：`docs/669_独立审计.md` 给出总体可信度 **6/10**，并指出
> **holdout 与 external corpus 两个数字依赖未被声明的 WSL 环境**，在缺 WSL 的机器上重跑会
> **静默掉分**（external 35.0% → 10.0%）而现有护栏仍报绿。**在 P0-1/P0-2 修复前，
> 第 6 章的任何数字都不得对外引用。**

---

## 摘要

LLM 正在大量生产技术知识（断言、规则、教程），但"这些知识对不对"缺少可独立复算的判据。
已有的两条路都不解决问题：**用模型评模型**（LLM-as-a-judge）把验证者与被验证者放在同一个失效域里；
**检测文本是否 AI 生成**则答错了问题——文本来源与断言真假无关。

本文提出**阙疑（Queyi）**：一个把"结论—证据—复算"三者**绑成一条可被外部打断的链**的验证系统。
它的对象不是模型输出，而是**可执行的 C++ 知识断言**；它的判决不是二值，而是
**四态 `pass / fail / unknown / contradict`**（`unknown` 与 `miss` 严格分离）；
它的可信度不来自自证，而来自三件事：证据带 provenance 且语义作用域（semantic scope）单独声明、
元状态由**不依赖内核**的独立对账器核对、**失败驱动**地把每一个外部样本的漏检转化为新的验证能力。

**我们主张的核心区别**：Benchmark Self-Evolving、ArenaBencher 一类工作演化的是**题目**（让 benchmark 变新变难）；
我们演化的是**验证能力**（让 judge 变强），并且要求这种演化能被外部样本度量、能被第三方复算、能被证明"不是把分数刷上去的"。

系统现状（全部有复算命令）：判决规则 **67** 条内嵌引擎；实卡 **42** 张 + 草稿 10；
权威账本 **452** 事件（零改动红线）；Merkle 目录根覆盖 **5** 个受控目录；
holdout 盲态样本检出率 **87.5%（14/16）**（双档 `-O0`+`-O2` 口径，分母 = catch+miss）；
外部 corpus 全样本口径 **35.0%（14/40）**、可测口径 43.8%（14/32）；
反事实算子 F1 **1.0（上界，分母 10）**。
第 6 章的三个实验（主实验 / ablation / 演化曲线）结果**全部留占位符**，待 669 批次填入。

**关键词**：知识验证 · 四态判决 · 失败驱动演化 · 可复现评估 · LLM 生成内容 · 度量治理

---

## 1. 引言（Introduction）

### 1.1 问题：生成容易，验证困难

一个 LLM 可以在几分钟内写出上千条关于 C++ 的技术断言（"这个写法是未定义行为""这个优化在 -O2 下成立"）。
这些断言有三个特点：**量大**（人工逐条核不动）、**似真**（语法、术语、语气都对）、
**错误隐蔽**（错的那些通常只在特定编译档、特定编译器、特定平台上才暴露）。

于是产生一个不对称：**生成成本趋近于零，而验证成本不变**。这个不对称是本工作的问题起点。

### 1.2 三条动机（为什么现有办法不够）

**动机一 · SWE-bench 的污染教训：分数高不等于能力强。**
SWE-bench（Jimenez 等，ICLR 2024）把"修真实 GitHub issue"变成了 LLM 编码能力的标准标尺 [1]。
但后续工作给出了系统性的反证：Liang 等（2025）用"只看 issue 文本猜文件路径"和"复现 ground-truth 函数"两个诊断任务
证明 SWE-bench-Verified 上的提升**部分来自记忆而非推理**——模型在 SWE-bench 仓库上定位准确率最高 76%，
在仓库外的同类任务上只有最高 53% [2]；Prathifkumar 等（2025）用同样思路发现模型在 SWE-bench-Verified 上的表现
是另外两个同类基准的 **3 倍**、定位编辑文件的能力是 **6 倍**，而该任务在逻辑上本应无法完成 [3]。
SWE-MERA 进一步报告 SWE-bench 上 32.67% 的成功补丁涉及直接解法泄漏、31.08% 因测试用例不充分而误通过 [4]。

> **对本工作的意义**：一个"验证系统"如果也用自己熟悉的数据测自己，就会复现同样的失败。
> 这直接决定了我们的三条设计：**外部样本优先**（§5.1 的 D2/D3/D4）、**盲态不可逆**（§5.4）、
> **分层报告而不合并成一个漂亮数字**（§5.5）。

**动机二 · AI 文本检测是一个答错了问题的问题。**
DetectGPT（Mitchell 等，ICML 2023）用概率曲率做零样本机器文本检测 [5]；
水印方案（Kirchenbauer 等，ICML 2023）在生成侧嵌入可检测信号 [6]。
但 Sadasivan 等（TMLR）证明：**在非对抗 setting 下检测器的可靠性本身就随文本长度与领域急剧退化，
且对改写/同义替换极其脆弱** [7]。更根本的是——**"这段文本是不是 AI 写的"与"这个断言是不是真的"是两个独立的问题**。
一段人写的 C++ 知识同样可能是错的；一段 AI 写的推导同样可能是对的。

> **对本工作的意义**：我们不检测来源，我们**检验断言**。判据一律是"跑一遍看会发生什么"
> （编译、告警、sanitizer、跨编译器差分、跨优化档差分），而不是"这段话像不像机器写的"。

**动机三 · 监管把 provenance 从"好习惯"变成"义务"。**
欧盟《人工智能法》Regulation (EU) 2024/1689 第 50 条对生成式 AI 输出规定了透明度义务
（机器可读标记与可追溯性要求）[8]。这与本系统的 provenance 设计同向：
**每条知识必须携带"谁生成的 / 谁验的 / 证据在哪 / 在什么条件下成立"**。

### 1.3 贡献（三段式）

1. **一个验证系统（§4）**：`atoms → evidence → verdict → ledger` 的四层结构；
   四态判决；L0/L1 门禁分层；**provenance 与 semantic scope 强制拆分**；
   **不依赖内核的元状态对账器**（反自证）；以及核心机制——
   **失败驱动的验证能力演化闭环**（外部样本漏检 ⇒ 新增证据获取能力 ⇒ 回到同一批外部样本重测）。
2. **一套实验协议（§5）**：五层数据集 D0–D4（开发 / 历史缺陷 / 盲 holdout / 外部 corpus / 独立生成），
   三类 baseline（静态门禁 / 静态+变异 / budget-matched random），
   A–F 六组 ablation（每组预写假设），七项指标，以及**先冻结后执行**的统计口径
   （Clopper–Pearson 主报、Wilson 敏感性、Fisher/Boschloo、精确 McNemar、BH/Holm）。
3. **一份开放 artifact（§5.6、§9）**：Merkle 目录根 + 透明日志 + 452 事件权威账本 +
   逐样本明细产物 + **单命令复算入口**。任何人可以不信任我们而验证我们——
   （a）复跑 `--check` 验签名，（b）用给出的命令重跑编译/检测，
   （c）在不服时指出**哪一环**证据不足。

### 1.4 我们不主张什么（引言就写清楚）

我们**不**主张做出了更好的 C++ 教材，**不**主张做出了更强的检测器，
**不**提供形式化证明。**不**声称"验证器变强了"，除非这个"变强"是在
**同一批外部样本、同一口径**下被度量的（§6.3 的演化曲线专门测这件事）。

---

## 2. 相关工作（Related Work）

> **诚实前置**：v0.4 §7 曾声明"60 个方向调研的原始材料未留存"。
> 本稿按 `669_调研消化/02` 的 A32 处置：**不再出现"据调研"这类无源表述**，
> 下表每一条都给可查证的出处，且我们在 §2.4 明确标注**哪些对比是定位性的、不是实测的**。

### 2.1 自演化 / 抗污染 benchmark（演化的是题目）

| 工作 | 演化的对象 | 机制 |
|---|---|---|
| **Benchmark Self-Evolving**（Wang 等，COLING 2025, arXiv:2402.11443）[9] | 题目难度与分布 | 多智能体协作改写/扩充现有 benchmark |
| **ArenaBencher**（Liu 等，arXiv:2510.08569）[10] | 测试用例 | 多模型竞争式评估，自动更新测试项以对抗数据泄漏 |
| **SWE-bench-Live**（Zhang 等，arXiv:2505.23419）[11] | 样本时效性 | 从持续新增的真实 GitHub issue 自动构造任务 + 每任务 Docker 镜像 |
| **DynaBench**（Kiela 等，NAACL 2021, arXiv:2104.14337）[12] | 样本（人在环） | 标注者专门构造能让目标模型出错、人不出错的样本 |
| **LiveBench**（White 等，ICLR 2025 Spotlight, arXiv:2406.19314）[13] | 题目新鲜度 | 月度更新 + 客观 ground truth 自动评分，规避 LLM 评审与人工众包偏差 |

**共同点**：它们都在对抗"模型记住了题目"。**分歧点**：它们演化的是**被测对象**，
而"谁来判、判得对不对"仍然由固定的测试/裁判承担。

### 2.2 LLM 变异引导的测试生成（最接近的工程形态）

- **ACH / Mutation-Guided LLM-based Test Generation at Meta**（Foster、Gulati、Harman 等，arXiv:2501.12862，FSE 2025 主题报告）[14]：
  用 LLM 生成"高度相关的变异体"与"保证能杀死这些变异体的测试"，把变异测试从**评估手段**变成**生成手段**，
  并用于合规加固（Automated Compliance Hardening）。
- **MUTGEN**（Wang、Xu、Briand、Liu，IEEE TSE，arXiv:2506.02954）[15]：
  把变异反馈直接写进 prompt，在 204 个被测对象上显著优于 EvoSuite 与朴素 prompt；
  并给出一个关键观察——**有些测试套件 100% 覆盖率却只有 4% 变异得分**。
- **Cleverest**（Liu、Lee、Losiouk、Böhme，PACMSE 3(FSE)，arXiv:2501.11086）[16]：
  LLM 做即时回归测试生成，2 分钟内找到的 bug 数与定向灰盒模糊器 24 小时相当。

**与我们的关系**：我们**复用**"变异反馈驱动生成"这一思路（内部自证层，§4.3 的 L1），
但明确**拒绝**把变异得分当作缺陷检测率（§3.3 的 T7 度量混淆、§8.1 的 construct 威胁）。
ACH/MUTGEN 的变异体是**我们自己设计的**，验证器"熟悉"它们——这正是我们要用外部样本对冲的东西。

### 2.3 LLM-as-a-Judge 与程序验证（两条我们部分采用、部分拒绝的路）

- **LLM-as-a-judge**（Zheng 等，NeurIPS 2023 D&B，arXiv:2306.05685）[17]：
  用强模型评弱模型，是当下最实用的可扩展评审手段。我们**只在"生成候选"环节使用 LLM，
  在"判决"环节不用**——判决全部程序化（§4.2）。理由是：judge 与被 judge 共享失效域。
- **形式化验证**：seL4（Klein 等，SOSP 2009 / CACM 2010）[18]、CompCert（Leroy，CACM 2009）[19]
  证明了"证明力可以做到极强"。代价是**极高的人力成本与极窄的覆盖面**，且**证明本身难被外部复核**。
  我们**明确不追形式化证明**（667 规划 §9 冻结清单），转而追"**证据可被第三方逐条复算**"——
  这是一个可验证性/覆盖面的不同取舍点，而不是"更差的证明"。
- **变异测试综述**（Jia & Harman，IEEE TSE 2011）[20]：变异测试五十年发展的系统梳理。
  我们采用它的框架，但**只用于自证层**。

### 2.4 度量治理与可复现性（我们的方法学来源）

- **Goodhart 定律**与"当一项指标成为目标，它就不再是好指标"（Strathern, 1997；源于 Goodhart, 1975）[21]；
  **reward hacking 的形式化刻画**（Skalse 等，arXiv:2209.13085）[22]；
  **奖励模型过优化的缩放律**（Gao 等，ICML 2023，arXiv:2210.10760）[23]。
- **Datasheets for Datasets**（Gebru 等，CACM 2021，arXiv:1803.09010）[24] 与
  **Model Cards**（Mitchell 等，FAT\* 2019，arXiv:1810.03993）[25]：文档化即治理。
  本系统的 `denominator` / `caliber` / `env` 字段就是"数据集说明书"在**单个数字粒度**上的落地。
- **机器学习可复现性**（Pineau 等，JMLR 2021）[26]：复现清单与"可复现性不是声明而是机制"。
- **统计方法**：Clopper–Pearson 精确区间（1934）[27]、Fisher 精确检验 [28]、
  McNemar 检验（1947）[29]、BH-FDR（1995）[30] 与 Holm 校正（1979）[31]、Cohen's κ（1960）[32]。

### 2.5 形式化验证与 LLM 辅助证明（我们明确不追的"强证明"）

- **LLVM Translation Validation Automated with LLMs and Lean**（Liao 等，arXiv:2609.19583，2026-09-17）[37]：用 LLM 把 LLVM IR 的翻译验证条件生成出来，再交给 Lean 证明；代表"LLM 做苦力、证明器做裁决"的路线。
- **Can LLMs Enable Verification in Mainstream Programming?**（Shefer 等，arXiv:2503.14183，2025-03-18）[38]：系统评估 LLM 在主流语言验证（Dafny/Coq 风格）中的可用性，结论是"能辅助、不能替代"。
- **Formal Disco**（Poesia 等，arXiv:2607.04631，2026-07-06）[39]：开放式的、可扩展的形式化验证程序生成。

**与我们的关系**：§2.3 已列 seL4/CompCert 证明"证明力可以极强"。本批补的 3 篇说明**LLM 正在把形式化验证从奢侈品变工具**，但代价仍是证明器依赖与窄覆盖面。我们**坚持不追形式化证明**（667 冻结清单），只追"证据可被第三方逐条复算"——与 [37][38][39] 的"LLM 辅助、证明器裁决"是**互补而非竞争**：我们连证明器都不必有，只要规则可复算。

### 2.6 LLM 代码错误分类与诊断（我们"检错"的对手方文献）

- **All Smoke, No Alarm: Oracle Signals in Agent-Authored Test Code**（Banik 等，arXiv:2606.18168，2026-06-16）[40]：指出 agent 生成的测试里藏着"看起来像断言、实际不检验任何东西"的 oracle 信号——这正是我们 §4.2 四态与 `caliber` 字段要显式排除的"假命中"。
- **Uncovering Weaknesses in Neural Code Generation**（Lian 等，arXiv:2407.09793，2024-07-13）[41]：系统刻画神经代码生成的失败模式，可与 §7.1 的错误类型分析对照。
- **Will Your Next Pair Programming Partner Be Human?**（Lyu 等，arXiv:2505.08119，2025-05-12）[42]：一学期课堂实测中 generative AI 作为协作队友的实证——提供"人 vs AI 检错"的对照视角。

**与我们的关系**：[40] 的"oracle 信号"问题直接对应我们的 construct 威胁（§8.1）——检测器报 `catch` 不等于断言为真；我们的 third_criterion（machine_marker，§6.4）就是为对冲这类"假 oracle"而设。

### 2.7 溯源审计与证据问责（我们的 provenance / OTS 方向的同行）

- **Constant-Size Cryptographic Evidence Structures for Regulated AI Workflows**（Kao，arXiv:2511.17118，2025-11-21）[43]：受监管 AI 工作流下的定长密码学证据结构——与我们 §4.4 的 provenance 三元组（`mutation_set_hash` / `mutation_count` / `generator_version`）同源。
- **Who Audits the Auditor? Tamper-Proof Fraud Detection with Blockchain-Anchored Explainable ML**（Wang，arXiv:2604.22096，2026-04-23）[44]：区块链锚定的防篡改可解释 ML——对应我们 §8.5 的 Merkle 目录根 + OTS 时间锚方向。
- **A Systematic Review of NeurIPS Dataset Management Practices**（Wu 等，arXiv:2411.00266，2024-10-31）[45]：数据集管理实践的系统综述——与 §2.4 的 Datasheets/Model Cards 一脉相承，给出"数据出处治理"的同行证据。

**与我们的关系**：我们的 provenance 强制拆分（§4.4）与 Merkle+OTS（§8.5）属于"证据问责"这一方向；[43][44] 证明这是受监管场景的活跃研究线，[45] 提供数据集侧的治理参照。需注意：我们的 OTS 锚当前仍是**零 attestation 占位符**（§8.5 残余风险），尚未达到 [44] 的"真锚定"标准。

### 2.8 定位：我们做的不是 benchmark 演化，是**验证能力演化**

| 维度 | Benchmark 演化（§2.1） | 变异引导测试生成（§2.2） | 形式化验证（§2.3） | **阙疑（本工作）** |
|---|---|---|---|---|
| 演化的对象 | 题目/样本 | 测试与变异体 | 证明（静态） | **判决能力与证据获取能力** |
| 谁判对错 | 固定测试/裁判 | 固定测试 oracle | 证明检查器 | **程序化规则 + 四态 + 元状态对账** |
| 能否表达"不知道" | 通常不能 | 通常不能 | 不适用 | **能（`unknown` 是一等公民）** |
| 分数提升的含义 | 模型变强 | 测试套件变强 | 无分数 | **验证能力变强**（需外部样本度量） |
| 防"刷分"的机制 | 换新题 | 换变异体 | 不适用 | **失败驱动 + 盲态 + 预算匹配对照** |

**一句话定位**：在"生成—评估"的军备竞赛里，前面所有工作都在换**被测物**；
我们换的是**尺子**，并且要求**换尺子这件事本身可被外部度量**（§6.3 演化曲线）、
**可被证明不是把刻度偷偷改短**（§4.6 的"旧数字作废"纪律与 §8.1 的 meta-Goodhart 缓解）。

> **诚实标注**：上表是**定位性/定性**的对比（说明我们把哪一维当主要矛盾），
> **不是**对这些系统的实测结论；对它们的能力判断以各自原文为准（§8.3 外部效度威胁的残余风险之一）。

---

## 3. 问题定义与威胁模型（Problem & Threat Model）

### 3.1 形式化

- **知识断言** $a$：一条可判定的技术陈述（如"对 `signed char` 做 `<<` 溢出是 UB"），
  附带**边界三元组** $\langle$ 输入域 $D$、前提 $P$、失效条件 $F \rangle$。
- **证据** $e$：一次可重放的观测（编译器版本 + 命令 + 优化档 + 输出 + 内容寻址哈希）。
- **判决** $v \in \{\texttt{pass}, \texttt{fail}, \texttt{unknown}, \texttt{contradict}\}$。
- **验证器** $V: (a, E) \mapsto v$；**验证能力** $\mathcal{C}$ = 可用的证据获取手段集合（检测器、编译器、档位、平台）。

**目标不是最大化 $\Pr[v=\texttt{pass}]$，而是最大化"判决与真值的一致率"，同时**不许把 `unknown` 伪装成 `pass`**。
后者是本工作最重要的约束——它把"看起来很好看"和"真的很好"分开。

### 3.2 为什么必须是四态（这是问题定义的一部分，不是实现细节）

`unknown` 是一等公民，因为**"检测器不可用"与"检测器说没问题"是两种完全不同的知识状态**：
- 把 `unknown` 记成 `miss` ⇒ 低估能力，且污染分母；
- 把 `unknown` 记成 `pass` ⇒ **假 pass**，这是最危险的；
- 把 `miss` 记成 `unknown` ⇒ 掩盖真实的能力缺口。

本系统因此规定：**分母 = catch + miss（可测样本）**，`unknown` 单独报告且不计入分母，
`not_error`（本来就不是错误的对照）单独一类。这条口径写进产物（`denominator` 字段），
而不是写在论文正文里（`669_调研消化` A13 的由来）。

### 3.3 十二类威胁（T1–T12）

> 来源：`research/04_threat_model.md`（12 类威胁）。下表给出威胁、现有缓解、残余风险，
> 并在 §3.4 展开**三个重点威胁**。§8 的 Threats to Validity 是本表在论文口径下的重述与量化。

| # | 威胁 | 缓解机制 | 残余风险 |
|---|---|---|---|
| **T1** | **自证威胁**：验证器用自己的工具链证明自己 | 元状态对账器**不依赖内核**（§4.5） | 对账器自身仍需人核；`--check` ≠ 独立实现 |
| **T2** | **自造分布偏差**：变异算子是我们设计的，验证器"熟悉" | 盲 holdout + 外部 corpus（D2/D3）对冲 | 外部样本量小（见 §8.3） |
| **T3** | **holdout 泄漏**：开发期偷看 holdout | reveal **不可逆**；默认不扫 `data/holdout/` | 665 追加的 10 条**无盲态**（见 T9） |
| **T4** | **开发者知情偏差**：写错误的人同时写验证器 | 独立生成（A/B/C 三方） | A/B/C 同进程上下文，**非真正独立** |
| **T5** | **口径漂移**：文档数字与仓库实际不符 | `status_reconciler --check` 对账 | 只覆盖已登记字段 |
| **T6** | **语义 scope 误用**：把"我实验里成立"当"普遍成立" | provenance / semantic scope 强制拆分（§4.4） | 存量卡 semantic scope 完整度 **0/26**（审计实测） |
| **T7** | **度量混淆**：变异得分当缺陷检测率 | 指标分层；变异率**只作自证**（§4.3 L1） | 外部 reader 仍可能误读 |
| **T8** | **选择偏差（预算）**：失败驱动只是因为投入更多 | budget-matched random 对照（§5.2） | **Phase 4 未跑**（§8.3 残余） |
| **T9** | **过拟合到历史缺陷**：D1 是已知已修的缺陷 | 盲态 D2 + 外部 D3 补未知分布 | 扩样样本**无盲态** ⇒ 只能增大分母 |
| **T10** | **复现危机**：环境/版本不可复现 | Merkle 目录根 + 编译器版本落盘 + OTS 锚 | **OTS 是占位**（未上链）；**WSL 依赖未声明**（审计 P0-1） |
| **T11** | **Authority 操纵**：账本被偷偷改 | 452 事件账本**零改红线** | 红线是纪律，非密码学强制 |
| **T12** | **AI 署名不清**：LLM 贡献未登记 | `research/AI_USAGE_LOG.md` + 本稿的 `AI_USAGE_shturl` | 贡献度划分仍是**约定** |

### 3.4 三个重点威胁（本工作的主攻方向）

#### （a）Construct threat：**机器判"执行通过" ≠ "知识正确"**

这是本工作**最主要**的效度威胁。检测器报 `catch` 只意味着"在这条夹具、这个编译档、这个编译器下出现了特定信号"；
它**不**意味着断言 $a$ 成立，也不意味着 $a$ 不成立。反向也一样：`miss` 可能是夹具形态的问题，不是能力问题。

**本系统已观测到的实证**：同一批 ASan 类样本在 `-O1` 下被优化掉整段内存操作（无可观测副作用）⇒ 报不出；
`-O0` 下立刻报出。**666 批把 pipeline 从单档改为 `-O0`+`-O2` 双档后，检出率 66.7% → 87.5%，
而检测器一行代码都没改。**

> 这个事实必须被写进论文，而不是被当成"性能提升"：**变的是口径，不是能力。**
> 两组数字**不可直接比较**，旧值应当作废（§4.7 的口径纪律）。

**缓解**：① 所有检出率必须带 `caliber`（口径）与 `denominator`（分母）字段；
② 编译档/命令/编译器版本随证据落盘；③ 双档都跑，任一档报出即 `catch`；
④ `unknown` 与 `miss` 三态分离且各有对照（C 层 4/4 unknown 是"缺检测器"的对照证据）。
**残余**：跨环境（非本机）复现未验证；**本次审计已证明该残余是真风险**（缺 WSL ⇒ 静默掉分）。

#### （b）Meta-Goodhart：**验证器优化它自己定义的度量**

Goodhart 定律的一阶形态是"指标被优化 ⇒ 指标失效"；**二阶形态（meta-Goodhart）更危险**：
当"验证能力的度量"本身由验证系统产出时，系统可以通过**改口径、改分母、把红灯修绿**来提升分数，
而**没有任何外部参照物能发现**。

本项目的**真实事故**（写进论文，作为 meta-Goodhart 的实例）：
666 批修改了检测器的档位，但**没有重跑生成器**，产物仍停留在旧口径；
论文与前端却写上了新估计值 **81.2%（13/16）**——而这个数字**从未出现在任何产物里**。
更糟的是当时的 `--check` **不比对这两个字段** ⇒ 一路绿。

**缓解（三层）**：
1. **口径变更三步纪律**（R6）：改口径 ⇒ 重跑 ⇒ **作废旧数字**（不是悄悄替换）；
2. **射程自检**（R4）：加了比对字段就必须能被"故意改一个数 ⇒ 变红"验证
   （`tests/test_drift_guard_668.py`，本次审计实测 5/5 变红、0 误报）；
3. **旧数字必须交代下场**：v0.4.1 修订表逐条写明"曾写 / 实测 / 为什么错"。

**残余（审计新发现，必须写进论文）**：现有 `--check` 比的是 **产物 ↔ 前端数字**，
**不重跑探测器** ⇒ 666 那类"改了代码没重跑"的事故形态**今天仍能重演**。审计把它定为 P0-2。

#### （c）Evaluation contamination：**验证器见过被验证的样本**

与 SWE-bench 的 contamination 同源（§1.2 动机一），但在验证系统里有三种具体形态：
1. **样本泄漏**：holdout 在开发期被偷看（T3）；
2. **判据同源**：真值标签与判据按同一标准生成 ⇒ 分数是**上界**而非能力
   （本系统反事实算子 F1=1.0 就是这种：真值按 `external_anchor` 标注，第三判据照同一标准打的分）；
3. **无盲态扩样**：665 追加的 10 个样本是在原 reveal **之后**加入的 ⇒ 无盲态，只能增大分母，
   **不得**据此 Claim 外部效度。

**缓解**：① reveal 不可逆 + 开封事件日志；② 上界声明**写进产物 docstring 与论文**（不是口头声明）；
③ 无盲态样本在工具与论文里都显式标注；④ 分层报告（盲态/非盲态、A/B/C 三层）不得合并。
**残余**：标签效度的**独立复核**（IRR）未做——第二标注者 0 人（§8.3）。

---

## 4. 方法（Method）

### 4.1 系统架构：`atoms → evidence → verdict → ledger`

```
  Book/ (147 章) ──► atoms/ 知识卡 ──► evidence/ 证据卡 ──► verdict 判决 ──► ledger 账本
     断言来源           (42 实卡+10 草稿)     (67 文件)        (四态+provenance)   (452 事件, append-only)
                            ▲                    ▲                  ▲                  ▲
                            │                    │                  │                  │
                     边界三元组           真机编译/运行          67 条规则引擎       零改红线
                     provenance           内容寻址存证          L0/L1 分层          哈希链
```

- **atoms**：知识卡。每条断言带**边界三元组**（输入域/前提/失效条件）。
  缺三元组的卡**不得**预写判决——按 657 规则，四态应为 `unknown`（这是**正确输出**，不是缺陷）。
- **evidence**：证据卡。每次编译/运行落**内容寻址**证据（编译器版本 + 命令 + 档位 + 输出 + sha256）。
  现状：**28** 张卡有 L1 证据、**28** 张双编译器确认、**147** 次真实编译（`compiler_probe_645`）。
- **verdict**：四态判决，由 **67** 条规则引擎产出（两源一致：`gate_engine.RULES` == `data/_gate_rules.json`）。
- **ledger**：权威账本 **452** 事件，append-only，**零改动红线**。

### 4.2 四态判决

| 态 | 含义 | 处置 |
|---|---|---|
| `pass` | 证据支持断言，且边界三元组完备 | 可进入教学台账 |
| `fail` | 证据与断言矛盾 |  counterexample 入教学反例集 |
| `unknown` | **证据不足或检测器不可用** | 不得记为 pass/miss；单独报告 |
| `contradict` | 两条证据互相矛盾（如跨编译器差分） | 升级为人核，机器不裁决 |

**关键设计**：`contradict` 的存在是为了**不让机器在证据冲突时选边**——
冲突本身是信息，选边是人的事（也对应 §8.5 的署名与治理威胁）。

**机器卡一律 `needs_review=true` 且不得混入"已验证卡"计数**；
`verified` **唯人签**（引擎规则把"机器自称已验证"判红）。

### 4.3 门禁分层 L0 / L1

- **L0（阻断层）**：元状态对账、门禁分层合法、真实缺陷检出、盲化 holdout 状态、658 单元测试。
  现状 **7** 个 L0 gate；`run_658_gate` 编排的 5 个阶段**本次审计逐阶段单跑全部 PASS**。
- **L1（建议层）**：变异得分、边界 provenance 报告、供应链完整性。现状 **10** 个 L1 gate。
  L1 红**不阻断**，但必须登记。

> **为什么分层**：把所有东西都设为阻断 ⇒ 人会为了"变绿"而放宽断言（meta-Goodhart 的温床）；
> 全部设为建议 ⇒ 红线失去意义。分层的作用是**把"必须守的"和"可以讨论的"分开**。

### 4.4 provenance 与 semantic scope 的强制拆分

这是本方法学上最"反直觉"但最重要的一条设计：

| 字段 | 回答的问题 | 例子 |
|---|---|---|
| **provenance** | 这条断言**从哪来、谁生成的** | generator 版本、变异集哈希、证据 sha256、编译器版本 |
| **semantic scope** | 这条断言**在什么范围内成立** | 标准条款 / 编译器 / 平台 / 优化档 |

**为什么必须拆**：一条 provenance 完备（谁写的、哪来的都清楚）的断言，
**仍然可能**被误用于它不适用的范围（T6）。把两者写在一起，读者会默认"来源清楚 ⇒ 到处成立"。

**现状（审计实测）**：`boundary_scope_658 --report` 给出
边界卡总数 **26**、provenance 完整 **26/26**、**semantic scope 完整 0/26**。
⇒ **provenance 与 semantic scope 的拆分在机制上已经落地，但语义作用域的回填基本为空**——
这是当前**最大的方法学缺口**之一，直接限制 §8.3 的外部效度（"不知道在哪成立" = 不能 Claim 外部效度）。

### 4.5 元状态对账器（反自证）

**问题**：报告、门禁、指标都由同一套工具链产出 ⇒ 自证闭环（T1）。

**设计**：`status_reconciler_658.py` 是一个**不依赖内核**的独立对账器——
它重新扫描事实源（扫卡面 `claim_structured`、扫 `atoms/` 目录、读 `gate_engine.RULES`），
与 `baseline.json` 与 `_auto/status.json` 对账，**不一致即 `META-STATE-CONFLICT`，exit 1**。

**去写死三原则**（666 A2，对账器自身的实现纪律）：
断言只能写死"口径"，不许写死"测量值"。三条替代路径：
① **事实源对齐**（现算）；② **可加性/划分性**（`block+warn+advice == total`）；
③ **结构不变量**（降序、截断、投影差值）。

> **残余**：对账器"不依赖内核"只意味着它不 import 内核，
> **不意味着它由第三方实现**（`--check` ≠ 独立复现）。这一条在 §8.3 明确承认。

### 4.6 核心机制：失败驱动的验证能力演化闭环

这是本工作与"静态验证器"的根本区别。闭环形式化为：

```
  外部样本集 X（盲 holdout / 外部 corpus / 独立生成）
        │
        ▼
  ① 用当前能力 C_t 测 X  ──►  得到 miss 集合 M_t 与 unknown 集合 U_t
        │
        ▼
  ② 对 M_t ∪ U_t 逐条归因：是"能力缺口"还是"测量配置错"？
        │            （这一问很关键——见 §3.4(a)：双档案例证明大量 miss 是后者）
        ├── 测量配置错 ──► 改配置 + **作废旧数字**（不是能力提升）
        └── 能力缺口   ──► ③ 新增证据获取手段（检测器/档位/平台）⇒ C_{t+1}
        │
        ▼
  ④ 回到**同一批** X 重测 ⇒ 度量 Δ（检出率差值 + CI）
        │
        ▼
  ⑤ 若 Δ 显著 ⇒ 记入演化曲线；若不显著 ⇒ 该能力扩充**不进 Claim 表**
```

**为什么必须回到同一批 X 重测**：否则"能力提升"与"换了一批更简单的样本"无法区分——
这正是 666 那次口径漂移事故的认识论根源。

**为什么必须与 budget-matched random 对照（§5.2）**：
失败驱动看起来有效，可能只是因为它**投入了更多预算**。
同等预算下随机扩充若也能追平，那么"失败驱动"这个机制本身就不成立（ablation F）。

### 4.7 口径纪律（把方法学钉进工程）

- **双档 pipeline**：sanitizer 类检测器**先 `-O0`、再 `-O2`**，任一档报出即 `catch`；两档都不可用才 `unknown`。
- **口径随产物落盘**：`caliber` / `denominator` / `opt_levels` / `env` 写进产物，不写在论文正文里。
- **改口径三步**：改 ⇒ 重跑 ⇒ **作废旧数字**（R6）。
- **射程自检**：新增比对字段必须能被"改一个数必红"验证（R4）。

---

## 5. 评估协议（Evaluation Protocol）

> **本协议在看到结果之前冻结**（667 规划 M1 / A08）。此后任何修改必须记录并说明对已出数字的影响。

### 5.1 数据集五层（D0–D4）

| 层 | 内容 | 用途 | 能否 Claim 外部效度 | 现状 |
|---|---|---|---|---|
| **D0 开发集** | 开发期可见的内部变异样本 | 调参、自证 | ❌ **绝不** | core 变异得分 96.5%（**仅自证**） |
| **D1 历史缺陷** | 已知已修的真实缺陷（重注入） | 真实缺陷召回 | ⚠ 有限（已见过） | 重注入子集 1/1；覆盖登记 12/15 |
| **D2 盲 holdout** | reveal 前不可见的 planted 缺陷 | **盲态召回（主指标）** | ✅ | 30 样本；可测真错 16；**87.5%（14/16）** |
| **D3 外部 corpus** | 来自本仓库之外的真实技术陈述 | **外部召回（主指标）** | ✅ | 40 条；**35.0%（14/40）** 全样本口径 |
| **D4 独立生成** | 独立生成流程产出的断言 | 独立生成召回 | ✅ | 16 张机器卡（`needs_review=true`，**无人签**） |

**分层纪律**：D0 的数**只作自证**，永不进 Claim 表；D2 内部再分**盲态层 / 非盲态层**
（665 追加的 10 条属后者，**只能增大分母**）；D3 再分 A/B/C 三层（按检测器可用性），
**不许合并成一个漂亮数字**。

### 5.2 Baseline（三类，全部 budget-matched）

| Baseline | 定义 | 对齐条件（必须写进产物） |
|---|---|---|
| **B1 静态门禁** | 只跑静态规则（不获取运行时证据） | 同语料、同判定粒度 |
| **B2 静态 + 变异** | 静态规则 + 变异测试（自证层全开） | 同上 + 同变异预算 |
| **B3 budget-matched random** | **同等预算下随机**扩充证据获取（不按失败驱动选） | 同预算（时间/调用次数）、同语料、同档位 |
| （补充）**B4 现成工具** | cppcheck / clang-tidy / sanitizer 组合 | 同上 |

**B3 是最关键的一个**：它把"失败驱动"从"因为投入多所以看起来好"里分离出来（对应 T8 与 ablation F）。
**现状：0 个 baseline 已跑**（667 规划 M3，2027-01）⇒ 这是当前最大的实验缺口。

### 5.3 Ablation（A–F，每组**预写假设**）

| 组 | 去掉/改变什么 | 预写假设 | 主指标 |
|---|---|---|---|
| **A** | Full（全系统） | 基线 | 盲 holdout 召回 + 外部分层召回 |
| **B** | − 变异测试模块 | 内部自证指标消失，**外部召回不变**（验证"变异率 ≠ 检测率"） | 外部召回差值 + CI |
| **C** | − Merkle / 供应链 | 可复算性下降（复现者失败点增多），召回不变 | 复现失败点数 |
| **D** | − 证据获取层（B1 头部层） | 证据完整度下降 ⇒ **`unknown` 比例上升** | `unknown` 比例 |
| **E** | − 边界三元组强制 | 四态退化，`unknown` 被误记为 `pass` ⇒ **假 pass 率上升** | 假 pass 率 |
| **F** | **random-budget 对照** | 若收益主要来自"更多尝试"，则 random-budget 会追平 | 同等预算下的召回率 |

**纪律**：每组先写假设再看结果；**结果与假设不符时原样报告**（不删、不改假设）。
**现状：0 组已跑**（667 规划 M4，2027-02）。

### 5.4 盲态协议

- 冻结日 + **不可逆 reveal** + 开封事件日志；
- reveal 后**永不回盲**；扩样样本若在 reveal 之后加入 ⇒ **无盲态**，标注且只用于增大分母；
- 工具默认**不扫** `data/holdout/`（防泄漏 T3）。

### 5.5 指标（七项）

| 指标 | 定义 | 分母声明 |
|---|---|---|
| 1. 真实缺陷召回 | D1 上被判 `catch` 的比例 | catch+miss |
| 2. **盲 holdout 召回** | D2 盲态层上 `catch` 比例 | catch+miss（`unknown` 不计） |
| 3. **外部召回** | D3 上 `catch` 比例 | 同时报 catch+miss 与全样本两个口径 |
| 4. **FPR（对照误报）** | 对照子集（非缺陷）被判 `catch` 的比例 | 对照样本数（现状 9，误报 1） |
| 5. 变异得分 | D0 上的 kill rate | **仅自证，不得当检测率** |
| 6. 回归保留率 | 演化后旧能力是否退化 | 旧通过样本数 |
| 7. 成本 | 每检出一条真缺陷的时间/调用次数 | 用于 budget 匹配 |

### 5.6 统计口径（冻结，此后不改）

| 场景 | 方法 |
|---|---|
| 单比例 CI | **Clopper–Pearson 精确 95% CI**（主报）；Wilson 作敏感性分析；**禁用小样本 Wald** |
| 独立样本比较 | **Fisher 精确检验 / Boschloo** |
| 同批样本前后比较（演化曲线） | **精确 McNemar** |
| 多重比较 | 探索性 **BH-FDR**；确认性少量比较 **Holm**；检验族**预先定义** |
| 效应量 | 必须报**差值 + CI**，不能只报 p |
| 聚类相关 | 先数 source clusters、估 ICC/DEFF/n_eff；必要时聚合到源文件（**40 张同源卡 ≠ 40 个独立观测**） |
| IRR | 两人 Cohen's κ；多人/缺失 Krippendorff's α；**α ≥ 0.67** 才作 tentative 结论 |

**红线（写进论文，不违反）**：
不声称"显著优化"；不把 0/8 写"无效"（写 `0/8 (95% CI 0–36.9%)`）；
不把 6/6 裸写 100%；**不把变异 kill rate 称检测率**；
**不把同源判据下的 F1=1.0 称"已校准"**。

### 5.7 复算入口（现状）

| 命令 | 作用 |
|---|---|
| `python tools/holdout_reveal_3_665.py` | D2 盲 holdout 检出率 + 逐样本明细 + 环境（**需 WSL**） |
| `python tools/external_corpus_reveal_665.py` | D3 外部 corpus + 分母声明（**需 WSL**） |
| `python tools/counterfactual_extend_665.py` | 反事实算子 P/R/F1 + 分母 + 上界声明 |
| `python tools/web_metrics_666.py --check` | 三个率的漂移比对（**只比产物↔前端**，见 §3.4(b) 残余） |
| `python tools/status_reconciler_658.py --check` | 元状态对账（T1） |
| `python tools/merkle_integrity.py --check` | 供应链 5 目录根核验 |
| `python tools/run_658_gate.py` | L0 门禁编排（会写 `data/`） |

---

## 6. 实验（Experiments）

> **本章所有数字均为占位符**，等 669 批次实验填入。**不填任何未经产物落盘的值。**
> 每个占位符都注明：**需要什么数据 / 由哪条命令产生 / 用哪个统计口径**。

### 6.1 E1 · 主实验：静态门禁 vs 失败驱动

**研究问题**：在 D2/D3 上，失败驱动的证据获取是否显著优于静态门禁？

| 系统 | 盲 holdout 召回 (k/n, CP 95% CI) | 外部召回 (k/n, CP 95% CI) | 对照 FPR (k/n) | 成本（秒/条） |
|---|---|---|---|---|
| B1 静态门禁 | `{{TODO_669: k/n + CP CI}}` | `{{TODO_669: k/n + CP CI}}` | `{{TODO_669: k/n}}` | `{{TODO_669}}` |
| B2 静态 + 变异 | `{{TODO_669}}` | `{{TODO_669}}` | `{{TODO_669}}` | `{{TODO_669}}` |
| **Full（失败驱动）** | `{{TODO_669}}` | `{{TODO_669}}` | `{{TODO_669}}` | `{{TODO_669}}` |
| **差值（Full − B1）+ CI** | `{{TODO_669: 差值 + 95% CI；检验 = Fisher/Boschloo}}` | `{{TODO_669}}` | — | — |

- **需要什么数据**：`tools/baseline_*.py`（A03，尚未建）在 D2（30）+ D3（40）上的**逐样本原始输出**；
  Full 侧已有 D2/D3 产物，但需要**同一口径重跑**以对齐。
- **统计口径**：差值 + CI（§5.6）；多重比较 3 组用 Holm。
- **⚠ 前置条件**：必须先完成审计 P0-1（环境声明）与 P0-2（真机重跑比对），
  否则基线侧与 Full 侧可能跑在不同环境里，实验不可解释。

### 6.2 E2 · Ablation：Full vs −失败驱动 vs random-budget

**研究问题**：Full 的收益有多少来自"失败驱动的选择"，有多少只是"预算更多"？

| 组 | 盲 holdout 召回 | 外部召回 | `unknown` 比例 | 假 pass 率 | 复现失败点 |
|---|---|---|---|---|---|
| A Full | `{{TODO_669}}` | `{{TODO_669}}` | `{{TODO_669}}` | `{{TODO_669}}` | `{{TODO_669}}` |
| B −变异 | `{{TODO_669}}` | `{{TODO_669}}` | `{{TODO_669}}` | `{{TODO_669}}` | — |
| C −Merkle | `{{TODO_669}}` | `{{TODO_669}}` | — | — | `{{TODO_669}}` |
| D −证据获取层 | `{{TODO_669}}` | `{{TODO_669}}` | `{{TODO_669}}`（假设：上升） | — | — |
| E −边界强制 | `{{TODO_669}}` | `{{TODO_669}}` | — | `{{TODO_669}}`（假设：上升） | — |
| **F random-budget** | `{{TODO_669: 与 A 同预算}}` | `{{TODO_669}}` | — | — | — |
| **A − F（差值 + CI）** | `{{TODO_669: 这是本文最关键的一个数}}` | `{{TODO_669}}` | — | — | — |

- **需要什么数据**：A–F 六组各跑一遍 D2/D3；预算对齐证明（同语料/同档/同粒度/同时间预算）。
- **统计口径**：A−F 是**同批样本上的配对比较** ⇒ 用**精确 McNemar**；其余跨组用 Fisher/Boschloo；BH 校正。
- **判读规则（预写）**：若 A−F 差值 CI 跨 0 ⇒ **"失败驱动"这个机制不成立**，必须原样报告（不删假设 B/F）。

### 6.3 E3 · 演化曲线：迭代次数 → 检出率

**研究问题**：验证能力随迭代是否真的在提升？（这是"验证能力演化"主张的直接证据）

| 迭代 t | 新增能力 | 同一批 X 上的召回 (k/n, CP CI) | Δ vs t−1（McNemar） | 回归保留率 |
|---|---|---|---|---|
| t=0（基线） | — | `{{TODO_669}}` | — | — |
| t=1 | `{{TODO_669: 例：双档 pipeline}}` | `{{TODO_669}}` | `{{TODO_669}}` | `{{TODO_669}}` |
| t=2 | `{{TODO_669}}` | `{{TODO_669}}` | `{{TODO_669}}` | `{{TODO_669}}` |
| … | … | … | … | … |

- **⚠ 口径红线**：表中每一行的 X **必须是同一批样本**。
  已发生的反面教材必须写进图注：**66.7% → 87.5% 不是演化，是口径变更**（检测器零改动），
  因此它**不得**作为演化曲线的一个点。
- **需要什么数据**：每个能力扩充点的"重测同一批 X"产物（当前**只有一个点**：668 的双档重测）。
- **诚实预判**：在只有一个能力扩充点被记录的情况下，本图的说服力有限；
  若 669 只补到 t=1，则论文应把主张降级为"**单次能力扩充的可度量性**"而非"演化趋势"。

### 6.4 现有（非占位）数字一览（供 §7/§8 引用）

| 量 | 值 | 复算命令 | Claim 档 |
|---|---|---|---|
| 判决规则 | 67（block 0 / warn 176 / advice 55） | `len(gate_engine.RULES)` | 能支撑 |
| 实卡 / 草稿 | 42 / 10 | `tools/counts_659.py` | 能支撑 |
| D2 盲 holdout 召回 | **87.5%（14/16）**，miss 2（h5/h29），unknown 1 | `holdout_reveal_3_665.py` | 能支撑（**但本环境不可复现，见审计 A1**） |
| D2 对照 FPR | 1/9 | 同上 | 能支撑（n=9，CI 极宽，**只能点估计**） |
| D3 外部召回 | 全样本 **35.0%（14/40）**；可测口径 43.8%（14/32）；A 54.2% / B 12.5% / C 0%(4/4 unknown) | `external_corpus_reveal_665.py` | **不可复现**（审计 A3：缺 WSL 重跑得 10.0%） |
| 反事实算子 | P=R=F1=**1.0**，分母 10，tp2/fp0/tn8/fn0 | `counterfactual_extend_665.py` | 能支撑（**上界，非校准**） |
| 编译证据 | 28 卡 L1 / 28 双编译器 / 147 次编译 | `compiler_probe_645.py --limit N` | 能支撑 |
| 内部变异（自证） | core 96.5% / all 81.8% | — | **不得当检测率** |
| 权威账本 | 452 事件，零改 | `wc -l data/646_authority_rule_annotation.jsonl` | 能支撑 |
| 供应链 | Merkle 5 目录（atoms 54 / evidence 67 / Examples 1571 / Book 183 / mutation_baselines） | `merkle_integrity.py --check` | 能支撑 |
| OTS | **占位**（无 attestation），锚已过期 | `ots_anchor_613.py --check` → exit 1 | **不能支撑"已上链"** |

---

## 7. 分析（Analysis）

### 7.1 错误类型分析：哪类错误检不出

沿用 D3 的三层划分（按**检测器可用性**，不是按难度），并把 `miss` 与 `unknown` 分开看：

| 层 | 含义 | 现状（可测口径） | 解释 |
|---|---|---|---|
| **A 本地可跑**（asan/ubsan/tsan/compiler-warn/wunsequenced） | 本机有检测器 | **`{{TODO_669: A 层 k/n + CP CI}}`**（668 产物值 54.2%，24 可测；**审计重跑为 30.0%，10 可测 ⇒ 该值环境依赖**） | 能力上限区 |
| **B 跨编译器 / 测量类** | 需差分或测量 | **`{{TODO_669: k/n + CI}}`**（668：12.5%，8 可测） | **几乎抓不到** ⇒ 缺"跨编译器差分"这一维能力 |
| **C 无本地检测器** | 本机根本没有手段 | **0/4 全 unknown**（95% CI 0–36.9%） | **这是"缺检测器"假说的对照证据，不是失败** |

**核心判断**：C 层 4/4 全 `unknown` 与 B 层 12.5% 一起指向同一个结论——
**当前能力的主要缺口不在"检测器不够聪明"，而在"证据获取的维度不够"**（跨编译器、跨平台、跨档位、测量类）。
这正好说明 §4.6 的"失败驱动 → 新增证据获取手段（而不是加深 detector）"为什么是正确的主要矛盾。

**诚实边界**：A/B/C 三层是**按检测器可用性**分的，不是按"错误难度"分的；
因此**不能**用它断言"难的错误检不出"。这个混淆是 §8.1 construct 威胁的一部分。

### 7.2 成本—收益分析

| 项 | 现状 | 需要的数据 |
|---|---|---|
| 单卡生产成本 | 约 1.5–2 h（选题 15min + 夹具/证据 30–60min + 边界 20min + 校验 15min） | 667 规划 §3.3 估算 |
| 每检出一条真缺陷的成本 | `{{TODO_669: 总机时 / catch 数}}` | A03 baseline 跑完后可算 |
| 失败驱动 vs random 的成本效率比 | `{{TODO_669: ablation F 的预算对齐证明}}` | 同上 |
| 演化一轮的边际收益 | `{{TODO_669: E3 的 Δ/迭代}}` | E3 |

**判读规则**：若"失败驱动"的每检出成本**高于** budget-matched random，
即使召回更高，也应把主张降级为"**在预算不受限时更准**"。

### 7.3 失败案例研究（至少 3 个 miss 的深度分析）

> **纪律**：每个案例必须回答四个问题——① 真值是什么、判据是什么；
> ② 为什么没检出（能力缺口 or 测量配置错）；③ 修复属于哪一类（改配置 / 加能力 / 承认缺口）；
> ④ **修复后是否回到同一批样本重测**（否则不算演化）。

**案例 1 · h5（D2 盲 holdout，两档都不报）**
- 真值 / 判据：`planted=true`；`{{TODO_669: 该样本的详细归因，来源 data/holdout/reveal_3_detail_668.json}}`
- 为什么没检出：`{{TODO_669: 是夹具形态问题还是检测器能力问题？}}`
- 归属判定：`{{TODO_669}}`｜修复后重测：`{{TODO_669}}`

**案例 2 · h29（D2 盲 holdout，两档都不报）**
- 同四问：`{{TODO_669}}`

**案例 3 · D3 外部 corpus B 层（跨编译器/测量类，12.5%）**
- 真值 / 判据：外部来源，类别级出处（`verified_source` 有 false 项 ⇒ **未本机验证**）
- 为什么没检出：**缺"跨编译器差分"这一维能力**（不是检测器不聪明）⇒ 指向 §7.1 的核心判断
- 归属判定：**能力缺口** ⇒ 应触发 §4.6 闭环的 ③
- 修复后重测：`{{TODO_669}}`

**案例 4（对照）· 假 pass 风险**
- 需要 E 组 ablation（−边界三元组强制）实测才能量化；当前**无数据**。
- **诚实登记**：在 ablation E 未跑之前，**"假 pass 率"是一个未被度量的风险**，不得声称"不存在假 pass"。

---

## 8. Threats to Validity

> 五层：**construct / internal / external / statistical / temporal**。
> 每层写：威胁 → 缓解 → **残余风险**（残余风险不许省略）。

### 8.1 Construct validity（我们在测的东西，是不是我们以为在测的）

- **威胁（主威胁）**：检测器报 `catch` 只代表"特定夹具 + 特定编译档 + 特定编译器下出现特定信号"，
  **不等于断言为真**。反向同理。实证：双档改动使检出率 66.7% → 87.5% 而检测器零改动。
  次生威胁：**A/B/C 三层是按检测器可用性分的，不是按难度分的**，容易被误读为"难的错误检不出"。
- **缓解**：`caliber` / `denominator` / `opt_levels` / `env` 全部随产物落盘；双档都跑；
  三态分离（catch/miss/unknown/not_error）；口径变更**作废旧数字**而不是替换。
- **残余**：① 跨环境复现未验证——**本次审计已将其从"残余"升级为"已发生的失败"**
  （缺 WSL ⇒ external 从 35.0% 掉到 10.0%，护栏仍绿）；② 标签效度的独立复核未做（第二标注者 0 人）。

### 8.2 Internal validity（因果）

- **威胁**：① **meta-Goodhart**（§3.4(b)）——系统可通过改口径/改分母/把红灯修绿来提升分数；
  ② **选择偏差（预算）**——失败驱动看起来有效只是因为它投入更多（T8）；
  ③ **改代码没重跑**——产物停在旧口径而文档写新值（666 的 81.2% 事故）。
- **缓解**：口径三步纪律（R6）；射程自检（R4，本次审计实测 5/5 变红）；
  budget-matched random 对照（ablation F）；元状态对账器不依赖内核。
- **残余**：① **护栏只比"产物 ↔ 前端"，不重跑探测器** ⇒ 666 事故形态仍可重演（审计 P0-2，未修）；
  ② ablation A–F **一组都没跑**，因果主张目前**无对照支撑**。

### 8.3 External validity（能不能推广）

- **威胁**：① 样本量小——D2 可测真错 16、D3 全样本 40、对照 9 ⇒ **全是点估计**
  （n=30 时 CI 宽约 ±37pp；要 ±10pp 需 n≈93–104）；
  ② **选择偏差**——卡来自本项目自己的语料（同源），40 张同源卡 ≠ 40 个独立观测（需 ICC/DEFF 修正）；
  ③ **semantic scope 回填为空（0/26）** ⇒ "在哪个范围成立"基本未知，**推广缺乏边界**；
  ④ 领域单一（C++）。
- **缓解**：分层报告（盲态/非盲态、A/B/C），不合并成一个数；明示"两轮样本集不同故不可比"；
  无盲态样本只用于增大分母；聚类相关处理纳入统计计划（§5.6）。
- **残余**：① **baseline 0 个、ablation 0 组** ⇒ 无法回答"比别的方法好在哪"；
  ② **对账器仍是我们自己实现的**（`--check` ≠ 第三方独立实现）；
  ③ **第三方复现者 0 人**（M6 硬节点未到）；④ semantic scope 0/26。

### 8.4 Statistical validity

- **威胁**：多重比较（3 baseline + 6 ablation + 3 层）；小样本下 Wald 区间严重失效；
  聚类相关导致 CI 过窄；**只报 p 不报效应量**。
- **缓解**：统计计划**先冻结**（§5.6）；主报 Clopper–Pearson、Wilson 作敏感性；
  Fisher/Boschloo + 精确 McNemar；BH（探索性）/ Holm（确认性）；**必须报差值 + CI**。
- **残余**：① `tools/stats_667.py` **尚未建成**（667 规划 M1，2026-11）⇒ 上述口径目前**未工具化**，
  存在"人工挑口径"的空间；② 现有数字（87.5% / 35.0% / F1=1.0）**均无 CI**
  （n=16 时 95% CI 约 61.7–98.4%；n=40 全样本 35.0% 约 20.6–51.7%——**这些区间必须补上**）；
  ③ IRR 未做（α 未知）。

### 8.5 Temporal validity（时间维度：会不会随时间失效）

- **威胁**：① **OTS 锚过期**——当前 `.ots` 是零 attestation 占位符，未提交日历，无比特币区块证明
  （本次审计实测 `ots_anchor_613 --check` exit=1，摘要不一致）⇒ **"该台账在某时刻已存在"这件事没有被证明**；
  ② **样本老化**——外部 corpus 一旦公开就可能被后续模型记忆（与 SWE-bench 同源问题）；
  ③ **环境漂移**——编译器版本、sanitizer 可用性、OS 行为随时间变化（TSan 在 WSL 高熵 ASLR 下间歇性无法初始化，
  本项目已用 `setarch -R` 关 ASLR 处理，但**这是环境修补，不是可移植的解法**）。
- **缓解**：Merkle 目录根 + 透明日志（哈希链）；编译器版本与命令随证据落盘；
  真实历史凭证已归档至 `data/supply_chain/ots_archive/`；扩样与封存计划（M5）。
- **残余**：① **OTS 真锚定未做**（需人 + 网络执行 `ots stamp`）；
  ② **Merkle 每次重钉都会使锚失效** ⇒ 在真锚定之前，"不可篡改"只剩**内容哈希一致**这一半（B3 PASS / B4 FAIL）；
  ③ **WSL 硬依赖未声明** ⇒ 时间推移中换机器即复现失败（审计 P0-1）。

### 8.6 本稿残余风险 ↔ 669d 门禁映射（可审计化）

> 669d 批次把上述残余风险中"可机械判定的"固化成 6 条门禁（B1–B6，见 `tools/gate_tiers_669d.json`）；
> 不可机械判定的以 `data/669d_known_gaps.json` 诚实登记（共 19 条：G-STATS-FROZEN 3、G-BOUNDARY-REQUIRED 15、G-BASELINE-EXISTS 1），不静默。
> 门禁判据一律**现算**（禁止从产物抄数），详见 `tools/gate_rules_669d.py` 与 `tools/run_669d_gate.py`。

| 威胁层 | 本稿残余风险（节） | 对应 669d 门禁 | 登记状态 |
|---|---|---|---|
| Construct | 跨环境复现未验证（WSL 缺位 ⇒ external 35.0%→10.0%，护栏仍绿） | G-BOUNDARY-REQUIRED（env 边界） | 已知缺口 ×15 |
| Construct | 标签效度独立复核未做（第二标注者 0 人） | G-IRR（L1，WARN 不 BLOCK） | 残余（待补第二标注者） |
| Internal | 护栏只比产物↔前端，不重跑探测器（666 事故形态可重演） | G-RATE-CONSISTENCY | 未自动登记 ⇒ 建议补登 known_gap（审计 P0-2） |
| Internal | ablation A–F 0 组，因果无对照 | G-BASELINE-EXISTS（L0） | 已知缺口 ×1 |
| Statistical | `stats_667.py` 未建成，口径未工具化 | G-STATS-FROZEN（L0） | 已知缺口 ×3 |
| Statistical | 现有三数（87.5% / 35.0% / F1=1.0）无 CI | G-DENOMINATOR + G-STATS-FROZEN | 附录 A 待补 CI |
| External | baseline 0 个、ablation 0 组 ⇒ 无法比别的方法 | G-BASELINE-EXISTS | 已知缺口 ×1 |
| External | 对账器仍为本方实现（`--check` ≠ 第三方） | —（第三方独立实现未做） | 残余 |
| External | semantic scope 0/26，"在哪成立"未知 | G-BOUNDARY-REQUIRED | 已知缺口 ×15 |
| Temporal | OTS 真锚定未做（零 attestation 占位） | —（Merkle/OTS 计划 M5） | 附录 A 待消项 |
| Temporal | WSL 硬依赖未声明 ⇒ 换机器即复现失败 | G-BOUNDARY-REQUIRED | 已知缺口 ×15 |

**说明**：① 上表只覆盖"可审计化"的残余项；construct/internal 中涉及**人为判断**的部分（如定位性对比是否误导读者）不在门禁射程内，靠同行评审与作者自律。② G-IRR 为 L1 ADVISORY，当前 0 条 IRR 记录只 WARN 不 BLOCK，符合"先登记、不假绿"原则。③ 所有门禁的"通过"都依赖 `data/669d_known_gaps.json` 中**已登记**的缺口；任何**新出现**的未登记问题一律不得豁免（见 `tools/gate_tiers_669d.json` 的 invariants）。

---

## 9. 结论（Conclusion）

LLM 让技术知识的**生成**成本趋近于零，但**验证**成本没有变。
本文主张：验证问题不能靠"用模型评模型"（共享失效域）或"检测文本是否 AI 生成"（答错问题）来解决，
而必须把**判决—证据—复算**绑成一条**可被外部打断**的链。

阙疑把这件事拆成四个可验收的机制：**四态判决**（`unknown` 是一等公民，不许假 pass）、
**provenance 与 semantic scope 强制拆分**（来源清楚 ≠ 到处成立）、
**不依赖内核的元状态对账器**（反自证）、以及**失败驱动的验证能力演化闭环**
（外部样本漏检 ⇒ 新增证据获取能力 ⇒ 回到同一批样本重测）。

我们也把**自己的失败**写成了方法的一部分：66.7% → 87.5% 不是能力提升而是口径变更，旧值必须作废；
81.2% 从未出现在任何产物里，"改了代码没重跑"必须被护栏抓住（而它**今天还没被抓住**）。
本次同步完成的第三方只读审计给出总体可信度 **6/10**：基础设施可信，**数字脆弱**。

**下一步（按优先级）**：① 补环境声明与真机重跑比对（审计 P0-1/P0-2）；
② 建 4 个 budget-matched baseline 并跑 A–F ablation（论文 T2 的硬门槛）；
③ 把现有三个数字全部补上 Clopper–Pearson CI；④ 找到第 1 名无上下文复现者（M6 硬节点）。

> **本稿的立场**：在 baseline 与 ablation 跑完之前，本文**不**主张"我们的方法比别的好"。
> 我们主张的是：**这套机制让"好不好"变成一个可以被外部度量、被第三方打断、被自己否证的问题。**

---

## 参考文献

> 标注约定：**[API 核验]** = 本批次通过 arXiv API 当场核对过标题/作者/日期/venue；
> **[待核]** = 出自作者知识，ID 或卷期未经本次当场核验，**投稿前须人工逐条核**。

1. [API 核验] Jimenez, C. E., Yang, J., Wettig, A., et al. **SWE-bench: Can Language Models Resolve Real-World GitHub Issues?** ICLR 2024. arXiv:2310.06770.
2. [API 核验] Liang, S., Garg, S., Zilouchian Moghaddam, R. **The SWE-Bench Illusion: When State-of-the-Art LLMs Remember Instead of Reason.** arXiv:2506.12286 (2025-06-14).
3. [API 核验] Prathifkumar, T., Mathews, N. S., Nagappan, M. **Does SWE-Bench-Verified Test Agent Ability or Model Memory?** arXiv:2512.10218 (2025-12-11).
4. [API 核验] Adamenko, P., Ivanov, M., Valeev, A., et al. **SWE-MERA: A Dynamic Benchmark for Agenticly Evaluating LLMs on Software Engineering Tasks.** EMNLP 2025 (Demos). arXiv:2507.11059. DOI 10.18653/v1/2025.emnlp-demos.30.（文中引用的 "32.67% 解法泄漏 / 31.08% 测试不充分" 出自其摘要对 SWE-bench 的统计）
5. [API 核验] Mitchell, E., Lee, Y., Khazatsky, A., et al. **DetectGPT: Zero-Shot Machine-Generated Text Detection using Probability Curvature.** ICML 2023. arXiv:2301.11305.
6. [API 核验] Kirchenbauer, J., Geiping, J., Wen, Y., Katz, J., Miers, I., Goldstein, T. **A Watermark for Large Language Models.** ICML 2023. arXiv:2301.10226.
7. [API 核验] Sadasivan, V. S., Kumar, A., Balasubramanian, S., et al. **Can AI-Generated Text be Reliably Detected?** TMLR. arXiv:2303.11156.
8. [待核] **Regulation (EU) 2024/1689 of the European Parliament and of the Council（欧盟《人工智能法》）**, OJ L 2024/1689, 12.7.2024；第 50 条（生成式 AI 输出透明度义务）。
9. [API 核验] Wang, S., Long, Z., Fan, Z., Wei, Z., Huang, X. **Benchmark Self-Evolving: A Multi-Agent Framework for Dynamic LLM Evaluation.** COLING 2025. arXiv:2402.11443.
10. [API 核验] Liu, Q., Dineen, J., Huang, Y., Zhang, S., Poon, H., Zhou, B., Chen, M. **ArenaBencher: Automatic Benchmark Evolution via Multi-Model Competitive Evaluation.** arXiv:2510.08569 (2025-10-09).
11. [API 核验] Zhang, L., He, S., Zhang, C., et al. **SWE-bench Goes Live!** arXiv:2505.23419 (2025-05-29).
12. [API 核验] Kiela, D., Bartolo, M., Nie, Y., et al. **Dynabench: Rethinking Benchmarking in NLP.** NAACL 2021. arXiv:2104.14337.
13. [API 核验] White, C., Dooley, S., Roberts, M., et al. **LiveBench: A Challenging, Contamination-Limited LLM Benchmark.** ICLR 2025 Spotlight. arXiv:2406.19314.
14. [API 核验] Foster, C., Gulati, A., Harman, M., Harper, I., Mao, K., Ritchey, J., Robert, H., Sengupta, S. **Mutation-Guided LLM-based Test Generation at Meta**（ACH，Automated Compliance Hardening）. arXiv:2501.12862 (2025-01-22)，FSE 2025 主题报告。
15. [API 核验] Wang, G., Xu, Q., Briand, L., Liu, K. **Mutation-Guided Unit Test Generation with a Large Language Model**（MUTGEN）. IEEE TSE. arXiv:2506.02954. DOI 10.1109/TSE.2026.3682975.
16. [API 核验] Liu, J., Lee, S., Losiouk, E., Böhme, M. **Evaluating LLM-Based Regression Test Generation**（Cleverest）. PACMSE 3(FSE). arXiv:2501.11086. DOI 10.1145/3808129.
17. [API 核验] Zheng, L., Chiang, W.-L., Sheng, Y., et al. **Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.** NeurIPS 2023 Datasets & Benchmarks. arXiv:2306.05685.
18. [待核] Klein, G., Elphinstone, K., Heiser, G., et al. **seL4: Formal Verification of an OS Kernel.** SOSP 2009；Communications of the ACM 53(6), 2010.
19. [待核] Leroy, X. **Formal Verification of a Realistic Compiler**（CompCert）. Communications of the ACM 52(7), 2009.
20. [待核] Jia, Y., Harman, M. **An Analysis and Survey of the Development of Mutation Testing.** IEEE Transactions on Software Engineering 37(5), 2011.
21. [待核] Goodhart, C. A. E. **Problems of Monetary Management: The U.K. Experience.** 1975；Strathern, M. **"Improving ratings": audit in the British university system.** European Review 5(3), 1997.（"当一项指标成为目标，它就不再是好指标"的常见出处）
22. [API 核验] Skalse, J., Howe, N. H. R., Krasheninnikov, D., Krueger, D. **Defining and Characterizing Reward Hacking.** arXiv:2209.13085 (2022-09-27).
23. [API 核验] Gao, L., Schulman, J., Hilton, J. **Scaling Laws for Reward Model Overoptimization.** ICML 2023. arXiv:2210.10760.
24. [API 核验] Gebru, T., Morgenstern, J., Vecchione, B., et al. **Datasheets for Datasets.** CACM 64(12), 2021. arXiv:1803.09010.
25. [API 核验] Mitchell, M., Wu, S., Zaldivar, A., et al. **Model Cards for Model Reporting.** FAT\* 2019. arXiv:1810.03993. DOI 10.1145/3287560.3287596.
26. [待核] Pineau, J., Vincent-Lamarre, P., Sinha, K., et al. **Improving Reproducibility in Machine Learning Research（NeurIPS 2019 可复现性项目报告）. ** JMLR 22(164), 2021.
27. [待核] Clopper, C. J., Pearson, E. S. **The use of confidence or fiducial limits illustrated in the case of the binomial.** Biometrika 26(4), 1934.
28. [待核] Fisher, R. A. **The Design of Experiments**（精确检验的 tea-tasting 实验）. 1935；亦见 JRSS 98, 1935.
29. [待核] McNemar, Q. **Note on the sampling error of the difference between correlated proportions or percentages.** Psychometrika 12(2), 1947.
30. [待核] Benjamini, Y., Hochberg, Y. **Controlling the false discovery rate.** Journal of the Royal Statistical Society B 57(1), 1995.
31. [待核] Holm, S. **A simple sequentially rejective multiple test procedure.** Scandinavian Journal of Statistics 6(2), 1979.
32. [待核] Cohen, J. **A coefficient of agreement for nominal scales.** Educational and Psychological Measurement 20(1), 1960；Krippendorff, K. **Content Analysis: An Introduction to Its Methodology**, 1980（α 系数）.
33. [待核] Shadish, W. R., Cook, T. D., Campbell, D. T. **Experimental and Quasi-Experimental Designs for Generalized Causal Inference.** 2002.（construct validity 术语来源）
34. [API 核验] Chen, M., Tworek, J., Jun, H., et al. **Evaluating Large Language Models Trained on Code**（HumanEval）. arXiv:2107.03374.
35. [待核] Merkle, R. C. **A Digital Signature Based on a Conventional Encryption Function.** CRYPTO '87 / LNCS 293, 1988.（Merkle 树）
36. [待核] **OpenTimestamps**（OTS）协议与日历服务——本系统用于台账时间锚定的外部依赖（当前为占位状态，见 §8.5）。
37. [API 核验] Liao, C., Xu, H., Zhou, X., Zhang, Y., Sun, C. **LLVM Translation Validation Automated with Large Language Models and Lean.** arXiv:2609.19583 (2026-09-17).
38. [API 核验] Shefer, A., Engel, I., Alekseev, S., Berezun, D., Verbitskaia, E., Podkopaev, A. **Can LLMs Enable Verification in Mainstream Programming?** arXiv:2503.14183 (2025-03-18).
39. [API 核验] Poesia, G., Henniger, S., Hsu, T.-H., Du, Y., Amin, N. **Formal Disco: Scalable Open-Ended Generation of Formally Verified Programs.** arXiv:2607.04631 (2026-07-06).
40. [API 核验] Banik, D., Chowdhury, K., Shamim, S. I. **All Smoke, No Alarm: Oracle Signals in Agent-Authored Test Code.** arXiv:2606.18168 (2026-06-16).
41. [API 核验] Lian, X., Wang, S., Ma, J., Liu, F., Tan, X., Zhang, L., Shi, L., Gao, C. **Uncovering Weaknesses in Neural Code Generation.** arXiv:2407.09793 (2024-07-13).
42. [API 核验] Lyu, W., Wang, Y., Sun, Y., Zhang, Y. **Will Your Next Pair Programming Partner Be Human? An Empirical Evaluation of Generative AI as a Collaborative Teammate in a Semester-Long Classroom Setting.** arXiv:2505.08119 (2025-05-12).
43. [API 核验] Kao, L. **Constant-Size Cryptographic Evidence Structures for Regulated AI Workflows.** arXiv:2511.17118 (2025-11-21).
44. [API 核验] Wang, Z. **Who Audits the Auditor? Tamper-Proof Fraud Detection with Blockchain-Anchored Explainable ML.** arXiv:2604.22096 (2026-04-23).
45. [API 核验] Wu, Y., Ajmani, L., Longpre, S., Li, H. **A Systematic Review of NeurIPS Dataset Management Practices.** arXiv:2411.00266 (2024-10-31).

---

## 附录 A · 占位符清单（投稿前必须全部消项）

| 占位符 | 所在节 | 需要什么 |
|---|---|---|
| E1 全表（4 行 × 4 列） | §6.1 | 4 个 baseline 的 D2/D3 逐样本输出（A03）+ 预算对齐证明 |
| E2 全表（6 组 × 5 列） | §6.2 | ablation A–F（A04）+ 每组预写假设的落地记录 |
| E3 演化曲线（t≥2） | §6.3 | 每个能力扩充点对**同一批 X** 的重测产物 |
| A/B/C 三层 CI | §7.1 | `stats_667.py` 建成后对现有 k/n 现算（A08/A15） |
| 成本—收益 4 项 | §7.2 | 机时记录 + baseline 预算数据 |
| 失败案例 1/2 的归因 | §7.3 | `data/holdout/reveal_3_detail_668.json` 的 h5/h29 逐条人工归因 |
| 现有三数的 CI | §6.4 | 同上（87.5% / 35.0% / F1=1.0） |

## 附录 B · 本稿的 AI 使用声明（摘要）

本稿由 LLM（CodeBuddy / DeepSeek 系列）**辅助起草**，人类作者负责选题、结构、claim 边界与最终裁决。
**逐条登记见 `research/AI_USAGE_shturl`**，包括：用途、是否影响结论、影响面、人工验证方式、残留风险。
凡未经登记的 AI 贡献，按本项目纪律视为未声明作者。
