# C3 类型系统：整数、浮点、指针与隐式转换陷阱

> 参考：《C 语言极致详解手册》。编译器 GCC 15.3.0（`gcc -std=c11 -O2 -Wall -Wextra`），所有输出为真实运行/编译产物。
> 示例源：`c/_demo/c3_types.c`

## ① 我们真正要回答的问题 <span class="badge badge-std">标准</span>

1. `long` 到底是几个字节？为什么 Windows 和 Linux 不一样？
2. 为什么 `-1 < 1u` 的结果是 **false**？
3. 数组名什么时候是数组、什么时候是指针？为什么函数里的 `sizeof(arr)` 拿不到数组长度？
4. 为什么 `0.1 + 0.2 != 0.3`？

先给判断：**C 的类型系统「宽度不保证、转换很积极」。** C 里绝大多数诡异 bug，根源都是「你以为的类型」与「编译器按转换规则实际使用的类型」不一致。本章把这层规则摊开看。

## ② 基本类型尺寸：标准只保下限，不保确切宽度

真实输出（本机 MinGW GCC 15.3.0，64 位 Windows）：

```text
== sizeof (LLP64) ==
char=1 short=2 int=4 long=4 long long=8
float=4 double=8 void*=8 size_t=8
```

| 类型 | 本机（Windows / MinGW） | Linux x86-64 | 说明 |
|------|------------------------|--------------|------|
| `char` | 1 | 1 | 标准保证 `sizeof(char) == 1` |
| `short` | 2 | 2 | ≥ 16 位 |
| `int` | 4 | 4 | ≥ 16 位（实际几乎都是 32） |
| `long` | **4** | **8** | ⚠️ 不同！标准只保证 ≥ 32 位且 ≥ `int` |
| `long long` | 8 | 8 | ≥ 64 位 |
| `void *` | 8 | 8 | 64 位平台指针 8 字节 |
| `size_t` | 8 | 8 | 无符号，`sizeof` 的返回类型 |

差异来自**数据模型**（data model）：

| 模型 | `int` | `long` | 指针 | 典型平台 |
|------|-------|--------|------|----------|
| ILP32 | 32 | 32 | 32 | 32 位 Linux/Windows |
| **LP64** | 32 | **64** | 64 | **Linux / macOS（64 位）** |
| **LLP64** | 32 | **32** | 64 | **Windows（含 MinGW）** |

> 立场：[标准] C 标准**从不规定** `int`/`long` 的确切字节数，只规定最小取值范围与 `sizeof(char) == 1`。所以「`long` 是 8 字节」只是 Linux 上的经验，不是语言事实。需要确定宽度就用 `<stdint.h>` 的 `int32_t` / `uint64_t` / `intptr_t`。这条与 Part0 A5 的「`struct { long; }` 跨平台尺寸不同」是同一件事的两面。

> 立场：[经验] 工程后果很直接：**跨进程/跨机器传输的结构体里不要用 `long`**（它的宽度会变）；序列化、网络协议、文件格式一律用 `<stdint.h>` 定宽类型。C6 讲对齐时还会再撞上这个问题。

## ③ 整数提升与通常算术转换

两个必须分清的转换：

1. **整数提升**（integer promotion）：`char`、`short`、`_Bool`、位域这类「比 `int` 窄」的类型，参与运算前先提升为 `int`（若 `int` 装不下则提升为 `unsigned int`）。
2. **通常算术转换**（usual arithmetic conversions）：两个操作数类型不同时，把较窄的一侧转成较宽的一侧，使两边同类型再运算。

真实输出：

```text
== integer promotion ==
sizeof(char)=1  sizeof(c+d)=4  c+d=200
```

`c` 和 `d` 都是 `char`（各占 1 字节），但 `c + d` 的类型是 **`int`**（4 字节），所以 `100 + 100 = 200` **不会**在 `char` 里溢出成负数——因为加法发生在 `int` 域。这就是整数提升在背后救了你一次。

而「通常算术转换」里那条**致命分支**在下节。

## ④ 陷阱 1：有符号 / 无符号混用（`-1 < 1u` 为 false）

真实输出与编译警告：

```text
== signed/unsigned trap ==
-1 < 1u ? false
(unsigned)(-1) = 4294967295
```

```text
c3_types.c:34:33: warning: comparison of integer expressions of different signedness:
                 'int' and 'unsigned int' [-Wsign-compare]
```

规则：当一侧是无符号、另一侧是有符号，且**无符号那侧的等级不低于有符号侧**时，**有符号值被转换成无符号**。`-1` 于是变成 `4294967295`（`UINT_MAX`），自然不小于 `1`。

它咬人的三种常见形态：

| 写法 | 问题 |
|------|------|
| `if (strlen(s) - 1 < 0)` | `strlen` 返回 `size_t`，减 1 下绕成巨大正数，条件**永不成立** |
| `for (size_t i = n - 1; i >= 0; --i)` | `i >= 0` 对无符号**恒真** → 无限循环 |
| `int len = strlen(s);` | 大字符串时 `size_t` → `int` 可能截断为负 |

正确写法（倒序遍历无符号下标）：

```c
for (size_t i = n; i-- > 0; ) {   /* 习惯用法：先判断后自减，天然无下绕 */
    /* 使用 i，范围 n-1 .. 0 */
}
```

> 立场：[标准] 这条规则出自 N1570 6.3.1.8，不是「某个编译器的怪癖」——所有合规实现都这样。GCC 的 `-Wsign-compare`（由 `-Wextra` 打开）能抓到直接的比较，但**抓不到**间接场景（比如 `size_t` 减法后再比较），所以不能只依赖警告。

## ⑤ 陷阱 2：数组退化，以及函数参数里的「假数组」

**退化规则**：数组名在绝大多数表达式中会退化为指向首元素的指针（即 `a` → `&a[0]`）。只有三种例外：`sizeof(a)`、`&a`、以及用字符串字面量初始化 `char[]`。

真实输出：

```text
== array decay ==
sizeof(a)=20 (数组本身)  sizeof(p)=8 (退化后的指针)
inside probe: sizeof(arr)=8 (已退化为指针，[5] 无意义)
```

编译警告：

```text
c3_types.c:12:18: warning: 'sizeof' on array function parameter 'arr'
                 will return size of 'int *' [-Wsizeof-array-argument]
```

**最坑的是函数参数**：`void probe(int arr[5])` 中的 `[5]` 是**给人看的注释**，编译器把它完全当作 `int *arr`。所以函数内部 `sizeof(arr)` 得到的是指针大小（8），**永远拿不到数组长度**。

这正是 C 里 `void f(int *arr, size_t n)` 这一惯用法的由来——长度必须显式另传。它也是现代 C++ 引入 `std::span`（带长度的视图）和 `std::array`（不退化）的直接动因（见主书 part07）。

> 立场：[经验] 判断依据：在函数里看到「数组参数」时，一律当成指针。任何想在函数内用 `sizeof(arr)/sizeof(arr[0])` 求长度的写法都是错的，而 GCC 的 `-Wsizeof-array-argument` 会直接替你抓出来。

## ⑥ 陷阱 3：整数除法截断

```text
== integer division ==
1/2 = 0 ; 1.0/2 = 0.5
```

只要**两个操作数都是整数**，除法就执行整数除法并直接截断小数部分。想保留小数，让至少一个操作数是浮点（`1.0/2`、`(double)a/b`）。

经典 bug：算百分比 `percent = a / b * 100;` ——`a/b` 先截断成 0，结果永远是 0。应先乘后除，或转浮点。

## ⑦ 陷阱 4：浮点无法精确表示十进制小数

```text
== float precision ==
0.1+0.2 == 0.3 ? false
0.1+0.2 = 0.30000000000000004
```

原因：`0.1` 在二进制浮点（IEEE-754 双精度）里是**无限循环小数**，只能存近似值；两个近似值相加的误差不再是 `0.3` 的近似值。

对策：

- **不要用 `==` 直接比较浮点**，改用容差：`fabs(x - y) < 1e-9`；
- 金额、计数一类需要精确十进制的场景，用整数（如「分」）代替浮点；
- **不要用浮点变量做循环计数器**（累加误差会让循环次数出错）。

## ⑧ 陷阱 5：`char` 的符号性是实现定义的

```text
== char signedness (implementation-defined) ==
(signed char)200 = -56
```

- 普通 `char` 到底是有符号还是无符号，**标准交给实现决定**：x86 上的 GCC 默认是 `signed`，而部分 ARM 工具链默认是 `unsigned`。
- 本例中 `signed char sc = 200;` 在 `-Wall -Wextra` 下**没有任何警告**（本章这两条选项只报出了 `-Wsign-compare` 与 `-Wsizeof-array-argument`），要靠 `-Wconversion` 才会提示——这也是它格外危险的原因。

对策：需要符号就明确写 `signed char` / `unsigned char`；处理**字节**一律用 `unsigned char`；跨平台代码用 `<stdint.h>` 的 `int8_t` / `uint8_t`。

## ⑨ 防御清单（可直接抄进项目）

1. **用定宽类型**：`<stdint.h>` 的 `int32_t` / `uint64_t` / `intptr_t`，以及 `size_t` 表示尺寸。
2. **打开更严的警告**：`-Wall -Wextra -Wconversion -Wsign-conversion`。本章示例在 `-Wall -Wextra` 下已经真实抓出两条（`-Wsign-compare`、`-Wsizeof-array-argument`），加上 `-Wconversion` 还能抓到窄化赋值。
3. **有符号与 `size_t` 比较前显式转换**，并先做范围检查。
4. **倒序无符号循环**用 `for (size_t i = n; i-- > 0; )`。
5. **浮点比较用容差**；金额用整数；浮点不做循环计数器。
6. **数组传参必须同时传长度**（`f(int *arr, size_t n)`），别指望 `sizeof`。

## ⑩ 小结与路线图

C 的类型系统给的是「最小保证 + 积极转换」：宽度不保证（所以 `long` 跨平台会变、要用定宽类型），转换很积极（所以 `-1 < 1u` 会翻车、数组会退化、整数除法会截断、浮点会失精）。这些规则在编译期就已决定，却要到运行期才咬人。

下一章（C4）进入函数：调用约定、栈帧的实况，以及变参函数 `stdarg` 为什么是类型不安全的典型。

## 参考引用

- `[std-c11]`（N1570，本地 `docs/references/external/standards/N1570_C11.pdf`）：6.2.5 类型、6.3.1.1 整数提升、6.3.1.8 通常算术转换、6.3.2.1 左值与数组退化、7.20 `<stdint.h>`。
- `[cppref:c/language/conversion]`：隐式转换规则（离线 cppreference，`C:\Users\ASUS\Desktop\cppb参考资料\cppreference\`）。
- `[cert:INT02-C]` 理解整数转换规则；`[cert:FLP30-C]` 不要用浮点变量做循环计数器（CERT 为在线源，本机 403 未本地化）。
- `[gcc:mingw-w64]`：本机数据模型为 LLP64（`long` 4 字节、指针 8 字节）。
- 交叉引用：Part0 `asm/asm05_data_layout.md`（结构体字段偏移与对齐）、`asm/asm03_stack_abi.md`（Microsoft x64 调用约定）。
