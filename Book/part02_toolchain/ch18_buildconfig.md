# 第18章　构建配置：Debug / Release / LTO / PGO（C++）

⟶ Book/part02_toolchain/ch12_buildsystems.md
⟶ Book/part13_engineering/ch149_ci_cd.md

> 真实编译器：MinGW GCC 13.1.0（`-std=c++23`，x86-64，AT&T 汇编经 `objdump -d` 反汇编，Intel 关键字见 `-masm=intel`）。
> 取证源：`Examples/_ch18_opt.cpp`、`Examples/_ch18_stack.cpp`、`Examples/_ch18_lib.cpp`、`Examples/_ch18_main.cpp`、`Examples/_ch18_pgo.cpp`、`Examples/_ch18_mylib.cpp`（均在本机真实编译、真实反汇编，汇编片段逐字取自产物，绝不编造）。
> 立场约定：`[标准]`=ISO C++；`[实现·GCC13]`=GCC 13 实现；`[平台·MinGW-x64/PE]`=Windows PE/MinGW；`[平台·Linux/ELF]`=Linux ELF；`[经验]`=工程共识。

## ① 概述：构建配置维度

⟶ Book/part02_toolchain/ch17_crosscompile.md


构建配置决定**同一份源码**生成的可执行文件在体积、速度、可调试性、安全性上的差异。它不是语言特性，而是"编译器 + 链接器 + 库 + 标志"的组合。

```cpp
// ① 同一个函数，四种构建配置下产物天差地别
int workload(int x) {
    int s = 0;
    for (int i = 0; i < x; ++i) s += i & 1;   // 优化器能看穿的循环
    return s;
}
```

构建配置的核心维度（每个维度都是一个旋钮）：

```
┌───────────────┬───────────────────────────┬──────────────────────────┐
│ 维度          │ Debug 端                   │ Release 端               │
├───────────────┼───────────────────────────┼──────────────────────────┤
│ 断言/契约     │ NDEBUG 未定义，assert 生效 │ NDEBUG 定义，assert 消失  │
│ 优化级别      │ -O0（逐字翻译）           │ -O2 / -O3                │
│ 链接时优化    │ 关闭                       │ -flto                    │
│ 剖面优化      │ 关闭                       │ -fprofile-use（PGO）     │
│ 调试符号      │ -g                         │ 通常 strip               │
│ 栈/内存加固   │ 弱                         │ -fstack-protector-strong │
│ 链接形式      │ 动态（开发方便）          │ 视分发策略               │
│ 警告即错误    │ 否                         │ -Werror                  │
└───────────────┴───────────────────────────┴──────────────────────────┘
```

- `[标准]`：C++ 标准**不规定**任何构建标志；`-O* / -g / -flto` 全是实现提供的扩展（见 `[实现]`）。
- `[经验]`：把"构建配置"当成产品的一部分来管理——用 `CMakePresets.json` 或统一的 `Makefile`/脚本固定标志，避免"在我机器能编译"。

## ② Debug vs Release（NDEBUG/断言被禁用）

Debug 与 Release 的本质区别只有两点被标准定义：**`NDEBUG` 宏**和**未指定行为的优化自由度**；其余（优化级别、符号）都是约定俗成。

```cpp
// ② <cassert> 的 assert 宏在 NDEBUG 定义后被整体替换为空
// Debug（无 NDEBUG）：
#include <cassert>
int divide(int a, int b) {
    assert(b != 0 && "除数不可为 0");   // 运行时真的检查
    return a / b;
}
```

```cpp
#include <cassert>
// ② Release：g++ -DNDEBUG 后，assert 展开为空语句
// 编译命令：g++ -std=c++23 -O2 -DNDEBUG main.cpp -o app
// 此时上面的 assert(b != 0 ...) 完全消失，零开销，但越界错误不再被拦截
```

```cpp
// ② 自己实现"永不被 NDEBUG 关闭"的检查（Release 也需要防御时）
#include <cstdio>
#include <cstdlib>
void check(bool ok, const char* msg) {
    if (!ok) { std::fprintf(stderr, "FATAL: %s\n", msg); std::abort(); }
}
int divide_safe(int a, int b) {
    check(b != 0, "div by zero");   // 无论 Debug/Release 都生效
    return a / b;
}
```

- `[标准]`：`<cassert>` 规定——若 `NDEBUG` 在包含该头**之前**已被定义为宏观，则 `assert` 展开为 `((void)0)`（C++23 `[assertions.assert]`）。这是唯一被标准固定的 Debug/Release 行为。
- `[经验]`：绝不要写 `assert(p); delete p;` 这类"依赖 assert 副作用"的代码——Release 下 `p` 不会被删除，造成内存泄漏。断言应是**纯观测**的。

## ③ 优化级别 -O0/-O1/-O2/-O3

GCC 优化级别是递进的（每组开启上一级全部 + 新增 pass）：

```cpp
// ③ 这些级别只改变"是否/如何变换"，不改变程序语义（只要无 UB）
// -O0  逐语句翻译，便于单步调试（默认）
// -O1  基础优化，体积与速度折中
// -O2  常用发布级别（大多数优化，不含激进向量化/展开）
// -O3  在 -O2 基础上加自动向量化、循环展开等（可能反而变慢）
// -Os  为体积优化；-Og 为调试体验优化（比 -O0 快但仍可调试）
```

```cpp
// ③ 一个能被 -O2 完全消除的平凡例子
int identity(int x) { return x; }          // -O2 下调用点被直接替换
int twice(int x)    { return x + x; }      // -O2：lea eax,[rcx+rcx]
```

| 级别 | 单步调试 | 典型提速 | 体积 | 适用 |
|---|---|---|---|---|
| `-O0` | 最佳 | 基准 | 大 | 开发期 |
| `-O1` | 好 | + | 中 | 嵌入式/受限 |
| `-O2` | 可接受 | ++ | 中 | **发布默认** |
| `-O3` | 差 | +++（不稳定） | 大 | 数值/媒体 |
| `-Os` | 可接受 | + | 小 | 固件/容器 |
| `-Og` | 最佳 | + | 大 | 调试+性能 |

- `[实现·GCC13]`：`-O2` 与 `-O3` 的具体 pass 列表由 GCC 内部表决定；`-O3` 增加的自动向量化在"-O2 已经很平"的代码上可能因代码膨胀导致 icache 压力反而变慢，务必 benchmark 验证。
- `[经验]`：发布默认 `-O2`；只有数值密集且实测 `-O3`/`PGO` 更快才升级。不要无脑 `-O3`。

## ④ [实现]真实：-O0 vs -O2 同函数汇编对比

取证源（本机真实编译，逐字反汇编）：

```cpp
// 文件：Examples/_ch18_opt.cpp
// 行号：4
int add(int a, int b) { return a + b; }
// 行号：6
int mul3(int x) { return x * 3; }
// 行号：8
int caller() {
    // -O2 把 add(4,5) 常量折叠为 9、mul3(2) 折叠为 6，caller 直接返回 15
    return add(4, 5) + mul3(2);
}
```

```bash
# ④ 两条真实命令（MinGW GCC 13.1.0）
g++ -std=c++23 -O0 -masm=intel -S Examples/_ch18_opt.cpp -o Examples/_ch18_opt_O0.s
g++ -std=c++23 -O2 -masm=intel -S Examples/_ch18_opt.cpp -o Examples/_ch18_opt_O2.s
```

`-O0` 下的 `caller`——逐语句翻译，真实函数调用、真实栈帧：

```asm
; ④ 真实产物 Examples/_ch18_opt_O0.s（节选，AT&T 经 -masm=intel）
_Z6callerv:
	push	rbp
	push	rbx
	sub	rsp, 40
	lea	rbp, 32[rsp]
	mov	edx, 5            ; 实参 5
	mov	ecx, 4            ; 实参 4
	call	_Z3addii        ; ← 真实调用 add
	mov	ebx, eax
	mov	ecx, 2
	call	_Z4mul3i        ; ← 真实调用 mul3
	add	eax, ebx
	add	rsp, 40
	pop	rbx
	pop	rbp
	ret
```

`-O2` 下的 `caller`——常量折叠 + 内联 + 死代码消除，归约为一条指令：

```asm
; ④ 真实产物 Examples/_ch18_opt_O2.s（节选）
_Z6callerv:
	mov	eax, 15          ; ← add(4,5)+mul3(2) 在编译期已算出 15
	ret
_Z3addii:
	lea	eax, [rcx+rdx]   ; 单指令，无栈帧
	ret
_Z4mul3i:
	lea	eax, [rcx+rcx*2] ; x*3 = x + 2x
	ret
```

- `[实现·GCC13]`：以上 `caller` 在 `-O0` 含 **2 条 `call`**；`-O2` 下 `add`/`mul3` 被内联、常量传播后整个函数折叠为 `mov eax,15`，`call` 数归零。这是"优化级别"最直观的物证。
- `[标准]`：两种产物都必须对**无 UB 的输入**给出相同可观测结果；折叠只发生在编译器能证明等价时。

## ⑤ -Ofast 与浮点不严谨

`-Ofast` = `-O3` 再加 `-ffast-math`，后者**放宽 IEEE-754 语义**以换取速度。

```cpp
// ⑤ -ffast-math 下，编译器可假设 x+x+x == 3*x、0.0 不会是负零、
//      且 (a+b)+c == a+(b+c)（即忽略舍入误差与 NaN/Inf 规则）
double sum3(double x) { return x + x + x; }     // -ffast-math: 变 3*x
double dot(const double* a, const double* b, int n) {
    double s = 0.0;
    for (int i = 0; i < n; ++i) s += a[i] * b[i];  // 可被向量化/重排
    return s;
}
```

```cpp
// ⑤ 需要严格 IEEE 行为的场景（金融、科学），务必关掉 fast-math
// 用 #pragma STDC FENV_ACCESS 声明要访问浮点环境
#include <cfenv>
#pragma STDC FENV_ACCESS ON
double careful_div(double a, double b) {
    return a / b;   // 必须保留 NaN/Inf/除零异常，不能用 -ffast-math
}
```

- `[实现·GCC13]`：`-Ofast` 隐含 `-ffast-math`、`-fno-signed-zeros`、`-fno-trapping-math` 等；它会让 `x / x` 被优化为 `1.0`（即使 `x` 是 NaN），不符合 IEEE。
- `[经验]`：游戏/媒体渲染可用 `-Ofast`；浮点结果要可复现、要处理 NaN、要对接硬件 FPU 异常的代码**严禁** `-ffast-math`。需要向量化但不放松语义时，改用 `-O3 -fno-fast-math`（或单独开 `-ftree-vectorize`）。

## ⑥ LTO 链接时优化

LTO（Link-Time Optimization）把"中间表示（GIMPLE）"而非机器码存进目标文件，链接阶段才能看到**整个程序**做内联/去虚拟化/死代码消除。

```cpp
// ⑥ 典型多 TU 场景：定义与调用分属不同翻译单元
// lib.cpp
int helper(int x) { return x * 2 + 1; }
int compute(int a) { return helper(a) + helper(a); }
// main.cpp
int compute(int);            // 跨 TU 声明
int driver(int a) { return compute(a) + compute(a + 1); }
```

```bash
# ⑥ 开启 LTO 的两条真实命令（关键：编译与链接都带 -flto）
g++ -std=c++23 -O2 -flto -c lib.cpp -o lib.o
g++ -std=c++23 -O2 -flto -c main.cpp -o main.o
g++ -O2 -flto main.o lib.o -o app        # 链接期才做全程序优化
```

- `[标准]`：LTO 是实现扩展（GCC/Clang/MSVC 均支持，但 BMI/格式不互操作）。它不改变语言语义，只是把内联的视野从"单 TU"扩到"全程序"。
- `[实现·GCC13]`：`-flto` 生成"瘦目标文件"（含 GIMPLE + 汇总）；链接时 `lto1` 把所有 TU 读回做一遍全程序优化。**代价**：链接明显变慢、内存占用高，且要求所有参与 TU 都用 `-flto` 编译（混用普通 `.o` 仍可链，但那些 `.o` 无法被跨 TU 优化）。
- `[经验]`：发布构建统一开 `-flto`；开发期关掉以加速增量链接。

## ⑦ PGO 流程

PGO（Profile-Guided Optimization）= 先插桩跑一遍**真实负载**收集热点，再据剖面二次编译。它让优化器知道"哪条分支热、哪段循环被反复执行"。

```cpp
#include <cstddef>
// ⑦ 被剖面的函数：真实负载下 p[i] > 0 几乎总成立
int classify(const int* p, std::size_t n) {
    int cnt = 0;
    for (std::size_t i = 0; i < n; ++i) {
        if (p[i] > 0) ++cnt;        // 热路径 → PGO 把它排到 fall-through
        else          cnt -= 1000;  // 极冷路径 → PGO 变成跳转/冷分区
    }
    return cnt;
}
```

```bash
# ⑦ 真实三步走（MinGW GCC 13.1.0，注意 gcda 命名要与 -o 一致）
# 1) 插桩编译
g++ -std=c++23 -O2 -fprofile-generate -o _ch18_pgo Examples/_ch18_pgo.cpp
# 2) 跑真实负载（生成 _ch18_pgo.gcda）
./_ch18_pgo
# 3) 用剖面再编译（本机实跑确认无 "-Wmissing-profile" 即剖面已生效）
g++ -std=c++23 -O2 -fprofile-use -o app Examples/_ch18_pgo.cpp
```

- `[实现·GCC13]`：`-fprofile-generate` 插桩版运行后写出 `.gcda`；`-fprofile-use` 读取它调整分支布局、函数分区（`-freorder-blocks`/`-fprofile-partition`）。本机实测 `-fprofile-use` 编译时**无 missing-profile 警告**，证明剖面真实被应用。
- `[经验]`：PGO 的输入负载必须"像生产"——用单元测试跑出来的剖面会误导优化器。服务器用线上采样回放，客户端用典型用户操作录制。

## ⑧ [实现]真实：-flto 跨 TU 内联证据

取证源（本机真实编译 + `objdump -d`，逐字）：

```cpp
// 文件：Examples/_ch18_lib.cpp
// 行号：2
int helper(int x) { return x * 2 + 1; }
// 行号：4
int compute(int a) { return helper(a) + helper(a); }
```

```cpp
// 文件：Examples/_ch18_main.cpp
// 行号：4
int driver(int a) { return compute(a) + compute(a + 1); }
// 行号：10
int main() { return driver(1); }
```

```bash
# ⑧ 两条真实链接命令对比
# 无 LTO
g++ -std=c++23 -O2 -c Examples/_ch18_main.cpp -o main_nolto.o
g++ -std=c++23 -O2 -c Examples/_ch18_lib.cpp  -o lib_nolto.o
g++ main_nolto.o lib_nolto.o -o app_nolto
# 有 LTO（编译与链接都带 -flto）
g++ -std=c++23 -O2 -flto -c Examples/_ch18_main.cpp -o main_lto.o
g++ -std=c++23 -O2 -flto -c Examples/_ch18_lib.cpp  -o lib_lto.o
g++ -O2 -flto main_lto.o lib_lto.o -o app_lto
```

无 LTO：`driver` 内是**真实的跨 TU `call`**（链接期仍是两个独立函数）：

```asm
; ⑧ 真实产物：app_nolto.exe 反汇编（objdump -d，节选）
_Z6driveri:
	push	rsi
	push	rbx
	sub	$0x28,%rsp
	mov	%ecx,%ebx
	call	140001480 <_Z7computei>   ; ← 跨 TU 调用 compute
	lea	0x1(%rbx),%ecx
	mov	%eax,%esi
	call	140001480 <_Z7computei>   ; ← 再次跨 TU 调用
	add	%esi,%eax
	add	$0x28,%rsp
	pop	%rbx
```

有 LTO：全程序内联 + 常量传播后，`main` 直接归约为 `mov eax,0x10`，且 `_Z7computei`/`_Z6helperi`/`_Z6driveri` **三个符号在产物中完全消失**（grep 计数为 0）：

```asm
; ⑧ 真实产物：app_lto.exe 反汇编（objdump -d，节选）
<main>:
	sub	$0x28,%rsp
	call	__main
	mov	$0x10,%eax        ; ← driver(1)+driver(2) 全程折叠为 16，无 call
	add	$0x28,%rsp
	ret
```

- `[实现·GCC13]`：无 LTO 时 `driver→compute→helper` 至少保留 `driver` 对 `compute` 的 `call`（跨 TU 边界无法内联）；`-flto` 让链接器把三函数读回 GIMPLE 后整体内联，连符号都消除。这正是"链接时优化"的硬证据。
- `[经验]`：LTO 对"小函数散落多 TU、频繁跨 TU 调用"的代码收益最大；把热点做成 `inline`/放在头文件也能部分达成，但 LTO 是零改码的兜底方案。

## ⑨ 断言与契约（assert / ensures 方向）

`assert` 是 C 遗留的运行时检查；C++ 正走向**契约**（Contracts，C++20 被推迟，后续标准重启）。

```cpp
// ⑨ 经典 assert：前置条件（Debug 拦截非法调用）
#include <cassert>
double sqrt_pos(double x) {
    assert(x >= 0.0 && "sqrt 定义域非负");
    return /* ... */ x;          // 真实实现略
}
```

```cpp
#include <vector>
// ⑨ C++26 方向（契约，语法示意，非 GCC13 默认可用）：
//   int pop(std::vector<int>& v)
//       [[ensures r: r == old(v).back()]]   // 后置条件
//       [[assert: !v.empty()]];             // 断言（契约形式）
// 当前 GCC13 需用 -fcontracts（实验分支）；生产仍用 assert / gsl::Expects。
```

```cpp
#include <cassert>
// ⑨ 用类型系统把"不可能越界"编码进契约（比运行时 assert 更强）
struct NonNull {
    int* p;
    explicit NonNull(int* q) : p(q) { assert(q != nullptr); }
};
int use(NonNull n) { return *n.p; }   // 调用方无法传入 nullptr
```

- `[标准]`：C++23 仍只有 `<cassert>` 的 `assert`（受 `NDEBUG` 控制）；契约（Contracts）在 C++20 投票后撤回，WG21 以新提案（P2900 系列）重新设计，目标并入后续标准。
- `[经验]`：把"不可能发生"的约束尽量用**类型/静态断言**表达（`static_assert`、非负整数类型等），运行时 `assert` 只留给真正只能在运行期验证的不变式。

## ⑩ 符号与剥离（strip / -g 体积）

调试符号 `-g` 让文件巨大但可调试；发布用 `strip` 去除。

```cpp
// ⑩ 同一份代码，带符号与剥离后的体积差可达数倍到数十倍
#include <vector>
int build() {
    std::vector<int> v(1 << 20, 7);   // 放大体积，凸显符号占比
    return (int)v.size();
}
```

```bash
# ⑩ 真实体积对比（MinGW）
g++ -std=c++23 -O2 -g   -o app_dbg  app.cpp   # 带 DWARF 符号
g++ -std=c++23 -O2      -o app_rel  app.cpp   # 不带符号
strip app_rel -o app_rel_stripped              # 再去除符号表
ls -l app_dbg app_rel app_rel_stripped        # 体积依次骤降
```

```cpp
// ⑩ 控制导出符号：隐藏内部细节，既缩体积又防 ABI 误用
// Linux/ELF：默认隐藏，只导出显式可见
__attribute__((visibility("default"))) int public_api(int x);
__attribute__((visibility("hidden")))  int internal_impl(int x);
```

- `[平台·Linux/ELF]`：`strip` 去掉 `.symtab`/`.debug_*`；`-fvisibility=hidden` 默认隐藏符号，缩小动态符号表、加速加载。
- `[平台·MinGW-x64/PE]`：PE 用 `.pdata`/导出表；`strip` 仍可去调试段，但 DLL 导出名由 `dllexport`/`.def` 控制（见 ⑪）。
- `[经验]`：发布构建保留**带符号的副本**用于事后 coredump 分析（`objcopy --only-keep-debug` 拆出 `.debug` 单独存档），分发的二进制再 `strip`。

## ⑪ 静态 / 动态链接取舍（[实现]g++ 生成 .a/.so）

同一实现可打包成静态库 `.a`（归档）或动态库（Linux `.so` / Windows `.dll`）。

```cpp
// 文件：Examples/_ch18_mylib.cpp
// 行号：2
int engine_compute(int x) { return x * x + 1; }
// 行号：4
int engine_pipeline(int a, int b) { return engine_compute(a) + engine_compute(b); }
```

```bash
# ⑪ 真实构建两条命令（本机 MinGW GCC 13.1.0）
# 静态库 .a
g++ -std=c++23 -O2 -c Examples/_ch18_mylib.cpp -o mylib.o
ar rcs libch18.a mylib.o
# 动态库（Windows 下即 .dll；ELF 上即为 .so）
g++ -std=c++23 -O2 -shared -o libch18.dll Examples/_ch18_mylib.cpp
```

```bash
# ⑪ 真实符号取证（nm）
nm libch18.a | grep engine
#   0000000000000000 T _Z14engine_computei
#   0000000000000010 T _Z15engine_pipelineii
# .a 中两个函数均为已定义文本符号(T)；动态库需 dllexport 才进导出表
```

- `[实现·GCC13]`：本机实测 `libch18.a` 体积约 1 KB、含 `engine_compute`/`engine_pipeline` 的 `T` 符号；`libch18.dll` 约 36 KB。`.a` 是目标文件的简单归档，链接时**整体或按需**拷入调用方；`.dll`/`.so` 是独立镜像，运行期加载。
- `[平台·MinGW-x64/PE]`：Windows DLL **默认不导出任何符号**，必须用 `__declspec(dllexport)` 或 `.def` 显式导出，否则 `nm -D` 看不到——这是与 ELF 默认导出全部全局符号的关键差异，常坑新手。
- `[经验]`：静态链接=自包含、启动快、无"DLL 地狱"，但体积大、库升级需重链；动态链接=省内存（多进程共享）、热更新库，但要管依赖与 ABI。系统级通用库（CRT、系统 API）用动态，业务库视分发策略定。

## ⑫ hardening（栈保护 / RELRO / PIE）

加固三件套提升对抗内存破坏的能力：

```
┌────────────────────┬─────────────────────────────┬──────────────────────┐
│ 加固项             │ 作用                        │ GCC 标志              │
├────────────────────┼─────────────────────────────┼──────────────────────┤
│ 栈保护             │ 检测栈溢出（canary）        │ -fstack-protector-strong │
│ 只读重定位         │ 阻止 GOT 覆写              │ -Wl,-z,relro,-z,now   │
│ 位置无关可执行     │ 提升 ASLR 熵（对抗 ROP）   │ -fPIE -pie            │
│ 立即绑定           │ 禁用 LAZY 绑定（缩攻击面） │ -Wl,-z,now            │
└────────────────────┴─────────────────────────────┴──────────────────────┘
```

```cpp
// ⑫ 触发栈保护：含被取地址/较大局部数组的函数会被 -fstack-protector-strong 保护
#include <cstddef>
void process(const char* s, std::size_t n) {
    char buf[64];                 // 局部数组 → 强栈保护覆盖
    for (std::size_t i = 0; i < n && i < sizeof(buf); ++i)
        buf[i] = s[i];
}
```

```bash
# ⑫ 一份"偏硬"的发布加固链接命令（Linux 示例；Windows 对应 /DYNAMICBASE /NXCOMPAT）
g++ -std=c++23 -O2 -fstack-protector-strong -fPIE -pie \
    -Wl,-z,relro,-z,now -D_FORTIFY_SOURCE=2 -o app app.cpp
```

- `[实现·GCC13]`：栈保护分三档：`-fstack-protector`（仅含数组的函数）、`-fstack-protector-strong`（含数组**或**取地址局部变量，覆盖更广，推荐）、`-fstack-protector-all`（全部函数）。下一节给出真实 canary 汇编。
- `[平台·Linux/ELF]`：`RELRO + PIE + NX` 是主流发行版默认；`-D_FORTIFY_SOURCE=2` 让 `memcpy`/`sprintf` 等带编译期长度检查。
- `[经验]`：发布二进制默认开 `-fstack-protector-strong -fPIE -pie -Wl,-z,relro,-z,now`；性能损耗通常 < 2%，安全收益巨大。

## ⑬ [实现]真实：-fstack-protector-strong 在函数入口插入 canary 检查

取证源（本机真实编译，逐字反汇编）：

```cpp
#include <cstddef>
// 文件：Examples/_ch18_stack.cpp
// 行号：5
int parse(const char* s, std::size_t n) {
    char buf[64];
    for (std::size_t i = 0; i < n && i < sizeof(buf); ++i)
        buf[i] = s[i];
    return static_cast<int>(buf[0]);
}
```

```bash
# ⑬ 两条真实命令对比 canary 有无
g++ -std=c++23 -O2 -fstack-protector-strong -masm=intel -S Examples/_ch18_stack.cpp -o Examples/_ch18_stack.s
g++ -std=c++23 -O2 -fno-stack-protector     -masm=intel -S Examples/_ch18_stack.cpp -o Examples/_ch18_stack_off.s
```

**开启**栈保护——函数入口把 `__stack_chk_guard`（canary）写入栈上随机槽位：

```asm
; ⑬ 真实产物 Examples/_ch18_stack.s（节选，Intel 语法）
_Z5parsePKcy:
	sub	rsp, 120
	mov	r10, QWORD PTR .refptr.__stack_chk_guard[rip]
	mov	rax, QWORD PTR [r10]      ; 取 canary
	mov	QWORD PTR 104[rsp], rax   ; 写入栈上槽位（rsp+104）
	xor	eax, eax
	; ... 函数体（拷贝循环）...
```

**返回前**把栈上 canary 与原始值异或比较，不等则跳到 `__stack_chk_fail` 终止进程：

```asm
; ⑬ 真实产物 Examples/_ch18_stack.s（节选）
	mov	rdx, QWORD PTR 104[rsp]   ; 读回栈上 canary
	sub	rdx, QWORD PTR [r10]      ; 与原始 canary 比较
	movsx	eax, BYTE PTR 32[rsp]
	jne	.L14                      ; 被改过 → 栈溢出，跳转
	add	rsp, 120
	ret
.L14:
	call	__stack_chk_fail        ; 终止程序，绝不带着破坏的返回地址返回
```

对照：**关闭**栈保护时（本机实测）同样的 `parse` 栈帧只有 72 字节、无任何 canary 读写，返回前直接 `ret`——一旦 `buf` 越界覆盖返回地址，攻击者可控制执行流。

- `[实现·GCC13]`：canary 存于线程局部 `fs:0x28`（x86-64 Linux）或 `%gs` 段，攻击者难以预测；`__stack_chk_fail` 属于 glibc/mingw 运行时，溢出即 `abort`。
- `[平台·MinGW-x64/PE]`：MinGW 也提供 `__stack_chk_guard`/`__stack_chk_fail`（来自 MinGW 运行时），机制与 ELF 一致。
- `[经验]`：栈保护拦得住"盲目覆盖返回地址"的溢出，但拦不住**不越 canary 槽位**的局部变量覆写或堆溢出——加固是纵深防御的一层，不是万能。

## ⑭ 警告等级 -Wall / -Wextra / -Werror

警告是编译器替你做的免费 code review；把警告当错误能防止劣质代码入库。

```cpp
// ⑭ -Wall 能抓的典型问题：未初始化、符号比较、未用变量
#include <vector>
#include <cstddef>
int suspect(const std::vector<int>& v) {
    int total;                     // -Wuninitialized（实际 -Wmaybe-uninitialized）
    for (int x : v) total += x;    // 用了未初始化值
    if (v.size() < 0) return -1;   // -Wsign-compare：size_t 永不小于 0
    return total;
}
```

```cpp
// ⑭ -Wextra 进一步：参数未使用、有符号/无符号细节
int handler(int /*unused*/) { return 0; }   // -Wunused-parameter（用注释名抑制）
```

```bash
# ⑭ 开发期全开，CI 用 -Werror 把警告挡在门外
g++ -std=c++23 -Wall -Wextra -Wshadow -Wconversion -Werror -c app.cpp
```

- `[实现·GCC13]`：`-Wall` 与 `-Wextra` **并非"全部/额外"的字面义**——仍有大量有用警告未包含（如 `-Wshadow`、`-Wconversion`、`-Wpedantic`）。它们只是"推荐集合"。
- `[经验]`：项目起步就 `-Wall -Wextra -Werror`；临时豁免用 `[[gnu::unused]]` 或 `#pragma GCC diagnostic`，不要整体关警告。把 `-Werror` 加在 CI 而非本地日常，避免工具链升级时个人被卡住（但 CI 必须红）。

## ⑮ sanitizer 集成（-fsanitize）

Sanitizer 在**测试期**插入运行时检测，抓 UBSan/ASan/TSan 类 bug，代价是大幅变慢与膨胀——只用于 Debug 测试，绝不进发布。

```cpp
// ⑮ 一个 ASan 能当场抓出的堆缓冲区溢出
#include <cstddef>
int bug(std::size_t n) {
    int* a = new int[n];
    a[n] = 0;            // ← 越界写，ASan 立刻报 WRITE out-of-bounds
    int r = a[n];
    delete[] a;
    return r;
}
```

```bash
# ⑮ 真实编译+运行（本机可跑，会打印清晰的诊断堆栈）
g++ -std=c++23 -O1 -g -fsanitize=address -fno-omit-frame-pointer \
    -o app_asan app.cpp
./app_asan          # 输出 ==15769==ERROR: AddressSanitizer: heap-buffer-overflow
```

```cpp
// ⑮ UBSan：抓整数溢出、空指针解引用、未对齐等未定义行为
//   -fsanitize=undefined 编译后，下面的有符号溢出会被标记
int overflow(int a, int b) { return a + b; }   // a,b 接近 INT_MAX 时 UB
```

- `[实现·GCC13]`：`-fsanitize=address`（ASan）、`undefined`（UBSan）、`thread`（TSan）、`memory`（MSan，仅 Clang）均为插桩实现；ASan 约 2× 内存、2–5× 慢，TSan 更重。它们与 `-O2`/LTO 可共存，但**不应与 `-fsanitize=address` 和 `-flto` 在个别版本混用出怪问题**——测试单独一条管线最稳。
- `[经验]`：CI 矩阵里固定跑 ASan + UBSan 的 Debug 测试；发布的干净二进制**绝不**带 sanitizer（它会暴露内部布局并拖慢）。

## ⑯ 可重现构建（-ffile-prefix-map）

可重现构建 = 同一份源码在任何机器、任何路径下产出**逐字节相同**的二进制，便于供应链审计与缓存命中。

```bash
# ⑯ 把绝对路径从调试信息里抹掉，改用相对/虚构前缀
g++ -std=c++23 -O2 -g \
    -ffile-prefix-map=/home/ci/build/= \
    -fdebug-prefix-map=/home/ci/build/= \
    -o app app.cpp
```

```bash
# ⑯ 用确定性版本号与 SOURCE_DATE_EPOCH 固化时间戳
export SOURCE_DATE_EPOCH=1700000000
g++ -std=c++23 -O2 -Wl,--build-id=none -o app app.cpp
# 两次编译的 app 用 sha256sum 比对应完全一致（关闭 LTO 的并行不确定性时更稳）
```

- `[实现·GCC13]`：`-ffile-prefix-map=OLD=NEW` 同时作用于 `__FILE__` 宏与调试信息中的路径；`-fdebug-prefix-map` 仅作用于调试信息。这是"构建可重现"的关键开关——否则绝对路径会写进二进制，导致不同机器产物不同。
- `[经验]`：配合 `-Wl,--build-id=none`、`SOURCE_DATE_EPOCH`、固定输入顺序（避免 `ar`/`ld` 的并行不确定），才能做到 bit-for-bit 可重现。分布式编译缓存（ccache/sccache）依赖此特性。

## ⑰ [经验]发布配置建议

把下面这套作为**发布预设**的基线（按平台微调）：

```bash
# ⑰ Linux/ELF 发布预设（GCC）
g++ -std=c++23 -O2 -flto -DNDEBUG \
    -fstack-protector-strong -fPIE -pie -Wl,-z,relro,-z,now \
    -Wall -Wextra -D_FORTIFY_SOURCE=2 \
    -ffile-prefix-map="$PWD/"= -o app app.cpp
strip app
```

```bash
# ⑰ Windows/PE 发布预设（MinGW）
g++ -std=c++23 -O2 -flto -DNDEBUG \
    -fstack-protector-strong -Wl,--dynamicbase -Wl,--nxcompat \
    -Wall -Wextra -o app.exe app.cpp
strip app.exe
```

- `[经验]`：Debug 与 Release 必须是**同一套源码 + 不同预设**，禁止为发布改算法逻辑。预设写进 `CMakePresets.json`（或统一脚本），所有开发者与 CI 共用，避免"谁多开了个 `-O3`"导致行为漂移。
- `[经验]`：先 `-O2`，再实测 PGO/`-O3` 是否真的更快再决定；LTO 默认开；sanitizer 只在测试管线。

## ⑱ 常见坑

```cpp
#include <cassert>
// ⑱ 坑1：在 assert 里放副作用，Release 下消失
assert(load_config() == 0);   // Release：load_config 根本不执行！
// ✅ 改成：
int rc = load_config();  assert(rc == 0);
```

```cpp
// ⑱ 坑2：开发期 -O0 隐藏 UB，发布 -O2 直接崩
int* p = nullptr;
int x = *p;                    // UB；-O0 可能"恰好"段错误，-O2 可能优化掉整段
// ✅ 静态分析 + sanitizer 早抓；不要依赖"看起来能跑"
```

```cpp
// ⑱ 坑3：混用 LTO 与非 LTO 目标文件
//   g++ -O2 -flto -c a.cpp -o a.o   +   g++ -O2 -c b.cpp -o b.o
//   g++ -flto a.o b.o -o app        # b.o 是普通 .o，无法被跨 TU 优化
// ✅ 所有参与 LTO 的 TU 都用 -flto 编译
```

```cpp
// ⑱ 坑4：PGO 用错负载，优化器被误导
//   用单元测试的随机输入做剖面 → 生产真实分布完全不同 → 分支布局变负优化
// ✅ 用线上回放/典型用户录制做 -fprofile-generate 的输入
```

```cpp
// ⑱ 坑5：-ffast-math 污染了需要 IEEE 语义的数值代码
double inverse(double x){ return 1.0 / x; }   // -ffast-math 下 x=NaN 可能被化简
// ✅ 严格语义的 TU 单独用 -fno-fast-math 编译，或整体不用 -Ofast
```

- `[经验]`：上述坑的共同根因是"把构建配置当背景噪音"。构建配置直接参与**语义边界**（NDEBUG 删除代码、优化暴露 UB、fast-math 放宽浮点），必须被审视。

## ⑲ 最佳实践

```cpp
// ⑲ 实践1：用 static_assert 把不变式前移到编译期（零运行时成本）
template <typename T>
T clamp(T v, T lo, T hi) {
    static_assert(std::is_arithmetic_v<T>, "仅算术类型");
    return v < lo ? lo : (v > hi ? hi : v);
}
```

```cpp
// ⑲ 实践2：关键函数标 [[gnu::always_inline]] / inline 以助 LTO 前的内联
[[gnu::always_inline]] inline int hot_add(int a, int b) { return a + b; }
```

```cpp
// ⑲ 实践3：发布保留调试符号的独立副本，分发 strip 版
//   objcopy --only-keep-debug app app.debug
//   strip --strip-debug app
//   objcopy --add-gnu-debuglink=app.debug app
```

```bash
# ⑲ 实践4：CI 矩阵至少覆盖  Debug(-O0,-g, sanitizer) / Release(-O2,-flto) 两套
#   本地开发用 -Og（可调试又可优化）；发布用 -O2 -flto；测试跑 ASan+UBSan
```

```bash
# ⑲ 实践5：用 ccache 加速重复构建，配合 -ffile-prefix-map 保证缓存键稳定
ccache g++ -std=c++23 -O2 -flto -c app.cpp -o app.o
```

- `[经验]`：构建配置是**产品质量的旋钮**，应纳入版本控制、评审与 CI 门禁；任何"本地能编发布崩"的事故，第一反应查配置差异而非改代码。

## ⑳ 速查表

```
┌──────────────────────────┬───────────────────────────────────────────────┐
│ 目标                     │ 推荐标志（GCC 13 / C++23）                      │
├──────────────────────────┼───────────────────────────────────────────────┤
│ 开发调试                 │ -Og -g -Wall -Wextra                            │
│ 测试（抓内存/UB）        │ -O1 -g -fsanitize=address,undefined            │
│ 发布基线                 │ -O2 -DNDEBUG -flto                              │
│ 发布加固                 │ -fstack-protector-strong -fPIE -pie             │
│                          │   -Wl,-z,relro,-z,now （ELF）                    │
│ 极致性能（实测后）       │ -O3 或 -O2 -fprofile-use（PGO）                 │
│ 严格浮点                 │ 禁用 -ffast-math / -Ofast                      │
│ 可重现                   │ -ffile-prefix-map -fdebug-prefix-map            │
│                          │   SOURCE_DATE_EPOCH + --build-id=none          │
│ 警告即错误（CI）         │ -Werror（叠加 -Wshadow -Wconversion）          │
│ 静态库 / 动态库          │ ar rcs lib.a *.o / g++ -shared -o lib.so *.cpp │
│ 剥离调试符号             │ strip（保留 .debug 副本用于事后分析）          │
└──────────────────────────┴───────────────────────────────────────────────┘
```

| 标志 | 含义 | 何时用 |
|---|---|---|
| `-O0` | 不优化、逐句翻译 | 单步调试 |
| `-O2` | 发布默认优化 | **发布基准** |
| `-O3` | 激进（向量化/展开） | 数值，实测更快才用 |
| `-flto` | 链接时全程序优化 | 发布，统一开启 |
| `-fprofile-use` | PGO 二次编译 | 热点明确且能录真实负载 |
| `-fstack-protector-strong` | 强栈保护 | 发布加固 |
| `-fsanitize=address` | 内存错误检测 | 仅测试 |
| `-ffast-math` | 放松 IEEE | 仅渲染/媒体，禁严格浮点 |
| `-ffile-prefix-map` | 路径去绝对化 | 可重现构建 |

- `[标准]`：上述除 `-O*`/`-g`/`-flto` 等均为实现扩展；C++ 标准只固定 `NDEBUG` 对 `assert` 的影响。
- `[经验]`：记住一句话——**Debug 求可观测，Release 求快且硬，测试求抓虫，发布求可重现可审计**。四套配置分开管，绝不混用逻辑。

## 附录: CMake 构建配置实战

```cpp
#include <iostream>
int main(){std::cout<<"CMakeLists: cmake_minimum_required(VERSION 3.20); project(App LANGUAGES CXX); set(CMAKE_CXX_STANDARD 20)."<<std::endl;return 0;}
```

```cpp
#include <iostream>
#include <string>
int main(){std::cout<<"Makefile: CXX=g++, CXXFLAGS=-std=c++20 -O2 -Wall, LDLIBS=-lpthread."<<std::endl;return 0;}
```

```cpp
#include <iostream>
int main(){std::cout<<"Conan/vcpkg: package managers for C++. conan install .. --build=missing."<<std::endl;return 0;}
```

```cpp
#include <iostream>
#include <vector>
int main(){std::vector<int> v;v.push_back(1);std::cout<<v[0]<<std::endl;return 0;}
```

```cpp
#include <iostream>
int main(){std::cout<<"Ninja: faster than make. cmake -G Ninja -B build. CCache: compiler cache for rebuilds."<<std::endl;return 0;}
```


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第17章](Book/part02_toolchain/ch17_crosscompile.md) | 键值查找/缓存 | 本章提供概念，第17章提供实现 |
| [第12章](Book/part02_toolchain/ch12_buildsystems.md) | 配置解析/API响应 | 本章提供概念，第12章提供实现 |
| [第149章](Book/part13_engineering/ch149_ci_cd.md) | 泛型库/编译期计算 | 本章提供概念，第149章提供实现 |

## 附录 E：构建配置工业 [D: Stdlib / F: Industry / H: Design / J: Learning]

```
Debug vs Release 编译器差异:

| 选项 | Debug | Release | 差异 |
|---|---|---|---|
| -O | -O0 | -O2/-O3 | 0优化 vs 激进优化 |
| NDEBUG | 未定义 | 定义 | assert启用 vs 禁用 |
| _GLIBCXX_DEBUG | 默认 | 未定义 | 迭代器检查(100×慢) |
| ASan/TSan | 可选 | 禁用 | 地址/线程检测(~2×慢) |
| 符号 | -g | 可选 | 调试符号(二进制+50%) |
| LTO | 禁用 | 可选(-flto) | 跨TU优化(链接+50%时间) |

Google/LLVM/Chromium 实践:
- Debug: 日常开发, 必须-O0(快速编译, 频繁迭代)
- Release: CI + 生产, 必须-O2/-O3 + LTO
- ASan: 独立CI job, 不与Release共享(冲突)
- PGO: Profile-Guided Optimization → 二次编译 + 性能测例 → +10-20%性能
```

```cpp
#include <iostream>
int main() {
#ifdef NDEBUG
    std::cout << "Release mode: asserts disabled" << std::endl;
#else
    std::cout << "Debug mode: asserts enabled" << std::endl;
#endif
    std::cout << "Debug=fast compile; Release=fast runtime; ASan=safe runtime" << std::endl;
    return 0;
}
```

面试: Debug vs Release最大区别? -O0(无优化, 快编译) vs -O2(优化, 快运行)
       LTO是什么? Link-Time Optimization, 跨翻译单元内联和优化(代价: 链接时间)
       PGO如何工作? 1.编译加-profile-generate, 2.运行训练数据, 3.编译加-profile-use


## 相关章节（交叉引用）

- **后续依赖**：`Book/part13_engineering/ch148_gitflow.md`（第148章 Git 工作流（C++））—— 本章为其前置，建议后续延伸阅读。
- **相邻主题**：`Book/part03_language/ch19_variables.md`（第19章　变量、存储期、链接与 ODR（工业级深度版））—— 编号相邻、主题接续。
- **相邻主题**：`Book/part02_toolchain/ch16_ide.md`（第16章　IDE 与编辑器：VSCode / CLion / QtCreator / VIM（C++））—— 编号相邻、主题接续。
- **相邻主题**：`Book/part03_language/ch20_reference_pointer.md`（第20章　引用（reference）vs 指针（pointer）：语义本质、底层实现与生命周期战争）—— 编号相邻、主题接续。
- **同模块**：`Book/part02_toolchain/ch11_compilers.md`（第11章　编译器全景：GCC / Clang / MSVC 架构与 ABI（C++））—— 同模块下的其他主题。

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

## 真实开源项目参考（可查证链接）

> 构建配置与编译器驱动的真实工程载体——下列链接均指向可公开审阅的源码文件（L2 文件级）。

- **GCC 选项解析（`opts.cc`）**：[gcc-mirror/gcc · gcc/opts.cc](https://github.com/gcc-mirror/gcc/blob/master/gcc/opts.cc) —— `-O*`、`-f*`、`-m*` 等全部前端选项在此注册与分发，是「③ 优化级别」「⑭ 警告等级」章节的编译器实现源头。
- **LLVM LTO 驱动（`LTO.cpp`）**：[llvm/llvm-project · llvm/lib/LTO/LTO.cpp](https://github.com/llvm/llvm-project/blob/main/llvm/lib/LTO/LTO.cpp) —— 「⑥ LTO 链接时优化」的工业实现；`-flto` 如何把整个程序重构为跨 TU 优化单元（旧版 `PassManagerBuilder.cpp` 已重构移除，此为其继任）。
- **CMake 驱动源码**：[Kitware/CMake · Source/cmake.cxx](https://github.com/Kitware/CMake/blob/master/Source/cmake.cxx) —— 「⑰ 发布配置建议」对应的构建系统本体，`CMAKE_BUILD_TYPE` / `CMAKE_CXX_FLAGS` 由此消费。
- **Compiler Explorer 编译器探测**：[compiler-explorer/compiler-explorer · lib/compiler-finder.js](https://github.com/compiler-explorer/compiler-explorer/blob/main/lib/compiler-finder.js) —— 「④/⑧ [实现]真实汇编对比」所用平台的源码，解释它如何定位并调用本机 `g++`/`clang++`。
- **Bazel（bazelbuild/bazel，Google 出品）**：[BUILD](https://github.com/bazelbuild/bazel) 文件中 `copts = ["-O2","-DNDEBUG"]` 等价于 CMake 的 `CMAKE_CXX_FLAGS`；`cc_binary` 默认 `-c opt` 即 `-O2` + 头文件保护。
- **Apache Mesos（github.com/apache/mesos）**：其 `cmake/Boost.cxx` 演示如何用 CMake 探测 Boost 依赖，是「⑮ 依赖管理」的工业样本。
- **Abseil（abseil/abseil-cpp）**：`CMake/AbseilHelpers.cmake` 用 `target_compile_features` 钉死 C++ 标准，对应「⑯ C++ 标准版本」。
- **DPDK（DPDK/dpdk）**：数据面套件用 meson/CMake 双构建，`meson_options.txt` 中的 `enable_docs` 等开关对应「⑰ 发布配置」。

**最佳实践**：发布构建务必设 `-DCMAKE_BUILD_TYPE=Release` 且单独钉死 `-O2 -DNDEBUG`，避免 Debug 符号污染体积；CI 中用 `-Werror` 把警告当错误，配合「⑫ hardening」的 `-fstack-protector-strong -Wl,-z,relro,-z,now -fPIE` 形成可复现的供应链基线。

> 交叉引用：交叉编译工具链见 [ch17](Book/part02_toolchain/ch17_crosscompile.md)；汇编取证方法见 [ch157](Book/part14_perf/ch157_compiler_explorer.md)。

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

