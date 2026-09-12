# 资料研究第六十二轮：Linux 内核源码精读——调度器/内存/文件系统关键路径走读（__schedule、伙伴系统、ext4 写路径）

> 2026-09-11，底层工程资料研究员。主题：内核阅读的最小路径集（调度/分配/IO 三条主线）、schedule()→__schedule() 调用链拆解（preempt_disable→pick_next→context_switch）、CFS 的 pick_next_task_fair 与 vruntime 红黑树、页分配路径 __alloc_pages（zone/伙伴系统/快速路径）、ext4 写路径（page cache→jbd2 事务→块层）、sched_debug/proc 观察工具、给 CPP-Bible 读者的内核阅读路线（跟随函数而非目录）。
> 检索方式：general_search + Linux Kernel 官方 CFS 设计文档 + mozengtao Linux scheduler deep dive（schedule/__schedule 源码行号级）+ minzkn 调度器与 CFS 源码走读 + IBM CFS 深入 + Gorman 物理页分配（mm/page_alloc.c）+ CSDN 调度流程。
> **内核源码域第一轮（全新域）**。与 60 调度器（概念）、51 内存管理（概念）、64 文件系统（概念）衔接——本轮是"概念 → 代码"的落地。

---

## 一、内核阅读的最小路径集

概念轮（60/51/64）给了地图，本轮选三条**最小路径**从函数级走通：

| 主线 | 关键函数 | 回答什么 |
|---|---|---|
| 调度 | schedule() → __schedule() | CPU 如何换任务 |
| 分配 | __alloc_pages() | 内存从哪来 |
| IO | ext4 写路径 | 数据如何落盘 |

- 方法：**跟随一个请求的调用链，不按目录读**（75 轮方法论的内核版）
- 工具：/proc/sched_debug、ftrace、perf——内核也有"动态阅读"

## 二、调度路径：schedule() → __schedule()

```
schedule()                          kernel/sched/core.c
├── sched_submit_work()             提交待处理的块 IO（睡眠前先落盘）
└── __schedule()                    核心调度函数
    ├── preempt_disable()           禁止抢占（调度本身不可抢占）
    ├── rq_lock()                   拿当前 CPU 运行队列锁
    ├── 更新 prev 任务状态（信号挂起则 TASK_RUNNING，否则睡眠）
    ├── pick_next_task()            选下一个任务 ← CFS 的核心
    ├── context_switch()            切换地址空间 + 寄存器（切换 CPU 上下文）
    └── preempt_enable()            恢复可抢占
```

- **CFS 的 pick_next_task_fair()**：从 vruntime 红黑树取最左节点（vruntime 最小 = 最"欠" CPU 的任务）——CFS 设计文档原话：运行一点→vruntime 增加→左移→被公平替换
- 简单路径与组调度路径分离（pick_next_task_fair 优化路径）——**内核也做"快路径"优化**（衔接 50 轮 CPU 的快速路径思想）
- context_switch：地址空间（mm）切换 + 线程切换（switch_to 宏）——这就是"进程切换"的全部

- **来源**：mozengtao 源码行号走读 + minzkn + 官方 sched-design-CFS.txt
- **可信度**：S

---

## 三、页分配路径：__alloc_pages()

```
__alloc_pages()                     mm/page_alloc.c
├── 快速路径：从当前 zone 的 per-cpu 页列表取（无锁、无扫描）
├── 伙伴系统：按 2^n 阶取块（不够则向上分裂大块）
├── 回收路径：kswapd / 直接回收（dirty 页写回、清 cache）
└── OOM：杀死进程（最后手段）
```

- **快路径优先**：per-cpu 页列表（每 CPU 私有，免锁）→ 伙伴系统（锁在 zone）→ 回收 → OOM——**四层降级**是理解分配性能的钥匙
- 伙伴系统的本质：2^n 页块按阶分类，分配时分裂、释放时合并（51 轮概念 → 这里看到代码）
- 观察：/proc/buddyinfo 显示各阶空闲块——教学实验可以直接看
- **来源**：Gorman（mm/page_alloc.c 源码讲解）+ 51 轮概念
- **可信度**：S

## 四、ext4 写路径：从 write() 到磁盘

```
write(fd, buf, n)
→ 通用写：copy_from_user → 写入页缓存（dirty 页标记）
→ 后台：flush 线程把 dirty 页写出
  → ext4 层：分配块（extent 映射）→ 更新 inode
  → jbd2：事务开始 → 元数据写入日志 → 提交点（commit）
  → 块层：bio 提交 → 磁盘 DMA
```

- **关键认知**：write() 返回 ≠ 数据落盘——只写到了页缓存（64 轮"日志≠安全"的代码级版本）
- 数据安全层级：页缓存 → fsync（强制刷盘）→ O_DIRECT（绕过缓存）——三个层次的 API 语义
- jbd2 事务：ordered 模式保证"元数据提交前数据已落盘"（64 轮概念 → 这里看到代码）

## 五、给 CPP-Bible 读者的内核阅读路线

1. **别读全内核**：三条路径（调度/分配/IO）足够建立"内核如何工作"的心智模型
2. **跟随函数不跟目录**：schedule() → __schedule() → pick_next_task() → context_switch()，一条链走到底
3. **用 /proc 和 ftrace 验证**：跑实验看数据（sched_debug、buddyinfo、perf）——内核也有"证据链"精神
4. **版本锚定**：内核 API 变化快，阅读时固定版本（如 6.x）——与本项目"版本边界"纪律同源

## 六、知识网络

```
内核源码
├── 调度：schedule → __schedule → pick_next_task_fair → context_switch
├── 分配：__alloc_pages → per-cpu 页 → 伙伴系统 → 回收 → OOM
├── IO：write → 页缓存 → ext4 extent → jbd2 事务 → bio → DMA
├── 方法：跟随函数、快路径优先、/proc+ftrace 验证
└── 纪律：版本锚定、最小路径集
```

---

## 七、本轮最重要的资料

1. **Linux Kernel 官方 sched-design-CFS.txt**（S）——设计权威
2. **mozengtao Linux scheduler deep dive**（S）——schedule/__schedule 源码行号
3. **Gorman Physical Page Allocation**（S）——__alloc_pages 源码
4. **minzkn CFS 源码走读**（A+）——pick_next_task_fair 细节
5. **IBM Inside CFS**（A）——经典讲解

## 八、适合进入 CPP-Bible 的原子

- "schedule 三件套：拿锁、选任务、切上下文"（OS/ENG）
- "per-cpu 页列表：免锁快路径"（OS/PERF，衔接分配器轮）
- "write() 返回 ≠ 落盘：页缓存的语义"（OS/ENG，fsync/O_DIRECT）
- "四层降级：分配失败的处理阶梯"（OS 工程）
- 实验：读 /proc/sched_debug + buddyinfo 解释观察结果

## 九、与已有调研的关联

- 第六十轮调度器概念 → 本轮代码落地
- 第五十一轮内存管理 → __alloc_pages 代码
- 第六十四轮文件系统 → ext4 写路径代码
- 第七十一轮分配器：用户态 malloc ↔ 内核页分配的四层降级对照
- 第七十轮调试器：内核调试（kgdb/ftrace）是同一技能

## 十、下一轮方向

缓存一致性协议与内存屏障（MESI/store buffer/TSO vs ARM 弱序）。

---

*本轮新增知识节点：__schedule、schedule()、pick_next_task、pick_next_task_fair、vruntime、红黑树、context_switch、switch_to、__alloc_pages、per-cpu 页列表、伙伴系统、zone、kswapd、OOM、buddyinfo、ext4 写路径、页缓存、dirty 页、flush 线程、extent、jbd2 事务、bio、DMA、fsync、O_DIRECT、ftrace、sched_debug、kgdb、快路径、版本锚定。补齐了"内核源码精读"域核心空白。*
