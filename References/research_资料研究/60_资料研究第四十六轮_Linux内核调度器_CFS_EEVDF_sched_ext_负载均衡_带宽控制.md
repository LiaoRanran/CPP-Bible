# 资料研究第四十六轮：Linux 内核调度器——CFS、EEVDF、sched_ext、负载均衡、带宽控制、实时/截止时间类

> 2026-09-11，底层工程资料研究员。主题：调度器的目标（公平/响应/吞吐/实时保证）、CFS 的 vruntime 红黑树设计、**EEVDF 对 CFS 的替代**（Linux 6.6，lag/eligible 概念）、调度类层次（RT/DL/CFS/IDLE）、cgroup 公平分组与带宽控制（quota/period 硬限制）、负载均衡（per-CPU runqueue、拉取 vs 推送）、sched_ext（eBPF 可编程调度器）、可观测性（/proc/schedstat、sched_debug）。
> 检索方式：general_search + Linux Kernel 官方文档（sched-design-CFS、sched-eevdf.rst）+ CSDN 调度子系统从 rq 到 EEVDF + minzkn CFS 带宽控制。
> **操作系统调度域第二轮**。第一轮：31 实时调度与分时调度（理论层）。与 44 嵌入式 RTOS 调度、58 轮未编号（上轮收官）衔接。

---

## 一、调度器要解决的问题

调度器回答：**"CPU 只有一个，下一微秒给谁？"**

| 目标 | 问题 |
|---|---|
| 公平 | 同优先级任务均分 CPU（不能饿死） |
| 响应 | 交互任务（编辑器/终端）及时唤醒 |
| 吞吐 | 计算任务满负荷跑（减少切换开销） |
| 实时保证 | 截止时间前必须完成（DL） |
| 组公平 | 容器/cgroup 之间按配额分（不是按任务数） |

Linux 用**调度类（scheduling class）**分层实现：RT > DL > CFS(FAIR) > IDLE，高优先级类有可运行任务时低优先级类让位。

## 二、CFS（Completely Fair Scheduler）：vruntime 红黑树

### 1. 核心思想

- **vruntime（虚拟运行时间）**：任务实际运行时间按权重归一化（权重高的任务 vruntime 增长慢 → 分到更多 CPU）
- 调度决策 = **选 vruntime 最小的任务**（红黑树最左节点，O(log n)）
- 目标：逼近"理想多任务硬件"（无限个 CPU 同时跑所有任务）

### 2. 关键机制

- **sched_period / sched_latency**：一个周期内所有可运行任务至少各跑一次
- **权重（nice 值）**：nice 从 -20 到 +19，映射到 weight 表——CFS 的"权重"直接决定 vruntime 增长速度
- **组调度（cgroup）**：CONFIG_FAIR_GROUP_SCHED 把任务分组，公平性作用在"组"上（组内再按组递归）——容器 CPU 隔离的实现基础
- **带宽控制**：cgroup 的 cpu.max = quota/period（如 50000/100000 = 半核），quota 耗尽 → 整组节流（throttled），防止超额

### 3. 问题

- CFS 的"选 vruntime 最小"是贪心：对**时延敏感**任务不够好（刚唤醒的任务 vruntime 小会插队，也可能被新任务反复插队）
- 惩罚/补偿机制（wakeup preemption）靠启发式参数，行为难预测

- **来源**：Linux Kernel 官方 CFS 文档 + minzkn
- **可信度**：S

---

## 三、EEVDF：Linux 6.6 起的接班人

### 1. 背景

- CFS 的 vruntime 只保证"长期公平"，对短时间窗的延迟没有形式化保证
- EEVDF = **Earliest Eligible Virtual Deadline First**（最早"合格"虚拟截止时间优先），源自 1995 年论文（P. S. Rao 等），被 Peter Zijlstra 引入 Linux

### 2. 核心概念

- **lag（滞后）**：任务相对"公平份额"的欠账。lag > 0 = 还欠它 CPU（欠账）；lag < 0 = 它多用了（透支）
- **eligible（合格）**：任务的虚拟时间 ≥ 它的"应得时间"才算合格——防止新任务无限插队
- **虚拟截止时间（virtual deadline）**：从"合格"集合里选**虚拟截止时间最早**的任务（而非像 CFS 直接选 vruntime 最小）
- 效果：**延迟有界、公平可证明**，且新任务/唤醒任务的插队行为有形式化规则

### 3. 为什么比 CFS 好

| | CFS | EEVDF |
|---|---|---|
| 选择依据 | vruntime 最小（贪心） | 合格集中虚拟截止时间最早 |
| 延迟保证 | 启发式 | 形式化（lag/deadline） |
| 新任务插队 | 容易反复插队 | 必须"合格"才可入选 |
| 公平性 | 长期统计 | 每时刻可计算（lag 显式） |

### 4. 与 DL 类的关系

- SCHED_DEADLINE（dl 类）：CBS（Constant Bandwidth Server）——每个任务有 runtime/deadline/period，按绝对截止时间选——EEVDF 是"尽力而为"侧的相似思想（公平共享 + 有界延迟），dl 类是硬实时保证

- **来源**：Kernel sched-eevdf.rst（官方）+ CSDN
- **可信度**：S

---

## 四、负载均衡

- 每个 CPU 有自己的 runqueue（per-CPU rq）——**共享 runqueue 会有锁竞争**
- 负载均衡：周期性地/事件驱动地把任务从重载 CPU **拉取（pull）**到轻载 CPU（work stealing 思想，衔接 39 轮无锁/工作窃取）
- 依据：各 rq 的**负载贡献（load_avg）**（不是瞬时长度，是衰减历史——PELT，per-entity load tracking）
- NUMA 感知：任务尽量留在原节点（memory locality），跨节点迁移有代价——调度与内存布局强耦合

## 五、sched_ext：用 eBPF 写调度器

- Linux 6.12 合入的 **sched_ext**：调度策略用 eBPF 程序实现（内核只提供基础设施）
- 意义：
  - 调度器从"内核配置开关"变成"可编程组件"——公司可针对自家工作负载写调度策略
  - 孵化新调度思想（如 Google 的 scx_lavd 等）而不用改内核
  - 与 52 轮 eBPF 网络（XDP）同一技术底座：**把内核策略用户态可编程化**
- 代价：eBPF 程序质量决定系统行为，需严格测试（实时性系统慎用）

## 六、可观测性与调试

- `/proc/schedstat`：每 CPU 统计（运行/等待/迁移）
- `sched_debug`：每任务 vruntime/lag/权重 明细
- `perf sched`：调度事件分析（wait time / 唤醒延迟）
- cgroup cpu.stat：throttled 次数——"CPU 明明空闲但程序很慢"的排查入口

## 七、知识网络

```
Linux 调度器
├── 调度类：RT（FIFO/RR）> DL（CBS）> CFS/EEVDF（FAIR）> IDLE
├── CFS：vruntime、红黑树、权重/nice、组调度、带宽控制
├── EEVDF：lag、合格集、虚拟截止时间、有界延迟
├── 负载均衡：per-CPU rq、pull、PELT load_avg、NUMA 感知
├── sched_ext：eBPF 可编程调度器
└── 观测：schedstat、sched_debug、perf sched、cpu.stat
```

---

## 八、本轮最重要的资料

1. **Linux Kernel sched-design-CFS（官方）**（S）——CFS 设计权威
2. **Kernel sched-eevdf.rst（官方）**（S）——EEVDF 设计文档
3. **CSDN 调度子系统从 rq 到 EEVDF**（A+）——rq/EEVDF 全貌中文
4. **minzkn CFS 带宽控制**（A）——quota/period 机制

## 九、适合进入 CPP-Bible 的原子

- "调度器在做什么：从公平到实时的一族算法"（OS/ALGO）
- "vruntime：用虚拟时钟把权重变成可比数值"（OS，衔接 31 轮理论）
- "EEVDF vs CFS：从启发式到可证明公平"（OS/演进案例）
- "cgroup 带宽控制：配额怎么硬限制 CPU"（OS 工程）
- "per-CPU 队列与负载均衡：无共享数据的并行"（OS/CONC，衔接 39 轮）

## 十、与已有调研的关联

- 第三十一轮调度：实时调度理论（RMS/EDF）是这轮的内核落地
- 第四十四轮 RTOS：FreeRTOS 抢占式调度与 Linux 调度类对照
- 第五十二轮 eBPF：sched_ext 与 XDP 同底座
- 第五十轮 CPU 微架构：调度的硬件基础（cache/NUMA）
- 第五十三轮无锁：runqueue 无锁化与工作窃取

## 十一、下一轮方向

数据库查询执行（火山模型/向量化/优化器）。

---

*本轮新增知识节点：Linux 调度器、调度类、CFS、vruntime、红黑树、nice、权重、组调度、cgroup、带宽控制、quota、period、throttled、EEVDF、lag、eligible、虚拟截止时间、sched_ext、eBPF 调度器、负载均衡、per-CPU runqueue、pull、PELT、load_avg、NUMA 感知、SCHED_DEADLINE、CBS、/proc/schedstat、sched_debug、perf sched。补齐了"内核调度器实现"域核心空白。*
