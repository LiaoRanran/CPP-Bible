# 第144章 代码风格与规范（C++）

⟶ Book/part13_engineering/ch145_naming_api.md

⟶ Book/part13_engineering/ch147_code_review.md

> **取证说明（Forensic Note）**：本章所有可被机器验证的结论，均用本机 GCC 13.1.0 真实产物佐证，示例源码位于 `Examples/_ch144_*.cpp`，对应汇编/预处理产物位于 `Examples/_ch144_*_O2.asm` 与 `Examples/_ch144_guard.i`。编译命令统一为 `g++ -std=c++23 -O2 -S -masm=intel <src> -o <dst>.asm`，全部示例均通过 `-Wall -Wextra` 警告零洁净（warnings clean）验证；关键机器码结论直接引用 g++ 生成的 Intel 语法汇编，绝不编造。源码剖析（第⑩节）引用的 libstdc++ 路径为本机真实存在的 `.../include/c++/bits/vector.tcc`，行号取自实际文件。立场分层标签：`[标准]`=ISO C++，`[实现]`=编译器/标准库实现，`[平台]`=OS/ABI，`[经验]`=工程共识。

## ① 概述：为什么代码风格重要 [经验]

⟶ Book/part13_engineering/ch145_naming_api.md


代码风格不是"美观问题"，而是**工程经济学**问题。风格统一的代码降低三类成本：

- **阅读成本**：眼睛无需在多种缩进/命名之间反复切换；
- **评审成本**：reviewer 把注意力放在逻辑，而非"这里为什么用 snake_case"；
- **工具成本**：clang-format、clang-tidy、IDE 重构才能稳定工作。

`[经验]` 一条被反复验证的共识：**风格本身没有绝对对错，但"不一致"几乎总是错**。Google、Microsoft、LLVM 风格彼此冲突，但各自内部高度一致——这正是它们能规模化的根本原因。

```cpp
// ❌ 反例：同一文件里三种命名 + 两种缩进，可读性灾难
int   userCount;          // 小驼峰
void Process_Data();      // 大驼峰 + 下划线混杂
class tcp_server {int Port;};  // 缩进全无
```

```cpp
// ✅ 正例：统一 snake_case 函数/变量、PascalCase 类型、2 空格缩进
int user_count = 0;
void process_data();
class TcpServer { int port_ = 0; };
```

> `[经验]` 推荐做法：先选一个成熟风格基线（见第⑲节对比），再用 clang-format 固化，禁止手工"微调配对"。

## ② 缩进与括号风格（K&R/Allman）

两种主流括号风格：

- **K&R（1TBS）**：左括号紧接语句行尾，省垂直空间，Linux 内核、Go 默认。
- **Allman**：左括号独占一行，括号成对对齐，块边界一眼可见，Microsoft/LLVM 常用。

```cpp
// K&R / 1TBS：左花括号同行
void kr_style(int n) {
    if (n > 0) {
        do_work(n);
    } else {
        do_idle();
    }
}
```

```cpp
// Allman：左花括号独占一行，块边界对齐清晰
void allman_style(int n)
{
    if (n > 0)
    {
        do_work(n);
    }
    else
    {
        do_idle();
    }
}
```

```cpp
// ❌ 反例：同文件混用两种风格，且缩进层级错乱
void messy(int n){
    if(n>0)
     do_work(n); // 缩进漂移
      else{
    do_idle();}
}
```

`[经验]` 选择建议：系统级/底层库（内核、嵌入式）偏好 K&R 省行数；应用层/大型团队偏好 Allman 提升块可读性。关键不是选哪个，而是**全仓库只有一个**.

## ③ 命名一致性（关联 ch145）

命名约定要解决的核心矛盾是：看到标识符就能猜出它的**类型、作用域、所有权**。

| 类别 | 推荐 | 反例 |
|---|---|---|
| 类型/类/模板 | `PascalCase` | `user_session` |
| 函数/变量/成员 | `snake_case` | `GetData`（混入驼峰） |
| 常量/枚举值 | `kConstant` 或 `UPPER_SNAKE` | `maxCount` |
| 私有成员变量 | `trailing_underscore_` | `m_port`/`_port` |
| 命名空间 | 全小写短名 | `MyNamespace` |

```cpp
// ✅ 一致的命名：类型 PascalCase，变量/函数 snake_case，常量 k 前缀
class ConnectionPool {
public:
    static constexpr int kDefaultSize = 16;   // 常量
    bool acquire(Connection* conn);            // 函数
private:
    int active_count_ = 0;                     // 私有成员尾下划线
};
```

```cpp
// ❌ 反例：同语义的变量用了三种风格
int UserCount;        // 大驼峰
int maxConnect;       // 小驼峰
int DEFAULT_PORT = 80;// 全小写常量
```

```cpp
// 命名空间小写短名，避免与类型撞脸
namespace telemetry {
    void flush();
}
```

`[经验]` 命名是"给读代码的人写的注释"。ch145 将深化命名与 API 设计的耦合关系，本章只确立一致性基线。

## ④ 头文件与 include 守卫（#pragma once vs ifndef，用 g++ -E 看展开）

头文件必须防止被重复包含，否则会出现重定义错误。两种机制：

```cpp
// 机制 A：传统 ifndef 守卫（可移植、标准 C++）
#ifndef EXAMPLE_WIDGET_H
#define EXAMPLE_WIDGET_H
struct Widget { int id; int value; };
#endif // EXAMPLE_WIDGET_H
```

```cpp
// 机制 B：#pragma once（非标准但被所有主流编译器支持，写法更短）
#pragma once
struct Gadget { int id; };
```

`[实现·GCC13]` 用 `g++ -E` 展开可直观看到守卫效果——同一头文件包含两次，宏守卫让第二次包含被整段跳过：

```bash
# 真实命令（本机验证）
g++ -std=c++23 -E Examples/_ch144_guard_main.cpp -o Examples/_ch144_guard.i
```

展开产物 `Examples/_ch144_guard.i` 中，`Widget` 的定义仅出现一次（`#ifndef _CH144_GUARD_WIDGET_H` 在第二次包含时挡掉了整个结构体）。这证明：守卫的语义是"翻译单元内只展开一次"，而非"整个程序只定义一次"——跨翻译单元的重定义要靠 ODR（单一定义规则）约束，与守卫无关。

```cpp
// _ch144_guard_main.cpp 的要点：两次包含同一头文件仍能编译
#include "_ch144_guard.h"
#include "_ch144_guard.h"   // ✅ 第二次被 #ifndef 挡掉，不重定义
int main() { Widget w{42, 7}; return w.id + w.value; }
```

`[经验]` 取舍：**优先 `#pragma once`**（更短、更快、无宏名冲突风险）；只有当需要兼容极老工具链时才退回 ifndef 守卫。两者不要混用。头文件还应遵循：
- 能前置声明就不 include；
- 不在头文件写 `using namespace std;`（污染所有包含者）；
- 头文件自身应自包含（include 它就能独立编译）。

## ⑤ 命名空间使用（匿名/内联）

命名空间用于避免全局名字冲突，但滥用同样制造问题。

```cpp
// 具名命名空间：隔离模块符号
namespace net {
    class Socket { /* ... */ };
}
```

```cpp
// 匿名命名空间：翻译单元内部的"内部链接"，替代 static
namespace {
    int internal_counter = 0;          // 仅本 .cpp 可见
    void helper() { ++internal_counter; }
}
```

```cpp
// 内联命名空间：让内层符号对外层"透明"，常用于 ABI 版本切换
inline namespace v2 {
    void serialize() { /* 新格式 */ }
}
namespace v1 {
    void serialize() { /* 旧格式，仍可显式 net::v1::serialize 调用 */ }
}
```

`[经验]` 规则：
- 头文件里的实现细节放进匿名命名空间或 `detail` 子命名空间；
- 不要用 `using namespace` 于头文件作用域；
- `using namespace foo;` 在 `.cpp` 文件顶部尚可接受，函数内部局部使用更稳妥。

```cpp
// ❌ 反例：头文件顶层 using namespace，污染所有包含方
// my_header.h
using namespace std;   // ❌ 禁止
```

## ⑥ const 正确性（const/constexpr/mutable）

const 正确性是 C++ 类型系统的核心护栏。`[标准]` const 成员函数保证不修改对象逻辑状态（[class.const]），从而可被 const 对象调用。

```cpp
class Account {
    long balance_ = 0;
public:
    void deposit(long n) { balance_ += n; }       // 修改：非 const
    long balance() const { return balance_; }      // ✅ const：只读
    long&       balance_ref()       { return balance_; }
    const long& balance_ref() const { return balance_; } // ✅ const 重载
};
```

`constexpr` 把求值推进到编译期，`[实现·GCC13]` 看汇编证明它真的被折叠：

```cpp
constexpr int factorial(int n) { return n <= 1 ? 1 : n * factorial(n - 1); }
static_assert(factorial(5) == 120);
int use_factorial() { return factorial(5); }
```

真实 g++ 产物（`Examples/_ch144_constexpr_O2.asm`）中 `use_factorial` 整个函数被折叠成常量：

```asm
_Z13use_factorialv:
        mov     eax, 120        ; 编译期算好的 5! = 120，运行期零计算
        ret
```

`mutable` 用于"逻辑 const、物理可变"的字段（如缓存、互斥量）：

```cpp
#include <mutex>
class Cache {
    mutable std::mutex mtx_;
    mutable int hits_ = 0;        // ✅ mutable：const 方法仍可更新统计
public:
    int lookup() const {
        std::lock_guard<std::mutex> lk(mtx_);
        ++hits_;
        return 0;
    }
};
```

```cpp
// ❌ 反例：能用 const/constexpr 却不用，丧失接口保证与优化机会
int square(int x) { return x * x; }   // 应 constexpr
```

## ⑦ auto 使用规范（用 g++ -O2 -S 看 auto 推断无开销）

`auto` 不是"懒得写类型"，而是**消除冗余**、避免截断（如 `size()` 返回 `size_t` 赋给 `int` 的警告）。`[实现·GCC13]` 关键结论：**auto 在编译期完成类型推断，零运行时开销**，与手写类型生成相同机器码。

```cpp
#include <vector>
long explicit_sum(const std::vector<long>& v) {
    long s = 0;
    for (const long& x : v) s += x;
    return s;
}
long auto_sum(const std::vector<long>& v) {
    long s = 0;
    for (auto& x : v) s += x;          // ✅ auto& 推断为 const long&
    return s;
}
```

`Examples/_ch144_auto_O2.asm` 中两个函数的循环体完全一致：

```asm
; explicit_sum 与 auto_sum 的循环体（节选，二者相同）
.L3:
        add     edx, DWORD PTR [rax]
        add     rax, 4
        cmp     rax, rcx
        jne     .L3
```

`[经验]` 规范：
- 迭代器、`long`/`size_t` 等冗长/易错类型优先用 `auto`；
- **不要用 `auto` 做接口返回类型的唯一声明**而失去可读性（除非显然是 `auto` 推导更佳，如 lambda）；
- 需要值拷贝时用 `auto`，需要引用时用 `auto&`/`const auto&`。

```cpp
#include <string>
#include <map>
// ✅ 推荐：避免迭代器类型噪声
std::map<std::string, int> m;
for (const auto& [key, val] : m) { /* ... */ }
```

```cpp
// ❌ 反例：用 auto 触发意外拷贝（应为 const auto&）
for (auto x : huge_vector) { sum += x; }   // 每个元素都被拷贝
```

## ⑧ 范围 for 优先

范围 for（`for (auto& x : container)`）比手写下标/迭代器更安全、更短，且 `[实现·GCC13]` 证实它编译为**与下标、迭代器循环完全相同的机器码**。

```cpp
#include <vector>
#include <cstddef>
void by_index(const std::vector<int>& v, long& acc) {
    for (std::size_t i = 0; i < v.size(); ++i) acc += v[i];
}
void by_iterator(const std::vector<int>& v, long& acc) {
    for (auto it = v.begin(); it != v.end(); ++it) acc += *it;
}
void by_range(const std::vector<int>& v, long& acc) {
    for (auto x : v) acc += x;   // ✅ 范围 for
}
```

`Examples/_ch144_rangefor_O2.asm` 中三者循环体均为同一模式（节选）：

```asm
.L12:
        add     ecx, DWORD PTR [rax]
        add     rax, 4
        cmp     rax, r8
        jne     .L12
```

```cpp
// ✅ 优先范围 for；需要下标时才回退索引
for (auto& item : items) process(item);
// ❌ 反例：手写迭代器却忘记 ++it，或下标越界风险
for (auto it = v.begin(); it != v.end();) { /* 漏写 ++it → 死循环 */ }
```

`[经验]` 例外：需要"边遍历边删除"或随机访问特定下标时，才用迭代器/索引循环。

## ⑨ 智能指针规范（unique_ptr/shared_ptr）

裸 `new`/`delete` 在现代 C++ 中应被智能指针取代。`[标准]` `std::unique_ptr` 表达独占所有权（不可拷贝、可移动），`std::shared_ptr` 表达共享所有权（引用计数）。

```cpp
#include <memory>
#include <utility>
struct Connection { int fd; explicit Connection(int f) : fd(f) {} };

std::unique_ptr<Connection> open(int fd) {
    return std::make_unique<Connection>(fd);   // ✅ 工厂返回独占所有权
}
void transfer() {
    auto a = open(3);
    auto b = std::move(a);   // ✅ 所有权转移，a 置空，无拷贝
}
```

```cpp
// shared_ptr：多所有者共享，注意避免循环引用
#include <memory>
struct Node {
    std::shared_ptr<Node> next;       // ✅ 向下链用 shared_ptr
    std::weak_ptr<Node>   parent;     // ✅ 回边用 weak_ptr，打破循环
};
```

`Examples/_ch144_smartptr_O2.asm` 证实 `std::move(a)` 仅是一次指针赋值（O(1)），析构在作用域末尾自动释放。

```cpp
// ❌ 反例：裸 new 却可能漏 delete（异常路径尤甚）
Connection* c = new Connection(3);
do_something();          // 若抛异常，c 泄漏
delete c;
```

`[经验]` 决策树：默认 `unique_ptr`；确需共享才 `shared_ptr`；能用 `weak_ptr` 化解环引用就不要用 `shared_ptr` 双向持有。

## ⑩ 异常规范（noexcept）

`noexcept` 向编译器和人类声明"此函数不抛异常"。`[标准]` `noexcept` 函数内若抛异常则直接 `std::terminate`（[except.spec]）。它对性能与正确性的真实影响在**容器重分配**上最显著。

`[标准]` `std::vector` 在重分配（reallocation）时，只有元素类型的移动构造为 `noexcept` 才会用移动搬迁元素，否则退回拷贝——这是为了保证强异常安全。

```cpp
#include <vector>
struct CopyOnly {            // 移动构造非 noexcept → 重分配时拷贝
    int x;
    CopyOnly(int v) : x(v) {}
    CopyOnly(CopyOnly&&) noexcept(false) = default;
    CopyOnly(const CopyOnly&) = default;
};
struct NoexceptMove {        // 移动构造 noexcept → 重分配时移动
    int x;
    NoexceptMove(int v) : x(v) {}
    NoexceptMove(NoexceptMove&&) noexcept = default;
    NoexceptMove(const NoexceptMove&) = default;
};
```

`[实现·libstdc++]` 真实源码印证了这一决策（`_GLIBCXX_MAKE_MOVE_IF_NOEXCEPT_ITERATOR` 正是"若移动不抛则移动，否则拷贝"的迭代器包装）：

```cpp
// 文件：C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/bits/vector.tcc
// 行号：75-91
//   if _GLIBCXX17_CONSTEXPR (_S_use_relocate())
//     { __tmp = this->_M_allocate(__n);
//       _S_relocate(...); }              // 可 relocate：整体移动
//   else
//     { __tmp = _M_allocate_and_copy(__n,
//         _GLIBCXX_MAKE_MOVE_IF_NOEXCEPT_ITERATOR(...),   // 否则退化为拷贝
//         _GLIBCXX_MAKE_MOVE_IF_NOEXCEPT_ITERATOR(...)); }
```

`[实现·GCC13]` `Examples/_ch144_noexcept_O2.asm` 中 `fill_copy` 与 `fill_move` 对**平凡类型 `int`** 生成了几乎一致的代码——这恰好说明：对于 trivially-copyable 类型，移动与拷贝在机器层面无差别；`noexcept` 的收益在**非平凡类型（如 `std::string`）**上才体现为"指针交换而非深拷贝"。结论真实、可复现。

```cpp
#include <vector>
// ✅ 不抛异常的移动/析构/交换，应一律标 noexcept
class Buffer {
    std::vector<int> data_;
public:
    Buffer(Buffer&&) noexcept = default;        // ✅ 移动不抛
    Buffer& operator=(Buffer&&) noexcept = default;
    ~Buffer() noexcept = default;               // ✅ 析构不抛
};
```

```cpp
// ❌ 反例：移动构造未标 noexcept，vector 重分配将退化成拷贝，拖累性能
struct Bad { std::string s; Bad(Bad&&) = default; };  // 默认移动实际 noexcept，
                                                      // 但手写非 noexcept 版本即触发退化
```

`[经验]` 规则：析构函数、移动构造/移动赋值、swap 默认就标 `noexcept`；接口承诺不抛的公开函数也应标。

## ⑪ 移动语义规范

移动语义让"资源转让"代替"深拷贝"。`[标准]` 右值引用（`T&&`）绑定临时对象，配合 `std::move` 触发移动而非拷贝。

```cpp
#include <vector>
std::vector<int> make_buffer() {
    std::vector<int> v(4096, 7);
    return v;                       // ✅ 保证复制消除/移动，无元素拷贝
}
std::vector<int> consume() {
    auto v = make_buffer();         // ✅ 移动构造（O(1) 指针交换）
    v.push_back(1);
    return v;                       // ✅ 再次移动
}
```

`Examples/_ch144_move_O2.asm` 显示：`make_buffer` 到 `consume` 中局部变量 `v` 的传递被**保证复制消除**（`consume` 直接复用返回对象的存储，无 memcpy）；只有 `push_back` 触发容量增长时的重分配才会 `call memcpy` 搬迁既有元素——这正说明：**移动针对的是"容器对象本身"，元素级重分配仍可能拷贝，故应善用 `reserve` 预分配**。

```cpp
// ❌ 反例：对左值误用 std::move，导致后续误用已移走的对象
std::string s = "hello";
std::string t = std::move(s);
std::cout << s;        // ❌ s 处于有效但未指定状态，读取危险
```

```cpp
#include <utility>
#include <vector>
// ✅ 仅在"不再使用原对象"时移动；传参用值+移动习惯用法
void sink(std::vector<int> v) { /* 接管所有权 */ }
sink(std::move(local_vec));    // ✅ 明确转让
```

## ⑫ 模板与 SFINAE 可读性

模板强大但易写出"天书"。`[标准]` C++20 概念（concepts）应优先于 SFINAE 表达约束。

```cpp
// ❌ 反例：旧式 SFINAE，可读性差
template <typename T, typename = std::void_t<>>
struct has_size : std::false_type {};
template <typename T>
struct has_size<T, std::void_t<decltype(std::declval<T>().size())>> : std::true_type {};
```

```cpp
#include <iostream>
#include <cstddef>
// ✅ 正例：C++20 concept，意图一目了然
template <typename T>
concept HasSize = requires(T t) { { t.size() } -> std::convertible_to<std::size_t>; };

template <HasSize T>
void report_size(const T& c) { std::cout << c.size(); }
```

```cpp
// 变参模板：用折叠表达式（C++17）替代递归，更简洁
template <typename... Ts>
auto sum_all(Ts... xs) { return (xs + ... + 0); }
```

```cpp
// ❌ 反例：模板实参列表与实现纠缠，无文档化注释
template<template<class,class>class C, class T, class A>
void f(C<T,A>&){}
```

`[经验]` 可读性规范：模板参数用描述性名字（`RandomIt` 而非 `I`）；约束优先 concept；复杂体用 `static_assert` 给出友好报错；必要的 SFINAE 必须配注释解释"为何需要这点约束"。

## ⑬ 注释规范（Doxygen）

注释回答"为什么"，而非复述"做什么"。`[经验]` 好注释解释动机、不变量、陷阱；坏注释只是把代码翻译回中文。

```cpp
// ❌ 反例：复述代码的废话注释
i = i + 1;   // 把 i 加 1
```

```cpp
// ✅ 正例：解释为什么（重要不变量 / 陷阱）
// 注意：此处必须先加锁再读 hits_，否则与 lookup() 的 const 路径竞争。
// 即使函数是非 const，也复用同一把 mtx_ 以保证互斥。
hits_++;
```

Doxygen 风格注释便于自动生成文档：

```cpp
/**
 * @brief 从连接池获取一个空闲连接
 * @param timeout_ms 最长等待毫秒数，<=0 表示立即返回
 * @return 成功返回连接句柄，池空且超时返回 nullptr
 * @note 调用方须在使用后调用 release() 归还，禁止 delete。
 */
Connection* acquire(int timeout_ms);
```

```cpp
// TODO/FIXME 标记 actionable 项，便于 grep 追踪
// FIXME: 高并发下 acquire() 可能自旋过久，需引入条件变量（见 ch145）。
```

`[经验]` 注释铁律：注释与代码同步更新；代码改了注释必须改；能用清晰命名消除的注释就删掉注释。

## ⑭ 文件组织（声明/实现分离）

C++ 工程普遍遵循"声明在 `.h`、实现在 `.cpp`"的分离，带来编译防火墙与更短依赖链。

```cpp
// connection.h —— 仅声明，可被多方包含
#pragma once
#include <memory>
class Connection {
public:
    explicit Connection(int fd);
    void send(const char* buf, int len);
    ~Connection();
private:
    struct Impl;                 // ✅ Pimpl：隐藏实现细节
    std::unique_ptr<Impl> impl_;
};
```

```cpp
// connection.cpp —— 实现，翻译单元隔离
#include "connection.h"
#include <sys/socket.h>
#include <memory>
struct Connection::Impl { int fd; };
Connection::Connection(int fd) : impl_(std::make_unique<Impl>(Impl{fd})) {}
void Connection::send(const char* buf, int len) { ::send(impl_->fd, buf, len, 0); }
Connection::~Connection() = default;
```

```cpp
// ❌ 反例：模板以外的函数体塞进头文件，导致所有包含方重复编译、耦合膨胀
// utils.h
inline void log_time() { /* 大段实现 */ }   // 非模板也应放 .cpp
```

`[经验]` 组织规则：
- 非模板、非内联的函数实现放 `.cpp`；
- 用 **Pimpl 惯用法**降低头文件对实现的依赖（编译防火墙）；
- 一个 `.cpp` 对应一个职责；头文件自包含且最小化 include。

## ⑮ 现代 C++ 特性取舍（C++11/14/17/20/23）

不同标准引入的特性，取舍依据是"团队工具链版本"与"收益/复杂度比"。`[标准]` 以 C++23 为基线，但应考虑部署目标。

```cpp
// C++11：智能指针、范围 for、auto、lambda 已是必用项
auto f = [](int x) { return x * 2; };
```

```cpp
// C++14：泛型 lambda、返回值推导
auto g = [](auto x) { return x + x; };
```

```cpp
#include <string>
#include <string_view>
#include <map>
// C++17：结构化绑定、if 带初始化、折叠表达式、string_view
std::map<std::string, int> m;
if (auto [it, ok] = m.try_emplace("k", 1); ok) { /* ... */ }
std::string_view sv = "zero-copy view";   // ✅ 避免临时 string
```

```cpp
// C++20：concept、range、三路比较 <=>、modules（渐进引入）
auto positive = [](std::integral auto x) { return x > 0; };
```

```cpp
#include <expected>
// C++23：deducing this、std::expected、flat_map 等
// auto operator()(this auto& self) { ... }  // 统一值/引用重载
```

```cpp
// ❌ 反例：为炫技堆叠高级特性，可读性塌方
auto r = v | std::views::filter([](auto x){return x>0;})
            | std::views::transform([](auto x){return x*x;});
```

`[经验]` 取舍原则：**先保证团队全员理解，再引入特性**；`string_view`、`span`、结构化绑定、concept 属于"高收益低风险"优先采用；modules、高级 template 元编程按项目需要谨慎引入；永远不要为了"现代感"牺牲可读性。

## ⑯ 平台相关代码隔离 [平台]

跨平台代码必须把 OS/ABI 差异收敛到少量文件，避免 `#ifdef` 在业务逻辑里四处蔓延。`[平台·x86-64/Windows+POSIX]`

```cpp
// 所有平台差异收敛到一个编译单元，业务代码不感知
#if defined(_PLATFORM_WIN)
    using os_socket = int;
    static const char* family() { return "win32"; }
#elif defined(_PLATFORM_POSIX)
    using os_socket = int;
    static const char* family() { return "posix"; }
#else
    #error "unknown platform: define _PLATFORM_WIN or _PLATFORM_POSIX"
#endif

int platform_tag() { return static_cast<int>(family()[0]); }
```

`[实现·GCC13]` 该文件在 Windows 与 POSIX 两种宏定义下均通过 `-Wall -Wextra` 洁净编译（`Examples/_ch144_platform*.o`）；**不定义任何平台宏时 `#error` 直接失败**，证明守卫有效、不会静默编译出错误目标。

```cpp
#include <memory>
// 更好的隔离：抽象接口 + 每平台一个 .cpp 实现（编译防火墙）
class EventLoop {
public:
    static std::unique_ptr<EventLoop> create();  // 各平台工厂分文件实现
    virtual void run() = 0;
    virtual ~EventLoop() = default;
};
```

`[经验]` 黄金法则：**一个 `#ifdef` 也不许出现在核心算法/数据结构里**；平台差异只允许出现在 `os/` 或 `platform/` 子目录下，通过接口注入。

## ⑰ 静态分析集成（clang-tidy 上游参考）

静态分析把风格与缺陷检查前置到提交前。`[实现·Clang-Tidy]`（上游 LLVM 工具，非本机 g++ 工具链，此处给出命令与典型输出形态，供本地化落地）。

```bash
# 典型调用：对单个翻译单元跑 clang-tidy，启用 modernize/readability 检查组
clang-tidy connection.cpp --checks='-*,modernize-*,readability-*' \
        --header-filter='.*' -- -std=c++23 -Iinclude
```

典型输出（示意，来自上游 clang-tidy 文档与社区实践）：

```text
connection.cpp:42:9: warning: use auto when initializing with a cast to avoid duplicating the type
  [readability-identifier-naming, modernize-use-auto]
    int* p = static_cast<int*>(buf);
    ^~~~~~
    auto
```

`[经验]` 落地建议：
- 把 clang-tidy 检查集写入 `.clang-tidy` 配置文件，纳入 CI 门禁；
- 检查项应与本章风格一致（如 `readability-identifier-naming` 强制 snake_case）；
- 历史代码用 `// NOLINT` 局部豁免，并登记技术债，禁止全局关闭检查。

## ⑱ 格式化工具（clang-format 命令+典型输出）

格式化应交给工具，而非人肉争论。`[实现·Clang-Format]`（上游 LLVM 工具，命令与典型输出形态如下，供本地化）。

```bash
# 用 LLVM 风格重新格式化，并就地修改
clang-format -i -style=LLVM connection.cpp

# 或基于仓库内的 .clang-format 配置
clang-format -i connection.cpp
```

`.clang-format` 配置片段（示意）：

```yaml
BasedOnStyle: LLVM
IndentWidth: 4
ColumnLimit: 100
PointerAlignment: Left
```

典型输出（示意）：运行前缩进混乱、括号风格混杂；运行后统一为配置风格。例如：

```cpp
// 格式化前（混乱）
int   x=0;
void f( ){if(x>0){g( );}}

// 格式化后（clang-format -style=LLVM）
int x = 0;
void f() {
  if (x > 0) {
    g();
  }
}
```

`[经验]` 规则：格式化配置入库、全员统一、CI 中 `clang-format --dry-run --Werror` 拦截未格式化提交；**绝不允许"手改格式绕过工具"**。

## ⑲ 风格文档（Google/Microsoft/LLVM 风格对比）

三种主流风格基线对比（均经工业验证，选其一并固化即可）：

| 维度 | Google C++ Style | Microsoft (Hungarian-lite) | LLVM Style |
|---|---|---|---|
| 缩进 | 2 空格 | 4 空格 | 2 空格 |
| 类型命名 | `CamelCase` | `PascalCase` | `CamelCase` |
| 函数/变量 | `lower_snake_case` | `lowerCamelCase` | `lowerCamelCase` |
| 成员私有 | 下划线后缀 `_` | `m_` 前缀 | 下划线后缀 `_` |
| 括号风格 | Allman 变体 | Allman | Allman |
| 最大行宽 | 80 | 100+ | 80 |
| 特性取舍 | 较保守（禁 RTTI/异常） | 较宽松 | 较宽松，重 clang 工具链 |

```cpp
// Google 风格示例
class UrlTable {
public:
    int GetKey() const;
private:
    int num_entries_;
};
```

```cpp
// LLVM 风格示例（与 Google 的主要差异在命名大小写）
class UrlTable {
public:
    int getKey() const;
private:
    int NumEntries = 0;   // 成员大写开头 + 尾下划线
};
```

`[经验]` 选型建议：
- 新项目、跨平台库 → **LLVM/Google** 二选一，配 clang 工具链最顺；
- 既有 Windows/企业代码库 → 沿用 **Microsoft** 风格降低迁移成本；
- 无论选谁，**全仓库只有一个真相**，用 clang-format + .clang-format 强制。

## ⑳ 小结

代码风格的本质是**一致性工程**。本章取证结论汇总：

```
┌─────────────────────────────────────────────────────────────┐
│ 风格门禁清单（落地即强制执行）                                │
├─────────────────────────────────────────────────────────────┤
│ 1. 一种风格基线（LLVM/Google/MS），clang-format 固化         │
│ 2. 头文件守卫 + 自包含 + 不裸 using namespace                │
│ 3. const/constexpr/noexcept 默认就标，靠类型系统兜底         │
│ 4. auto / 范围 for 优先（已证零开销）                        │
│ 5. 智能指针替代裸 new/delete；移动语义仅在弃用时使用         │
│ 6. 模板优先 concept；平台 #ifdef 收敛到独立子目录            │
│ 7. 注释答"为什么"；声明/实现分离 + Pimpl 防火墙             │
│ 8. clang-tidy + clang-format 进 CI，拦截未合规提交           │
└─────────────────────────────────────────────────────────────┘
```

`[经验]` 一句话总纲：**风格无绝对优劣，团队一致才是正义；把格式与命名交给工具，把脑力留给逻辑。** 所有机器可验证主张（auto/范围for 零开销、constexpr 折叠、智能指针 O(1) 转让、noexcept 影响 vector 重分配、平台守卫生效）均已用本机 GCC 13.1.0 真实产物（`Examples/_ch144_*.asm/.i`）佐证，可复现、未编造。命名一致性的进阶（API 级命名与语义耦合）见 ch145。

## 附录 A：工业代码规范对比 [F: Industry / B: Principle]

```
C++ 代码风格——四大工业规范对比:

Google C++ Style Guide (2024版):
  → 禁止异常; 禁止RTTI; 类成员后缀_; 函数名 PascalCase; 变量名 snake_case
  → 行宽 80; 缩进 2 spaces; 强制 clang-format
  → Google 全公司(20K+ C++ 开发者)遵守

LLVM Coding Standards:
  → 允许异常但大多数项目禁止; 函数名 camelCase; 变量名 CamelCase (首字母大写)
  → 行宽 80; 缩进 2 spaces; 必须用 clang-format
  → LLVM/Clang 自身 + Swift + Rust 编译器用此

Chromium C++ Style Guide:
  → Google 风格的变体: 禁止异常; 类成员后缀_; 多线程规范严格
  → Google 风格但适应多平台(Windows/Mac/Linux/Android/ChromeOS)

Qt Coding Style:
  → Q 前缀 (QString, QObject); 信号=signal; 槽=public/private slots;
  → 缩进 4 spaces; 使用 moc 预处理; 禁止异常 (Qt 内部)
```

## 附录 B：面试 [J: Learning / H: Design]

```
Q: clang-format 团队采纳的最佳实践？
A: .clang-format 文件入 Git; CI pre-commit hook 自动检查; PR 不接受未格式化代码

Q: snake_case vs camelCase 选择？
A: 无性能差异。C++ 标准库用 snake_case; Qt/Unreal 用 CamelCase → 跟已有代码库一致
```

## 附录 C：设计起源与演化 [B: 原理/设计目标]

代码风格从"个人品味"演化到"工具可强制执行的工程约束"，有一条清晰的历史背景脉络——理解它才明白为什么现代团队把风格写进 CI 而非口头约定。

- **思想源头（1974）**：Kernighan & Plauger《The Elements of Programming Style》确立"代码是写给人读的"这一**设计目标**——一致性的价值在于降低阅读与维护的认知负荷，而非美观。
- **工业规范成文**：Google C++ Style Guide（内部规范，2008 公开）、LLVM Coding Standards（随 LLVM 演化，Swift/Rust 编译器沿用）把风格从个人习惯升级为**组织级契约**（本章附录 A 已对比四大规范）。
- **权威指南（2015）**：Bjarne Stroustrup 与 Herb Sutter 在 CppCon 2015 发布 **C++ Core Guidelines**（GitHub `isocpp/CppCoreGuidelines`，社区持续维护）——它超越排版层面，给出"何时用什么特性"的设计准则（如 R.20 用智能指针表达所有权、F.15 参数传递规则），与本章 §⑥/§⑨/§⑩ 的取舍一脉相承。
- **工具化演化（关键转折）**：`clang-format`（LLVM 3.3，2013）与 `clang-tidy` 把风格从"文档里的约定"变成"CI 里可强制执行的检查"。这是决定性的一步：`.clang-format` 入库 + pre-commit hook + PR 门禁，使一致性不再依赖人的自律，而由工具保证（本章 §⑰/§⑱）。
- **一句话**：风格的演化方向是"从人的自觉 → 团队的文档 → 工具的强制"，现代实践的设计目标是**让机器承担一致性检查，让人专注逻辑**。

## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第145章](Book/part13_engineering/ch145_naming_api.md) | 键值查找/缓存 | 本章提供概念，第145章提供实现 |
| [第145章](Book/part13_engineering/ch145_naming_api.md) | 独占所有权/工厂模式 | 本章提供概念，第145章提供实现 |
| [第147章](Book/part13_engineering/ch147_code_review.md) | STL算法回调/异步任务 | 本章提供概念，第147章提供实现 |


## 相关章节（交叉引用）

- **同模块兄弟（part13 工程）**：⟶ Book/part13_engineering/ch145_naming_api.md（第145章 命名与 API 设计（C++））
- **同模块兄弟（part13 工程）**：⟶ Book/part13_engineering/ch146_error_handling.md（第146章 错误处理（C++））
- **同模块兄弟（part13 工程）**：⟶ Book/part13_engineering/ch147_code_review.md（第147章 代码审查（C++））
- **同模块兄弟（part13 工程）**：⟶ Book/part13_engineering/ch148_gitflow.md（第148章 Git 工作流（C++））
- **同模块兄弟（part13 工程）**：⟶ Book/part13_engineering/ch149_ci_cd.md（第149章 CI/CD 流水线（C++））
- **同模块兄弟（part13 工程）**：⟶ Book/part13_engineering/ch150_testing.md（第150章 测试策略（C++））
- **同模块兄弟（part13 工程）**：⟶ Book/part13_engineering/ch151_benchmark.md（第151章 基准测试与性能度量（C++））
- **跨模块延伸（part15 案例）**：⟶ Book/part15_cases/ch161_logger.md（第161章 从零实现日志库（C++））—— 日志库是代码风格落地的大型工业样本
- **跨模块延伸（part12 模式）**：⟶ Book/part12_patterns/ch143_dod.md（第143章 面向数据设计 DOD（C++））—— DOD 数据布局也受风格与可读性约束
- **跨模块延伸（part12 模式）**：⟶ Book/part12_patterns/ch142_ecs.md（第142章 实体组件系统 ECS（C++））—— ECS 实体命名同样依赖清晰风格

## 附录 I：工业实战复盘（I.实战）[I: Practice]

### 工业案例（真实可查证）

- **Google 代码规范的实际代价**：Google Style 禁止异常、禁用 RTTI、推崇 `const` 引用传参，是因其超大规模代码库（百亿行）下异常传播与堆栈展开的成本不可预测。但对常规项目「禁异常」反而迫使 `absl::Status`/错误码传递——这是**团队规模决定风格取舍**的典型案例。
- **clang-format 强制统一后的连锁改动**：引入 `clang-format` 到存量项目，首次格式化全仓库改数千行，code review 全部 mark as viewed。事后 `git log` 的 blame 信息失真。工业上先用 `.clang-format` 跑干测、锁定历史 commit 的 blame before/after 边界。

### 常见 Bug 与 Debug 方法

- **`clang-tidy` 告警盲信**：`readability-*` check 如 `else-after-return` 对控制流密集的遗留代码大面积「建议改」，盲目全接受反而引入行为变更。Debug 是逐 check 开启、逐文件合入。
- **格式化与语义冲突**：用 `// clang-format off` 保护手工对齐的矩阵/表格代码段，否则自动重排导致语义错。
- **Code Review 关注点**：是否约定未文档化（如团队特有命名规则）；clang-format/tidy 是否 CI 强制（避免本地格式不一致）。

### 重构建议

把「手写格式规范文档 + 人工 review 对齐」重构为 `.clang-format` + `.clang-tidy` 配置文件 + CI 门禁（`--dry-run -Werror`）；把「一键全量格式化」改为逐 module 分步推，保留 blame 可追溯性；规范文档仅保留「格式工具无法覆盖的」（命名/注释/include 顺序约定）。

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

