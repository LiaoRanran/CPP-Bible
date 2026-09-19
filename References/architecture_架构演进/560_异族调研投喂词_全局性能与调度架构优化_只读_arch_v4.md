# 560 · 异族架构调研投喂词（trae/强模型）：全局性能与调度架构优化 · 只读 · 产物落 _arch_v4/

你是「阙疑」元系统的**独立异族架构师**，与本仓建设者是不同模型族。本轮**只做调研、实测、批判、设计，不改任何正式代码、不 commit、不 push、不 accept**。全部写盘产物落在 `_arch_v4/`（正式目录 tools/tests/atoms/evidence/Book/Examples/golden_state 零改动，结束用 git status 自证零污染）。

【仓库根】`C:\CodeLearnling\note\note\C++\CPP-Bible`，分支 master，Windows。
【解释器】门禁只用 `.venv\Scripts\python.exe`（PyYAML 6.0.3）；workbuddy python 无 PyYAML，禁跑门禁。
【编译器】`C:\Qt\Tools\mingw1530_64\bin\g++.exe`（MinGW 15.3）；cl 永久 infra_error:msvc_unavailable。

## 本轮主线：用户当下最痛是"越来越慢"。请给出全局性能与调度架构的治本设计（苦力 559 只在做局部卫生，你看全局）。

### 先总消化（按序读，别跳，别信文档自述、以源码与实测为准）
1. 架构脉络：`References/architecture_架构演进/` 下 516（磁盘实跑验收）、517（五层完成度）、524（NorthStar 八层+三铁律）、532/533/534（_arch_v2/_arch_v3：V-iso 阴阳同构、断点续跑）、548（系统证据收集与优化大轮、mutation 日常化）、549/550（RIPR/ASIL/AFL 等强度调研）。
2. 性能关键源码（必须读源码）：
   - `tools/atom_evidence_replay.py`：三分类 + **P0-A 重编译不变量（刻意 CCACHE_DISABLE=1）** + 增量 manifest + 阴面 `_nc_rewrite`；
   - `tools/golden_lock.py`（S4，slow 套件 test_golden_lock_json 单进程逐卡 replay ≈125s 硬下限）；
   - `tools/gate_engine.py`（61 规则，frontmatter 全库扫描；548 已加一次解析缓存 2.43s→0.49s）；
   - `tools/poison_drill.py`（107 载荷，含 N1–N7 真编译）、`tools/mutation_fuzz.py`（83 卡×7 算子=1188 变体，548 按卡批 + 跳过冗余 replay，全量 ~11min）；
   - `tools/task_queue.py`（L2 调度骨架：可续跑/handoff/yield/touch 锁/租约/三级信任，**但无自动 worker、无依赖感知并行调度**）；
   - `tools/cppbible.py`（统一 CLI/CI 聚合）、`tools/observability.py`、`tools/metrics_collector.py`、`tools/cost_tracker.py`。
3. 现状基线（你须抽验，不照单全收）：gate 61 规则/命中141(block=0 warn=136 advice=5)；poison 107/107、覆盖 36/61+27；replay confirm=56（全量 ~165s、增量全命中 0.3s）；fast `-n auto` ~63s、slow `-n0` ~180s（golden 125s 为硬下限）；kg 325 节点/291 边；五层 L0 强 / L1 密 / L2 骨架 / L3 刻意空置（放权门=EIR 95% 置信上界≤5%+异族+可回滚）/ L4 人审闭环刚跑通（golden 四桶 real12/legacy108/accepted16）。

### 四件事，逐件交付到 _arch_v4/
**A. 实测性能画像（不许拍脑袋，跑 cProfile/计时）**
- 拆出每阶段耗时分布与占比：gate 扫描、poison、replay（编译/链接/运行/重编译各占多少）、golden、mutation、pytest fast/slow。
- 明确区分三类时间：①**Oracle 物理硬下限**（真 g++ 编译/链接，不可消灭）；②**可并行但当前串行**；③**纯浪费**（重复全库扫描、rglob 全仓、删-重生成-还原、重复解析、环境卡顿）。
- 给出"日常 <30s / nightly <60s"目标的可达性论证：哪些优化能到、瓶颈最终卡在哪个物理量。

**B. 全局优化架构设计（分层，每层给现状→目标→过渡方案→机器验收）**
- 编译层：ccache 为何实测仅 1.22×（P0-A 刻意禁缓存是主因之一）；在**不破坏重编译不变量**前提下，哪些编译可缓存、哪些必须每次真跑；预编译头/并行 make/对象级缓存/-O 分级（日常 -O0、nightly -O2）是否适用。
- replay/golden 层：按卡拆锁、工作树隔离每卡编译、产物内容寻址缓存、把"删→重生成→比 sha→还原"换成不可变工件目录；**golden 125s 能否多进程并行**（508 曾因共享锁+瞬时态失败，请给出确定性的隔离方案，而非"加 xdist"）。
- 测试层：受影响测试选择（impact/dep 指纹驱动，只跑变更相关）、快照、fixture 复用；fast/slow 两阶段之外是否需要第三层（冒烟/增量/全量）。
- gate 层：规则索引化、frontmatter 缓存失效键、避免全仓 rglob（499 曾 rglob 读 28588 文件全文）。
- 调度层（L2 实质推进）：task_queue 如何从"手工状态笔记本"长出**依赖感知的 worker 池/并行调度**——给数据结构、子命令、状态机、与 replay 锁/工作树隔离的接口粒度；明确 G-supervisor 默认 OFF、系统不自起 worker、接管决策归人的边界。

**C. 前沿调研（2025–2026 真实来源，每条带可访问链接+检索日期，区分"现在做/攒数据/等模型"）**
增量验证/构建缓存、test impact analysis & test selection、确定性并行测试隔离、content-addressed build、Temporal/Airflow/LangGraph 类 checkpoint 与任务调度、LLM agent harness 的可恢复执行；以及任何能把"错误率有上界的验证"做得更快的强度方法。
**（E 追加）** 再补检索与记忆方向：coding agent 的长期记忆/经验回放、retrieval-augmented verification / RAG 在高保证验证里的正确用法、从结构化源建知识图谱（含如何避免"节点堆成袋"）、memory 系统在多会话编码代理中的做法。明确拒绝会削弱 Oracle 的方案（如 LLM-as-judge 替代编译、检索结果直接当证据、同质辩论、在线改权重）。

**D. 批判与自攻击（最重要）**
- 红队审视你自己的每个优化：缓存是否会让 P0-A 重编译不变量退化成恒真比对（这正是 CCACHE_DISABLE 存在的原因）？并行是否引入新的非确定性/竞态，使"全绿"再次不可信？测试选择是否会漏判跨卡规则（548 已踩"diff 不许按卡裁剪"）？
- 每条优化必须回答：**它动没动"必须真跑外部 Oracle 才信"这条铁律**；动了的一律否决或给出可证明等价的护栏。
- 找不到更多可压项就明说"已到物理下限"，不要为显价值硬凑。

**E.（本轮追加）外置搜索 / 外置记忆 / 外置知识层的优化调研**
用户要这块。请把它当作与"速度"并列的第二条主线来设计：
- **外置检索增强（RAG）**：系统与建设者如何高效检索外部权威知识（C++ 标准、编译器/优化手册、cppreference、平台 ABI、已知问题库、历史 worklog/对抗报告），并把检索结果**只当"待证线索"**——检索到的任何断言，必须经本仓 Oracle/gate 独立复算、引用闭包可追溯，才允许入卡。调研在"结论必须外部 Oracle 验证"的硬约束下，RAG 的正确用法、检索粒度、引文可追溯、如何防止"检索到即当真"。
- **外置/项目长期记忆**：跨会话记忆、失败案例库（poison/mutation 的逃逸模式、假红根因、环境坑、双解释器/锁/tmp 等坑）、模型能力与成本档案、canary/回归基线。目标是做成**可机器查询、随批次累积、能指导下一轮选任务**的资产，而不是又一堆只读 .md 流水账。读现有 `MEMORY.md`、`docs/kernel/system_debt_ledger.md`、`cost_tracker.py`、`observability.py`、`metrics_collector.py`，指出它们离"可查询的长期记忆"还差什么。
- **与 knowledge_graph 对接**：现 kg 325 节点/291 边，但跨原子连通≈0（529 批判：标签袋不是概念图）。设计外部知识怎么入图才有**真实语义边**，而不是堆孤立节点；contrasts/contradicts 拆边、概念连通指标怎么从"候选"变"真信号"。
- **红线（务必在设计中显式遵守，不要给出越界方案）**：自动 KG 入库是战略冻结项（529 已否决）；外部检索结果不得绕过三分类直接变 verified；外部知识进 inference 仍需人签或登记独立基准（526 铁律）；外部检索"加速生产力"与"外部检索当证据"必须在架构上分两条通道。

【硬纪律】实测为准（每个论断挂文件:行号或实跑输出，区分已实现/设计/未实现）；不编数字、不猜版本；只读、产物全在 `_arch_v4/`、零污染自证；已知死路勿重复（pytest-xdist `-n auto` 全量不稳、`--dist loadgroup` 实测无效、ccache 仅 1.22×、给 .asm 加注释破 sha、.gitignore 行内注释失效、impact 数据源是 frontmatter dict 非 SQLite 禁用 CTE、SQLite WAL 需显式退避）。
【已知并发真相】poison 含真编译载荷，与 replay 并发会偶发假红；slow 两例（golden_lock_json/writer_selfcheck）共享 replay 锁，全量 -n auto 假红、串行全绿（苦力 559 正在加防护，你不必修，但设计并行方案时必须把这类共享可变状态列为一等约束）。

【最终交付】`_arch_v4/` 下：①性能画像（A，带原始计时）；②全局优化架构设计（B，苦力可照做规格）；③前沿调研与批判吸收（C，含检索/记忆）；④方案自攻击与风险（D）；⑤**外置搜索/外置记忆/外置知识层的优化设计（E：检索双通道、可查询长期记忆、kg 真语义边）**；⑥一张"现在做 / 攒数据 / 等模型变强"三档路线图，每条挂预期收益（可测，不许拍脑袋）、回退条件、机器验收判据。
读完源码先一句话回答两件事：**(1) 当前性能架构里最大的、且不削弱 Oracle 就能压掉的瓶颈是哪一个、为什么之前没压；(2) 外置知识/记忆现在是"用起来了"还是"又一堆只读文件"，最大的浪费在哪。**
