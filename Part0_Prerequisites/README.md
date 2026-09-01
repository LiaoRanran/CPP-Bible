# Part 0 — 前置基础：汇编与 C 语言

> **定位**：本目录是《现代 C++ 终极圣经》的**前置预备篇**，独立于主书 147 章体系之外（不计入 `Book/` 章节数、不参与主书质量门禁扫描），作为学习现代 C++ 之前的「从机器到 C」地基。
> **工具链**：GCC 15.3.0（`C:/Qt/Tools/mingw1530_64/bin/g++.exe`，`-std=c++23`）；汇编反汇编统一用同目录 `bin/objdump.exe`（`-M intel` 语法）。
> **红线**：所有汇编块均来自 GCC 15.3 真机 `objdump` 产物，**禁止伪造**；C 示例均为可独立编译的程序。

## 为什么需要 Part 0

现代 C++ 的许多「为什么」只能落到两层之下才讲得清：

- **汇编层**：`inline` 是否真内联、虚函数调用为何多一次间接、栈对象为何零成本、`constexpr` 在编译期算到了哪、UB 为何被编译器「优化」成对的结果——这些命题的判据都在生成的机器码里。
- **C 层**：C++ 脱胎于 C（"C with Classes"），指针、`malloc`、数组退化、结构体内存布局、调用约定、`extern "C"` 与名字改编（name mangling）全部继承自 C。不懂 C，就懂不透 C++ 的 ABI 与零成本抽象。

本篇不与主书重复：主书讲 C++ 的「是什么 / 怎么用」，本篇讲「落到金属上是什么样」。

## 目录（15 章，汇编 6 + C 9）

### 汇编部分（`asm/`）

| 章 | 文件 | 主题 |
|----|------|------|
| A1 | `asm/asm01_intro.md` | 导论：为何 C++ 程序员要懂汇编 + 工具链（编译/反汇编/Compiler Explorer） |
| A2 | `asm/asm02_registers.md` | x86-64 寄存器模型、内存视角、数据移动指令（`mov`/`lea`） |
| A3 | `asm/asm03_stack_abi.md` | 栈帧与函数调用约定（Microsoft x64：传参/返回值/被调用者保存/shadow space） |
| A4 | `asm/asm04_controlflow.md` | 控制流：`cmp`/`test`、条件跳转、循环与分支预测痕迹 |
| A5 | `asm/asm05_data_layout.md` | 数据结构在汇编层：数组寻址、结构体字段偏移与对齐 |
| A6 | `asm/asm06_inline_and_opt.md` | 内联汇编与读编译器输出：从 C++ 源码反推优化（`-O0` vs `-O2`） |

### C 语言部分（`c/`，参考《C 语言极致详解手册》）

| 章 | 文件 | 主题 |
|----|------|------|
| C1 | `c/c01_overview.md` | C 概述与核心哲学（对照 C++） |
| C2 | `c/c02_toolchain.md` | C 工具链：GCC 四阶段、预处理、`objdump` 读 `.o` |
| C3 | `c/c03_types.md` | 类型系统：整数/浮点/指针/数组退化/隐式转换陷阱 |
| C4 | `c/c04_functions.md` | 函数：调用、栈帧、变参 `stdarg` |
| C5 | `c/c05_memory.md` | 指针与内存：`malloc`/`free`、进程内存布局 |
| C6 | `c/c06_structs.md` | 结构体/联合体/位域、对齐 padding 与 `#pragma pack` |
| C7 | `c/c07_preprocessor.md` | 预处理：宏、头文件、include guard、`#ifdef` |
| C8 | `c/c08_stdlib.md` | 标准库精要：`stdio`/`string`/`stdlib` |
| C9 | `c/c09_cpp_interop.md` | C 与 C++ 互操作：`extern "C"`、name mangling、ABI 边界 |

## 阅读约定

- 汇编示例统一 Intel 语法（`objdump -d -M intel`）。**调用约定**：本机工具链为 Windows/MinGW GCC 15.3，所有反汇编实例采用 **Microsoft x64 调用约定**（整数前 4 参数 `rcx, rdx, r8, r9`，其余压栈；返回值 `rax`）；Linux/macOS 的 System V AMD64 ABI（前 6 参数 `rdi, rsi, rdx, rcx, r8, r9`）在差异点注明。所有 objdump 均为本机可复现的真实产物。
- 每个 ```` ```cpp ```` / ```` ```c ```` 代码块均为**自包含、可独立编译**程序（`#include` + `int main`）。
- 汇编证据块一律标注生成命令与编译器版本，可复现。

## 进度

| 章 | 状态 | 关键证据 |
|----|------|----------|
| A1–A6（汇编） | ✅ 已完成 | 全部带 GCC 15.3 `objdump -d -M intel` 真机产物 |
| C1（C 概述） | ✅ 已完成 | 对照 C++ 的核心差异 |
| C2（工具链） | ✅ 已完成 | GCC 四阶段真机产物；`objdump -h`（`.bss` 不占磁盘空间）、`-r`（`__mingw_printf` 重定位）、`-d`（`add` 印证 **Microsoft x64 影子空间 `rbp+0x10`**） |
| C3（类型系统） | ✅ 已完成 | LLP64 实测（`long`=4、指针=8）；真实警告 `-Wsign-compare`（`-1 < 1u` 为 false）、`-Wsizeof-array-argument`（数组形参退化） |
| C4–C9 | ⏳ 待写 | 函数与栈帧 / 指针内存 / 结构体对齐 / 预处理 / 标准库 / C↔C++ 互操作 |

_创建：2026-09-01 | 不计入主书 147 章_
