# 648 · C 标准原文抓取（C11/C17/C23）

| 标准 | 文档 | ISO | 形式 | 下载 | 字节 | sha256（前 16） |
|---|---|---|---|---|---|---|
| C11 | N1570 | ISO/IEC 9899:2011 | html | ✅ | 1972999 | `356d916a27ef5d52…` |
| C17 | N2310 | ISO/IEC 9899:2018 | pdf | ✅ | 2531740 | `6a01dfbfd271a2b6…` |
| C23 | N3096 | ISO/IEC 9899:2024 | pdf | ✅ | 3459096 | `a1262b7d5d2ab0e4…` |

## 抽取到的条款（**逐字来自 N1570**，带字节偏移可复核）

| 卡 | 条款 | 主题 | 命中方式 | 偏移 | 原文（截断） |
|---|---|---|---|---|---|
| decay | 6.7.6.3p7 | 数组形参退化为指针 | anchor | 415081 | A declaration of a parameter as ''array of type'' shall be adjusted to ''qualified pointer to type'', where the type qualifiers (if any) are those specified within the [ and ] of t |
| malloc | 7.22.3.3p2 | free(NULL) 是空操作；free 不清空指针 | anchor | 958873 | The free function causes the space pointed to by ptr to be deallocated, that is, made available for further allocation. If ptr is a null pointer, no action occurs. Otherwise, if th |
| strbound | 7.21.6.5p3 | snprintf 返回值是'本该写入的长度' | anchor | 898708 | The snprintf function returns the number of characters that would have been written had n been sufficiently large, not counting the terminating null character, or a negative value  |
| fnptr | 6.5.2.2p9 | 经不兼容函数指针调用 ⇒ UB | anchor | 274411 | If the function is defined with a type that is not compatible with the type (of the expression) pointed to by the expression that denotes the called function, the behavior is undef |
| volatile | 6.7.3p7 | volatile：什么算一次访问是实现定义 | anchor | 380807 | An object that has volatile-qualified type may be modified in ways unknown to the implementation or have other unknown side effects. Therefore any expression referring to such an o |
| setjmp | 7.13.2.1p3 | longjmp 后非 volatile 局部变量值不确定 | anchor | 733616 | All accessible objects have values, and all other components of the abstract machine 249) have state, as of the time the longjmp function was called, except that the values of obje |
| intpromo | 6.3.1.8p1 | 常用算术转换：有符号/无符号比较 | anchor | 196616 | Many operators that expect operands of arithmetic type cause conversions and yield result types in a similar way. The purpose is to determine a common real type for the operands an |
| bitfield | 6.7.2.1p11 | 位域分配顺序/对齐是实现定义 | anchor | 359259 | An implementation may allocate any addressable storage unit large enough to hold a bit- field. If enough space remains, a bit-field that immediately follows another bit-field in a  |
| macro | 6.10.3.1p1 | 宏实参先展开再替换（故括号与副作用由使用者负责） | anchor | 505977 | After the arguments for the invocation of a function-like macro have been identified, argument substitution takes place. A parameter in the replacement list, unless preceded by a # |
| signedovf | 6.5p5 | 表达式结果超出可表示范围 ⇒ UB | anchor | 257122 | If an exceptional condition occurs during the evaluation of an expression (that is, if the result is not mathematically defined or not in the range of representable values for its  |

**命中 10/10**。

## 诚实登记

- C17（N2310）是 PDF，本环境无 PDF 解析库 ⇒ 只留下载留痕（bytes=2531740、sha256=6a01dfbfd271a2b6…），**未抽取原文、未核对条款号**。人核命令：用任意 PDF 阅读器打开 https://www.open-std.org/jtc1/sc22/wg14/www/docs/n2310.pdf 并检索 C11 对应条款号。
- C23（N3096）是 PDF，本环境无 PDF 解析库 ⇒ 只留下载留痕（bytes=3459096、sha256=a1262b7d5d2ab0e4…），**未抽取原文、未核对条款号**。人核命令：用任意 PDF 阅读器打开 https://www.open-std.org/jtc1/sc22/wg14/www/docs/n3096.pdf 并检索 C11 对应条款号。
- 卡的 `sources[]` 只写**能机器核对的** N1570（C11）条款；C17 与 C23 **不写条款号**（本批未核对），只登记在 `claim_boundary.standard` 的实测范围里。
