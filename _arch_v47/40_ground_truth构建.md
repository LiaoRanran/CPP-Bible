# 方向 40：ground truth 构建（金标准如何为"知识断言真伪"构造可信锚点）

> 研究对象：**阙疑 / queyi**——C++ 知识验证系统，判定"C++ 知识断言 / 知识卡"是否成立。本方向聚焦一个问题：当我们说某条知识卡"真 / 假 / 存疑"时，这个标签（ground truth）从哪来、凭什么可信、怎么评估其质量、又如何与"软标签 vs 硬标签"的学术争论对接。所有讨论最终落回阙疑已实测的两个锚点：**真实缺陷夹具 15**（重注入 6/6=100%、历史覆盖 12/15=80%）与**盲 holdout 30**（真错 17，检出 66.7%）。

---

## 核心结论

1. **金标准不是只有"专家标注"一种来源，程序化 / 构造式来源（known-answer test、差分测试、变异注入）才是可复算、可独立验证的硬锚点。** Yang et al.（PLDI 2011）用 Csmith 做差分测试，在**三年**内于 GCC、LLVM 等主流 C 编译器中报告了 **"more than 325 previously unknown bugs"**，且全程**不需要预言机（oracle）**——仅靠"同一程序多编译器输出比对"即可判定错误。阙疑的"真实缺陷夹具 15"本质就是这一路线在"C++ 知识断言"上的等价物：标签由构造过程本身保证为真，而非由人拍板。

2. **一致性 ≠ 质量；高标注者一致度可能恰好掩盖系统性偏差。** tianpan.co（2026-04-17）直言 *"High Agreement Is Not the Same as High Quality"*，并指出 Cohen's kappa 在不平衡类别上会虚高；Bhardwaj et al.（NeurIPS 数据策展评估，arXiv:2410.22473）发现 2021–2023 年 60 个数据集中**情境意识（context awareness）通过率为 0%、环境足迹为 0%**，且最低标准通过率中位数从 78%→67%→61% 逐年下滑。阙疑必须把金标准本身变成**可审计对象**（append-only 哈希链 + Merkle checkpoint + 不依赖内核的独立对账器），而不是去"信任专家判断"。

3. **"软标签"比"硬标签"更能承载知识断言的"不确定边界"，而阙疑的四态判决天然是软标签结构。** Pavlovic, Paun, Poesio（2026，arXiv:2605.18648）在 MNIST / Mukhoti 上证明：人类软标签训练的模型 KLD 校准误差 **0.669**，显著优于多数投票硬标签的 **1.661**（越低越好），且能映射人类不确定性（Spearman 相关 −0.70）。阙疑应把"真对 / 真错 / 存疑 / 未定"显式建模为软标签概率，而非硬 0/1，并把"存疑"态的置信区间写进 gold ledger。

---

## 精确数字与案例

### 一、金标准的四种来源：专家标注 / 交叉验证 / 程序化构造 / 已知缺陷夹具

ground truth 的构造来源直接影响"可信度上限"。下表按来源类型归纳其机制、可信度性质与阙疑对应物。

| 来源类型 | 机制 | 可信度性质 | 代表工作或工具 | 阙疑对应 |
|---|---|---|---|---|
| 专家标注 (expert annotation) | 人类判定标签 | 受标注者偏差、人数、专业度影响；一致性≠正确 | NeurIPS D&B 数据集（60 个样本，Bhardwaj 2024） | 37 实卡中 verified 23 / red-team 3 / draft 11 的人工状态 |
| 交叉验证 (cross-validation) | 多划分多训练估计泛化 | 估计样本外表现，但本身不产标签 | Shao & Tu 体系；NeurIPS 2024 论文 2407.02754 | 盲 holdout 30 作为独立估计集 |
| 程序化构造 (programmatic) | 由构造过程保证标签正确 | 可复算、可独立验证，最强 | Csmith 差分测试（PLDI 2011，325+ bug） | 真实缺陷夹具 15（重注入 6/6=100%） |
| 已知缺陷夹具 (known-defect fixture) | 把真实历史缺陷重注入作已知答案 | known-answer test（KAT）性质 | 密码学 KAT 测试向量（NIST PQC） | 历史覆盖 12/15=80% |

**差分测试是"无预言机"构造金标准的典范。** DeepWiki 对 Csmith 的描述：*"the same test input is processed by multiple implementations... outputs are compared to identify discrepancies"*，具体通过 *"Internal consistency is verified by comparing checksums across optimization levels for the same compiler. External consistency is verified by comparing checksums across different compilers."*（DeepWiki, csmith/5.1）。这意味着**金标准不是预先写好的答案，而是"多实现不一致即可疑"的涌现信号**——这与阙疑"独立对账器不信任内核地复算判决"的设计哲学同构。

**已知答案测试（KAT）是构造式金标准的最简形式。** 密码学实现正确性验证中，KAT 被称 *"密码算法质量的'第一道防线'"*（openHiTLS 博客，2025-08-24），即只有通过与已知答案向量比对，实现才进入后续测试。阙疑"真实缺陷夹具 15"正是 C++ 知识断言域的 KAT：每条夹具的"正确答案"（真错 / 真对）由真实历史缺陷保证，而非由评审委员会投票。

**四种来源在"知识断言"上的映射与取舍。** 把上表转译到阙疑的任务：一条 C++ 知识卡（如"在 C++20 中 `std::weak_order` 对 NaN 返回什么"）若靠专家标注，标签质量取决于标注者是否熟悉 C++ 标准与实现差异；若靠交叉验证（多个 LLM / 多个内核划分互验），得到的是"一致性"而非"正确性"；若靠程序化构造（用编译器实际行为 + 标准条文自动判定），则标签可由构造过程复算；若靠已知缺陷夹具（把真实踩坑的代码片段作为 KAT），则标签由"历史上确实编译/运行出某结果"保证。经验法则：**凡是能被程序化或夹具化的断言，就不要用专家标注**，因为前者可独立复算、可进版本库、可被第三方审计，后者只能靠"相信人"。阙疑当前 37 实卡中 verified 23 的状态若长期依赖人工判定，应在论文中明确其金标准等级低于夹具 15 与盲 holdout 30，否则会被审稿人按 Bhardwaj 2024 的 rubric 扣分（"可靠性 / 真实性"维度）。

### 二、金标准质量评估：一致性、覆盖率、偏差

金标准造出来后，仍需评估其质量。三个维度有硬证据：

**一致性（consistency）**：NeurIPS 数据策展评估用 ICC（ intraclass correlation）衡量评分者间信度，框架本身可靠性高（*最终轮 ICC 中位数 0.90*，各 rubric 类别 0.83–0.98，Bhardwaj 2024），但这是"评估框架一致"，**不是数据集标签正确**。tianpan.co 指出更危险的陷阱：*"Annotators can be consistently wrong"*，系统性错误（shared misconception）在多数投票下不会被平均掉——*"Collecting twice as many annotations wouldn't have helped"*（AV 标注框系统性偏大案例）。

**覆盖率（coverage）**：Bhardwaj 评估发现 18 项中 *"情境意识"与"环境足迹"的最低标准通过率均为 0%*；MMLU 教训更直接：独立审计发现大模型的**污染率高达 91.8%**，数学子集约 **2% 题目本身错误**（标签错误 / 措辞模糊 / 数学错误），且前沿模型得分已饱和在 **88%–90%**（SevenNews, 2026-07-28）。覆盖率不足使金标准天花板失真。

**偏差（bias）**：tianpan.co 举 UNESCO 研究——*主要模型把女性与"home/family"关联的频率是男性的 4 倍*，可追溯到标注团队技术判断角色中男性偏多；媒体偏差检测中众包标注者缺乏领域知识导致质量下降。下表汇总三类质量风险的证据：

| 质量维度 | 关键数字 | 来源 | 对阙疑的警示 |
|---|---|---|---|
| 一致性（框架） | ICC 中位数 0.90 | Bhardwaj 2024 | 需报告内核 vs 独立对账器判决一致性 |
| 一致性（标签陷阱） | kappa 在不平衡类虚高 | tianpan.co 2026 | 四态分布不平衡时勿只看 kappa |
| 覆盖率缺口 | 情境意识 0%、环境足迹 0% | Bhardwaj 2024 | 需声明夹具 15 未覆盖的 C++ 主题 |
| 覆盖率失真 | 污染 91.8% / 饱和 88–90% | SevenNews 2026 (MMLU) | 避免知识卡泄漏进训练语料 |
| 偏差 | 性别关联偏差 4× | tianpan.co / UNESCO | 标注团队需多样性 + 子群分析 |

**系统性误差比随机噪声更难修，对阙疑的启示是"别只做多数投票"。** tianpan.co 区分了两类误差：随机误差（疲劳、偶然歧义）可被多标注平均掉；系统性误差（共同误解、有缺陷的指南、文化假设）则"collecting twice as many annotations wouldn't have helped"。映射到阙疑：若 67 条规则与 9 个保护器都是由同一作者（双非本科生、单人对齐标准理解）在相近语境下写就，那么"内核 vs 独立对账器一致"可能恰恰反映的是**同一个人的系统性理解偏差被对账器继承**——这正是对账器设计要"不依赖内核"却仍可能共享同一知识来源的风险。缓解办法不是加人，而是把"真错 17"的盲 holdout 当作与外部知识源（C++ 标准条文、编译器实测）对齐的硬约束，使系统性偏差在 gold 层被拦截。

**覆盖率的"天花板失真"是金标准最隐蔽的失效。** MMLU 案例表明：当 2% 题目本身错误、且模型得分被与含错天花板比较时，两模型 2 分之差可能只是"谁在错的 2% 里更走运"。阙疑外部 corpus 40 当前 A/B/C 三层检出率 54.2% / 12.5% / 0%，且 ctx 已标注"算术不自洽待修"——若 gold 自身算术不自洽，则 43.8% 的总检出率数字不可信，必须先把 corpus 40 的金标准算术复算修好，再对外报告，否则会落入与 MMLU 相同的"测量地板"陷阱。

### 三、软标签 vs 硬标签：知识断言该用哪种

把"知识断言真伪"压成硬 0/1 会丢掉"不确定边界"。Pavlovic et al.（2026）做了受控审计：

- **数据集**：MNIST 子集（2,131 训练 / 457 验证 / 457 测试）、Mukhoti 模糊 MNIST（1,738 / 373 / 373），每图平均 **6 个标注**（N=480 标注者）。
- **核心发现**：先前研究把软标签的益处与重标注时的标签模式偏移混为一谈；MNIST 上约 **3% 准确率增益来自修复标签错位**，Mukhoti 重标注使 **约 33% 样本主流标签改变**。
- **校准**：HLV（高人类标签变异）子集 KLD（越低越好）`orig` 2.214 → `maj_n`（硬）1.661 → **`soft_w`（软）0.669**；人类软标签与模型置信度 Spearman 相关 **−0.70 (p<0.001)**，而合成硬标签仅 −0.09（几乎不携带人类不确定性）。

**对阙疑的含义**：四态判决 {真对、真错、存疑、未定} 不是四选一的硬标签，而应视为**软标签的离散化**——"存疑"态携带"人类 / 内核都不确定"的信息，硬打成 0/1 会像 MNIST 那样丢失对齐人类不确定性的校准收益。建议：把每条卡的判决概率写入 gold ledger，而非仅存最终态。

**硬标签的校准风险在"知识断言"上尤其致命。** Pavlovic 等指出合成硬标签（one-hot）与人类不确定性相关性仅 −0.09，几乎不携带人类感知的不确定性；若阙疑把"存疑"强行二分为"真/假"，当某条 C++ 标准条款在不同编译器版本行为不一致时，系统会给出高置信度的错误判决，且无任何"我不确定"的信号可供下游（如论文写作、代码生成）消费。这正是软标签作为**正则化器**的价值：即便准确率增益有限（MNIST 上 HLV 子集仅 1–4%），校准增益（KLD 0.669 vs 1.661）使系统在边界案例上"在人类不确定时也保持不确定"，对知识验证系统的可信度远比原始准确率重要。阙疑的四态设计已经走在软标签方向上，缺的只是把概率与置信区间显式落盘、并像 Pavlovic 那样用 6 个以上独立标注者（而非单作者）去标定"存疑"的边界。

| 标签形式 | KLD(↓) HLV 子集 | 对齐人类不确定性 | 阙疑映射 |
|---|---|---|---|
| one-hot 硬标签 | 1.661 (MNIST) | 弱（−0.47） | 仅存最终态 → 丢失校准 |
| 人类软标签 | **0.669** | 强（−0.70） | 四态 + 置信区间 |
| 合成标签 | 1.612 | 可忽略（−0.09） | 反事实算子（待修，当前 P=R=F1=0） |

### 四、阙疑的 ground truth 锚点：真实缺陷夹具 15 与盲 holdout 30

根据项目实测（2026-09，ctx 锚点）：

| 锚点 | 规模 | 关键数字 | 在 ground truth 中的角色 |
|---|---|---|---|
| 真实缺陷夹具 15 | 15 条 | 重注入 **6/6 = 100%**；历史覆盖 **12/15 = 80%** | **known-answer test 集**：标签由真实缺陷构造保证 |
| 盲 holdout 30 | 30 条 | 真错 **17**，检出 **66.7%** | **盲态独立估计集**：真值先于系统构建已知、且评估时不可见 |
| 外部 corpus 40 | 40 条 | 检出 43.8%（A 54.2% / B 12.5% / C 0%） | 三层覆盖检验（算术不自洽待修） |
| 变异 core/all | 97.3% / 81.5% | **已放弃当作缺陷检测率** | 仅作稳健性信号，不进 gold |

**两个锚点恰好覆盖了"构造式"与"盲态独立"两类最可信的金标准来源**：
- 夹具 15 = KAT / 已知缺陷夹具（方向一第四类），其 6/6=100% 重注入率证明"标签可复算"；12/15=80% 历史覆盖率则暴露**覆盖盲区**（有 3 条历史缺陷未被现有 67 规则捕获）——这正是方向二"覆盖率"维度要声明的风险。
- 盲 holdout 30 = 交叉验证 / 独立估计集（方向一第二类），其"真错 17"是**先于系统、且在评估时不可见**的 gold，66.7% 检出率为系统给出无偏估计。它之所以可信，正是因为"盲态协议不可回盲"——标签不会在系统跑分后被偷偷修改。

**把锚点做成可发布的 gold artifact 是 NeurIPS E&D 的硬性要求**：2026 CFP 明确 *"Code... is required at submission when the primary contribution is a reusable executable artifact, such as a benchmark suite, evaluation environment, data generator, or software tool"*（neurips.cc, 2026）。阙疑应把夹具 15 的重注入脚本、盲 holdout 30 的 gold ledger（含 verdict、evidence_hash、reconciler_sig）随稿发布，并附 **Croissant + Responsible AI (RAI)** 元数据。

**两个锚点必须保持"来源独立"，否则会共因失效。** 夹具 15 来自真实历史缺陷（构造式），盲 holdout 30 来自独立收集的真错（盲态估计），二者若由同一批 37 实卡派生，则 66.7% 检出率与 80% 历史覆盖率会共享同一偏置、无法互相印证。论文应显式声明：夹具 15 与盲 holdout 30 的卡片**不重叠**、且都不参与 67 规则的训练/调参（防止"用自己的训练集当测试集"的泄漏，类似 MMLU 91.8% 污染）。此外，随系统规模增长，锚点存在**饱和风险**——当检出率逼近 100% 时，锚点失去区分力，需按 HLE / GPQA Diamond 的"动态滚动更新"思路，持续向夹具集补充新的真实缺陷（如新标准条款、新编译器版本行为漂移），使 gold 始终有未饱和的鉴别力。这是阙疑作为"活系统"相对一次性静态基准的可持续优势，应在局限性之外作为卖点陈述。

---

## 对阙疑的 3 条具体行动

1. **把"真实缺陷夹具 15"升级为可发布的 known-answer test 集，并补录覆盖盲区。**
   在 `C:/CodeLearnling/note/note/C++/CPP-Bible/_arch_v47/` 下新增 `40b_fixtures_KAT.md`，逐条记录 15 夹具的构造来源（GitHub issue / commit hash / CVE）、重注入命令与复算脚本，显式复现 **6/6=100%** 与 **12/15=80%**；对未覆盖的 **3 条**历史缺陷列出根因（是规则缺失还是断言不可机器判定）。时间点：**2027-05 前**完成，以满足 NeurIPS E&D "code release required when artifact is reusable executable" 与 Croissant RAI 元数据要求。

2. **用独立对账器 + Merkle checkpoint 把盲 holdout 30 的"真错 17"做成不可回盲 gold ledger。**
   在 `gate_engine.py`（当前 3826 行）之外，将 30 条 gold 判决写入 append-only 哈希链，字段含 `verdict / evidence_hash / reconciler_sig / timestamp`，由"不依赖内核的独立对账器"签名；与现有 **452 条判决账本**对齐，并修复 ctx 提到的 **227 项工作树漂移**与 README 口径滞后，使 gold 与代码状态一致可验。

3. **把四态判决显式建模为软标签，并报告内核 vs 独立对账器的一致性指标。**
   在 67 规则 + 9 保护器之上，为每条知识卡输出 {真对, 真错, 存疑, 未定} 的概率向量而非仅最终态；对盲 holdout 30 用 **Cohen's kappa / ICC** 量化内核与对账器判决一致性（参考 Bhardwaj 2024 的 ICC 0.90 口径），并对"存疑"态给出置信区间。反事实算子当前 **P=R=F1=0 待修**，修复后需重新校验软标签分布是否改变 gold 标签——该步骤纳入 2027 审稿前回归。

---

## 盲区（诚实标注）

- **NeurIPS 2027 E&D 的具体 CFP 尚未发布**：当前 neurips.cc 官网仅有 2026 版（双盲、Croissant RAI、摘要截止 2026-05-04）。2027 年的关键日期、是否维持双盲、RAI 字段是否仍强制——**未核实**，需 2026 下半年官网更新后复核。
- **阙疑"真实缺陷夹具 15"的原始账本未逐条读取**：12/15=80% 中"未覆盖 3 条"的具体缺陷与根因、6/6 重注入所用脚本命令，均来自 ctx 摘要，**未核实**原始 452 条账本与 15 夹具文件。
- **"变异 core 97.3% / all 81.5% 已放弃当缺陷检测率"的弃用理由未核实**：该决定如何影响 ground truth 锚点（是否仍可作稳健性佐证）未读原始决议。
- **反事实算子 P=R=F1=0 待修**：修复是否会改变软标签 / gold 标签分布**未核实**，属未来回归风险。
- **Barr et al. 2015《The Oracle Problem in Software Testing: A Survey》的 taxonomy 细节（specification / derived / pseudo-oracle 等分类）仅据摘要**，未逐字核实具体分类表。
- **本机 sanitizer 运行时缺失**（GCC `cannot find -lubsan`、Clang 缺 `libclang_rt.asan_dynamic_runtime_thunk.a`）：阙疑"程序化构造"的金标准**无法在本机用 sanitizer 复算验证**，是项目自身盲区，需在论文中声明限制。
- **MMLU "91.8% 污染率 / 2% 题目错误"** 来自 SevenNews（2026-07-28）二手报道，原始审计论文的 DOI / 样本量**未核实**，引用时建议溯源至原始审计。

---

## 来源

1. NeurIPS 2026 Evaluations & Datasets Track CFP — https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets — 关键引文：*"evaluation becomes an object of scientific study in its own right"*、*"Submissions need not introduce a new model or outperform prior work"*、code release required for executable artifacts、Croissant RAI；摘要截止 2026-05-04 — NeurIPS 组委会 — 2026。
2. Yang, Chen, Eide, Regehr, *Finding and Understanding Bugs in C Compilers*, PLDI 2011 — https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf — 关键数字：*"more than 325 previously unknown bugs"* 在 GCC/LLVM/商业编译器，三年；差分测试无需 oracle — University of Utah — 2011。
3. Csmith Differential Testing Process (DeepWiki) — https://deepwiki.com/csmith-project/csmith/5.1-differential-testing-process — 关键引文：*"Internal consistency... across optimization levels... External consistency... across different compilers"*，checksum 比对 — csmith-project — 2025。
4. Bhardwaj, Gujral, Wu, Zogheib, Maharaj, Becker, *The State of Data Curation at NeurIPS*, arXiv:2410.22473 — https://arxiv.org/html/2410.22473v1 — 关键数字：60 数据集、18 元素、ICC 中位数 0.90、情境意识 0%、环境足迹 0%、最低标准通过率 78%→67%→61% — 多伦多大学 — 2024。
5. SevenNews, *MMLU benchmark retirement: contamination, flawed answer key* — https://www.seventnews.com/zh/articles/mmlu-... — 关键数字：污染率 91.8%、数学子集 ~2% 题目错误、饱和 88–90%、HLE/GPQA Diamond 替代 — Emmanuel Fabrice Omgbwa Yasse — 2026-07-28。
6. tianpan.co, *Annotator Bias in Eval Ground Truth* — https://tianpan.co/blog/2026/04/17/annotator-bias-eval-ground-truth — 关键引文：*"High Agreement Is Not the Same as High Quality"*、*"Annotators can be consistently wrong"*、UNESCO 女性关联偏差 4×、Cohen's kappa 不平衡类虚高 — Tian Pan — 2026-04-17。
7. Pavlovic, Paun, Poesio, *An Assessment of Human vs. Model Uncertainty in Soft-Label Learning and Calibration*, arXiv:2605.18648 — https://arxiv.org/html/2605.18648 — 关键数字：MNIST KLD soft_w 0.669 vs maj_n 1.661、Spearman −0.70、每图 6 标注、Mukhoti 33% 主流标签改变 — Queen Mary University London / Amazon / Utrecht — 2026-05。
8. Barr, Harman et al., *The Oracle Problem in Software Testing: A Survey*, IEEE TSE 2015 — https://coinse.github.io/publications/pdfs/Barr2015qd.pdf — 关键引文：*"All forms of test oracles, even the humble human, involve challenges of reducing cost and increasing benefit"* — King's College London / UCL — 2015。
9. Ali et al., *Empirical Fault Patterns for Mutation Testing* (及相关变异测试实证), arXiv:2311.16913 — https://arxiv.org/pdf/2311.16913.pdf — 关键数字：>0.7 million 量子电路变异体研究 fault seeding — 2023（变异注入 / 缺陷重注入方法论参考）。
10. Bayle et al. (通讯作者 Shao), *Is Cross-Validation the Gold Standard to Evaluate Model Performance?*, NeurIPS 2024 — https://arxiv.org/abs/2407.02754 — 关键结论：CV 并非总是估计样本外表现的金标准（高阶 Taylor 分析）— NeurIPS 2024（交叉验证作为估计手段的局限）。
11. openHiTLS, *密码实现安全测试基础篇 · KAT（已知答案测试）* — https://blog.csdn.net/openHiTLS/article/details/150634293 — 关键引文：KAT 是*"密码算法质量的'第一道防线'"* — 2025-08-24（KAT 作为构造式金标准的最简范例）。
12. NeurIPS 2025 Datasets and Benchmarks Track (历史对照) — https://neurips.cc/Conferences/2025/CallForDatasetsBenchmarks — D&B 轨道定位与范围演变参考 — NeurIPS 组委会 — 2025。
