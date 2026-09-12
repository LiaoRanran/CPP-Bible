# 资料研究第四十七轮：数据库查询执行——火山模型、向量化执行、查询优化器、代价模型、Join 算法、并行执行

> 2026-09-11，底层工程资料研究员。主题：查询处理流水线（SQL → 语法树 → 逻辑计划 → 物理计划 → 执行）、三大执行模型（迭代器/火山、物化、向量化批处理）、火山模型的由来（Graefe 1994 论文）与代价（每行虚函数调用、解释器开销 50-80%）、向量化执行如何让 SIMD/缓存友好（ClickHouse/OceanBase 实践）、Join 算法谱系（嵌套循环/哈希/归并排序）、查询优化器（规则重写 + 代价模型、基数估计）、并行查询执行（exchange 算子、数据分片）。
> 检索方式：general_search + CMU 15-445 Lecture #13 Query Processing（课程权威）+ ACM Volcano 论文（Graefe 1994）+ ClickHouse 向量化执行 + OceanBase 向量化引擎 + TUM 缓存感知执行模型 + neo01 PostgreSQL 火山模型 + CSDN OLAP 核心技术 + SIGMOD 2025 Contest 并行引擎。
> **数据库域第二轮**。第一轮：22 SQLite 架构（查询处理初览）。与 34 存储引擎、55 GC（物化内存）、65 轮（待写）事务衔接。

---

## 一、查询处理流水线

```
SQL 文本 → 词法/语法分析（AST）→ 绑定/语义分析
  → 逻辑计划（关系代数树：scan/join/filter/aggregate）
  → 查询优化（规则重写 + 代价估算选物理算子）
  → 物理计划（hash join？index scan？并行？）
  → 执行（火山/向量化/编译执行）
```

**优化器是数据库的"编译器后端"**（衔接编译器域）：SQL 是声明式语言，优化器负责"决定怎么算"——与 C++ 编译器把抽象语法翻译成高效机器码同构。

## 二、三大执行模型

### 1. 迭代器模型（Volcano/火山）

```cpp
class Operator { virtual Row next() = 0; };  // 每个算子一个 next()
// Filter → 调 Join → 调 Scan，逐行拉取（pull）
```

- Goetz Graefe 1994 论文提出（"Encapsulation of Parallelism in the Volcano Query Processing System"，ACM SIGMOD）
- 优点：算子可组合（任意算子叠起来就是新计划）、内存可控（流水线式，不物化中间结果）
- 缺点：**每行一次虚函数调用链**——解释器开销占 CPU 时间 50-80%（火山论文作者自己测的）→ 现代硬件上性能天花板明显

### 2. 物化模型（Materialization）

- 每算子输出**整个结果集**（存内存/临时表），下个算子整体处理
- 优点：简单、利于迭代式算法；缺点：中间结果可能巨大（OOM 风险）
- 用途：OLAP 部分场景、单算子处理（排序等需要全量输入的算子天然物化）

### 3. 向量化/批处理模型（Vectorized）

```cpp
// 每算子一次处理一批（1024~4096 行），一列一列紧循环
void Filter::next() { batch = child->next(); out = predicate(batch.col); }
```

- 保留 pull 结构但**批量返回**：内部把循环"拉进算子"（loop fusion）
- 收益：
  - 摊薄解释器/虚调用开销（ClickHouse 量化）
  - 列式处理 → **编译器能发 SIMD**（衔接 20 轮 SIMD）
  - 内存访问连续 → 缓存友好（衔接 50 轮微架构）
- 代表：ClickHouse、DuckDB、OceanBase 向量化引擎、Databend

### 4. 编译执行（Code Generation）

- 把查询**即时编译成机器码**（LLVM），消除解释器完全（HyPer/Umbra 路线）
- 向量化 vs 编译：向量化=批量解释（简单、可移植）；编译=逐查询生成代码（最极致但复杂、编译时间）

- **来源**：CMU 15-445 + ClickHouse + JZLeetCode
- **可信度**：S

---

## 三、Join 算法谱系（性能的决胜点）

| 算法 | 思路 | 适用 | 复杂度 |
|---|---|---|---|
| Nested Loop Join | 外层每行扫内层 | 小表/有索引 | O(N×M)（无索引） |
| Index Nested Loop | 内层走索引 | 内表有索引 | O(N×logM) |
| Hash Join | 小表建哈希表，大表探测 | 等值连接、无索引 | O(N+M) |
| Merge Join | 两侧按 key 归并 | 已排序/需排序输出 | O(N+M) |

- Hash Join 两阶段：**build（建哈希表，用小的那侧）→ probe（探测，大的那侧）**
- 数据放不下内存 → 分区（external hash join，写磁盘分片）——衔接 34 轮磁盘存储
- OceanBase 向量化 hash join：探测时把哈希值批算、预取 bucket 进缓存——SIMD+缓存协同（衔接 20 轮）

- **来源**：CMU + neo01 + OceanBase
- **可信度**：S

---

## 四、查询优化器

### 1. 规则重写（基于规则的优化，RBO）

- 谓词下推（先过滤再 join）、投影剪枝（少取列）、子查询去关联化、连接顺序枚举（交换律）

### 2. 代价模型（基于代价的优化，CBO）

- 为每个物理算子估算代价：`代价 ≈ 磁盘 IO + CPU（+ 内存）`，选总代价最小的计划
- **基数估计（cardinality estimation）**是命门：估算"某过滤后剩多少行"决定 join 顺序/算法
  - 假设均匀分布 + 直方图（histogram）+ 采样
  - 相关列/数据倾斜 → 估算爆炸错误 → 执行计划灾难（经典"SELECT * 慢如狗"根因）
- 动态规划/贪心枚举 join 顺序（O(n!) 全枚举不行，用 DP + 剪枝）

### 3. 自适应执行

- 运行时统计修正计划（如 PostgreSQL 的 jit、Polr 系）
- 现代趋势：learning-based optimizer（机器学习估基数）——研究热点但工程落地少

- **来源**：CMU + CSDN OLAP
- **可信度**：S

---

## 五、并行查询执行

- **Exchange 算子**（Graefe Volcano 论文的核心贡献之一）：把并行性封装成一个算子（数据重新分区到多线程）
- 模型：
  - 流水线并行（不同算子不同线程，接力）
  - 数据并行（同一算子处理不同数据分片，汇总）
- 并行 join：分区 → 每分区独立 hash join → 合并（分而治之）
- 同步：barrier/汇合点（SIGMOD 2025 用树形 barrier 降开销）——衔接 39 轮无锁/同步
- 并行度上限：数据倾斜时单分区成瓶颈（skew 处理是难题）

## 六、知识网络

```
查询执行
├── 流水线：SQL → 逻辑计划 → 优化 → 物理计划 → 执行
├── 执行模型
│   ├── 火山/迭代器（每行虚调用，解释器开销 50-80%）
│   ├── 物化（整体结果，内存风险）
│   ├── 向量化（批处理+列循环+SIMD，ClickHouse/DuckDB）
│   └── 编译执行（LLVM 即时生成，HyPer）
├── Join：NLJ / Index NLJ / Hash（build-probe）/ Merge
├── 优化器：RBO（谓词下推等）+ CBO（代价模型+基数估计）
└── 并行：Exchange 算子、数据并行、分区 hash join、skew
```

---

## 七、本轮最重要的资料

1. **CMU 15-445 Lecture #13 Query Processing**（S）——三大模型权威课程
2. **Graefe "Encapsulation of Parallelism in the Volcano..."（ACM SIGMOD 1994）**（S）——火山模型原始论文
3. **ClickHouse 向量化查询执行**（S）——工业向量化实践
4. **OceanBase 向量化引擎**（A+）——分布式向量化实现
5. **neo01 PostgreSQL 火山模型**（A）——算子调用关系表

## 八、适合进入 CPP-Bible 的原子

- "火山模型：把查询变成算子的组合"（DB/ENG，接口设计案例）
- "向量化执行：为什么按列批处理快"（DB/PERF，衔接 SIMD 轮）
- "Hash Join 的 build-probe：算法与内存的权衡"（DB/ALGO）
- "基数估计：优化器为什么翻车"（DB/ENG，真实案例驱动）
- "Exchange 算子：把并行封装进查询"（DB/CONC）

## 九、与已有调研的关联

- 第二十二轮 SQLite：查询处理初览 → 本轮深挖执行层
- 第三十四轮存储引擎：B+ 树索引服务查询
- 第六十五轮（待写）事务：并发控制与执行交叠
- 第五十五轮 GC：物化中间结果的内存生命周期
- 第五十轮微架构：缓存友好/分支预测决定向量化收益

## 十、下一轮方向

Rust 与 C++ 对照（所有权/借用/内存安全）——全新语言域开篇。

---

*本轮新增知识节点：查询执行、query execution、火山模型、Volcano、迭代器模型、物化、materialization、向量化执行、vectorized、编译执行、codegen、LLVM、Graefe、算子、operator、Next、Hash Join、build、probe、Nested Loop、Merge Join、查询优化器、RBO、CBO、代价模型、基数估计、cardinality、直方图、谓词下推、Exchange、并行执行、数据倾斜、skew、ClickHouse、DuckDB、HyPer、OceanBase。补齐了"数据库查询执行"域核心空白。*
