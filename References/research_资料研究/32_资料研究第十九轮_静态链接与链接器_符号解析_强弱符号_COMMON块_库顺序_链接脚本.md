# 资料研究第十九轮：静态链接与链接器——符号解析、强弱符号、COMMON 块、库顺序与链接脚本

> 2026-09-11，底层工程资料研究员。主题：静态链接器 ld 的工作原理（符号解析与重定位）、强弱符号规则、COMMON 块（Fortran 遗留）、静态库链接顺序与循环依赖、ar 归档、链接脚本（linker script）。
> 检索方式：general_search + CMU CSAPP 链接讲义 + GNU ld 官方文档 + GCC 代码生成选项文档 + Oracle 链接编辑器文档 + Apple WWDC 2022 "Link fast"。
> **系统域第三轮**（前两轮：动态链接与加载、ELF 文件格式，本轮静态链接，三者构成完整的"编译→链接→加载"链路）。

---

## 一、静态链接器的两大任务

### 1. 符号解析（Symbol Resolution）

> 将每个符号引用与**恰好一个**符号定义关联起来。

- 目标文件（.o）中定义和引用符号（函数、全局变量、静态变量）
- 符号定义存储在符号表中（.symtab）
- 链接器遍历所有输入文件，把未定义的符号引用匹配到某个定义
- 匹配不上 → `undefined reference` 链接错误

### 2. 重定位（Relocation）

> 编译器和汇编器生成从地址 0 开始的代码和数据节。链接器把每个符号定义与一个内存位置关联，然后修改所有对符号的引用。

- 合并所有输入文件的 .text/.data/.bss 等 section
- 分配最终虚拟地址
- 根据重定位条目（.rela.text 等）修改机器代码中的占位地址
- 重定位条目告诉链接器：修改哪个位置、用什么公式、引用哪个符号

- **来源**：CMU CSAPP Chapter 7 + JHU CSF Lecture 18
- **可信度**：S

---

## 二、链接器的工作流程

```
输入：main.o foo.o libbar.a
  │
  ├─ 1. 按命令行顺序处理输入文件
  │     ├─ .o 文件：全部加载，合并 section
  │     └─ .a 静态库：只提取"需要的"成员（能解析当前未定义符号的 .o）
  │
  ├─ 2. 符号解析
  │     ├─ 维护"已定义符号"集合和"未定义符号"集合
  │     ├─ 每加载一个 .o，更新两个集合
  │     └─ 处理完所有文件后，未定义集合非空 → 报错
  │
  ├─ 3. Section 合并
  │     ├─ 所有 .text 合并成一个 .text
  │     ├─ 所有 .data 合并成一个 .data
  │     └─ 所有 .bss 合并成一个 .bss
  │
  ├─ 4. 地址分配
  │     └─ 给每个 section 和符号分配最终虚拟地址
  │
  └─ 5. 重定位
        └─ 遍历重定位条目，用公式计算最终地址，修改机器代码
```

### 关键：静态库只提取"需要的"成员

- 静态库（.a）是 .o 文件的归档
- 链接器**不会**把静态库的所有 .o 都链进来
- 只提取那些能解析当前未定义符号的成员
- 这就是为什么静态库链接顺序很重要（见第五节）
- **来源**：Oracle 输入文件处理文档 + Checkoway 静态库讲义
- **可信度**：S

---

## 三、强弱符号规则（CMU CSAPP 经典三条）

### 1. 强符号 vs 弱符号

| 类型 | 强符号 | 弱符号 |
|---|---|---|
| C 语言 | 函数、已初始化全局变量 | 未初始化全局变量（tentative definition） |
| C++ | 函数、所有全局变量 | `__attribute__((weak))` 标记的符号 |
| 汇编标记 | STB_GLOBAL | STB_WEAK |

### 2. 三条规则

> **规则 1**：多个强符号同名 → **链接错误**（`multiple definition`）
>
> **规则 2**：一个强符号 + 多个弱符号同名 → **选强符号**（弱符号被覆盖，不报错）
>
> **规则 3**：多个弱符号同名 → **任选一个**（不报错，行为不确定）

### 3. 经典陷阱

```c
/* a.c */
int x = 1;          /* 强符号 */

/* b.c */
int x;              /* 弱符号（tentative definition） */
int main() { return x; }  /* 链接时选 a.c 的 x=1，不报错 */
```

```c
/* a.c */
int x = 1;          /* 强符号 */

/* b.c */
int x = 2;          /* 强符号 */
/* 链接错误：multiple definition of 'x' */
```

- **来源**：CMU CSAPP 09-linking.pdf + UT Austin CS429 链接讲义
- **可信度**：S

---

## 四、COMMON 块（Fortran 遗留）

### 1. 什么是 tentative definition（暂定定义）？

- C 语言中，**未初始化的全局变量**是 tentative definition
- 编译器不直接把它放 .bss，而是放在 **COMMON 块**（符号类型 STT_COMMON，节索引 SHN_COMMON）
- 链接器合并所有同名 tentative definition 为一个（取最大大小）

### 2. 为什么叫 COMMON？

- 来自 Fortran 的 `COMMON` 块——多个编译单元可以共享同名的全局变量
- C 语言继承了这个机制，允许多个 .c 文件定义同名全局变量而不报错
- 最终链接时合并为一个变量

### 3. -fcommon vs -fno-common

| 选项 | 行为 | GCC 默认 |
|---|---|---|
| `-fcommon` | 未初始化全局变量放 COMMON 块，允许多重定义合并 | GCC < 10 |
| `-fno-common` | 未初始化全局变量直接放 .bss，多重定义报错 | GCC 10+（2020 年起） |

- GCC 10 把默认从 -fcommon 改成 -fno-common，因为 COMMON 块会导致隐蔽的 bug（两个文件不小心定义了同名全局变量，静默合并）
- **C++ 始终是 -fno-common 行为**——C++ 没有 tentative definition，所有全局变量都是强符号

### 4. 为什么 -fno-common 更好？

- COMMON 块意味着全局变量的访问可能需要额外的间接层（速度和代码大小惩罚）
- 静默合并可能导致难以调试的 bug（两个模块以为各自有独立的变量，实际共享）
- GCC 文档明确说："This behavior is inconsistent with C++"

- **来源**：GCC 代码生成选项文档 + GCC Common Variable Attributes
- **可信度**：S

---

## 五、静态库链接顺序

### 1. 为什么顺序很重要？

- 链接器按命令行顺序处理输入文件，**静态库只扫描一次**
- 静态库只提取能解析**当前**未定义符号的成员
- 如果 libA 依赖 libB 的符号，但 libA 在 libB 后面：
  - 处理 libA 时，libB 的符号还没被加载
  - libA 中需要 libB 符号的成员不会被提取（因为当时没有未定义引用）
  - 处理 libB 时，libA 的未定义引用已经过去了
  - 结果：`undefined reference`

### 2. 正确顺序

```bash
# 正确：被依赖的库放在后面
gcc main.o -lA -lB -o prog   # libA 依赖 libB → A 在前，B 在后

# 错误
gcc main.o -lB -lA -o prog   # 处理 libB 时没有未定义引用，跳过；处理 libA 时需要 libB 的符号，但 libB 已经过了
```

### 3. 循环依赖的解决方案

```bash
# 方案 1：--start-group / --end-group（推荐）
gcc main.o -Wl,--start-group -lA -lB -lC -Wl,--end-group -o prog
# 组内库反复扫描，直到没有新的未定义引用

# 方案 2：把库写两次（不推荐，丑陋）
gcc main.o -lA -lB -lA -o prog

# 方案 3：消除循环依赖（最佳，重构代码）
```

- `--start-group/--end-group` 的代价：链接变慢（反复扫描），所以只在确实有循环依赖时用
- **来源**：GNU ld 选项文档 + FunWithLinux 循环依赖分析
- **可信度**：S

---

## 六、ar 归档工具

### 1. 创建静态库

```bash
# 编译为 .o
gcc -c foo.c bar.c

# 创建静态库
ar rcs libfoo.a foo.o bar.o
#   r：替换/添加成员
#   c：创建（不提示"正在创建"）
#   s：写入符号索引（等同于 ranlib）
```

### 2. 静态库的结构

```
libfoo.a
├── 归档头部（!<arch>\n）
├── 符号索引表（__SYM64 / __.SYMDEF）
│   └── 符号名 → 成员偏移的映射（加速链接器查找）
├── foo.o（成员 1）
└── bar.o（成员 2）
```

- 符号索引表很重要——没有它，链接器需要逐个检查每个成员的符号表（慢）
- `ar s` 或 `ranlib` 生成/更新符号索引
- 现代 ar 默认 `r` 就会更新符号索引（`s` 是默认行为的显式声明）

### 3. 常用命令

| 命令 | 作用 |
|---|---|
| `ar rcs lib.a a.o b.o` | 创建/更新静态库 |
| `ar t lib.a` | 列出成员 |
| `ar x lib.a` | 提取所有成员 |
| `ar d lib.a a.o` | 删除成员 |
| `ranlib lib.a` | 更新符号索引 |

- **来源**：maneesh29s 静态库教程 + Oracle 归档文档
- **可信度**：A

---

## 七、链接脚本（Linker Script）

### 1. 什么是链接脚本？

- 用 ld 的命令语言（Linker Command Language）控制输出文件的内存布局
- 桌面 Linux 用默认链接脚本（`/usr/lib/ldscripts/`），通常不需要自定义
- **嵌入式开发必须写链接脚本**——指定中断向量表位置、代码/数据在 Flash/RAM 的布局

### 2. 核心命令

#### MEMORY：定义内存区域

```ld
MEMORY
{
    FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 512K
    RAM   (rwx) : ORIGIN = 0x20000000, LENGTH = 128K
}
```

#### SECTIONS：定义输出 section 布局

```ld
SECTIONS
{
    .isr_vector :
    {
        . = ALIGN(4);
        KEEP(*(.isr_vector))   /* 中断向量表，KEEP 防止被 GC 删除 */
        . = ALIGN(4);
    } >FLASH

    .text :
    {
        . = ALIGN(4);
        *(.text)               /* 所有输入文件的 .text */
        *(.text*)              /* 包括 .text.startup 等 */
        . = ALIGN(4);
    } >FLASH

    .rodata :
    {
        *(.rodata*)
    } >FLASH

    .data :
    {
        _sdata = .;            /* 定义符号：_sdata = 当前地址 */
        *(.data*)
        _edata = .;
    } >RAM AT >FLASH          /* 运行时在 RAM，加载时在 Flash（AT 指定加载地址） */

    .bss :
    {
        _sbss = .;
        *(.bss*)
        *(COMMON)              /* COMMON 块 */
        _ebss = .;
    } >RAM
}
```

### 3. 常用命令

| 命令 | 作用 |
|---|---|
| `ALIGN(n)` | 地址对齐到 n 字节 |
| `KEEP(...)` | 保留 section，不被垃圾回收（--gc-sections 删除） |
| `PROVIDE(symbol = .)` | 定义符号，仅当被引用时 |
| `AT >region` | 指定加载地址（区别于运行地址） |
| `>region` | 分配到指定内存区域 |
| `. = expr` | 设置当前位置计数器 |
| `symbol = .` | 定义符号为当前地址 |

### 4. .data 的 AT > FLASH 技巧

- .data 是已初始化的全局变量，运行时在 RAM（可读写），但初始值存在 Flash（只读）
- 启动代码需要把 .data 的初始值从 Flash 复制到 RAM
- `>RAM AT >FLASH` 表示：运行地址在 RAM，加载地址在 Flash
- 这是嵌入式开发的标准模式

- **来源**：GNU ld 官方文档 + STM32 链接脚本实例 + RTEMS 链接脚本指南
- **可信度**：S

---

## 八、静态链接 vs 动态链接

| 维度 | 静态链接 | 动态链接 |
|---|---|---|
| 代码位置 | 全部复制进可执行文件 | 运行时从共享库加载 |
| 运行时依赖 | 无 | 需要 .so 文件存在 |
| 文件大小 | 大 | 小 |
| 启动速度 | 快（无加载开销） | 慢（ld.so 加载+重定位） |
| 更新库 | 需重新链接 | 替换 .so 即可 |
| 兼容性 | 自包含 | 依赖系统库版本 |
| 内存共享 | 每个进程一份代码 | 代码段多进程共享 |
| 典型场景 | 嵌入式、分发独立二进制 | 桌面、服务器（系统库） |

---

## 九、知识网络

```
静态链接与链接器
├── 两大任务
│   ├── 符号解析（引用→定义）
│   └── 重定位（分配地址→修改引用）
│
├── 工作流程
│   ├── 按命令行顺序处理
│   ├── .o 全部加载
│   ├── .a 只提取需要的成员
│   ├── 合并 section
│   ├── 分配地址
│   └── 应用重定位
│
├── 强弱符号规则
│   ├── 强符号：函数、已初始化全局变量
│   ├── 弱符号：未初始化全局变量（C）、__attribute__((weak))
│   ├── 规则1：多强符号 → 错误
│   ├── 规则2：一强多弱 → 选强
│   └── 规则3：多弱符号 → 任选
│
├── COMMON 块
│   ├── tentative definition（C 未初始化全局变量）
│   ├── Fortran COMMON 遗留
│   ├── -fcommon（GCC<10）vs -fno-common（GCC10+）
│   └── C++ 始终 -fno-common
│
├── 静态库链接顺序
│   ├── 库只扫描一次
│   ├── 被依赖的库放后面
│   ├── 循环依赖：--start-group/--end-group
│   └── 最佳：消除循环依赖
│
├── ar 归档
│   ├── ar rcs lib.a a.o b.o
│   ├── 符号索引表（__SYM64）
│   └── ranlib 更新索引
│
├── 链接脚本
│   ├── MEMORY（Flash/RAM 区域）
│   ├── SECTIONS（输出布局）
│   ├── ALIGN/KEEP/PROVIDE/AT
│   └── 嵌入式必需，桌面用默认
│
└── 静态 vs 动态链接
```

---

## 十、本轮最重要的 10 个资料

| # | 资料 | 级别 | 核心价值 |
|---|---|---|---|
| 1 | CMU CSAPP Chapter 7（Linking） | S | 强弱符号三条规则的经典出处 |
| 2 | GNU ld 官方文档（sourceware） | S | 链接器和链接脚本的权威定义 |
| 3 | GCC 代码生成选项文档（-fcommon/-fno-common） | S | COMMON 块的官方说明 |
| 4 | Oracle 链接编辑器文档（符号解析） | S | 符号决议的详细规则 |
| 5 | Apple WWDC 2022 "Link fast" | A+ | 链接器工作流程的直观解释 |
| 6 | GNU ld 选项文档（--start-group） | S | 循环依赖解决方案的权威说明 |
| 7 | UT Austin CS429 链接讲义 | A | 强弱符号的教学解释 |
| 8 | STM32 链接脚本实例 | A | 嵌入式链接脚本的真实范例 |
| 9 | Checkoway 静态库讲义 | A | 静态库选择性提取的清晰解释 |
| 10 | FunWithLinux 循环依赖分析 | A | 库顺序问题的实用总结 |

## 十一、强烈建议深入研究的 5 个资料

1. **CMU CSAPP Chapter 7**——链接的经典教材，强弱符号规则必读
2. **GNU ld 官方文档**——链接脚本语法的完整参考
3. **GCC -fcommon 文档**——理解 COMMON 块为什么被废弃
4. **Apple WWDC 2022 "Link fast"**——链接器工作流程的可视化解释
5. **一个真实的 STM32 链接脚本**——跟着 MEMORY/SECTIONS 理解嵌入式布局

## 十二、适合直接进入 CPP-Bible 的资料

| 资料 | 进入方式 | 目标原子/章节 |
|---|---|---|
| 链接器两大任务 | "编译器之后发生了什么" | TOOL 域原子 |
| 强弱符号规则 | "为什么两个同名全局变量有时报错有时不报错" | LANG/TOOL 交叉 |
| COMMON 块 | "GCC 10 为什么改了默认行为" | TOOL 域原子 |
| 静态库链接顺序 | "undefined reference 的最常见原因" | TOOL 域专题 |
| 链接脚本 | "嵌入式程序的内存布局怎么控制" | EMBEDDED 域原子 |

## 十三、对 CPP-Bible 的工程升级建议

1. **TOOL 域新增"静态链接"原子**——符号解析+重定位+强弱符号，这是理解编译全链路的关键一环
2. **TOOL 域新增"静态库链接顺序"专题**——`undefined reference` 的最常见原因，含正确/错误示例和 --start-group 解法
3. **LANG 域新增"强弱符号与 COMMON 块"原子**——C 和 C++ 在 tentative definition 上的差异，GCC 10 默认变更的影响
4. **EMBEDDED 域新增"链接脚本"原子**——MEMORY/SECTIONS/ALIGN/KEEP/AT，含 STM32 真实示例
5. **构建系统建议**：项目 CMake 可以加 `--gc-sections`（删除未引用 section）和 `-fno-common`（确保 C++ 行为一致）

## 十四、发现的知识空白

1. **静态链接完全空白**——项目没有任何链接器相关内容
2. **强弱符号规则空白**——最常见的链接错误原因完全没讲
3. **COMMON 块空白**——GCC 10 默认变更的重要话题
4. **静态库链接顺序空白**——`undefined reference` 的最常见原因
5. **链接脚本空白**——嵌入式开发的必备技能

## 十五、下一轮推荐搜索方向

1. **SIMD intrinsics 与手写向量化（按顺序）**——SSE/AVX/AVX-512/NEON、intrinsics 编程、自动向量化 vs 手写、成本模型
2. **CMake 构建系统**——target 模型、generator 表达式、大型项目组织、FetchContent、ExternalProject
3. **编译器前端**——词法/语法分析、AST、语义分析、模板两阶段查找、name mangling
4. **C++ 对象模型与 ABI**——vtable、vptr、RTTI、内存布局、多重继承、虚继承
5. **性能分析与 profiling**——perf、gprof、Valgrind、cachegrind、火焰图、性能优化方法论

---

*本轮新增知识节点：静态链接、符号解析、重定位、强符号、弱符号、tentative definition、暂定定义、COMMON 块、-fcommon、-fno-common、多重定义、multiple definition、静态库、归档、ar、ranlib、符号索引、__SYM64、链接顺序、undefined reference、--start-group、--end-group、循环依赖、链接脚本、linker script、MEMORY、SECTIONS、ALIGN、KEEP、PROVIDE、AT、加载地址、运行地址、位置计数器、--gc-sections、垃圾回收。补齐了"静态链接与链接器"域的全部核心空白——至此"编译→汇编→静态链接→动态链接→加载"全链路的系统域基础已全部覆盖。*
