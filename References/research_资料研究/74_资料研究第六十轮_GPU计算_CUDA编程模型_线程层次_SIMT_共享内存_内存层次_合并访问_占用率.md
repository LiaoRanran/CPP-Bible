# 资料研究第六十轮：GPU 计算——CUDA 编程模型、线程层次、SIMT、共享内存、内存层次、合并访问、占用率

> 2026-09-11，底层工程资料研究员。主题：CUDA 三大抽象（线程层次/共享内存/屏障同步）、Thread→Warp(32)→Block→Grid 组织、SIMT 执行模型（warp 锁步 vs 分支发散）、GPU 内存层次（寄存器/共享/全局/本地）、合并内存访问（coalesced access）与 bank conflict、占用率（occupancy）与性能、kernel 启动与网格分派、GPU 与 CPU 体系结构的本质差异（吞吐 vs 延迟）、CUDA 教学价值（SIMD 的跨代进化）。
> 检索方式：general_search + NVIDIA CUDA C++ Programming Guide 官方 + eunomia-bpf basic-cuda-tutorial（GPU 架构教程）+ NVIDIA CUDA Performance Optimization 白皮书 + ziababar cheat sheet + anaumghori 执行模型笔记 + epicure CUDA Deep Dive。
> **GPU 计算域第一轮（全新域）**。与 28 GPU 图形（渲染管线）、33 SIMD、50 CPU 微架构直接衔接——CUDA 是"吞吐优先"体系结构的编程视图。

---

## 一、CUDA 三大抽象（官方原话）

> "核心是三个关键抽象：线程组层次、共享内存、屏障同步"

1. **线程层次**：kernel 启动后组织为 Grid → Block → Thread（可 1D/2D/3D 索引）
2. **共享内存**：Block 内所有线程可见、与 Block 同生命周期（片上、极快）
3. **屏障同步**：__syncthreads() 让 Block 内线程在共享数据交换点对齐

```
Thread（最小执行单元）
  ↓ ×32
Warp（线程束——真实执行单元！）
  ↓ ×N
Thread Block（线程块，共享内存 + 同步单位）
  ↓ ×M
Grid（一次 kernel 启动的全部线程）
```

- **关键认知**：你编程写 Thread，但 GPU 真正执行的是 **Warp（32 线程一组）**——写代码的心态必须建立在这个事实上（eunomia 教程明确："even though you program individual threads, the GPU executes them in groups of 32"）

## 二、SIMT：吞吐优先的执行模型

- **SIMT（Single Instruction, Multiple Threads）**：Warp 内 32 线程**同时执行同一条指令**，但各自有独立寄存器/指令地址/分支能力
- 与 SIMD 对比（CPU）：SIMD 是"一条指令操作 8 个数据"；SIMT 是"一条指令驱动 32 个线程"——**理念同源、组织不同**（CPU 隐藏延迟用乱序，GPU 用海量线程并行）
- **分支发散（warp divergence）**：if/else 两分支都要执行（一侧被掩蔽）→ 性能减半——**发散是 GPU 编程头号性能杀手**
- 锁步语义：Warp 内线程"同时开始同地址"，可独立分支（NVIDIA 文档）

## 三、内存层次（对照 CPU）

| 层级 | 归属 | 延迟 | 用途 |
|---|---|---|---|
| 寄存器 | 单线程 | 最低 | 局部变量 |
| 共享内存 | Block | 几十周期 | **线程间协作数据**（手动管理！） |
| 全局内存 | Grid | 数百周期 | 主数据（kernel 进出） |
| 本地内存 | 单线程（溢出） | 慢 | 寄存器溢出/数组局部 |

- **共享内存是显式管理的缓存**：CPU 缓存自动、GPU 共享内存手控——"load once, reuse many"（anaumghori：数据从全局加载一次到共享，多次本地复用）
- 对应 CPU 体系：共享内存 ≈ L1 缓存的位置，但**程序员手动控制**——这是 GPU 编程与 CPU 的最大思维差异

## 四、性能三定律

### 1. 合并访问（Coalesced Access）

- 一个 Warp 同时访问全局内存，硬件**合并成最少的事务**（32 线程的连续地址 = 1 次大传输）
- 不连续（跨步）访问 → 多个事务 → 带宽浪费——**访问模式决定带宽利用率**（写代码就要想"相邻线程访问相邻地址"）

### 2. Bank Conflict（共享内存）

- 共享内存分 32 个 bank，同一指令多线程访问**同一 bank** 的不同地址 → 串行化（冲突）
- 解法：padding（+1 偏移）打散映射——经典技巧

### 3. 占用率（Occupancy）

- 每个 SM 能驻留的 Warp 数/上限 = 占用率——**用海量线程隐藏全局内存延迟**（GPU 无乱序执行，靠换线程）
- 限制因素：寄存器数/共享内存大小（用多了 → 驻留 warp 少 → 隐藏延迟能力下降）
- 权衡：每线程寄存器 vs 占用率——优化的经典张力（CUDA Performance Optimization 白皮书）

## 五、Kernel 启动与分派

- `kernel<<<grid, block>>>(args)`：一次性声明所有线程（Grid 维数）
- 调度：Block 分派到 SM（任意顺序、可并发可串行）→ SM 把 Block 拆 Warp 调度执行
- 数据流：H2D 拷贝 → kernel → D2H 拷贝（PCIe/显存带宽是瓶颈——**数据传输往往比计算贵**）

## 六、与 C++ 的关系

- CUDA 是 C++ 扩展（__global__/__device__/<<<>>>）——编译器把 kernel 编译为 GPU SASS（衔接 35 轮编译器：同一编译器前后端哲学）
- 现代异构：SYCL/HIP 跨厂商抽象、cuBLAS/cuDNN 库层、tensor cores（AI 矩阵运算）
- 教学价值：**CUDA 把"并行思维"显式化**——相比 CPU 多线程，GPU 强制你想清数据布局与访问模式（对 CPP-Bible 读者是高级并行教材）

## 七、知识网络

```
GPU/CUDA
├── 三抽象：线程层次 / 共享内存 / 屏障同步
├── 执行：Warp=32、SIMT、分支发散
├── 内存：寄存器/共享/全局/本地 + 合并访问
├── 性能：coalescing、bank conflict、occupancy
├── 调度：Grid→Block→SM→Warp
└── 生态：SYCL/HIP、cuBLAS、tensor core
```

---

## 八、本轮最重要的资料

1. **NVIDIA CUDA C++ Programming Guide**（S）——权威（warp/SIMT 定义）
2. **NVIDIA CUDA Performance Optimization 白皮书**（S）——内存层次/占用率
3. **eunomia-bpf basic-cuda-tutorial**（A+）——GPU 架构简明教程
4. **ziababar cheat sheet**（A）——概念速查
5. **epicure CUDA Deep Dive**（A）——warp 机制图

## 九、适合进入 CPP-Bible 的原子

- "Warp：你写线程，GPU 跑线程束"（GPU/ARCH）
- "SIMT vs SIMD：吞吐优先的执行哲学"（GPU，衔接 SIMD 轮）
- "合并访问：相邻线程访问相邻地址"（GPU/PERF）
- "共享内存：程序员手动管理的缓存"（GPU，与 CPU 缓存对照）
- "占用率：用线程数隐藏延迟"（GPU/PERF，与乱序执行对照）
- 实验：矩阵乘法三版（朴素 → 共享内存 → 合并访问）

## 十、与已有调研的关联

- 第三十三轮 SIMD：CPU 向量化的 GPU 侧对应
- 第五十轮 CPU 微架构：延迟隐藏的两种策略（乱序 vs 线程）
- 第二十八轮 GPU 图形：渲染管线 vs 计算 kernel
- 第六十三轮 AI 编译器：XLA 把算子编译到 GPU（tensor core）
- 第七十三轮列存：SIMD 扫描与 GPU 加速分析同源

## 十一、下一轮方向

大型 C++ 代码库阅读方法论（Chromium/LLVM）。

---

*本轮新增知识节点：CUDA、GPU 计算、kernel、Grid、Block、Thread、Warp、线程束、SIMT、分支发散、warp divergence、共享内存、shared memory、全局内存、本地内存、合并访问、coalesced access、bank conflict、占用率、occupancy、SM、流处理器、屏障同步、__syncthreads、H2D、D2H、tensor core、cuBLAS、cuDNN、SYCL、HIP、SASS、PTX、PCIe 带宽、延迟隐藏、吞吐优先。补齐了"GPU 计算"域核心空白。*
