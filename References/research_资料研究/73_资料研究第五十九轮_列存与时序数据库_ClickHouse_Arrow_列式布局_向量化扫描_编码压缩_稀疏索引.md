# 资料研究第五十九轮：列存与时序数据库——ClickHouse/Arrow、列式布局、向量化扫描、编码压缩、稀疏索引

> 2026-09-11，底层工程资料研究员。主题：行存 vs 列存（OLTP vs OLAP 的根本分歧）、列式布局的压缩优势（同类型相邻）、ClickHouse 向量化执行（块 = 65,536 值数组、SIMD 分派）、编码栈（Delta/DoubleDelta/Gorilla/T64/LZ4/ZSTD + LowCardinality 字典）、稀疏主索引与跳数索引（minmax/Bloom）、MergeTree 家族与分区、Apache Arrow 的列式内存格式、列存为什么是分析型数据库的答案（MonetDB/X100 血统）、与 CPP-Bible 教学的关系（SIMD 实战案例）。
> 检索方式：general_search + ClickHouse 官方（Why columnar databases are fast / What is columnar / Database compression）+ ClickHouse 架构文档 + ClickHouse Internals 源码路径拆解 + sadensmol ClickHouse 指南 + dontech 设计哲学 + GitHub parallax ClickHouse internals。
> **数据库域第四轮**。与 61 查询执行（向量化）、33 SIMD、65 事务（OLTP 对照）直接衔接——列存是"向量化查询执行"的最佳舞台。

---

## 一、行存 vs 列存：两套世界的分歧

| | 行存（OLTP，MySQL/Postgres） | 列存（OLAP，ClickHouse/Redshift） |
|---|---|---|
| 布局 | 一行连续（记录内聚） | 一列连续（同类型相邻） |
| 读模式 | 按行取（整行字段） | 按列扫描（只取要的列） |
| 写入 | 快（追加一行） | 慢（每列文件各追加） |
| 压缩 | 差（类型混杂） | 好（同类相邻，5-10x） |
| 场景 | 点查/事务 | 聚合/分析/大扫描 |

- **关键权衡**：OLTP 写多读点、OLAP 读多扫全——同一份数据布局无法两全（ClickHouse 官方明确：列存 tradeoff 是写入）
- 现代方案：HTAP（混合：TiDB/TigerBeetle）——但本质仍是两套引擎的整合

## 二、列式布局为什么压缩好

- **同一列 = 同类型 + 相似分布** → 相邻值相似 → 差值小 → 压缩率极高
- 实例：Date 列万亿行可压 100:1；字典/游程/差值编码在真实列数据上 5-10x（ClickHouse 官方数据）
- 压缩不只是省空间：**压缩后数据更小 → 磁盘读更少 → 更快**（IO 是分析查询的主瓶颈）

## 三、向量化执行：列存的灵魂

```
行存扫描:  for row in rows:  if row[age] > 30: ...   （每行一判断）
列存扫描:  整列加载 → SIMD 比较 → 掩码 → 结果
```

- **块（Block）= 每列一个数组，默认 65,536 值**：一次处理整列向量，循环内零解释开销
- **SIMD 分派**：同一算子按 CPU 特性分派 SSE/AVX 变体（ClickHouse CPU dispatch 博客）——衔接 33 轮 SIMD
- 血统：MonetDB/X100 开创（向量化论文），ClickHouse 明确继承（架构文档："vectorized execution model similar to MonetDB/X100"）
- 对比 61 轮火山模型：列存把"每行虚调用"变成"整列循环"——两个世界性能差 10-100x 的主因

## 四、编码栈（Codecs）：按列选择武器

| Codec | 原理 | 适合 |
|---|---|---|
| Delta / DoubleDelta | 存差值/二阶差值 | 单调 ID、时间戳 |
| Gorilla | 浮点异或压缩（时序专用） | 浮点指标 |
| T64 / GCD | 位宽打包/最大公约数 | 整数 |
| LZ4（默认）/ ZSTD | 通用压缩 | 通用（快/率高） |
| LowCardinality | 字典化（列内去重成 ID） | 低基数枚举（状态码） |

- **可堆叠**：`CODEC(Delta, ZSTD(3))`——先差值再压缩，两层增益
- 工程要点：**无银弹**——按列数据形状选 codec（tailrocks 拆解给出一一对应表：时间戳用 Delta、浮点用 Gorilla、日志串用 ZSTD）

## 五、索引：稀疏与跳数

- **稀疏主索引**：按主键排序的分区（part），索引只记每区边界——一次扫描跳过大块（比 B+ 树稀疏得多）
- **跳数索引（skip index）**：非主键列可选 minmax/Bloom/集合索引——查询时预剪枝块
- 与 B+ 树（34 轮）对比：B+ 树精确导向行；稀疏索引"块级粗筛 + 全块扫描"——**列存放弃精索引，换顺序扫描的简单暴力**

## 六、存储与合并：MergeTree

- **写入 = 追加不可变小分区（part）**，后台**异步合并**成大片——写友好（只追加）+ 读友好（大片顺序读）
- 与 LSM（34 轮提到）同哲学：**不可变 + 后台合并**；列存是"分析版 LSM"
- 分区裁剪（partition pruning）：按时间分区，查询只扫相关分区

## 七、Apache Arrow：列存的内存格式

- 把列式布局**标准化到内存**（跨语言、跨进程）：Parquet（磁盘）↔ Arrow（内存）↔ Flight（传输）
- 意义：列存不只是数据库——**任何分析工具都可以用列式内存格式交换数据**（零拷贝传递）
- 与 C++：Arrow 是 C++ 实现的高性能库（SIMD 内核），适合做源码阅读素材

## 八、知识网络

```
列存/时序
├── 行 vs 列：OLTP 写点查 vs OLAP 扫聚合
├── 压缩：同类相邻 5-10x、字典/游程/差值
├── 向量化：Block=65K 数组、SIMD 分派、MonetDB 血统
├── Codec 栈：Delta/Gorilla/T64/LZ4/ZSTD/LowCardinality
├── 索引：稀疏主索引、跳数索引（minmax/Bloom）
├── MergeTree：不可变 part + 后台合并（LSM 哲学）
└── Arrow：列式内存格式、零拷贝交换
```

---

## 九、本轮最重要的资料

1. **ClickHouse "Why columnar databases are fast"**（S）——官方权威
2. **ClickHouse 架构文档**（S）——向量化执行血统
3. **Database compression（编码详解）**（S）——codec 权威
4. **tailrocks ClickHouse Internals**（A+）——源码路径拆解
5. **sadensmol ClickHouse 指南**（A）——codec 实例

## 十、适合进入 CPP-Bible 的原子

- "行存 vs 列存：一种布局、两套世界"（DB/ARCH）
- "向量化执行：为什么列存快 100 倍"（DB/PERF，衔接 SIMD 轮）
- "编码栈：按列选择压缩武器"（DB/ALGO）
- "稀疏索引 vs B+ 树：放弃精索引换暴力扫描"（DB 设计权衡）
- "MergeTree：不可变 + 后台合并"（DB/ENG，LSM 对照）
- 实验：用 SIMD 写 50 行列扫描（比较 vs 标量循环）

## 十一、与已有调研的关联

- 第六十一轮查询执行：火山模型 vs 向量化模型正面对照
- 第三十三轮 SIMD：向量化的硬件基础
- 第三十四轮存储引擎：B+ 树行存 vs 列存稀疏索引
- 第六十五轮事务：OLTP 事务特性 vs OLAP 批量特性
- 第六十三轮 AI 编译器：XLA 的算子融合与列存批量处理同源

## 十二、下一轮方向

GPU 计算（CUDA 编程模型）。

---

*本轮新增知识节点：列存、columnar、OLAP、OLTP、行存、ClickHouse、向量化执行、vectorized、Block、MonetDB、X100、SIMD 分派、codec、Delta、DoubleDelta、Gorilla、T64、GCD、LZ4、ZSTD、LowCardinality、字典编码、游程编码、稀疏索引、跳数索引、skip index、minmax、Bloom filter、MergeTree、part、合并、分区裁剪、HTAP、TiDB、Redshift、Apache Arrow、Parquet、Flight、列式内存格式、零拷贝、时序数据库、GreptimeDB、InfluxDB。补齐了"列存/分析型数据库"域核心空白。*
