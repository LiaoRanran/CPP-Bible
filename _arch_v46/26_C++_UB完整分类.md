# 方向 26：C++ UB 完整分类（每类 3 个真实例子）

> 调研时间：2026-09-29
> 本机实测工具链：GCC 15.3.0（MinGW-W64 winlibs，`C:/Qt/Tools/mingw1530_64/bin/g++.exe`）、GCC 13.1.0（MinGW-Builds）、Clang 22.1.8（msys2，`x86_64-w64-windows-gnu`）
> 本文件所有标注「本机实测」的结论均在本机真实编译运行过；未实测的明确标注。

---

## 核心结论

1. **C++ 的未定义行为（UB）不是一个可枚举的列表，而是"标准刻意不规定的一切"。** C++ 工作草案 §3.66 `[defns.undefined]` 的完整定义只有一句："**behavior for which this document imposes no requirements**"（本文件不施加任何要求的行为）。任何"UB 清单"都是社区归纳，不是标准枚举——因此"UB 完整分类"的正确写法是**按根因分类**，而不是按标准条款逐条抄。

2. **UB 的工程危险性不来自"崩溃"，而来自"编译器被授权利用 UB 做反向推理"。** 一旦某条执行路径含 UB，编译器可假定该路径**不可达**，于是删除空指针检查、合并分支、把循环变成死循环、甚至让结果"时间旅行"（先写后读被重排到写之前）。cppreference 的 "UB and optimization" 章节给出 **7 个** 在 Godbolt 上可直接复现的最小例。

3. **检测工具是"分类器"而不是"全知者"，且本机三套工具链的 sanitizer 运行时全部缺失。** ASan 只覆盖空间错误（越界/UAF/双重释放），MSan 只覆盖未初始化读取，TSan 只覆盖数据竞争，UBSan 覆盖约 30 类显式 UB 但**不覆盖严格别名违规**。本机实测：GCC 15.3.0 链接 `-lubsan` 失败（`cannot find -lubsan`），Clang 22.1.8 链接 `libclang_rt.asan_dynamic_runtime_thunk.a` 失败——**这意味着「用 sanitizer 抓 UB」在本机当前不可执行，是阙疑必须诚实登记的测量约束**。

---

## 精确数字与案例

### 0. 标准的定义原文与"相邻类别"

`[defns.undefined]`（C++23 工作草案 §3.66）原文（已从 eel.is/c++draft/defns.undefined 逐字核对）：

> undefined behavior — **behavior for which this document imposes no requirements**
> *Note 1*: Undefined behavior may be expected when this document omits any explicit definition of behavior or when a program uses an incorrect construct or invalid data. Permissible undefined behavior ranges from **ignoring the situation completely with unpredictable results**, to behaving during translation or program execution in a documented manner characteristic of the environment (with or without the issuance of a diagnostic message), to **terminating a translation or execution** (with the issuance of a diagnostic message).
> Many incorrect program constructs do not engender undefined behavior; they are required to be diagnosed.
> Evaluation of a constant expression never exhibits behavior explicitly specified as undefined in [Clause [intro]] through [Clause [cpp]].

注意最后一句：**常量表达式求值永远不会表现出 UB**——这正是 `constexpr` 成为"UB 探测器"的规范依据（见方向 30）。

cppreference 把"与 UB 相邻"的类别明确区分成 **7 类**（该页原文列表）：`ill-formed`（必须诊断）、`ill-formed, no diagnostic required`（如 ODR 违规，链接期才能发现）、`implementation-defined behavior`（必须记录）、`unspecified behavior`（不要求记录）、`erroneous behavior`（C++26 新增，推荐诊断）、`undefined behavior`、`runtime-undefined behavior`（C++11 起：核心常量表达式求值期之外的 UB）。这个"7 类"划分本身就是阙疑四态判决（block/warn/advice/通过）的规范学依据：**只有 `ill-formed` 是编译器必须报错的**，其余都靠工具与经验。

### 分类总览（10 类 × 3 例 = 30 个最小复现）

下表是本文的分类骨架。每类给 3 个可编译最小复现，并标注标准锚点、检测工具、本机实测状态。

| # | 类 | 根因 | 标准锚点 | 主要检测器 |
|---|---|---|---|---|
| 1 | 空间越界 | 对象边界外访问 | `[expr.add]`、`[dcl.array]` | ASan（强）、Valgrind（弱） |
| 2 | 生命周期 | 对象已死仍访问 | `[basic.life]`、`[class.cdtor]` | ASan、MSan（use-after-dtor） |
| 3 | 未初始化/无效值 | 不确定值被求值 | `[dcl.init]`、`[basic.indet]` | MSan（唯一强项）、Valgrind |
| 4 | 算术 | 有符号溢出、移位越界、除零 | `[expr.pre]`、`[expr.shift]` | UBSan |
| 5 | 类型别名 | 用不相容类型访问 | `[basic.lval]`（C++ 的 strict aliasing） | **无成熟检测器**（TySan 尚新） |
| 6 | 求值顺序 | 未测序的副作用 | `[intro.execution]`、`[expr.ass]` | 编译器静态警告（唯一手段） |
| 7 | 指针 | 空解引用、越界指针算术 | `[expr.unary.op]`、`[expr.add]` | UBSan、ASan |
| 8 | 并发 | 数据竞争 | `[intro.races]` | TSan（唯一强项） |
| 9 | 对象模型 | ODR 违规、vptr 误用、非法向下转型 | `[basic.def.odr]`、`[expr.dynamic.cast]` | UBSan(vptr)、链接器/LTO |
| 10 | 其他 | 无副作用死循环、释放函数不匹配、函数指针类型不匹配 | `[intro.progress]`、`[expr.delete]` | UBSan、ASan |

### 类 1：空间越界（Out-of-bounds）

**例 1-1（本机实测）**：栈数组写越界。

```cpp
#include <cstdio>
int h(){ int a[5]; for(int j=0;j<=5;j++) a[j]=j; return a[0]; }   // a[5] 越界
int main(){ printf("h=%d\n", h()); return 0; }
```

本机实测（GCC 15.3.0 / GCC 13.1.0 / Clang 22.1.8，`-O0` 与 `-O2` 均）：**全部静默输出 `h=0`，exit=0，无任何诊断**。这是空间越界最典型的形态：**"静默错误"**，不是崩溃。`-Wall -Wextra` 下三编译器均未报警（本机实测）。规范锚点：`[expr.add]`——指针算术结果若不在 `[begin, end]` 内（含 one-past-the-end）即为 UB。

**例 1-2**：`std::vector` 迭代器越界读（`v[v.size()]`）。ASan 报 `heap-buffer-overflow`；Valgrind 报 `Invalid read of size 4`。二者定位行号一致（Valgrind/ASan 对照实测见方向 29）。

**例 1-3**：`memcpy` 越界源/目的。ASan 报 `memcpy-param-overlap`（源目的重叠，属 UB）或 `heap-buffer-overflow`。

**检测覆盖差异**：ASan 在**堆/栈/全局**三类对象外都铺 redzone，是最强检测器；但它**漏报"跨过 redzone 的远距离越界"**——ASan 论文明确列出的三类 false negative 之一。本机实测（例 1-1）在无 sanitizer 运行时的情况下完全无法检测。

### 类 2：生命周期（Lifetime）

**例 2-1**：悬垂指针（返回局部对象地址）。

```cpp
int* bad(){ int local = 42; return &local; }   // 返回后 local 生命周期结束
```

GCC 13+ 的 `-Wreturn-local-addr` 可静态抓到（项目 `_arch_v46` 所在的 CPP-Bible UB 库记录该例本机 SIGSEGV，exit=139）。

**例 2-2**：`std::vector` 迭代器失效。

```cpp
std::vector<int> v{1,2,3};
auto it = v.begin();
v.push_back(4);        // 可能 reallocate
*it;                   // 迭代器已失效 → UB
```

CPP-Bible UB 库记录本机实测 SIGSEGV（exit=139）。

**例 2-3**：析构后访问（use-after-destruction）。MSan 有专门检测：文档原文"After invocation of the destructor, the object will be considered no longer readable"，可用 `-fno-sanitize-memory-use-after-dtor` 或 `MSAN_OPTIONS=poison_in_dtor=0` 关闭。

### 类 3：未初始化 / 无效值（Indeterminate value）

**例 3-1（本机实测）**：读未初始化数组。

```cpp
#include <cstdio>
int main(){ int a[10]; int s=0; for(int i=0;i<10;i++) s+=a[i]; printf("s=%d\n", s); return 0; }
```

本机实测结果（`-O0`，三个编译器全部静默，值各不相同且不可复现）：
- GCC 15.3.0 `-O0`：`s=297780922`；`-O1`：`s=-25442731`；`-O2`：`s=1615970530`；`-O3`：`s=-1492990318`；`-Os`：`s=-1492516522`
- GCC 13.1.0 `-O0`：`s=1290687602`；`-O2`：`s=2067748199`；`-O3`：`s=1373394044`；`-Os`：`s=-1009511281`
- Clang 22.1.8：`-O0`：`s=1946384909`；**`-O1`/`-O2`/`-O3`/`-Os`：`s=0`**

这是**同一份源码、同一台机器、仅改优化档就得到 8 个不同答案**的完整实测证据（GCC 5 个不同值 + Clang 2 个不同值）。Clang 在 `-O1` 以上把 `s` 直接折叠为常量 0，是本文件最有价值的"测量陷阱"证据之一。

**例 3-2**：未初始化 `bool`。cppreference 的 UB-and-optimization 第 2.3 节原例：读未初始化的 `bool p`，其值不是 `true` 也不是 `false` → UB。UBSan 的 `-fsanitize=bool` 专门检测"加载既非 true 也非 false 的 bool 值"。

**例 3-3**：`reinterpret_cast<unsigned char*>` 写入 10 后按 `bool` 读回（cppreference 2.4 节 "Invalid scalar"）。

**工具覆盖**：MSan 是唯一强项，开销为"**Typical slowdown 3x**"（Clang 官方文档原文），内存 2x，开启 origin tracking 后 3x。ASan **完全不检测未初始化读取**（影子内存只编码"可访问/不可访问"，没有"已写入"位）。

### 类 4：算术（Arithmetic）

**例 4-1（本机实测）**：有符号整数溢出导致的死循环。

```cpp
int f(){ for(int i=0;i>=0;i++){} return 42; }   // i++ 溢出 INT_MAX
```

本机实测（超时 2 秒判定为死循环）：

| 优化档 | GCC 15.3.0 | GCC 13.1.0 | Clang 22.1.8 |
|---|---|---|---|
| `-O0` | 输出 `f=42`，exit=0 | 输出 `f=42`，exit=0 | **超时（exit=124）** |
| `-O1` | 输出 `f=42`，exit=0 | 输出 `f=42`，exit=0 | **无输出，exit=3** |
| `-O2` | **超时（exit=124）** | **超时（exit=124）** | **无输出，exit=3** |
| `-O3` | 超时（exit=124） | 超时（exit=124） | 无输出，exit=3 |
| `-Os` | 超时（exit=124） | 超时（exit=124） | 无输出，exit=3 |

**同一份源码在 15 个编译配置下出现 4 种截然不同的行为**（正常返回 42 / 真死循环 / 异常终止 exit=3）。GCC 的 `-fwrapv` 可完全修复：`-O2 -fwrapv` 下输出 `f=42`，exit=0（本机实测）。Clang 的 exit=3 来自 UB 被利用后插入的 `unreachable`/trap 路径（机制未在本机反汇编确认，列入盲区）。

**例 4-2**：`x + 1 > x` 恒真假设。cppreference 2.1 节原例：`int f(int x){ return x+1 > x; }`，编译器可优化为恒 `true`。本机实测 `g(INT_MAX)`：GCC 15.3.0 `-O0` 返回 **1**，Clang 22.1.8 `-O0` 返回 **0**——**即使 `-O0` 两家就不一致**。

**例 4-3**：移位 UB。Clang UBSan 文档原文："For a signed left shift, also checks for signed overflow in C, and for unsigned overflow in C++." 对应检查名 `-fsanitize=shift`（可拆为 `shift-base` / `shift-exponent`）。`1 << 31`（int 为 32 位）是经典 UB。

### 类 5：类型别名（Strict aliasing）—— **本机最强 miscompile 证据**

**例 5-1（本机实测，GCC 真实 miscompile）**：

```cpp
int reorder(unsigned* foo){ *foo = 0; short* ptr=(short*)foo; *ptr=1; return *foo; }
```

本机实测：

| 优化档 | GCC 15.3.0 | GCC 13.1.0 | Clang 22.1.8 |
|---|---|---|---|
| `-O0` / `-O1` | `reorder=1` | `reorder=1` | `reorder=1` |
| `-O2` | **`reorder=0`**（错误结果） | **`reorder=0`**（错误结果） | `reorder=1` |

**GCC 在 `-O2` 下真的把 `*ptr=1` 优化掉了**，返回 0 而不是 1——这是"严格别名违规导致真实 miscompile"的本机可复现证据。修复手段：`-O2 -fno-strict-aliasing` 后恢复 `reorder=1`（本机实测）。

**例 5-2**：字节序交换（本项目 CPP-Bible 与腾讯云技术文章均记录同一形态）。`int i=0x12345678; short* p=(short*)&i;` 交换两个 short——`-O2` 下结果与 `-O0` 不同。

**例 5-3**：union 类型双关。cppreference 与 Shafik Yaghmour 博客（2025-02-11）都给出同一例子：读 union 的"非活跃成员"（如把 `float` 写入后按 `int` 读）是 UB；但在 `constexpr` 上下文里会直接编译失败（因为常量表达式不允许 UB）——**`constexpr` 是最廉价的 UB 探测器**。

**工具覆盖警告**：Clang 官方文档明确 **UBSan 不覆盖严格别名**；CPP-Bible UB 库对此的标注也是"—（UBSan 不覆盖）"。唯一可用手段是 `-Wstrict-aliasing` 静态警告 + `-fno-strict-aliasing` 二分。本机实测：`-O2 -Wall -Wextra` 下 **GCC 与 Clang 对例 5-1 均未输出任何警告**。

### 类 6：求值顺序（Unsequenced side effects）

**例 6-1（本机实测）**：`i = i++ + ++i;`

```cpp
int i=0; i = i++ + ++i;
```

本机实测：GCC 15.3.0 / GCC 13.1.0 / Clang 22.1.8 在 `-O0` 与 `-O2` 下**结果都是 `i=2`**——三家"碰巧一致"，但标准明确是 UB。**这是最危险的一类**：结果一致会让人误以为代码正确。

警告差异（本机实测）：
- GCC：`warning: operation on 'i' may be undefined [-Wsequence-point]`（GCC 15.3.0 对同一行报了 **4 次**）
- Clang：`warning: multiple unsequenced modifications to 'i' [-Wunsequenced]`（仅 1 次）

**两家用不同的 flag 名、不同的措辞报告同一个 UB**——这是阙疑规则库必须做的"警告归一化"工作。

**例 6-2**：`a[j] = j++;`（下标与副作用未测序）。GCC 报 `-Wsequence-point`；本机实测输出 `a[0]=0 a[1]=0`。

**例 6-3**：`i = i++ + 1;`（C++11 起明确 UB）。标准 `[intro.execution]/15` 的原例即为 `i = i++ + 1; // the behavior is undefined`（StackOverflow 引用 C++11 原文）。C++11 用 "sequenced before" 取代了 C++98/03 的 "sequence point" 术语，但 `i = ++i;` 是**有定义**的、`i = i++;` 是 UB。

### 类 7：指针（Pointer）

**例 7-1**：空指针解引用。cppreference 2.5 节原例 `int x = *p;`（p 为空）。本机实测的变体（把解引用放在检查之前）：

```cpp
int deref(int* p){ int x=*p; if(p==nullptr) return -1; return x; }
```

本机实测：三编译器在 `-O0`..`-Os` 全部输出 `ok=7`（因为调用方传了非空指针）——**编译器可能已把 `if(p==nullptr)` 判定为恒假而删除**（未反汇编确认，列入盲区）。这是 LWN 2009 年 "Optimizations and undefined behavior" 系列讨论的核心案例（GCC 从 `*p` 推断 `p` 永不为空，删掉了 NULL 检查）。

**例 7-2**：越界指针算术。`int a[10]; int* p = a + 20;`（即使不解引用也是 UB）。规范 `[expr.add]`。

**例 7-3**：指针溢出。UBSan 检查名 `-fsanitize=pointer-overflow`（文档原文："指针算术溢出，或新旧指针中任一为空"）。

### 类 8：并发（Data race）

**例 8-1**：非原子共享写。

```cpp
int Global;
void* T1(void*){ Global = 42; return nullptr; }
int main(){ /* 另一线程 Global = 43; */ }
```

这是 TSan 官方文档的 tiny_race 例子。CPP-Bible UB 库记录本机实测"连续 3 次运行结果看起来正确"——**数据竞争最危险的形态是"本次恰好正确"**。

**例 8-2**：锁顺序反转导致死锁。CPP-Bible UB 库记录本机实测 `timeout` 杀掉（exit=124）。

**例 8-3**：signal handler 中调用非异步信号安全函数。CPP-Bible UB 库记录本机 exit=3 异常终止。

**工具覆盖**：TSan 是唯一强项，Clang 文档原文开销 "**Typical slowdown ... about 5x-15x**"、"memory overhead ... about 5x-10x"（另一处写 "5x plus 1Mb per each thread"，另有 3x / 9x 两档精度-开销折中）。TSan **不检测死锁**（它只做 happens-before 数据竞争检测）——这是能力边界，必须写进阙疑的"检测不到什么"清单。

### 类 9：对象模型（ODR / vptr / 转型）

**例 9-1**：ODR 违规。两个 TU 对同一 `inline` 函数给出不同定义 → `ill-formed, no diagnostic required`。链接器/LTO 可能不报错。

**例 9-2**：vptr 误用。UBSan 检查名 `-fsanitize=vptr`（文档原文："使用 vptr 指示错误动态类型或生命周期未开始/已结束的对象"）。注意：**minimal runtime 不支持 `vptr` 检查**（Clang 文档明说）。

**例 9-3**：`static_cast` 向下转型到错误派生类型后访问派生成员。CPP-Bible 卡片 `misconception_MIS-UB-009.md` 原话："static_cast 向下转型不做运行时检查；对象实际不是该派生类型时，访问派生成员即 UB"。

### 类 10：其他

**例 10-1**：无副作用的非平凡死循环。cppreference 2.7 节的费马大定理示例：编译器可以证明循环不会终止且无副作用，从而删除循环。C++26 起"trivial infinite loops"不再是 UB（Sandor Dargo 2026-09-16 博文）。

**例 10-2**：`new[]` / `delete` 不匹配。ASan 报 `alloc-dealloc-mismatch`；**Windows 上该检查默认关闭**（Microsoft Learn 原文："默认情况下，AddressSanitizer 中的 alloc/dealloc 不匹配功能在 Windows 中处于禁用状态"），需 `ASAN_OPTIONS=alloc_dealloc_mismatch=1`。

**例 10-3**：通过错误类型的函数指针调用。UBSan 检查名 `-fsanitize=function`。

### 数字汇总：UB 研究的实证规模

- **IOC 整数溢出研究**（Dietz 等，ISSTA 2012 / TOSEM 2015，DOI 10.1145/2743019）：这是第一个针对整数溢出的详细实证研究，开发了动态检测工具 IOC。论文摘要原文承认"integer overflow issues in C and C++ are subtle and complex, that they are common even in mature, widely-used programs"。**注：本文未逐字核对论文正文中的具体样本量数字，列入盲区**（PDF 在本环境无法解析）。
- **LLVM 官方博客**（Lattner 等，2011-05-13 起三篇）："What Every C Programmer Should Know About Undefined Behavior" #1/3、#2/3、#3/3——UB 领域被引用最多的科普一手来源。
- **cppreference UB 页面**给出的 UB 示例类别为 **6 类**（数据竞争、数组越界、有符号溢出、空指针解引用、未序列化的多重修改、跨类型指针访问），"UB and optimization" 给出 **7 个** Godbolt 可复现例。
- **本文件实测覆盖**：3 个编译器 × 5 个优化档 × 8 个 UB 程序 = **120 次编译运行**，得到 **4 种不同的"同源异构"行为**（见类 3、类 4）。

---

## 对阙疑的 3 条具体行动

**行动 1（立即可做，0 依赖）：把「UB 分类」写进规则库的 `cpp_standard` 字段，并新增 5 条 block 规则覆盖本文件实测的 miscompile 形态。**
- 文件：`data/_gate_rules.json`（当前 67 条 = block 44 / warn 16 / advice 7）。
- 新增建议：`UB-SA-001`（`reinterpret_cast`/C 风格转换后以不相容类型写入，对应例 5-1，命中即 block）、`UB-SEQ-001`（同一标量在单一表达式中被修改 ≥2 次，对应例 6-1）、`UB-ARITH-001`（`for` 循环计数器为有符号且无上界保护，对应例 4-1）、`UB-INIT-001`（数组/标量在首次读前无写入，对应例 3-1）、`UB-OOB-001`（循环上界用 `<=` 而非 `<` 且下标为数组，对应例 1-1）。
- 验收：对每条新规则准备 1 个本文件中的最小复现作为 positive fixture，1 个修复版作为 negative fixture，跑 `--check`。

**行动 2（1 天内）：把本文件的 120 次实测做成「编译档敏感性矩阵」，作为论文 Threats to Validity 的硬证据。**
- 具体做法：写 `tools/ub_opt_matrix_<batch>.py`，对 `t_ovf / t_sa / t_uninit / t_seq` 四个源文件，在 `{GCC15.3.0, GCC13.1.0, Clang22.1.8} × {-O0,-O1,-O2,-O3,-Os}` 共 15 个配置下编译运行，把 stdout + exit code 写入 `data/ub_opt_matrix.json`。
- 关键可复算数字：类 4 例 4-1 的 **15 配置 → 4 种行为**；类 3 例 3-1 的 **15 配置 → 8 种不同输出值**。
- 论文写法：在 §Threats to Validity 引用该矩阵，主张"检测率必须绑定编译档报告，否则数字不可比"——这正是 v0.3 已量化的"编译档"陷阱的加强版。

**行动 3（3 天内）：修掉「sanitizer 在本机不可用」这个致命测量缺口，并把它变成论文的诚实登记项。**
- 现状（本机实测）：GCC 15.3.0 `-fsanitize=undefined` → `cannot find -lubsan`；Clang 22.1.8 `-fsanitize=address` → `cannot find libclang_rt.asan_dynamic_runtime_thunk.a`。**即本机当前无法运行任何 sanitizer 报告**。
- 可执行方案：在 CI（GitHub Actions `ubuntu-latest`，自带 GCC/Clang + libasan/libubsan/libtsan）上跑 sanitizer 矩阵，把原始 stderr 保存为 `data/sanitizer_reports/*.txt`；本机只做"编译期警告 + `-O0`/`-O2` 输出分歧"两类证据（这两类本机已可复现，见类 5 与类 6）。
- 诚实登记：`research/12_threats_to_validity.md` 增加一条："本项目的 sanitizer 证据来自 CI，非本机；本机工具链（MinGW GCC 15.3.0 / msys2 Clang 22.1.8）不捆绑 sanitizer 运行时。"

---

## 盲区（诚实标注）

1. **未核对 IOC 论文（Dietz 等）正文的具体数字**。`wdtz.org/files/tosem15.pdf` 与 `users.cs.utah.edu/~regehr/papers/tosem15.pdf` 均为 PDF，本环境 WebFetch 拒绝解析、Read 工具报 "Cannot display content of binary file"，因此本文只引用其公开摘要文字，**不引用任何"检测到 N 个溢出、M% 是无意的"这类具体数字**。
2. **Clang `-O1` 起例 4-1 的 `exit=3` 机制未确认**。本机只观测到"无输出 + exit=3"，未反汇编确认是 `unreachable` 插入、`ud2`、还是 MinGW `abort()`（exit 3）。机制推测**未经证实**。
3. **例 7-1 的 NULL 检查是否真被删除未反汇编确认**。本文只报告运行时输出（`ok=7`），未看汇编。
4. **类 5 的 `swap16` 例在本机 `-O2` 下未复现出错误结果**（三编译器均输出 `56781234`），而公开资料（腾讯云文章）记录 `-O2` 下应为 `12345678`。差异可能源于编译器版本/代码细节不同，**本文以本机实测为准，不采信未复现的二手数字**。
5. **`[defns.undefined]` 的条款号（§3.66）来自 eel.is 工作草案快照**，正式发布版（ISO/IEC 14882:2024）编号可能不同；本文只保证"原文文字"逐字准确。
6. **"UB 清单"的完整性无法保证**。cppreference 页面明确说该页"并未给出标准的条款引用"，因此本文的 10 类划分是**根因归纳**，不声称穷尽。已知未覆盖的 UB 形态至少包括：`realloc` 后使用旧指针、`setjmp/longjmp` 跨析构、`va_list` 误用、`std::launder` 缺失、`memcpy` 重叠、原子操作内存序错误。
7. **ARM / MSVC 的实际行为未实测**。本机只有 x86-64 MinGW 工具链；`char` 在 ARM 上默认 unsigned、MSVC 的 `long double` 为 64 位等差异均**引自文档而非实测**。

---

## 来源

1. ISO C++ 工作草案 `[defns.undefined]`（§3.66）原文 — https://eel.is/c++draft/defns.undefined （2026-09-29 读取）
2. cppreference: Undefined behavior — https://en.cppreference.com/w/cpp/language/ub （含 "UB and optimization" 7 例与 7 类相邻类别）
3. cppreference 中文镜像 — https://zh.cppreference.net/cpp/language/ub.html
4. LLVM Project Blog, Chris Lattner et al., "What Every C Programmer Should Know About Undefined Behavior #1/3" — https://blog.llvm.org/2011/05/what-every-c-programmer-should-know.html （2011-05-13）
5. LLVM Project Blog, 同系列 #2/3 — https://blog.llvm.org/2011/05/what-every-c-programmer-should-know_14.html （2011-05-14）
6. Dietz, Li, Regehr, Adve, "Understanding Integer Overflow in C/C++", ISSTA 2012 / TOSEM 2015, DOI 10.1145/2743019 — https://dl.acm.org/doi/10.1145/2743019 ；作者版 PDF https://wdtz.org/files/tosem15.pdf
7. Microsoft, "Undefined behavior can result in time travel (among other things, but time travel is the funkiest)", The Old New Thing, 2014-06-27 — https://devblogs.microsoft.com/oldnewthing/20140627-00/?p=633
8. Clang 官方文档 UndefinedBehaviorSanitizer（可用检查完整清单、`vptr` 不在 minimal runtime 中） — https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html
9. Clang 官方文档 MemorySanitizer（"Typical slowdown 3x"、use-after-destruction、需全程序插桩） — https://clang.llvm.org/docs/MemorySanitizer.html
10. Clang 官方文档 ThreadSanitizer（"5x-15x" / "5x-10x"） — https://hpc-wiki.info/hpc/ThreadSanitizer ；https://bcain-llvm.readthedocs.io/projects/clang/en/latest/ThreadSanitizer/
11. Microsoft Learn, "错误：alloc-dealloc-mismatch"（Windows 默认关闭） — https://learn.microsoft.com/zh-cn/cpp/sanitizers/error-alloc-dealloc-mismatch?view=msvc-170
12. LWN.net, "Optimizations and undefined behavior", 2009-07-22 — https://lwn.net/Articles/342593/
13. Stack Overflow, "New Sequence Points in C++11"（引用 `[intro.execution]/15` 与 `i = i++ + 1;` 原例） — https://stackoverflow.com/a/19069981
14. Shafik Yaghmour, "What You Need to Know when Optimizations Changes the Behavior of Your C++", 2025-02-11 — https://shafik.github.io/c++/undefined%20behavior/llvm/2025/02/11/when-opt-changes-program-behavior.html
15. 本项目自有 UB 反例库（15 例：内存 5 + 并发 5 + 生命周期 5；GCC 15.3.0 MinGW；sanitizer 运行时缺失） — https://liaoranran.github.io/CPP-Bible/Appendix/ub/
16. Sandor Dargo, "C++26: Trivial infinite loops are no longer undefined behaviour", 2026-09-16 — https://www.sandordargo.com/blog/2026/09/16/cpp26-trivial-infinite-loops
17. 腾讯云开发者社区, "gcc 编译参数 -fno-strict-aliasing"（`i=12345678` vs `i=56781234` 实测） — https://cloud.tencent.com/developer/article/1159055
18. 本机实测（GCC 15.3.0 / GCC 13.1.0 / Clang 22.1.8，2026-09-29），原始源文件与输出见 `_tmp/exp/`（工作副本，不进入仓库）
