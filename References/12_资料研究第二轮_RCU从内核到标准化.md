# 资料研究第二轮：RCU（Read-Copy-Update）——从 Linux 内核到 C++ 标准化

> 2026-09-11，底层工程资料研究员。主题：RCU 深入。
> 检索方式：web.fetch 一手来源（kernel.org / LWN / GitHub / wg21.link）。

---

## 一、核心资料（S 级）

### 1. Linux Kernel "What is RCU?"（whatisRCU.txt）

- **类型**：官方技术文档
- **来源**：Linux Kernel（kernel.org）
- **链接**：https://www.kernel.org/doc/Documentation/RCU/whatisRCU.txt
- **作者**：Paul E. McKenney（RCU 发明者）、Jonathan Walpole
- **核心内容**：RCU 的完整入门——核心 API（5 个原语）、使用示例、toy 实现（2 种）、与读写锁的对比、完整 API 列表（4 个家族 50+ API）、Quick Quiz 及答案
- **解决的问题**：如何在读者完全无锁的情况下安全地并发修改数据结构
- **为什么重要**：RCU 是 Linux 内核中使用量**超过锁**的同步机制；这是 McKenney 亲自写的权威文档
- **技术亮点**：
  - 三步更新序列：移除指针 → 等待已有读者完成（grace period）→ 安全回收
  - **Classic RCU 读端零开销**：非抢占内核中 `rcu_read_lock()`/`rcu_read_unlock()` 编译为空
  - `synchronize_rcu()` 的概念实现 = 在每个 CPU 上跑一次（强制上下文切换），因为 RCU 读端不允许阻塞，上下文切换意味着所有已有读端已完成
  - 两种 toy 实现：基于读写锁的（易理解但性能差）、Classic RCU（读端零开销）
  - 与读写锁的 unified diff 对比——差异极小：read_lock→rcu_read_lock、write_lock→spin_lock、加 synchronize_rcu()
- **与 C++ 的关系**：RCU 思想影响了 C++ 的 read-copy-update 提案（P0566R1）；`rcu_assign_pointer`/`rcu_dereference` 与 C++ atomic 的 release/acquire 语义同源
- **与 CPP-Bible 的关系**：CONC 域"读多写少场景的最优同步"核心资料；可以做成 CONC/PERF 交叉原子（读端零开销的性能实验）
- **可以放入哪个章节**：part09_concurrency（高级同步）、part14_perf
- **适合讲什么**：RCU 三机制、grace period 概念、读端零开销、与读写锁的对比
- **可以提取什么源码**：toy 实现 #2（Classic RCU，~10 行）、rcu_assign_pointer/rcu_dereference 的内存屏障实现
- **可以设计什么实验**：对比 RCU 读端 vs 读写锁读端的性能（RCU 读端无原子操作、无 cache miss）；在 x86 上验证 rcu_dereference 编译为空
- **可以设计什么案例**：Linux dcache（目录项缓存）使用 RCU 的真实场景——读路径完全无锁
- **历史背景**：RCU 2002 年 10 月进入 Linux 2.5 开发版；McKenney 从 1990 年代开始研究
- **工程背景**：Linux 必须支持从 UP 到 4096 CPU 的全谱系；RCU 的读端可扩展性是关键
- **相关论文**：McKenney "Exploiting Deferred Destruction in Operating System Kernels"（博士论文 2004）
- **相关项目**：liburcu（用户态）、folly RCU？（folly 有 hazptr 但没有完整 RCU）
- **相关作者**：Paul E. McKenney
- **可信度**：S
- **教材价值**：S

### 2. LWN "What is RCU, Fundamentally?"（McKenney 2007）

- **类型**：技术科普（经典系列）
- **来源**：LWN.net
- **链接**：https://lwn.net/Articles/262464/（Part 1/3）
- **作者**：Paul E. McKenney（IBM Linux Technology Center）、Jonathan Walpole（Portland State University）
- **核心内容**：RCU 的三个基本机制——①发布-订阅（插入，publish-subscribe）②等待已有读者完成（删除，wait for pre-existing readers）③维护多版本（读者容忍并发修改，maintain multiple versions）
- **解决的问题**：用最直观的方式解释 RCU 为什么能工作
- **为什么重要**：**这是 RCU 最好的入门文章**，没有之一。McKenney 亲自写的 LWN 三部曲，用链表替换的例子逐步演示多版本机制
- **技术亮点**：
  - 发布-订阅机制：`rcu_assign_pointer` 确保读者看到的要么是旧版本要么是新版本，不会是半更新
  - 多版本维护的图解：删除/替换时旧版本仍被已有读者引用，grace period 后才能回收
  - Quick Quiz 贯穿全文（如"seqlock 不也允许读者和更新者并发吗？"）
  - "RCU 读端零开销"的解释：非抢占内核中读端原语编译为空，synchronize_rcu 靠上下文切换检测
- **与 C++ 的关系**：RCU 的 publish-subscribe 机制与 C++ atomic 的 release/acquire 模式完全对应
- **与 CPP-Bible 的关系**：RCU 入门教学的最佳参考写法；"先给直觉再给 API"的教学法可以借鉴
- **可以放入哪个章节**：part09_concurrency
- **适合讲什么**：RCU 三机制的直觉理解
- **可以设计什么实验**：链表替换的多版本演示（用调试输出展示旧版本何时被回收）
- **历史背景**：2007 年 12 月发表，LWN 三部曲；当时 RCU 已进入内核 5 年但仍被认为"难以理解"
- **可信度**：S
- **教材价值**：S

### 3. WG21 P0566R1 "Concurrent Data Structures: Hazard Pointer and RCU"

- **类型**：C++ 标准提案
- **来源**：WG21（open-std.org）
- **链接**：https://wg21.link/P0566R1
- **作者**：Maged Michael（Hazard Pointer 发明者）、Paul McKenney（RCU 发明者）等
- **核心内容**：C++ 标准化 Hazard Pointer 和 RCU 的完整措辞——`rcu_domain`（域）、`rcu_obj_base`（继承式回收基类）、`rcu_guard`（RAII 读端守卫）；Hazard Pointer 的 `hazptr_domain`/`hazptr_holder`
- **解决的问题**：把两种工业界验证的无锁内存回收机制标准化进 C++
- **为什么重要**：**这是 C++ 并发标准化的重要方向**——Hazard Pointer 和 RCU 被放在同一份提案里，因为它们是"两种竞争的延迟回收机制"。提案明确引用了 folly 的 hazptr 实现和 Linux 的 RCU
- **技术亮点**：
  - RCU 的 C++ API 设计：`rcu_domain::read_lock()/read_unlock()/synchronize()`、`rcu_obj_base<T>::retire()`、`rcu_guard`（RAII）
  - 提案明确说"高质量实现的读端常见路径不使用锁、RMW 原子操作、或导致 cache miss 的内存访问"——这是 RCU 的核心性能承诺
  - Hazard Pointer 和 RCU 的对比：HP 保护**特定对象**（对象级），RCU 保护**临界区内所有数据**（域级）
  - 两者都与 `atomic_shared_ptr`（引用计数）和 GC 并列，是"延迟回收"的四种技术
- **与 C++ 的关系**：就是 C++ 标准提案本身；C++26 可能纳入 Hazard Pointer（P2530R3），RCU 仍在 Concurrency TS
- **与 CPP-Bible 的关系**：HIST/CONC 交叉原子——"两种无锁回收机制的标准化历程"；可以解释为什么 folly 选了 HP 而 Linux 选了 RCU
- **可以放入哪个章节**：part09_concurrency（lock-free 内存回收）、C++历史章节
- **适合讲什么**：Hazard Pointer vs RCU 的设计取舍、延迟回收的四种技术
- **可以设计什么实验**：实现最小 RCU（~50 行）和最小 Hazard Pointer（~80 行），对比性能和适用场景
- **历史背景**：P0566R1 是 2017 年版本；Hazard Pointer 2004 年由 Maged Michael 发明；RCU 2002 年进入 Linux
- **相关论文**：Michael 2004 "Hazard Pointers"、McKenney RCU 论文
- **相关项目**：folly Hazptr（上一轮）、liburcu
- **可信度**：S
- **教材价值**：A+

---

## 二、工业实现（A+ 级）

### 4. liburcu（Userspace RCU）

- **类型**：开源库
- **来源**：GitHub urcu/userspace-rcu
- **链接**：https://github.com/urcu/userspace-rcu
- **核心内容**：用户态 RCU 的工业级实现，4 种 flavor：
  - **memb**（首选）：用 Linux `sys_membarrier()` 系统调用，读端快、grace period 检测快；不支持时回退到 mb
  - **qsbr**（Quiescent State Based RCU）：读端最快，但需手动调用 `rcu_quiescent_state()`，侵入性强
  - **mb**（Memory Barrier）：读写端都用内存屏障，grace period 检测快但读端慢
  - **bp**（Bulletproof）：无需修改应用（init/register 都是 nop），用于 tracing 库 hook，性能最差
- **解决的问题**：把 Linux 内核的 RCU 机制移植到用户态
- **为什么重要**：这是用户态 RCU 最成熟的实现；被 LTTng（Linux 跟踪工具）等项目使用
- **技术亮点**：
  - 4 种 flavor 的设计取舍——没有"最好的 RCU"，只有"最适合场景的"
  - `sys_membarrier()` 的利用——Linux 4.14+ 提供的系统调用，让一个进程可以强制其他 CPU 执行内存屏障
  - 线程注册/注销机制（用户态没有内核的 per-CPU 上下文）
  - `defer_rcu`/`call_rcu` 异步回调机制
  - 与 `fork()` 的复杂交互（只有 bp flavor 能安全处理 fork 后不 exec 的场景）
- **与 C++ 的关系**：纯 C 实现，但可直接在 C++ 中使用；其设计思路影响了 C++ RCU 提案
- **与 CPP-Bible 的关系**：用户态 RCU 的工业案例；4 种 flavor 的取舍可以做成"工程权衡"教学案例
- **可以放入哪个章节**：part09_concurrency、part40_large_scale_engineering
- **适合讲什么**：RCU 的多种实现取舍、sys_membarrier 的妙用、用户态 vs 内核态 RCU 的差异
- **可以提取什么源码**：memb flavor 的读端实现（应该是几行内联汇编或 compiler barrier）
- **可以设计什么实验**：对比 4 种 flavor 的读端/写端性能
- **历史背景**：liburcu 由 Mathieu Desnoyers（LTTng 作者）维护，从 2000 年代末开始
- **相关项目**：LTTng、folly（HP 而非 RCU）
- **可信度**：A+（工业级，LGPL 许可）
- **教材价值**：A+

---

## 三、知识网络

```
RCU 三机制（McKenney LWN 2007）
├── 发布-订阅（插入）→ rcu_assign_pointer → C++ atomic store(release)
├── 等待已有读者（删除）→ synchronize_rcu → grace period
└── 维护多版本（读者）→ 旧版本延迟回收 → 与 Hazard Pointer 竞争
    │
    ├── Linux 内核实现（whatisRCU.txt）
    │   ├── Classic RCU（读端零开销）
    │   ├── Preemptible RCU（实时内核）
    │   ├── SRCU（可阻塞读端）
    │   └── RCU-bh/RCU-sched（特殊场景）
    │
    ├── 用户态实现（liburcu）
    │   ├── memb（sys_membarrier）
    │   ├── qsbr（最快读端）
    │   ├── mb（内存屏障）
    │   └── bp（bulletproof）
    │
    └── C++ 标准化（P0566R1）
        ├── rcu_domain / rcu_obj_base / rcu_guard
        └── 与 Hazard Pointer 并列（两种延迟回收机制）

延迟回收四技术：
1. RCU（域级保护，读端极快，写端延迟）
2. Hazard Pointer（对象级保护，读端有开销，写端可预测）
3. 引用计数（atomic_shared_ptr，自动回收，读端有 RMW 开销）
4. GC（全自动，暂停时间不可控）
```

---

## 四、RCU vs Hazard Pointer 对比（教学核心）

| 维度 | RCU | Hazard Pointer |
|---|---|---|
| 保护粒度 | 域级（临界区内所有数据） | 对象级（特定指针） |
| 读端开销 | 零（非抢占内核）/ 极低 | 每次保护需写 hazard pointer（RMW） |
| 写端开销 | 等待 grace period（可批处理） | 扫描所有 hazard pointer（O(线程数)） |
| 读端是否需声明 | 是（rcu_read_lock） | 是（hazptr_holder::protect） |
| 内存使用 | 低（每域少量状态） | 高（每线程固定数量 HP） |
| 可阻塞读端 | 否（经典 RCU）/ SRCU 可以 | 是 |
| 典型用户 | Linux 内核 | MongoDB、folly |
| C++ 标准化 | P0566R1（Concurrency TS） | P2530R3（可能 C++26） |
| 最大优势 | 读端极致快 | 回收时间可预测 |
| 最大劣势 | 写端延迟不可控 | 读端有 cache miss |

**教学洞察**：这两种机制的对比是"工程权衡"的绝佳案例——没有银弹，只有场景适配。读多写少、读端延迟敏感→RCU；写多、回收延迟敏感→Hazard Pointer。

---

## 五、本轮最重要的 10 个资料

| # | 资料 | 级别 | 核心价值 |
|---|---|---|---|
| 1 | Linux whatisRCU.txt | S | RCU 权威文档，toy 实现+API 全列表 |
| 2 | LWN "What is RCU, Fundamentally?" | S | 最好的 RCU 入门，三机制直觉 |
| 3 | WG21 P0566R1 | S | C++ 标准化 RCU+HP，两种机制对比 |
| 4 | liburcu | A+ | 用户态 RCU 4 flavor 工业实现 |
| 5 | McKenney 博士论文 | S | RCU 深度理论（需获取） |
| 6 | folly Hazptr（上一轮） | A+ | HP 工业实现，与 RCU 对比 |
| 7 | folly MPMCQueue（上一轮） | A+ | 无锁队列，序列号同步 |
| 8 | Boehm PLDI 2005（上一轮） | S | 内存模型奠基 |
| 9 | preshing 系列（上一轮） | A+ | 内存序可复现实验 |
| 10 | perfbook（上一轮） | S | 并行编程全面指南 |

## 六、强烈建议深入研究的 5 个资料

1. **Linux whatisRCU.txt**——必须精读，特别是 Section 5 的两个 toy 实现和 Section 6 的读写锁对比
2. **LWN 三部曲**——Part 1（基本原理）、Part 2（用法）、Part 3（API），建立完整直觉
3. **liburcu memb flavor 源码**——理解 sys_membarrier 如何实现用户态 grace period
4. **P0566R1 完整措辞**——理解 C++ 标准化的 API 设计考量
5. **McKenney 博士论文**——RCU 的形式化基础和性能分析

## 七、适合直接进入 CPP-Bible 的资料

| 资料 | 进入方式 | 目标原子/章节 |
|---|---|---|
| whatisRCU.txt | RCU 三机制 + toy 实现实验 | CONC 域"读多写少同步"原子 |
| LWN 三部曲 | 教学写法参考 + 多版本图解 | CONC 域 motivation |
| P0566R1 | RCU vs HP 对比 + 标准化历程 | HIST/CONC 交叉原子 |
| liburcu | 4 flavor 工程取舍案例 | 工程权衡章节 |
| RCU vs HP 对比表 | 直接作为原子的 superiority 内容 | CONC lock-free 原子 |

## 八、发现的知识空白

1. **RCU 完全未覆盖**——全书 147 章无 RCU 内容，这是 Linux 内核最重要的同步机制之一
2. **无锁内存回收四技术对比缺失**——RCU/HP/引用计数/GC 的对比是理解 lock-free 的关键
3. **读端零开销的性能实验缺失**——RCU 读端无原子操作、无 cache miss，这是可以用证据卡验证的
4. **sys_membarrier 系统调用未覆盖**——这是用户态 RCU 的关键使能技术，也是 Linux 内核与用户态协作的精彩案例
5. **grace period 的实现原理缺失**——"如何知道所有读者都完成了"是 RCU 最巧妙的部分

## 九、下一轮推荐搜索方向

1. **C++ 标准提案追踪**——P2530R3 Hazard Pointer 最新进展、P0566 RCU 现状、atomic_ref
2. **无锁数据结构**——Michael-Scott queue、Treiber stack、lock-free hash map（folly/AtomicHashMap）
3. **真实并发 bug 案例**——PostgreSQL/MySQL/Redis 中的内存序 bug、C++ 并发 bug 数据库
4. **内存模型形式化验证**——Linux tools/memory-model/（herd7 工具）、Cambridge 内存模型
5. **ARM 弱内存模型**——ARM Architecture Reference Manual、ARM 上的重排实验（需 QEMU）
6. **seqlock / per-CPU 数据结构**——Linux 其他读多写少同步机制，与 RCU 对比

---

*本轮新增知识节点：RCU 三机制、grace period、读端零开销、4 种 liburcu flavor、RCU vs HP 对比、延迟回收四技术、sys_membarrier。补齐了 CONC 域"读多写少最优同步"和"无锁内存回收"两个空白。*
