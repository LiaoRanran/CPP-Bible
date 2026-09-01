# C9 C↔C++ 互操作：链接层的名字与布局

> 参考：C 侧 GCC 15.3.0（`gcc -std=c11`），C++ 侧 G++ 15.3.0（`g++ -std=c++17`）。所有符号/链接证据为本机真实产物。汇编视角见 A3（调用约定）、A5（结构体偏移）。
> 示例源：`c/_demo/c09_lib.c`、`c/_demo/c09_call_good.cpp`、`c/_demo/c09_call_bad.cpp`

## ① 我们真正要回答的问题 <span class="badge badge-std">标准</span>

1. 为什么 C 写的 `cadd` 函数，C++ 直接声明后链接会报 `undefined reference`？
2. `extern "C"` 到底改了什么——是改了代码，还是改了名字？
3. C 的结构体，C++ 能直接 `sizeof` 一样、按值传参一样吗？

> 判决先行：**C 与 C++ 能互相调用，当且仅当两层达成一致：①链接层的「名字」一致；②数据层的「布局」一致。** `extern "C"` 解决前者（关掉 C++ 的名字改写）；布局一致由同一 ABI 保证（接 C6 的偏移/对齐、A3 的调用约定）。少一层，要么链接失败，要么链接成功却运行时错位。

> 历史注脚：`ritchie:chist` 记载 C 的符号朴素——函数名就是链接器看到的名字（本机 `cadd`）。C++ 为支持函数重载必须给同名函数造不同链接名，于是引入 name mangling（名字改写）；为了还能调用海量的 C 库，又专门发明了 `extern "C"` 把改写关掉。两套名字体系之间的桥，就是这个关键字。

## ② 证据一：C 的符号朴素，C++ 的会改名

C 库 `c09_lib.c`（`int cadd(int,int)` + `struct Point`）编译成目标文件，用 `nm` 看符号：

```text
0000000000000000 T cadd
0000000000000010 T point_sum
```

`T` = 已定义的代码符号，名字就是 `cadd`——**C 不做任何改写**。

同一份调用，在 C++ 里**不写** `extern "C"`，只看目标文件里的「未解析引用」：

```text
                 U _Z4caddii
```

`U` = 未定义；`_Z4caddii` 是 C++ 把 `cadd(int,int)` 改写后的名字：**`_Z` 前缀 + `4`(名字长度) + `cadd` + `ii`(两个 int 参数)**。C 那边叫 `cadd`，C++ 这边找 `_Z4caddii`——**名字对不上，链接器自然找不到**。

## ③ 证据二：缺 `extern "C"` → 链接失败（真机）

把 `c09_call_bad.cpp`（只声明 `int cadd(int,int)`，无 `extern "C"`）链接进 `c09_lib.o`：

```text
ld.exe: ... undefined reference to `cadd(int, int)'
collect2.exe: error: ld returned 1 exit status
```

链接器把 C++ 改名的 `_Z4caddii` 去 C 库里找，只找到 `cadd`，匹配失败。**编译能过、链接暴死**——这是互操作最典型的「看着对、跑不起来」。

## ④ 证据三：加上 `extern "C"` → 桥接成功（真机）

`c09_call_good.cpp` 用 `extern "C"` 把声明包起来，再链接、运行：

```text
cadd(3,4)=7
point_sum{1,2}=3
```

`extern "C"` 让 C++ 侧也用 `cadd` 这个名字去链接，桥接通了；而且 `struct Point` 按值从 C++ 传进 C 函数、字段 `x=1,y=2` 被正确读出——**说明同一 ABI 下 C 结构体在 C++ 里布局完全一致**（接 C6：字段偏移/对齐由 ABI 定，与语言无关）。

## ⑤ 事故现场：比链接失败更阴险的「链接成功却错位」

链接失败至少报错；下面两种是**链接通过、运行时炸**：

1. **结构体两侧定义不一致**：C 侧 `struct Point{int x;int y;}` 与 C++ 侧 `struct Point{int y;int x;}`（字段顺序反了）。两边名字都是 `Point`、都能编能链，但 C 把 `x` 放 @0、C++ 按自己的定义读 @0 当 `y`——**数据静默错位**。所以跨语言的结构体声明必须逐字段、逐顺序、逐类型完全相同（最好放同一头文件，用 `#ifdef __cplusplus` 守卫）。
2. **`long` 尺寸跨平台**（接 C6）：C 与 C++ 在同一平台一致，但 Windows(LLP64,`long`=4) 与 Linux(LP64,`long`=8) 的结构体布局不同。跨平台互传裸结构体仍会错位（C6 事故 2）。

> 立场：[标准] `extern "C"` 是 **C++ 特性**（C 里写它不合法），作用是「让这个函数/变量用 C 链接（不做 C++ 名字改写）」。它不改变函数体、不改调用约定，只改名字。
> 立场：[实现·GCC15.3] 改名规则稳定可预测（`_Z` + 名长 + 名 + 参数编码），`c++filt` 可还原——排「undefined reference」时先 `nm`/`c++filt` 对比两侧名字。
> 立场：[经验] 跨语言头文件用「`#ifdef __cplusplus extern "C" { #endif ... #ifdef __cplusplus } #endif`」守卫，让一份声明 C/C++ 通吃；**ABI 边界只暴露 C 能表达的东西**——别用 C++ 重载/模板/异常/带虚表类当跨语言接口（虚表布局、异常 ABI 各编译器不同，是更深的坑）。

## ⑥ 小结与路线图

C 符号朴素（`cadd`），C++ 改名（`_Z4caddii`）；`extern "C"` 关掉改名、桥接链接；同一 ABI 下结构体布局跨语言一致，但**定义不一致或跨平台**会静默错位。互操作的两大支柱：名字（`extern "C"`）+ 布局（C6 偏移/对齐、A3 调用约定）。

Part 0 收官：汇编（A1–A6）讲机器怎么跑，C（C1–C9）讲贴近硬件的高级语言怎么想。下一站是主书 147 章——对象模型、模板、标准库，全站在这些地基上。

## 参考引用

- `[std-c11]`（N1570）：6.2.8 对齐、6.7.2.1 结构体布局（ABI 一致性基础）。
- `[cppref:cpp/language/extern]`（离线 cppreference）：`extern "C"` 与名字改写（C++ 侧事实源）。
- `[ritchie:chist]`：Ritchie《The Development of the C Language》——C 符号朴素、与 BCPL 的渊源（人文源，见 `humanities_index.md`）。
- 交叉引用：C2（链接器符号解析）；C6（结构体布局/LLP64，ABI 一致性）；A3（调用约定，ABI 另一半）；A5（§④ 偏移硬编码进指令）；主书 ch33–ch34（C++ 类与虚表布局，跨语言接口禁区）、ch 与 C 互操作章。
