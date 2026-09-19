# 582 · 调研苦力大调研：知识资产层——让阙疑从"能验证几十张卡"变成"可累积、可溯源、可换代、可上规模"（只读 · 产物落 _arch_v9/）

> 你是**调研苦力**（同族工程/学术调研，不是建设者）。本任务**全程只读**：联网调研 + 读现有代码 + 纯统计/静态分析，**不改任何正式文件、不写卡/规则/工具、不 golden accept、不 push**。所有产物只写进新建目录 `_arch_v9/`。
> 与你并行的还有一个**建设苦力在跑 581**（正在改 `tools/poison_drill.py` 与覆盖率口径）。你们共享同一工作树——**这是硬隔离要求，违反即事故**：
> - **禁止**跑 `pytest`（全量/子集都禁止）、`poison_drill`、`mutation_fuzz`、`gate_engine --update`、`tool_integrity --update`、`git checkout/reset/clean/add/commit`、任何会写或"还原真实仓库"的命令（上一轮调研苦力跑 pytest，其还原逻辑 checkout 销毁了建设方未提交文件）。
> - 本批主题主要靠**外部调研 + 静态读代码**，默认零实跑。确有必要实跑的探针，**必须先 `git worktree add` 一个独立工作树或另克隆一份**，在隔离副本里跑，主仓只读；探针产物放副本或 `_arch_v9/probes/`，绝不碰 `build/`、`atoms/ evidence/ Examples/ Book/`。
> - 读代码以**磁盘当前内容**为准；若发现 581 正在改 poison 覆盖率相关代码，记录"建设进行中"即可，不要评价半成品、不要替它改。

## 独立性纪律（同族调研必须人工补上，逐条照做）
1. 每个外部工作（论文/系统/标准/库）必须给：**可访问 URL + 你的检索日期（2026-09）+ 一句话它实际是什么 + 一手还是二手**。区分【已查证】（读到一手原文/官方文档）与【一方称】（只有厂商博客/聚合二手）。**严禁编造 arXiv 编号、版本号、性能数字、发布日期**；查不到一手就标【一方称】或【未查证】，不许用想象补齐。
2. **先找反例、先找"不适用"的理由**，不要附和仓库既有结论，也不要附和本任务书给的种子系统名——种子只是起点，你要核实它是否还活着、是否真有所述能力、license/语言/Windows 可行性。
3. 算不出/没数据的明说"算不出/缺什么"，不填 0、不编默认值。任何给本仓的数字要么来自读代码/只读统计，要么标【估算并写清假设】。
4. 每条建议都要过三关：**零误伤（不改判决语义）/ 弱模型可执行（不依赖还不存在的 LLM 能力）/ 不依赖模型当裁判**；过不了的归入"等条件"。
5. 结束写 `_arch_v9/zero_pollution.md`：列你读过/写过的路径，证明正式目录零改动（用 `git status --short` 只读快照，**不要** checkout）。

---

## 一、当前真实基线（2026-09-18，避免再拿过时数字；以你磁盘读到的为准，发现不一致要指出）

- 系统：阙疑/QueYi 元系统（机器可核验、错误率有上界、可审计、可随模型换代换验证者的知识生产系统），CPP-Bible 是 C++ 试车场。三方分工：豆包=架构/红队/验收，苦力=建设，异族（换新模型会话）=只读范式批判。
- 规模：27 张原子卡带 `claim_structured`、**79 命题（observation 50 / inference 29）**；卡级签署 card_signed 76 / unsigned 3；50 条 observation 待补命题级 liveness 锚（`data/prop_liveness_todo.md`，知识活，机器不代填）；negative_controls 真阴面仅 EV-CONC-001 一张；另有 80 条 MIS 误解库"字段填满、机器没判真伪"（564 定性的弱 Oracle 第三态）。
- 门禁：gate **63 规则 / 191 命中（block=0 warn=186 advice=5）**；poison **118/118**、攻击面 424、零覆盖攻击面无；replay confirm=56/refute=0（56 卡真编译 Oracle）；fast pytest `-n auto` 约 42–70s、slow `-n0` 约 203s（test_task_queue_stateful 单测约 79s 占 39%）。
- mutation 权威串行基线 v5（清态）：1183 变体，**blocked 989（严格 619）/ escaped 9 / n_a 185**；逃逸率版本史 v1 23.7%（含 M2 的 207 条尺子 bug 假逃逸）→ v2 6.3% → v3 3.8% → v5 约 0.9%；M6 仍 8 条逃逸待定性。统计用纯标准库 `tools/stat_bounds.py`（Clopper-Pearson，无 scipy/numpy）。
- 已有的"知识资产层"雏形（**先读再评，别当不存在**）：`data/propositions.db`（`tools/prop_graph.py` 派生视图，SCHEMA_VERSION=2 自愈，命题/签署/证据锚）、`data/overturned_events.jsonl`（只追加推翻事件，human 推翻须 git 作者绑定，系统绝不自动产生）、`data/oracle_registry.json`（gcc/gate/replay 版本登记，verified_by_oracle 只写不读、开关全 OFF）、`data/metrics.jsonl`（收敛三曲线：逃逸率/被推翻数/生存时间，带运行间方差声明）、`data/golden_state.json`（人审基线四桶）、git 历史本身。
- 已冻结（**不要建议现在实现，只评估"解冻信号"**）：LLM-as-judge 终审、自动 KG、在线改权重、G-supervisor、密码学签名/身份、自动 LLM 推翻、开放激励、zkVM/Lean 化证明。LLM 放行权开门条件≈误判上界 ≤1%（约 460 条零误判量级，Clopper-Pearson）。
- 前五轮异族/调研结论位置（**先读，明确"不重复"，你的增量要建立在其上**）：`_arch_v4/`（性能五层、Bazel CAS/Nix、Letta 记忆、TIA/TestPrune 浅尝）、`_arch_v5/`（无终极底座、四预留口子、zkVM/FLT/AIXI/active inference）、`_arch_v6/`（Clopper-Pearson 上界、Dung 论证 grounded 三值、异族分权、correct-by-construction）、`_arch_v7/`（抽走 g++ 两张清单、三 meta 攻击实锤、NEJM 人审 RCT、clingo 可装、激励冻结）、`_arch_v8/`（fast/slow 实测、testmon/Bazel sharding/ESLint cache、B3/B4 提速归 W）。

## 二、伞主题

> **当命题从 79 涨到 1 万、当验证者（编译器版本/规则引擎/模型）换代、当系统要吸收外置知识时，阙疑的"知识资产层"该长什么样，才能保证：累积不丢真、溯源可追、换验证者可无损重验、规模上去查询不塌、攻击随系统一起进化、"在收敛"这件事有在线统计保证？**

围绕六个 lens 调研，每个 lens 都必须落到同一套三段式：**【外部有什么：带链接/日期/一二手】→【本仓现状：读代码指明具体文件与缺口】→【现在借 N / 攒数据 D / 等条件 W】**，N 档必须零 Oracle 风险、弱模型可做、有机器验收。

### Lens 1 · 双时序与不可变知识账本（事实何时成立 × 何时被知道 × 被哪个验证者版本判过）
本仓已有 overturned_events + metrics 三曲线 + git，但都是散装。调研：bitemporal/temporal 数据模型（XTDB/Crux、Datomic、SQL:2011 `AS OF`/`SYSTEM_TIME`、TerminusDB）、event sourcing 与不可变 log、Datalog/Datascript/Asami 这类"事实+时间"查询、W3C **PROV-O** 溯源本体。回答：阙疑的一条命题应记录哪几条时间轴（asserted_at / valid_at / verified_by 版本 / overturned_at）？现有 jsonl+sqlite+git 三件套够不够，缺什么视图？怎么在不引重依赖（纯标准库优先）下拿到"某验证者版本下的命题快照"与"任意时刻被推翻集合"？

### Lens 2 · 命题网络的规模化与一致性（79 → 10k：去重、依赖、不一致检测、查询引擎选型）
读 `tools/prop_graph.py` 与 impact_analysis（已有多跳闭包/环检测）。调研：属性图 vs RDF/OWL vs Datalog/ASP 的边界；**clingo/ASP（564 已核实 5.8.2 cp313 win wheel 可装）到底该承担哪类查询**（grounded 是 P 类、preferred/stable 是 NP 完全，566/563 提过，要给出"什么查询用 SQL、什么才值得上 ASP"的判据）；ontology debugging / justification（OWL MUPS、最小不一致子集）；命题同义/重复/冲突的机器检测；什么时候 sqlite 递归 CTE 不够、需要图/逻辑引擎。给一个**随命题量分级的选型表**（<1k / 1k–10k / >10k 各用什么）。

### Lens 3 · 换验证者的交接契约（阙疑最差异化的能力，562 只开了四个口子）
调研：Thompson《Reflections on Trusting Trust》与 Wheeler **DDC（diverse double-compiling）**、**LCF 内核架构**（checker 必须远简单于 prover，de Bruijn 原则）、Milawa/CakeML/seL4 的自举可信链、**proof-carrying code/evidence**（Necula）、软件供应链的 SBOM（SPDX/CycloneDX）/**in-toto attestations**/**SLSA levels**、模型卡/系统卡（Mitchell model card）与"AI BOM"。映射到阙疑：设计一份**"知识 BOM / 验证者能力声明"**——每条命题/证据登记它被哪个版本的什么 Oracle 判过、该 Oracle 的能力与 TCB 边界；验证者换代（g++ 升级、规则引擎重写、未来上模型）时，哪些结论自动失效必须重验（fail-closed）、哪些可继承？给出 verified_by_oracle 换代的**重验调度算法草案**与最小数据结构（只设计、不实现）。

### Lens 4 · 可核验的外置知识与记忆（用户点名方向；v4 只浅尝 Letta）
两条线：
- (a) **RAG/检索的事实性与引用核验**：RAGAS、ARES、CRAG（corrective RAG）、Self-RAG、grounding/citation 核验（AlignScore、TRUE 类）、FEVER 式事实核查。核心对应本仓"**引用 ID 存在 ≠ 引用内容真**"（MIS 80 条弱 Oracle、reference audit）：外置材料进系统，必须携带什么形态的证据、过什么机检才被接受？哪些今天就能用确定性规则做（引用锚定、出处可达性、引文与原文 span 比对），哪些必须等模型？
- (b) **记忆系统纵深**：MemGPT/Letta Context Repositories、Mem0、A-MEM、Zep/**Graphiti（双时序知识图谱，重点对照 Lens 1）**、LangGraph memory。判断：哪些机制适合一个"错误率要有上界"的系统（即记忆不能静默改写事实）？外置记忆层与本仓 jsonl/sqlite/prop_graph 的物理边界怎么划（560 E 提过"检索双通道物理隔离、四表可查询记忆、kg 三种真语义边且自动入库仍冻结"，你要核实并推进或反驳它）。

### Lens 5 · 攻击生成系统化 + 等价变异体（让 mutation 从 7 个手写算子长成攻击生成器）
当前 mutation 7 算子（M1–M7）是手写的，且反复出现"**变异点不在门禁读取面**"的无效变异（M2 曾 207 条假逃逸、M6 8 条待定性）。调研学术界 **equivalent mutant / trivial mutant problem**（Jia & Harman mutation testing 综述、Offutt）、mutmut/Stryker/PIT 工程实践、**coverage-guided fuzzing（AFL/libFuzzer）、grammar fuzzing、metamorphic testing（Chen）**、property-based（已用 Hypothesis）、LLM 红队框架（**PyRIT、Garak、MITRE ATLAS**）。回答：怎么自动生成"落在门禁真实读取面、且语义上真的弱化断言"的变异？怎么**机器识别并剔除等价/无效变异**（而不是把它们算进逃逸或拦截率分母）？怎么评估攻击集自身的多样性/覆盖（attack-surface coverage）？给 M6 那 8 条逃逸一个定性方法学（不要求改代码）。

### Lens 6 · 在线收敛的统计监测（把三曲线从静态 C-P 区间升级为带错误率保证的连续监测）
现在每批跑一次 Clopper-Pearson 静态区间。但系统是逐批运行、持续看逃逸率下降的——**反复看同一指标会导致假阳性累积**（peeking）。调研：**序贯概率比检验 SPRT（Wald）、always-valid / anytime 置信序列（anytime-valid inference）、alpha-spending（O'Brien-Fleming）、CUSUM/EWMA/Shewhart 控制图**、A/A 与 flaky 的统计判定、连续监测下"何时才能合法宣称单调收敛/逃逸率真的下降了"。产出可落地的判据：在 `stat_bounds.py`/`metrics.jsonl` 上，连续 N 批满足什么条件、用什么检验，才能把"逃逸率在降"从印象变成带错误率上界的结论（给公式、输入数据路径、开门所需批次数；算不出的明说）。

---

## 三、交付清单（全部在 `_arch_v9/`，Markdown，中文，可只读复跑的探针放 `probes/`）

1. `00_总览_现在借什么_攒什么_等什么.md`：一页纸结论——六个 lens 各自**最该立刻做的一件 N 档小事**（合计不超过 6 件，每件挂：改哪个文件、机器验收命令、预期零误伤证据）、一张"79→1万命题的知识资产层演进路线图"、以及一句话回答伞主题。
2. `01_双时序账本.md` … `06_在线收敛统计.md`：六个 lens 各一份，每份固定四段：外部图谱（带 URL/日期/一二手/2026 是否还活着）· 本仓现状（具体文件:行/表/字段）· 差距与风险 · N/D/W 三档建议。
3. `07_可计算判据集.md`：所有"现在就能加进 stat_bounds/metrics/prop_graph 的机器判据"，给公式、输入路径、需要的样本量/批次数、假设成立与不成立条件；算不出的单列并写清缺什么数据。
4. `08_自攻击_这些方案在本仓会怎么失效.md`：红队你自己的提案——每个 N 档建议若被采纳，攻击者/苦力/未来的自己会怎么钻空子（参照 564 的 PoC 风格：能不能伪造、能不能静默降级、换验证者时会不会假继承），每条带回退/失败触发条件。
5. `zero_pollution.md`：只读自证（读了哪些正式文件、写了哪些 _arch_v9 文件、`git status --short` 只读快照证明正式目录零改动；若用了 worktree 隔离副本，写明副本路径且主仓零写）。

## 四、明确不做 / 边界
- 不改任何代码/卡/规则/台账/基准；不跑写命令与 pytest（见硬隔离）；不替 581 的覆盖率改造下结论。
- 不重复 v4–v8 已有结论：凡引用前轮，一句话带过并标注"详见 _arch_vX/某文件"，你的篇幅用于**增量**。
- 冻结项（LLM 裁判/自动 KG/密码学签名/自动推翻/激励）只评估"解冻的可判定信号与所需证据量"，不设计实现蓝图、不鼓励提前做。
- 不做地图、不产出需要外网 CDN 才能看的东西；报告纯 Markdown，表格能在 GitHub 直接渲染。
- 若某个 lens 调研后结论是"本仓现阶段不需要/是过度工程"，**直接说不需要并给理由**——否掉一个方向也是合格交付，不要为凑篇幅硬推技术。

## 五、提醒（省得重踩）
- Windows + PowerShell；解释器 `.venv\Scripts\python.exe`（Py3.13 + PyYAML，**无 scipy/numpy/pandas**，统计探针纯标准库）；clingo 若要试装只在隔离副本。
- 外部资料优先一手（官方文档/论文原文/标准正文），博客与聚合二手必须标【一方称】；2025–2026 的"最新进展"尤其要核实，模型训练数据可能滞后。
- 你是同族（不是换新模型的异族），更要刻意唱反调：每个推荐技术同时写"什么情况下它会害了我们"。
