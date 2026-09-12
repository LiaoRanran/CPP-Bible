# 资料研究第三十七轮：Linux 内存管理——虚拟内存、页表/MMU、伙伴系统、slab/slub、vmalloc、缺页异常、demand paging、mmap

> 2026-09-11，底层工程资料研究员。主题：虚拟内存"谎言与抽象"、页表结构（多级页表、THP 大页）、MMU/TLB、内存区 VMA、伙伴分配器（buddy，order 拆分/合并、碎片）、slab/slub 对象缓存、kmalloc vs vmalloc vs kvmalloc、GFP 标志、缺页异常（demand paging、COW、major/minor fault）、mmap 与匿名映射、内存压缩/回收（kswapd、LRU）、zoned 内存（ZONE_DMA/NORMAL/HIGHMEM）、页回收与 OOM。
> 检索方式：general_search + Linux Kernel 官方（MM concepts/physical memory/memory allocation）+ kernel-internals.org Memory Management 故事 + Columbia CS 内核分页讲义 + infra-by-michaelhill systems handbook + CSDN Linux 内存管理深度 + minzkn 内核内存管理。
> **操作系统域第四轮**。前三轮：17 cache/虚拟内存（用户视角）、31 调度、44 文件系统（Page Cache）。与第十七轮（用户态堆/栈）、第三十轮（页面缓存写回）、第五十轮（TLB/缓存）强关联。

---

## 一、虚拟内存：计算机最重要的抽象之一

- 每个进程以为自己在用从 0 开始的连续 128TB 私有地址空间
- 实际上物理内存有限且碎片化，虚拟内存是"谎言"，但这个谎言换来：
  1. **隔离**：进程间地址互不可见，一个崩溃不影响另一个
  2. **按需加载**：只把真正用到的页放进物理内存
  3. **共享**：同一物理页可映射进多个进程（共享库、mmap 文件）
  4. **交换/回收**：不用的页可驱逐到磁盘

## 二、页表与 MMU

### 1. 翻译过程

```
虚拟地址 → MMU 查页表 → 物理地址
每个进程一套页表（进程切换时换页表基址寄存器 CR3/TTBR）
```

- 页大小通常 4KB；64 位地址空间页表巨大 → 用**多级页表**（x86-64 四级：PML4→PDPT→PD→PT→Offset）
- 多级的好处：稀疏地址空间只建用到的中间表（进程地址空间大部分空洞不占内存）
- **THP（Transparent Huge Page）**：2MB 大页，减少页表项数 + TLB 命中率提升（HugeTLB 显式配置）

### 2. TLB（Translation Lookaside Buffer）

- 页表查询慢（多级内存访问），TLB 缓存最近用过的 VA→PA 映射
- TLB miss 代价大：要查多级页表（可能触发硬件遍历/软件填表）
- 大页减少页表项 → TLB 覆盖更多内存 → 为什么大页对大数据集性能关键
- 进程切换时 TLB 部分失效（ASID 隔离可避免全刷）→ 上下文切换的间接成本（衔接第三十一轮）

- **来源**：kernel-internals + Columbia + Kernel 官方
- **可信度**：S

---

## 三、VMA 与缺页

### 1. VMA（Virtual Memory Area）

- 进程地址空间按用途切成段：代码段、数据段、堆、栈、各 mmap 区域，每个是一个 VMA（红黑树组织）
- VMA 记录：起止地址、权限（r/w/x）、映射类型（文件/匿名/设备）、偏移、共享属性
- /proc/<pid>/maps 就是 VMA 列表的可读形式

### 2. 缺页异常（Page Fault）

- 访问的虚拟页还没映射物理页 → CPU 触发 page fault → 内核处理：
  - **major fault（主缺页）**：页在磁盘（文件/交换区），要读盘 → 慢（毫秒级）
  - **minor fault（次缺页）**：页已在内存（共享页、刚分配过），只要建映射 → 快（微秒级）
- **demand paging（按需分页）**：mmap/加载程序时只建 VMA 不分配物理页，真正访问才 fault —— 这就是为什么程序启动后 RSS 远小于虚拟大小
- **COW（Copy-on-Write，写时复制）**：fork 时父子共享所有物理页（只读映射），谁写谁 fault → 复制该页再写。fork 因此接近零成本，代价是首次写慢

### 3. /proc 观测

- /proc/<pid>/statm（虚拟/常驻）、/proc/<pid>/smaps（每 VMA 明细）、ps -o majflt,minflt
- perf stat page-faults、bcc tools（faults、mmapcount）观测

- **来源**：Columbia + devweekends + CSDN
- **可信度**：S

---

## 四、物理内存分配：伙伴系统

### 1. Buddy Allocator（伙伴系统）

- 核心数据结构：**按 order（2^order 页）分组的空闲链表**（order 0..10，即 4KB..4MB）
- 分配：从请求的最小 order 找，没有则拆大块（高阶→低阶拆分）
- 释放：归还后检查"伙伴"（buddy，物理相邻同 order）是否也空闲 → **合并**回高阶
- 特性：
  - 分配/释放 O(1)（链表头操作 + 合并检查）
  - 追求**物理连续**（DMA 需要）
  - 代价：**外部碎片**——长时间运行/频繁申请释放后，没有足够大的连续块（虽然高阶块会合并，但分散的 allocation 无法合并）

### 2. GFP 标志（分配行为）

```
GFP_KERNEL：常规内核分配，可睡眠、可触发回收
GFP_ATOMIC：中断/原子上下文，不可睡眠（没有可用的页就直接失败）
GFP_HIGHUSER/GFP_DMA：特定 zone
```

- 中断上下文分配是程序员经常踩的坑（spinlock 持有时也不能睡眠）→ 与并发调研衔接

- **来源**：Kernel 官方 memory-allocation + systems-handbook + CSDN
- **可信度**：S

---

## 五、对象分配：slab/slub

### 1. 为什么需要

- 内核反复分配同类型对象（task_struct、dentry、inode、文件对象）
- 伙伴系统按页分配太粗（一个 512B 对象也占 4KB 页 → 内部碎片）
- 每次分配/释放都走伙伴系统太慢

### 2. Slab/SLUB 机制

- 为每种对象类型建一个**缓存（cache）**：预分配若干页，切成等大小对象
- 空闲对象用 free list 串起来，分配 O(1) 取一个，释放 O(1) 归还
- SLUB 是现代默认（简化了 slab 的彩色/复杂队列）；SLOB 是极简嵌入版
- **每 CPU 局部缓存**：每个 CPU 有自己的空闲对象池，避免锁竞争（per-CPU 思想，衔接第八轮）
- 内核的"内存池"模式，与用户态的内存池/分配器（第五十一轮之后的 C++ 定制分配器）异曲同工

- **来源**：systems-handbook + CSDN + minzkn
- **可信度**：A+

---

## 六、kmalloc / vmalloc / kvmalloc

| API | 物理连续性 | 适用 | 限制 |
|---|---|---|---|
| kmalloc / kmem_cache_alloc | 物理连续 | 小对象、DMA | 最大约 4MB，GFP 控制行为 |
| vmalloc | 虚拟连续、物理可散 | 大块（模块、缓冲） | 访问有 TLB 开销（页表条目多），不能 DMA |
| alloc_pages / __get_free_pages | 物理连续页 | 大块、页级 | order 上限（MAX_ORDER 默认 10） |
| kvmalloc | 先试 kmalloc 失败降级 vmalloc | 大小皆可 | 内核 4.12+ 推荐通用入口 |

- 用户态对照：malloc 大块（>128KB）走 mmap，小块走堆（brk/arena）——第 17 轮已讲
- 内核 API 设计体现的工程思想：**按用途选分配器，而不是"统一万能分配器"**——可作 C++ 定制 allocator 的教学参照

- **来源**：Kernel 官方 + minzkn + CSDN
- **可信度**：S

---

## 七、内存回收与 OOM

### 1. 回收（Reclaim）

- 物理内存不够时，内核回收页：脏页写回（Page Cache，衔接第三十轮）、匿名页交换（swap）、只读页直接丢弃（重新从文件读）
- **LRU 列表**：每类型页维护 LRU，从尾端回收
- **kswapd**：后台内核线程，水位低于 low 时异步回收；同步回收（direct reclaim）是最后手段（分配线程自己回收，很慢）

### 2. OOM Killer

- 回收都失败 → 选一个进程杀掉（oom_score 按内存占用/存活时长等评分）
- 对应用的意义：**内存不足不等于 malloc 返回 null**（overcommit + OOM 杀手）——这就是为什么内存分配要"有界/可观测"，与 C++ 工程中控制内存峰值呼应

### 3. 内存压缩（Compaction）与移动页

- 为满足高阶连续分配，把已分配页移动（moveable 页），腾出连续区 → 缓解外部碎片
- 页的可移动性标注（movable/reclaimable）由 GFP 标志决定

- **来源**：Kernel 官方 + CSDN + 综合
- **可信度**：A+

---

## 八、知识网络

```
Linux 内存管理
├── 虚拟内存抽象（隔离/按需/共享/交换）
├── 页表（多级 4 级/THP 大页）
├── MMU + TLB（ASID、大页提升命中）
├── VMA（地址空间分段、红黑树、/proc/maps）
├── 缺页（major/minor、demand paging、COW）
├── 物理分配
│   ├── 伙伴系统（order、拆分/合并、碎片）
│   ├── slab/slub 对象缓存（per-CPU、free list）
│   └── kmalloc/vmalloc/kvmalloc 选择
├── GFP 标志（KERNEL/ATOMIC）
└── 回收（LRU、kswapd、swap、OOM killer、compaction）
```

---

## 九、本轮最重要的资料

1. **Linux Kernel 官方 MM Concepts / Physical Memory / Memory Allocation**（S）——权威基线
2. **kernel-internals.org Memory Management: The Story**（S）——虚拟内存抽象的教学叙述
3. **Columbia CS Linux Paging**（S）——页表/VMA/反向映射体系
4. **systems-handbook Linux Memory Management**（A+）——分配栈分层清晰
5. **CSDN Linux 内存管理深度解析**（A）——kmalloc/vmalloc/GFP 中文总结

## 十、适合进入 CPP-Bible 的原子

- "虚拟内存：进程为什么以为自己独占 128TB"（SYS）
- "按需分页与 COW：为什么 fork 快、为什么 RSS 和 VSZ 不一样"（SYS，实验：fork 后观测 RSS/缺页）
- "伙伴系统与 slab：内核的两级分配哲学"（SYS/ALGO，可与 C++ 定制分配器对照）
- "mmap：文件映射的内存视角"（SYS/PERF，与第三十轮 Page Cache 衔接）
- "kmalloc/vmalloc：为什么没有万能分配器"（ENG 工程哲学）
- 实验：观测 /proc/self/statm、majflt/minflt、mmap 大文件后 RSS 变化——全部可本机验证

## 十一、与已有调研的关联

- 第十七轮用户态内存（栈/堆/malloc arena）：本轮补内核侧
- 第三十轮文件系统：Page Cache 写回/脏页/fsync 由本轮的回收机制驱动
- 第五十轮 CPU：TLB 缺失、大页、上下文切换的地址空间切换
- 第三十一轮调度：进程切换 = 地址空间切换 + TLB 开销
- 第八轮 per-CPU 数据：slab 的 per-CPU 缓存同思想

## 十二、下一轮方向

链接器深度（重定位/COMDAT/ICF/LTO）或 TCP/拥塞控制。

---

*本轮新增知识节点：虚拟内存、virtual memory、页表、page table、多级页表、PML4、MMU、TLB、ASID、大页、THP、HugeTLB、VMA、/proc/maps、缺页、page fault、major fault、minor fault、按需分页、demand paging、COW、写时复制、伙伴系统、buddy allocator、order、外部碎片、GFP、GFP_KERNEL、GFP_ATOMIC、slab、slub、kmem_cache、per-CPU 缓存、kmalloc、vmalloc、kvmalloc、alloc_pages、MAX_ORDER、内存回收、reclaim、LRU、kswapd、swap、OOM killer、compaction、movable 页、overcommit、RSS、VSZ、statm、smaps。补齐了"Linux 内存管理"域核心空白。*
