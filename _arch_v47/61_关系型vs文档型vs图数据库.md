# 方向 61：关系型 vs 文档型 vs 图数据库

## 核心结论

1. **在阙疑的规模（全库节点数 47 知识卡 + 67 规则 + 452 判决 = 566 个节点，边数约 10³ 量级）下，结论是明确的：用 SQLite（关系型）+ 递归 CTE，不要用图数据库，也不要单独上文档数据库。** 依据是一份可复现的实测：SQLite 用递归 CTE 做图遍历，在 **10K 节点**规模下 1-hop 是 **0.80 ms**、2-hop **2.50 ms**、3-hop **6.50 ms**、4-hop **18.00 ms**（CongraphDB Benchmark 的 SQLite 引擎页）。阙疑的图比 10K 小约 **17.7 倍**，且遍历深度只有 2–3 跳。**在这个量级上，图数据库相对 SQLite 的性能优势在绝对时间上是"1 毫秒 vs 0.1 毫秒"的差别——而代价是多一个进程、一套查询语言、一份运维负担。**

2. **阙疑的三类数据里，只有一类真正是图状的；把三类混在一个图数据库里是错误建模。** 具体判定：(a) **知识卡 + 规则 + 二者的依赖关系** → 真图（需要闭包、环检测），但规模 114 个节点、深度 2–3 跳；(b) **判决账本** → **不是图，是线性链表**（每条只指向前一条的哈希），"沿链回溯"就是 `ORDER BY seq DESC` 的普通查询，**用图数据库处理它是把最简单的问题套上最复杂的工具**；(c) **证据指纹 / 判决快照 / 环境元数据** → 文档型（JSON blob），但这些字段**既不需要独立查询、也不需要跨文档事务**，作为 SQLite 的 TEXT 列存 JSON 完全够用。**结论：一个 SQLite 文件、三张表（cards / rules / ledger）+ 一张边表（deps），是这个系统的正确形态。**

3. **如果非要在 SQLite 之外再选一个，唯一可辩护的候选是 Kùzu（嵌入式属性图，Apache 2.0，C++ 原生），而不是 Neo4j 或 MongoDB**。理由与代价都很具体：(a) Kùzu 是**嵌入式**的（无独立服务进程），符合阙疑"单人 + 需嵌入"的约束；(b) 它是 **C++ 原生**实现，与阙疑的 C++ 方向同构；(c) 但代价是**多一个原生依赖**，且有报告指出 **Alpine Linux（musl）与 ARM 架构可能编译失败**（SitePoint 的 Kùzu vs SQLite 对比文，2026-09）——**这对"嵌入式方向"的阙疑是实质风险，因为嵌入式目标平台常常正是 ARM**。Neo4j 需要 JVM 与独立服务进程（企业版报价被第三方文章列为 **$15K+/年**），MongoDB 的跨文档事务与 append-only 语义匹配度差，**两者都不应考虑**。

---

## 精确数字与案例

### 一、可复现的实测：同一份 Cypher 查询在 Neo4j 与 PostgreSQL+AGE 上的差异

来源：baem1n.dev《Neo4j vs Apache AGE Benchmark — Same Cypher, Same Data, Different Results》（2026-04-03）。这是本次调研中**唯一一份公开了完整环境、数据集、方法与逐条数字的对比**，且**数据集规模（1,000 节点 / 2,000 边）恰好与阙疑同量级**。

**环境（逐字）**：Neo4j 5（Docker）vs PostgreSQL 18 + Apache AGE 1.7.0（Docker）；两端同一台机器、默认 Docker 容器；方法学为 *"3 warmup runs, then N iterations, reporting p50 (median)"*，`iterations=50`。

**数据集**：1,000 个 `:Node {idx, name}`，2,000 条 `:LINK` 边。

| 测试用例 | Neo4j 5 (p50) | AGE 1.7.0 (p50) | 胜出方 | 倍数 |
|---|---|---|---|---|
| Point lookup（按属性 MATCH） | 2.0 ms | **0.9 ms** | AGE | 2.2× |
| 1-hop traversal | 1.7 ms | **1.0 ms** | AGE | 1.7× |
| **3-hop traversal** | **1.7 ms** | 25.8 ms | Neo4j | **14.9×** |
| **6-hop traversal** | **2.4 ms** | 27.7 ms | Neo4j | **11.6×** |
| Full count（聚合） | 1.5 ms | **1.0 ms** | AGE | 1.5× |
| Single CREATE | 3.3 ms | **0.9 ms** | AGE | 3.7× |
| Batch CREATE（100 节点） | 2.6 ms | **1.1 ms** | AGE | 2.4× |
| Schema introspection | 16.6 ms | **7.9 ms** | AGE | 2.1× |

**一个极其重要的反转**（同一篇文章的"逃生通道"实验）：AGE 提供 `traverse()`（内部走 `WITH RECURSIVE`），在**同一张 1K 节点图上**把 6-hop 从 **28.2 ms 降到 1.4 ms（19× 提速）**，**反超 Neo4j 的 2.4 ms 达 1.7 倍**。原文逐字：*"AGE's `traverse()` (WITH RECURSIVE CTE) reduces 6-hop traversal from 28.2ms to 1.4ms — 19x faster — beating Neo4j's 2.4ms by 1.7x."*、*"With traverse(), AGE beats Neo4j even on deep traversals."*

**对阙疑的直接推论**：这篇 benchmark 证明**"图数据库在深遍历上快 11–15 倍"这个结论依赖于查询怎么写**。只要把递归查询写对（用 CTE 而不是逐层 JOIN），关系型数据库在小图上就追平甚至反超。**阙疑的深度是 2–3 跳，落在 AGE 在 1-hop 就更快（1.0 vs 1.7 ms）的区间。所以"我们需要图数据库来做依赖闭包"这个论证在本规模上不成立。**

**该文章的结论表（逐字）**：

| 工作负载 | 推荐 | 理由 |
|---|---|---|
| RAG（1–2 跳 + CRUD） | **AGE** | Point lookup 快 2.2×，CREATE 快 3.7× |
| 社交网络分析（3–6 跳） | **Neo4j** | 深遍历快 11–15× |
| 成本优化 | **AGE** | $0 vs $15K+/年 |
| 已有 PostgreSQL 基础设施 | **AGE** | 只需装扩展 |
| 企业支持 | **Neo4j** | SLA、7×24 支持 |

（**注意**：$15K+/年这个 Neo4j 企业版报价来自该第三方博客，我**未从 Neo4j 官方定价页核验**。）

### 二、SQLite 的图遍历实测（这是阙疑最该看的表）

来源：CongraphDB Benchmark 的 SQLite 引擎页（congraph-ai.github.io/congraphdb-benchmark/engines/sqlite/，2026-09-18 抓取）。该 benchmark 把 SQLite 与原生图引擎（含 CongraphDB）在三个规模上对比。**注意这是厂商（CongraphDB）自建 benchmark，其对比对象是自己的产品，存在利益冲突；但 SQLite 的绝对数字（遍历 ms、内存 MB）仍有参考价值。**

**SQLite + 递归 CTE 的综合得分：65.8/100，第 4 名**

| 指标 | 数值 | 排名 |
|---|---|---|
| 摄入 | 45,000 节点/秒（10K 规模） | 第 5 |
| 遍历 | **8.5 ms 平均（4-hop）** | 第 5 |
| PageRank | 5.5 s（10 次迭代） | 第 4 |
| 内存 | **85 MB**（10K 规模） | 第 3 |

**遍历延迟随规模与跳数的完整表（单位 ms）**：

| 跳数 | Small (10K) | Medium (100K) | Large (1M) |
|---|---|---|---|
| 1-hop | **0.80** | 1.20 | 2.50 |
| 2-hop | **2.50** | 4.50 | 8.50 |
| 3-hop | **6.50** | 12.50 | 28.00 |
| 4-hop | **18.00** | 35.00 | N/A |
| 5-hop | N/A | N/A | N/A |

**内存随规模**：Small (10K) **85 MB**（比 CongraphDB 高 89%）、Medium (100K) 680 MB（+77%）、Large (1M) 5,200 MB（+60%）。

**该页面明确列出的 SQLite 弱点（逐字）**：
- *"No Native Graph - Recursive CTEs are slow"*
- *"Traversal Limits - 4-hop max before timeouts"*
- *"Performance - 180% slower than CongraphDB"*
- *"Complexity: SQLite requires 10+ lines vs 2 lines for Cypher"*

**"什么时候该用 SQLite"（逐字）**：*"Existing SQLite App"*、*"Simple Graph Queries - 1-2 hop traversals only"*、*"SQL Preference"*、*"Mixed Workload - Need both relational and graph queries"*。**"什么时候该避免"**：*"Performance Critical"*、*"Deep Traversals - 4+ hops are very slow"*、*"Graph-First"*。

**对阙疑的判定**：阙疑落在"该用 SQLite"这一栏的**全部四个条件**里——已有关系型数据（账本）、只需 1–2 跳（依赖闭包实际深度）、需要混合负载（账本查询 + 依赖闭包 + 统计聚合）、以及最重要的一条：**阙疑的绝对延迟预算是毫秒级不是微秒级**（判决是离线复算的，不是在线服务的）。**"180% slower"听起来很吓人，但基数是从 3 ms 到 8.5 ms——对一个单机离线复算器，这个差别不构成任何工程问题。**

**关于"4-hop 超时"这条**：它指的是该 benchmark 在大规模（1M）数据上的表现。阙疑 566 个节点、2–3 跳，**离这个边界有 3 个数量级的余量**。

### 三、SQLite 的适用边界：另一个独立来源给出的阈值

来源：SitePoint《Embedded Graphs in Node.js: Kùzu vs SQLite Recursive CTEs》（2026-09 抓取）。该文是架构对比而非 benchmark，**它明确声明没有实测数字**（8 节点数据集上两者都是"亚毫秒级"，差异可忽略）。但它给出了一个**理论阈值**，逐字：

> *"for graphs under roughly 5,000 nodes with traversals of three hops or less, SQLite's recursive CTEs work fine. Beyond that, benchmark your own dataset; the crossover point depends on fan-out, depth, and query patterns."*

以及理论复杂度说明：在平均扇出（fan-out）为 **10**、深度为 **6** 的图上，SQLite 递归 CTE 最坏需要 **O(fan-out^depth)** 次 B 树索引探测；Kùzu 用邻接表存储"从结构上避免了这一成本"。

**阙疑对照**：节点 566 < 5,000 ✓，跳数 2–3 ≤ 3 ✓。**两个条件都满足，且有 8.8 倍的节点余量。**

该文的环境数字（可用于复现）：Node.js **24.0.0+**、TypeScript **5.x**、`kuzu` **0.10.0**、`better-sqlite3` **11.0.0**、SQLite 的 `WITH RECURSIVE` 自 **3.8.3（2014）** 起可用；Kùzu 许可 **Apache 2.0**；原生编译在 macOS 需 Xcode CLI tools、Debian/Ubuntu 需 `build-essential`、Windows 需 Visual Studio Build Tools。**关键风险逐字**：Kùzu 原生插件在主流平台可编译，但 *"Alpine Linux musl 构建和 ARM 架构可能编译失败"*（该文建议查 Kùzu 的 GitHub issue tracker）。

**该文的最终建议（逐字）**：

> *"Start with SQLite if graph queries are a small part of your workload today. Migrate to Kùzu when your CTE cycle-detection code becomes a maintenance burden or your traversal depth outgrows what B-tree index probes can handle efficiently."*

**这句话可以直接作为阙疑的选型理由**：阙疑的图查询是**工作负载的一小部分**（大部分是账本读写与统计），所以"从 SQLite 开始"是对的。

### 四、三类数据的建模对比（这是本方向的核心交付物）

| 维度 | 知识卡 + 规则（依赖图） | 判决账本（哈希链） | 证据 / 快照（blob） |
|---|---|---|---|
| **数据形态** | 真图（有向，可能有环） | **线性链表**（每节点最多一个后继、一个前驱） | 文档（嵌套 JSON） |
| **规模** | 47 卡 + 67 规则 = **114 节点** | **452 节点、451 条边** | 452 个 blob |
| **查询模式** | 依赖闭包（传递闭包）、环检测、可达性 | 顺序扫描、范围查询（`seq <= k`）、逐条哈希校验 | 按主键取整块、偶尔按字段过滤 |
| **关系型建模** | `deps(from_id, to_id, kind)` + 递归 CTE | `ledger(seq PK, prev_hash, payload_json, hash)` | 作为 `ledger` 的一个 TEXT 列 |
| **文档型建模** | 卡片文档内嵌 `deps` 数组（但**跨文档闭包查询会退化**） | 每个判决一个文档，链式 `prev` 字段（**无法原子地保证链一致**） | 天然合适 |
| **图数据库建模** | 天然合适（`(Card)-[:DEPENDS_ON]->(Rule)`） | **强行建模**——线性链在图里是退化的图 | 作为节点属性 |
| **该用哪个** | 关系型（递归 CTE）**够用** | **关系型（唯一合理选择）** | 关系型的 TEXT 列 |
| **不用图数据库的理由** | 114 节点 / 2–3 跳，SQLite 3-hop 只需 **6.5 ms**（10K 规模） | 线性链在图数据库里没有任何优势 | 不涉及图 |

**三条关键判定，逐条给出理由**：

**(1) 判决账本不是图，是链表。** 这一点必须写清楚，因为"哈希链 + Merkle 树"的表述容易让人误以为需要图数据库。**哈希链的"沿链回溯"是一个 `ORDER BY seq DESC LIMIT k` 查询**，任何关系型数据库都能用 B 树索引做到 O(log n + k)。而 Merkle 树**根本不需要存在数据库里**——它的结构由叶子数唯一确定（RFC 6962 §2.1，见方向 56），**只需要存"树大小 + 根哈希"两个字段，树本身在需要时由 452 个叶子哈希现算**（成本约 0.53 ms，见方向 56 的换算）。**结论：账本在数据库里只需要一张两列宽的表。**

**(2) 文档型的唯一优势（schema 灵活性）在阙疑这里是负收益。** 阙疑的判决结构是**固定的四态 + 固定的证据字段**——这正是关系型最擅长的情况。文档型的"灵活 schema"会带来一个真实风险：**不同版本的判决记录结构漂移，导致 452 条账本的字段不可比**——而阙疑的整个卖点是"可复算"，结构漂移会直接摧毁可复算性。**方向 64（append-only 存储设计）会进一步讨论"schema 演进与 append-only 的冲突"。**

**(3) 图数据库唯一真正带来价值的能力是"变长路径 + 自动环检测"，而这两件事在 SQLite 里都可控。** SitePoint 的文章提到 SQLite 需要**手动循环检测**（用 sentinel-padded `INSTR` 检查路径数组），并指出该方法把每次递归行的工作量从 `O(depth × path_length)` 降到 `O(path_length)`。**这是一个 10 行左右的 SQL 技巧，不是架构决策。** 而 Kùzu 的"自动环检测"带来的收益，在 566 节点规模上不足以抵消多一个原生依赖的成本（尤其考虑到 ARM/musl 编译风险）。

### 五、规模阈值：什么时候该重新评估

综合本方向的三个数据源，给出阙疑的**重新评估触发条件**（这些是给未来的自己设的规则，不是当前决策）：

| 触发条件 | 阈值 | 依据 |
|---|---|---|
| 节点数超过 | **5,000** | SitePoint：*"under roughly 5,000 nodes with traversals of three hops or less, SQLite's recursive CTEs work fine"* |
| 遍历深度超过 | **3 跳** | 同上；且 CongraphDB 表显示 4-hop 在 10K 规模已到 18 ms |
| 单次遍历延迟超过 | **100 ms**（离线复算的可接受上界，阙疑自定） | 无外部依据，是工程判断 |
| 内存占用超过 | **500 MB** | CongraphDB 显示 SQLite 在 100K 节点占 680 MB；阙疑目标机器可能资源受限 |
| 出现需要图算法的需求 | PageRank / 社区发现 / 最短路径 | 这些在 SQLite 里要自己实现（CongraphDB 页面显示 SQLite 的 PageRank 比原生实现慢 **80%**） |

**按阙疑当前增速估算**：从 452 条到 5,000 条需要约 **11 倍**增长。若每天新增 2 条判决，需要约 **6.2 年**。**也就是说，如果阙疑按当前节奏发展，这个阈值在 2028 年毕业前不会被触及。**

---

## 对阙疑的 3 条具体行动

1. **把存储层固化为单个 SQLite 文件 + 四张表，并写一份 `schema.sql` 作为唯一权威定义**。建议 schema（**请按你的实际字段调整，这里给的是结构骨架**）：

```sql
PRAGMA journal_mode = WAL;      -- 见方向 62
PRAGMA foreign_keys = ON;

CREATE TABLE cards (
  card_id      TEXT PRIMARY KEY,
  state        TEXT NOT NULL CHECK (state IN ('verified','red_team','draft')),
  title        TEXT NOT NULL,
  body_json    TEXT NOT NULL,       -- 证据/快照作为文档型 blob
  created_seq  INTEGER NOT NULL     -- 关联到账本序号
);

CREATE TABLE rules (
  rule_id      TEXT PRIMARY KEY,
  severity     TEXT NOT NULL CHECK (severity IN ('block','warn','advice')),
  spec_json    TEXT NOT NULL
);

-- 唯一的"真图"：依赖边
CREATE TABLE deps (
  from_id  TEXT NOT NULL,           -- 'card:C012' 或 'rule:R031'
  to_id    TEXT NOT NULL,
  kind     TEXT NOT NULL,           -- 'depends_on' | 'protects' | 'supersedes'
  PRIMARY KEY (from_id, to_id, kind)
);
CREATE INDEX idx_deps_to ON deps(to_id);

-- 账本：链表，不是图
CREATE TABLE ledger (
  seq        INTEGER PRIMARY KEY,
  prev_hash  BLOB NOT NULL,         -- 32 字节
  self_hash  BLOB NOT NULL UNIQUE,  -- 32 字节
  payload_json TEXT NOT NULL,
  tree_size  INTEGER NOT NULL,      -- Merkle checkpoint 的树大小
  root_hash  BLOB                   -- Merkle checkpoint 的根（可为 NULL）
);
```

**关键点**：(a) `deps` 的 `from_id`/`to_id` 用带前缀的 TEXT（`card:` / `rule:`）实现多态，避免建两张边表；(b) `ledger` **不存 Merkle 树的内部节点**，只存 `tree_size` 与 `root_hash`，内部节点按 RFC 6962 现算；(c) `cards.body_json` 承担文档型角色，但**只作为不参与查询的载荷**——任何需要过滤的字段都应提升为独立列。**时间点：2026-11 前**（这是数据结构冻结的前提）。

2. **写一份 `research/18_storage_choice.md`（2–3 页），把"为什么不用图数据库"写成有数字的论证，时间点 2027-04 前**。必须包含：(a) 阙疑的真实规模表（节点数、边数、最大跳数、每次遍历的目标延迟）；(b) 引用 CongraphDB 的 SQLite 遍历表（1-hop **0.80 ms** / 2-hop **2.50 ms** / 3-hop **6.50 ms** @ 10K 节点）并说明阙疑规模小 17.7 倍；(c) 引用 SitePoint 的阈值 *"under roughly 5,000 nodes with traversals of three hops or less"*；(d) 引用 baem1n.dev 的"反转点"（AGE 的 `traverse()` 把 6-hop 从 28.2 ms 降到 1.4 ms，反超 Neo4j 1.7×），用来说明**"图数据库更快"这一结论依赖于查询写法**；(e) 一段结论逐字建议："本系统的数据规模（566 节点、2–3 跳）低于文献给出的 SQLite 适用阈值（5,000 节点、3 跳），且图查询只占工作负载的一小部分。因此本系统采用 SQLite + 递归 CTE，不引入图数据库。若未来节点数超过 5,000 或遍历深度超过 3 跳，首选迁移目标为 Kùzu（嵌入式、Apache 2.0、C++ 原生），而非 Neo4j（需 JVM 与独立服务进程）。"

3. **加一个"存储层压力测试"脚本，用合成数据把阈值验证出来，而不是只引用文献，时间点 2027-06 前**。具体做法：生成 5 个规模的合成依赖图（**500 / 1,000 / 2,000 / 5,000 / 10,000 节点**，扇出按阙疑实际值设定），对每个规模测三件事：(a) 依赖闭包（1/2/3 跳）的 p50 与 p99 延迟；(b) 全量账本校验（452→10,000 条的哈希链重算）的耗时；(c) 数据库文件大小与峰值内存。把结果写成 `exp/storage_scaling.csv`，字段 `n_nodes, n_edges, max_hop, p50_ms, p99_ms, db_size_mb, peak_mem_mb`。**这个脚本的价值在于：它让"我们选了 SQLite"从文献论证变成自测论证**——而 E&D Track 的审稿人对"自己测了"的评价远高于"引用了别人测的"。**同时它给出了那张阈值表的自测版本，是论文附录里很有说服力的一张表。**

---

## 盲区（诚实标注）

- **CongraphDB Benchmark 是厂商自建 benchmark，对比对象包含其自家产品 CongraphDB**。因此它给出的"SQLite 比 CongraphDB 慢 180%"这类**相对**数字有利益冲突。我在正文里只使用了 SQLite 的**绝对**数字（遍历 ms、内存 MB、摄入 节点/秒），这些相对可信，但**仍应视为二手**——阙疑若引用，应当自己按同样的 schema 复现一次。
- **baem1n.dev 的 benchmark 没有公布硬件规格**（只说 "same machine, Docker container"，用默认 Docker 配置）。该文自己列出了 "Benchmark Limitations"：*"该测试仅在 1K 节点小图上进行、使用默认 Docker 配置、且未涵盖向量搜索"*。**所以那 8 个数字的绝对值不可跨机器比较，只有倍数关系（11–15×）有意义。**
- **inferensys.com 的 Kùzu vs DuckDB 数字我判断不可用**。该页给出的 Kuzu "3-Hop ~12ms vs DuckDB recursive CTE ~850ms"，但同一页在"Storage Footprint (Library)"一栏写 Kuzu **~15 MB**，而在下面的"Embedded Deployment Size"一栏写 Kuzu **< 5MB**——**同一页面内部自相矛盾**。该页还有大量营销内容（"Limited slots / Get a Free AI Consultation"）。**我在正文里完全没有采用它的数字**，仅在此说明为什么不采用。
- **Kùzu 的官方论文我没拿到**。OpenReview 的 PDF（openreview.net/pdf?id=Eg3MthXzeT，标题 *"Kùzu: Graph Learning Applications Need a Modern Graph..."*）下载后解析为空（可能是非 PDF 响应或被拦截），所以**Kùzu 的架构细节（CSR、列式存储、向量化执行的具体设计）与官方性能数字我未核验**。Kùzu 的版本号 0.10.0 来自 SitePoint 文章的 package.json，**不是官方最新版**。
- **"Which Category Is Better: Benchmarking Relational and Graph Database Management Systems"（Springer, *Data Science and Engineering*, 2019-11-11）我三次尝试都没能拿到正文**：Springer 页面被 Cloudflare "Client Challenge" 拦截，ResearchGate 的 PDF 链接返回 20 KB 的非 PDF 内容，scispace 页面要求人机验证。**该论文的具体数字（RDBMS 与 GDBMS 在同一 benchmark 上的执行时间对比）我完全没有核验。** 这是本方向最大的一个缺口——如果阙疑要在论文里做"关系型 vs 图"的定量论证，这篇 2019 年的统一 benchmark 是绕不开的引用，**必须自己补上**。
- **Neo4j 企业版 $15K+/年的报价来自第三方博客，未核验官方定价页**。Neo4j 有社区版（免费，但仍有 GPL 许可与服务进程要求），这个数字若进论文会被审稿人质疑。
- **"4-hop max before timeouts"这个说法我没有理解清楚**。CongraphDB 页面的遍历表里 4-hop 在 Small/Medium 有数字（18.00 / 35.00 ms），只有 Large 是 N/A。**"timeout"的阈值（多少毫秒算超时）未说明**。所以我在正文里把它表述为"指大规模数据上的表现"，这是推断不是原文。
- **SQLite 的 85 MB 内存数字（10K 节点）与阙疑的场景不直接可比**：那个 benchmark 的 schema 是通用 `nodes/edges` 双表 + JSON 属性（见其页面给出的 `CREATE TABLE` 语句），而阙疑的 schema 更紧凑（无 `properties_json` 用于图的节点）。**阙疑实际内存占用应当更低，但具体低多少需要自测（这正是行动 3 要测的）。**
- **样本偏差**：本方向的中文搜索结果（CSDN《从SQL到Cypher：一个后端工程师的Neo4j避坑实战笔记》系列出现三次不同 URL 的同一内容、百度文库、raybyte.cn 的 SQLite 递归 CTE 系列）**有明显的 AI 批量生成特征**（同一篇文章在 blog.csdn.net / wenku.csdn.net 两个域下以几乎相同标题重复出现，且"阅读量 0"）。我完全没有采用这些来源的数字。**这也再次提醒：阙疑自己的 `_arch_v46/` 里那批 AI 生成文档，在 Pangram 视角下属于同一类。**
- **一个未验证的关键假设**：我在核心结论里说"阙疑的依赖闭包深度只有 2–3 跳"。**这个数字我是推断的，不是查证的**——我没有看过阙疑的实际规则依赖图。**如果实际依赖链有 10 跳，那么整节结论需要重写**（10 跳在 SQLite 上按 O(fan-out^depth) 会显著变慢）。**阙疑必须先测出自己的实际最大深度和平均扇出，再决定存储方案**——这是行动 3 的前置条件。

---

## 来源

1. Neo4j vs Apache AGE Benchmark — Same Cypher, Same Data, Different Results — https://baem1n.dev/en/posts/neo4j-vs-age-benchmark/ — 逐字引文：环境 "Neo4j 5 (Docker)" vs "PostgreSQL 18 + AGE 1.7.0 (Docker)"；数据集 1,000 nodes / 2,000 edges；方法 "3 warmup runs, then N iterations, reporting p50 (median)"，`iterations=50`；"AGE wins 6 out of 8 tests (point lookup 2.2x, CREATE 3.7x, schema 2.1x faster). Neo4j wins deep traversals by 11–15x (3+ hops)."；"AGE's `traverse()` (WITH RECURSIVE CTE) reduces 6-hop traversal from 28.2ms to 1.4ms — 19x faster — beating Neo4j's 2.4ms by 1.7x."；"Most LLM/RAG applications need only 1–2 hops."；"$0 vs $15K+/year" — baem1n.dev — 2026-04-03（**硬件规格未公布**）
2. CongraphDB Benchmark — SQLite + Recursive CTEs — https://congraph-ai.github.io/congraphdb-benchmark/engines/sqlite/ — 逐字/表格：Overall Score **65.8/100 - 4th Place**；Ingestion 45K nodes/s（Small 10K）；Traversal **8.5ms avg (4-hop)**；Memory **85 MB**（Small 10K，+89% vs CongraphDB）；遍历表 1-hop 0.80/1.20/2.50 ms、2-hop 2.50/4.50/8.50、3-hop 6.50/12.50/28.00、4-hop 18.00/35.00/N/A（Small/Medium/Large）；"Traversal Limits - 4-hop max before timeouts"；"Performance - 180% slower than CongraphDB"；"Complexity: SQLite requires 10+ lines vs 2 lines for Cypher"；PageRank 慢 80% — CongraphDB 项目 — 2026-09-18 抓取（**厂商自建 benchmark，有利益冲突**）
3. Embedded Graphs in Node.js: Kùzu vs SQLite Recursive CTEs — https://www.sitepoint.com/embedded-graphs-nodejs-kuzu-sqlite-recursive-ctes/ — 逐字引文："for graphs under roughly 5,000 nodes with traversals of three hops or less, SQLite's recursive CTEs work fine. Beyond that, benchmark your own dataset; the crossover point depends on fan-out, depth, and query patterns."；"On the 8-node seed dataset used here, both approaches return results in sub-millisecond timescales, and the difference is negligible."；"Start with SQLite if graph queries are a small part of your workload today. Migrate to Kùzu when your CTE cycle-detection code becomes a maintenance burden or your traversal depth outgrows what B-tree index probes can handle efficiently."；Kùzu 0.10.0 / better-sqlite3 11.0.0 / Node.js 24.0.0+ / SQLite `WITH RECURSIVE` 自 3.8.3（2014）；Kùzu 许可 Apache 2.0；Alpine Linux musl 与 ARM 可能编译失败 — SitePoint — 2026-09 抓取
4. Which Category Is Better: Benchmarking Relational and Graph Database Management Systems — https://link.springer.com/article/10.1007/s41019-019-00110-3（*Data Science and Engineering*）与 https://www.researchgate.net/publication/337169617 — 摘要逐字（仅摘要可得）："Over decades, relational database management systems (RDBMSs) have been the first choice to manage data. Recently..."；"we first extend a unified benchmark for RDBMSs and GDBMSs over the same..." — Springer — 2019-11-11（**正文三次尝试均未获取**）
5. Which Category Is Better: Benchmarking the RDBMSs and GDBMSs（会议版）— https://link.springer.com/chapter/10.1007/978-3-030-26075-0_16 — 逐字："In this paper, we propose a unified benchmark for RDBMSs and GDBMSs, to evaluate them under the same..." — Springer — 2019-07-17
6. Query Performance Comparison of PostgreSQL vs. Neo4j. A Basic Approach on TPC-H — https://ieeexplore.ieee.org/document/10722626 — 逐字："In this paper, we present a module for converting the TPC-H benchmark database from PostgreSQL to Neo4j, and we built a set of..." — IEEE — 2024-09-20（**正文未获取**）
7. Kùzu: Graph Learning Applications Need a Modern Graph DBMS — https://openreview.net/pdf?id=Eg3MthXzeT — 逐字（仅搜索摘要）："We present Kùzu, an open-sourced graph DBMS that aims to fill this gap. Kùzu is an embeddable system that runs as part of users'..." — OpenReview（**PDF 下载后解析为空，正文未获取**）
8. Kuzu Documentation — https://kuzudb.github.io/docs/ — 逐字："Because Kuzu is an embedded database, it runs within your application process, making it easy to set up and use..."；"Kuzu is a state-of-the-art graph DBMS that came out of state-of-the-art academic research" — KuzuDB — 页面标注 2025-10-10
9. kuzudb/kuzu（GitHub）— https://github.com/kuzudb/kuzu — "Kuzu is an embedded graph database built for query speed and scalability. Kuzu is optimized for handling complex analytical..." — KuzuDB — 抓取于 2026-09-29
10. Kuzu vs DuckDB: Embedded Graph Memory for Local Agents — https://inferensys.com/differences/knowledge-graph-and-semantic-memory-systems/long-term-agent-memory-frameworks/kuzu-vs-duckdb-embedded-graph-memory-for-local-agents — 逐字（**该页内部自相矛盾：Kuzu 库体积一处写 "~15 MB"、另一处写 "< 5MB"；含营销内容；本方向未采用其任何数字**）："Multi-hop Traversal (3-Hop) ~12ms / ~850ms (Recursive CTE)" — Inference Systems — 抓取于 2026-09-29
11. LDBC Social Network Benchmark (LDBC SNB) — https://ldbcouncil.org/benchmarks/snb/ 与 https://ldbcouncil.org/ldbc_snb_docs/ — "The Social Network Benchmark (SNB) suite defines graph workloads..."；包含 Interactive Complex Reads、BI reads 等查询类别 — LDBC Graph Data Council — 抓取于 2026-09-29（**具体吞吐/延迟数字未获取**）
12. Understanding Graph Databases: A Comprehensive Tutorial and Survey — https://arxiv.org/html/2411.09999v1 — "This tutorial is curated as a one-stop shop for understanding graph databases, as it emphasizes the foundations of..." — arXiv — 2024-11-18（**未打开正文**）
13. Graph and Relational Database Comparison — https://learn.microsoft.com/en-us/fabric/graph/graph-relational-databases — "Graph databases excel at modeling and analyzing highly connected data, such as social networks, knowledge..." — Microsoft Learn — 2026-06-02（**未打开正文**）
14. How to Build an Audit Log System with MongoDB — https://oneuptime.com/blog/post/2026-03-31-mongodb-how-to-build-an-audit-log-system-with-mongodb/view — "Learn how to build an immutable audit log system with MongoDB for compliance and security, using capped..." — oneuptime.com — 2026-03-31（**未打开正文；仅作"文档型做账本"存在性证据**）
15. MongoDB Schema Flexibility: Benefits & Tradeoffs — https://learn.programmingline.com/learn/mongodb/mongodb-schema-flexibility — "Learn how MongoDB's flexible document schema works internally, when it helps, when it hurts, and how to add..." — ProgrammingLine — 2026-08-04（**未打开正文**）
16. 从SQL到Cypher：一个后端工程师的Neo4j避坑实战笔记 — https://blog.csdn.net/weixin_26800111/article/details/160464802 与 https://wenku.csdn.net/column/tg38ksexm89 — "本文分享了后端工程师从SQL转向Neo4j的实战经验，重点对比..."（**同一内容在多个域名下以近乎相同标题重复出现、阅读量 0，AI 批量生成特征明显；本方向未采用其任何数字，仅作反面例证**） — CSDN — 2026-08-18 / 2026-04-20
