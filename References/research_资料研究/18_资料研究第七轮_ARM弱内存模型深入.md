# 资料研究第七轮：ARM 弱内存模型深入——从 ARMv7 到 ARMv8 的演化与屏障指令

> 2026-09-11，底层工程资料研究员。主题：ARM 弱内存模型深入。
> 检索方式：web.fetch 一手来源（learn.arm.com / kernel.org / Cambridge / ACM）+ general_search。

---

## 一、核心资料（S/A+ 级）

### 1. ARM Architecture Reference Manual：AArch64 Application Level Memory Model

- **类型**：架构规范（权威定义）
- **来源**：ARM 官方
- **链接**：ARM ARM §B2（The AArch64 Application Level Memory Model）
- **核心内容**：ARMv8 内存模型的正式定义。**关键事实：ARM ARM 中的描述是 `aarch64.cat` 文件的转写——aarch64.cat 才是权威定义**。
- **解决的问题**：ARM CPU 上内存访问的顺序规则
- **为什么重要**：**这是 ARM 内存模型的"宪法"**。而且 ARM 用形式化模型（cat 文件）作为权威定义，文字描述只是转写——这是"形式化优先于散文"的典范。
- **技术亮点**：
  - **ARMv8 是 multi-copy atomic (MCA)**：一个写如果被某个观察者看到，就必须被所有观察者看到（除了写者自己可以提前看到自己的写）
  - **ARMv7 是非 MCA**：写可以先对某些线程可见再对其他线程可见——但 ARMv8 改了，因为非 MCA 的硬件优化收益不足且带来复杂性
  - **允许所有四种重排**：Load-Load、Load-Store、Store-Store、Store-Load 都可以重排（x86 只允许 Store-Load）
  - **为 C/C++11 SC-DRF 设计**：Will Deacon（ARM 首席工程师）明确说"Explicitly designed with C/C++11 (SC-DRF) in mind"
- **与 C++ 的关系**：C++ `memory_order_acquire` 编译为 LDAR，`memory_order_release` 编译为 STLR，`memory_order_seq_cst` 编译为 LDAR+STLR 或 DMB
- **与 CPP-Bible 的关系**：CONC 域"ARM 内存模型"章节的权威来源；与第五轮 herd7/aarch64.cat 直接衔接
- **可以放入哪个章节**：part09_concurrency、part17_cpu
- **适合讲什么**：弱内存模型、multi-copy atomicity、ARM 屏障指令
- **可以设计什么实验**：用 herd7 对比 x86-TSO.cat 和 aarch64.cat 的同一个 litmus test，看哪些执行在 ARM 上允许但 x86 上不允许
- **历史背景**：ARMv7 非 MCA → ARMv8 改为 MCA（2011 年 ARMv8 发布时确定）
- **可信度**：S（ARM 官方架构手册）
- **教材价值**：S

### 2. Cambridge 论文：Simplifying ARM Concurrency（ARMv8 为什么改成 MCA）

- **类型**：学术论文（POPL 2017）
- **来源**：University of Cambridge（Peter Sewell 团队）
- **链接**：https://www.repository.cam.ac.uk/bitstream/handle/1810/274172/top_openaccess.pdf
- **作者**：Christopher Pulte、Shaked Flur、Will Deacon（ARM）等
- **核心内容**：解释 ARMv8 为什么从非 multi-copy atomic 改成 multi-copy atomic：
  - 非 MCA 允许写先对某些线程可见再对其他线程可见（"其他线程可以看到不同的写顺序"）
  - 但这种能力在生产实现中从未被利用
  - 对应的硬件优化收益在 ARM 上下文中不足
  - 非 MCA 与其他 ARMv8 特性结合时产生微妙的复杂性
  - 因此 ARMv8 架构被修订为 MCA 模型，并简化了其他部分
- **为什么重要**：**这是"架构简化"的经典案例**——去掉一个理论上更强但实际没人用的特性，换来模型的简洁和可推理。这和 C++ 标准化的"先最小可用"策略异曲同工。
- **技术亮点**：
  - 非 MCA 的 IRIW（Independent Reads of Independent Writes）测试可以有非常反直觉的结果
  - MCA 让"本地推理"成为可能——不需要分析整个多线程程序
  - ARMv8 还引入了更强的内存访问（LDAR/STLR）和更弱的屏障（DMB LD/DMB ST）
- **可信度**：S（POPL 论文 + ARM 首席工程师合著）
- **教材价值**：A+

### 3. ARM 屏障指令体系（DMB / DSB / ISB / LDAR / STLR）

- **类型**：架构指令文档
- **来源**：ARM 官方 + Microsoft OldNewThing + 多方确认
- **核心内容**：ARM 内存屏障分三层，从轻到重：

| 指令 | 作用 | 是否停流水线 | 典型用途 |
|---|---|---|---|
| **DMB**（Data Memory Barrier） | 保证内存访问顺序 | 否（只告诉内存控制器保序） | 普通数据同步 |
| **DSB**（Data Synchronization Barrier） | 保证顺序 + 等所有 prior 内存访问完成 | 是（停流水线） | cache/TLB 维护后、异常返回前 |
| **ISB**（Instruction Synchronization Barrier） | 刷新指令流水线 | 是（最重） | 系统寄存器修改、上下文切换、代码自修改 |

每种都有域限定：
- `SY`：全系统
- `ISH`：Inner Shareable（SMP 内核常用）
- `ST`：只影响 store（DMB ST / DSB ST）
- `LD`：只影响 load（DMB LD）

**轻量 acquire/release 指令**（ARMv8 引入，比 DMB 轻量）：
- `LDAR`：load-acquire——此 load 之后的所有内存访问不能重排到它之前
- `STLR`：store-release——此 store 之前的所有内存访问不能重排到它之后
- LDAR+STLR 配对实现 RCsc（roach motel 语义：可以进不能出）

- **为什么重要**：**这是"屏障不是只有一种"的最佳教学案例**。x86 只有 mfence/lfence/sfence 三种，ARM 有 DMB/DSB/ISB × 多种域限定 + LDAR/STLR，层次更丰富。
- **与 C++ 的关系**：C++ 原子操作的内存序在 ARM 上编译为这些指令——`memory_order_acquire` → LDAR，`memory_order_release` → STLR，`memory_order_seq_cst` → LDAR+STLR（或 DMB）
- **教学价值**：S

---

## 二、其他高价值资料（A 级）

### 4. Will Deacon：Formalising the Armv8 memory consistency model

- **类型**：技术演讲幻灯片
- **来源**：kernel.org（Will Deacon，ARM 首席工程师，Linux 内核 maintainer）
- **链接**：https://www.kernel.org/pub/linux/kernel/people/will/slides/mm-openshmem-2018.pdf
- **核心内容**：
  - ARMv8 是弱序的，需要特殊指令恢复 SC
  - 明确为 C/C++11 (SC-DRF) 设计
  - 依赖类型：Control（控制依赖）、Data（数据依赖）、Address（地址依赖）
  - LDAR/STLR 是 RCsc（roach motel 语义）
- **教学价值**：ARM 首席工程师亲自讲的内存模型，和 Linux 内核的实际使用结合。

### 5. Apple M1 内存模型分析论文

- **类型**：学术论文（2024）
- **来源**：Leibniz Universität Hannover
- **链接**：https://www.sra.uni-hannover.de/Publications/2024/wrenger_24_jsa.pdf
- **核心内容**：实测分析 Apple M1 的内存序行为。M1 是 ARMv8 实现，MCA，但实际实现可能比架构规范更强（允许更少的重排）。
- **教学价值**：**"架构规范 vs 实际实现"的差异**——ARM CPU 可能比规范更强（允许更少重排），这不是违规。但代码不能依赖实现的强顺序，因为换一个 CPU 就可能崩。

### 6. ARM 同步原语案例（LDAR/STLR 实战）

- **类型**：官方教程
- **来源**：learn.arm.com
- **链接**：https://learn.arm.com/learning-paths/servers-and-cloud-computing/memory_consistency/examples/
- **核心内容**：用 LDAR/STLR 实现自旋锁、message passing 等同步原语，对比用 DMB 的实现。
- **教学价值**：acquire/release 指令的实际使用，和 C++ `memory_order_acquire/release` 直接对应。

### 7. x86 vs ARM 内存模型对比

- **类型**：技术博客
- **来源**：Jonathan Beard（2026）
- **核心内容**：
  - x86-TSO：只允许 Store-Load 重排，其他三种不允许
  - ARM：允许所有四种重排
  - x86 的 load 自带 acquire、store 自带 release（免费）
  - ARM 需要显式 LDAR/STLR 或 DMB
- **教学价值**："x86 能跑 ARM 失败"的根本原因——x86 的强模型掩盖了内存序错误。

---

## 三、核心概念：multi-copy atomicity

```
multi-copy atomic (MCA)：
  线程 A 写 x=1
  如果线程 B 看到了 x=1
  那么所有其他线程也必须看到 x=1（除了 A 自己可以提前看到）

非 MCA（ARMv7 / Power）：
  线程 A 写 x=1
  线程 B 可能看到 x=1
  但线程 C 可能还看到 x=0
  （写传播到不同线程的时间可以不同）
```

**IRIW 测试**（Independent Reads of Independent Writes）是区分 MCA 和非 MCA 的经典 litmus test：
- P0: x=1; P1: y=1; P2: r1=x; r2=y; P3: r3=y; r4=x
- 问：P2 看到 (1,0) 且 P3 看到 (0,1) 可能吗？
- MCA：不可能（如果 x=1 被 P2 看到，那 P3 也必须看到 x=1）
- 非 MCA：可能（写传播顺序可以不同）

**ARMv8 改成 MCA 的意义**：让程序员可以"本地推理"——不需要分析整个多线程程序的全局写传播顺序。

---

## 四、x86 vs ARM 重排允许矩阵

| 重排类型 | x86-TSO | ARMv8 | 说明 |
|---|---|---|---|
| Load → Load | ❌ 不允许 | ✅ 允许 | x86 load 不重排 |
| Load → Store | ❌ 不允许 | ✅ 允许 | x86 load 不重排 |
| Store → Store | ❌ 不允许 | ✅ 允许 | x86 store 不重排（store buffer 保序） |
| Store → Load | ✅ 允许 | ✅ 允许 | 两者都允许（store buffer 延迟） |

**结论**：x86 只有 Store→Load 一种重排（因为 store buffer），ARM 四种全允许。这就是为什么 x86 上能跑的并发代码迁到 ARM 经常出问题——x86 的强模型免费提供了 acquire/release 语义。

---

## 五、C++ 内存序 → ARM 指令映射

| C++ memory_order | ARM 指令 | 说明 |
|---|---|---|
| `relaxed` | 普通 LDR/STR | 无屏障 |
| `acquire`（load） | LDAR | load-acquire |
| `release`（store） | STLR | store-release |
| `acq_rel`（RMW） | LDAR + STLR | 原子读改写 |
| `seq_cst` | LDAR + STLR（+ DMB 可选） | RCsc，全局全序 |
| `atomic_thread_fence(release)` | DMB ST | 只保 store 顺序 |
| `atomic_thread_fence(acquire)` | DMB LD | 只保 load 顺序 |
| `atomic_thread_fence(seq_cst)` | DMB SY | 全屏障 |

---

## 六、知识网络

```
ARM 弱内存模型
├── 架构演化
│   ├── ARMv7：非 MCA（写传播可不同步）
│   └── ARMv8：MCA（写传播同步，简化模型）
│       └── 为 C/C++11 SC-DRF 设计
│
├── 重排允许
│   ├── 四种全允许（vs x86 只允许 Store-Load）
│   └── 依赖保留：控制/数据/地址依赖不重排
│
├── 屏障指令
│   ├── DMB（最轻，只保序，不停流水线）
│   │   ├── DMB SY / ISH / ST / LD
│   ├── DSB（保序 + 等完成，停流水线）
│   ├── ISB（最重，刷新指令流水线）
│   └── LDAR/STLR（轻量 acquire/release）
│
├── 形式化定义
│   ├── aarch64.cat（权威定义）
│   └── ARM ARM §B2（cat 的转写）
│
└── 与 C++ 的关系
    ├── acquire → LDAR
    ├── release → STLR
    ├── seq_cst → LDAR+STLR
    └── fence → DMB
```

---

## 七、本轮最重要的 10 个资料

| # | 资料 | 级别 | 核心价值 |
|---|---|---|---|
| 1 | ARM ARM §B2 内存模型 | S | 权威定义，aarch64.cat 优先 |
| 2 | Cambridge Simplifying ARM Concurrency | S | ARMv8 为什么改成 MCA |
| 3 | ARM 屏障指令体系 | S | DMB/DSB/ISB/LDAR/STLR 完整分层 |
| 4 | Will Deacon 形式化演讲 | A+ | ARM 首席工程师视角 |
| 5 | Apple M1 内存模型分析 | A | 架构规范 vs 实际实现 |
| 6 | ARM LDAR/STLR 实战教程 | A | acquire/release 指令使用 |
| 7 | x86 vs ARM 重排矩阵 | A | "x86 能跑 ARM 失败"根因 |
| 8 | aarch64.cat（第五轮） | S | 形式化模型文件 |
| 9 | herd7/litmus7（第五轮） | S | 验证工具 |
| 10 | PostgreSQL 编译器屏障 bug（第四轮） | S | 只在非 x86 触发的真实 bug |

## 八、强烈建议深入研究的 5 个资料

1. **Cambridge Simplifying ARM Concurrency 论文**——理解 MCA vs 非 MCA 的本质区别
2. **ARM ARM §B2**——读 aarch64.cat 的权威定义
3. **Will Deacon 演讲幻灯片**——ARM 首席工程师的实际视角
4. **ARM 官方 LDAR/STLR 教程**——跟着做 acquire/release 实验
5. **Apple M1 论文**——理解架构规范和实现的差异

## 九、适合直接进入 CPP-Bible 的资料

| 资料 | 进入方式 | 目标原子/章节 |
|---|---|---|
| ARM 内存模型 | "ARM 弱内存模型"章级内容 | CONC/CPU 交叉 |
| x86 vs ARM 重排矩阵 | 直接作为对比表 | CONC 域 |
| 屏障指令分层 | "屏障不是只有一种"pitfall | CONC 域原子 |
| ARMv7→ARMv8 MCA 演化 | "架构简化"历史案例 | HIST 域 |
| C++ 内存序→ARM 指令映射 | 编译原理教学 | CONC/编译器交叉 |

## 十、对 CPP-Bible 的工程升级建议

1. **CONC 域新增"跨架构内存模型"章节**——x86-TSO vs ARMv8 vs Power 的对比，重排允许矩阵
2. **"x86 能跑 ARM 失败"的可复现实验**——用 herd7 对比两个架构的 cat 模型，MP 测试在 ARM 上 (1,0) 可能、x86 上不可能
3. **屏障指令分层教学**——DMB/DSB/ISB/LDAR/STLR 的层次，对应 C++ 内存序
4. **"架构规范 vs 实现"教学**——Apple M1 比规范更强，但代码不能依赖

## 十一、发现的知识空白

1. **ARM 内存模型完全未覆盖**——全书只讲 C++ 内存模型，不讲硬件内存模型
2. **multi-copy atomicity 概念缺失**——这是理解弱内存模型的核心概念
3. **屏障指令分层无内容**——只讲 C++ fence，不讲底层 DMB/DSB/ISB
4. **x86 vs ARM 对比无实验**——没有跨架构的可复现对比
5. **架构演化（ARMv7→ARMv8）无案例**——MCA 简化是重要的架构决策

## 十二、下一轮推荐搜索方向

1. **seqlock / per-CPU 数据结构**——Linux 其他读多写少同步机制，与 RCU 对比
2. **无锁数据结构正确性验证工具**——CDSChecker、Relacy、GenMC
3. **KCSAN（Kernel Concurrency Sanitizer）**——Linux 内核动态数据竞争检测，与 TSan 对比
4. **STL 域源码调研**——std::sort / std::vector / std::unordered_map 实现细节（换域）
5. **C++26 reflection / contracts**——C++26 其他重要特性（换域）
6. **Power 内存模型**——比 ARM 更弱（非 MCA），极端案例

---

*本轮新增知识节点：multi-copy atomicity、ARMv7 非 MCA、ARMv8 MCA、DMB/DSB/ISB、LDAR/STLR、aarch64.cat 权威定义、重排允许矩阵、C++→ARM 指令映射。补齐了 CONC 域"硬件内存模型"和"跨架构对比"两个空白。七轮调研覆盖并发域从理论到硬件、从语言到架构的完整层次。*
