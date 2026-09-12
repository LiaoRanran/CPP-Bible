# 资料研究第五十一轮：数据库事务与隔离——ACID、MVCC、两阶段锁、快照隔离、写偏斜、可串行化

> 2026-09-11，底层工程资料研究员。主题：事务的 ACID 四性质、隔离级别谱系（读未提交→读已提交→可重复读→可串行化）与异常（脏读/不可重复读/幻读）、MVCC（多版本并发控制）的实现——Postgres 元组版本 vs MySQL undo log vs Oracle undo 表空间、快照隔离（Snapshot Isolation）与写偏斜（write skew）陷阱、两阶段锁（2PL）与死锁、可串行化（Postgres SSI vs MySQL 锁序列化）、并发控制的选择（锁 vs 版本 vs 乐观）。
> 检索方式：general_search + PostgreSQL 官方事务隔离文档 + PlanetScale 事务对照 + The Data Lakehouse Hub 并发控制对照 + cloudstreet Database Internals ch8 MVCC + TheCodeForge 快照隔离写偏斜 + Sciencx MySQL vs Postgres 事务 + wenha 隔离级别 + habr 五数据库隔离实践 + rhcwlq89 隔离级别指南。
> **数据库域第三轮**。与 22 SQLite、34 存储引擎、61 查询执行直接衔接——事务是"并发控制 + 存储版本"的组合。

---

## 一、ACID 四性质

| 性质 | 含义 | 实现 |
|---|---|---|
| A 原子性 | 全部成功或全部回滚 | WAL/undo log（衔接 64 轮日志） |
| C 一致性 | 事务前后约束成立 | 应用+数据库配合 |
| I 隔离性 | 并发事务互不干扰 | 隔离级别 + 并发控制（本轮主题） |
| D 持久性 | 提交后不丢 | WAL fsync（先写日志再落盘） |

- C 是"性质"，其余三个是"机制"——一致性由 A+I+D 共同实现
- **WAL（写前日志）与文件系统日志同构**（衔接 64 轮 jbd2）：都是"先记录意图再执行"的崩溃安全范式

## 二、隔离级别与异常

| 级别 | 脏读 | 不可重复读 | 幻读 | 说明 |
|---|---|---|---|---|
| Read Uncommitted | ✅（可见未提交） | — | — | 几乎不用 |
| Read Committed | ❌ | ✅ | ✅ | Postgres 默认 |
| Repeatable Read | ❌ | ❌ | 部分（MySQL 用 gap lock 消） | MySQL 默认 |
| Serializable | ❌ | ❌ | ❌ | 最强 |

- 脏读：读到别人**未提交**的修改（他回滚你就读错了）
- 不可重复读：同事务两次读同一行，结果不同（被已提交事务改了）
- 幻读：同事务两次查询，**行数**不同（新行插入）
- **选隔离级别 = 正确性需求 × 并发性能权衡**（越高并发越低，这是永恒矛盾）

- **来源**：Postgres 官方 + wenha + rhcwlq89
- **可信度**：S

---

## 三、MVCC：用版本替代锁

### 1. 核心思想

- **写不阻塞读，读不阻塞写**：每个写操作产生**新版本**，读操作看自己的快照
- 事务看到"哪个版本"由**快照（Read View）**决定：只看到"在我开始前已提交"的版本
- 效果：绝大多数 OLTP 读永远不被锁——并发度大增（现代数据库默认方案）

### 2. 三种实现

| 系统 | 机制 | 代价 |
|---|---|---|
| PostgreSQL | 行内保留**旧版本元组**（heap 里多版本共存），VACUUM 清理 | 膨胀（bloat），需 autovacuum |
| MySQL/InnoDB | 更新时覆盖旧值，**undo log** 保存旧版本（回滚段） | undo 膨胀，purge 线程清理 |
| Oracle | undo 表空间（类似 MySQL） | 自动 undo 管理 |

- 关键差异：Postgres "版本留在原地"（无锁但膨胀），MySQL "版本搬到日志"（原地覆盖但依赖 undo）
- 快照与 GC：MVCC 旧版本回收是"带版本条件的 GC"（衔接 55 轮 GC——这里"垃圾"= 无事务再引用的旧版本）

- **来源**：PlanetScale + datalakehousehub + cloudstreet
- **可信度**：S

---

## 四、快照隔离与写偏斜（Snapshots 的陷阱）

### 1. 快照隔离（SI）

- 事务读到**开始时**的一致快照（Repeatable Read 的实现基础）
- 写冲突：只在"同一行被并发改"时失败（first-committer-wins）
- 解决了脏读/不可重复读/幻读，**但**：

### 2. 写偏斜（Write Skew）——SI 的著名缺陷

```
医生值班表：要求至少一人值班
事务1（Alice）：查当前没人值班 → 设置自己值班
事务2（Bob）：  查当前没人值班 → 设置自己值班
并发提交 → 两人都以为没人，最终系统无人值班 ❌
```

- 两人读的是**同一快照**（都看到"无人"），各自写**不同行**——快照隔离检测不到（行级写冲突不存在）
- 结论：快照隔离 ≠ 可串行化；**约束检查需要更强的隔离或显式锁（SELECT ... FOR UPDATE）**

## 五、可串行化：最高隔离的两条路

### 1. 悲观：两阶段锁（2PL）

- 加锁分两阶段：**扩张（只加锁）→ 收缩（只放锁）**；提交前持所有锁
- 死锁：互相等锁 → 检测（等待图）+ 牺牲一个事务回滚
- 悲观但直观；锁竞争大时并发差

### 2. 乐观：SSI（Postgres Serializable Snapshot Isolation）

- 不预先锁：检测**读写冲突环**（r-w dependency 形成环 = 不可串行化），提交时中止一个
- 让 SI 之上的事务"模拟串行执行"——正确性靠运行时中止 + **应用重试**（Postgres 官方文档明确要求应用处理 serialization failure）
- 效果：比 2PL 并发高，但"中止重试"是新的应用负担

### 3. 现实工程

- 默认隔离是"够用就好"：MySQL RR + next-key lock、Postgres RC + SI
- 需要串行化时：小事务 + 显式锁/SSI + 重试；**长事务是可串行化的敌人**（锁持有久/快照旧）

## 六、并发控制选择矩阵

| 维度 | 2PL（悲观锁） | MVCC（版本） | OCC（乐观） |
|---|---|---|---|
| 读不阻塞写 | ❌ | ✅ | ✅ |
| 写冲突处理 | 等锁 | 版本冲突检测 | 提交时校验 |
| 死锁 | 有（需检测） | 无 | 无 |
| 适用 | 写多、冲突高 | 读多 OLTP（默认） | 冲突低的分布式 |
| 代表 | SQL Server 部分 | PG/MySQL/Oracle | CockroachDB |

- **选型哲学**：冲突概率决定——冲突多选悲观（等待比重试便宜），冲突少选乐观（无锁开销）

## 七、知识网络

```
事务与隔离
├── ACID：A=WAL/undo、C=应用约束、I=隔离级别、D=fsync
├── 隔离谱系：RC/RR/SERIALIZABLE + 三异常
├── MVCC：快照 Read View、PG 元组版本 vs MySQL undo、VACUUM/purge
├── SI：写偏斜陷阱、FOR UPDATE
├── Serializable：2PL（死锁）vs SSI（中止重试）
└── 选型：悲观/版本/乐观 × 冲突率
```

---

## 八、本轮最重要的资料

1. **PostgreSQL 官方 Transaction Isolation 文档**（S）——SSI 权威
2. **PlanetScale 事务实现对照**（S）——PG vs MySQL MVCC 机制
3. **cloudstreet Database Internals ch8**（S）——MVCC 系统讲解
4. **TheDataLakeHouseHub 并发控制对照**（A+）——五大系统表
5. **TheCodeForge 写偏斜**（A）——SI 陷阱清晰案例

## 九、适合进入 CPP-Bible 的原子

- "MVCC：写不阻塞读的版本魔法"（DB/CONC，与无锁对照）
- "写偏斜：快照隔离不够用的场景"（DB，真实正确性陷阱教学）
- "WAL：数据库与文件系统同一种崩溃范式"（DB/OS，跨域洞见）
- "2PL vs SSI：悲观与乐观的正确性代价"（DB/ALGO）
- "选隔离级别：正确性与并发的永恒权衡"（DB/ENG）

## 十、与已有调研的关联

- 第六十四轮文件系统：WAL/日志同构
- 第三十四轮存储引擎：B+ 树上的版本记录
- 第六十一轮查询执行：事务在算子之上的外层控制
- 第二十九轮分布式：分布式事务（2PC）是这轮的延伸
- 第五十五轮 GC：MVCC 旧版本回收即带条件 GC

## 十一、下一轮方向

高性能网络（DPDK/XDP/eBPF 用户态网络）。

---

*本轮新增知识节点：ACID、事务、原子性、隔离级别、脏读、不可重复读、幻读、MVCC、多版本并发控制、Read View、快照、undo log、回滚段、VACUUM、autovacuum、purge、快照隔离、SI、写偏斜、write skew、两阶段锁、2PL、死锁、可串行化、SSI、Serializable Snapshot Isolation、next-key lock、gap lock、悲观锁、乐观锁、OCC、WAL、fsync、FOR UPDATE、CockroachDB、first-committer-wins。补齐了"事务/并发控制"域核心空白。*
