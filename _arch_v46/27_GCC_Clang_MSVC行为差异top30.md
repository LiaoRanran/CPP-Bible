# 方向 27：GCC / Clang / MSVC 行为差异 top 30

> 调研时间：2026-09-29
> 本机实测工具链：GCC 15.3.0（MinGW-W64 winlibs，x86_64-msvcrt-posix-seh）、GCC 13.1.0（MinGW-Builds x86_64-posix-seh-rev1）、Clang 22.1.8（msys2，target `x86_64-w64-windows-gnu`）
> ⚠️ 本机**没有 MSVC**。凡 MSVC 一栏，标注「文档」的是引自 Microsoft Learn / 标准文档，**不是本机实测**；标注「未核实」的一律不写具体数字。
> 本表 30 条中，**第 1–14 条为本机实测**，第 15–30 条为文档依据（已标）。

---

## 核心结论

1. **"三编译器行为差异"的主体不是 bug，而是标准明确授权的三类自由度**：`implementation-defined`（必须记录，如 `char` 符号、`long` 尺寸）、`unspecified`（不要求记录，如实参求值顺序）、以及"标准未规定"（如 `std::vector` 扩容因子、`typeid().name()` 格式）。**阙疑的规则库若把这三类当"错误"报，就是设计性误报。**

2. **最危险的不是"结果不同"，而是"结果不同但没人知道"**。本机实测最有价值的一条是：`g(INT_MAX)`（`x+1 > x`）在 **`-O0`** 下 GCC 返回 1、Clang 返回 0——**连"关掉优化就一致"这个常识都不成立**。这与阙疑 v0.3 记录的"`-O1`→`-O0` 使 3/5 miss 被同一 sanitizer 抓住"是同一现象的两种表现。

3. **跨平台差异的量化单位应当是"配置"，不是"编译器"**。本机 3 个编译器 × 5 个优化档 = 15 个配置，仅 4 个测试程序就产生了 4 种"同源异构"行为（详见方向 26 类 3/类 4）。因此阙疑的 `compiler`/`platform` 元数据字段不能只写 "gcc"，必须写 `gcc-15.3.0-mingw-x86_64-msvcrt-O2`。

---

## 精确数字与案例（30 条）

### 【实测组】第 1–14 条

**1. 函数实参求值顺序（`unspecified`）**

```cpp
char tr[8]; int n=0;
int f(char c,int v){ tr[n++]=c; return v; }
void g(int,int,int){}
int main(){ g(f('A',1),f('B',2),f('C',3)); tr[n]=0; printf("arg order=%s\n",tr); }
```

| | GCC 15.3.0 | GCC 13.1.0 | Clang 22.1.8 |
|---|---|---|---|
| `-O0` | `CBA` | `CBA` | `ABC` |
| `-O2` | `CBA` | `CBA` | `ABC` |

**GCC 右到左，Clang 左到右，优化档无关。** 规范：`[expr.call]`——实参求值顺序 unspecified（C++17 起只保证"indeterminately sequenced"，不重叠）。**无 bug 编号，这是规范授权的自由度。**

**2. `char` 的默认符号（`implementation-defined`）**

本机实测（x86-64 MinGW，三编译器一致）：`(char)-1 < 0` → **1**，即 `char` 默认为 **signed**。文档依据：GCC 手册 "Characters implementation" 说明 `-fsigned-char` / `-funsigned-char` 可切换；ARM/AArch64 平台默认 **unsigned**（本机无 ARM 工具链，未实测）。**MSVC（文档）：`char` 默认 signed。** 无 bug 编号。

**3. `sizeof(long)`（`implementation-defined`，LLP64 vs LP64）**

本机实测：GCC 15.3.0 / GCC 13.1.0 / Clang 22.1.8 全部 **4 字节**（Windows LLP64）。
- Linux x86-64 LP64（文档）：**8 字节**。
- MSVC（文档）：**4 字节**。

预定义宏实测：`__SIZEOF_LONG__ = 4`（两个 MinGW 工具链一致）。

**4. `sizeof(long double)` 与有效精度（`implementation-defined`）**

本机实测：三者全部 `sizeof(long double) = 16`、`alignof = 16`、`__LDBL_DIG__ = 18`，`printf("%.20Lf", 1.0L/3.0L)` 输出 **`0.33333333333333333334`**（20 位十进制有效）→ 实际是 **x87 80 位扩展精度**（16 字节里只有 10 字节有效 + 6 字节 padding）。
- MSVC（文档）：`long double` 与 `double` 相同，**8 字节、53 位尾数**。
- 关键差异：**同一份浮点代码在 MinGW 与 MSVC 下精度不同**，且 `printf("%Lf")` 的 ABI 传递方式也不同。

**5. `sizeof(wchar_t)`**

本机实测：三者全部 **2 字节**（Windows，UTF-16）。
- Linux（文档）：**4 字节**（UTF-32）。
- 实测宏：`__SIZEOF_WCHAR_T__ = 2`。

**6. `__cplusplus` 宏的值**

本机实测（`-std=c++23`）：

| | 值 |
|---|---|
| GCC 15.3.0 | `202302` |
| GCC 13.1.0 | **`202100`** |
| Clang 22.1.8 | `202302` |

**同一 `-std=c++23` 下 GCC 13 报 202100、GCC 15 报 202302。**
- MSVC（文档，Microsoft Learn `/Zc:__cplusplus` 页原文）："**默认情况下，Visual Studio 始终为 `__cplusplus` 预处理器宏返回值 199711L**"，需显式加 `/Zc:__cplusplus` 才报新值。
- 这是"用 `__cplusplus` 做特性检测"最经典的翻车点。

**7. `std::vector` 扩容因子**

本机实测（libstdc++，三编译器共用同一份 libstdc++）：`push_back` 40 次，capacity 序列 = **`1 2 4 8 16 32 64`** → **2 倍增长**。
- MSVC STL（文档/社区共识）：**1.5 倍**。
- 结论：`vector` 的 `capacity()` 是**可观测的**，所以"扩容因子不同"会让同一程序的 `capacity()` 输出不同——**但这是标准未规定的实现细节，不是 bug**。

**8. `sizeof(std::string)` 与 SSO 阈值**

本机实测：`sizeof(std::string) = 32`（libstdc++）。
- libc++（文档/社区共识）：**24 字节**，SSO 阈值 22 字符。
- libstdc++：32 字节，SSO 阈值 15 字符。
- MSVC STL（文档/社区共识）：**32 字节**，SSO 阈值 15 字符。
- 后果：`sizeof(std::string)` 出现在 ABI 边界上会导致**跨库二进制不兼容**（见第 20 条）。

**9. 严格别名优化（strict aliasing）**

```cpp
int reorder(unsigned* foo){ *foo = 0; short* ptr=(short*)foo; *ptr=1; return *foo; }
```

本机实测：

| | `-O0` | `-O1` | `-O2` | `-O3` | `-Os` |
|---|---|---|---|---|---|
| GCC 15.3.0 | 1 | 1 | **0** | — | — |
| GCC 13.1.0 | 1 | 1 | **0** | — | — |
| Clang 22.1.8 | 1 | 1 | **1** | — | — |

**GCC 在 `-O2` 下真的 miscompile（返回 0），Clang 不利用这条假设（返回 1）。** 加 `-fno-strict-aliasing` 后 GCC 恢复为 1（本机实测）。

**汇编级证据（本机 `-S` 实测，GCC 15.3.0，x86-64）**——这是本文件最硬的一条证据：

```
# g++ -std=c++23 -O2 -S t_sa.cpp     ← 错误版本
_Z7reorderPj:
        xorl    %eax, %eax          ; 返回 0（错！源码期望 1）
        movl    $1, (%rcx)          ; 只发出一条 4 字节存储，把 *foo=0 与 *ptr=1 合并了
        ret

# g++ -std=c++23 -O2 -fno-strict-aliasing -S t_sa.cpp   ← 正确版本
_Z7reorderPj:
        movl    $1, %eax            ; 返回 1（正确）
        movl    $1, (%rcx)
        ret
```

两条指令的差异就说明了全部问题：`-O2` 下 GCC 认定"`short*` 的写"不会影响"`unsigned*` 的读"，因此把 `return *foo` 当作已知常量 0 折叠掉；同时它又在另一个 pass 里把两次写合并成一条 4 字节存储。**同一个函数里两个优化 pass 对程序的理解互相矛盾**——这正是 Alan Wu 在《How I think about C99 strict aliasing rules》里描述的"the mov and the xor are likely coming from two separate parts of the compiler that don't share the same understanding of our program"。

- 相关真实 bug：**GCC PR 17510**（2004-09，"`-fstrict-aliasing` triggers miscompilation"，reporter `rguenth`，i686-pc-linux-gnu，原文："The testcase is miscompiled using `-O2` ... and works ok adding `-fno-strict-aliasing`"）；**GCC PR 124429**（2026-03-10，"Incorrect code generation for pointer-to-array access under -O2 on x86_64"，GCC 11.3/12.x/13.x 均复现，`-O2 -fno-strict-aliasing` 消失，Clang `-O2` 正确）。
- **`-fno-strict-aliasing` 是 work-around 不是 fix**。GCC 手册原文用词是："To disable optimizations based on alias-analysis for **faulty legacy code**, the option `-fno-strict-aliasing` can be used as a **work-around**"。而 GCC PR 122610（2025-12）证明存在**即使加了 `-fno-strict-aliasing` 仍然复现**的 miscompile（根因在 `ipa-modref` 而非 TBAA）——所以这个逃生舱并不总是有效。
- MSVC（文档）：**MSVC 不实现 C++ 意义上的 strict aliasing 优化**，因此该形态在 MSVC 下通常"看起来正常"——**这会让开发者误以为代码正确**，是"跨编译器差异"里最阴险的一类。

**10. `typeid().name()` 的格式（`unspecified`）**

本机实测（Itanium ABI mangling）：
- `typeid(int).name()` = **`i`**
- `typeid(std::string).name()` = **`NSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE`**
- `typeid(V2).name()` = **`2V2`**

MSVC（文档/社区共识）：`int`、`class std::basic_string<char,...>`（可读格式）。
- 后果：**任何依赖 `typeid().name()` 字符串的日志/序列化/哈希在跨编译器时全部失效**。无 bug 编号（`unspecified`）。

**11. 有符号溢出的"恒真"假设（本机实测 `-O0` 就不一致）**

```cpp
int g(int x){ return x+1 > x; }
```

本机实测 `g(INT_MAX)`：

| | `-O0` |
|---|---|
| GCC 15.3.0 | **1** |
| GCC 13.1.0 | **1** |
| Clang 22.1.8 | **0** |

**注意：这是 `-O0`，没有任何优化。** Clang 在 `-O0` 也把 `x+1 > x` 折叠为 `false`（因为 `x+1` 溢出是 UB，Clang 前端/常量折叠已利用）。
- 无 bug 编号（这是 UB 利用，不是 bug）。

**12. 无副作用死循环的处理**

```cpp
int f(){ for(int i=0;i>=0;i++){} return 42; }
```

本机实测（超时 2 秒判定）：

| | GCC 15.3.0 | GCC 13.1.0 | Clang 22.1.8 |
|---|---|---|---|
| `-O0` | `f=42` exit 0 | `f=42` exit 0 | **超时 exit 124** |
| `-O1` | `f=42` exit 0 | `f=42` exit 0 | **无输出 exit 3** |
| `-O2` | **超时 exit 124** | **超时 exit 124** | 无输出 exit 3 |

C++26 起 "trivial infinite loops" 不再是 UB（Sandor Dargo, 2026-09-16），但本机工具链对 C++23 仍按 UB 处理。**Clang 的 exit=3 机制未反汇编确认，列入盲区。**

**13. 未初始化读取的结果（本机实测，15 配置 → 8 种输出）**

```cpp
int a[10]; int s=0; for(int i=0;i<10;i++) s+=a[i]; printf("s=%d\n", s);
```

| | `-O0` | `-O1` | `-O2` | `-O3` | `-Os` |
|---|---|---|---|---|---|
| GCC 15.3.0 | 297780922 | -25442731 | 1615970530 | -1492990318 | -1492516522 |
| GCC 13.1.0 | 1290687602 | — | 2067748199 | 1373394044 | -1009511281 |
| Clang 22.1.8 | 1946384909 | **0** | **0** | **0** | **0** |

**Clang 在 `-O1` 以上把 `s` 折叠为常量 0。** 无 bug 编号。

**14. 编译器识别宏（本机实测）**

| 宏 | GCC 15.3.0 | Clang 22.1.8 |
|---|---|---|
| `__GNUC__` | **15** | **4**（伪装成 GCC 4.2） |
| `__clang__` | 未定义 | 1 |
| `__MINGW32__` | 1 | 1 |
| `__cplusplus` | 202302L | 202302L |

**Clang 定义 `__GNUC__ = 4`**，因此 `#if __GNUC__ >= 5` 在 Clang 下**为假**——这是最经典的"编译器检测写错"陷阱。MSVC（文档）：只定义 `_MSC_VER`，不定义 `__GNUC__`。

### 【文档组】第 15–30 条

**15. 变长数组 VLA（GCC/Clang 扩展，MSVC 不支持）**
GCC/Clang 在 C 模式与（作为扩展）C++ 模式下支持 `int a[n];`；MSVC 报错。社区问答（CSDN 2025-06-28、2025-12-20）反复出现"VS2022 不支持 VLA"的求助。**这是扩展 vs 无扩展，不是 bug。**

**16. `__int128` / `__int128_t`**
GCC/Clang 提供 128 位整数扩展；MSVC 无对应类型（文档）。**未在本机实测**（未编译验证）。

**17. 两阶段名称查找（two-phase lookup）**
GCC/Clang 严格实现两阶段查找；MSVC 在 `/permissive-` 之前对模板中的非依赖名做了"延迟查找"（MSVC 的非标准扩展），导致依赖模板参数的代码在 MSVC 下能过、在 GCC/Clang 下报错。`/permissive-`（VS2017 15.5+ 默认开启）修复。文档依据：Microsoft Learn `/permissive-` 说明与多篇迁移实践文。

**18. `constexpr` 求值步数上限**
GCC 有 `-fconstexpr-ops-limit`（社区常引默认值 33554432）、`-fconstexpr-loop-limit`（262144）、`-fconstexpr-depth`（512）；Clang 有 `-fconstexpr-steps`（社区常引默认值 1048576）。**本文未在本机实测这些默认值，也未在官方文档中逐字核对——列入盲区。** 结论性表述：**`constexpr` 的"能编译"是编译期资源上限的函数，跨编译器不可移植。**

**19. 属性语法**
GCC/Clang：`__attribute__((packed))`；MSVC：`__declspec(align(n))` / `#pragma pack`。C++11 标准属性（`[[nodiscard]]` 等）三家都支持，但**厂商扩展属性不互通**。本机实测 `__attribute__((packed))` 生效：`struct{char c; int i;}` → 未 packed 时 8 字节、packed 时 **5 字节**（三编译器一致）。

**20. 名称修饰（name mangling）与 ABI**
GCC/Clang 用 **Itanium C++ ABI**（本机实测 `typeid(std::string).name()` = `NSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE`）；MSVC 用自有 mangling。后果：**MSVC 编译的 .obj/.lib 与 MinGW 的 .o/.a 不能互相链接**，这是硬事实。无 bug 编号。

**21. 多重继承的 vtable 布局**
本机实测：`struct MID: MI1, MI2 { int c; }`（两个带虚函数的基类）→ `sizeof(MID) = 32`（两个 vptr + 两个 int 基类成员 + 一个 int = 2×8 + 4 + 4 + padding = 32）。Itanium ABI 在多重继承下**为每个多态基类各放一个 vptr**。MSVC 的布局不同（未实测）。虚拟继承实测 `sizeof(VBase) = 16`。

**22. 空类与空基类优化（EBO）**
本机实测：`sizeof(struct E{}) = 1`（三编译器一致，标准要求 ≥1）；`struct Empty{}; struct D1:Empty{int a;};` → `sizeof(D1) = 4`，即 **EBO 生效**（空基类不占空间）。三编译器一致。

**23. `#pragma pack` 与对齐**
本机实测 `sizeof(struct{char c; double d;}) = 16`（三编译器一致，默认 8 字节对齐）。MSVC（文档）默认 `#pragma pack(8)`，与 GCC/Clang x86-64 一致；但 **ARM 上的默认对齐规则不同**，未实测。

**24. 警告 flag 命名与措辞（本机实测）**
同一行 `i = i++ + ++i;`：
- GCC 15.3.0：`warning: operation on 'i' may be undefined [-Wsequence-point]`（同一行报 **4 次**）
- Clang 22.1.8：`warning: multiple unsequenced modifications to 'i' [-Wunsequenced]`（报 **1 次**）

**两家用不同的 flag 名（`-Wsequence-point` vs `-Wunsequenced`）、不同的措辞、不同的重复次数。** 这是阙疑"警告归一化"层必须解决的第一个问题。

**25. 严格别名违规的警告覆盖（本机实测）**
对第 9 条的 `reorder` 例，`-O2 -Wall -Wextra` 下 **GCC 与 Clang 均未输出任何警告**（本机实测，stderr 为空）。因此"靠警告抓严格别名"在本机不可行；唯一可用手段是 `-O0`/`-O2` 输出分歧 + `-fno-strict-aliasing` 二分。

**26. `std::regex` 的实现差异**
libstdc++ / libc++ / MSVC STL 三套独立实现，性能差异可达数量级（社区广泛报告，**本文未找到一手基准数字，列入盲区**）。结论性表述：**`std::regex` 的行为（尤其 `\d`、字符类、`std::regex_constants` 默认）在跨实现时可能不同。**

**27. `std::sort` 的稳定性与最坏复杂度**
标准不要求 `std::sort` 稳定；libstdc++ 用 introsort（保证 O(N log N)），libc++ 也用 introsort，MSVC 用 introsort 变体。**三者的"元素相等时的相对顺序"都可能不同，且都不是 bug。**

**28. `long long` 在 C++98 模式下的可用性**
GCC/Clang 在 `-std=c++98` 下把 `long long` 作为扩展支持（可能有警告）；MSVC 一直支持。**未在本机实测**（未验证警告行为）。

**29. `printf` 格式与 CRT 差异（Windows 特有）**
MinGW-w64 有 `msvcrt`（旧）与 `ucrt`（新）两套 C 运行时；`%zu`、`%lld` 在旧 msvcrt 上可能不被支持（社区广泛报告的 `%I64u` 替代方案）。本机实测：GCC 15.3.0 是 **`x86_64-msvcrt-posix-seh`**（msvcrt 版），`%zu` 与 `%lld` **均正常输出**（`%zu test: 42`、`%lld test: 1099511627776`）。MSVC（文档）：现代版本支持 `%zu`。

**30. `nullptr` 传入可变参数（`...`）**
`printf("%p", nullptr)` 是 UB（`nullptr_t` 不是 `void*`）；GCC/Clang 有 `-Wformat` 警告，MSVC 有 `/analyze`。**未在本机实测。** 相关规范：`[expr.call]` 关于"未定义参数类型"的规定。

### 附：本机预定义宏原始实测（可复算）

```
GCC 15.3.0 : __GNUC__=15  __MINGW32__=1 __MINGW64__=1 __SIZEOF_LONG__=4
             __SIZEOF_WCHAR_T__=2 __cplusplus=202302L __BYTE_ORDER__=__ORDER_LITTLE_ENDIAN__
Clang 22.1.8: __GNUC__=4  __clang__=1 __MINGW32__=1 __MINGW64__=1 __SIZEOF_LONG__=4
             __SIZEOF_WCHAR_T__=2 __cplusplus=202302L __BYTE_ORDER__=__ORDER_LITTLE_ENDIAN__
```

### 附：配置指纹补测（本机实测，GCC 15.3.0 与 Clang 22.1.8 完全一致）

| 探针 | GCC 15.3.0 | Clang 22.1.8 | 说明 |
|---|---|---|---|
| `sizeof(long long)` / `alignof(long long)` | 8 / 8 | 8 / 8 | 一致 |
| `alignof(double)` | 8 | 8 | 一致 |
| `alignof(long double)` | **16** | **16** | x87 80 位，对齐到 16 |
| `alignof(max_align_t)` | 16 | 16 | 一致 |
| `sizeof(char8_t)` | 1 | 1 | 一致 |
| `CHAR_BIT` | 8 | 8 | 一致 |
| `CHAR_MIN` | **-128** | **-128** | 即 `char` 为 signed |
| `EOF` | -1 | -1 | 一致 |
| `sizeof(struct{})`（空类） | 1 | 1 | 标准要求 ≥1 |
| `sizeof(struct{char c; double d;})` | 16 | 16 | 含 7 字节 padding |
| `sizeof(struct{char c; int i;} __attribute__((packed)))` | **5** | **5** | packed 生效 |
| `sizeof(多继承双虚基类派生类)` | **32** | **32** | 2 个 vptr + 3 个 int + padding |
| `sizeof(虚继承派生类)` | 16 | 16 | 虚拟基类 |
| `sizeof(std::string)` | 32 | 32 | libstdc++ |
| `vector` capacity 序列（40 次 push_back） | 1 2 4 8 16 32 64 | 1 2 4 8 16 32 64 | 2 倍增长 |
| `typeid(int).name()` | `i` | `i` | Itanium mangling |
| `typeid(std::string).name()` | `NSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE` | 同左 | Itanium mangling |

**这张表本身就是一个结论**：**在"同一个 OS + 同一个 ABI + 同一份标准库（libstdc++）"的前提下，GCC 与 Clang 的差异极小**。真正制造差异的是三件事——(1) 优化档（第 9、11、12、13 条）、(2) **标准库实现**（libstdc++ vs libc++ vs MSVC STL，第 7、8 条）、(3) **OS/ABI**（LLP64 vs LP64，第 3、4、5 条）。

**因此"GCC vs Clang 差异"这个提法本身就是误导**：本机 15 个配置里，绝大部分差异来自"档位"和"标准库"，而不是"编译器品牌"。**阙疑的元数据模型应该以 `(os, arch, abi, stdlib, compiler, version, opt)` 七元组为键，而不是以编译器品牌为键。**

### 附：本文件实测的复现命令（可独立验证）

```bash
# 环境
G15="C:/Qt/Tools/mingw1530_64/bin/g++.exe"     # GCC 15.3.0
G13="C:/Qt/Tools/mingw1310_64/bin/g++.exe"     # GCC 13.1.0
C22="/c/msys64/mingw64/bin/clang++.exe"        # Clang 22.1.8

# 第 9 条（严格别名 miscompile）
$G15 -std=c++23 -O2 t_sa.cpp -o sa.exe && ./sa.exe          # → reorder=0（错）
$G15 -std=c++23 -O2 -fno-strict-aliasing t_sa.cpp -o sa.exe && ./sa.exe   # → reorder=1
$C22 -std=c++23 -O2 t_sa.cpp -o sa.exe && ./sa.exe          # → reorder=1（Clang 不利用）

# 第 1 条（实参求值顺序）
$G15 -std=c++23 -O0 t_arg.cpp -o a.exe && ./a.exe           # → arg order=CBA
$C22 -std=c++23 -O0 t_arg.cpp -o a.exe && ./a.exe           # → arg order=ABC

# 第 14 条（编译器识别宏）
$C22 -std=c++23 -dM -E -x c++ /dev/null | grep -E "__GNUC__|__clang__"
```

---

## 对阙疑的 3 条具体行动

**行动 1（立即可做）：把 `compiler` / `platform` 元数据字段从"枚举值"升级为"完整配置串"，并回填到 37 张实卡。**
- 现状：26 张 verified 卡在批次 663 C1 补了 `cpp_standard` / `compiler` / `platform` / `input_domain` 四个 semantic scope 字段（见 `git log` 中 `6045e4fb`）。
- 改法：`compiler` 字段的取值域从 `{gcc, clang, msvc}` 改为 `{gcc-15.3.0-mingw-x86_64-msvcrt-posix-seh, clang-22.1.8-mingw-x86_64-gnu, ...}`；`platform` 至少含 `os` + `arch` + `abi`（`llp64` vs `lp64`）。
- 依据：本文件第 3、4、6 条证明 **同一编译器家族不同版本就产生不同答案**（GCC 13 的 `__cplusplus=202100` vs GCC 15 的 `202302`）。
- 验收：`data/_gate_rules.json` 中新增一条 `advice` 级规则 `META-CONFIG-001`："判决证据若引用 `sizeof` / `__cplusplus` / `capacity()` / 浮点结果，必须带完整配置串"。

**行动 2（1 天内）：新增 3 条 block 规则覆盖本文件实测的"跨编译器不一致"。**
- `XCC-EVALORD-001`：单一函数调用实参中出现 2 个以上带副作用的表达式（对应第 1 条，GCC `CBA` vs Clang `ABC`）→ block。
- `XCC-CHAR-SIGN-001`：对 `char` 做 `< 0` / `>= 128` 之类依赖符号的比较或索引（对应第 2 条）→ warn。
- `XCC-MACRO-DETECT-001`：`#if __GNUC__ >= N` 且同文件未同时检测 `__clang__`（对应第 14 条，Clang 定义 `__GNUC__=4`）→ block。
- 每条配 1 个 positive fixture（本文件对应代码）+ 1 个 negative fixture（修复版）。

**行动 3（3 天内）：把"15 配置矩阵"固化为可复算资产，作为论文的独立证据来源。**
- 写 `tools/xcc_matrix_<batch>.py`，对第 1、2、3、4、5、6、7、8、9、11、12、13 条的 12 个源文件，在 `{GCC15.3.0, GCC13.1.0, Clang22.1.8} × {-O0,-O1,-O2,-O3,-Os}` = 15 配置下编译运行，输出 `data/xcc_matrix.json`（含 stdout、exit code、stderr 警告数）。
- 论文写法：§Evaluation 新增一张表 "同源异构：12 个跨编译器敏感程序 × 15 配置"，报告"12 个程序中 N 个在配置间输出不一致"——**这是"外部效度优先"叙事最强的实证**，因为它不依赖任何内部指标，任何人可独立复算。
- 诚实边界：MSVC 一栏空缺，必须在 §Threats to Validity 明写"本研究的跨编译器结论仅覆盖 GCC 与 Clang，MSVC 数据来自文档"。

---

## 盲区（诚实标注）

1. **本机无 MSVC，所有 MSVC 结论均为文档依据，非实测。** 涉及第 3、4、5、6、9、10、15、16、17、18、23、27、29、30 条的 MSVC 栏。
2. **无 ARM 工具链**，第 2 条（ARM 默认 `char` unsigned）与第 23 条（ARM 对齐规则）未实测。
3. **第 12 条 Clang `exit=3` 的机制未确认**（未反汇编；推测为 UB 利用后的 `unreachable`/trap 路径）。
4. **第 18 条 `constexpr` 步数默认值未实测、未在官方文档逐字核对**，仅引社区常见数字，**不建议直接引用**。
5. **第 26 条 `std::regex` 性能差异没有一手基准数字**，本文不写任何倍数。
6. **第 16、28、30 条未实测**（未编译验证），仅作为"已知差异清单项"列出。
7. **第 7、8 条的 libc++ / MSVC STL 数字来自社区共识（CSDN、博客园、知乎多篇一致），未找到标准或官方文档级别的权威来源。** 标注为"社区共识"。
8. **"top 30" 的排序是本调研的主观排序**（按"实测可得性 × 工程影响面"排），不是任何统计意义上的 top 30。真实的差异清单远超 30 条（仅 GCC 手册的 "Implementation-Defined Behavior" 章节就列出上百条）。

---

## 来源

1. 本机实测（GCC 15.3.0 / GCC 13.1.0 / Clang 22.1.8，2026-09-29），源文件与输出见 `_tmp/exp/`（工作副本，不进入仓库）
2. GCC 手册 "Characters implementation" — https://gcc.gnu.org/onlinedocs/gcc/Characters-implementation.html
3. Microsoft Learn, `/Zc:__cplusplus`（"默认返回值 199711L"原文） — https://learn.microsoft.com/zh-cn/cpp/build/reference/zc-cplusplus?view=msvc-170
4. Microsoft Learn, `char、wchar_t、char8_t、char16_t、char32_t` — https://learn.microsoft.com/zh-cn/cpp/cpp/char-wchar-t-char16-t-char32-t?view=msvc-170
5. Microsoft Learn, 数据类型范围 — https://learn.microsoft.com/zh-cn/cpp/cpp/data-type-ranges?view=msvc-170
6. GCC PR 17510（2004-09）"-fstrict-aliasing triggers miscompilation" — https://gcc.gnu.org/pipermail/gcc-bugs/2004-September/131032.html ；https://gcc.gnu.org/bugzilla/show_bug.cgi?id=17510
7. GCC PR 124429（2026-03-10）"Incorrect code generation for pointer-to-array access under -O2 on x86_64" — https://gcc.gnu.org/pipermail/gcc-bugs/2026-March/951019.html
8. GCC PR 122610（2025-12）"[13/14/15/16 regression] Load after store incorrectly deleted with -O2 -fno-strict-aliasing" — https://gcc.gnu.org/pipermail/gcc-bugs/2025-December/938061.html
9. GCC PR 105598（2022-05）"Flag -O2 causes code to misbehave"（gcc 11.1/11.2/11.3 输出 2 而非 4） — https://gcc.gnu.org/pipermail/gcc-bugs/2022-May/786963.html
10. Stack Overflow, "New Sequence Points in C++11"（`[intro.execution]/15` 原文） — https://stackoverflow.com/a/19069981
11. Sandor Dargo, "C++26: Trivial infinite loops are no longer undefined behaviour", 2026-09-16 — https://www.sandordargo.com/blog/2026/09/16/cpp26-trivial-infinite-loops
12. 社区共识：`std::vector` 扩容因子 1.5×（MSVC）vs 2×（libstdc++/libc++） — https://yunpan.plus/t/20358-1-1 ；https://limuran.top/p/cpp-vector-capacity-growth-strategy/
13. 社区共识：`sizeof(std::string)` 32（libstdc++/MSVC STL）vs 24（libc++） — https://www.tskau.com/docs/content/3336.html ；https://jishuzhan.net/article/2085891285113520130
14. Alan Wu, "How I think about C99 strict aliasing rules"（GCC `-O2` 与 `-fno-strict-aliasing` 汇编对照） — https://www.alanwu.space/post/strict-aliasing
15. 腾讯云开发者社区, "gcc 编译参数 -fno-strict-aliasing" — https://cloud.tencent.com/developer/article/1159055
16. 本项目自有 UB 反例库（跨编译器 miscompile 分歧、无 sanitizer 运行时的环境声明） — https://liaoranran.github.io/CPP-Bible/Appendix/ub/
17. Microsoft Learn, `/permissive-`（两阶段查找合规） — https://codechina.net/article/weixin_33700809/294569
18. Shafik Yaghmour, "What You Need to Know when Optimizations Changes the Behavior of Your C++", 2025-02-11 — https://shafik.github.io/c++/undefined%20behavior/llvm/2025/02/11/when-opt-changes-program-behavior.html
