# 资料研究第五十七轮：内存分配器深入——glibc ptmalloc、jemalloc、tcmalloc、arena、tcache、size class、内存池

> 2026-09-11，底层工程资料研究员。主题：为什么 malloc 不是简单的"找块大内存"、ptmalloc 的 arena/bins 结构（main arena vs thread arena、unsorted/small/large/fast bins、tcache）、jemalloc 的 arena/extent/run 分层与防碎片策略、tcmalloc 的 ThreadCache/CentralCache/PageHeap 三层与 per-CPU cache、size class 与内存池思想、三大分配器对比（性能/碎片/可扩展性）、分配器与缓存层级（衔接 50 轮 CPU）、自定义分配器（STL allocator、pmr）的工程价值。
> 检索方式：general_search + tcmalloc 官方 design.md/overview + JZLeetCode 分配器设计 + padho.ai malloc internals + iq-dev-lab 三大分配器对比 + CSDN ptmalloc/tcmalloc/jemalloc + Benicio 线程缓存 malloc 实现 + locklessinc 可扩展内存分配。
> **内存管理域深入轮**。与 51 内存管理（虚拟内存/伙伴系统）、36 ABI、55 GC、59 泛型（pmr）直接衔接——用户态分配器是内核分配器的"用户侧镜像"。

---

## 一、问题：malloc 到底在干什么

- 用户态分配器**不直接向内核要内存**（每次 brk/mmap 都是系统调用）——而是：
  - 一次性向内核申请大块（heap/arena）
  - 自己管理块内的分配/释放（free list、bin）
- 设计目标（相互拉扯）：
  - **快**：分配/释放 O(1)（无锁或少锁）
  - **少碎片**：外部碎片（空闲块太碎）与内部碎片（size class 取整浪费）
  - **可扩展**：多线程下无全局锁竞争
- 这是"数据结构 + 并发 + 系统调用"的合流问题——allocator 是最被低估的系统软件

## 二、glibc ptmalloc2：bins 的世界

### 1. 分层结构

```
Main Arena（主线程，brk 连续区）
└── bins[]：按大小分类的空闲链表
    ├── [0] unsorted bin：刚释放的块先放这（快速复用）
    ├── fast bins（16-80B）：小块，不合并（快、碎片少）
    ├── small bins（16-512B）
    └── large bins（512B-256KB）
Thread Arena（每个线程，mmap 独立区，上限 ≈ 8×CPU 核数）
```

### 2. 关键机制

- **tcache（2.26+ 引入）**：线程本地小块缓存（≤ ~1000B）——单线程分配大幅提速、减少锁（Benicio 文章明说）
- **chunk 元数据**：块头存 size/prev_size/标志位（对齐 16 字节）——free 时靠相邻块合并（coalescing）
- **top chunk**：arena 末尾的"预留区"，不够时从这里切（或用 brk/mmap 扩）
- 代价：多线程高并发时 arena 竞争仍存在（arena 数量有上限）；碎片控制一般
- 已知弱点：tcache 是 double-free 攻击的热点（安全视角，衔接 79 轮安全）

## 三、tcmalloc：三层缓存

```
ThreadCache（每线程/每 CPU，本地无锁）
└── CentralCache（中央，锁保护，span 管理）
    └── PageHeap（按页大小管理，向内核要内存）
```

- **size class**：对象尺寸取整到离散档位（如 8/16/24/32...），每档一条 free list——分配 = 从对应 class 取一个（O(1)）
- **per-CPU 模式**：Linux RSEQ（重启序列，4.18+）支持下缓存挂到逻辑核——**热点 class 自动扩容、冷 class 收缩**（动态容量，tcmalloc design.md）
- 大对象（>32K）：直接从 CentralCache/PageHeap 分配，页对齐
- 优势：多线程扩展性好（每核本地化）、分配快；代价：内部碎片（取整）、内存占用偏高（缓存不释放）

## 四、jemalloc：arena + extent + run

- **arena 双数**（核数的 2 倍），每线程哈希到 arena——比"每线程一个"更省、比"全局"更并发
- **分层**：arena → extent（大块内存区）→ run（同 size class 的页序列）
- **防碎片**：小对象从 run 分配（同尺寸集中）、懒合并、脏页延迟回收（dirty decay）
- 特色：**redzone/填毒检测**（debug 构建）、profiling 内建（heap profile）——Facebook/MySQL/Redis 选它
- 工程评价：大并发下内存占用比 tcmalloc 略高、碎片控制最好（业界普遍认知）

## 五、三大分配器对比

| | ptmalloc | tcmalloc | jemalloc |
|---|---|---|---|
| 核心 | arena + bins | ThreadCache + CentralCache + PageHeap | arena + extent + run |
| 线程扩展 | 中（arena 上限） | 好（per-CPU） | 好（2×核 arena） |
| 碎片控制 | 中 | 中（内部碎片略多） | 好（run 集中） |
| 内存占用 | 低 | 中高（缓存不还） | 中高（decay 回收） |
| 特色 | 系统默认 | RSEQ per-CPU、动态容量 | profiling、redzone |
| 适用 | 通用 | 高并发服务（Google） | 高并发 + 大内存（DB） |

- **没有完美分配器**：快 ↔ 碎片 ↔ 内存占用，三选二——选型是工作负载的问题（这也是"数据库换 jemalloc"流行的原因）

## 六、思想：内存池与 size class

- **内存池（memory pool）**：预分配大块 + 固定大小切分 + 快速回收——游戏引擎/网络库的标配
- size class 思想的本质：**把任意尺寸请求离散化为有限档位 → free list 数量有限 → 分配 O(1)**
- 与内核伙伴系统（51 轮）同构：内核按 2^n 页分类，用户态按 size class 分类——**"分级缓存"是内存管理的通用解法**

## 七、C++ 视角：自定义分配器

- STL allocator / pmr（polymorphic allocator）：容器可换分配策略（arena 复用、线程本地、对齐控制）
- 何时值得：高频小对象（每对象分配开销显著）、需要局部性（同批对象放同一 region）、需要统计/对齐
- 反模式：过早自定义（默认分配器已被极度优化；自定义 ≠ 更快）

## 八、知识网络

```
内存分配器
├── ptmalloc：arena/bins/tcache/chunk 元数据/合并
├── tcmalloc：ThreadCache/CentralCache/PageHeap、size class、per-CPU RSEQ
├── jemalloc：arena×2核/extent/run、dirty decay、profiling
├── 对比：快 vs 碎片 vs 内存占用
├── 思想：内存池、size class、分级缓存（与伙伴系统同构）
└── C++：STL allocator、pmr、何时自定义
```

---

## 九、本轮最重要的资料

1. **tcmalloc 官方 design.md**（S）——per-CPU/动态容量权威
2. **JZLeetCode How Memory Allocators Work**（S）——bins 结构清晰
3. **padho.ai malloc internals**（A+）——四分配器对照
4. **CSDN ptmalloc/tcmalloc/jemalloc 总结**（A+）——中文全览
5. **Benicio 线程缓存 malloc 实现**（A）——从零实现教程

## 十、适合进入 CPP-Bible 的原子

- "malloc 不是系统调用：用户态分配器分层"（SYS/OS）
- "size class：把任意尺寸离散化的艺术"（ALGO/ENG）
- "tcache/ThreadCache：线程本地化的并发答案"（CONC，衔接无锁轮）
- "三大分配器选型：快/碎片/内存的三角"（ENG 决策）
- "自定义分配器：何时值得"（C++ 工程）
- 实验：实现 100 行 size class 分配器（free list + 合并）

## 十一、与已有调研的关联

- 第五十一轮内存管理：伙伴系统/slab 是用户态分配器的内核版
- 第五十轮 CPU：分配器的缓存局部性（size class 提升命中率）
- 第五十五轮 GC：GC 堆 vs 手动分配器的回收哲学
- 第五十九轮泛型：pmr 是 allocator 的运行时多态版
- 第五十三轮无锁：无锁分配器（如 mimalloc 的部分）是两者结合

## 十二、下一轮方向

C++ 网络框架源码（Boost.Asio/grpc 线程模型）。

---

*本轮新增知识节点：malloc、ptmalloc、glibc、arena、main arena、thread arena、bin、unsorted bin、fast bin、small bin、large bin、tcache、chunk、top chunk、coalescing、合并、tcmalloc、ThreadCache、CentralCache、PageHeap、size class、per-CPU cache、RSEQ、restartable sequences、jemalloc、extent、run、dirty decay、redzone、heap profile、mimalloc、内存池、memory pool、STL allocator、pmr、polymorphic allocator、内部碎片、外部碎片、double-free、伙伴系统。补齐了"内存分配器"域核心空白。*
