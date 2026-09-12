# 资料研究第四十轮：构建系统——Ninja、CMake 生成器、依赖图、增量构建、ccache、Bazel、统一构建

> 2026-09-11，底层工程资料研究员。主题：构建系统的层级（元构建 vs 底层构建）、Ninja 的设计哲学（最小语法、依赖图、并行调度、depfile）、CMake 的 Ninja 生成器、增量构建的正确性（.ninja_log、mtime/内容哈希）、ccache/sccache 编译缓存、Bazel/Meson 的沙箱与远程执行、unity build、大型工程构建时间的工程实践。
> 检索方式：general_search + Ninja 官方 manual（权威）+ CMake Ninja generator 官方 + pkglog 构建系统对比 + x-cmd ninja + Wasil Zafar CMake generators + dr-sergey Ninja 实战 + engincancicek unity build。
> **工程工具链域第二轮**。第一轮：21 CMake。与第三十八轮链接器（链接时间）、第三十二轮编译器（编译开销）、第五十二轮 lld（并行架构）强关联。

---

## 一、构建系统的分层

| 层 | 角色 | 代表 |
|---|---|---|
| 元构建（Meta-build） | 写人类可读的高层描述，生成底层构建文件 | CMake、Meson、Bazel（自带执行）、GN |
| 底层构建（Low-level） | 高效执行依赖图，只管"哪个目标依赖哪个输入，命令怎么跑" | Ninja、Make、Bazel（内部） |
| 编译缓存 | 按输入哈希复用已编译产物 | ccache、sccache |
| 远程/分布式 | 把编译任务分发到多机 | Bazel Remote Execution、IncrediBuild、FastBuild |

核心思想：**人类决策（配置）与机器执行（调度）分离**——CMake 负责所有"应该怎么编"的决策，Ninja 只负责"以最小代价重编"。这就是 Ninja 官方自称"最小必要功能"的原因：它的语法刻意贫瘠，复杂逻辑全部留给生成器。

## 二、Ninja 的设计哲学

### 1. 三个核心概念

```
build output: inputs
    command = cc -c input.c -o output
    depfile = output.d        # 编译器的头文件依赖写这里
```

- **目标（build 语句）**：输出文件 ← 输入文件 + 命令
- **依赖图（DAG）**：所有 build 语句组成图，Ninja 按图调度
- **restat/depfile**：编译器生成的真实依赖（头文件列表）通过 depfile 汇入，保证**精确依赖**

### 2. 为什么快

| 特性 | Make | Ninja |
|---|---|---|
| 解析启动 | 每次重新解析大 Makefile | 极简二进制格式，毫秒级 |
| 依赖 | 文件 mtime 启发式 | .ninja_log + depfile 精确 |
| 并行 | 手动 -j | 自动按依赖图智能并行（默认全部核心） |
| 增量判定 | 粗糙 | 精确到单个输入变化 |
| 典型加速 | 基线 | 大型项目 2-10x |

- Ninja 不提供配置语言（没有 if/循环/宏）——**这不是缺陷，是设计**：所有决策由 CMake 之类生成器一次做完，Ninja 只执行，从而解析极快、行为可预测

### 3. 增量构建的正确性

- 判定重编：输入 mtime/哈希 比输出新，或输出被删
- `.ninja_log` 记录上次构建的命令与状态，Ninja 据此跳过未变化的命令（甚至跳过"输出比输入新但命令变了"的检查，通过 restat 逻辑）
- 头文件依赖（#include 变化）由 depfile 捕获 → 改一个头文件只重编真正 include 它的文件

- **来源**：Ninja 官方 manual（权威）+ x-cmd + dr-sergey
- **可信度**：S

---

## 三、CMake 与 Ninja 生成器

- CMake 的生成器家族：Unix Makefiles（默认）、Ninja（现代推荐）、Visual Studio 工程、Xcode、Eclipse 等
- `cmake -G Ninja -B build` → 生成 build.ninja
- 优点：
  - 配置期信息全部提前固化（编译器路径、flag、生成器表达式求值）
  - 并行度自动（Ninja 默认所有核心）
  - 支持显式/隐式依赖、order-only 依赖、pool（限制并行，如链接池）
- CMake 3.30+ 支持并行 install；跨平台生成器一致性好

- **来源**：CMake Ninja generator 官方 + Wasil Zafar + CSDN
- **可信度**：S

---

## 四、编译缓存：ccache/sccache

- 原理：把"预处理结果 + 编译器版本 + 编译参数"做哈希，命中则直接复制缓存的目标文件，不真正编译
- 关键点：**同一份输入+参数必得同一份输出**（编译器确定性）——所以缓存安全的根基是"编译是纯函数"
- ccache 本地缓存；sccache（Mozilla）支持远程缓存（S3/Redis），CI 间共享
- 局限：头文件重编的跨文件场景（改了头，所有依赖 TU 的输入哈希都变，缓存全失效）——所以 LTO/unity build/头文件最小化是配套手段
- CI 里是**构建时间的头号杠杆**（结合 GitHub Actions cache）

- **来源**：pkglog + engincancicek
- **可信度**：A+

---

## 五、Bazel/Meson 与现代构建思想

### 1. Bazel（Google）

- 更重的元构建：**沙箱执行**（每个 action 在隔离环境，输入输出声明式）→ 可复现、可缓存、可远程分发
- **内容寻址缓存**：输出按输入内容哈希寻址，任何机器命中即复用
- 远程执行：把 action 发给集群（+ 分布式调度），工程级加速
- 代价：学习曲线陡、配置繁琐、对 Windows 支持一般（RBE 生态以 Linux 为主）

### 2. Meson

- 更现代的元构建：声明式、快（Python 写核心但生成 Ninja）、默认覆盖测试/安装
- 哲学与 Ninja 一致：决策在元层，执行在 Ninja

### 3. Unity Build（统一构建）

- 把多个 .cpp 合并成一个"大翻译单元"再编译（CMAKE_UNITY_BUILD）
- 收益：头文件解析次数剧降、内联机会增多 → 构建快（可数倍）
- 代价：编译单元间命名冲突、调试/增量粒度变粗、LTO 交互复杂

- **来源**：pkglog + engincancicek + 综合
- **可信度**：A+

---

## 六、大型工程构建时间实践（对本项目最实用）

1. **依赖最小化**：头文件里少 include（用前置声明）、pimpl——头文件是构建时间的隐藏炸弹
2. **增量优先**：Ninja + depfile 精确追踪，避免"改了头全量重编"
3. **缓存兜底**：ccache/sccache 命中率目标 >90%（本机 + CI）
4. **并行上限**：链接/内存密集任务用 pool 限流（避免 OOM）
5. **按需构建**：只编测试需要的目标；不用的目标不编
6. **CI 分层**：快速门禁（lint/单测）与全量构建分离
7. **模块化**：物理/逻辑模块划分，降低跨模块头依赖（衔接大型工程架构）

## 七、知识网络

```
构建系统
├── 分层：元构建（CMake/Meson/Bazel）→ 底层（Ninja/Make）→ 缓存（ccache）→ 远程
├── Ninja
│   ├── 最小语法（build/rule/command/depfile）
│   ├── 依赖图 DAG 与并行调度
│   ├── .ninja_log 增量判定
│   └── restat/depfile 精确依赖
├── CMake 生成器（Make/Ninja/VS/Xcode）
├── ccache/sccache（编译=纯函数，哈希复用）
├── Bazel（沙箱、内容寻址缓存、远程执行）
├── Meson（声明式 + Ninja 后端）
└── Unity Build（合并 TU、头解析复用）
```

---

## 八、本轮最重要的资料

1. **Ninja 官方 Manual**（S）——语法/哲学/restat 权威
2. **CMake Ninja Generator 官方文档**（S）——生成器行为
3. **pkglog 构建系统对比（CMake/Make/Ninja/Meson）**（A+）——中文系统对照
4. **Wasil Zafar CMake Mastery Part26**（A）——生成器切换实操
5. **dr-sergey Ninja 实战**（A）——Make vs Ninja 量化对比

## 九、适合进入 CPP-Bible 的原子

- "Ninja 为什么快：最小语法与依赖图调度"（TOOL/ENG）
- "增量构建的正确性：depfile 与 mtime 的坑"（TOOL，实验可复现）
- "ccache：为什么编译可以当纯函数缓存"（TOOL，工程哲学）
- "头文件是构建时间的隐形炸弹：include 成本"（TOOL/ENG，配合 22 轮编译过程）
- "Bazel 沙箱：可复现构建的代价"（ENG 架构案例）

## 十、与已有调研的关联

- 第二十一轮 CMake：target 模型/generator 表达式——本轮补执行层
- 第三十八轮链接器：链接是构建图里的一个节点，ld 性能决定构建时间
- 第三十二轮编译器：编译开销决定增量粒度
- 第五十二轮 lld 并行：与 Ninja 并行调度同哲学（消除全局状态、并发调度）
- CI（本项目 GitHub Actions）：ccache 是 CI 提速第一杠杆

## 十一、下一轮方向

GC 深度（分代/标记清除/并发收集）或 TCP/拥塞控制。

---

*本轮新增知识节点：构建系统、元构建、meta-build、Ninja、depfile、restat、.ninja_log、依赖图、DAG、增量构建、incremental build、mtime、CMake 生成器、generator、ccache、sccache、编译缓存、内容哈希、Bazel、沙箱执行、内容寻址缓存、远程执行、Meson、Unity Build、统一构建、编译池、pool、前置声明、pimpl、include 成本。补齐了"构建系统/工程效率"域执行层空白。*
