# 552 · 质变调研（四）：用广泛引用的成熟库替换手搓轮子 —— 依赖分级与核心代码优化地图

> 本轮目标（监工指定）：找被广泛验证、能直接用在阙疑元系统、让核心代码可优化的数据库/库/算法。结论先行：**不是什么都该上库**。fail-closed 门禁核心刻意保持零依赖（双解释器、可审计、少供应链面），重型/智能库放在离线分析与测试侧。检索 2026-09-16。

## 〇、一张表看清（库 → 替换哪个手搓轮子 → 分级）
| 库 | 成熟度 | 替换/强化的手搓部件 | 分级 |
|---|---|---|---|
| **Hypothesis** | Python PBT 事实标准 | task_queue 状态机测试、parser 差分、V-iso 蜕变生成 | **现在就用** |
| **SQLite recursive CTE** | 内置、SQL:1999、图灵完备 | impact_analysis / 依赖影响的手搓图遍历 | **现在就用（零新依赖）** |
| **syrupy** | 零依赖 pytest 快照插件 | golden_lock 之外的"输出结构漂移"锁 | **现在就用** |
| **scipy/statsmodels** | 科学计算基座 | 批次 J 共形二项上界（替代手搓 beta 分位） | **现在就用** |
| **DuckDB** | 嵌入式 OLAP，类 SQLite | mutation/metrics/成本/warn 的手搓 Python 聚合 | 选择性用（分析侧） |
| **Pydantic v2 (strict)** | Python 数据验证标准 | 离线工具/CLI/配置 schema、未声明键拒绝 | 选择性用（不进 gate 热路径） |
| **MAPIE / crepes** | scikit-learn-contrib 共形库 | RCPS/LTT 风险控制、Mondrian 分组共形实验 | 选择性用（离线校准） |
| **mutmut** | Python 变异测试主流 | 反过来测"自己工具的测试/规则质量" | 选择性用（定期元测试） |
| **Kùzu** | 嵌入式图库（图里的 SQLite） | knowledge_graph 的 Cypher 多跳 | 等规模（现 325 节点） |
| **tree-sitter / ast-grep / weggli / impactguard** | GitHub 级结构化解析 | 汇编/C++ 区间定位、调用影响 | 等需要（M3/静态 Oracle） |
| Nemo/Soufflé (Datalog) | 学术/工业推导引擎 | 大规模规则推导 | 等规模 |
| Fortuna(JAX)/TorchCP(PyTorch) | 共形/不确定库 | — | 不碰（不训练 NN，过重） |

## 一、现在就用（高杠杆、低风险、纯增量）

### 1. Hypothesis —— 一个库同时强化三处，本轮最高 ROI
Python property-based testing 事实标准；2026 指南明确它同时支持 **stateful / differential / metamorphic / targeted** 四种测试设计，并自动把失败 shrink 到最小复现。
- **Stateful（RuleBasedStateMachine）→ task_queue**：随机生成 claim/yield/touch/takeover/complete/heartbeat 的操作序列，每步后校验不变量（无双领、预算不超发、depth≤3、verify 不自证），自动发现状态机/并发漏洞并 shrink 出最短复现。比手写 62 个 pytest 例高一个维度——545 对抗是人手构造 3 个 L2 探针，Hypothesis 能自动枚举数百条操作路径。这是给 L2 调度层配的"变异器"。
- **Differential → 551 的 parser 差分（M8）**：同一批畸形 YAML 喂给 PyYAML 与零依赖解析器，断言判决一致；Hypothesis 自动生成多态/边界语法。
- **Metamorphic → V-iso 阴阳面**：自动生成 source/follow-up 对（删 anchor 行）并断言探针翻转，把 533 手做的阴面构造变成可批量生成的性质。
- 落地：纯测试依赖（requirements-dev），不碰正式代码路径，零门禁风险。

### 2. SQLite recursive CTE —— 零新依赖，把手搓图遍历换成声明式 SQL
recursive CTE 是 SQL:1999 标准、图灵完备，单源可达/传递闭包是其看家场景；SQLite 内置，当前 325 节点规模毫秒级。
- impact_analysis.py 的上游依赖遍历、knowledge_graph 的连通性/孤立判定/（未来）Dung grounded 扩展，都可用 `WITH RECURSIVE` 表达，减少手写图算法、正确性由引擎保证。
- 纪律：这是**重构减债**，不是加能力；改一处用回归锁（syrupy 快照输出）钉住前后结果一致。DuckDB v2 递归 CTE 快 40× 但现在不需要。

### 3. syrupy —— 零依赖快照，专治"数字悄悄漂移"
zero-dependency pytest 快照插件（MIT），断言结构化输出不变、给可读 diff、人审后才 `--snapshot-update`。
- 系统历史上多次出现规则数/warn 数/卡数文档失真、warn 32→54→59→136 无显形。把 gate 汇总、poison 覆盖、kg stats、mutation 拦截率、tool_integrity 的**结构化输出**锁快照，任何意外漂移立即变红并出 diff。
- 关键纪律（approval testing 通则）：**首次快照不自动通过，必须人审 approve**——与"golden accept 权唯人"完全同构。
- 与 golden_lock 互补不替代：syrupy 锁"输出结构稳定性"，golden_lock 管"warn 四桶分类签署"。

### 4. scipy/statsmodels —— 批次 J 共形门的统计底座
Clopper-Pearson 精确二项上界就是 beta 分布分位（`scipy.stats.beta.ppf`），用成熟实现替代手搓，避免边界错误（k=0、N 小）。scipy 是事实标准、可审计（公式透明）。

## 二、选择性用（用对地方，不进门禁核心热路径）

### 5. DuckDB —— 离线分析加速器（类 SQLite 的 OLAP）
嵌入式、列存、单文件、pip install、能直接对 JSON/Parquet/CSV 跑分析型 SQL。mutation 全量 1188 变体报告（data/mutation/*.json）、metrics、成本、warn 分类的多维聚合，现在是手搓 Python；DuckDB 可直接 `read_json_auto` 后用 SQL 切片（按算子/卡/规则/严重度）。**只做分析侧只读工具，不碰 gate/replay 核心数据**，避免给核心引依赖。

### 6. Pydantic v2 strict —— schema 即声明，unknown 字段即拒
Rust 内核（比 jsonschema 快 10-100×）、strict mode 不做隐式类型强转、`extra='forbid'` 天然挡"未声明键注入"（正是 M5/攻击面 A6）、自动生成 JSON Schema。
- **但不塞进 gate 核心 frontmatter 解析**：系统刻意保留零依赖解析器（workbuddy 无 PyYAML 也要能跑基础检查），引 pydantic-core（Rust 二进制）会破坏双解释器与可审计性。
- 正确位置：新离线工具/CLI 入参/任务队列配置/mutation 配置的校验；或作为 .venv 环境下 PyYAML 解析之后的**第二道可选 schema 层**（无则降级，fail-closed 不放宽）。

### 7. MAPIE / crepes —— 共形的"风险控制"与分组，离线实验用
- MAPIE（scikit-learn-contrib，引用最广）1.0 的 `mapie.risk_control` 实现 **RCPS/LTT**——当目标不是覆盖率而是给"逃逸率/假阴性"设硬上界时直接可用（549 的 conformal risk control）。
- crepes 极轻、model-agnostic、支持 **Mondrian 分组共形**（按 claim 类型/风险级分组校准）。
- 分工：**门禁核心的简单比例上界用 scipy 几行**（可读、可审、少供应链）；MAPIE/crepes 用于离线校准实验、分组共形、RCPS 调参，验证成熟后再把结论（不是依赖）固化进核心。
- Fortuna(JAX)/TorchCP(PyTorch) 不碰：系统不训练神经网络。

### 8. mutmut —— 用变异测试检验"验证器自身"
mutmut 3+（fork 模型，比 Java PIT 快，静态分析标 equivalent mutant）变异的是 **Python 源码**。用途是元层次：变异 gate_engine.py / task_queue.py / mutation_fuzz.py 自身，看现有 pytest 能否杀死——即"测试套件/规则到底有没有用"。定期离线跑，surviving mutant 指出测试盲区。与系统对 C++ 知识卡做的 mutation_fuzz 是两个层次（一个测工具代码，一个测知识证据）。

## 三、等规模 / 等需要（给明确触发条件，避免过度设计）
- **Kùzu**（嵌入式属性图库，Cypher、列存、MIT、单机数亿节点）：等知识节点上万、多跳模式查询成刚需、SQLite CTE 难维护时再迁；现 325 节点/291 边，迁移纯负担。
- **tree-sitter / ast-grep / weggli / impactguard**：tree-sitter 增量 CST、O(n)、S-expression 查询，比正则健壮；ast-grep 是其 Rust 结构化搜替；weggli 专注 C/C++、不需可构建代码；impactguard 用 tree-sitter 提取 C++ 调用点/影响面。触发条件：当**汇编/源码文本+正则成为误报源**（典型是 M3 区间降级——需要稳判"断言是否落在目标函数区间/全区间成立"）或要做 C++ 调用影响分析时引入。**铁律：静态结构模式只作 advice/warn，永不替代编译器/replay 这个主 Oracle**（编译器当判官是系统刻意的强设计，静态模式是弱证据）。
- **Datalog（Nemo/Soufflé）**："推导用 Datalog、查询用 SQL"；等规则/推导量大到 recursive CTE 难维护再评估。

## 四、依赖分层治理原则（本轮沉淀的架构纪律）
1. **两层依赖隔离**：
   - **core 门禁层**（gate_engine/replay/poison/frontmatter 解析）：零第三方依赖或仅标准库 +（.venv 的）PyYAML，公式可读、双解释器可跑、供应链面最小、fail-closed。
   - **分析/测试侧**（Hypothesis/syrupy/DuckDB/Pydantic/MAPIE/mutmut）：可自由引入成熟库，产物不进信任判定热路径。
2. 入库标准：广泛引用 + 活跃维护 + 轻量（优先零依赖/纯 Python/嵌入式）+ 有成熟替代退路；新增分 `requirements`（核心）与 `requirements-dev`（测试/分析）。
3. 引库不引信任：任何库产出的"结论"若要进 block 判定，仍须过机器可复核 + 毒样例 + 存量零误伤；库先在离线侧证明自己，结论固化进核心时优先沉淀"判据"而非"依赖"。
4. 与 tool_integrity 校验和衔接：分析侧工具变更不重钉核心校验和；核心工具被动过才走 --update 流程。

## 五、落地批次建议（接到 J/K 之后或并行）
- **批次 J（不变，最高）**：conformal_gate 用 scipy 上界 + RIPR reachability 诚实分类。
- **批次 T（测试加固，可与 J 并行，纯 dev 依赖、零正式代码风险）**：
  - Hypothesis stateful 接管 task_queue 状态机/并发测试；
  - Hypothesis differential 落地 parser 差分（551 M8）；
  - syrupy 锁 gate/poison/kg/mutation 关键输出快照；
  - mutmut 首次离线跑核心工具，出 surviving mutant 报告（只报告，先不改）。
- **批次 R（减债重构）**：impact_analysis/kg 图遍历改 recursive CTE，syrupy 钉前后等价。
- **批次 A（分析侧，可选）**：DuckDB 读 data/mutation + metrics 做 OLAP 看板；Pydantic 收编新工具入参。
- **等规模档**：Kùzu / tree-sitter / Datalog，触发条件见第三节。

## 六、给监工的一句话
这轮的结论很省心：**系统最该换的手搓轮子，全都能用"测试侧/分析侧"的成熟库解决，且不必动门禁核心的零依赖洁癖**——Hypothesis 给 L2 状态机和 parser 差分自动生成攻击（最该立刻上）、recursive CTE 减图遍历债、syrupy 堵数字漂移、scipy 托底共形；DuckDB/Pydantic/MAPIE 在离线侧提效；Kùzu/tree-sitter 明确等触发条件。核心代码因此能显著变强、变短、变可审计，而信任根依旧简单可控。
