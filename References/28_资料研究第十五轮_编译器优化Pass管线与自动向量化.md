# 资料研究第十五轮：编译器优化 Pass 管线与自动向量化

> 2026-09-11，底层工程资料研究员。主题：LLVM/GCC 优化 pass 管线、关键 pass 详解（Inline/LICM/GVN/DCE）、-O 级别对比、自动向量化（Loop Vectorizer + SLP）与成本模型。
> 检索方式：general_search + LLVM 官方 Passes 文档 + LLVM 开发者大会演讲 + arXiv 2026 量化研究 + GCC 官方优化选项文档。
> **编译器域第三轮**（第十三轮 UB 与优化原理、第十四轮 LTO/PGO/BOLT/Sanitizer，本轮 pass 管线与向量化）。

---

## 一、LLVM Pass 管线结构

### 1. 三层管线

```
模块级（Module）
├── 早期简化（Early Simplification）
│   ├── SimplifyCFG（控制流图简化）
│   ├── SROA（Scalar Replacement of Aggregates，结构体拆分到寄存器）
│   └── EarlyCSE（早期公共子表达式消除）
│
├── CGSCC（Call Graph SCC，后序遍历）
│   └── 重复运行（内联后暴露更多优化机会）：
│       ├── Inliner（函数内联）
│       └── 函数简化管线（Function Simplification Pipeline）
│
├── 函数简化管线（buildFunctionSimplificationPipeline）
│   ├── SROA → SimplifyCFG → InstCombine → Reassociate
│   ├── GVN（全局值编号）→ DCE（死代码消除）
│   └── LICM（循环不变代码外提）
│
└── 模块优化管线（buildModuleOptimizationPipeline）
    ├── 全局 DCE、全局优化
    └── 循环变换/向量化：
        ├── loop-rotate（循环旋转）
        ├── indvars（归纳变量规范化）
        ├── loop-vectorize（循环向量化）
        ├── loop-unroll（循环展开）
        └── SLP vectorizer（超字级并行向量化）
```

- **来源**：LLVM 2023 开发者大会 "A Whirlwind Tour of the LLVM Optimizer"（Popov）+ TUM 大学编译原理讲义
- **可信度**：S

### 2. Pass 顺序的非平凡交互

- 内联必须在 GVN/LICM **之前**——内联后函数体可见，才能做跨函数的冗余消除和循环外提
- 向量化在循环展开**之前**——向量化需要原始循环结构来分析依赖
- 有些 pass **重复运行**——前面的 pass 创造了新的优化机会（如内联后 InstCombine 又能简化）
- arXiv 2026 论文 "A Multi-Dimensional, Per-Pass Empirical Study" 量化了每个 pass 的影响：
  - **LICM 是变化最大的 pass**：cycles -47% 到 +70%（取决于程序），LLC 可达 +295%
  - loop-rotate 和 indvars 均匀有益（指令数 -7~11%，能耗 -8~9%）
- **来源**：arXiv 2606.31238（2026）
- **可信度**：A+

---

## 二、关键 Pass 详解

### 1. Mem2Reg / SROA（SSA 构造）

- **Mem2Reg**：把 `alloca`（栈变量）提升为寄存器，构造 SSA 形式。插入 phi 节点处理多分支赋值
- **SROA**（Scalar Replacement of Aggregates）：把结构体/数组的 alloca 拆分成标量，进一步提升到寄存器
- 这是所有后续优化的基础——没有 SSA，GVN/DCE 等都无法高效工作
- **可信度**：S

### 2. InstCombine（指令组合）

- 把复杂指令序列规范化/简化为更简单的形式
- 例如：`(x + 0) → x`、`(x * 1) → x`、`(x & x) → x`、`(a & b) | (a & c) → a & (b | c)`
- 是 LLVM 中最大的 pass 之一（数千条模式匹配规则）
- 运行频率极高——几乎每个其他 pass 后都会跑一次 InstCombine
- **可信度**：S

### 3. DCE / ADCE（死代码消除）

- **DCE**：SSA 下非常简单——结果没有使用者的指令就是死的，直接删除
- **ADCE**（Aggressive DCE）：反向思维——假设所有指令都死，从有副作用的指令（store/call/return）反向标记活的，剩下的删除
- **来源**：LLVM Passes 官方文档
- **可信度**：S

### 4. GVN（Global Value Numbering，全局值编号）

- 给"必定产生相同结果"的表达式分配相同的值编号
- 哈希公式：`hash = opcode + operand_value_numbers`（Click 1995, PLDI）
- 如果两个表达式值编号相同，后面的可以替换为前面的结果（消除冗余计算）
- 也做冗余 load 消除（基于 MemorySSA）
- LLVM NewGVN 用 Rosen/Wegman/Zadeck 1988 稀疏公式
- **示例**：
  ```
  %x = add i32 %a, %b
  %y = mul i32 %x, 3
  %z = add i32 %a, %b   ; 和 %x 值编号相同 → 替换为 %x
  ```
- **可信度**：S（LLVM 官方文档 + 经典论文）

### 5. LICM（Loop Invariant Code Motion，循环不变代码外提）

- 把循环中**操作数不随迭代变化**的计算提到循环前置块（preheader）
- 也可以把只在退出路径使用的计算下沉到退出块（sinking）
- 依赖：支配分析（DominatorTree）+ 别名分析（AliasAnalysis）
- 还能把 must-alias 的内存位置提升到寄存器（promotion）
- **算法**：
  1. 遍历函数中所有循环
  2. 识别循环不变指令（所有操作数在循环外定义）
  3. 检查是否安全外提（无副作用、不抛异常）
  4. 移到 preheader
  5. 重复直到没有可外提的指令
- **来源**：LLVM LICM.cpp 源码注释 + 实现教程
- **可信度**：S

### 6. Inline（函数内联）

- 把函数调用替换为函数体，消除调用开销
- 有**成本模型**：估算内联后的代码大小增长 vs 性能收益，超过阈值不内联
- 内联是"使能优化"——内联后暴露跨函数的 GVN/LICM/向量化机会
- CGSCC 管线中内联和函数简化**重复运行**，因为一次内联可能创造新的内联机会
- **可信度**：S

### 7. Loop Unroll（循环展开）

- 把循环体复制多份，减少迭代次数和分支开销
- 暴露更多 ILP（指令级并行）
- 可能增加代码大小（-Os 禁用）
- **可信度**：A

---

## 三、-O 级别对比

| 级别 | 目标 | 关键特征 | 代码大小 | 编译时间 |
|---|---|---|---|---|
| **-O0** | 调试 | 无优化，1:1 源码对应 | 最大 | 最快 |
| **-O1** | 基础 | 常量传播、DCE、简单分支优化、帧指针合并 | 减小 | 略增 |
| **-O2** | 标准 | 大部分优化（devirtualize、thread-jumps、align-functions、GCSE），不含激进大小/速度权衡 | 可能增大 | 显著增加 |
| **-O3** | 激进 | -O2 + 自动向量化 + 循环展开 + 函数克隆 + 更激进内联 | 显著增大 | 最多 |
| **-Os** | 大小 | 类似 -O2 但禁用增加代码大小的优化 | 最小 | 类似 -O2 |
| **-Oz** | 最小大小 | Clang 特有，更激进（不内联） | 更小 | 类似 -O2 |
| **-Ofast** | 极速 | -O3 + -ffast-math（允许非标准浮点） | 最大 | 最多 |

### -O2 具体开启的 flag（GCC 官方）

```
-fthread-jumps, -falign-functions, -falign-jumps, -falign-loops,
-falign-labels, -fcaller-saves, -fcrossjumping, -fcse-follow-jumps,
-fcse-skip-blocks, -fdelete-null-pointer-checks, -fdevirtualize,
-fdevirtualize-speculatively, -fexpensive-optimizations, -fgcse,
-fgcse-lm, -fpeephole2, -fschedule-insns, -ftree-pre, -ftree-vrp,
-finline-functions（仅在 -O3）...
```

### -O3 在 -O2 基础上额外开启

```
-finline-functions（跨函数内联，不只是 static）
-funswitch-loops（循环外提条件）
-fpredictive-commoning
-fgcse-after-reload
-ftree-loop-distribute-patterns
-ftree-slp-vectorize（SLP 向量化）
-ftree-vectorize（循环向量化）
```

### 重要警告

> **-O3 不保证比 -O2 更快**——它可能因为代码膨胀导致 i-cache miss 增加，反而变慢。数值计算/向量化友好的代码可能显著加速，但一般代码 -O2 往往更稳。

- **来源**：GCC 官方优化选项文档 + Federico Busato C++ 性能优化讲义
- **可信度**：S

---

## 四、自动向量化（Auto-Vectorization）

### 1. 两个向量化器

| 维度 | Loop Vectorizer | SLP Vectorizer |
|---|---|---|
| 全称 | Loop Vectorizer | Superword-Level Parallelism |
| 加入时间 | 2012（LLVM 3.2） | 2013 年 4 月 |
| 处理对象 | 循环 | 直线代码（基本块内的独立标量操作） |
| 方法 | 把循环迭代打包成向量操作 | 自底向上把相邻独立操作打包成向量 |
| 覆盖范围 | 单个循环 | 多个基本块（树、菱形、循环） |
| 启用级别 | -O3（或 -O2 + -ftree-vectorize） | -O3（Clang 在 -O2 也启用 SLP） |

### 2. Loop Vectorizer 工作流程

```
1. 合法性检查（Legality）
   ├── 循环携带依赖？→ 不能向量化
   ├── 指针别名？→ 不能证明不重叠就不能向量化
   ├── 复杂控制流？→ 可能需要 if-conversion
   └── 不可向量化的类型/调用？→ 不能

2. 成本模型（Cost Model）
   ├── 计算不同向量化因子（VF=1,2,4,8,16...）的成本
   ├── 计算不同展开因子（UF）的成本
   ├── 选总成本最低的 VF+UF 组合
   └── 支持固定宽度（SSE/AVX）和可伸缩宽度（SVE/RVV）

3. 生成向量代码
   ├── 向量操作（<8 x i32> 等）
   ├── 标量尾声（处理剩余元素）
   └── 运行时别名检查（如果无法编译期证明不重叠）
```

### 3. 为什么循环不能向量化（五大原因）

| 原因 | 说明 | 解决方案 |
|---|---|---|
| **循环携带依赖** | 上一次迭代的结果被下一次读取（如 `a[i] = a[i-1] + 1`） | 重构算法、用前缀和 |
| **指针别名** | 无法证明两个指针不重叠（如 `void f(int *a, int *b)`） | `__restrict__` 关键字 |
| **复杂控制流** | 循环内有 if/switch，数据路径不统一 | if-conversion、简化控制流 |
| **不可向量化操作** | 函数调用、递归、不可向量化的类型 | 内联函数、拆出循环 |
| **不规则内存访问** | gather/scatter（间接寻址 `a[b[i]]`）成本高 | 数据布局优化、SOA |

### 4. 诊断工具（极其有用）

```bash
# 成功向量化的循环
clang -O3 -Rpass=loop-vectorize program.cpp

# 向量化失败的循环及原因
clang -O3 -Rpass-missed=loop-vectorize program.cpp

# 向量化分析信息
clang -O3 -Rpass-analysis=loop-vectorize program.cpp

# 强制向量化宽度（调试用）
clang -O3 -mllvm -force-vector-width=8 program.cpp
```

### 5. 成本模型的细节

- 向量化不是"免费的"——需要考虑：
  - 向量指令本身的成本（通常比标量便宜，但不是 1/N）
  - 数据重排成本（shuffle、permute）
  - 标量尾声成本
  - 运行时别名检查成本
  - 寄存器压力（向量化用更多向量寄存器）
- 如果成本模型判断向量化后更慢，**不向量化**
- 2024 LLVM 技术演讲讨论了成本模型的平局处理（preferFixedOverScalableIfEqualCost）和 RISC-V 的采纳
- **来源**：LLVM Vectorizers 官方文档 + LLVM 2024 技术演讲 "Loop Vectorization: how good is it?"
- **可信度**：S

---

## 五、知识网络

```
编译器优化 Pass 管线与向量化
├── Pass 管线结构
│   ├── 早期简化（SimplifyCFG/SROA/EarlyCSE）
│   ├── CGSCC（Inliner + 函数简化，重复运行）
│   ├── 函数简化（InstCombine/GVN/DCE/LICM）
│   └── 模块优化（全局 DCE + 循环变换/向量化）
│
├── 关键 Pass
│   ├── SROA（结构体拆分到寄存器）
│   ├── InstCombine（指令规范化，最大的 pass）
│   ├── DCE/ADCE（死代码消除）
│   ├── GVN（全局值编号，冗余计算消除）
│   ├── LICM（循环不变代码外提，变化最大的 pass）
│   ├── Inline（函数内联，使能优化）
│   └── Loop Unroll（循环展开）
│
├── -O 级别
│   ├── -O0（无优化）
│   ├── -O1（基础）
│   ├── -O2（标准，devirtualize/GCSE）
│   ├── -O3（激进，向量化/展开/克隆）
│   ├── -Os/-Oz（大小优化）
│   └── -Ofast（-O3 + fast-math）
│
└── 自动向量化
    ├── Loop Vectorizer（循环向量化）
    │   ├── 合法性检查（依赖/别名/控制流）
    │   ├── 成本模型（VF/UF 选择）
    │   └── 运行时别名检查
    ├── SLP Vectorizer（超字级并行）
    │   └── 直线代码中的独立标量操作打包
    ├── 不能向量化的五大原因
    └── 诊断工具（-Rpass/-Rpass-missed）
```

---

## 六、本轮最重要的 10 个资料

| # | 资料 | 级别 | 核心价值 |
|---|---|---|---|
| 1 | LLVM Passes 官方文档 | S | 所有 pass 的权威定义 |
| 2 | LLVM 2023 "Whirlwind Tour of the LLVM Optimizer" | S | pass 管线的完整导览 |
| 3 | LLVM Vectorizers 官方文档 | S | 向量化器的权威说明 |
| 4 | GCC 官方优化选项文档 | S | -O 级别具体开启哪些 flag |
| 5 | arXiv 2026 "Per-Pass Empirical Study" | A+ | 每个 pass 的量化影响（LICM 变化最大） |
| 6 | LLVM LICM.cpp 源码注释 | S | LICM 的精确实现描述 |
| 7 | LLVM 2014 "Auto-Vectorization in LLVM"（Golin） | A+ | SLP/Loop 向量化器的设计历史 |
| 8 | LLVM 2024 "Loop Vectorization: how good is it?" | A | 成本模型最新进展 |
| 9 | "Why Your Compiler Cannot Vectorize That Loop" | A | 五大原因的实用总结 |
| 10 | TUM 大学编译原理讲义（LLVM 优化） | A | 学术视角的 pass 管线讲解 |

## 七、强烈建议深入研究的 5 个资料

1. **LLVM Passes 官方文档**——逐个读 pass 的定义和示例
2. **LLVM 2023 "Whirlwind Tour" 演讲**——理解 pass 之间的顺序和交互
3. **LLVM Vectorizers 文档 + `-Rpass-missed` 实战**——用诊断工具看自己的循环为什么没向量化
4. **arXiv 2026 Per-Pass 量化研究**——理解每个 pass 对性能的真实影响（不是所有 pass 都有益）
5. **GCC 优化选项文档**——查 -O2/-O3 具体开启了哪些 flag

## 八、适合直接进入 CPP-Bible 的资料

| 资料 | 进入方式 | 目标原子/章节 |
|---|---|---|
| Pass 管线结构 | "编译器怎么一步步优化你的代码" | 编译器域原子 |
| LICM/GVN/Inline 详解 | "三个最重要的优化 pass" | 编译器域原子 |
| -O 级别对比 | "-O2 和 -O3 到底差在哪" | PERF/TOOL 交叉 |
| 自动向量化五大原因 | "为什么你的循环没有被向量化" | PERF 域原子 |
| -Rpass 诊断工具 | "怎么看编译器做了什么优化" | TOOL 域原子 |

## 九、对 CPP-Bible 的工程升级建议

1. **TOOL 域新增"编译器优化诊断"专题**——`-Rpass`/`-Rpass-missed`/`-Rpass-analysis` 系列，教学生看编译器做了什么优化、为什么没做
2. **PERF 域新增"自动向量化"原子**——Loop Vectorizer + SLP + 五大不能向量化原因 + `__restrict__` 解决方案
3. **证据卡新增"优化诊断"字段**——每张性能类证据卡附 `-Rpass-missed` 输出，证明编译器确实做了/没做某个优化
4. **编译器域新增"Pass 管线"原子**——从 SROA → InstCombine → GVN → LICM → 向量化的完整流程，用 `clang -S -emit-llvm -O2` 观察 IR 变化
5. **-O3 警告写入 M2 实证方法**——"-O3 不保证比 -O2 快，性能类实验必须同时报告 -O2 和 -O3 结果"

## 十、发现的知识空白

1. **编译器 pass 管线完全空白**——项目用 -O2 但没有讲解编译器内部做了什么
2. **自动向量化空白**——PERF 域没有向量化相关原子
3. **-O 级别对比空白**——学生不知道 -O2 和 -O3 的具体区别
4. **优化诊断工具空白**——`-Rpass` 系列是极好的教学工具但完全没提
5. **GVN/LICM 等经典 pass 空白**——编译原理核心内容

## 十一、下一轮推荐搜索方向

1. **C++ 异常实现（换域到运行时）**——零开销异常、表驱动展开、libunwind、异常性能开销、`-fno-exceptions`
2. **动态链接与加载（换域到系统）**——PLT/GOT、延迟绑定、符号解析、ld.so、符号可见性
3. **SIMD intrinsics 与手写向量化（换域到体系结构）**——SSE/AVX/AVX-512/NEON、intrinsics 编程、编译器自动向量化 vs 手写
4. **CMake 构建系统（换域到工程工具链）**——target 模型、generator 表达式、大型项目组织
5. **编译器前端（换域到编译原理）**——词法/语法分析、AST、语义分析、模板实例化（两阶段查找）

---

*本轮新增知识节点：Pass 管线、CGSCC、SROA、InstCombine、GVN、全局值编号、DCE、ADCE、LICM、循环不变代码外提、preheader、Inline、成本模型、Loop Unroll、-O0/-O1/-O2/-O3/-Os/-Oz/-Ofast、devirtualize、函数克隆、自动向量化、Loop Vectorizer、SLP Vectorizer、超字级并行、向量化因子 VF、展开因子 UF、循环携带依赖、指针别名、`__restrict__`、-Rpass 诊断、if-conversion。补齐了"编译器优化 pass 管线"和"自动向量化"两大空白——这是理解 -O2 到底做了什么的核心一轮。*
