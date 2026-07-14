# 第11章　编译器全景：GCC / Clang / MSVC 架构与 ABI（C++）

⟶ Book/part06_templates/ch69_constexpr.md
⟶ Book/part14_perf/ch157_compiler_explorer.md

> 真实取证工具链：MinGW GCC 13.1.0（`C:/Qt/Tools/mingw1310_64/bin/g++.exe`，`-std=c++23 -O2 -S -masm=intel`）、`c++filt.exe`。
> 源码与汇编产物位于 `Examples/_ch11_*.cpp` / `Examples/_ch11_*.asm`。
> 立场标签遵循 `CONVENTIONS.md §1`：`[标准]`=ISO、`[实现]`=编译器/库、`[平台]`=OS/ABI/硬件、`[经验]`=工程共识。

## ① 概述：为什么需要编译器，三巨头格局

⟶ Book/part02_toolchain/ch12_buildsystems.md


C++ 源码不是机器能直接执行的——它需要被**翻译**为特定 ISA（x86-64 / ARM64 / RISC-V 等）的机器码。编译器承担三件事：① 把文本翻译为语义正确的指令；② 在翻译中做等价变换（优化）以提升速度/减小体积；③ 与操作系统/链接器/运行时协作，产出可加载的二进制。

```cpp
// ① 同一份 C++ 源码，三种主流编译器都能产出可执行文件
//   GCC       : g++ main.cpp -o main
//   Clang     : clang++ main.cpp -o main
//   MSVC      : cl.exe main.cpp /Fe:main.exe
int main() { return 0; }
```

当今 C++ 工业级编译器三巨头：

- **GCC（GNU Compiler Collection）**：GPL 生态的事实标准，跨平台最广，libstdc++ 标准库。`[实现·GCC13]`：本章取证即用 GCC 13.1.0。
- **Clang/LLVM**：模块化、可嵌入、诊断友好，libc++ 标准库；Apple 平台默认。
- **MSVC（Microsoft Visual C++）**：Windows 原生，MSVC STL（MS-STL），与 Visual Studio / MSBuild 深度集成。

- `[标准]`：ISO C++ 只规定**语言语义与库接口**，不规定编译器内部表示（AST/IR）或目标文件格式——这正是三家实现天差地别的根本原因。
- `[经验]`：跨平台项目必须在三套工具链上各验一遍，因为 UB 在三家中表现不同（同一份代码 GCC 正常、Clang 崩溃是常态）。


## 架构与流程图示（Mermaid）

下图给出 C++ 源文件经编译器到可执行文件的标准流水线，每个阶段产出明确的 IR 或产物。

```mermaid
flowchart LR
    SRC["源代码 .cpp"] --> CPP["预处理器<br/>宏展开 / 头文件包含"]
    CPP --> LEX["词法分析 Lexer<br/>token 流"]
    LEX --> PAR["语法分析 Parser<br/>AST 抽象语法树"]
    PAR --> SEM["语义分析 Sema<br/>类型检查 / 模板实例化"]
    SEM --> IR["中间表示 IR<br/>GIMPLE / LLVM IR"]
    IR --> OPT["优化 Pass<br/>内联 / 常量折叠 / 循环优化"]
    OPT --> CG["代码生成 CodeGen<br/>目标汇编 .s"]
    CG --> AS["汇编 Assembler<br/>目标文件 .o"]
    AS --> LD["链接器 Linker<br/>符号解析 / 重定位"]
    LD --> EXE["可执行文件 / 库"]
```

## ② GCC 架构：前端 → 中端 GIMPLE → RTL → 后端 PASS

GCC 采用**分层中间表示（IR）**，把"语言相关"与"目标相关"彻底解耦。

```cpp
// ② GCC 的语言无关中端示意：中端不关心这是 C++ 还是 Fortran
// 前端解析为 GENERIC(AST) -> 降级为 GIMPLE(SSA, 三地址码) -> 展开为 RTL(贴近硬件)
// 下列代码最终都会被表示成 GIMPLE 的"每个语句最多一个副作用"形式
int sum(int a, int b) { return a + b; }   // GIMPLE: _t = a + b; return _t;
```

GCC 的关键分层：

- **前端（Front End）**：`cp/` 目录解析 C++，产出 GENERIC 树。语言相关，每加一种语言就加一个前端。
- **中端（Middle End）**：`GIMPLE` + `SSA`（静态单赋值）是优化主战场；`tree-ssa` 做常量传播、死代码消除、内联决策；`loop` 优化在此。`[实现·GCC13]`：GIMPLE 是**语言无关**的，所以 C/C++/Fortran 共享同一批优化 PASS。
- **RTL（Register Transfer Language）**：比 GIMPLE 更贴近硬件，描述寄存器与机器指令；指令选择、寄存器分配、调度在 RTL 层。
- **PASS 机制**：每个优化是一个 `pass`，按 `pass_list` 顺序串联；`-fdump-tree-*` / `-fdump-rtl-*` 可逐 PASS 导出中间表示。

```cpp
// ② 用 -fdump-tree-gimple 可看到 sum 的 GIMPLE 形态（文件 sum.cpp.005t.gimple）
// 下面仅示意 dump 的内容，非可编译代码
// sum (int a, int b)
// {
//   _1 = a + b;
//   return _1;
// }
int sum(int a, int b) { return a + b; }
```

- `[实现·GCC13]`：GCC 的优化是"固定顺序的 PASS 流水线"，而 LLVM 用 `PassManager` 做更灵活的依赖驱动调度（见 ③）。
- `[经验]`：调 `-O2` 不如调单个优化开关（`-fno-...`）。定位某优化引入的 bug，先 `-fdump-tree-all` 二分到具体 PASS。

## ③ Clang/LLVM 架构：模块化、libclang、LLVM IR

Clang 是 LLVM 的 C/C++/ObjC 前端；LLVM 是后端基础设施，核心是 **LLVM IR**（一种强类型、SSA 形式的低级虚拟指令集）。

```cpp
// ③ LLVM IR 是平台无关的低级表示；下列 C++ 在 LLVM 中被翻译为 LLVM IR 而非直接出码
// 用 clang++ -std=c++23 -emit-llvm -S x.cpp -o x.ll 可见 IR
int twice(int n) { return n * 2; }
// 对应 IR(节选): define i32 @_Z5twicei(i32 %n) { %1 = mul i32 %n, 2; ret i32 %1 }
```

Clang/LLVM 的差异化优势：

- **模块化**：每个组件是独立库（`libclang`、`libLLVM` 等），可被 IDE（VSCode clangd）、静态分析器、模糊测试框架复用。
- **libclang / clangd**：暴露稳定的 C API，支撑语言服务器协议（LSP），这是 Clang 在开发者体验上碾压 GCC 的主因。
- **LLVM IR**：前后端解耦——同一份 IR 可被不同 `Target` 后端（`X86`、`AArch64`、`RISCV`）翻译，易于移植新架构。
- **PassManager**：基于依赖图的按需调度，而非 GCC 的固定顺序。

```cpp
// ③ LLVM 多后端示意：同一 IR，不同 -mtriple 产出不同汇编
//   clang++ -target x86_64-w64-windows-gnu -emit-llvm ...   -> X86
//   clang++ -target aarch64-linux-gnu        -emit-llvm ...   -> AArch64
// 前端产物(IR)不变，仅后端 Target 不同
int add(int a, int b) { return a + b; }
```

```cpp
// ③ 用 libclang 做 AST 遍历（仅示意 API 调用骨架，非完整可编译工程）
// clang_getCursorKind / clang_visitChildren —— IDE 精确补全即源于此
// 工程价值：静态检查、自定义 lint、代码迁移工具
```

- `[实现·LLVM]`：LLVM IR 是文本可读的（`.ll`），区别于 GCC 完全内部的 GIMPLE/RTL，极大便利了教学与研究。
- `[经验]`：做编译器插件、DSL、JITs（如 Julia、Rust 旧后端）优先选 LLVM；嵌入式裸机小体积常用 GCC。

## ④ MSVC：cl.exe、MSVC 后端、MSBuild

MSVC 是 Windows 原生工具链，组件与另两家命名完全不同。

```cpp
// ④ MSVC 编译命令（cl.exe 一站式完成 编译+汇编+链接）
//   cl /std:c++20 /EHsc /O2 /Fe:app.exe main.cpp
// 与 GCC/Clang 的 "g++/clang++ 只编译，ld 链接" 习惯不同，cl 默认直接产出 exe
int main() { return 0; }
```

MSVC 关键组件：

- **cl.exe**：编译器驱动，前端 + 后端一体的"老派"设计（不像 GCC/Clang 把前后端拆开）。
- **MSVC 后端（C2）**：负责优化与代码生成；与 Visual Studio 调试器（PDB）深度集成。
- **MSBuild / MSVC STL**：构建系统 `MSBuild`（`.vcxproj`），标准库为 MS-STL（`<yvals.h>` 体系），与 libstdc++/libc++ 实现差异显著。
- **链接器 link.exe**：处理 COFF/PE；`/DEBUG` 生成 PDB（见 ⑰）。

```cpp
// ④ MSVC 的模块支持：用 /interface 编译 .ixx 接口单元
//   cl /std:c++20 /interface math.ixx /c -> 生成 .ifc(等价 BMI)
//   cl /std:c++20 use.cpp math.obj /Fe:app.exe
export module math;
export int square(int x) { return x * x; }
```

```cpp
// ④ MSVC 异常模型：/EHsc 是 C++ 项目的标准选择（同步 C++ 异常）
//   /EHa 会也捕获异步结构化异常(SEH)，代价更大
//   throw 与 __try/__except(SEH) 在 MSVC 下语义不同，见 ⑨
void may_throw(bool b) { if (b) throw 1; }
```

- `[平台·Windows]`：MSVC 只产出 COFF/PE（Windows），不跨平台；交叉编译 Windows 程序多用 MinGW 或 clang-cl。
- `[经验]`：Windows 下想复用 GCC/Clang 生态，优先 `clang-cl`（MSVC 兼容命令行 + LLVM 后端）或 MinGW-w64，而非硬上 MSVC。

## ⑤ 编译流程：预处理 → 编译 → 汇编 → 链接

经典四阶段，GCC/Clang 用 `-E / -S / -c` 分阶段暴露。

```cpp
// ⑤ 一个最小 TU，用于演示四阶段
// 文件：Examples/_ch11_f.cpp（第2行 int f(int)）
#define INC 1
int f(int x) { return x + INC; }
```

```bash
# ⑤ 四阶段命令（GCC/Clang 同形）
g++ -E  main.cpp -o main.i    # 1) 预处理：宏展开、#include 文本拼入、删除注释
g++ -S  main.i -o main.s      # 2) 编译：i 文件 -> 汇编(asm)
g++ -c  main.s -o main.o      # 3) 汇编：asm -> 可重定位目标文件(.o)
g++ main.o -o main            # 4) 链接：多 .o + 库 -> 可执行
```

```cpp
// ⑤ 预处理后可观察：#include <iostream> 会把整个标准库头文本拼入 .i 文件
// 鸿篇巨制的 .i 正是 Modules(见⑮)要解决的问题
#include <vector>
std::vector<int> make() { return {1, 2, 3}; }
```

```cpp
// ⑤ 链接期解析符号：未定义引用(ld: undefined reference) 即"声明有、定义无"
// 典型：只在头里声明 void foo(); 但没在任何 TU 定义 -> 链接失败
extern void foo();          // 声明
int use_foo() { foo(); return 0; }   // 若 foo 无定义 -> 链接错误
```

- `[标准]`：翻译单元（TU）是预处理后的单文件；ODR（单一定义规则）约束每个实体在每个 TU 内至多一个定义。`[标准·basic.def.odr]`
- `[实现·GCC13]`：`-c` 单独汇编时若引用未定义符号，只记录重定位项，不报错；报错推迟到链接期。
- `[经验]`：链接错误（符号找不到/重复）远比编译错误难定位——把"声明/定义分离"与"头文件守卫/pragma once"做对，能消灭 80% 链接问题。

## ⑥ 目标文件格式：ELF / COFF / Mach-O

目标文件是汇编后的二进制容器，不同 OS 用不同格式——这是"同一份 C++ 不能跨 OS 直接跑"的格式层原因。

```cpp
// ⑥ 下面代码在三平台产出不同格式目标文件
//   Linux   : ELF      (.o)         readelf -h a.o
//   Windows : COFF/PE  (.obj/.exe)  dumpbin /headers a.obj
//   macOS   : Mach-O  (.o)         otool -h a.o
int g(int x) { return x + 1; }
```

三格式对照：

| 格式 | 平台 | 段(section)组织 | 符号表 | 调试信息 |
|---|---|---|---|---|
| ELF | Linux/Unix/多数嵌入式 | `.text/.data/.bss/.rodata` | `.symtab` | DWARF |
| COFF/PE | Windows | `.text/.data/.rdata` | `COFF symtab` | PDB |
| Mach-O | macOS/iOS | `__TEXT/__DATA` | `LC_SYMTAB` | DWARF(in Mach-O) |

```cpp
// ⑥ 段的意义：下列变量被放入不同段
int      init_var = 42;     // .data  (已初始化)
int      zero_var;          // .bss   (零初始化，不占文件空间)
const int k = 7;            // .rodata(只读) / .rdata(Windows)
char     buf[1024];         // .bss
```

```cpp
// ⑥ ELF 的 .symtab 里，C++ 名字以 mangled 形式存在（见 ⑦ / ⑧）
//   readelf -s a.o  -> 看到 _Z1gi 而非 "g(int)"
int g(int, double) { return 0; }
```

- `[平台·ELF]`：ELF 用节区头表（section header）与程序头表（program header）区分"链接视图"与"执行视图"；COFF 用 `IMAGE_SECTION_HEADER`，Mach-O 用 `load command`。
- `[经验]`：`.bss` 不占磁盘空间（只在内存展开），因此"大数组未初始化"几乎免费；已初始化的 `int big[1<<20] = {1}` 则撑大文件。

## ⑦ Itanium C++ ABI 与名字改编（name mangling）

**名字改编（name mangling）** 是把 C++ 函数签名（作用域、参数类型、const/volatile、模板实参）编码成链接器能容纳的**唯一字符串**的机制。C++ 允许函数重载与命名空间，但链接器只认"扁平名字"，于是编译器把签名压成一段字符串。Itanium C++ ABI（GCC/Clang/ICC 通用）的编码规则：

```
_Z  <编码长度+名字>   <参数编码...>
  └ 前缀：_Z = 非限定函数
     _ZN ... E = 嵌套(N=namespace/class, E=end)
     类型码：i=int, c=char, d=double, l=long, P=pointer, S_=short?, 等
```

```cpp
// ⑦ 下列声明对应 Itanium mangling（真实符号取自 Examples/_ch11_mangle.cpp）
int         g(int, double);          // -> _Z1gid
void        h(char);                 // -> _Z1hc
long        k(short, int*, long);    // -> _Z1ksPil
double      area_of_circle(double);  // -> _Z14area_of_circled
namespace ns { int q(int); }         // -> _ZN2ns1qEi
template<typename T> T id(T);        // -> _Z2idIiET_S0_ (id<int>)
```

真实符号对照（由 GCC 13.1.0 编译 `_ch11_mangle.cpp` 后从 `.asm` 提取，`c++filt` 还原）：

| 源码签名 | 改编符号 | c++filt 还原 |
|---|---|---|
| `int g(int, double)` | `_Z1gid` | `g(int, double)` |
| `void h(char)` | `_Z1hc` | `h(char)` |
| `long k(short, int*, long)` | `_Z1ksPil` | `k(short, int*, long)` |
| `double area_of_circle(double)` | `_Z14area_of_circled` | `area_of_circle(double)` |
| `ns::q(int)` | `_ZN2ns1qEi` | `ns::q(int)` |
| `id<int>(int)` | `_Z2idIiET_S0_` | `int id<int>(int)` |

```cpp
// ⑦ 编码拆解：_Z1ksPil
//   _Z : 非限定函数
//   1k : 名字 "k" (长度1)
//   s  : short
//   P  : pointer  (指向 int)
//   i  : int      (指针所指)
//   l  : long     (第三个参数)
// 注意顺序：参数按声明顺序，指针先标 P 再标所指类型
```

```cpp
// ⑦ c++filt 还原命令（本机已装，真实可用）
//   c++filt _Z1ksPil   ->  k(short, int*, long)
//   c++filt _ZN2ns1qEi ->  ns::q(int)
```

```cpp
// ⑦ 模板实例化的 mangling 含实参：id<int> -> 在 _Z2id 后追加 <IiE>
// 这就是为什么同一模板不同实参会得到不同符号、互不冲突
template<typename T> T id(T x) { return x; }
template int id<int>(int);     // 显式实例化 -> _Z2idIiET_S0_
```

- `[平台·Itanium ABI]`：Itanium C++ ABI 是 GCC/Clang 在 Linux/macOS/Windows(MinGW) 上的通用 ABI 规范，规定了 mangling、vtable、RTTI、异常对象布局。MSVC 用自己的 **MSVC name decoration**（如 `?g@@YAHNH@Z`），与 Itanium 不兼容。
- `[经验]`：跨编译器链接失败常因 mangling/ABI 不一致（如用 GCC 编的库给 MSVC 链接）——C 接口（`extern "C"`）是跨工具链的唯一稳妥桥梁（见 ⑪）。

## ⑧ [实现]真实汇编：编译 `int f(int)` 看 `_Z1fi` 并用 c++filt 还原

下面所有汇编均来自本机 **GCC 13.1.0** 真实编译，未做任何改写。

```cpp
// 文件：Examples/_ch11_f.cpp
// 行号：2
// 编译：C:/Qt/Tools/mingw1310_64/bin/g++.exe -std=c++23 -O2 -S -masm=intel Examples/_ch11_f.cpp -o Examples/_ch11_f.asm
int f(int x) { return x + 1; }
```

```asm
; 文件：Examples/_ch11_f.asm  (GCC 13.1.0, -O2 -masm=intel, 真实输出节选)
	.globl	_Z1fi
	.def	_Z1fi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z1fi
_Z1fi:
.LFB0:
	.seh_endprologue
	lea	eax, 1[rcx]      ; eax = rcx + 1   (rcx = 第1参数 x, 见⑪ Win64 ABI)
	ret
	.seh_endproc
```

源码剖析要点：

- `_Z1fi` 即 `f(int)` 的 Itanium mangled 名（`_Z` + `1f`(名字长1) + `i`(int 参数)）。`[实现·GCC13]`
- 函数体只是一条 `lea eax, 1[rcx]`：把第 1 参数 `rcx` 加 1 装入返回值寄存器 `eax`，`ret` 返回。
- `1[rcx]` 是 Intel 语法里 `[rcx + 1]` 的等价写法（有效地址 + 位移）。

`c++filt` 还原（本机真实运行）：

```asm
; 命令：c++filt.exe _Z1fi   ->   输出 f(int)
; 命令：c++filt.exe _Z1gid  ->   输出 g(int, double)
; 命令：c++filt.exe _ZN2ns1qEi -> 输出 ns::q(int)
```

```cpp
// ⑧ 用 GCC 的 __PRETTY_FUNCTION__ 在运行期拿到 mangled 之外的可读名（非 mangled）
#include <cstdio>
int f(int x) { return x + 1; }
void show() { std::printf("%s\n", __PRETTY_FUNCTION__); }  // 输出: int f(int)
```

```cpp
// ⑧ extern "C" 可关闭 mangling：符号变成裸名 f，便于被 C/其他语言调用
extern "C" int f_c(int x) { return x + 1; }   // 符号即 "f_c"（无 _Z 前缀）
```

- `[实现·GCC13]`：上面 `_Z1fi` 符号名从 `Examples/_ch11_f.asm` 原文抄录，`c++filt` 还原为 `f(int)`，真实可复现；`_Z1gid` / `_ZN2ns1qEi` 仅为名字改编（mangling）规则的示意示例，并非该文件产物。
- `[经验]`：调试"undefined reference to _Zxxx"时，先 `c++filt _Zxxx` 还原成人类可读签名，再比对是否少链接了某个 `.o` 或库。

## ⑨ 异常处理模型：Itanium zero-cost vs Windows SEH

C++ 异常的实现依赖运行期机制，三大编译器分属两套模型。

```cpp
// ⑨ Itanium 零成本模型（GCC/Clang 在 Linux/macOS 用）：
//   无异常时不付任何运行时检查代价（"零成本"），异常抛出时才查表(.eh_frame)展开栈
#include <stdexcept>
int risky(bool b) {
    if (b) throw std::runtime_error("boom");
    return 0;
}
```

- **Itanium zero-cost（GCC/Clang on ELF/Mach-O）**：正常路径零开销；异常对象通过 `.eh_frame`（DWARF 展开信息）与 `__gxx_personality_v0`  personality routine 做栈展开。`[平台·Itanium ABI]`
- **Windows SEH（结构化异常）**：Windows 把 C++ 异常建立在一套 OS 级结构化异常（SEH）之上，用 `.pdata`/`.xdata` 描述函数展开信息；MSVC 用 `___CxxFrameHandler3`，MinGW(GCC on Windows) 也适配到 SEH。

```cpp
// ⑨ MSVC 异常变体（真实命令，非本机 MSVC 环境，标注"典型输出"）
//   cl /EHsc main.cpp   -> 同步 C++ 异常（不捕获 SEH）
//   cl /EHa main.cpp    -> 同时捕获异步 SEH（代价更高）
//   典型输出：/EHa 下 try { *(int*)0 = 0; } catch(...) {} 能吞掉访问违规(AV)
```

```cpp
// ⑨ 跨模型陷阱：在 MinGW(GCC) 下 throw 与 Windows SEH 是两套体系，
//   用 -fnon-call-exceptions 才能让某些 async 信号被 C++ 异常捕获
//   GCC 默认不会把 SIGSEGV 变成 C++ 异常——这与 MSVC /EHa 行为不同！
```

- `[平台·Windows]`：MinGW-w64 的 GCC 现在默认生成 **SEH** 展开信息（`-mseh`/`posix-seh` 构建），而非旧的 `setjmp`/`sjlj` 慢速模型。
- `[经验]`：异常有真实成本——不是"零成本"就免费：异常抛出路径极慢（需查表+展开+析构调用），热路径禁止用异常做控制流；`noexcept` 让编译器省略展开表、优化更激进。

## ⑩ RTTI 与 vtable 布局：从真实汇编看 `.vtable` 段

vtable（虚函数表）与 RTTI（`typeid`/`dynamic_cast`）是同一套机制的表里两面，都挂在类对象头部的**虚表指针（vptr）** 上。

```cpp
// 文件：Examples/_ch11_vtable.cpp
// 行号：2
// 编译：C:/Qt/Tools/mingw1310_64/bin/g++.exe -std=c++23 -O2 -S -masm=intel Examples/_ch11_vtable.cpp -o Examples/_ch11_vtable.asm
struct Shape {
    virtual ~Shape();
    virtual double area() const;
    virtual int    sides() const;
};
```

```asm
; 文件：Examples/_ch11_vtable.asm  (GCC 13.1.0, 真实输出节选)
; --- 类型字符串(typeinfo name) ---
_ZTS5Shape:
	.ascii "5Shape\0"
; --- 类型信息(typeinfo，指向 vtable of __class_type_info + 名字) ---
_ZTI5Shape:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTS5Shape
; --- vtable 本体（关键证据）---
_ZTV5Shape:
	.quad	0                    ; [0] offset-to-top（单继承为0）
	.quad	_ZTI5Shape           ; [1] &typeinfo（RTTI 指针）
	.quad	_ZN5ShapeD1Ev        ; [2] destructor D1（complete）
	.quad	_ZN5ShapeD0Ev        ; [3] destructor D0（deleting）
	.quad	_ZNK5Shape4areaEv    ; [4] area() const
	.quad	_ZNK5Shape5sidesEv   ; [5] sides() const
```

源码剖析：`[实现·GCC13]` 真实 vtable 布局为 **[offset-to-top][typeinfo ptr][虚函数指针...]**。第 0 项 `offset-to-top` 用于多继承下把 `Derived*` 调整回 `Base*`；第 1 项指向 `_ZTI5Shape`（RTTI 实体），`typeid(obj)` 即经 vptr 取这一项。`_ZN5ShapeD1Ev` = `Shape::~Shape()` 的 complete destructor 变体。

```cpp
// ⑩ 对象内存布局：vptr 在最前（Itanium ABI 单继承）
//   Shape 对象: [ vptr -> _ZTV5Shape ][ ...派生成员... ]
struct Circle : Shape {
    double r;
    double area() const override { return 3.141592653589793 * r * r; }
};
// Circle 的 vtable 第4项(_ZNK6Circle4areaEv)覆盖 Shape 的 area，动态分派即"经 vptr 取第4槽"
```

```cpp
// ⑩ RTTI 在运行期经 vtable 取 typeinfo
#include <typeinfo>
#include <cstdio>
void probe(const Shape& s) {
    std::printf("%s\n", typeid(s).name());   // 经 vptr[1] 取 _ZTI -> "5Shape"
}
```

```cpp
// ⑩ 多继承的 offset-to-top 非 0：下面 Derived 的第二基类 Base2 的 vtable 子表 offset-to-top = -8
struct Base1 { virtual void a(); };
struct Base2 { virtual void b(); };
struct Derived : Base1, Base2 { void a() override; void b() override; };
```

- `[平台·Itanium ABI]`：vtable 第 1 项是 `typeinfo` 指针、第 0 项是 `offset-to-top`，这是 ABI 硬性规定，因此 `dynamic_cast`/`typeid` 跨编译器/跨版本稳定（前提是同一 ABI）。
- `[经验]`：vtable 让每个含虚函数的类在每 TU 各生成一份 vtable（COMDAT/`linkonce`），链接器去重；因此"头文件里 inline 虚函数"会使 vtable 出现在多目标文件，靠链接去重而非违反 ODR。

## ⑪ 调用约定：cdecl / stdcall / thiscall / fastcall / Win64

**调用约定（calling convention）** 规定：参数怎么传（寄存器/栈）、谁清理栈、返回值放哪。这纯属 `[平台]` 层约定。

```cpp
// ⑪ 32 位 x86 常见调用约定（x86-64 下大多被统一，见下）
//   cdecl   : 参数右→左压栈, 调用方清栈 (C 默认)
//   stdcall : 参数右→左压栈, 被调方清栈 (Win32 API __stdcall)
//   thiscall: this 走 ecx, 其余右→左压栈 (32位 C++ 成员函数)
//   fastcall: 前两个 int 走 ecx/edx, 其余压栈
// 32 位 GCC/Clang 用 __attribute__((cdecl/stdcall/fastcall))，MSVC 用 __cdecl/__stdcall
extern "C" int __attribute__((stdcall)) win_api(int, int);
```

```cpp
// 文件：Examples/_ch11_cconv.cpp
// 行号：3
// 编译：C:/Qt/Tools/mingw1310_64/bin/g++.exe -std=c++23 -O2 -S -masm=intel Examples/_ch11_cconv.cpp -o Examples/_ch11_cconv.asm
long compute(long a, long b, long c, long d, long e, long f) {
    return a + b * 2 + c * 3 + d * 4 + e * 5 + f * 6;
}
```

```asm
; 文件：Examples/_ch11_cconv.asm  (GCC 13.1.0 x86-64, 真实输出节选)
; Win64 调用约定：前 4 个整型参数依次 rcx, rdx, r8, r9；其余压栈
_Z7computellllll:
	.seh_endprologue
	lea	r8d, [r8+r8*2]          ; r8   = c*3
	mov	eax, ecx               ; eax  = a  (rcx = 第1参)
	mov	ecx, DWORD PTR 40[rsp]  ; 第5参 e 来自栈 [rsp+40]
	mov	r10d, edx              ; r10  = b  (rdx = 第2参)
	mov	edx, DWORD PTR 48[rsp]  ; 第6参 f 来自栈 [rsp+48]
	lea	eax, [rax+r10*2]        ; eax  = a + b*2
	add	eax, r8d               ;     += c*3
	lea	eax, [rax+r9*4]         ;     += d*4  (r9  = 第4参)
	lea	ecx, [rcx+rcx*4]        ; ecx  = e*5
	lea	edx, [rdx+rdx*2]        ; edx  = f*6
	add	eax, ecx               ;     += e*5
	lea	eax, [rax+rdx*2]        ;     += f*6
	ret
```

源码剖析：`[平台·x86-64 Win64 ABI]` 真实汇编证实——第 1~4 参在 `rcx/rdx/r8/r9`，第 5、6 参在栈偏移 `[rsp+40]`、`[rsp+48]`（因返回地址 8 + 32 字节"影子空间(shadow space)"占 40）。这正是 Windows x64 调用约定，与 System V x86-64（Linux）用 6 个寄存器传参不同。

```cpp
// ⑪ 成员函数的 thiscall(32位) / this 在 x86-64 走 rcx(第1参)
struct Widget { int v; int get() const { return v; } };
// x86-64: Widget::get(Widget const* this) -> this 在 rcx
```

```cpp
// ⑪ extern "C" 统一 ABI 边界：C 函数无 mangling、用 cdecl，是跨编译器/跨语言的安全接口
extern "C" void log_event(const char* msg);   // 任何编译器产出的符号都是裸名 log_event
```

- `[平台·Win64]`：x86-64 上 cdecl/stdcall/fastcall 的区分基本消失（统一为 4 寄存器 + 栈），仅在 32 位代码或特殊互操作时才有意义。
- `[经验]`：写跨编译器库（如 DLL 给 C# P/Invoke、给 Rust FFI）一律用 `extern "C"` + 简单参数（POD/指针），避开 C++ mangling、异常、虚表、STL 容器——这些在不同工具链间不保证二进制兼容。

## ⑫ 内联与优化管道

内联是把被调函数体直接复制到调用点，是绝大多数优化（常量传播、死代码消除）的前提。

```cpp
// ⑫ inline 提示（非强制）；编译器据成本模型决定是否真内联
inline int square(int x) { return x * x; }
int use1(int a) { return square(a) + 1; }   // 很可能被内联
```

```cpp
// ⑫ __attribute__((always_inline)) / [[gnu::always_inline]] 强制内联（GCC/Clang）
//   注意 MSVC 用 __forceinline
[[gnu::always_inline]] inline int triple(int x) { return x * 3; }
int use2(int a) { return triple(a); }
```

```cpp
// ⑫ 优化级别对照： -O0 不内联、不优化；-O2 开全套；-O3 加向量化/循环展开
//   g++ -O0 -S x.cpp   -> 直译式汇编，每个语句对应几条指令
//   g++ -O2 -S x.cpp   -> 内联 + 常量折叠，square(a)+1 可能直接成 lea
//   g++ -O3 -S x.cpp   -> 额外自动向量化(如 SSE/AVX 处理数组)
int add_one(int x) { return x + 1; }
```

```cpp
// ⑫ Link-Time Optimization(LTO)：跨 TU 内联，需 -flto 与配套链接
//   g++ -O2 -flto a.cpp b.cpp -o app   (a/b 间也能内联)
//   clang++ -O2 -flto=thin ...         (ThinLTO 增量)
```

```cpp
// ⑫ 编译器看不到定义时无法内联（跨 TU 默认不内联 -> 用 LTO 或头内 inline）
// foo 在另一 TU 定义，本 TU 只能 call，无法内联
extern int foo(int);
int wrap(int x) { return foo(x) * 2; }
```

- `[实现·GCC13]`：`-O2` 已包含内联（受 `--param max-inline-insns-auto` 等成本预算约束）；`-O3` 提高预算并启用更激进的循环与向量化。
- `[经验]`：热路径把小函数放头文件 `inline` 或开 LTO；但**别盲目 `always_inline`**——内联膨胀会毁掉指令缓存（I-cache），有时反而更慢。

## ⑬ 标准符合度对比（C++23 支持度）

三家的 C++23 实现进度不同，选型前必须查官方状态页（非本机工具，给真实 URL + 标注"官方文档"）。

```cpp
// ⑬ C++23 特性示例：std::expected（错误处理新范式，三家均已支持）
#include <expected>
std::expected<int, const char*> parse(const char* s) {
    if (!s || !*s) return std::unexpected("empty");
    return (int)s[0];
}
```

官方标准符合度文档（标注"官方文档"，需联网查阅）：

- `[标准]` GCC libstdc++：https://gcc.gnu.org/onlinedocs/libstdc++/manual/status.html#status.iso.2023
- `[标准]` Clang libc++：https://libcxx.llvm.org/Status/Cxx23.html
- `[标准]` MSVC STL：https://learn.microsoft.com/cpp/visual-cpp-language-conformance

```cpp
// ⑬ C++23 的 if consteval（编译期分支，三家 C++23 模式均支持）
consteval int compile_time(int x) { return x * 2; }
int f(int v) {
    if consteval { return compile_time(v); }   // 仅在编译期求值分支
    else          { return v + 1; }
}
```

```cpp
// ⑬ 三家对"实验性特性"的门控宏不同：
//   GCC     : __cpp_modules / __cpp_concepts (特性测试宏，ISO 规定)
//   Clang   : 同样支持特性测试宏 __cpp_xxx
//   MSVC    : 也支持 __cpp_xxx，但部分需 /std:c++latest
#ifndef __cpp_modules
#error "本编译器未开启 Modules 支持"
#endif
```

- `[标准]`：特性测试宏（`__cpp_xxx`）是 ISO 规定的可移植探测手段，比"猜版本号"可靠。`[cpp.cond]`
- `[经验]`：不要假设"都支持 C++23"。用 `#ifdef __cpp_xxx` 做特性门控，或构建期查三家官方状态页；MSVC 常需 `/std:c++latest` 才能拿到最新特性。

## ⑭ 诊断与报错质量对比

编译器报错质量直接决定开发体验，这是 Clang 的传统强项。

```cpp
// ⑭ 同一错误在三家中的表现差异（以下为"典型输出"示意，因本机仅装 GCC13）
//   错误：漏写分号 / 模板实参推导失败 / 类型不匹配
template<typename T> T max_of(T a, T b) { return a < b ? b : a; }
auto x = max_of(1, 2.0);   // ❌ 推导冲突：T=int 与 T=double 不一致
```

```cpp
// ⑭ GCC 经典报错（较"朴素"，但 13 已大幅改善）：
//   error: no matching function for call to 'max_of(int, double)'
//   note: candidate template ignored: deduced conflicting types for parameter 'T'
//   （信息正确，但缺"可视化对比箭头"）
```

```cpp
// ⑭ Clang 经典报错（带 ~~~ 下划线与"期望/实际"对照）：
//   note: candidate template ignored: deduced type 'int' for parameter 'T'
//         does not match deduced type 'double' for parameter 'T'
//   （多出代码片段高亮，定位更快）
```

```cpp
// ⑭ MSVC 经典报错（编号体系，需查 MSDN）：
//   error C2782: 'T max_of(T,T)' : template parameter 'T' is ambiguous
//   编号化便于检索文档，但信息密度低
```

- `[经验]`：Clang 的报错/警告最友好（含修复建议 `-fixits`）；GCC 13 已追平大部分；MSVC 报错偏 terse 且用编号。CI 里同时跑 GCC + Clang 可互补抓出对方漏报的警告。
- `[实现·GCC13]`：`-Wall -Wextra -Wpedantic` 是 GCC 基线警告集；Clang 另有 `-Weverything`（过于吵，仅用于一次性审计）。

## ⑮ 模块（Modules）支持现状

Modules（C++20）是 `#include` 的文本包含的语义化替代（详见本书 Modules 章，本处只对比三家工具链支持）。`[标准·modules]`

```cpp
// ⑮ GCC 13：用 -fmodules-ts（仍是技术规范 TS 门控）
//   g++ -std=c++23 -fmodules-ts -c math.ixx -o math.o  生成 BMI(.gcm)
export module math;
export int square(int x) { return x * x; }
```

```cpp
#include <vector>
// ⑮ Clang：最成熟，用 -fmodules 或 -std=c++20（含标准库模块 std）
//   clang++ -std=c++20 -fmodules -c math.cppm -o math.o
import std;                       // Clang 的 std 模块较完整
int use() { std::vector<int> v{1,2,3}; return (int)v.size(); }
```

```cpp
// ⑮ MSVC：用 /std:c++20 + .ixx + /interface
//   cl /std:c++20 /interface math.ixx /c -> math.ifc
export module math;
export int square(int x) { return x * x; }
```

```cpp
// ⑮ 三家的 BMI 格式互不相通！同一模块无法跨编译器复用 .gcm/.ifc
//   所以团队必须锁定"单一编译器 + 固定版本"才能做模块迁移
import math;
int main() { return square(7); }
```

- `[平台]`：GCC 的 BMI 扩展名 `.gcm`、Clang 用 `.pcm`、MSVC 用 `.ifc`——格式均非标准，跨编译器共享不可行。
- `[经验]`：Modules 的最大收益是 `import std;` 省去海量头重解析（大型项目编译常降 30%~70%）；但构建系统（CMake 3.28+/Ninja）需先编接口再编使用方，迁移痛点多在构建侧。

## ⑯ 跨平台与三元组（target triple）

"同一份源码跨平台"靠的是编译器**目标三元组**：`arch-vendor-os-abi`。

```cpp
// ⑯ 指示编译器产出不同平台代码，源码 C++ 不变
//   x86_64-w64-mingw32   -> Windows x64 (MinGW)
//   x86_64-linux-gnu     -> Linux x64
//   aarch64-apple-darwin -> macOS ARM64 (Apple Silicon)
//   riscv64-unknown-elf  -> RISC-V 裸机
int portable() { return sizeof(void*) == 8 ? 8 : 4; }   // 64位平台返回8
```

```cpp
// ⑯ 三元组常经宏暴露给代码，用于条件编译
//   __x86_64__ / __aarch64__ / __riscv  (GCC/Clang 内置宏)
//   _M_X64 / _M_ARM64                    (MSVC 内置宏)
#ifdef __x86_64__
static constexpr bool kIsX64 = true;
#elif defined(__aarch64__)
static constexpr bool kIsX64 = false;
#endif
```

```cpp
// ⑯ 交叉编译：在 x64 主机上为 ARM 设备编出镜像
//   aarch64-linux-gnu-g++ main.cpp -o main_arm   (工具链前缀即三元组前缀)
//   注意：交叉编译出的目标文件是 ELF(ARM)，不能在 x64 主机直接运行
int cross() { return 0; }
```

- `[平台]`：三元组决定**默认调用约定、字长、ABI、目标文件格式**——`x86_64-w64-mingw32` 用 Win64 调用约定 + COFF/PE，`x86_64-linux-gnu` 用 System V 约定 + ELF。
- `[经验]`：跨平台库在 CI 里用交叉工具链（如 `aarch64-linux-gnu-g++`）做编译验证，比等真机便宜得多；但**运行验证**仍需真机或 QEMU。

## ⑰ 调试信息：DWARF vs PDB

调试器需要知道"机器码地址 ↔ 源码行 ↔ 变量名"的映射，这就是调试信息格式的差异点。

```cpp
// ⑰ GCC/Clang 在 ELF/Mach-O 上产出 DWARF（嵌入 .debug_* 段或独立 .dwo）
//   g++ -g -O2 main.cpp -o main     (-g 开启 DWARF)
//   DWARF 是开放标准，gdb/lldb 通用
int traced(int x) { return x * x; }   // 断点可停在源码行，变量可见
```

```cpp
// ⑭/⑰ MSVC 产出 PDB（Program Database），由 link.exe /DEBUG 生成
//   cl /Zi /EHsc main.cpp /link /DEBUG   -> main.exe + main.pdb
//   PDB 是 Microsoft 专有格式，VS / WinDbg 使用
int traced2(int x) { return x + 1; }
```

```cpp
// ⑰ 拆分调试信息（发布时分离，减小二进制）：
//   GCC : objcopy --only-keep-debug a.out a.debug ; strip a.out
//         gdb 需要时再 "symbol-file a.debug"
//   Clang 亦支持 -gsplit-dwarf 把 DWARF 放 .dwo
int release(int x) { return x; }
```

- `[平台·ELF]`：DWARF 是开放标准，被 gdb/lldb/LLDB 跨平台支持；PDB 是 MS 专有，仅 Windows 工具链。
- `[经验]`：发布版保留 `-g` 再 `strip` 出独立符号文件，既能调试又减小交付体积；**永远别用 `-O0` 做性能评测**——优化会大幅改变真实行为。

## ⑱ 与构建系统集成

编译器很少被手写命令直接调用，而是藏在构建系统之下。

```cpp
// ⑱ Make：手写规则，命令即 g++（最透明，但大项目维护成本高）
//   %.o: %.cpp
//       g++ -std=c++23 -O2 -c $< -o $@
int build_make() { return 0; }
```

```cpp
// ⑱ CMake：跨编译器/跨平台生成器（可产 Makefile / Ninja / VS 工程）
//   cmake_minimum_required(VERSION 3.28)
//   project(demo CXX)
//   set(CMAKE_CXX_STANDARD 23)
//   add_executable(demo main.cpp)
//   换工具链只需 -DCMAKE_CXX_COMPILER=clang++ 或指定 toolchain 文件
int build_cmake() { return 0; }
```

```cpp
// ⑱ Bazel / Ninja：Google/Chrome 等超大型项目用，增量编译极快
//   Ninja 由 CMake 生成 build.ninja，背后仍调用 g++/clang++
//   MSBuild：Visual Studio 的构建引擎，驱动 cl.exe + link.exe
int build_bazel() { return 0; }
```

```cpp
// ⑱ 模块要求构建系统保证"先编接口单元"的依赖序
//   CMake 3.28+ 自动识别 export module 单元并排定顺序；
//   旧 Make 需手动写规则先编 .ixx 再编使用者
export module demo;
export int answer() { return 42; }
```

- `[经验]`：构建系统选 CMake（跨平台事实标准）、Bazel（超大规模）、MSBuild（纯 Windows/VSS）；核心原则是"编译器可换、构建脚本不变"。
- `[经验]`：把编译器标志集中在 `CMAKE_CXX_FLAGS`/顶层变量，别散落进每条命令；统一 `-Wall -Wextra` 让警告不被遗漏。

## ⑲ [经验]选型建议

选型没有银弹，按场景决策。

```cpp
// ⑲ 场景 → 推荐（经验法则，非铁律）
//   科学计算/超算/Linux 服务   -> GCC（libstdc++，最长历史、最优数值代码）
//   macOS/iOS/IDE 体验/静态分析 -> Clang（clangd、最佳诊断、libc++）
//   纯 Windows 桌面/游戏/驱动   -> MSVC（PDB、/EH、MS-STL、VS 集成）
//   跨平台库(对外发布)          -> 三套全验 + extern "C" ABI 边界
int choose() { return 0; }
```

```cpp
// ⑲ 团队工具链统一原则：锁版本！
//   例：CMakePresets.json 固定 compiler + version，避免"我机器能编"问题
//   { "cacheVariables": { "CMAKE_CXX_COMPILER": "g++-13" } }
```

- `[经验]`：CI 同时跑 GCC + Clang 可互补抓警告/UB；但**发布二进制只认一种编译器**，避免混链不同 STL 引发的 ODR/ABI 灾难。
- `[经验]`：嵌入式/裸机优先 GCC（支持架构最多）；想要 LLVM 基础设施（JIT/自定义 Pass）选 Clang/LLVM；Windows 原生体验选 MSVC，跨平台 Windows 构建选 MinGW 或 clang-cl。

## ⑳ 速查表

编译器命令与关键差异总览：

```cpp
// ⑳ 三巨头最小可用命令速查
//   GCC     : g++ -std=c++23 -O2 -Wall -Wextra main.cpp -o main
//   Clang   : clang++ -std=c++23 -O2 -Wall -Wextra main.cpp -o main
//   MSVC    : cl /std:c++20 /O2 /EHsc /W4 main.cpp /Fe:main.exe
int main() { return 0; }
```

| 维度 | GCC 13 | Clang/LLVM | MSVC |
|---|---|---|---|
| 标准库 | libstdc++ | libc++ | MS-STL |
| 调试格式 | DWARF | DWARF | PDB |
| 目标格式 | ELF/COFF/Mach-O | ELF/COFF/Mach-O | COFF/PE |
| 默认异常 | Itanium zero-cost | Itanium zero-cost | SEH(/EH) |
| mangling | Itanium (`_Z`) | Itanium (`_Z`) | MSVC (`?name@@...`) |
| 模块标志 | `-fmodules-ts` | `-fmodules`(最成熟) | `/std:c++20` + `.ixx` |
| LTO | `-flto` | `-flto[=thin]` | `/LTCG` |
| 诊断体验 | 中(13 已改善) | 最佳 | 偏 terse(编号) |
| 内置宏(64) | `__x86_64__` | `__x86_64__` | `_M_X64` |
| 强制内联 | `[[gnu::always_inline]]` | 同左 | `__forceinline` |

```cpp
// ⑳ 取证命令速查（本机 GCC13 + c++filt 已验证可用）
//   g++ -std=c++23 -O2 -S -masm=intel x.cpp -o x.asm   // 取真实汇编
//   c++filt _Z1fi                                     // -> f(int)
//   g++ -fdump-tree-gimple x.cpp                      // 看 GIMPLE
//   g++ -E x.cpp | tail                               // 看预处理结果
//   readelf -s x.o  /  objdump -t x.o                 // 看符号表(需 ELF 工具)
int trivia(int x) { return x; }
```

- `[平台]`：mangling、vtable 布局、异常模型、目标格式均属 ABI 层；GCC 与 Clang 共享 Itanium ABI，因此 `.o` 可互通，但与 MSVC 不互通。
- `[经验]`：记住一句话——**源码可移植靠 ISO 标准，二进制可链接靠 ABI 一致**。换编译器或换 STL 版本都可能破坏 ABI；对外发布的库用 `extern "C"` + 稳定 POD 接口最稳。


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第12章](Book/part02_toolchain/ch12_buildsystems.md) | 配置解析/API响应 | 本章提供概念，第12章提供实现 |
| [第69章](Book/part06_templates/ch69_constexpr.md) | 泛型库/编译期计算 | 本章提供概念，第69章提供实现 |
| [第157章](Book/part14_perf/ch157_compiler_explorer.md) | 错误恢复/不可恢复错误 | 本章提供概念，第157章提供实现 |

## 附录 E：编译器面试与设计 [B: Principle / H: Design / I: Practice / J: Learning]

```
C++编译器选择的工业现实:

Google: GCC (Linux) + Clang (macOS) + MSVC (Windows)
  → 原因: 每个平台的native编译器性能最优

LLVM: 自举 (Clang编译Clang) → 验证编译器正确性
  → Clang编译LLVM = ~30min (16核, debug), ~5min (release, ccache)

Chromium: Clang (跨平台统一) + MSVC (Windows兼容性)
  → 2018年全平台切换到Clang, 减少编译器差异bug

游戏引擎 (Unreal/Unity):
  → MSVC (Windows/开发) + Clang (Mac/iOS) + GCC (Linux/server)
  → 每个编译器必须通过完全相同的测试矩阵
```

```cpp
#include <iostream>
int main() {
    std::cout << "GCC: Linux default, GPLv3, ~13M lines C/C++" << std::endl;
    std::cout << "Clang: LLVM native, Apache2, ~5M lines C++" << std::endl;
    std::cout << "MSVC: Windows native, proprietary, ~15M lines C++" << std::endl;
    std::cout << "Q: why 3 compilers? A: different ABIs, optimizations, platforms" << std::endl;
    return 0;
}
```

| 编译器 | 平台 | 许可证 | 特点 |
|---|---|---|---|
| GCC | Linux/Windows/macOS | GPLv3 | 最完整C++23支持 |
| Clang | Linux/Windows/macOS | Apache2 | 最好错误信息, LLVM后端 |
| MSVC | Windows | Proprietary | Windows生态最优化 |

面试: GCC vs Clang? GCC=兼容性最好; Clang=错误信息最好, 工具化(LLVM)
       -O2 vs -O3? -O2=标准优化; -O3=更激进(循环展开+向量化, 可能增二进制)


## 相关章节（交叉引用）

- **后续依赖**：`Book/part02_toolchain/ch16_ide.md`（第16章　IDE 与编辑器：VSCode / CLion / QtCreator / VIM（C++））—— 本章为其前置，建议后续延伸阅读。
- **后续依赖**：`Book/part02_toolchain/ch17_crosscompile.md`（第17章　交叉编译与嵌入式工具链（C++））—— 本章为其前置，建议后续延伸阅读。
- **相邻主题**：`Book/part01_history/ch10_version_matrix.md`（第10章　版本特性全景对照表与迁移指南）—— 编号相邻、主题接续。
- **相邻主题**：`Book/part01_history/ch09_cpp26.md`（第09章　C++26：已确定特性与方向）—— 编号相邻、主题接续。
- **相邻主题**：`Book/part02_toolchain/ch13_packaging.md`（第13章　包管理：vcpkg / Conan（C++））—— 编号相邻、主题接续。
- **同模块**：`Book/part02_toolchain/ch14_debugging.md`（第14章　调试与诊断：GDB / LLDB / Sanitizer / Valgrind（C++））—— 同模块下的其他主题。

## 附录 F：工业实战复盘与设计取舍 [I: Practice / H: Design]

### 工业案例（真实可查证）

- **同一份代码在 GCC/MSVC 下行为不同**：`std::unordered_map` 的迭代顺序、浮点 `constant folding` 精度、结构体对齐填充在两家 ABI 下不一致，曾导致跨平台序列化字节差、网络协议握手失败。生产上用 `static_assert(sizeof(T)==N)` 锁定布局。
- **`-O2` 优化暴露 UB**：某些代码在 `-O0` 正常、`-O2` 崩溃——编译器基于「无 UB」假设做死代码消除（DCE）。典型如 `signed` 溢出、空指针「只是读一下」、有符号位移未定义。这是优化器信任契约的代价。

### 常见 Bug 与 Debug 方法

- **优化相关崩溃**：二分法降优化等级（`-O1`→`-O0`）定位；`-fsanitize=undefined` 抓 UB（溢出/移位/对齐）；`-fno-elide-constructors` 隔离拷贝省略干扰。
- **模板/宏报错**：`-fdiagnostics-show-template-tree` 折叠模板树；`-E` 看预处理展开确认宏污染。
- **Code Review 关注点**：是否依赖实现定义行为（如 `char` 符号性、指针大小）；`#pragma`/`__attribute__` 是否可移植（用 `__has_builtin`/`__has_cpp_attribute` 守护）。

### 设计取舍（Trade-off）与反模式（Anti-Pattern）

| 维度 | 选择 | 代价 |
|------|------|------|
| 标准化 | 只依赖 ISO C++ 可移植子集 | 放弃平台特化性能 |
| 诊断 | 全量开启 `-Wall -Wextra -Werror` | 第三方头文件噪音大 |
| 优化 | `-O2` 平衡 / `-O3` 激进 | `-O3` 可能增大二进制、回归 |

- **反模式**：在头文件里 `#pragma GCC optimize("O3")`（破坏 TU 一致性、ODR 风险）；用 `-fpermissive` 掩盖错误而非修根因；跨模块传 `long double`（x86 80-bit vs ARM 64-bit 不兼容）。
- **API Design**：对外库头用 `__cplusplus` 守护特性；错误用 `[[nodiscard]]` 防止忽略返回值；暴露 `inline` 接口减少 ABI 面。

### 重构建议

把「依赖实现定义的位操作」重构为 `<cstdint>` 固定宽度类型 + `std::bit_cast`；把 `-fpermissive` 容忍的含糊构造改为显式 `static_cast`，让 `-Werror` 能上 CI。

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

写一个 `max` 函数模板，要求对任意可比较类型都能用，且对混合有符号/无符号比较安全。

<details><summary>答案与解析</summary>

使用 `std::common_comparison_category` 或 `std::cmp_less` 避免符号陷阱：

```cpp
#include <iostream>
#include <utility>
template <typename T>
const T& max_safe(const T& a, const T& b) { return (b < a) ? a : b; }
int main() { std::cout << max_safe(3, 7) << '\n'; }
```

[标准] 模板参数推导按实参进行；两实参同类型时 `T` 唯一确定。

</details>

### 练习 2（难度 ★★）

用 `std::integral` 概念约束一个 `add` 函数，使其只接受整数类型，并对浮点调用给出清晰的错误。

<details><summary>答案与解析</summary>

C++20 概念取代 SFINAE 做编译期约束：

```cpp
#include <iostream>
#include <concepts>
template <std::integral T> T add(T a, T b) { return a + b; }
int main() { std::cout << add(2, 3) << '\n'; /* add(1.0, 2.0) 编译失败 */ }
```

[标准] 违反概念约束是硬错误（而非 SFINAE 静默失败），诊断信息更可读。

</details>

### 练习 3（难度 ★★）

写一个 `constexpr` 阶乘函数，并用 `static_assert` 在编译期验证 `fact(5)==120`。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
constexpr int fact(int n) { return n <= 1 ? 1 : n * fact(n - 1); }
static_assert(fact(5) == 120);
int main() { std::cout << fact(5) << '\n'; }
```

[标准] `constexpr` 函数在常量表达式上下文（如模板实参、`static_assert`）中于编译期求值。

</details>

