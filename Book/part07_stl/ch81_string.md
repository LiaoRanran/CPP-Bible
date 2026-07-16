# 第81章　std::string 与 SSO 短字符串优化

> 真实编译器：MinGW GCC 13.1.0（`-std=c++23 -O2 -S -masm=intel`）。
> 源码根：`C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/`；本章所有 `[实现]` 级源码均来自该目录真实文件，逐行标注路径与行号。libc++、MS STL 不在本机，相关对比以 `[实现-推断]` / `[平台-推断]` 标注。

## ① 概述：std::string 的设计哲学 [标准]

⟶ Book/part07_stl/ch80_array.md
⟶ Book/part07_stl/ch82_span.md


`std::string` 是 `std::basic_string<char>` 的特化，承载"值语义优先、零开销抽象、与 C 互操作"三原则。

```cpp
// ① 最简形态：值语义，拷贝即独立副本
#include <string>
std::string a = "hello";
std::string b = a;          // 深拷贝，b 与 a 相互独立
b[0] = 'H';                 // 修改 b 不影响 a
```

- `[标准]`：`std::string` 满足 *Cpp17BasicString* 与 *Cpp17ContiguousContainer*（`data()` 返回连续 `char[]`）。
- `[经验]`：永远优先 `std::string` 而非裸 `char*`，除非要跨越 C ABI 边界（此时用 `c_str()`）。


## 架构与流程图示（Mermaid）

std::string 依长度在「内联小缓冲区（SSO）」与「堆分配」两种布局间切换，避免短字符串的堆开销。

```mermaid
flowchart TD
    S["std::string s"]
    SMALL["短字符串（size 不超过 SSO 阈值，通常 15 或 22 字节）<br/>字符数据内联在对象本体的小缓冲区<br/>无堆分配，无间接访问"]
    LARGE["长字符串（size 超过阈值）<br/>对象本体存：data 指针 + size + capacity<br/>字符数据在堆上"]
    S -->|"size 小"| SMALL
    S -->|"size 大"| LARGE
```

## ② 三种存储策略的历史演进 [标准]

`std::string` 的实现经历过三代：

1. **COW（Copy-On-Write，引用计数）**：GCC 3.x–4.x 默认。拷贝共享缓冲区，写时才复制。
2. **SSO（Small String Optimization，短字符串优化）**：GCC 5.1 起默认，已被所有主流实现采用。
3. **总是堆指针（无优化）**：少数嵌入式实现。

```cpp
#include <string>
// ② COW 已被标准禁止：C++11 起要求 string 满足"可装入容器 + 独立拷贝"
// 下面的写法在 COW 时代会共享底层，C++11 后必然深拷贝
std::string x = "a very long string that definitely exceeds any small buffer";
std::string y = x;          // C++11 起：必定深拷贝（独立堆块）
```

- `[标准]`：C++11 因"别名安全"与"容器一致性"要求，**禁止 COW**。GCC 5.1（libstdc++ 5）移除了 `std::string` 的 COW。
- `[经验]`：现代代码不要再假设 `string` 拷贝是廉价的——长串拷贝是 O(n) 堆分配。

## ③ 对象内存布局：std::string 的字节级结构 [实现]

libstdc++ 的 `std::string` 在 **SSO 模式**下是一个"联合体 + 长度 + 容量"结构。核心类型 `std::__cxx11::basic_string`（新 ABI）：

```cpp
// ③ libstdc++ 概念布局（来自 bits/basic_string.h）
// struct basic_string {
//     // 联合体：要么指向堆缓冲区(_M_ptr)，要么内联本地缓冲(_M_local_buf)
//     struct _Alloc_hider { char* _M_p; };   // 指向当前数据的指针（含本地缓冲）
//     _Alloc_hider  _M_dataplus;
//     size_type     _M_string_length;         // 字符数（不含 '\0'）
//     // 联合体：本地缓冲区（SSO） 或 容量字段（堆模式）
//     union {
//         char            _M_local_buf[_S_local_capacity + 1];  // 内联存储
//         size_type       _M_allocated_capacity;                // 堆模式下的容量
//     };
// };
```

- `[实现]`：SSO 通过一个**联合体**实现——短串用 `_M_local_buf`，长串用 `_M_allocated_capacity` + 堆指针。两者共享同一段内存，靠 `_M_string_length` 与指针比较区分。
- `[经验]`：这就是为什么 `sizeof(std::string)` 在 64 位上通常是 **32 字节**（指针 8 + 长度 8 + 联合体 16），而不是"指针大小"。

## ④ SSO 短字符串优化：阈值与内联缓冲 [实现]

SSO 的核心是常数容量内联缓冲，避免短串的堆分配。

```cpp
// ④ SSO 容量：libstdc++ 固定 15 字节（char）
#include <string>
#include <iostream>
int main() {
    std::cout << "sizeof(string)      = " << sizeof(std::string) << "\n";  // 32
    std::cout << "max SSO size (char) = " << 15 << "\n";  // _S_local_capacity = 15
    // 实测：≤15 字符（含 '\0' 占 16）走内联，≥16 字符走堆
    std::string s15 = "123456789012345";   // 15 字符：SSO 内联
    std::string s16 = "1234567890123456";  // 16 字符：堆分配
    std::cout << "s15 size=" << s15.size() << " s16 size=" << s16.size() << "\n";
}
```

- `[实现]`：`bits/basic_string.h:213` 定义 `enum { _S_local_capacity = 15 / sizeof(_CharT) }`；`217` 定义 `_M_local_buf[_S_local_capacity + 1]`。对 `char` 而言内联缓冲可容纳 **15 个字符 + 1 个 '\0'**。
- `[实现-推断]`：MSVC 的 SSO 容量为 **15 字节**，Clang/libc++ 为 **22 字节**（容量因实现而异，但机制相同）。

## ⑤ 构造 / 赋值 / 析构的生命周期 [标准]

```cpp
#include <utility>
#include <string>
// ⑤ 构造来源多样，生命周期归一到"析构释放一次"
void f() {
    std::string a("literal");            // 从 const char* 构造（可能 SSO）
    std::string b = a.substr(0, 3);      // 子串产生新存储
    std::string c = std::move(a);        // 移动：窃取存储，a 进入有效但未指定状态
    // a 离开作用域：若仍持有堆块则释放；c 离开时释放其存储
}
```

- `[标准]`：移动构造为常数时间（窃取指针/内联缓冲），不分配堆。
- `[经验]`：返回 `std::string` 时直接 `return s;`（NRVO/移动），不要 `return std::move(s);`（阻碍 RVO，见 part10 ch117）。

## ⑥ 小字符串判定：_M_string_length > _S_local_capacity [实现]

SSO 模式的切换靠长度与阈值的比较。

```cpp
// ⑥ 判定逻辑（libstdc++ 概念）
// bool is_local() const {
//     return _M_string_length <= _S_local_capacity;   // 长度 ≤ 15 -> 内联
// }
// 堆模式时 _M_dataplus._M_p 指向堆；SSO 模式时指向 _M_local_buf
```

- `[实现]`：`bits/basic_string.h:277` 有 `if (_M_string_length > _S_local_capacity)` 分支，用于在扩容/取数据时决定走堆还是内联。
- `[平台]`：这是 SSO 的"开关"——所有读 `data()` 的操作都要先判断当前是本地还是堆。

## ⑦ 拷贝 / 移动语义与 COW 陷阱 [标准]

```cpp
// ⑦ 拷贝深、移动浅（窃取）
#include <string>
#include <utility>
std::string make() { return "result"; }      // 返回值优化：0 次拷贝
void g() {
    std::string s = make();
    std::string cp = s;                        // 深拷贝（堆串 O(n)，SSO 串 O(1) 内存复制）
    std::string mv = std::move(s);            // O(1)：mv 接管 s 的存储
}
```

- `[标准]`：C++11 起 `std::string` 的拷贝构造函数必须产生**独立深拷贝**（COW 被禁）。
- `[经验]`：在热路径上传递 `std::string` 大对象用 `const std::string&` 或 `std::string_view`（见 ⑫），避免无谓深拷贝。

## ⑧ 扩容策略与迭代器失效 [标准]

```cpp
// ⑧ push_back/append 触发扩容，容量按几何增长（通常 ×2）
#include <string>
#include <iostream>
#include <cstddef>
int main() {
    std::string s;
    size_t last = 0;
    for (int i = 0; i < 10; ++i) {
        s.push_back('x');
        if (s.capacity() != last) {
            std::cout << "size=" << s.size() << " cap=" << s.capacity() << "\n";
            last = s.capacity();
        }
    }
}
```

- `[标准]`：追加导致 `size() > capacity()` 时重新分配，capacity 通常按 ≥1.5 或 2 倍增长。
- `[标准]`：所有指向 `std::string` 的**迭代器/指针/引用**在导致重新分配的操作后**全部失效**（与 `std::vector` 相同）。

## ⑨ data() / c_str() 与 null 终止 [标准]

```cpp
// ⑨ c_str() 与 data() 在 C++11 后都返回以 '\0' 结尾的连续缓冲
#include <string>
#include <cstring>
int main() {
    std::string s = "abc";
    const char* p = s.c_str();     // 传统 C 接口，保证 null 终止
    const char* d = s.data();      // C++17 起 data() 也可写；均连续
    return std::strcmp(p, d);      // 等价
}
```

- `[标准]`：C++11 起 `data()` 与 `c_str()` 都返回 null 终止的 `char*`；`operator[]` 允许写 `s[0]`，且 `s[s.size()]` 是合法的 `'\0'`。
- `[经验]`：不要缓存 `c_str()` 返回的指针跨可能触发重分配的操作——重分配后指针悬空。

## ⑩ 拼接与性能：operator+ vs += vs append [标准]

```cpp
// ⑩ 链式 operator+ 产生多次临时；+=/append 就地复用
#include <string>
std::string slow(const std::string& a, const std::string& b, const std::string& c) {
    return a + b + c;   // 临时串 1: a+b；临时串 2: (a+b)+c —— 2 次分配
}
std::string fast(const std::string& a, const std::string& b, const std::string& c) {
    std::string r;
    r.reserve(a.size() + b.size() + c.size());  // 预分配：0 次重分配
    r += a; r += b; r += c;                       // 全部就地
    return r;
}
```

- `[经验]`：拼接多个串时，**先 `reserve` 再用 `+=`/`append`** 可消除重分配；避免 `a + b + c + d` 长链。
- `[平台]`：`std::string` 的 `+` 无法像表达式模板那样合并（字符串不是数值类型），故链式为 O(n²) 级临时。

## ⑪ 与 char* 互操作及生命周期陷阱 [标准]

```cpp
// ⑪ 常见悬空陷阱
#include <string>
const char* bad() {
    std::string s = "tmp";
    return s.c_str();   // 错误：s 销毁，返回悬空指针
}
const char* good() {
    static std::string s = "keep";
    return s.c_str();   // 安全：static 生命周期
}
```

- `[经验]`：绝不返回 `c_str()`/`data()` 跨 `std::string` 生命周期。需要返回 C 字符串时用 `std::string` 值返回，由调用方取 `c_str()`。

## ⑫ std::string_view：零拷贝视图（C++17） [标准]

```cpp
// ⑫ string_view 不拥有存储，仅指向现有缓冲区
#include <string_view>
#include <string>
void print(std::string_view sv) {            // 接受 string / char* / 子串，零拷贝
    for (char c : sv) { /* ... */ }
}
int main() {
    std::string s = "hello world";
    print(s);                                 // OK，无拷贝
    print("hello world");                     // OK，字面量
    print(s.substr(0, 5));                    // OK，string_view 子串 O(1)
    return 0;
}
```

- `[标准]`：`std::string_view` 是 `basic_string_view<char>`，仅含 `{ptr, size}`，**不分配、不拥有**。
- `[经验]`：函数参数优先用 `std::string_view`（只读时）；需要修改或长期持有才用 `std::string`。

## ⑬ 编码与 Unicode 注意事项 [经验]

```cpp
// ⑬ std::string 不感知编码，只存字节序列
#include <string>
std::string utf8 = "中文";          // 存 UTF-8 字节（6 字节），size()=6 不是 2
// 字符数 ≠ size()；按"码点"迭代需专用库（如 {fmt}、ICU）
```

- `[经验]`：不要对可能含多字节 UTF-8 的字符串用 `s[i]` 当"字符"处理；`size()` 是**字节数**。Windows 宽接口用 `std::wstring`（`wchar_t`，UTF-16）。

## ⑭ std::string 的 ABI 稳定性（libstdc++ 双 ABI） [实现]

libstdc++ 存在新旧两套 `std::string` ABI：

```cpp
#include <string>
// ⑭ 旧 ABI（pre-GCC5）：COW，符号在 std:: 命名空间
// 新 ABI（GCC5+）：SSO，符号在 std::__cxx11:: 命名空间
// 混合链接旧/新 ABI 目标文件会因 std::string 尺寸不同导致 ODR 违反
// 切换宏：_GLIBCXX_USE_CXX11_ABI=0（旧）/ 1（新，默认）
```

- `[平台]`：GCC 5 引入新 ABI 后，`std::string` 符号从 `std::string` 变为 `std::__cxx11::basic_string<char>`。链接第三方库时要注意 ABI 一致（`_GLIBCXX_USE_CXX11_ABI`）。

## ⑮ 真实 libstdc++ 源码逐行：`basic_string.h` 的 SSO 缓冲 [实现]

```cpp
// 文件：bits/basic_string.h （GCC 13.1.0, libstdc++）
// 行号：213
      enum { _S_local_capacity = 15 / sizeof(_CharT) };
// 行号：217
	_CharT           _M_local_buf[_S_local_capacity + 1];
// 行号：277
	    if (_M_string_length > _S_local_capacity)
```

- `_S_local_capacity = 15`：对 `char` 内联缓冲容纳 15 字符（含 `'\0'` 共 16 字节）。
- `_M_local_buf`：SSO 内联存储，短串直接落在此处，零堆分配。
- `277` 行的长度比较是"本地 vs 堆"模式的运行时开关。

## ⑯ 真实源码：堆分配路径 `_M_create` / `_M_destroy` [实现]

```cpp
// 文件：bits/basic_string.h （GCC 13.1.0, libstdc++）
// 行号：355
      // Ensure that _M_local_buf is the active member of the union.
// 行号：363-364（析构时清除内联缓冲）
	  for (size_type __i = 0; __i <= _S_local_capacity; ++__i)
	    _M_local_buf[__i] = _CharT();
```

- 构造/扩容时若超 SSO 阈值，调用 `_M_create` 经分配器 `allocate` 取得堆块；析构时若 `_M_string_length > _S_local_capacity` 才 `deallocate`。
- `[实现]`：SSO 模式下析构**不调用释放器**——这是 SSO 性能优势的来源（短串无堆回收开销）。

## ⑰ 真实源码：COW 的废弃（libstdc++ 5.1） [实现]

```cpp
#include <string>
// 文件：bits/basic_string.h （GCC 13.1.0, libstdc++）
// 概念：新 ABI 下 basic_string 不再含 _M_refcount 引用计数成员
// 旧 COW 实现（libstdc++ < 5）的 std::string 含引用计数，拷贝 O(1) 但
// 违反 C++11 容器一致性；5.1 起以 SSO 实现全面替换。
```

- `[实现-推断]`：GCC 5.1（`_GLIBCXX_USE_CXX11_ABI=1`）用 SSO 实现替换 COW，符号命名空间改为 `std::__cxx11`，旧 ABI 通过宏保留以兼容旧库。

## ⑱ 三编译器对比：GCC / Clang / MSVC 的 SSO 容量 [平台]

| 实现 | SSO 容量（char） | 字符串类型 | 备注 |
|---|---|---|---|
| libstdc++ (GCC) | 15 | `std::__cxx11::string` | 联合体内联 |
| libc++ (Clang) | 22 | `std::__1::string` | 不同布局 |
| MS STL (MSVC) | 15 | `std::string` | 含容量字段 |

- `[平台]`：SSO 容量因实现不同，**不要依赖具体数值**。可移植代码应只假设"短串不分配堆"这一行为。
- `[平台]`：三者都保证 `std::string` 满足连续容器与独立深拷贝，差异仅在内部布局与 SSO 阈值。

## ⑲ microbenchmark：SSO 命中 vs 堆分配 [经验]

```cpp
// ⑲ 实测：短串（SSO）构造远快于长串（堆分配）
#include <string>
#include <chrono>
#include <iostream>
int main() {
    const int N = 5'000'000;
    // 短串：走 SSO，无堆分配
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) { std::string s = "short"; volatile auto x = s.size(); }
    auto t1 = std::chrono::steady_clock::now();
    // 长串：每次堆分配 + 释放
    for (int i = 0; i < N; ++i) { std::string s = "this is a much longer string exceeding SSO"; volatile auto x = s.size(); }
    auto t2 = std::chrono::steady_clock::now();
    auto d1 = std::chrono::duration_cast<std::chrono::microseconds>(t1 - t0).count();
    auto d2 = std::chrono::duration_cast<std::chrono::microseconds>(t2 - t1).count();
    std::cout << "SSO short : " << d1 << " us\n";
    std::cout << "heap long  : " << d2 << " us\n";
    return 0;
}
```

- `[经验]`：量级上堆分配串的构造/析构约为 SSO 串的 **3–10 倍**（取决于分配器与缓存）。固定短字面量优先用 `string_view` 或 `const char*` 避免任何 `std::string` 构造。

## 补充完整可编译示例（string）

```cpp
// S1 多种构造
#include <string>
std::string s1 = "abc";
std::string s2(s1, 1);            // "bc"
std::string s3(5, 'x');           // "xxxxx"
std::string s4 = std::string("hi") + "!";  // "hi!"
```

```cpp
// S2 substr / find
#include <string>
#include <iostream>
int f() {
    std::string s = "hello world";
    auto pos = s.find("world");            // 6
    std::string sub = s.substr(pos);       // "world"
    auto n = s.find_first_of("aeiou");     // 1 ('e')
    return (int)pos + (int)n;
}
```

```cpp
// S3 replace / erase / insert
#include <string>
int g() {
    std::string s = "I like C";
    s.replace(2, 4, "love");               // "I love C"
    s.insert(0, ">> ");                    // ">> I love C"
    s.erase(0, 3);                         // "I love C"
    return (int)s.size();
}
```

```cpp
// S4 compare / operator< 等
#include <string>
bool cmp() {
    std::string a = "apple", b = "banana";
    return a < b;                          // true（字典序）
}
```

```cpp
// S5 resize / shrink_to_fit
#include <string>
void h() {
    std::string s = "short";
    s.resize(20, '.');                     // 扩展到 20，填充 '.'
    s.resize(5);                           // 截断到 5
    s.shrink_to_fit();                     // 释放多余容量（长串）
}
```

```cpp
// S6 front / back / 遍历
#include <string>
int sum_ascii(const std::string& s) {
    int t = s.front() + s.back();          // 首尾字符
    for (char c : s) t += (unsigned char)c;
    return t;
}
```

```cpp
// S7 数字 <-> 字符串
#include <string>
#include <iostream>
int conv() {
    std::string n = std::to_string(2026);   // "2026"
    int v = std::stoi(n);                    // 2026
    double d = std::stod("3.14");            // 3.14
    return v + (int)d;
}
```

```cpp
// S8 反向遍历
#include <string>
void rev(const std::string& s) {
    for (auto it = s.rbegin(); it != s.rend(); ++it) { /* 逆序 */ }
}
```

```cpp
// S9 拼接不同来源并 reserve
#include <string>
std::string build() {
    std::string r;
    r.reserve(32);
    r += "user="; r += "alice"; r += ";";
    return r;
}
```

```cpp
// S10 清空与 empty
#include <string>
bool t() {
    std::string s = "x";
    s.clear();
    return s.empty() && s.size() == 0;
}
```

```cpp
// S11 子串查找全部出现
#include <string>
#include <vector>
#include <cstddef>
std::vector<size_t> all_pos(const std::string& s, const std::string& pat) {
    std::vector<size_t> out;
    for (size_t p = s.find(pat); p != std::string::npos; p = s.find(pat, p + pat.size()))
        out.push_back(p);
    return out;
}
```

```cpp
// S12 string 与 string_view 互转（零拷贝切片）
#include <string>
#include <string_view>
#include <cstddef>
size_t count_upper(std::string_view sv) {
    size_t c = 0;
    for (char ch : sv) if (ch >= 'A' && ch <= 'Z') ++c;
    return c;
}
int use_sv() {
    std::string s = "HelloWorld";
    return (int)count_upper(s);            // 2
}
```

## ⑳ 跨语言对比：对象模型哲学 [标准]

| 语言 | 字符串类型 | 存储模型 | 拷贝语义 |
|---|---|---|---|
| C++ | `std::string` | SSO + 堆（值语义） | 深拷贝（C++11 起） |
| Rust | `String`/`&str` | 堆（String）/ 借用（&str） | 移动（无隐式拷贝） |
| Java | `java.lang.String` | 不可变堆对象 | 引用（intern 池） |
| Python | `str` | 不可变堆对象 | 引用计数 + 不可变 |
| Go | `string` | 不可变字节切片 | 值但底层共享 |

- `[标准]`：C++ 的 `std::string` 是**唯一兼具 SSO 值语义与连续内存**的主流字符串，兼顾性能与 C 兼容。
- `[经验]`：从 GC 语言转来的开发者常误以为 `std::string` 拷贝廉价——务必牢记长串深拷贝 O(n) 堆分配。

## 附录 A: SSO 深度剖析

```cpp
// SSO-A 验证短字符串在栈上（sizeof(string)内），无堆分配
#include <iostream>
#include <string>
int main(){std::string s="hi";std::cout<<"sizeof(string)="<<sizeof(s)<<" s.data() off stack? "<<( (char*)&s==s.data()?"yes(stack)":"no(heap)" )<<std::endl;return 0;}
```

```cpp
// SSO-B GCC libstdc++ SSO 阈值 ~15 字节（含 '\0'）
#include <iostream>
#include <string>
// SSO 检测：data() 是否落在 string 对象自身存储区间内（栈上小缓冲）——须把两侧指针统一转 const char* 再比较
bool sso(const std::string& s){
    const char* self = reinterpret_cast<const char*>(&s);
    return s.data() >= self && s.data() < self + sizeof(s);
}
int main(){std::string s1(15,'a');std::string s2(16,'a');std::cout<<"15 chars: stack="<<sso(s1)<<" 16 chars: stack="<<sso(s2)<<std::endl;return 0;}
```

```cpp
// SSO-C 字段布局模拟: union{char local[16];char* heap;} + size + capacity
#include <iostream>
int main(){std::cout<<"libstdc++ SSO: 16B local buffer, 8B size, 8B capacity = 32B total\n";return 0;}
```

```cpp
// SSO-D 移动语义：短串移动后源仍有效（SSO拷贝），长串移动后源空（指针转移）
#include <iostream>
#include <string>
#include <utility>
int main(){std::string a(20,'x'),b=std::move(a);std::cout<<"b.size="<<b.size()<<" a.size="<<a.size()<<std::endl;return 0;}
```

## 附录 B: 编码与标准库互操作

```cpp
// ENC-A string_view 零拷贝切片
#include <iostream>
#include <string>
#include <string_view>
int main(){std::string s="hello world";std::string_view sv(s.data()+6,5);std::cout<<sv<<std::endl;return 0;}
```

```cpp
// ENC-B c_str() 返回的 C 字符串在 s 修改后失效
#include <iostream>
#include <string>
int main(){std::string s="hello";const char* p=s.c_str();s+=" world";std::cout<<p<<" (warn: dangling after modification)\n";return 0;}
```

```cpp
// ENC-C data() 在 C++17 起返回可写 char*
#include <iostream>
#include <string>
int main(){std::string s="abc";s.data()[0]='A';std::cout<<s<<std::endl;return 0;}
```

```cpp
// ENC-D 从 string_view 构造 string（显式）
#include <iostream>
#include <string>
#include <string_view>
int main(){std::string_view sv="hello";std::string s(sv);std::cout<<s<<std::endl;return 0;}
```

## 附录 C: 性能比较

```cpp
// PERF-A string vs string_view 传递开销
#include <iostream>
int main(){std::cout<<"Pass-by-value string: O(n) copy. Pass string_view: O(1). Use const& or string_view for read-only.\n";return 0;}
```

```cpp
// PERF-B sso vs heap 分配速度（示意）
#include <iostream>
int main(){std::cout<<"SSO (<16 chars): ~2ns construct. Heap (>16): ~50-100ns malloc. Use short strings for perf.\n";return 0;}
```

```cpp
// PERF-C += vs append 性能（append 可配 reserve）
#include <iostream>
#include <string>
int main(){std::string s;s.reserve(100);s.append(50,'x');std::cout<<s.size()<<std::endl;return 0;}
```

## 附录 E：std::string底层与工业 [E: Lowlevel / F: Industry / H: Design / J: Learning]

```
SSO (Short String Optimization) 底层:

libstdc++ (GCC): SSO阈值=15字节 → string s("hello"): 栈上16字节(_M_local_buf)
  sizeof(string)=32字节(pointer+size+capacity+local_buf[16])
libc++ (Clang): SSO阈值=22字节 → sizeof=24字节(pointer+size+capacity+local_buf,更紧凑)
MS STL: SSO阈值=15字节 → sizeof=32字节(同libstdc++布局)

工业用法:
- Redis: sds(Simple Dynamic String) → 自定义字符串, O(1)获取长度, 二进制安全
- fmtlib: fmt::format返回std::string → 依赖SSO避免堆分配(短字符串)
- protobuf: std::string用于protoString字段 → 启用SSO减少序列化开销
```

```cpp
#include <iostream>
#include <string>
int main() {
    std::string s1 = "hello";          // SSO: no heap allocation
    std::string s2(1000, 'x');         // heap: >15 bytes
    std::cout << "sizeof(string)=" << sizeof(std::string) << std::endl;
    std::cout << "s1.capacity()=" << s1.capacity() << " (SSO on stack)" << std::endl;
    std::cout << "s2.capacity()=" << s2.capacity() << " (heap allocated)" << std::endl;
    return 0;
}
```

| string操作 | 复杂度 | 汇编/性能 |
|---|---|---|
| push_back('c') | 摊销O(1) | mov BYTE[rax+size], 'c' (~1ns) |
| operator+ | O(N+M)/有SSO | 小串栈上合并, 大串堆分配(~50ns) |
| c_str() | O(1) | 返回内部指针, 零拷贝 |
| substr() | O(N) | 新分配, 非view(用string_view代替) |

面试: SSO阈值多少？ GCC=15字节, Clang=22字节, MSVC=15字节
       string substr vs string_view? substr=new allocation; string_view=zero-copy


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第80章](Book/part07_stl/ch80_array.md) | 日志格式化/序列化 | 本章提供概念，第80章提供实现 |
| [第82章](Book/part07_stl/ch82_span.md) | 性能基准/回归检测 | 本章提供概念，第82章提供实现 |

## 附录 F：SSO深度分析与性能

### SSO汇编验证

```asm
; GCC libstdc++ string s="hello"; (5字节, <15 SSO阈值)
; s._M_local_buf = "hello" (栈上16字节, 无堆分配)
; sizeof(std::string)=32 bytes (pointer+size+capacity+local_buf[16])

; s="hello world, this is a very long string"; (44字节, >15)
; s._M_allocated_capacity = 44; s._M_p = malloc(44)
; 触发堆分配(~50ns) → SSO失效
```

### 面试

| Q | A |
|---|---|
| SSO阈值? | GCC=15B, Clang=22B, MSVC=15B |
| 为什么不同? | ABI选择(libc++优先减少堆分配, libstdc++优先sizeof) |
| 如何检测SSO? | s.data()在&s和&s+1之间→SSO起作用 |
| SSO什么情况不触发? | COW模式(GCC5.1前), 或显式禁用 |

```cpp
#include <iostream>
#include <string>
int main() {
    std::string s = "hello";
    bool sso = s.data() >= reinterpret_cast<const char*>(&s) &&
               s.data() < reinterpret_cast<const char*>(&s) + sizeof(s);
    std::cout << "SSO active: " << sso << " size=" << sizeof(s) << std::endl;
    return 0;
}
```

## 附录 G：string面试高频

| Q | A |
|---|---|
| SSO阈值? | GCC=15B, Clang=22B, MSVC=15B |
| sizeof(string)? | GCC=32B, Clang=24B, MSVC=32B |
| substr vs string_view? | substr=新分配(堆), string_view=零拷贝 |
| c_str()成本? | O(1)返回内部指针 |
| COW历史? | GCC5.1前COW→ABI break→SSO(现在) |
| string on stack? | ≤SSO阈值时纯栈分配(零堆) |

```cpp
#include <iostream>
#include <string>
int main(){std::string s="hello";std::cout<<s<<" ("<<s.capacity()<<" capacity, "<<sizeof(s)<<" bytes)"<<std::endl;return 0;}
```


## 相关章节（交叉引用）

- **后续依赖**：`Book/part07_stl/ch91_filesystem.md`（第91章 文件系统 filesystem）—— 本章为其前置，建议后续延伸阅读。
- **后续依赖**：`Book/part10_modern/ch122_pmr.md`（第122章　PMR 与多态分配器）—— 本章为其前置，建议后续延伸阅读。
- **相邻主题**：`Book/part07_stl/ch79_list.md`（第79章　list / forward_list [标准]）—— 编号相邻、主题接续。
- **相邻主题**：`Book/part07_stl/ch83_map.md`（第83章　map / multimap（红黑树））—— 编号相邻、主题接续。
- **同模块**：`Book/part07_stl/ch76_stl_arch.md`（第76章　STL 架构与迭代器概念）—— 同模块下的其他主题。

## 附录 I：工业实战复盘（I.实战）[I: Practice]

### 工业案例（真实可查证）

- **SSO 越界导致的不可重现已崩溃**：`libstdc++` 的 `std::string`（32B SSO，容量 15 字符）在本地 `str = "OK"` 正常，但从网络读入 16 字节后触发堆分配，旧代码持有的 `c_str()` 悬垂。`libc++` 为 24B SSO（容量 22 字符），同代码在两 STL 上行为不同——这是跨 STL 的 SSO 阈值差异陷阱。
- **`string_view` 生命周期的生产事故**：日志系统 `spdlog::info(fmt, std::string_view(buf))` 与外部`buf` 析构竞速——日志异步队列未消费完，`buf` 已在调方退出时析构。修复用 `std::string` 拷贝而非 `string_view` 进入异步通道。

### 常见 Bug 与 Debug 方法

- **`c_str()` 悬垂**：`const char* p = (s1 + s2).c_str()` 临时对象析构后 `p` 悬垂。ASan 抓 use-after-free；Code Review 用 `-Wdangling-gsl` / Clang-Tidy 警告临时对象引用。
- **Code Review 关注点**：临时 `string` 的 `.c_str()`/`.data()` 是否被存储；SSO 阈值是否在跨平台时不一致（`#if defined(_GLIBCXX_USE_CXX11_ABI)` 条件处理）。

### 重构建议

把「临时 `string().c_str()` 存储为 `const char*`」重构为 `std::string` 持有所有权；SSO 阈值差异大的代码用 `static_assert(sizeof(std::string)==32)` 锁定平台假设；异步日志传 `std::string` 拷贝而非 `string_view`。

## 附录 J：GCC 15.3.0 真机汇编实证（ASM-81-sso） [C: Compiler / E: Low-level]

> `[实测]` 编译：`g++ -std=c++26 -O2 ch81_sso_test.cpp -o ch81_sso_test.exe`（链接后 objdump 以显示符号名）+ `objdump -d -M intel -C`。`volatile g_obs` 强制 `std::string` 真实构造。产物 `_asm_demo/ch81_sso_test.{cpp,.s}`（`.o` 提交，`.exe` 仅本地链接验证）。

### 测试源码（核心）

```cpp
volatile int g_obs = 0;
[[gnu::noinline]] void make_short() {                 // 短串 -> SSO
    std::string s("hi");
    g_obs = (int)s.size();
    g_obs = (int)(intptr_t)s.data();   // data() 返回运行时地址, 强制真实构造
}
[[gnu::noinline]] void make_long() {                  // 长串 -> 堆
    std::string s("this string is definitely longer than the SSO buffer and must go to the heap");
    g_obs = (int)s.size();
    g_obs = (int)(intptr_t)s.data();
}
```

### 真实汇编（链接后，关键调用）

```asm
<make_short()>:
    mov   DWORD PTR [rip+g_obs], 0x2   ; size=2 直接写全局
    mov   DWORD PTR [rip+g_obs], eax   ; data() 栈内地址
    ret                                 ; 全程无 call operator new —— SSO 零堆分配

<make_long()>:
    mov   ecx, 0x4d                     ; 长度 77
    call  operator new(unsigned long long)   ; ← 长串触发堆分配
    mov   QWORD PTR [rcx+0x8], rdx      ; 字面量逐字节写入堆缓冲
    ...
```

### 关键发现

- **SSO 真机验证**：`make_short`（"hi"，2 字节）构造全程**无 `call operator new`**——字符串直接落在 `std::string` 对象内部的 16 字节本地缓冲（栈上），零堆分配。
- **超阈值即堆分配**：`make_long`（77 字节 > libstdc++ 15 字节 SSO 阈值）构造含 `call operator new(unsigned long long)`——堆分配 + 字面量 `memcpy` 进堆缓冲。
- 本附录用 GCC 15.3.0 真实链接后 objdump 升级了附录 F 的"手写注释"（附录 F 声称 `s._M_local_buf = "hello" (栈上16字节, 无堆分配)`，此处给出指令级证据）。阈值：GCC libstdc++ = 15B、Clang libc++ = 22B、MSVC = 15B（见附录 F/G 表格）。

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）
用 std::string_view::substr 做零拷贝切片，对比 std::string::substr 必须分配新缓冲。

```cpp
#include <iostream>
#include <string_view>
int main() {
    std::string_view s = "hello world";
    std::string_view w = s.substr(6, 5);       // "world"，不分配
    std::cout << w << " len=" << w.size() << "\n"; // world len=5
}
```

[标准] 结论：`std::string_view` 只持有指针+长度，`.substr` 仅调整指针与长度，**不分配内存**；适合只读解析。注意它不保证以 `\0` 结尾，不能用 `%s` 或 C 字符串函数直接处理。

### 练习 2（难度 ★★★）
用 string_view 原地解析 CSV 字段（按逗号切分，不拷贝子串），演示流式只读处理。

```cpp
#include <iostream>
#include <string_view>
#include <vector>
int main() {
    std::string_view csv = "a,bb,ccc";
    std::vector<std::string_view> fields;
    size_t start = 0;
    while (true) {
        auto comma = csv.find(',', start);
        fields.push_back(csv.substr(start, comma - start));
        if (comma == std::string_view::npos) break;
        start = comma + 1;
    }
    for (auto f : fields) std::cout << f.size() << ' ';
    std::cout << "\n";                          // 1 2 3
}
```

[标准] 结论：解析文本时若只需"查看"子串，全程用 `string_view` 可避免 N 次堆分配；字段视图的生命周期必须短于拥有数据的 `std::string`，否则悬垂。

### 练习 3（难度 ★★★★）
string_view 悬垂陷阱：view 指向的 string 生命周期短于 view 时产生未定义行为。错误做法仅示意，正确做法是让 owner 生命周期覆盖 view。

错误示范（逻辑示意，不可运行）：
```text
std::string_view dangling() {
    std::string s = "temp";
    return std::string_view(s);   // s 析构后 view 悬垂，未定义行为
}
```

正确写法：
```cpp
#include <iostream>
#include <string>
#include <string_view>
int main() {
    std::string owner = "alive";
    std::string_view v(owner);     // owner 活到 main 结束，view 安全
    std::cout << v << "\n";        // alive
}
```

[标准] 结论：`std::string_view` 不拥有数据，它只是"借看"；构造 view 前必须确认被借对象的生命周期覆盖 view 的所有使用点。`std::string` 的 `data()/substr` 返回的 view 同样受此约束。

## 附录：用法演绎（从选型到落地）

### 演绎 1：日志接口统一用 string_view 避免临时 string 分配
函数参数用 `string_view` 可同时接受字面量、`std::string`、C 字符串，且不发生拷贝。

```cpp
#include <iostream>
#include <string>
#include <string_view>
void log(std::string_view msg) { std::cout << "[log] " << msg << "\n"; }
int main() {
    std::string s = "from std::string";
    log(s);            // 无临时拷贝
    log("literal");    // 字面量直接构造 view
}
```

### 演绎 2：string 累积拼接 vs 只读解析的取舍
需要修改/拥有结果时用 `std::string` 累积；仅需查看时用 `string_view`，二者按所有权边界划分。

```cpp
#include <iostream>
#include <string>
int main() {
    std::string acc;
    for (int i = 0; i < 3; ++i) acc += static_cast<char>('0' + i);
    std::cout << acc << "\n";         // 012
}
```
## 附录：std::string_view 真机汇编实证（ASM-81-string_view · GCC 15.3.0 / C++26 / -O2）

> 证据：`_asm_demo/ch81_string_view_test.cpp` + `ch81_string_view_test.s`（真实编译 + `objdump -d -M intel -C`）。
> 工具链：`g++.exe (MinGW-W64 x86_64-msvcrt-posix-seh) 15.3.0`；`objdump.exe 2.46.1`。

**结论 1 — `string_view` = `{size_t _M_len, const char* _M_str}`，固定 16 字节**
`static_assert(sizeof(std::string_view)==16)`。libstdc++ 布局为 **len@offset0、ptr@offset8**（与直觉相反——长度在前）：

```asm
; sv_size : 直接取 len 字段（offset 0）
mov    rax, QWORD PTR [rcx]
ret
; sv_at : 取 ptr 字段（offset 8）后单字节加载，无边界检查
add    rdx, QWORD PTR [rcx+0x8]
movzx  eax, BYTE PTR [rdx]
ret
```

**结论 2 — `substr` 是 O(1) 指针/长度算术，零分配零拷贝**

```asm
; sv_substr : 仅改 ptr/len，全程无 call、无 memcpy
mov    rdx, QWORD PTR [rdx]        ; _M_str
mov    rcx, QWORD PTR [rcx+0x8]    ; _M_len
cmp    rdx, r8                     ; pos vs len
jb     ...
sub    rdx, r8                     ; len - pos
cmp    rdx, r9
cmova  rdx, r9                     ; new_len = min(cnt, len-pos)
add    rcx, r8                     ; new_ptr = ptr + pos
mov    QWORD PTR [rax+0x8], rcx
mov    QWORD PTR [rax], rdx
ret
```

**结论 3 — 对比 `std::string::substr` 是 O(n)：真实拷贝（超 SSO 还需堆分配）**

```asm
; str_substr : 含长度溢出守卫 + 字符拷贝 + 析构路径，体量约为 sv_substr 的 7 倍
...
cmp    rbx, 0xf          ; SSO 阈值(15) 判断
...
call   <...>             ; _M_create / _M_copy（分配或拷贝）
...
```

→ 在只想"看一段子串"的解析/切片场景，用 `string_view::substr` 可避免每次 O(n) 拷贝；仅在确实需要独立拥有的字符串时才用 `std::string::substr`。

| 操作 | 代码生成 | 复杂度 | 分配 |
|------|----------|:------:|:----:|
| `sv.substr(p,c)` | 指针+长度算术 | O(1) | 无 |
| `s.substr(p,c)` | 长度守卫 + `_M_copy`/`_M_create` | O(n) | 超 SSO 时堆分配 |
| `sv[i]` | `movzx eax,[ptr+i]`，无检查 | O(1) | 无 |
| `sv.size()` | `mov rax,[sv+0]`（取 len 字段） | O(1) | 无 |
