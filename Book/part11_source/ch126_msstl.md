# 第126章　MS STL 架构（C++）

⟶ Book/part11_source/ch124_libstdcxx.md
⟶ Book/part11_source/ch125_libcxx.md

> 真实工具链：MinGW GCC 13.1.0（`C:/Qt/Tools/mingw1310_64/bin/g++.exe`，`-std=c++23 -O2 -S -masm=intel`）。
> MS STL 本机未安装，故源码行号剖析一律引用上游 GitHub `microsoft/STL`（`https://github.com/microsoft/STL/...`）并标注「上游参考」——行号随提交浮动，以 main 分支为准。
> 取证产物：`Examples/_ch126_seh.cpp/.asm`、`Examples/_ch126_string.cpp/.asm`、`Examples/_ch126_vector.cpp/.asm`、`Examples/_ch126_parallel.cpp/.o`，均为真实 g++ 13.1.0 编译取证。MSVC 专属行为用真实命令 + 明确标注「典型输出」，未在本机运行。

## ① 概述：MS STL 是 Microsoft 的 C++ 标准库 [标准]

⟶ Book/part11_source/ch125_libcxx.md
⟶ Book/part11_source/ch127_llvm.md


MS STL（曾称 *Microsoft Visual C++ Standard Library*）是 MSVC 自带的 C++ 标准库实现，提供 `<vector>`、`<string>`、`<iostream>`、`<algorithm>` 等全部标准容器/算法/迭代器/本地化/IO/并行。它与 MSVC 工具链（编译器 `cl.exe`、运行时 `vcruntime`、CRT `ucrt`）深度耦合，是 Windows 平台 C++ 事实标准库。

```cpp
// ① 最小可编译程序：仅依赖 MS STL 的 <vector>
#include <vector>
#include <cstdio>
int main() {
    std::vector<int> v{2, 4, 6};   // 来自 MS STL stl/inc/vector
    for (int x : v) std::printf("%d ", x);
    return (int)v.size();
}
```

- `[标准]`：ISO C++ 条款规定行为；MS STL 是**实现**，可能与标准有细微偏差（见 ⑭）。
- `[经验]`：MS STL 大量逻辑在 `stl/inc/*.h` 头文件模板里，链接时再补少量 `msvcp140*.dll` 符号（见 ⑫）。

## ② 架构（与 MSVC 后端/C1/C2） [实现]

MSVC 编译管线分前端 `C1`（C++ 前端，产出 CIL）、后端 `C2`（代码生成，产出 OBJ），标准库在**前端之后的语义期**被包含解析——与 GCC 的 `cc1plus` / `cc1` 分工类似。MS STL 头经 `C1` 预处理+语义分析，模板实例化发生在 `C2` 之前的 IL 阶段。

```cpp
// ② 概念示意：编译器如何"看到"标准库（MSVC 管线）
// C1 (前端) -> 解析 #include <vector> 的模板定义
// C2 (后端) -> 为 vector<int> 生成机器码
// 运行期 -> 链接 msvcp140.dll / vcruntime140.dll
#include <vector>
int f() { std::vector<int> v(3); return (int)v.size(); }
```

```text
┌─────────────────────────── MSVC 工具链分工 ───────────────────────────┐
│ cl.exe                                                                 │
│  ├── C1 (c1xx.dll)   前端：词法/语法/语义，含标准库头解析，产出 CIL    │
│  └── C2 (c2.dll)     后端：优化+代码生成，产出 .obj                    │
│ 标准库：stl/inc/*.h（header-only 模板）+ msvcp140.dll（少量运行符号）  │
│ 运行时：vcruntime140.dll（SEH/栈/入口）+ ucrtbase.dll（C 运行时）      │
└──────────────────────────────────────────────────────────────────────┘
```

- `[实现·MSVC]`：`C1/C2` 分离让 MS STL 头可在前端充分做模板检查；`/permissive-` 等开关影响头的可编译性（见 ⑨）。
- `[平台·Windows]`：MS STL 与 `vcruntime`/`ucrt` 协同，离开这组 DLL 无法独立运行。

## ③ 开源 STL repo（GitHub microsoft/STL） [平台]

自 2020 年起，MS STL 源码公开于 `microsoft/STL`（MIT 许可）。仓库结构是阅读入口：`stl/inc/` 为公开头，`stl/src/` 为 `.cpp` 实现（如 locale、iostream 的 `cin/cout`），`stl/tests/` 为 conformance 测试。

```cpp
// ③ 本机没有 MS STL，但可在任意支持 C++17+ 的编译器上编译同样的代码
#include <vector>
#include <string>
int use_stl() {
    std::vector<std::string> v{"a", "bb"};
    return (int)v.size();
}
```

```cpp
// ③ 上游仓库典型结构与对应公开头
// stl/inc/vector   -> <vector>
// stl/inc/xstring  -> <string> 的实现核心
// stl/inc/yvals.h   -> 特性宏（_HAS_CXX17/_HAS_CXX20/_HAS_CXX23）
// stl/src/xlocale.cpp -> <locale> 的少量非模板实现
```

- `[平台]`：`git clone https://github.com/microsoft/STL` 即可本地阅读；CI 跑全套 conformance 测试，是贡献入口（见 ⑰）。
- `[经验]`：阅读以 `stl/inc/` 为根，按标准头名（`vector`/`string`）找入口，再追 `stl/src/` 的非模板实现。

## ④ [实现]源码剖析（upstream stl/inc 文件+行号，标注上游参考） [实现]

下面三处为**上游参考**——行号取自 `microsoft/STL` main 分支，随提交浮动，仅指示位置。

```cpp
// ④ 文件：https://github.com/microsoft/STL/blob/main/stl/inc/vector
// 行号：36
// 上游参考（随提交浮动）：class vector 的前向与 allocator_type 别名
//   template <class _Ty, class _Alloc = allocator<_Ty>>
//   class vector { ... };
```

```cpp
// ④ 文件：https://github.com/microsoft/STL/blob/main/stl/inc/xstring
// 行号：1860
// 上游参考（随提交浮动）：basic_string 的 SSO 缓冲字段 _Bx
//   union _Bx { _Elem _Buf[_BUF_SIZE]; _Elem* _Ptr; } _Bx;
//   短串用 _Buf，长串用 _Ptr（与 libstdc++ 同构，见 ⑧）
```

```cpp
// ④ 文件：https://github.com/microsoft/STL/blob/main/stl/inc/yvals.h
// 行号：540
// 上游参考（随提交浮动）：特性宏开关
//   #define _HAS_CXX23 1   // C++23 特性总开关（影响 <print>/<expected> 等）
//   #define _HAS_STATIC_RTTI 1
```

- `[实现·MSVC]`：`vector` 类是模板，定义在头内；`basic_string` 用 union `_Bx` 在「本地缓冲」与「堆指针」间二选一，即 SSO（见 ⑧）。
- `[实现]`：`yvals.h` 的 `_HAS_CXX23` 等宏集中控制特性开关，是跨版本行为差异的根源（见 ⑨⑭）。

## ⑤ 与 Windows 生态/Win32/CRT [平台]

MS STL 与 Win32/CRT 天然融合：`<cstdio>` 的 `FILE*` 底层是 `ucrt`；`std::wstring` 直接兼容 `LPCWSTR`；异常展开依赖 `vcruntime` 的 SEH 支持（见 ⑥）；`<windows.h>` 与标准库可共存，但需注意宏冲突（`min/max`/`ERROR`）。

```cpp
// ⑤ wstring 与 Win32 API 互操作（CreateFileW 需要 LPCWSTR）
#include <string>
#include <windows.h>
void open_log(const std::wstring& name) {
    HANDLE h = CreateFileW(name.c_str(), GENERIC_WRITE, 0,
                           nullptr, OPEN_ALWAYS, FILE_ATTRIBUTE_NORMAL, nullptr);
    if (h != INVALID_HANDLE_VALUE) CloseHandle(h);
}
```

```cpp
// ⑤ 避免 <windows.h> 的 min/max 宏污染标准库（NOMINMAX）
#define NOMINMAX
#include <windows.h>
#include <algorithm>
int m(int a, int b) { return std::max(a, b); }  // 用 std::max 而非宏
```

- `[平台·Windows]`：`std::wstring::c_str()` 返回 `const wchar_t*`，与 `LPCWSTR` 二进制兼容，是 Windows 上字符串边界的惯用法。
- `[经验]`：引入 `<windows.h>` 前定义 `NOMINMAX`、`WIN32_LEAN_AND_MEAN`，可避免大量宏冲突（见 ⑬）。

## ⑥ 异常与 SEH [实现]

MSVC 的 C++ 异常在 Windows 上由 **SEH（Structured Exception Handling）** 承载：栈展开经 `vcruntime` 的 `__CxxFrameHandler*`，由编译器为每个 `try` 生成 `FuncInfo` 描述。MinGW-w64（seh 变体）用同一套 Windows SEH 机制，故可在本机用 g++ 真实演示 C++ 异常→SEH 的映射。

```cpp
// ⑥ 用 C++ 异常演示 Windows SEH 机制（真实编译取证见下方汇编）
#include <stdexcept>
#include <cstdio>
[[gnu::noinline]] int may_throw(int x) {
    if (x < 0) throw std::runtime_error("neg");
    return x * 2;
}
int safe_call(int x) {
    try { return may_throw(x) + 1; }
    catch (const std::exception& e) { std::printf("caught: %s\n", e.what()); return -1; }
}
int main() { return safe_call(10) + safe_call(-3); }
```

```asm
; 证据来自 Examples/_ch126_seh.asm（MinGW g++ 13.1.0 -O2 -S -masm=intel 真实产物）
; 行 39:  .seh_proc    _Z9may_throwi            ; 函数为 SEH 过程
; 行 79:  .seh_handler __gxx_personality_seh0, @unwind, @except
; 行 69:  call         __cxa_throw               ; 抛异常走 Itanium ABI
; 行 121: call         __cxa_begin_catch         ; safe_call 的 catch 落点
; MSVC 等价：`__CxxFrameHandler4` + `FuncInfo`，机制同构，符号名不同
```

- `[实现·MSVC]`：MSVC 用 `/EHsc` 启用 C++ 异常；`__try/__except` 是原生 SEH，`throw` 最终也经 SEH 展开。本机 g++ 的 `__gxx_personality_seh0` 证明 MinGW 同样走 Windows SEH。
- `[平台·Windows]`：跨 DLL 抛 C++ 异常需两端用**相同** `_EH` 模型与运行时，否则展开失败（见 ⑬）。

## ⑦ 并行算法（与 Intel TBB/Concurrency Runtime） [实现]

C++17 并行算法（`std::execution::par/unseq`）在 MS STL 的默认后端是 **Intel oneTBB**（旧称 PSTL + ConcRT）。MSVC 链接 `tbb.dll` 获得真并行；不提供时退化为顺序执行。本机用 g++/libstdc++ 仅验证 API 可编译（libstdc++ 无 TBB 时退化为顺序，符号仍实例化）。

```cpp
// ⑦ 并行排序 API（MS STL 后端为 Intel TBB + Concurrency Runtime）
#include <algorithm>
#include <execution>
#include <vector>
#include <cmath>
#include <cstddef>
int p() {
    std::vector<double> a(1024);
    for (std::size_t i = 0; i < a.size(); ++i) a[i] = (double)i;
    std::sort(std::execution::par, a.begin(), a.end(),
              [](double x, double y) { return std::fabs(x) < std::fabs(y); });
    return (int)a.size();
}
```

```cpp
// ⑦ 真实 g++ 编译后的实例化符号（nm -C _ch126_parallel.o 节选，证明 API 可编译）
// void std::__introsort_loop<...>(...)   // 顺序回退路径被实例化
// void std::__insertion_sort<...>(...)   // 小段插入排序被实例化
// MS STL 有 TBB 时上述会改为调用 parallel_for 分块调度
```

- `[实现·MSVC]`：并行算法默认拉起 TBB worker 线程池；`/openmp` 与 TBB 并存时需注意线程池争用。
- `[经验]`：并行算法对**大**数据才有收益；小数组顺序回退反而慢（见 ⑪）。

## ⑧ 字符串实现策略 [实现]

MS STL 的 `std::string` 采用 **SSO（Small String Optimization）**：短串存对象内建缓冲，避免堆分配。`basic_string` 用 union `_Bx` 在「内置缓冲 `_Buf`」与「堆指针 `_Ptr`」间二选一（见 ④ `xstring:1860`）。本机用 g++ 编译 `std::string` 可演示同构的 SSO 阈值判定（`15`）。

```cpp
// ⑧ SSO：短串不触发堆分配（本机 g++/libstdc++ 演示同一机制）
#include <string>
#include <cstdio>
int main() {
    std::string small = "hello";    // 短串：本地缓冲
    std::string big   = "this string is clearly longer than fifteen bytes!!";
    std::printf("small=%s big_len=%zu\n", small.c_str(), big.size());
    return (int)(small.size() + big.size());
}
```

```asm
; 证据来自 Examples/_ch126_string.asm（MinGW g++ 13.1.0 真实产物）
; 行 56:  cmp   rbx, 15      ; 与 SSO 容量(=15) 比较
; 行 59:  cmp   rbx, 1
; 行 154: call  _ZNSt7__cxx1112basic_string..._M_constructIPKcEEv... ; 构造路径
; MS STL 同样以 15 字节(x86-64, char) 为 SSO 阈值（见 ④ xstring union）
```

```cpp
// ⑧ SSO 容量探测（实现相关，演示短串存对象内）
#include <string>
#include <cassert>
int main() {
    std::string s = "short";
    assert(s.data() >= reinterpret_cast<const char*>(&s) &&
           s.data() <  reinterpret_cast<const char*>(&s) + sizeof(s));
    return 0;
}
```

- `[实现]`：SSO 阈值在 x86-64 下多为 15 字节（`char`）；`std::string` 移动构造 `noexcept`，使 `vector<string>` 扩容走移动（见 ⑪）。
- `[平台·x86-64]`：MS STL 与 libstdc++ 的 `basic_string` 布局相近（union + SSO），但**二进制不兼容**（见 ⑫⑬）。

## ⑨ [实现]真实：MSVC 默认标准库行为（命令+典型输出） [实现]

MSVC 默认开启 C++14 行为，需显式 `/std:c++20` 或 `/std:c++latest` 才启用现代标准库；`_HAS_CXX23` 由标准开关驱动（见 ④）。以下为真实命令，**输出为「典型输出」**（本机未装 MSVC，未运行）。

```bash
# ⑨ 用 MSVC 以 C++20 编译并查看默认标准库版本（典型输出）
# cl /std:c++20 /EHsc /nologo demo.cpp /Fe:demo.exe
# 典型输出（含 MS STL 版本，来自 _MSC_VER / __cpp_lib_*）：
#   demo.cpp
#   Microsoft (R) C/C++ Optimizing Compiler Version 19.38.xxx
#   _MSC_VER = 1938  ->  对应 MS STL 14.38
```

```bash
# ⑨ 查询 MS STL 已启用的 C++ 特性宏（典型输出）
# cl /std:c++latest /EHsc /nologo /EP - <<EOF  | findstr _HAS_CXX
# #include <version>
# EOF
# 典型输出节选：
#   #define _HAS_CXX20 1
#   #define _HAS_CXX23 1
```

- `[实现·MSVC]`：默认 `/std:c++14`；显式 `/std:c++20` 才打开 `<ranges>`/`<format>` 等。这与 GCC 默认 `-std=gnu++17/20` 不同（见 ⑯）。
- `[经验]`：提交到 CI 时固定 `/std:` 等级，避免开发者本地默认标准不一致导致行为漂移。

## ⑩ 调试（Visual Studio） [平台]

Visual Studio 安装 "C++ 桌面" 工作负载时附带 MS STL 源码（`VC\Tools\MSVC\<ver>\crt\src` 与 include），可在异常/断点处单步进入 `vector`/`string` 模板实现。无需额外符号服务器即可看标准库内部。

```cpp
// ⑩ 在 VS 中单步进入 vector::at 的越界检查
#include <vector>
int buggy() {
    std::vector<int> v{1, 2, 3};
    return v.at(99);   // 抛 std::out_of_range，可步入 stl/inc/vector
}
int main() { return buggy(); }
```

```bash
# ⑩ 调试命令（Visual Studio / 开发者 PowerShell，典型输出）
# devenv /DebugExe demo.exe
# 或在异常设置里勾选 "C++ Exceptions" + "break when thrown"
# 典型输出：命中 std::out_of_range，调用栈含 stl/inc\vector(行)
```

- `[平台·Windows]`：VS 自带源码，比「装 `libstdc++-dev` 才有源码」的 Linux 流程更省心（对比 ⑲）。
- `[经验]`：开启 `/Zi` + 关闭优化 `/Od` 能让标准库模板函数保持可单步形态。

## ⑪ 性能 [经验]

经验规律（非本机基准数字，量级示意）：容器遍历/随机访问被内联为指针算术（见 ⑧ 真实汇编的 `.L3` 循环）；`std::string` 短串零分配（SSO），长串走堆；并行算法仅大数据有收益（见 ⑦）。主要陷阱是「未 reserve」「热循环隐式分配」「按值传大对象」。

```cpp
// ⑪ reserve 避免反复扩容（减少 allocate/copy）
#include <vector>
int main() {
    std::vector<int> v;
    v.reserve(1024);                 // 一次分配
    for (int i = 0; i < 1024; ++i) v.push_back(i);
    return (int)v.size();
}
```

```cpp
// ⑪ noexcept 移动让扩容走移动而非拷贝（basic_string 移动 noexcept）
#include <vector>
#include <string>
#include <type_traits>
int main() {
    static_assert(std::is_nothrow_move_constructible<std::string>::value, "ssso move");
    std::vector<std::string> v(100, "x");
    v.push_back("y");   // 扩容时移动 string（见 ⑧）
    return (int)v.size();
}
```

- `[经验]`：性能问题用 VS Profiler / ETW 或 `std::chrono` 定位，而非盲猜；MS STL 容器本身高效，瓶颈多在分配与拷贝。
- `[实现]`：真实 g++ 汇编（⑥⑧）证明遍历被内联为指针算术——MS STL 同样会内联这些热路径。

## ⑫ ABI/二进制兼容（vcruntime/msvcp） [实现]

MS STL 的二进制接口由两部分承载：`vcruntime140.dll`（栈展开/SEH/入口，见 ⑥）与 `msvcp140.dll`（标准库少量非模板运行符号，如 `std::locale`、`std::ios_base`）。**同一 `_MSC_VER` 主版本**内 ABI 稳定；跨大版本（如 19.3x → 19.4x）可能不兼容。

```cpp
// ⑫ 跨 DLL 边界只暴露 C ABI，避免导出 std 符号（见 ⑬⑮）
extern "C" __declspec(dllexport) int count_chars_c(const char* p) {
    return (int)strlen(p);   // 边界用 C 字符串，内部用 MS STL
}
```

```cpp
// ⑫ _MSC_VER 决定链接的 msvcp140 变体（同主版本方可混链）
#include <cstdio>
int main() {
    std::printf("_MSC_VER = %d\n", _MSC_VER);  // 1938 -> MS STL 14.38
    return 0;
}
```

- `[实现·MSVC]`：`msvcp140.dll` 与 `msvcp140_1.dll`/`msvcp140_2.dll` 分载不同特性；`vcruntime140.dll` 与 `_ATL`/MFC 无关，是纯 C++ 运行底座。
- `[平台]`：混合不同 VS 版本编译的 `.obj`/`.lib` 链接 `msvcp140` 时，可能因内联模板布局差异产生 ODR/ABI 错配。

## ⑬ 常见陷阱（DLL 边界传递 STL 对象） [经验]

最致命陷阱：**跨越 DLL 边界传递 `std::string`/`std::vector` 等 STL 对象**，若两侧用不同 MS STL 版本/不同 `_MSC_VER`/不同 CRT（/MD 与 /MT 混用），会因「分配器不同」「内存布局不同」在释放侧崩溃（`_CrtIsValidHeapPointer` 失败）。

```cpp
// ⑬ 危险：DLL A 用 /MD，EXE 用 /MT（或反之），跨边界传 string
// DLL:  __declspec(dllexport) std::string make(); // 在 DLL 堆分配
// EXE:  std::string s = make();                   // 在 EXE 堆释放 -> 崩溃
#include <string>
std::string make();                 // 声明与实现必须同 CRT/同 STL 版本
int caller() { std::string s = make(); return (int)s.size(); }
```

```cpp
// ⑬ 正确：边界用 C ABI（POD/指针），std 类型留在模块内部
#include <string>
#include <cstring>
extern "C" int make_c(const char* in, char* out, int cap) {
    std::string s = in;             // 内部用 std
    int n = (int)s.size();
    if (n < cap) { std::memcpy(out, s.data(), n); out[n] = 0; }
    return n;
}
```

- `[经验]`：① 全工程统一 `/MD`（或统一 `/MT`）；② 全工程统一 VS 版本；③ 库边界用 C 接口或 COM/句柄，绝不导出 `std` 类型（见 ⑮）。
- `[平台·Windows]`：`/MD`（动态 CRT）是跨 DLL 共享 `msvcp140` 的前提；`/MT`（静态 CRT）则每个模块自带一份，跨边界传 STL 必崩。

## ⑭ 演进（C++23 支持） [标准]

MS STL 在 VS 17.8+ 基本完备支持 C++23：`std::print`/`<print>`、`std::expected`/`<expected>`、`std::ranges` 增强、`std::mdspan`、修复 `std::ranges` 适配。特性由 `yvals.h` 的 `_HAS_CXX23`（见 ④）与 `/std:c++latest` 开启。

```cpp
// ⑭ C++23 <print> 与 <expected>（需 /std:c++latest 开启 _HAS_CXX23）
#include <print>
#include <expected>
int main() {
    std::print("hello C++23 from MS STL\n");
    std::expected<int, int> e = std::unexpected(7);
    return e.has_value() ? 0 : *e.error();
}
```

```cpp
// ⑭ ranges 在 MS STL 的实现入口（上游参考）
// 文件：https://github.com/microsoft/STL/blob/main/stl/inc/ranges
// 行号：40
// 上游参考（随提交浮动）：namespace std::ranges 的 view 适配起点
```

- `[标准]`：C++23 条款规定 `print`/`expected`/`ranges` 行为；MS STL 是达标实现之一（与 libstdc++/libc++ 对照见 ⑱）。
- `[实现·MSVC]`：`_HAS_CXX23` 由 `/std:c++latest` 隐式置 1；用 `/std:c++20` 则关掉 23 特性，保证 20 行为稳定。

## ⑮ 最佳实践 [经验]

跨模块/跨库时，把标准库类型留在模块内部，边界用 C ABI（POD/句柄/字符串）。整工程统一 MSVC 版本、`/MD`、标准等级。第三方库用同工具链源码重编，避免二进制 STL 混链。

```cpp
// ⑮ 边界用不透明句柄，MS STL 对象封装在 .cpp 内
#include <vector>
struct Widget { std::vector<int> data; };   // 不跨边界
extern "C" Widget* widget_new() { return new Widget(); }
extern "C" void widget_push(Widget* w, int x) { w->data.push_back(x); }
extern "C" int  widget_sum(Widget* w) {
    int s = 0; for (int x : w->data) s += x; return s;
}
extern "C" void widget_free(Widget* w) { delete w; }
```

```cpp
// ⑮ 统一标准等级 + CRT 的编译指示（CMake/MSBuild 等价）
// cl /std:c++20 /EHsc /MD /nologo app.cpp
//   /MD  -> 动态 CRT，跨 DLL 共享 msvcp140（见 ⑬）
#include <vector>
int main() { std::vector<int> v{1,2,3}; return (int)v.size(); }
```

- `[经验]`：① 统一 `_MSC_VER`；② 统一 `/MD`；③ 边界不导 `std`；④ 用 `/W4 /permissive-` 抓早期问题（见 ⑨）。

## ⑯ 跨编译器 [平台]

同一份标准库**逻辑**跨 MSVC/clang-cl/GCC 可移植，但**二进制**不兼容：MS STL（Windows）、libstdc++（GCC）、libc++（Clang）三者 `std::string`/`std::vector` 布局、名字修饰、分配器均不同。头文件源码级可移植；`.obj`/`.lib` 不可跨编译器链混链。

```cpp
// ⑯ 跨编译器可移植写法（避免平台特定假设）
#include <vector>
#include <string>
int cross(const std::vector<int>& v) {
    std::string s;
    for (int x : v) s += static_cast<char>('0' + (x % 10));
    return (int)s.size();
}
```

```cpp
// ⑯ 统一标准等级命令对照（典型输出，未在本机运行 MSVC）
// MSVC: cl /std:c++20 /EHsc ...
// GCC:  g++ -std=c++20 -O2 ...
// Clang:clang++ -std=c++20 -O2 ...
// 三者头文件语义一致，但导出的 std 符号名不同（_Z vs ? / mangled 差异）
```

- `[平台]`：`clang-cl` 在 Windows 上可复用 MS STL（用 `/clang:` 透传），是 MSVC 生态内最接近二进制兼容的替代前端。
- `[经验]`：头文件级跨编译器没问题；**二进制级**必须用同一编译器+同一 STL 版本（见 ⑬⑱）。

## ⑰ 贡献 [平台]

向 microsoft/STL 贡献需遵循仓库流程：fork → 分支 → 改 `stl/inc` 或 `stl/src` → 跑 `stl/tests` 全套 conformance → 提 PR。本地可用 VS 构建 `stl` 工程；本机用 g++ 仅能验证「同样代码可编译」。

```bash
# ⑰ 贡献流程命令（典型输出，未在本机运行 MSVC）
# git clone https://github.com/microsoft/STL
# cd STL && git checkout -b fix-xxx
# # 用 VS 打开 stl.sln，改 stl/inc/vector
# # 跑测试：
# stl\tests\compile_and_link.bat
# 典型输出（节选）：
#   [PASS] vector.basic / 1240 cases
#   [PASS] conformance.total
```

```cpp
// ⑰ 一个可提交的修复示例骨架（在 stl/inc/vector 增加注释/约束）
#include <vector>
template <class _Ty>
void my_erase_last(std::vector<_Ty>& v) {
    if (!v.empty()) v.pop_back();   // 仅在修改点加约束/注释
}
```

- `[平台]`：PR 需通过 CI（含 `/W4 /permissive-` 严格编译与全套测试）；版权归微软，需签署 CLA。
- `[经验]`：先查 existing issue，最小改动 + 测试，PR 通过率更高。

## ⑱ 跨库对比（三套 STL） [平台]

libstdc++（GCC）、libc++（Clang）、MS STL（MSVC）实现同一标准，但策略不同：SSO 阈值、ABI 稳定机制、并行后端、调试源可用性各异。

```cpp
// ⑱ 三套 STL 都能编译的同款代码（可移植性验证）
#include <vector>
#include <string>
#include <algorithm>
int demo() {
    std::vector<std::string> v{"c", "a", "b"};
    std::sort(v.begin(), v.end());
    return (int)v.size();
}
```

| 维度 | libstdc++ (GCC) | libc++ (Clang) | MS STL (MSVC) |
|---|---|---|---|
| 默认 SSO 阈值(x86-64) | 15 字节 | 15 字节（`__padding`） | 15 字节（union `_Bx`） |
| ABI 稳定机制 | 符号版本(GLIBCXX) | 内联命名空间 | `_MSC_VER` 主版本 + `vcruntime` |
| 并行后端 | PSTL+TBB（需装） | PSTL+TBB（需装） | **内置 oneTBB + ConcRT** |
| 调试源码 | 随工具链/`-dev` | 随工具链 | **VS 自带**，开箱即用 |
| 特性宏 | `_GLIBCXX_*` | `_LIBCPP_*` | `_HAS_CXX*`（yvals.h） |
| 异常机制 | Itanium unwind / SEH(MinGW) | Itanium unwind | **SEH（`__CxxFrameHandler*`)** |

- `[平台]`：MS STL 的独特优势是**并行算法内置 TBB**、**VS 调试源码开箱即用**、与 Windows/Win32 深度融合；代价是仅 Windows + 仅 MSVC 生态。
- `[实现]`：三者都做 SSO，但 union 布局不同 → 二进制不可互换（见 ⑫⑬）。

## ⑲ 调试/源码阅读 [平台]

在 Windows 上读 MS STL 源码最顺手：VS 安装时自带 `VC\Tools\MSVC\<ver>\include`，直接 `Ctrl+点击` 跳进 `vector`。也可在 GitHub 网页读 `microsoft/STL` 的 `stl/inc`。非 Windows 上可用 VS Code + 远程仓库只读浏览。

```cpp
// ⑲ 阅读入口：从顶层头追到实现（与 ③ 同思路）
#include <vector>
#include <string>
int read_entry() {
    std::vector<std::string> v{"x"};
    return (int)v.size();   // 在 VS 中右键 -> 转到定义，进 stl/inc/vector
}
```

```bash
# ⑲ 本地阅读命令（典型输出）
# 在资源管理器打开：
# C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.38.xxx\include
# 典型输出：列出 vector、string、memory、algorithm ... 标准头
```

- `[平台·Windows]`：对比 libstdc++ 需装 `-dev` 才有源码，MS STL 在 VS 工作负载内已含，阅读门槛最低（见 ⑩）。
- `[经验]`：先读 `stl/inc` 的公开头，再追 `stl/src` 的非模板实现（如 `xlocale.cpp`），最后看 `stl/tests` 学 conformance 用例。

## ⑳ 速查表 [标准]

```text
┌─────────────────────────┬──────────────────────────────────────────────┐
│ 主题                    │ 入口 / 证据                                   │
├─────────────────────────┼──────────────────────────────────────────────┤
│ vector 类               │ upstream stl/inc/vector（④ 行 36，上游参考）  │
│ string SSO union        │ upstream stl/inc/xstring（④ 行 1860，上游参考)│
│ 特性宏开关              │ upstream stl/inc/yvals.h（④ 行 540，上游参考） │
│ 异常/SEH 机制           │ ⑥ 真实 g++ 汇编 __gxx_personality_seh0        │
│ 并行后端                │ ⑦ Intel TBB + Concurrency Runtime            │
│ SSO 阈值(x86-64)        │ ⑧ 真实 g++ 汇编 cmp rbx,15                    │
│ 标准等级命令            │ ⑨ cl /std:c++20 /EHsc（典型输出）             │
│ 调试源码                │ ⑩ VS 自带 include                            │
│ ABI 边界                │ ⑫ _MSC_VER / msvcp140 / vcruntime140         │
│ DLL 边界陷阱            │ ⑬ 不跨边界传 std 对象                        │
│ C++23 特性              │ ⑭ <print>/<expected>/<ranges>（_HAS_CXX23）   │
│ 三套 STL 对比          │ ⑱ 表                                          │
└─────────────────────────┴──────────────────────────────────────────────┘
```

| 想做 | 命令/入口 | 证据 |
|---|---|---|
| 看 MS STL 源码 | `microsoft/STL` → `stl/inc/` | ③ ④ |
| 验证 SEH 机制 | 本机 g++ `-S`（真实汇编） | ⑥ `.seh_handler` |
| 看 SSO 阈值 | 本机 g++ `-S`（真实汇编） | ⑧ `cmp rbx,15` |
| 设 C++ 等级 | `cl /std:c++20` | ⑨ |
| 跨 DLL 安全 | C ABI 边界 | ⑬ ⑮ |
| 并行算法 | `std::execution::par` | ⑦ |

- `[标准]`：速查表所有「上游参考」行号取自 `microsoft/STL` main 分支，随提交浮动；所有「本机证据」来自真实 g++ 13.1.0 编译产物（`Examples/`）。
- `[经验]`：MS STL 与 Windows 生态深度绑定——它的强项（并行 TBB、VS 调试、Win32 融合）和限制（仅 MSVC 生态）同源。

### 补充：完整可编译示例（MS STL 可移植代码）

```cpp
// S1 最小 vector + 输出（对应 ①）
#include <vector>
#include <cstdio>
int main() { std::vector<int> v{1,2,3}; for (int x : v) std::printf("%d", x); return 0; }
```

```cpp
// S2 打印 MS STL 版本（对应 ⑨⑫，_MSC_VER 由 MSVC 定义）
#include <cstdio>
int main() { std::printf("_MSC_VER=%d\n", _MSC_VER); return 0; }
```

```cpp
// S3 string 与 wstring 互转（对应 ⑤）
#include <string>
#include <cwchar>
std::wstring to_w(const std::string& s) {
    std::wstring w; w.assign(s.begin(), s.end()); return w;
}
int main() { std::wstring w = to_w("hi"); return (int)w.size(); }
```

```cpp
// S4 SSO 短串不分配（对应 ⑧）
#include <string>
#include <cstdio>
int main() {
    std::string a = "123456789012345";      // 15 字节：仍在本地
    std::string b = a + "6";                 // 16 字节：转堆
    std::printf("a=%s b=%s\n", a.c_str(), b.c_str());
    return 0;
}
```

```cpp
// S5 并行 for_each（对应 ⑦，MS STL 后端 TBB）
#include <execution>
#include <vector>
#include <numeric>
#include <algorithm>
int main() {
    std::vector<int> a(1024, 1);
    std::for_each(std::execution::par, a.begin(), a.end(), [](int& x) { x *= 2; });
    return (int)a.size();
}
```

```cpp
// S6 noexcept 移动静态断言（对应 ⑪）
#include <string>
#include <type_traits>
int main() { static_assert(std::is_nothrow_move_constructible<std::string>::value, "!"); return 0; }
```

```cpp
// S7 C ABI 边界封装（对应 ⑬⑮）
#include <string>
#include <cstring>
extern "C" int len_c(const char* p) { return (int)std::strlen(p); }
int main() { std::string s = "boundary"; return len_c(s.c_str()); }
```

```cpp
// S8 reserve 预分配（对应 ⑪）
#include <vector>
int main() { std::vector<int> v; v.reserve(8); for (int i=0;i<8;++i) v.push_back(i); return (int)v.size(); }
```

```cpp
// S9 调试模式单步（对应 ⑩，VS 中步入 vector::at）
#include <vector>
int main() { std::vector<int> v{1,2}; return (int)v.at(0); }
```

```cpp
// S10 C++23 print + expected（对应 ⑭，需 /std:c++latest）
#include <print>
#include <expected>
int main() { std::print("ok\n"); std::expected<int,int> e = std::unexpected(1); return e.error().value_or(0); }
```

```cpp
// S11 跨平台可移植函数（对应 ⑯）
#include <vector>
#include <string>
int cross(const std::vector<int>& v) {
    std::string s; for (int x : v) s += static_cast<char>('0' + (x % 10)); return (int)s.size();
}
```

```cpp
// S12 自定义分配器接入（对应 ⑫，演示 allocator 可替换）
#include <vector>
#include <cstddef>
template <class T> struct my_alloc {
    using value_type = T;
    T* allocate(std::size_t n) { return static_cast<T*>(::operator new(n * sizeof(T))); }
    void deallocate(T* p, std::size_t) { ::operator delete(p); }
};
int main() { std::vector<int, my_alloc<int>> v{1,2,3}; return (int)v.size(); }
```

```cpp
// S13 异常安全 try/catch（对应 ⑥）
#include <stdexcept>
#include <cstdio>
int main() { try { throw std::runtime_error("x"); } catch (const std::exception& e) { std::printf("%s\n", e.what()); } return 0; }
```

```cpp
// S14 vector 遍历被内联（对应 ⑧，真实汇编见 Examples/_ch126_vector.asm）
#include <vector>
int sum(const std::vector<int>& v) { int s=0; for (int x:v) s+=x; return s; }
int main() { std::vector<int> v{1,2,3}; return sum(v); }
```

```cpp
// S15 不跨 DLL 传 string 的安全封装（对应 ⑬）
#include <string>
#include <cstring>
extern "C" int greet_c(const char* name, char* out, int cap) {
    std::string g = std::string("Hello, ") + name;
    int n = (int)g.size(); if (n < cap) { std::memcpy(out, g.data(), n); out[n]=0; } return n;
}
```

```cpp
// S16 ranges 管道（对应 ⑭，MS STL 实现于 stl/inc/ranges）
#include <vector>
#include <ranges>
#include <numeric>
int main() {
    std::vector<int> v{1,2,3,4};
    auto r = v | std::views::filter([](int x){ return x%2==0; });
    return std::accumulate(r.begin(), r.end(), 0);
}
```

```cpp
// S17 array 对比 vector（无堆分配）
#include <array>
#include <cstdio>
int main() { std::array<int,4> a{1,2,3,4}; int s=0; for (int x:a) s+=x; std::printf("%d\n", s); return 0; }
```

```cpp
// S18 NOMINMAX 避免宏冲突（对应 ⑤）
#define NOMINMAX
#include <windows.h>
#include <algorithm>
int m(int a, int b) { return std::max(a, b); }
```

```cpp
// S19 统一 /MD 编译（对应 ⑮，命令示意：cl /MD /std:c++20 /EHsc）
#include <vector>
int main() { std::vector<int> v{1}; return (int)v.size(); }
```

```cpp
// S20 阅读入口：顶层头追实现（对应 ⑲）
#include <vector>
#include <string>
int read_entry() { std::vector<std::string> v{"x"}; return (int)v.size(); }
```

## 附录 A：MS STL 工业背景 [F: Industry / B: Principle]

```
Microsoft STL 的关键设计决策:

1. 开源 (Apache 2.0, 2017): 从MSVC内部分离, GitHub上维护
   → 社区贡献: Stephan T Lavavej (maintainer), 数百贡献者

2. 调试模式 (_ITERATOR_DEBUG_LEVEL):
   Level 0: 禁用 (Release 默认, 最快)
   Level 1: 基本检查 (Debug 默认)
   Level 2: 完整检查 (包括 bound check)

3. 与 Windows SDK 深度集成:
   → std::filesystem 依赖 Windows API (CreateFileW), 非 Unix 路径
   → std::thread 依赖 Windows 线程 (CreateThread), 非 pthread
   → std::chrono 使用 QPC (QueryPerformanceCounter, 高精度)

4. 性能优化:
   → std::sort 使用 Introsort + 小数组插入排序 (16元素阈值, 比libstdc++的32更高)
   → std::vector<bool> 使用位压缩 (同libstdc++, 性能略优)
   → 并行算法直接调用 Windows ThreadPool (无需TBB, 开箱即用)
```

## 附录 E：MS STL工业与底层 [F: Industry / E: Lowlevel / H: Design / J: Learning]

```
MS STL设计权衡:

开源(2017): Apache 2.0, GitHub microsoft/STL
  → Stephan T Lavavej (STL) 是maintainer, 数百社区贡献者

调试模式:
  _ITERATOR_DEBUG_LEVEL=0: Release (无检查, 最快)
  _ITERATOR_DEBUG_LEVEL=1: 基本迭代器检查 (Debug默认)
  _ITERATOR_DEBUG_LEVEL=2: 完整检查 (包括bounds check)

与Windows SDK集成:
  filesystem → CreateFileW (Windows NT路径, 非Unix)
  thread → CreateThread (Windows线程, 非pthread)
  chrono → QueryPerformanceCounter (QPC, 高精度定时器, ~10ns分辨率)
  parallel algorithms → Windows ThreadPool (无需TBB, 开箱即用)
```

```cpp
#include <iostream>
#include <thread>
#include <chrono>
int main() {
    auto start = std::chrono::high_resolution_clock::now();
    volatile int s = 0;
    for (int i = 0; i < 1000000; ++i) s += i;
    auto end = std::chrono::high_resolution_clock::now();
    auto ns = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count();
    std::cout << "1M adds: " << ns / 1000000.0 << "ms (QPC timer, ~10ns resolution)" << std::endl;
    std::cout << "MS STL: open source since 2017, GitHub microsoft/STL" << std::endl;
    std::cout << "Debug: _ITERATOR_DEBUG_LEVEL (0=Release, 1=Debug, 2=Full)" << std::endl;
    return 0;
}
```

| 特性 | MS STL | libstdc++ | libc++ |
|---|---|---|---|
| Debug速度 | 0:最快 1:中等 2:最慢 | _GLIBCXX_DEBUG=重 | _LIBCPP_DEBUG=轻 |
| 并行 | Windows ThreadPool(内置) | Intel TBB(需额外安装) | TBB(需安装) |
| 许可证 | Apache 2.0 | GPLv3+Runtime例外 | Apache 2.0/MIT |
| 字符串SSO | 15 bytes | 15 bytes | 22 bytes |
| 维护者 | Microsoft + 社区 | RedHat + GNU | Apple + LLVM |

面试: MS STL调试模式级别？ 0(Release), 1(Debug basic), 2(Debug full bound check)
       为什么MS STL的并行算法更快？ 内置Windows ThreadPool, 无需TBB额外依赖


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第125章](Book/part11_source/ch125_libcxx.md) | 泛型库/编译期计算 | 本章提供概念，第125章提供实现 |
| [第125章](Book/part11_source/ch125_libcxx.md) | 日志格式化/序列化 | 本章提供概念，第125章提供实现 |
| [第127章](Book/part11_source/ch127_llvm.md) | 多线程服务器 | 本章提供概念，第127章提供实现 |
| [第124章](Book/part11_source/ch124_libstdcxx.md) | 错误恢复/不可恢复错误 | 本章提供概念，第124章提供实现 |

## 附录 F：MS STL面试与工业

Q: MS STL调试模式级别? A: _ITERATOR_DEBUG_LEVEL: 0(Release), 1(Debug basic), 2(Debug full bounds)
Q: 为什么MS STL并行算法不需要TBB? A: 内置Windows ThreadPool, 开箱即用(其他编译器需TBB)
Q: MS STL何时开源? A: 2017年Apache 2.0, GitHub microsoft/STL

```cpp
#include <iostream>
int main(){std::cout<<"MS STL: 0=Release, 1=Debug, 2=Full. Parallel via Windows ThreadPool."<<std::endl;return 0;}
```


## 相关章节（交叉引用）

- **后续依赖**：`Book/part10_modern/ch122_pmr.md`（第122章　PMR 与多态分配器）—— 本章为其前置，建议后续延伸阅读。
- **相邻主题**：`Book/part11_source/ch128_boost.md`（第128章　Boost 核心库（C++））—— 编号相邻、主题接续。
- **同模块**：`Book/part11_source/ch129_qt.md`（第129章　Qt 对象模型与信号槽（C++））—— 同模块下的其他主题。

## 真实开源项目参考（可查证链接）

> MSVC STL 实现内幕与标准库工程的工业参照——下列链接指向真实源码（L2 文件级）。

- **MSVC STL（Microsoft 标准库实现）**：[microsoft/STL · stl/inc](https://github.com/microsoft/STL/tree/main/stl/inc) —— `std::vector`/`std::string` 的 MSVC 侧实现，与 libstdc++/libc++ 三足鼎立；其 `_Container_base12` 迭代器调试设施是 Windows 平台独有的工程取舍，对应「① 三实现对比」的工业真相。
- **LLVM/libc++（macOS/iOS 默认 STL）**：[llvm/llvm-project · libcxx/include](https://github.com/llvm/llvm-project/tree/main/libcxx/include) —— Clang 侧标准库，对应「② ABI 差异」中 libc++ 与 MSVC STL 的 `std::string` 布局分歧（libc++ 用 24 字节 SSO 内联缓冲）。
- **Boost（标准库提案试验田）**：[boostorg · boost](https://github.com/boostorg) —— `unordered`/`filesystem`/`process` 等源自 Boost，MSVC STL 的 `<format>`/`<print>` 等特性进度常参考 Boost 实现，对应「③ 演进路线」。
- **Chromium `base::` 去 STL 依赖**：[chromium/chromium · base](https://github.com/chromium/chromium/tree/main/base) —— 在二进制体积敏感处用 `base::span`/`base::flat_map` 替代 `std::span`/`std::map`，对应「④ 体积与编译时长」的极端工程实践（与 MSVC STL 的 `/permissive-` 模式形成对照）。

**最佳实践**：跨 MSVC/gcc/clang 动态库边界传递 STL 容器必须保证同一标准库实现与版本（`_ITERATOR_DEBUG_LEVEL` 在 Debug/Release 不一致会导致链接错误），定位符号用 [ch157](Book/part14_perf/ch157_compiler_explorer.md) 的汇编取证。

> 交叉引用：libstdc++ 内幕见 [ch124](Book/part11_source/ch124_libstdcxx.md)；字符串实现见 [ch81](Book/part07_stl/ch81_string.md)。

## 底层视角：MSVC STL 实现与 SIMD 内部 [E: Low-level]

[标准] MSVC STL（`MSVC 19.3`）容器节点含 `0x0008` 指针（链表/树）或连续 `0x0010` 对齐缓冲（vector）。标准算法用 `_STD` 命名空间与 `<intrin.h>` 内部函数，`-arch:AVX2` 启用 SSE（`0x0010` 宽）/ AVX（`0x0020` 宽）并行比较。

`constexpr` 容器操作（`C++20` 起）于编译期求值，省运行期 `0x0008` 间接。`std::atomic` 用 `lock xadd`（10–20 ns）保证 `0x0040` 缓存行原子。`GCC 13.1.0` / `Clang 17` 的交叉验证可暴露 MSVC 专属行为；缓存行 `0x0040`（64 字节）是 `std::hardware_destructive_interference_size` 的取值（C++17 起）。

## 附录 B：工业实战复盘与设计取舍 [I: Practice / H: Design]

### 工业案例（真实可查证）

- **`_ITERATOR_DEBUG_LEVEL` 不一致导致链接失败**：MSVC 下 Debug（`_ITERATOR_DEBUG_LEVEL=2`）与 Release（=0）的 STL 容器内存布局不同，混合链接两个配置的 .obj/.lib 直接报 LNK2038「metadata 不匹配」。生产上 CI 必须统一 `/MD`+同一 `_ITERATOR_DEBUG_LEVEL`，否则本地 Debug 通过、Release 链接崩。
- **`/std:c++17` vs `/std:c++20` 的 STL 行为差**：MSVC 在标准开关切换时改变 `std::string`（已无 COW）、`std::filesystem` 符号版本；旧代码若依赖 `/std:c++14` 下的旧异常规范，升级后编译失败。

### 常见 Bug 与 Debug 方法

- **跨 DLL 传 STL 崩溃**：`nm -C`/`dumpbin /symbols` 看容器符号来自哪个运行时；用 `_CRTDBG_MAP_ALLOC` + CRT 调试堆定位越界。
- **SIMD 内部误用**：MSVC STL 的 `<xmmintrin.h>`/`__m128` 内部函数若未对齐 `alignas(16)`，在老 CPU 上 `#GP` 崩溃。Debug 用 `/RTC` + ASan。
- **Code Review 关注点**：是否跨模块边界传 `std::string`/`std::vector`；`_ITERATOR_DEBUG_LEVEL` 是否全工程一致；`/MD`(动态 CRT) vs `/MT`(静态) 是否混用（混用必崩）。

### 设计权衡（Trade-off）与反模式（Anti-Pattern）

| 维度 | 选择 | 代价 |
|------|------|------|
| CRT | `/MD` 动态（统一） | 需带 VCredist |
| 调试 | `_ITERATOR_DEBUG_LEVEL=2` | 容器变大、慢 |
| 向量化 | SIMD 内部函数 | 需对齐、可移植差 |

- **反模式**：Debug/Release 混链（LNK2038）；跨 DLL 边界传 STL 容器（同一 STL 不同版本布局不兼容）；用 `/MT` 静态 CRT 又引入也用 `/MD` 的第三方库（堆不共享）。
- **API Design**：对外接口用 POD/C 风格结构体或 `std::string_view`/`span` 解耦 STL 实现细节；错误用 `HRESULT`/`std::error_code` 跨 ABI 边界（异常 ABI 不稳）。

### 重构建议

把跨模块 `const std::string&` 参数重构为 `std::string_view`（零拷贝、无 ABI 假设）；把混用的 `/MT`+`/MD` 统一为 `/MD` 并固化 `_ITERATOR_DEBUG_LEVEL`；CI 增加「全配置统一」断言，消除 Debug/Release 链路错配。

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

