# 资料研究第三十九轮：无锁编程与内存回收——CAS 循环、ABA 问题、Hazard Pointer、EBR、RCU、Michael-Scott 队列

> 2026-09-11，底层工程资料研究员。主题：锁竞争 vs 无锁的取舍、CAS 与原子操作、Treiber 栈与 Michael-Scott 队列、ABA 问题（危害+防法：版本号/危险指针）、内存回收（SMR）：Hazard Pointer（危险指针）、EBR（Epoch-Based Reclamation，基于代际的回收）、RCU（读-复制-更新）、推迟回收的宽限期模型、无锁数据结构正确的验证（DRD/TSan/Loom）。
> 检索方式：general_search + ethancornell EBR vs HP 深度 + Kinda Technical ABA 与危险指针 + lbenicio EBR 队列实现 + Michael HPBR 论文（IPDPS 2006）+ HazardLFQ 工业实现 + nottldr 无锁数据结构 + devweekends RCU + arXiv 无协调无锁队列。
> **并发域第十轮收官**。前十轮：11 内存模型、12 RCU、13 无锁结构、14 真实 bug、16 形式化验证、17 内存模型（编译器视角）、19 seqlock/per-CPU、21 验证工具、35 C++26 内存回收标准化（hazard_pointer/rcu）。本轮把"回收与 ABA"完整闭环。

---

## 一、为什么无锁？为什么不是银弹

### 1. 锁的问题

- 锁竞争：线程排队，上下文切换/自旋浪费；锁粒度粗则吞吐崩
- 优先级反转、死锁、锁的持有者被调度走（调度延迟放大）

### 2. 无锁（Lock-Free）的定义（严格）

- 系统级保证：**至少一个线程总能前进**（whole-system progress）
- 更强：无等待（Wait-Free）——每个线程都有限步完成
- 更弱：无阻塞（Obstruction-Free）
- **无锁 ≠ 无等待 ≠ 无代价**：CAS 循环在竞争下反复重试、内存回收机制本身有开销、ABA 要防

### 3. 适用判断

- 高竞争 + 短临界区 + 读多（RCU 的黄金场景）
- 低竞争时锁反而更简单更快（futex 无竞争路径 ~20ns）
- 无锁数据结构的正确性极难保证 → 需要验证工具（衔接第二十一轮）

- **来源**：nottldr + CSDN 无锁性能陷阱
- **可信度**：A+

---

## 二、基础构件：原子操作与 CAS 循环

### 1. CAS（Compare-And-Swap）

```cpp
// 伪代码：如果 *p == expected，则 *p = desired，返回 true；否则返回 false
bool CAS(T* p, T expected, T desired);
// C++20: std::atomic<T>::compare_exchange_strong/weak
```

### 2. 通用模式：CAS 循环

```cpp
// Treiber 栈的 push：把"读旧顶 → 构造新顶 → CAS"循环到成功
node* old = top.load();
do {
    new_node->next = old;
} while (!top.compare_exchange_weak(old, new_node));
```

- 失败自动更新 expected（weak 版省一次重载），循环重试
- **CAS 循环解决"读-改-写"的原子性**：把竞争转化为重试

### 3. 其他构件

- LL/SC（Load-Linked/Store-Conditional）：ARM/POWER 的硬件原语，CAS 的替代；ABA 检测天然支持（地址变化即失败）
- fetch_add/xchg：无锁计数、队列头部推进用

- **来源**：Kinda Technical + 综合
- **可信度**：S

---

## 三、ABA 问题：无锁编程的头号陷阱

### 1. 发生场景（Treiber 栈经典）

```
初始：top → A → B → C
T1 准备 pop A：读到 A，还没 CAS
T1 被调度走
T2 弹出 A，释放 A；弹出 B；把 A 的地址重新分配成新节点推回（内存被复用）
T1 醒来：CAS(top, A, 新top)...  A 的地址值没变（被复用），CAS 成功！
但 T1 以为的"A->next = B" 现在指向的是 T2 数据结构的别处 → 栈损坏/UAF
```

- 本质：**CAS 只比较了"地址值"，没比较"版本"**——值回到原样，状态已变
- 危害：use-after-free、结构损坏，随机且难复现（并发 bug 之王）

### 2. 防法

| 方法 | 原理 | 代价 |
|---|---|---|
| 版本号（tagged pointer） | 指针低位/独立字放递增计数，CAS 同时比较指针+版本 | 指针空间受限/额外字 |
| 延迟回收（不释放，推迟） | 内存不被复用 → ABA 无源 | 内存上限不可控 |
| 危险指针 | 见下节 | 每线程 K 个槽 |
| 编译器/硬件辅助（LL/SC） | 地址变化即失败 | 硬件依赖 |

- **来源**：Kinda Technical + lbenicio + CSDN
- **可信度**：S

---

## 四、内存回收（SMR）：无锁的最后一环

无锁结构删除节点后**不能立即 free**：别的线程可能还持有指向它的指针。内存回收（Safe Memory Reclamation）解决"何时才能真正释放"。

### 1. Hazard Pointer（危险指针，Michael 2004）

- 每线程固定 K 个"危险槽"：访问共享节点前，把指针登记进槽（原子发布）
- 删除者：回收前检查所有线程的所有槽，只要有槽指向该节点 → 推迟释放
- 特点：**细粒度**——节点一旦无保护立即释放；**有界内存**（≤ H + R×N）
- 缺点：每个访问都要发布/清除槽（有原子开销）；读路径多次护栏
- 工业实现：Folly HazardPointer、C++26 hazard_pointer（衔接第十七轮）

### 2. EBR（Epoch-Based Reclamation，基于代际回收）

- 全局三（或多）个 epoch（代），循环切换
- 线程进入临界区时登记当前 epoch（本地读）；退出时清除
- 节点退役记入当前 epoch 的退役列表；**epoch N 的节点要到 N+2（两个宽限期后）才真正释放**——保证所有在 N 期间读过它的线程都已离开临界区
- 特点：**读路径开销极小**（一次读本地标记），高吞吐；缺点：线程卡在临界区不退出 → 退役列表无限增长（内存无界）
- 工业实现：Folly EBR、HazardLFQ（本报告案例）

### 3. 两者对比

| | Hazard Pointer | EBR |
|---|---|---|
| 读路径开销 | 每次访问发布/清除（原子） | 进入/离开临界区一次 |
| 内存上限 | 有界 | 线程卡住则无界 |
| 释放粒度 | 立即（无保护即释放） | 延迟两个宽限期 |
| 场景 | 读多写少、要求内存可控 | 高吞吐、临界区短 |

### 4. RCU（Read-Copy-Update）——内核的极致变体

- Linux 内核无锁同步之王（第二轮已深挖）：读路径零原子操作（只靠内存屏障+发布/订阅语义）
- 更新：复制新版本 → 发布指针 → 等待所有读端离开（宽限期）→ 释放旧版本
- 用户态（liburcu、C++26 std::experimental::rcu）已是标准化方向（第十七轮）

- **来源**：ethancornell 对比 + Michael IPDPS 论文 + lbenicio + HazardLFQ + devweekends RCU
- **可信度**：S

---

## 五、经典无锁结构

### 1. Michael-Scott 队列（1996）

- 无锁 MPMC FIFO：头尾两个指针 + CAS 推进；dummy 节点避免空队歧义
- 至今是工业无锁队列的标准基线（Folly MPMCQueue 是其优化变体，第十九轮已调研）
- 本报告引用的 HazardLFQ/EBRLFQ 就是它的完整工业实现（双回收策略 + 零 ABA）

### 2. Treiber 栈（1986）

- 无锁 LIFO：单 CAS 循环，教学最小示例
- 实际工程用得少（栈本身场景有限），但它是理解 CAS/ABA 的教科书

### 3. 无锁哈希表/链表

- 细粒度 CAS 链接、分裂顺序锁（与第八轮 seqlock 结合）、无锁读+锁写混合
- Split-Ordered List、Hopscotch Hashing 等

- **来源**：HazardLFQ + noooah2000 + 综合
- **可信度**：A+

---

## 六、正确性验证（无锁的命门）

- 无锁代码"看起来对"通常不对：需要
  - **动态验证**：TSan（数据竞争检测，第二十一轮）、Helgrind、DRD、Loom（Java）
  - **形式化**：C11/C++20 内存模型的模型检测（CDSChecker、GenMC）、TLA+（第三十四轮）
  - **压力测试 + 差分**：多核长时间随机操作，与串行参考实现对比结果
- 项目启发：CPP-Bible 的证据链方法正是"机器可验证"哲学，无锁原子最适合做"验证驱动开发"示范

- **来源**：综合 + 与第二十一轮衔接
- **可信度**：A+

---

## 七、知识网络

```
无锁编程
├── 定义：lock-free/wait-free/obstruction-free（系统级进度保证）
├── 构件：CAS/LL-SC/fetch_add、CAS 循环
├── ABA 问题（值回归的假成功）
│   ├── 版本号
│   ├── 延迟回收
│   └── 危险指针
├── 内存回收 SMR
│   ├── Hazard Pointer（细粒度、有界）
│   ├── EBR（代际、宽限期、高吞吐）
│   └── RCU（零原子读、宽限期、内核/用户态）
├── 经典结构：Treiber 栈、Michael-Scott 队列、无锁哈希
└── 验证：TSan/CDSChecker/TLA+/差分测试
```

---

## 八、本轮最重要的资料

1. **ethancornell LFQ_EBR：EBR vs Hazard Pointers 深度对比**（S）——两大回收策略量化
2. **Kinda Technical ABA 与 Hazard Pointers**（S）——ABA 场景逐步演示
3. **Michael & Scott "Making Lockless Synchronization Fast"（IPDPS 2006）**（S）——HPBR 原始论文
4. **HazardLFQ/EBRLFQ 工业实现**（A+）——双回收策略的 C++20 落地
5. **lbenicio EBR 队列实现**（A）——EBR 逐行讲解

## 九、适合进入 CPP-Bible 的原子

- "ABA：CAS 成功为何仍可能错"（CONC，实验：Treiber 栈复现 ABA + 版本号修复）
- "Hazard Pointer vs EBR：内存回收的两条路"（CONC，衔接 C++26 标准化）
- "Michael-Scott 队列：无锁 MPMC 的标准答案"（CONC/ALGO）
- "无锁 ≠ 无代价：什么场景才值得用"（CONC 工程判断）
- "宽限期（grace period）：为什么延迟释放是安全的"（CONC/MEM，RCU 核心思想）

## 十、与已有调研的关联

- 第一轮内存模型 / 第七轮 ARM 弱内存：CAS 与顺序一致性的硬件实现
- 第十二轮 RCU / 第十七轮 C++26 内存回收标准化：本轮是完整闭环（RCU=EBR 内核变体）
- 第十三轮无锁结构 / 第十九轮 MPMCQueue/seqlock：结构层
- 第二十一轮验证工具：TSan/DRD
- 第十六轮内存模型形式化 / 第三十四轮 TLA+：验证哲学
- 第三十六轮 CPU：CAS 依赖 cache 一致性（MESI），LL/SC 依赖硬件

## 十一、下一轮方向

构建系统（CMake/Ninja/增量构建）或 TCP/拥塞控制。

---

*本轮新增知识节点：无锁、lock-free、wait-free、obstruction-free、CAS、compare-and-swap、compare_exchange、LL/SC、load-linked、store-conditional、Treiber 栈、Michael-Scott 队列、ABA、ABA problem、版本号、tagged pointer、内存回收、SMR、safe memory reclamation、hazard pointer、危险指针、EBR、epoch-based reclamation、宽限期、grace period、退役列表、retired list、RCU、read-copy-update、liburcu、无锁哈希、split-ordered list、CDSChecker、GenMC、数据竞争检测、TSan。并发域十轮调研至此收官，素材足以支撑 CONC 域原子批量生产。*
