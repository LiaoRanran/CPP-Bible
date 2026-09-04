# 第 40 章　异常安全（Exception Safety）
> 层级：L2 进阶
> 【性能声明 · §10.3】本章所有绝对延迟/带宽数字（如 L1≈1ns、主存≈100ns、各基准 ms）均为 **x86-64 量级示意**，强依赖具体 CPU 型号/频率、编译器及版本、编译标志、OS、测试负载与样本量；非通用性能结论，绝对数字不可移植。微架构相关结论标 `[微架构·x86-64][UNVERIFIED]`；本机实测标 `[实验·本机实测][UNVERIFIED]`。断言形如「acquire 读比 relaxed 贵 X」仅在给定微架构下成立。

> 老兵标准：**异常安全不是「会不会抛异常」，而是「抛异常之后世界是否仍然自洽」。** 四种保证（noexcept / strong / basic / none）是 C++ 对异常的全部承诺；`noexcept` 决定 vector 扩容是移动还是拷贝——这一行代码关系到你整个程序的强度与性能。
> 本章遵循《现代 C++ 终极圣经》标准 v3：真实源码逐行 + GCC/LLVM/MSVC 三实现对照 + libstdc++/libc++/MS STL 三 STL 对照 + microbenchmark + 跨语言对比 + 推荐阅读已内化进正文。

立场分层约定：
- **<span class="badge badge-std">标准</span>**　语言/库标准规定（ISO C++、`[res.on.exception.handling]`、LWG 决议）。
- **<span class="badge badge-impl">实现</span>**　libstdc++ / libc++ / MS STL 的具体代码行为。
- **<span class="badge badge-platform">平台</span>**　MinGW GCC 13.1.0、Windows、Itanium/SEH ABI 相关事实。
- **<span class="badge badge-exp">经验</span>**　工程实践、坑与取舍。

环境事实（本机探测）：MinGW **GCC 13.1.0**；libstdc++ 头文件根目录
`C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/`；本章所有 `[实现]` 级源码均来自该目录的真实文件，逐行标注路径与行号。libc++、MS STL 不在本机，相关对比以 `[实现-推断]` / `[平台-推断]` 标注。

---

## ⓪ 历史动机：异常安全的来龙去脉

> 异常不是"出错就崩"，而是"出错后世界是否仍自洽"——这是 C++ 给异常立下的四档契约。

### 0.1 起源（谁·何时·为何）
异常处理思想源自 Ada 与 CLU 等；C++ 在 1980 年代末–1990 年代初（Stroustrup 与标准前委员会）引入 `try` / `catch` / `throw`。<span class="badge badge-history">史</span> 但"能抛异常"不等于"安全"——异常会打断任何一行，留下半更新的对象、锁未释、内存泄漏。<span class="badge badge-history">史</span><span class="badge badge-comment">评</span> 异常安全保证（noexcept / strong / basic / none）由 Herb Sutter 等人在 1990–2000 年代系统化成工程纪律。<span class="badge badge-history">史</span>

### 0.2 关键转折（编年）
- **C++98**：异常规范（dynamic exception specification `throw(T)`）入标准，后被证明鸡肋。<span class="badge badge-history">史</span>
- **C++11**：引入 `noexcept`（编译期、可被 `std::move_if_noexcept` 利用），废弃 `throw(T)` 动态规范。<span class="badge badge-history">史</span>
- **现代**：`noexcept` 直接决定 `std::vector` 扩容走移动还是拷贝——一行 `noexcept` 关乎性能与安全。<span class="badge badge-history">史</span>

### 0.3 设计哲学之争
"是否该有异常"本身在 C++ 社区是持久战；C++ 选择"有异常但默认不抛"的不强制，并把"强 / 基本 / 无"保证作为软性契约而非语言强制。<span class="badge badge-history">史</span><span class="badge badge-comment">评</span> `noexcept` 折中：它既是优化提示，也是接口承诺，把责任交还作者。<span class="badge badge-comment">评</span>

### 0.4 史料补遗与持续编年

0.2 停在 `noexcept` 直接决定 `std::vector` 扩容走移动还是拷贝。C++20 后异常安全从"语言机制"向"错误码替代"与"契约"延展。<span class="badge badge-history">史</span>

- **C++23 `std::expected`（P0323）提供"无异常的错误码"路径**：`std::expected<T, E>` 用值类型表达失败，完全不走 `throw` / `catch`，与异常安全四级保证并行，是 0.3 "有异常但不强制"之争的温和补充。<span class="badge badge-history">史</span>
- **契约（Contracts）提案的波折**：本计划进 C++20 的契约（`[[assert:]]` / `[[ensures]]` 等，P0542）在 2019 年被投票移出标准，后以 P2900 等重启讨论，目标是把"前置 / 后置条件"变成可被异常 / 终止强制的检查，是异常安全在"预防性"方向的延伸。<span class="badge badge-history">史</span><span class="badge badge-comment">评</span>
- **`std::error_code` / `std::system_error` 体系持续作为异常的低开销替代**：在拒绝异常的代码库（如部分大型服务 / 嵌入式）中，`std::expected` 与其并用，形成"关键路径无异常"的工程纪律。<span class="badge badge-history">史</span>
- **行业现实**：Chromium / Android 等大规模代码库长期禁用异常（`-fno-exceptions`），用错误码 + RAII（ch39）维持安全，印证 0.3 "默认不抛"的工程化选择。<span class="badge badge-history">史</span><span class="badge badge-comment">评</span>

> 史料来源：https://en.cppreference.com/w/cpp/utility/expected ｜ https://en.cppreference.com/w/cpp/error/error_code ｜ https://isocpp.github.io/CppCoreGuidelines/

!!! note "类比：异常安全 = 抛异常后世界仍自洽"
    异常安全可以**类比**为「抛异常之后世界是否仍自洽」——不是「会不会抛」，而是四种保证（noexcept / strong / basic / none）立下的契约。它**好比**电梯故障演练：不是「会不会卡」，而是卡住后乘客是否安全、楼层状态是否一致。
    换个角度：noexcept 既是优化提示也是接口承诺，直接决定 std::vector 扩容走移动还是拷贝，也**类似于**给编译器一张「我绝不抛」的保证书——它据此敢用更快的移动路径。

    > 失效边界：异常安全保证是软性契约而非语言强制；noexcept 一旦误标（实际会抛）会在边界上 terminate；Chromium / Android 等大型库长期禁用异常（-fno-exceptions）用错误码 + RAII 维持安全，证明「有异常但不强制」本身是工程化取舍，std::expected 只是并行补充。

## ① 概述：异常安全是什么，四种保证一览

[第 39 章　RAII 与 Rule of Zero/Three/Five](../part04_memory/ch39_raii_rule.md)
[第 41 章 智能指针全解（unique_ptr / shared_ptr / weak_ptr / enable_shared_from_this）](../part04_memory/ch41_smart_pointers.md)

**<span class="badge badge-std">标准</span>**　异常安全（exception safety）描述：**当异常在程序执行中途抛出时，程序应满足的不变式（invariant）与资源保证。** 它没有独立的章节标题，而是散落在 `[res.on.exception.handling]`（标准库对异常的处理）、`[basic.ctor]`、`[class.dtor]`、`[except]` 各处。C++ 社区（Sutter、Stroustrup）把异常安全归纳为**四级保证（guarantee）**：

| 等级 | 名称 | 承诺 |
|---|---|---|
| 最高 | **noexcept / nothrow** | 绝不抛异常，正常返回或 `std::terminate` |
| 高 | **strong（强）** | 操作成功，或**回滚到调用前状态**（提交或全无，commit-or-rollback） |
| 中 | **basic（基本）** | 不泄漏资源、所有对象不变量保持，但对象状态**可能改变** |
| 最低 | **none（无）** | 无承诺，可能泄漏资源、可能破坏不变量 |

**<span class="badge badge-exp">经验</span>**　关键认知：**保证等级是「最坏情况」承诺**。一个函数声明 strong 保证，意味着即便抛异常，世界也回到调用前；声明 basic，意味着可能留下「半改」的状态，但绝不泄漏、绝不崩溃到 UB。`none` 是大多数裸 C 风格代码的默认状态——这也是为什么 C++ 用 RAII（见 `ch39`）把 `none` 提升到 `basic` 甚至 `noexcept`。

本章主线：
- 四种保证精确定义与示例分级（第 2–3 节）。
- 栈展开与 double-exception（第 4 节，依赖 `ch36` 栈展开、`ch39` 析构 noexcept）。
- 异常规格历史与 `noexcept`（第 5 节）、`noexcept` 与移动的关系（第 6 节）。
- 真实 libstdc++ 源码逐行（第 7 节）、copy-and-swap（第 8 节）、`uncaught_exceptions`（第 9 节）。
- STL 异常条款（第 10 节）、构造异常（第 11 节）、`exception_ptr` 家族（第 12 节）。
- 异常成本与 Itanium zero-cost EH（第 13 节）、`-fno-exceptions` 与错误码（第 14 节）。
- 三编译器/三 STL 对比（第 15 节）、microbenchmark（第 16 节）、跨语言（第 17 节）。
- `noexcept` 优化影响（第 18 节）、工程清单（第 19 节）、源码路线（第 20 节）。

交叉引用：`ch19`（存储期，栈展开依赖自动存储期）、`ch36`（栈与堆、栈展开机制）、`ch37`（`new`/`delete` 裸资源来源）、`ch39`（RAII、析构 `noexcept` 基石）、`ch80`（容器异常保证详表）、`ch115`（移动语义，noexcept 移动的本源）。

**核心知识点 #1**：异常安全 = 抛异常后世界是否自洽；四级保证由高到低为 noexcept > strong > basic > none。

---

## ② 四种保证的精确定义

### 2.1 noexcept / nothrow（绝不抛）

**<span class="badge badge-std">标准</span>**　一个标记为 `noexcept` 的函数（见第 5 节）承诺不抛出；若其内部真的抛出，标准规定**调用 `std::terminate`**（`[except.spec]/9`），而非栈展开。这意味着 `noexcept` 不是「温柔地吞掉异常」，而是「以进程终止保证不变量」。析构函数默认隐式 `noexcept(true)`（见 `ch39`）。

**<span class="badge badge-exp">经验</span>**　`nothrow` 这一词来自 C++98 的 `operator new(std::nothrow)`——分配失败返回 `nullptr` 而非抛 `bad_alloc`。在异常安全语境里，`nothrow` 与 `noexcept` 是同一等级：不抛。

### 2.2 strong（强保证）

**<span class="badge badge-std">标准</span>**　强保证亦称「提交或回滚（commit-or-rollback）」：操作要么**完全成功**，要么**抛异常且程序状态等价于从未调用过该函数**。`std::vector::push_back` 在多数实现下提供 strong 保证（见第 3 节）。

**<span class="badge badge-exp">经验</span>**　强保证的代价是常需要「先构造新东西、成功后再替换旧东西」（copy-and-swap 即此思路，见第 8 节）。它难以在**含不可回滚外部副作用**时达成——例如「向网络发送数据后更新本地状态」：网络发送成功了就收不回，本地即使回滚，对端也已收到，强保证破裂（见第 3.4 节）。

### 2.3 basic（基本保证）

**<span class="badge badge-std">标准</span>**　基本保证：抛异常后**无资源泄漏**（`[res.on.exception.handling]/3` 要求标准库不泄漏），**所有对象的不变量仍成立**，但对**具体状态值不做回滚**——对象可能处于「其他合法但不同于调用前」的状态。

**<span class="badge badge-exp">经验</span>**　多数标准库 mutating 算法提供 basic 保证（如 `std::sort` 若比较器抛异常，序列可能乱序但仍是合法序列、无泄漏）。基本保证是「务实下限」：不崩、不漏，但调用方需重新读取状态。

### 2.4 none（无保证）

**<span class="badge badge-std">标准</span>**　无保证：`[res.on.exception.handling]` 之外、用户自己写的、会抛出且中间态可见还泄漏资源/破坏不变量的代码，即 none。标准明令**标准库函数不得提供 none 保证**（除非文档指明），但用户代码自由。

**核心知识点 #2**：noexcept 保证 = 不抛（抛则 terminate）；strong = 回滚到调用前；basic = 不漏 + 不变量保持但状态可能变；none = 无承诺。

**核心知识点 #3**：析构函数默认 noexcept(true)，是 basic/strong 保证得以成立的前提（否则栈展开会 double-exception → terminate，见 `ch39`、`ch36`）。

---

## ③ 示例：swap / push_back / operator= 的保证分级

### 3.1 swap 应为 noexcept

**<span class="badge badge-std">标准</span>**　`[swappable]` / `[algorithm.swap]`：标准库要求容器 `swap` 提供 **noexcept**（当元素 `swap` 不抛时）。libstdc++ 中 `vector::swap`：

> **示例 1** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 应为 noexcept
```cpp title="示例 1 · ★★☆☆☆"
// [示例 1] vector::swap 的 noexcept 声明（真实 libstdc++ 行号见第 7 节）
// bits/stl_vector.h:1581
// swap(vector& __x) _GLIBCXX_NOEXCEPT
#include <vector>
#include <type_traits>
int main() {
    static_assert(noexcept(std::declval<std::vector<int>&>().swap(
        std::declval<std::vector<int>&>())));
    std::vector<int> a{1,2,3}, b{4,5};
    a.swap(b);          // noexcept：O(1) 指针交换，绝不抛
}
```

**核心知识点 #4**：`std::swap` 与容器 `swap` 应为 noexcept；这是算法（如 `sort`）能在异常下保持强/基本保证的基础。

### 3.2 vector::push_back 的强保证与容量边界

**<span class="badge badge-std">标准</span>**　`[vector.modifiers]`：若 `push_back` **未触发重新分配（reallocation）**，提供 strong 保证（仅构造新元素，旧元素不动）；若**触发 reallocation**，libstdc++ 仍提供 strong 保证——因为它用 `move_if_noexcept` 在「移动可能抛」时**退化为拷贝**，拷贝抛异常可整体回滚（见第 6、7 节）。

> **示例 2** <span class="badge badge-exp">难度 ★★☆☆☆</span> · back 的强保证与容量边界
```cpp title="示例 2 · ★★☆☆☆"
// [示例 2] push_back 强保证实验：触发扩容时仍可回滚
#include <vector>
#include <iostream>
#include <stdexcept>
struct ThrowsOnCopy {
    int v;
    ThrowsOnCopy(int x=0):v(x){}
    ThrowsOnCopy(const ThrowsOnCopy&) { throw std::runtime_error("copy throws"); }
    ThrowsOnCopy(ThrowsOnCopy&&) noexcept = default;  // 移动不抛
};
int main(){
    std::vector<ThrowsOnCopy> v;
    v.reserve(1); v.emplace_back(1);                  // size=1,cap=1
    try { v.emplace_back(2); }                        // 扩容：移动不抛→直接 move，成功
    catch(...) { std::cout << "unreachable\n"; }
    // 若移动会抛而拷贝也会抛，则 realloc 的 catch 回滚到原状
}
```

### 3.3 operator= 的保证分级

**<span class="badge badge-std">标准</span>**　`[utility]/[container]/[class.copy]`：赋值运算符通常目标是 strong 保证；若无法（如多步不可回滚），至少 basic。copy-and-swap（第 8 节）是达成 strong 的标准手段。

**核心知识点 #5**：`push_back` 不扩容 = strong；扩容时靠 `move_if_noexcept` 决策仍保 strong；`swap` 恒 noexcept；`operator=` 目标 strong、退化 basic。

### 3.4 强保证为何在外部副作用前失效

**<span class="badge badge-std">标准</span>**　强保证是**纯内存/纯状态**概念，对**外部世界副作用**（I/O、网络、锁、硬件）无能为力——这些不可「回滚」。

> **示例 3** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 强保证为何在外部副作用前失效
```cpp title="示例 3 · ★★☆☆☆"
// [示例 3] 强保证破裂：网络发送不可回滚
#include <stdexcept>
#include <cstdio>
struct Ledger {
    void commit() {             // 想提供 strong 保证
        send_over_network();    // 副作用：成功则对端已收
        update_local_state();   // 若此处抛，网络已发出→无法回滚
    }
    void send_over_network(){}  // 假设成功
    void update_local_state(){ throw std::runtime_error("local fail"); }
};
int main(){
    Ledger l;
    try { l.commit(); } catch(const std::exception& e){ /* 世界已不一致 */ }
}
```

**<span class="badge badge-exp">经验</span>**　结论：对外有副作用的函数，承诺**至多 basic**；把「不可回滚的副作用」放到**最后一步**，并把可回滚的内存变更放在前面，是工程上的常用降级策略（见第 9 节 `uncaught_exceptions` 事务惯用法，正好反过来：先在析构里判断是否还在展开，再决定提交还是回滚）。

---

### 3.5 operator= 的强保证实现与退化路径

**<span class="badge badge-std">标准</span>**　赋值运算符常见三种实现，对应不同保证：
- **copy-and-swap**（第 8 节）：强保证，代价一次额外拷贝。
- **先拷贝再提交**：先把 rhs 拷到临时，成功后再「交换」内部句柄——强保证且无额外整体拷贝（仅临时）。
- **就地多步修改**：仅 basic 保证（示例 12）。

> **示例 4** <span class="badge badge-exp">难度 ★★☆☆☆</span> · = 的强保证实现与退化路径
```cpp title="示例 4 · ★★☆☆☆"
// [示例 33] 先拷贝临时再提交：强保证且比 copy-and-swap 省一次整体拷贝
#include <vector>
#include <utility>
struct Widget {
    std::vector<int> data;
    Widget& operator=(const Widget& rhs) {
        std::vector<int> tmp = rhs.data;        // 若抛，*this 未动（强）
        data.swap(tmp);                         // noexcept：提交
        return *this;
    }
    Widget& operator=(Widget&& rhs) noexcept {  // 移动不抛 → noexcept
        data = std::move(rhs.data);
        return *this;
    }
};
int main(){ Widget a, b; a = b; a = Widget{}; }
```

### 3.6 同一操作在不同类型上的保证差异

**<span class="badge badge-exp">经验</span>**　保证等级**依赖元素类型**。下面用 `is_nothrow_*` trait 在编译期自省，说明「为什么给你的类型写 noexcept 移动能提升整条调用链的保证」。

> **示例 5** <span class="badge badge-exp">难度 ★★★☆☆</span> · 同一操作在不同类型上的保证差异
```cpp title="示例 5 · ★★★☆☆"
// [示例 34] 编译期断言：noexcept 移动把 vector 移动升级为 noexcept
#include <type_traits>
#include <vector>
struct Good { Good(Good&&) noexcept = default; Good(const Good&)=default; };
struct Bad  { Bad(Bad&&); Bad(const Bad&)=default; };   // 移动抛
static_assert(std::is_nothrow_move_constructible_v<Good>);
static_assert(!std::is_nothrow_move_constructible_v<Bad>);
int main(){
    static_assert(noexcept(std::vector<Good>(std::declval<std::vector<Good>&&>())));
    // std::vector<Bad> 的移动构造不保证 noexcept：扩容回滚路径保留
}
```

## ④ 栈展开（stack unwinding）与 double-exception

**<span class="badge badge-std">标准</span>**　`[except.terminate]/1`：当异常从 `try` 块抛出，控制沿调用链向上寻找匹配的 `catch`；沿途**每个已构造的自动存储期对象按构造逆序析构**——这就是栈展开（见 `ch36`）。但若在**栈展开过程中（析构函数或栈展开代码里）又抛出新异常**，且未被立即捕获，则调用 `std::terminate`。

**<span class="badge badge-impl">实现</span>**　libstdc++ 在展开时若遇到二次抛出，由 unwinder（`__cxa_throw` → `__cxxabiv1::__forced_unwind`，见 `bits/cxxabi_forced.h`）触发 terminate。该文件中 `__forced_unwind` 是「强制展开」占位类，专用于识别「正在 terminate 流程中」的异常。

> **示例 6** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 栈展开与 double-exception
```cpp title="示例 6 · ★★☆☆☆"
// [示例 4] 栈展开：逐层析构自动变量（见 ch36）
#include <iostream>
struct Tracer {
    const char* name;
    Tracer(const char* n):name(n){ std::cout << "ctor " << name << "\n"; }
    ~Tracer(){ std::cout << "dtor " << name << "\n"; }  // 注意：非 noexcept 也行，只要不抛
};
void f(){ Tracer c("c"); throw 1; }                     // c 在抛出时析构
int main(){
    try { Tracer a("a"); Tracer b("b"); f(); }
    catch(int){ std::cout << "caught\n"; }
}
// 输出：ctor a, ctor b, ctor c, dtor c, dtor b, dtor a, caught
```

> **示例 7** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 栈展开与 double-exception
```cpp title="示例 7 · ★☆☆☆☆"
// [示例 5] double-exception → std::terminate
#include <iostream>
#include <stdexcept>
struct Bad {
    ~Bad(){ throw std::runtime_error("dtor throws"); }  // 展开中再抛
};
int main(){
    try { Bad b; throw std::runtime_error("outer"); }
    catch(...) { /* 永远到不了：dtor 抛 → terminate */ }
}
```

**<span class="badge badge-exp">经验</span>**　这就是为什么 `ch39` 反复强调**析构函数必须 `noexcept`**：一旦析构抛异常且当时正处于栈展开，立即 terminate——程序连 basic 保证都丢了。把可能抛的逻辑从析构移走，或内部 `try/catch` 吞掉并 `std::abort`/记录。

**核心知识点 #6**：栈展开 = 抛异常时沿调用链逆序析构自动对象（依赖 `ch36`）。
**核心知识点 #7**：栈展开中再抛未捕获异常 → `std::terminate`；因此析构必须 noexcept（连 `ch39`）。

---

### 4.1 set_terminate / 自定义终止行为

**<span class="badge badge-std">标准</span>**　`[except.terminate]`：`std::set_terminate` 可安装自定义终止处理函数，在 `terminate()` 被调用（含 double-exception、noexcept 违例、`[平台]` unwinder 强制展开）时执行——用于打日志/落盘/退出码，但**不得返回**（返回即 UB）。

> **示例 8** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · terminate / 自定义终止行
```cpp title="示例 8 · ★☆☆☆☆"
// [示例 39] 安装 terminate 处理器：捕获 double-exception 现场
#include <exception>
#include <iostream>
#include <cstdio>
void my_term(){ std::fprintf(stderr, "terminate called!\n"); std::abort(); }
struct Bad { ~Bad(){ throw 1; } };   // 析构抛 → 展开中再抛 → terminate
int main(){
    std::set_terminate(my_term);
    try { Bad b; throw 2; } catch(...){}
}
// 输出（到 stderr）：terminate called!  随后 abort
```

**<span class="badge badge-exp">经验</span>**　在服务器/守护进程中安装 `set_terminate` 把调用栈 dump 到日志，是定位「为何 terminate」的必备手段；但真正的防线仍是 **让析构 noexcept**（连 `ch39`），从根上消灭 double-exception。

## ⑤ 异常规格历史：从 `throw(type)` 到 `noexcept`

### 5.1 动态异常规格 `throw(T1,T2)` —— 已删除

**<span class="badge badge-std">标准</span>**　C++98 允许 `void f() throw(std::bad_alloc);` 声明「只抛这些类型」，否则 `unexpected()` → `terminate`。C++11 将其**弃用**，`[except.spec]` 在 C++17 起**删除动态异常规格**（仅保留 `throw()` 作为 `noexcept(true)` 的别名，也已废弃）。MSVC 长期接受但不强制检查（属于「注释性」）。

> **示例 9** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 动态异常规格 throw —— 已删除
```cpp title="示例 9 · ★★☆☆☆"
// [示例 6] throw(type) 动态规格：C++17 起非法（演示用 gnu++14 可编但弃用警告）
// 现代代码禁止再写。下面在 C++17+ 下编译失败：
// void old_style() throw(std::runtime_error);   // C++17 deleted
```

**<span class="badge badge-exp">经验</span>**　动态规格在运行期有成本（每次抛异常要匹配类型表），且「写着 A 实际抛 B」只会 terminate，毫无保护价值。`noexcept` 取代它，且**零运行期成本**（见第 13、18 节）。

### 5.2 noexcept 家族

**<span class="badge badge-std">标准</span>**　C++11 引入：
- `noexcept` ≡ `noexcept(true)`：承诺不抛。
- `noexcept(false)`：可能抛（也是无修饰函数的默认）。
- `noexcept(expression)`：**条件 noexcept**，当且仅当 `expression` 为 `true` 时不抛（`expression` 是**编译期 bool 常量表达式**）。
- `noexcept(expr)`：**运算符**，返回 `bool` 常量，表示「对 `expr` 求值是否可能抛」（用于条件 noexcept 内部）。

> **示例 10** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 家族
```cpp title="示例 10 · ★★☆☆☆"
// [示例 7] noexcept 运算符探测是否可能抛
#include <iostream>
#include <vector>
int main(){
    std::cout << std::boolalpha;
    std::cout << noexcept(1/0) << "\n";                 // true：内建运算不抛
    std::cout << noexcept(std::vector<int>()) << "\n";  // 依赖分配；noexcept 取决于 allocator
}
```

> **示例 11** <span class="badge badge-exp">难度 ★★★☆☆</span> · 家族
```cpp title="示例 11 · ★★★☆☆"
// [示例 8] 条件 noexcept：模板按成员操作决定自身 noexcept
#include <utility>
#include <type_traits>
struct S {
    S(S&&) noexcept;                            // 移动不抛
    S(const S&) noexcept(false);                // 拷贝抛
};
template<class T>
void move_or_copy(T& dst, T& src)
    noexcept(noexcept(T(std::declval<T&&>())))  // 若 T 移动不抛则本函数不抛
{
    dst = std::move(src);
}
int main(){ static_assert(noexcept(move_or_copy(std::declval<S&>(), std::declval<S&>()))); }
```

**核心知识点 #8**：`throw(type)` 动态规格 C++11 弃用、C++17 删除，仅 `throw()` 残存为 `noexcept(true)` 别名。
**核心知识点 #9**：`noexcept` ≡ `noexcept(true)`；`noexcept(bool)` 为条件规格；`noexcept(expr)` 是编译期运算符。

---

## ⑥ noexcept 与移动：vector 扩容的决策

**<span class="badge badge-std">标准</span>**　这是本章最重要的工程点。`std::vector` 扩容需把旧缓冲元素搬到新缓冲。若用**移动构造**且移动**可能抛**，则「搬了一半」时抛异常——已搬的元素在新缓冲、未搬的还在旧缓冲，旧对象还部分存活，**状态损坏**，违反 strong/basic 保证。因此 `[vector.modifiers]` 的精神（libstdc++ 实现）规定：**仅当元素移动构造为 `is_nothrow_move_constructible` 时，才用移动；否则用拷贝**（拷贝若抛，可整体回滚，因旧缓冲仍完整）。

**<span class="badge badge-impl">实现</span>**　libstdc++ 用 `std::move_if_noexcept` 实现该决策（第 7 节逐行）。语义：`move_if_noexcept(x)` 返回 `x` 的**右值引用**当且仅当移动构造不抛且可移动；否则返回 **`const T&`**（强制走拷贝）。`copy-and-swap` 之外，这是标准库「用 noexcept 信息保强保证」的核心机制。

> **示例 12** <span class="badge badge-exp">难度 ★★★☆☆</span> · 与移动：vector 扩容的决策
```cpp title="示例 12 · ★★★☆☆"
// [示例 9] move_if_noexcept 决策演示
#include <utility>
#include <type_traits>
#include <iostream>
struct NoThrowMove { NoThrowMove(NoThrowMove&&) noexcept; NoThrowMove(const NoThrowMove&); };
struct ThrowMove    { ThrowMove(ThrowMove&&);            ThrowMove(const ThrowMove&); };
int main(){
    // 这两个类型只声明了移动/拷贝构造（无默认构造），因此不能写 `NoThrowMove a;`。
    // move_if_noexcept 的返回类型判定是纯编译期的，用 declval 提供左值即可，无需真正建对象。
    // 对 NoThrowMove：移动不抛 → move_if_noexcept 返回 T&&（走移动）
    static_assert(std::is_same_v<
        decltype(std::move_if_noexcept(std::declval<NoThrowMove&>())), NoThrowMove&&>);
    // 对 ThrowMove：移动抛、可拷贝 → 返回 const T&（走拷贝）
    static_assert(std::is_same_v<
        decltype(std::move_if_noexcept(std::declval<ThrowMove&>())), const ThrowMove&>);
    // 行为：vector 扩容时对 ThrowMove 用拷贝，对 NoThrowMove 用移动
}
```

> **示例 13** <span class="badge badge-exp">难度 ★★★☆☆</span> · 与移动：vector 扩容的决策
```cpp title="示例 13 · ★★★☆☆"
// [示例 10] 扩容实验：移动抛（非 noexcept）→ move_if_noexcept 走拷贝 → 扩容成功
#include <vector>
#include <utility>
#include <type_traits>
#include <iostream>
struct M {
    int v=0;
    M(int x=0):v(x){}
    M(M&& o) noexcept(false) { v=o.v; throw "move throws"; }            // 移动抛，且未标 noexcept
    M(const M& o):v(o.v){ std::cout << "  [copy] v=" << o.v << "\n"; }  // 拷贝安全
};
int main(){
    std::vector<M> v; v.reserve(1); v.emplace_back(1);
    std::cout << "is_nothrow_move_constructible<M> = "
              << std::is_nothrow_move_constructible<M>::value << "\n";
    v.emplace_back(2);                                                  // 扩容：move_if_noexcept 见移动非 noexcept → 改用拷贝
    std::cout << "after: size=" << v.size() << "（扩容成功，走拷贝，未抛异常）\n";
}
```

**[实验·本机实测]** 真机输出（GCC 15.3.0 `-O0 -std=c++17 -static`）：

```text
is_nothrow_move_constructible<M> = 0
  [copy] v=1
after: size=2（扩容成功，走拷贝，未抛异常）
```

> 关键结论：`M` 移动构造是 `noexcept(false)`，故 `is_nothrow_move_constructible<M> = 0`；`vector` 扩容时 `move_if_noexcept` 据此**改用拷贝**（输出 `[copy] v=1`），拷贝安全不抛 → 扩容直接成功到 `size=2`，**根本没有异常、没有回滚**。这正是 strong 保证的实现方式——「移动可能抛就改走拷贝」在**源头**规避「搬一半抛异常」的状态损坏；「回滚」是另一场景（拷贝也抛时 `_M_realloc_insert` 的 catch 分支才触发，见第 7.2 节）。

**<span class="badge badge-exp">经验</span>**　**给你的类型写 `noexcept` 移动构造/移动赋值**——这是让 `vector`/`deque`/`string` 在扩容、排序、resize 时**用移动而非拷贝**的唯一开关，既保强保证又获性能（第 16、18 节 microbenchmark）。`ch115` 详述移动语义。

**核心知识点 #10**：vector 扩容若移动构造可能抛，会损坏状态，故仅当 `is_nothrow_move_constructible` 才移动，否则拷贝。
**核心知识点 #11**：`std::move_if_noexcept` 在移动不抛时返回 `T&&`、否则返回 `const T&` 强制拷贝。

---

### 6.1 trait 实战：用 is_nothrow_* 编写「自适应」异常安全代码

**<span class="badge badge-std">标准</span>**　`<type_traits>` 的 `is_nothrow_move_constructible`、`is_nothrow_swappable`、`is_nothrow_default_constructible` 等是编译期布尔常量，是标准库做 noexcept 决策的同一组工具（第 7 节 `move_if_noexcept` 内部即用 `is_nothrow_move_constructible`）。用户代码可复用它们编写「若元素够强则优化、否则回退」的泛型逻辑。

> **示例 14** <span class="badge badge-exp">难度 ★★★☆☆</span> · 实战：用 isnothrow 编写
```cpp title="示例 14 · ★★★☆☆"
// [示例 41] 泛型容器包装：移动不抛才 relocate，否则拷贝（复刻标准库思路）
#include <type_traits>
#include <utility>
#include <vector>
#include <iostream>
template<class T>
void relocate_or_copy(std::vector<T>& dst, std::vector<T>& src){
    if constexpr (std::is_nothrow_move_constructible_v<T>) {
        dst.insert(dst.end(), std::make_move_iterator(src.begin()),
                                 std::make_move_iterator(src.end()));  // 快路径
        std::cout << "relocated (noexcept move)\n";
    } else {
        dst.insert(dst.end(), src.begin(), src.end());                 // 安全路径
        std::cout << "copied (move may throw)\n";
    }
}
// 用户一旦声明移动构造，拷贝/移动赋值会被隐式删除；vector::insert 内部的
// move_backward 需要赋值运算符，故必须一并补齐，否则实例化时报错。
struct Safe { Safe(Safe&&) noexcept = default; Safe(const Safe&)=default;
              Safe& operator=(Safe&&) noexcept = default; Safe& operator=(const Safe&)=default; };
struct Unsafe { Unsafe(Unsafe&&); Unsafe(const Unsafe&)=default;
                Unsafe& operator=(Unsafe&&); Unsafe& operator=(const Unsafe&)=default; };
int main(){
    std::vector<Safe> a,b;   relocate_or_copy(a,b);                    // relocated
    std::vector<Unsafe> c,d; relocate_or_copy(c,d);                    // copied
}
```

**<span class="badge badge-exp">经验</span>**　`if constexpr` + `is_nothrow_*` 是「零成本分支」：非活跃分支根本不编译进二进制。这是把「异常安全信息转成性能开关」的标准现代写法（连 `ch115` 移动、`ch19`）。

## ⑦ 真实 libstdc++ 源码逐行

以下均来自本机 `C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/` 真实文件。

### 7.1 `bits/move.h:108-126` —— move_if_noexcept 本体

> **示例 15** <span class="badge badge-exp">难度 ★★★☆☆</span> · bits/move.h:108-12
```cpp title="示例 15 · ★★★☆☆"
108	  template<typename _Tp>
109	    struct __move_if_noexcept_cond
110	    : public __and_<__not_<is_nothrow_move_constructible<_Tp>>,
111	                    is_copy_constructible<_Tp>>::type { };
112	
113	  /**
114	   *  @brief  Conditionally convert a value to an rvalue.
...
121	  template<typename _Tp>
122	    _GLIBCXX_NODISCARD
123	    constexpr
124	    __conditional_t<__move_if_noexcept_cond<_Tp>::value, const _Tp&, _Tp&&>
125	    move_if_noexcept(_Tp& __x) noexcept
126	    { return std::move(__x); }
```

**逐行**：
- `109-111`：`__move_if_noexcept_cond<_Tp>` 是一个 trait，当「**移动构造可能抛** 且 **可拷贝**」时为 `true`。即「需要退化为拷贝」的条件。
- `124`：返回类型用 `__conditional_t`——若条件为 `true` 则返回 `const _Tp&`（左值引用，强制拷贝构造）；否则返回 `_Tp&&`（右值引用，走移动）。
- `125`：函数本身 `noexcept`（它只是做引用转换，绝不抛）。
- `126`：无论哪种，实现都是 `std::move(__x)`——区别在**返回类型**决定了后续调用的是移动还是拷贝构造。

### 7.2 `bits/vector.tcc:477-523` —— _M_realloc_insert 的 realloc + 回滚

> **示例 16** <span class="badge badge-exp">难度 ★★☆☆☆</span> · bits/vector.tcc:47
```text
477	  if _GLIBCXX17_CONSTEXPR (_S_use_relocate())
478	    {
479	      __new_finish = _S_relocate(__old_start, __position.base(),
480	                                 __new_start, _M_get_Tp_allocator());
...
488	  else
489	    {
491	      __new_finish
492	        = std::__uninitialized_move_if_noexcept_a
493	          (__old_start, __position.base(), __new_start, _M_get_Tp_allocator());
...
504	  __catch(...)
505	    {
506	      if (!__new_finish)
507	        _Alloc_traits::destroy(this->_M_impl, __new_start + __elems_before);
508	      else
509	        std::_Destroy(__new_start, __new_finish, _M_get_Tp_allocator());
510	      _M_deallocate(__new_start, __len);
511	      __throw_exception_again;        // 重新抛出，调用方看到原异常
512	    }
```

**逐行**：
- `477`：`_S_use_relocate()` 为真（元素可 noexcept relocate，见 7.3）时直接整体 relocate——最快路径。
- `492`：`__uninitialized_move_if_noexcept_a` 内部即用 `move_if_noexcept` 的迭代器：移动不抛→move，否则 copy（见 `bits/stl_uninitialized.h:393-401`）。
- `504-512`：**回滚核心**：若中途抛异常，已构造的新元素被 `_Destroy`、新缓冲被 `_M_deallocate` 释放，然后 `__throw_exception_again` 原样抛出。**旧缓冲从未被改动**，故 `push_back` 提供 strong 保证。
- 这正对应示例 2、10。

### 7.3 `bits/stl_vector.h:462-509` —— _S_use_relocate / noexcept 决策

> **示例 17** <span class="badge badge-exp">难度 ★★★☆☆</span> · bits/stlvector.h:4
```text
464	  static constexpr bool
465	  _S_nothrow_relocate(true_type)
466	  {
467	    return noexcept(std::__relocate_a(std::declval<pointer>(),
468	                                      std::declval<pointer>(),
469	                                      std::declval<pointer>(),
470	                                      std::declval<_Tp_alloc_type&>()));
471	  }
477	  static constexpr bool
478	  _S_use_relocate()
479	  {
483	    return _S_nothrow_relocate(__is_move_insertable<_Tp_alloc_type>{});
484	  }
486	  static pointer
487	  _S_do_relocate(..., true_type) noexcept
488	  { return std::__relocate_a(__first, __last, __result, __alloc); }
```

**逐行**：`_S_use_relocate()` 在**编译期**判定「能否无异常地把元素从旧缓冲 relocate 到新缓冲」（`__relocate_a` 的 `noexcept` 决定）。若能，realloc 走 7.2 的 `if` 分支（整段移动、最快且 noexcept）；否则走 `move_if_noexcept` 分支。`_S_do_relocate` 本身标 `noexcept`——因为它只在已确认 nothrow 时被调用。

### 7.4 `bits/exception_ptr.h:60-112` —— exception_ptr / current / rethrow

> **示例 18** <span class="badge badge-exp">难度 ★★★☆☆</span> · bits/exceptionptr.
```cpp title="示例 18 · ★★★☆☆"
61	  namespace __exception_ptr { class exception_ptr; }
66	  using __exception_ptr::exception_ptr;
75	  exception_ptr current_exception() _GLIBCXX_USE_NOEXCEPT;
78	  template<typename _Ex> exception_ptr make_exception_ptr(_Ex) _GLIBCXX_USE_NOEXCEPT;
81	  void rethrow_exception(exception_ptr) __attribute__ ((__noreturn__));
97	    class exception_ptr {
99	      void* _M_exception_object;
101	      explicit exception_ptr(void* __e) _GLIBCXX_USE_NOEXCEPT;
103	      void _M_addref() _GLIBCXX_USE_NOEXCEPT;
104	      void _M_release() _GLIBCXX_USE_NOEXCEPT;
```

**逐行**：`exception_ptr` 是**不透明句柄**（内部只持 `void* _M_exception_object` 指向异常对象）；`current_exception()` 取当前处理中异常的句柄；`rethrow_exception()` 标 `__noreturn__`（总会抛或 terminate）；引用计数通过 `_M_addref/_M_release` 管理生命周期，故可跨作用域/线程传递（第 12 节）。

### 7.5 `exception:121-130` —— uncaught_exception / uncaught_exceptions

> **示例 19** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · exception:121-130
```text
121	  _GLIBCXX17_DEPRECATED_SUGGEST("std::uncaught_exceptions()")
122	  bool uncaught_exception() _GLIBCXX_USE_NOEXCEPT __attribute__ ((__pure__));
124	  #if __cplusplus >= 201703L || !defined(__STRICT_ANSI__)
125	  #define __cpp_lib_uncaught_exceptions 201411L
130	  int uncaught_exceptions() _GLIBCXX_USE_NOEXCEPT __attribute__ ((__pure__));
```

**逐行**：`uncaught_exception()`（C++17 起弃用，建议用 `uncaught_exceptions()`）返回「是否有未捕获异常」；`uncaught_exceptions()` 返回**当前未捕获异常的个数**（C++17 引入，用于嵌套检测）。两者都 `noexcept` 且 `__pure__`（无副作用）。第 9 节用其实现事务惯用法。

### 7.6 `bits/cxxabi_forced.h:39-55` —— __forced_unwind

> **示例 20** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · bits/cxxabiforced.
```text
39	  namespace __cxxabiv1 {
48	    class __forced_unwind {
50	      virtual ~__forced_unwind() throw();
53	      virtual void __pure_dummy() = 0;
54	    };
```

**逐行**：`__forced_unwind` 是「强制展开」占位异常类，由 `std::terminate` 在栈展开时抛出以驱动 unwinder；其析构 `throw()`（noexcept）、`__pure_dummy` 阻止按值捕获。这是平台级展开机制的内部件（`[平台]`）。

**核心知识点 #12**：`move_if_noexcept` 靠返回类型 `T&&`/`const T&` 分流移动与拷贝；vector realloc 在 `__catch(...)` 中回滚并原样重抛，保 strong 保证。
**核心知识点 #23**：`_S_use_relocate()` 在编译期判定能否 noexcept relocate，决定 realloc 走最快路径还是 move_if_noexcept 路径。

---

## ⑧ copy-and-swap 惯用法（强保证）

**<span class="badge badge-std">标准</span>**　copy-and-swap 是用户类型达成**强保证赋值**的经典惯用法，依赖 `ch39` 的 RAII 与 `swap` 的 noexcept（第 3.1 节）。

**<span class="badge badge-impl">实现</span>**　机制：`T& operator=(T other) { swap(*this, other); return *this; }`——
1. `other` 是**按值参数**，由调用方的实参**拷贝（或移动）构造**而来。若此构造抛出，异常发生在 `swap` 之前，`*this` **毫发未动** → 自动强保证。
2. `swap` 是 noexcept（第 3.1 节）→ 交换绝不抛。
3. 返回前 `other`（旧状态）随函数退出析构 → 资源释放。

> **示例 21** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 惯用法（强保证）
```cpp title="示例 21 · ★★☆☆☆"
// [示例 11] copy-and-swap：强保证赋值
#include <utility>
#include <vector>
#include <cstddef>
class Buffer {
    std::vector<int> d_;
public:
    Buffer() = default;
    Buffer(const Buffer& o): d_(o.d_) {}        // 拷贝可能抛，但在 swap 前
    Buffer(Buffer&&) noexcept = default;        // 移动不抛
    Buffer& operator=(Buffer other) noexcept {  // 按值：拷贝/移动构造
        swap(*this, other);                     // noexcept 交换
        return *this;                           // other 析构释放旧资源
    }
    friend void swap(Buffer& a, Buffer& b) noexcept {
        using std::swap; swap(a.d_, b.d_);
    }
};
int main(){ Buffer x, y; x = y; }               // 若拷贝抛，x 不变（强保证）
```

> **示例 22** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 惯用法（强保证）
```cpp title="示例 22 · ★☆☆☆☆"
// [示例 12] 对比：朴素赋值仅 basic 保证（中途抛→半改状态）
#include <vector>
struct Naive {
    std::vector<int> a, b;
    Naive& operator=(const Naive& o) {  // 两步拷贝，第一步成功后第二步抛→半改
        a = o.a;                        // 成功
        b = o.b;                        // 若抛，a 已改，o 未变 → 状态不一致(basic)
        return *this;
    }
};
```

**<span class="badge badge-exp">经验</span>**　代价：copy-and-swap **总有一次额外拷贝**（即便 `rhs` 是右值也会走移动构造——还好，移动廉价；但左值会真的多拷贝一次）。性能敏感且能证明中间态可被局部回滚时，可手写「先改临时再 swap」或直接分两步并保 basic。强保证不是免费的——这是它「安全换性能」的本质（呼应第 3.4 节）。

**核心知识点 #13**：copy-and-swap 用「按值参数 + noexcept swap」把强保证化简为「构造可能抛（但 *this 未动） + 交换不抛」，代价是一次额外拷贝。

---

### 8.1 copy-and-swap 的代价可测量

**<span class="badge badge-exp">经验</span>**　强保证不是免费。copy-and-swap 在 rhs 是左值时**多一次完整拷贝**。下面量化「强保证赋值」与「basic 赋值」的性能差——权衡依据是：拷贝成本 vs 回滚需求。

> **示例 23** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 的代价可测量
```cpp title="示例 23 · ★★☆☆☆"
// [示例 35] copy-and-swap 与 in-place 赋值的代价对比（量级）
#include <vector>
#include <chrono>
#include <iostream>
struct Blob { std::vector<int> d = std::vector<int>(64); };
Blob& cas_assign(Blob& self, Blob other) noexcept {  // copy-and-swap
    using std::swap; swap(self.d, other.d); return self;
}
Blob& inl_assign(Blob& self, const Blob& o) {        // 就地（basic，无额外拷贝）
    self.d = o.d; return self;
}
int main(){
    const int N = 5'000'000;
    Blob a, b;
    auto t0=std::chrono::steady_clock::now();
    for(int i=0;i<N;++i) cas_assign(a,b);
    auto t1=std::chrono::steady_clock::now();
    for(int i=0;i<N;++i) inl_assign(a,b);
    auto t2=std::chrono::steady_clock::now();
    std::cout<<"copy-and-swap="<<std::chrono::duration<double,std::milli>(t1-t0).count()<<"ms\n";
    std::cout<<"in-place     ="<<std::chrono::duration<double,std::milli>(t2-t1).count()<<"ms\n";
}
// 量级：copy-and-swap 多一次拷贝，明显更慢；故"仅当强保证必需时才用"
```

## ⑨ std::uncaught_exceptions（C++17）：提交或回滚惯用法

**<span class="badge badge-std">标准</span>**　`[except.uncaught]` / `uncaught_exceptions()` 返回当前未捕获异常个数（≥1 表示正处于栈展开中）。C++17 加入以支持「**在析构中判断自己是否因异常而析构**」，从而区分「正常析构→提交」与「栈展开析构→回滚」。

**<span class="badge badge-impl">实现</span>**　典型用于「事务/日志/批量写入」：构造时记录 `int init = std::uncaught_exceptions();`，析构时比较 `std::uncaught_exceptions() > init`：若更大，说明**在自己生命周期内又发生了新异常（正在展开）→ 回滚**；否则→**提交**。

> **示例 24** <span class="badge badge-exp">难度 ★★☆☆☆</span> · std::uncaught_exceptions（C++17）：提交或回滚惯用法
```cpp title="示例 24 · ★★☆☆☆"
// [示例 13] 事务惯用法：展开中析构→回滚，正常析构→提交
#include <exception>
#include <cstdio>
struct Transaction {
    int init_ = std::uncaught_exceptions();  // 构造时快照
    void commit(){ std::printf("COMMIT data\n"); }
    void rollback(){ std::printf("ROLLBACK data\n"); }
    ~Transaction() {
        if (std::uncaught_exceptions() > init_)
            rollback();                      // 因异常展开→不提交
        else
            commit();                        // 正常离开作用域→提交
    }
};
int main(){
    try {
        Transaction t;                       // init_ = 0
        throw 1;                             // 抛→展开，t 析构时 uncaught=1>0
    } catch(int){}
    Transaction t2;                          // 正常析构，uncaught=0 → 提交
}
// 输出：ROLLBACK data  (t) \n COMMIT data (t2)
```

> **示例 25** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · std::uncaught_exceptions（C++17）：提交或回滚惯用法
```cpp title="示例 25 · ★☆☆☆☆"
// [示例 14] uncaught_exceptions 计数（嵌套）
#include <exception>
#include <iostream>
struct P { ~P(){ std::cout << "uncaught=" << std::uncaught_exceptions() << "\n"; } };
int main(){
    try { P p; throw 1; }   // p 析构时仍有 1 个未捕获异常
    catch(int){}
}
```

**<span class="badge badge-exp">经验</span>**　`uncaught_exception()`（单数，C++17 弃用）只回答「是否 >0」，无法区分「是本对象导致的展开」还是「进入前就有」。`uncaught_exceptions()` 用**计数差**解决，是 `gsl::final_action` / `std::experimental::scope_exit` 的底层机制（libstdc++ `experimental/scope:162,216` 即用此计数）。

**核心知识点 #14**：`uncaught_exceptions()`（C++17）返回未捕获异常个数；用「析构时计数 > 构造时计数」判断是否在栈展开，实现提交/回滚。

---

## ⑩ 异常安全的 STL 条款 [res.on.exception.handling]

**<span class="badge badge-std">标准</span>**　`[res.on.exception.handling]` 规定标准库对异常的总体承诺：
- （1）标准库函数若抛，必抛自 `std::exception` 派生的类型（或 `bad_alloc` 等标准类型）。
- （2）标准库函数**不得泄漏资源**、**不得破坏容器不变量**（即至少 basic 保证）。
- （3）特定操作有更强保证：`swap`、`clear`、`erase`（单元素，不重分配时）等多为 noexcept 或 strong；`push_back`/`insert` 在重分配时仍 strong（靠 move_if_noexcept，第 6、7 节）。
- （4）**析构函数不得抛**（否则展开中 terminate，见 `ch39`、`ch36`）。

**<span class="badge badge-impl">实现</span>**　libstdc++ 各容器在 realloc/insert 中统一用 `__uninitialized_move_if_noexcept_a` + `__catch` 回滚（见 7.2、7.3），即该条款的实现落点。

> **示例 26** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 异常安全的 STL 条款 [res.on.exception.handling]
```cpp title="示例 26 · ★☆☆☆☆"
// [示例 15] STL 基本保证验证：sort 比较器抛→无泄漏但序列可能乱序
#include <algorithm>
#include <vector>
#include <stdexcept>
int main(){
    std::vector<int> v{3,1,2};
    try {
        std::sort(v.begin(), v.end(), [](int a,int b){
            if (a==2) throw std::runtime_error("cmp throws"); return a<b; });
    } catch(...) { /* v 仍合法（无泄漏），但顺序未定义 */ }
}
```

**核心知识点 #15**：`[res.on.exception.handling]` 承诺标准库至少 basic（不漏、不变量保持）、特定操作 noexcept/strong；析构不抛。

---

### 10.1 常见 STL 操作的保证等级详表

**<span class="badge badge-std">标准</span>**　`[res.on.exception.handling]` 与各容器条款的具体落点（连 `ch80` 容器异常保证详表）：

| 操作 | 保证 | 备注 |
|---|---|---|
| `v.swap(v2)` | **noexcept**（元素 swap 不抛时） | O(1) 指针交换 |
| `v.push_back(x)` 不扩容 | **strong** | 仅构造新元素，旧不动 |
| `v.push_back(x)` 扩容 | **strong** | 靠 move_if_noexcept，抛则回滚 |
| `v.emplace_back(x)` | **strong** | 同上 |
| `v.insert(p, x)` 不扩容 | **strong** | 元素右移可能抛→回滚 |
| `v.insert(p, x)` 扩容 | **strong** | 同上 |
| `v.resize(n)` | **basic/strong** | 新增/销毁元素；异常时状态合法 |
| `v.clear()` | **noexcept** | 仅析构，析构不抛 |
| `v.erase(p)` 单元素 | **strong** | 其余元素前移 |
| `std::sort(first,last)` | **basic** | 比较器抛→序列合法但顺序未定义 |
| `std::find` / `std::for_each` | **strong** | 算法本身不修改（只读） |
| `std::vector` 移动构造/赋值 | **noexcept**（默认分配器） | O(1) 指针接管 |
| `std::unordered_map::rehash` | **basic** | 重哈希中抛→部分迁移，无泄漏 |

**<span class="badge badge-exp">经验</span>**　记住一句话：**「不修改已有元素、只追加/交换」的操作多 strong；「重排/重哈希」多 basic；「纯析构」多 noexcept**。这是判断任何标准库调用安全等级的心算公式。

## ⑪ 构造函数中的异常：成员自动析构

**<span class="badge badge-std">标准</span>**　`[except.ctor]/1`：若构造函数通过异常退出，则**已构造的基类子对象与成员子对象按逆序自动析构**，对象本身的内存被释放——**无资源泄漏**。这正是 RAII 与异常安全衔接点（见 `ch39`）。

> **示例 27** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 构造函数中的异常：成员自动析构
```cpp title="示例 27 · ★☆☆☆☆"
// [示例 16] 构造失败→已初始化成员自动析构
#include <iostream>
#include <stdexcept>
struct M { M(){ std::cout << "M ctor\n"; } ~M(){ std::cout << "M dtor\n"; } };
struct N { N(){ std::cout << "N ctor\n"; throw std::runtime_error("N fails"); } ~N() noexcept {} };
struct C {
    M m;  // 先构造
    N n;  // 构造抛→m 自动析构
};
int main(){ try { C c; } catch(const std::exception&){ std::cout << "caught\n"; } }
// 输出：M ctor, N ctor, M dtor, caught
```

**<span class="badge badge-exp">经验</span>**　推论：**成员用 RAII 类型（智能指针、容器）即可在构造失败后无泄漏**；若成员是裸指针/裸句柄，必须放在构造函数的函数体（try 块）里获取，并在 catch 中手动释放（或更好：改用 RAII 成员）。这正是 Rule of Zero（`ch39`、`ch41`）的价值。

**核心知识点 #16**：构造函数抛异常 → 已构造的基类/成员子对象逆序自动析构、对象内存释放，无泄漏。

---

## ⑫ std::current_exception / rethrow_exception / exception_ptr

**<span class="badge badge-std">标准</span>**　`[exception.ptr]`（C++11）：`std::exception_ptr` 是不透明句柄，可持有任意异常对象（含非 `std::exception` 派生类型）。`current_exception()` 在 `catch` 中取当前异常句柄；`rethrow_exception(p)` 重新抛出；`make_exception_ptr(e)` 从值造句柄。用于**跨线程传递异常**（worker 线程捕获、主线程重抛）。

**<span class="badge badge-impl">实现</span>**　libstdc++ 中 `exception_ptr` 内部是 `void* _M_exception_object`，引用计数管理（7.4）。`rethrow_exception` 标 `__noreturn__`。

> **示例 28** <span class="badge badge-exp">难度 ★★☆☆☆</span> · exception / rethro
```cpp title="示例 28 · ★★☆☆☆"
// [示例 17] 跨线程传递异常：worker 捕获，主线程重抛
#include <exception>
#include <thread>
#include <iostream>
#include <stdexcept>
int main(){
    std::exception_ptr ep;
    std::thread t([&]{ try { throw std::runtime_error("in thread"); }
                       catch(...) { ep = std::current_exception(); } });
    t.join();
    if (ep) {
        try { std::rethrow_exception(ep); }
        catch(const std::exception& e){ std::cout << "relayed: " << e.what() << "\n"; }
    }
}
```

> **示例 29** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · exception / rethro
```cpp title="示例 29 · ★☆☆☆☆"
// [示例 18] make_exception_ptr 直接构造句柄
#include <exception>
#include <iostream>
int main(){
    auto ep = std::make_exception_ptr(std::runtime_error("boom"));
    try { std::rethrow_exception(ep); }
    catch(const std::exception& e){ std::cout << e.what() << "\n"; }
}
```

**核心知识点 #17**：`exception_ptr` 是不透明句柄，可跨作用域/线程持有异常；`current_exception`/`rethrow_exception`/`make_exception_ptr` 构成异常转发三件套。

---

## ⑬ 异常成本：Itanium zero-cost EH

**<span class="badge badge-std">标准</span>**　`[实现]/[平台]`：在 GCC/Clang（Linux/macOS/MinGW 默认）使用 **Itanium C++ ABI** 的 zero-cost exception handling。**「zero-cost」指正常（不抛）路径零运行时开销**——编译器不插入任何异常检查指令，仅把展开信息写入独立的只读段（`.eh_frame` / `.gcc_except_table`，LSDA = Language-Specific Data Area）。

**<span class="badge badge-platform">平台</span>**　代价结构：
- **正常路径**：几乎零开销（仅多占一点代码/数据段存放表）。`try/catch` 本身在正常执行时不耗时（microbenchmark 见第 16 节）。
- **抛异常路径**：需**运行时查表**、解卷（unwind）、逐帧执行析构、匹配 `catch`——代价在 **数百 ns 到数 µs** 量级（取决于栈深度、析构数量、表大小）。

> **示例 30** <span class="badge badge-exp">难度 ★★★★☆</span> · 异常成本：Itanium zero-cost EH
```cpp title="示例 30 · ★★★★☆"
// [示例 19] 验证 try/catch 正常路径零/近零开销
#include <chrono>
#include <iostream>
volatile int sink = 0;
int main(){
    const int N = 100'000'000;
    auto t0 = std::chrono::steady_clock::now();
    for (int i=0;i<N;++i){ try { sink += i; } catch(...){} }  // 永不抛
    auto t1 = std::chrono::steady_clock::now();
    for (int i=0;i<N;++i){ sink += i; }                       // 无 try/catch
    auto t2 = std::chrono::steady_clock::now();
    auto a = std::chrono::duration_cast<std::chrono::milliseconds>(t1-t0).count();
    auto b = std::chrono::duration_cast<std::chrono::milliseconds>(t2-t1).count();
    std::cout << "with try/catch=" << a << "ms  without=" << b << "ms\n";
    // 两者接近：正常路径 try/catch 不显著变慢（Itanium zero-cost）
}
```

> **示例 31** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 异常成本：Itanium zero-cost EH
```cpp title="示例 31 · ★★☆☆☆"
// [示例 20] 抛异常延迟量级（仅量级参考）
#include <chrono>
#include <iostream>
int main(){
    const int N = 100'000;
    int caught = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (int i=0;i<N;++i){
        try { throw i; } catch(int){ ++caught; }
    }
    auto t1 = std::chrono::steady_clock::now();
    double us = std::chrono::duration<double,std::micro>(t1-t0).count()/N;
    std::cout << "throw+catch avg=" << us << " us per op\n";  // 通常 ~0.x–数 µs
}
```

**<span class="badge badge-exp">经验</span>**　结论：**用异常表达「真正罕见」的错误路径是正确的**——它几乎不污染热路径；但**不要用异常做常规控制流**（每次抛都是 µs 级，比 `if` 慢几个数量级）。Windows 的 SEH/`-EHa` 模型不同（第 15 节），其「零成本」假设弱一些。

**核心知识点 #18**：Itanium zero-cost EH：正常路径零运行期检查（仅查表段），异常路径查 `.eh_frame`/LSDA 展开，代价数百 ns–µs 级。

---

### 13.1 实地查看展开表：objdump / .eh_frame

**<span class="badge badge-platform">平台</span>**　zero-cost EH 的展开信息写在可执行文件的只读段。用 `objdump` 可验证「noexcept 函数确实没有展开表」：

```bash
# 对示例 26 生成的 a.out
objdump -h a.out | grep -E "eh_frame|\.gcc_except"
# .eh_frame    节存在（所有函数共用描述），但 noexcept 函数不分配 LSDA 描述
# g++ -fno-exceptions 时 .eh_frame 完全消失，二进制更小
```

> **示例 32** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 实地查看展开表：objdump / .eh_frame
```cpp title="示例 32 · ★☆☆☆☆"
// [示例 36] 用 __builtin 观察：noexcept 让编译器相信不会展开
#include <vector>
[[gnu::cold]] void log_fail(const char*);
void writer(std::vector<int>& v) noexcept {  // 编译器可省略展开注册
    v.push_back(1);                          // 即便内部可能"逻辑失败"，noexcept 承诺不抛
}
void writer_throw(std::vector<int>& v) {     // 保留完整展开表
    v.push_back(1);
}
int main(){ std::vector<int> v; writer(v); writer_throw(v); }
// 编译：g++ -O2 -S ch40_ex36.cpp；对比 writer / writer_throw 的 .cfi 指令条数
```

**<span class="badge badge-exp">经验</span>**　`.eh_frame` 占二进制体积但不占运行期；`-fno-exceptions` 彻底移除它，是嵌入式/游戏追求小体积的正当理由（代价见第 14 节）。

## ⑭ -fno-exceptions / 何时用异常 vs 错误码

### 14.1 -fno-exceptions

**<span class="badge badge-std">标准</span>/<span class="badge badge-platform">平台</span>**　GCC/Clang 的 `-fno-exceptions` 禁止异常机制：所有 `throw` 编译失败或 `std::terminate`，`try/catch` 无效，且库/生成代码更小更快（无展开表）。嵌入式、游戏、内核常开。代价：标准库容器等在无法分配时会 `std::abort` 而非抛 `bad_alloc`，且 `vector` 扩容的 strong 保证退化为「失败即终止」。

> **示例 33** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 异常安全
```cpp title="示例 33 · ★☆☆☆☆"
// [示例 21] -fno-exceptions 下需避免异常，改用错误码/必成功假设
// 编译：g++ -fno-exceptions 时下面无法通过 throw 表达错误
#include <cstdio>
// 替代：返回 bool 表示成功
bool parse(const char* s, int& out){
    if (!s) return false;          // 错误码代替异常
    out = 0; return true;
}
int main(){ int v; if(!parse(nullptr, v)) std::printf("fail\n"); }
```

### 14.2 异常 vs 错误码（std::error_code / std::expected）

**<span class="badge badge-std">标准</span>**　C++11 `std::error_code`/`std::error_condition`、C++17 `std::optional`、C++23 `std::expected<T,E>`（见后续章）提供**无异常的错误传递**。选择原则：
- **异常**：真正「罕见、跨多层、需展开栈」的错误（构造失败、I/O、解析失败）。
- **错误码/expected**：**可预期、频繁、调用方立即处理**的错误（如 `open` 失败、`find` 未命中）。
- **零开销要求 / `-fno-exceptions` 环境**：只能错误码。

> **示例 34** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 异常 vs 错误码
```cpp title="示例 34 · ★☆☆☆☆"
// [示例 22] std::expected（C++23）无异常错误传递
#include <expected>
#include <string>
#include <iostream>
std::expected<int, std::string> to_int(const char* s){
    if (!s || !*s) return std::unexpected(std::string("empty"));
    return std::atoi(s);              // 成功路径无异常、零展开开销
}
int main(){
    auto r = to_int(nullptr);
    if (!r) std::cout << "err: " << r.error() << "\n";
    else    std::cout << "ok: " << *r << "\n";
}
```

> **示例 35** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 异常 vs 错误码
```cpp title="示例 35 · ★☆☆☆☆"
// [示例 23] std::error_code 风格（C++11，系统错误）
#include <system_error>
#include <iostream>
#include <cstdio>
int main(){
    std::error_code ec;
    FILE* f = std::fopen("nope.txt","r");
    if (!f) { ec = std::make_error_code(std::errc::no_such_file_or_directory);
              std::cout << "errno-style: " << ec.message() << "\n"; }
}
```

**核心知识点 #19**：`-fno-exceptions` 禁用异常、代码更小更快但保证退化为终止；嵌入式/内核常用。
**核心知识点 #20**：异常用于罕见跨层错误；`expected`/`error_code` 用于可预期频繁错误；零开销/禁异常环境用错误码。

---

## ⑮ 三编译器 / 三 STL 对比：EH 模型与开关

### 15.1 EH 模型

| 编译器 | 平台 | EH 模型 | 说明 |
|---|---|---|---|
| **GCC** | Linux/MinGW | Itanium C++ ABI zero-cost | `.eh_frame` + LSDA，正常路径零开销（第 13 节） |
| **Clang** | 同 GCC（默认） | Itanium zero-cost（LLVM libunwind） | 与 GCC 兼容 DWARF 展开 |
| **MSVC** | Windows | **SEH**（结构化异常处理）融合 C++ EH | Windows x64 用基于表的 SEH；`/EH` 系列开关控制 |

**[平台-推断]**　MSVC 的 C++ 异常构建在 Windows SEH 之上（x64 用 `RtlUnwindEx` 与 `.pdata`/`.xdata` 表），同样属「基于表」而非「setjmp 式」；但 MSVC 默认并不假设「正常路径零开销」到与 Itanium 完全相同的程度，且 `/EHa` 会使 **C 异常（如访问违规）也被 C++ catch(...) 捕获**，带来额外检查成本。

### 15.2 MSVC 的 /EH 开关

| 开关 | 含义 |
|---|---|
| `/EHsc` | **默认**：C++ 异常，假定 `extern "C"` 函数不抛（不捕获异步 SEH）；安全且最快 |
| `/EHs` | 同 `/EHsc` 但不假定 `extern "C"` 不抛（很少用） |
| `/EHa` | **异步**：C++ 异常 + 捕获 SEH 异步异常（如访问违规进 `catch(...)`）；有运行期成本 |
| `/EHr` | 即使函数标记 noexcept，也生成「异常到达 noexcept → terminate」的运行时检查（强健壮性，略增代码） |

> **示例 36** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 的 /EH 开关
```cpp title="示例 36 · ★☆☆☆☆"
// [示例 24] MSVC /EHa 下 SEH 异常进入 C++ catch(...)（Windows 专属）
// 编译：cl /EHa 时下面会进 catch；/EHsc 下直接崩溃
#include <iostream>
int main(){
    try {
        int* p = nullptr; *p = 1;  // 访问违规（SEH）
    } catch (...) {                // /EHa 才能捕获，/EHsc 不能
        std::cout << "caught SEH via C++\n";
    }
}
```

### 15.3 /EHc：假定 extern "C" 不抛

**[平台-推断]**　`/EHc`（配合 `/EHsc`）让 MSVC 假定 `extern "C"` 函数绝不抛 C++ 异常，从而**跳过对这些函数的展开注册**，优化代码。若你真从 `extern "C"` 抛了 C++ 异常，行为是 UB——这是性能换安全的典型平台取舍。

### 15.4 三 STL 的 vector 扩容 noexcept 决策

| STL | 扩容决策 | 备注 |
|---|---|---|
| **libstdc++** | `__uninitialized_move_if_noexcept_a`（move_if_noexcept） | 见 7.2、7.3；另有 `_S_use_relocate` 最快路径 |
| **libc++** `[实现-推断]` | 同样基于 `is_nothrow_move_constructible` 决定 move/copy | `__swap_out_circular` 等内部使用 move_if_noexcept 同类逻辑 |
| **MS STL** `[实现-推断]` | 同样基于 `is_nothrow_move_constructible` 与 `_Traits` | `<xutility>` 的 `_Move_if_noexcept` 等价物 |

**<span class="badge badge-exp">经验</span>**　三库**语义一致**：都遵循「移动不抛才移动」原则，这是标准对 strong 保证的要求，非实现偏好。差异只在内部命名与 relocate 优化细节。

**核心知识点 #21**：GCC/Clang 用 Itanium zero-cost EH；MSVC 用 SEH 融合 EH，靠 `/EHsc`(默认)/`/EHa`(捕异步)/`/EHr`(noexcept 检查) 控制；`/EHc` 假定 extern C 不抛以优化。

---

### 15.5 noexcept 函数遇上 /EHr（MSVC 健壮性开关）

**[平台-推断]**　MSVC `/EHr` 会在**每个 `noexcept` 函数**插入运行期检查：「若有异常抵达 noexcept 边界 → 调用 terminate」。这牺牲少量体积/速度换取「即使第三方代码从 noexcept 逃逸异常也能优雅终止」，而 GCC/Clang 默认假定 noexcept 真的不会抛、不插入检查。

> **示例 37** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 函数遇上 /EHr
```cpp title="示例 37 · ★☆☆☆☆"
// [示例 40] /EHr 下 noexcept 逃逸异常被 terminate 捕获（MSVC 行为示意）
// 编译：cl /EHr /std:c++17
#include <iostream>
#include <exception>
void on_term(){ std::cout << "terminated via /EHr\n"; std::abort(); }
void boom() noexcept { throw 1; }   // 违反 noexcept：/EHr 下被捕获并 terminate
int main(){ std::set_terminate(on_term); boom(); }
///EHr：输出 terminated via /EHr；默认 /EHsc：未定义/崩溃（无检查）
```

**<span class="badge badge-exp">经验</span>**　跨编译器项目若需「noexcept 逃逸必终止」的强保证（如安全关键系统），在 MSVC 显式加 `/EHr`，GCC/Clang 侧则需靠代码审查与 `-fno-exceptions` 之外的静态断言保证。

## ⑯ 真实 microbenchmark：noexcept 移动 vs 拷贝扩容

### 16.1 noexcept 移动让扩容走移动（更快）

**<span class="badge badge-impl">实现</span>**　当元素移动构造 `noexcept`，`vector` 扩容用移动（或 relocate），否则用拷贝。下面测量两者差异。

> **示例 38** <span class="badge badge-exp">难度 ★★★☆☆</span> · 移动让扩容走移动（更快）
```cpp title="示例 38 · ★★★☆☆"
// [示例 25] 扩容：noexcept 移动 vs 拷贝（量级对比）
#include <vector>
#include <chrono>
#include <iostream>
struct NoThrow { NoThrow()=default; NoThrow(NoThrow&&) noexcept = default;
                 NoThrow(const NoThrow&)=default; int a[8]{}; };
struct Throws  { Throws()=default; Throws(Throws&&) {}  // 移动抛→走拷贝
                 Throws(const Throws&)=default; int a[8]{}; };
template<class T>
double bench(){
    const int N = 200'000;
    auto t0 = std::chrono::steady_clock::now();
    for (int k=0;k<50;++k){ std::vector<T> v; v.reserve(1);
        for (int i=0;i<N;++i) v.push_back(T{}); }       // 反复扩容
    auto t1 = std::chrono::steady_clock::now();
    return std::chrono::duration<double,std::milli>(t1-t0).count();
}
int main(){
    std::cout << "noexcept-move resize=" << bench<NoThrow>() << " ms\n";
    std::cout << "copy-on-resize     =" << bench<Throws>()  << " ms\n";
}
// 典型：noexcept 移动明显更快（移动 8 个 int 比拷贝 8 个 int 略快，差距随元素拷贝成本放大）
```

### 16.2 noexcept 对代码生成的影响（优化）

> **示例 39** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 对代码生成的影响（优化）
```cpp title="示例 39 · ★☆☆☆☆"
// [示例 26] noexcept 让编译器删除展开表（概念验证，需用 objdump 看）
#include <vector>
void f_noexcept(std::vector<int>& v) noexcept { v.push_back(1); }  // 不抛→无展开表
void f_throws(std::vector<int>& v)            { v.push_back(1); }  // 可能抛→保留展开表
// 编译：g++ -O2 -S 后对比 .eh_frame 尺寸：f_noexcept 更小
int main(){ std::vector<int> v; f_noexcept(v); f_throws(v); }
```

### 16.3 异常延迟量级汇总

> **示例 40** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 异常延迟量级汇总
```cpp title="示例 40 · ★★☆☆☆"
// [示例 27] 综合：正常路径零开销 + 抛异常延迟（复用示例 19/20 思路）
#include <chrono>
#include <iostream>
int main(){
    const int N = 50'000'000;
    volatile int s=0;
    auto a = std::chrono::steady_clock::now();
    for (int i=0;i<N;++i) try { s+=i; } catch(...){}
    auto b = std::chrono::steady_clock::now();
    int c=0; auto x=std::chrono::steady_clock::now();
    for (int i=0;i<100'000;++i) try { throw i; } catch(int){ ++c; }
    auto y = std::chrono::steady_clock::now();
    std::cout << "normal try/catch "
              << std::chrono::duration<double,std::milli>(b-a).count()/N*1e6
              << " ns/op\n";
    std::cout << "throw+catch "
              << std::chrono::duration<double,std::micro>(y-x).count()/100'000
              << " us/op\n";
}
```

**<span class="badge badge-exp">经验</span>**　量级参考（本机 MinGW GCC 13.1.0，仅量级）：正常路径 `try/catch` 约 **0.x ns/op**（与无 try 几乎相同）；`throw+catch` 约 **0.2–3 µs/op**（随栈深与析构数上升）。**结论：异常用于罕见路径，错误码用于热路径** `[实验·本机实测][VERIFIED]`。

---

### 16.4 测量 noexcept 移动对重排算法的影响

**<span class="badge badge-impl">实现</span>**　`std::sort`、`std::rotate` 等在「元素可 noexcept 移动」时可用移动而非拷贝交换元素，性能差异随元素大小放大。

> **示例 41** <span class="badge badge-exp">难度 ★★★☆☆</span> · 测量 noexcept 移动对重排算
```cpp title="示例 41 · ★★★☆☆"
// [示例 37] sort 中 noexcept 移动 vs 拷贝交换（量级）
#include <algorithm>
#include <vector>
#include <chrono>
#include <iostream>
// sort 内部靠 swap（移动构造 + 移动赋值）搬运元素；声明了移动构造后必须补齐赋值运算符。
struct BigNT { int a[16]; BigNT(BigNT&&) noexcept = default;
               BigNT(const BigNT&)=default; BigNT()=default;
               BigNT& operator=(BigNT&&) noexcept = default; BigNT& operator=(const BigNT&)=default; };
struct BigT  { int a[16]; BigT(BigT&&) {}              // 未标 noexcept → sort 退化用拷贝
               BigT(const BigT&)=default; BigT()=default;
               BigT& operator=(BigT&&) { return *this; }
               BigT& operator=(const BigT&)=default; };
template<class T> double bench_sort(){
    const int N=20000;
    auto t0=std::chrono::steady_clock::now();
    for(int k=0;k<200;++k){ std::vector<T> v(N); for(int i=0;i<N;++i) v[i].a[0]=N-i;
        std::sort(v.begin(),v.end(),[](const T&A,const T&B){return A.a[0]<B.a[0];}); }
    auto t1=std::chrono::steady_clock::now();
    return std::chrono::duration<double,std::milli>(t1-t0).count();
}
int main(){
    std::cout<<"noexcept-move sort="<<bench_sort<BigNT>()<<"ms\n";
    std::cout<<"copy sort       ="<<bench_sort<BigT>() <<"ms\n";
}
// 元素越大，noexcept 移动的优势越明显（交换从拷贝改为移动）
```

### 16.5 异常 vs 错误码：热路径成本对照

> **示例 42** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 异常 vs 错误码：热路径成本对照
```cpp title="示例 42 · ★★☆☆☆"
// [示例 38] 错误码（无展开）在热路径显著快于异常
#include <chrono>
#include <iostream>
volatile int sink=0;
int errcode_path(int i, int& out){ if(i<0) return -1; out=i; return 0; }
int main(){
    const int N=100'000'000;
    auto t0=std::chrono::steady_clock::now();
    for(int i=0;i<N;++i){ int o; if(errcode_path(i,o)==0) sink+=o; }
    auto t1=std::chrono::steady_clock::now();
    std::cout<<"error-code hot path="
              <<std::chrono::duration<double,std::nano>(t1-t0).count()/N<<" ns/op\n";
    // 对比示例 27：异常仅在"真正抛"时 µs 级；错误码每次仅 ns 级，但侵入式写法
}
```

## ⑰ 跨语言对比

| 语言 | 错误模型 | 成本 / 特点 | 与 C++ 对应 |
|---|---|---|---|
| **Rust** | `Result<T,E>` + `?` 传播；**无异常** | 零成本（是返回值）；编译期强制处理 | C++ `std::expected`/`std::error_code` |
| **Go** | 多返回值 `(T, error)`；无异常 | 零成本；错误需显式 `if err!=nil` | C++ 错误码 |
| **Java** | checked / unchecked 异常 | **有成本**（始终携带栈追踪构建）；checked 强制声明 | C++ 异常 + 文档约定 |
| **C#** | 异常 + `finally`/`using`(RAII 近似) | 有成本（同 JVM 栈追踪）；`finally` 类似析构 | C++ 异常 + RAII（`ch39`） |
| **Swift** | `Error` 协议 + `do/try/catch`；值语义 | 较低成本（enum 错误，非栈追踪）；无隐式抛检查 | C++ 异常 + `noexcept` 近似 |

> **示例 43** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 跨语言对比
```cpp title="示例 43 · ★☆☆☆☆"
// [示例 28] 对照：Rust Result 的 C++ expected 写法（概念映射）
// Rust:  fn parse(s:&str)->Result<i32,String> { ... }
// C++  (C++23):
#include <expected>
#include <string>
std::expected<int,std::string> parse(const char* s){
    if (!s) return std::unexpected(std::string("null"));
    return std::atoi(s);
}
```

**<span class="badge badge-exp">经验</span>**　Rust/Go 的「错误即值」在**热路径零开销**上胜过 C++ 异常，但 C++ 异常在**跨多层展开**时书写更简洁。C++23 `std::expected` 补齐了「无开销错误值」选项。

---

## ⑱ noexcept 对编译器优化的影响

**<span class="badge badge-std">标准</span>/<span class="badge badge-impl">实现</span>**　`noexcept` 给编译器的两条关键信息：
1. **无需生成展开表**（unwind table）：标记 `noexcept` 的函数，调用方不必为其注册展开信息 → 代码更小（见示例 26）。
2. **允许更激进的内联/移动**：编译器知道不会因异常展开而需回退，可自由重排、省略栈保存。

**[平台-推断]**　MSVC `/EHr` 会对 `noexcept` 函数仍插入「到达 noexcept 即 terminate」的运行期检查（牺牲一点体积换健壮性），与其他编译器默认「完全省略」略有差异。

> **示例 44** <span class="badge badge-exp">难度 ★★★☆☆</span> · 对编译器优化的影响
```cpp title="示例 44 · ★★★☆☆"
// [示例 29] noexcept 移动使容器放心移动 + 编译器删展开表
#include <vector>
#include <type_traits>
#include <utility>
// 注意：显式声明移动/拷贝构造会抑制隐式默认构造，而 vector<T>(10) 需要 T 默认可构造，
// 故显式补上 `T()=default`（两者均为空类型，默认构造平凡）。
struct Fast { Fast()=default; Fast(Fast&&) noexcept = default; Fast(const Fast&)=default; };
struct Slow { Slow()=default; Slow(Slow&&); Slow(const Slow&)=default; };  // 移动抛
static_assert(std::is_nothrow_move_constructible_v<Fast>);
static_assert(!std::is_nothrow_move_constructible_v<Slow>);
int main(){
    std::vector<Fast> a(10); std::vector<Fast> b(std::move(a));            // relocate/移动，无回滚表
    std::vector<Slow> c(10); std::vector<Slow> d(std::move(c));            // 走 move_if_noexcept→拷贝
}
```

**核心知识点 #22**：`noexcept` 让编译器省略展开表、更激进内联/重排；是「性能 + 强保证」的复利开关。

---

## ⑲ 工程实践清单与常见陷阱

**<span class="badge badge-exp">经验</span>**　异常安全工程清单：
1. **析构函数永远 `noexcept`**（见 `ch39`、`ch36`）——否则栈展开二次抛 → terminate。
2. **给移动构造/移动赋值加 `noexcept`**（第 6、18 节）——解锁 vector 移动扩容与 relocate。
3. **资源用 RAII**（智能指针、容器、锁守卫，`ch41`）——把 `none` 升到 `basic`/`strong`。
4. **赋值用 copy-and-swap** 求强保证，性能敏感处评估代价（第 8 节）。
5. **不要在析构里抛**：必须做的清理若可能失败，记录日志/标记而非抛。
6. **异常不要穿越 C ABI / `extern "C"`**：跨语言边界（C、FFI）用错误码（第 14 节，`[平台]`）。
7. **构造函数获取资源失败即抛**，成员用 RAII 保证无泄漏（第 11 节）。
8. **不要拿异常做常规控制流**（第 13 节：µs 级代价）。
9. **库边界的强保证要写进文档**：调用方才知道能否假设回滚。
10. **`-fno-exceptions` 环境**：全代码库统一用错误码，禁用 `throw`。

> **示例 45** <span class="badge badge-exp">难度 ★★★☆☆</span> · 工程实践清单与常见陷阱
```cpp title="示例 45 · ★★★☆☆"
// [示例 30] 反例：异常穿越 C ABI（危险，UB）
extern "C" int c_api() { throw 1; }     // 错误：C 调用方无法展开 C++ 栈
// 正确：
extern "C" int c_api_safe(int* ok){
    try { /* ... */ }
    catch(...) { *ok = 0; return -1; }  // 错误码过界
}
```

> **示例 46** <span class="badge badge-exp">难度 ★★★☆☆</span> · 工程实践清单与常见陷阱
```cpp title="示例 46 · ★★★☆☆"
// [示例 31] ScopeGuard：用 uncaught_exceptions 的工业级提交/回滚（简化版）
#include <exception>
#include <utility>
#include <iostream>
template<class F>
struct ScopeGuard {
    F f_; int init_ = std::uncaught_exceptions(); bool active_ = true;
    ScopeGuard(F f):f_(std::move(f)){}
    void dismiss(){ active_ = false; }
    ~ScopeGuard(){ if (active_ && std::uncaught_exceptions() > init_) f_(); }
};
int main(){
    try {
        ScopeGuard rollback([]{ std::cout << "rollback on throw\n"; });
        throw 1;                 // 展开时触发 rollback
    } catch(int){}
}
```

> **示例 47** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 工程实践清单与常见陷阱
```cpp title="示例 47 · ★★☆☆☆"
// [示例 32] 验证类型是否提供各级保证的 trait（编译期自检）
#include <type_traits>
#include <vector>
static_assert(std::is_nothrow_swappable_v<std::vector<int>>);           // swap noexcept
static_assert(std::is_nothrow_move_constructible_v<std::vector<int>>);  // 移动 noexcept
struct S { S(S&&) noexcept; S(const S&); };
static_assert(std::is_nothrow_move_constructible_v<S>);                 // 用户类型 noexcept 移动
int main(){}
```

---

### 18.1 noexcept 在虚函数覆盖（override）上的约束

**<span class="badge badge-std">标准</span>**　`[except.spec]/4`：覆盖（override）基类虚函数时，派生类的 `noexcept` 说明**不能比基类更宽**（即派生可声明 `noexcept(true)` 当基类是 `noexcept(false)`，但**不能**把基类 `noexcept(true)` 的覆盖成可能抛——那会编译错误）。这是「基类承诺了不抛，派生不得破坏」的协变规则。

> **示例 48** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 在虚函数覆盖（override）上的
```cpp title="示例 48 · ★★☆☆☆"
// [示例 42] 虚函数 noexcept 覆盖约束
#include <type_traits>
struct Base { virtual void f() noexcept; virtual void g(); };
struct D1 : Base { void f() noexcept override; };  // OK：同样不抛
struct D2 : Base { void g() override; };           // OK：基类可抛
// struct Bad : Base { void f() override; };               // 错误：基类 noexcept(true) 不能被覆盖成可能抛
int main(){ static_assert(std::is_same_v<decltype(&Base::f), void (Base::*)() noexcept>); }
```

**<span class="badge badge-exp">经验</span>**　给基类虚函数加 `noexcept` 是**单向承诺**：一旦发布，所有派生类都被锁死为不抛。设计基类接口时，把「一定不抛」才标 noexcept，否则留给派生自由。

### 19.1 更多工业级陷阱

**<span class="badge badge-exp">经验</span>**　补充 §19 清单之外的实战坑：

1. **异常穿越 `std::thread` 入口**：`std::thread` 函数体抛异常且未捕获 → `std::terminate`（线程没有调用方 `catch`）。必须线程入口自行 `try/catch` 并转 `exception_ptr`（见示例 17）。
2. **`std::async` 的异常会被存储并在 `get()` 时重抛**：这是异常安全的延迟传递，调用方务必 `try/catch` `get()`。
3. **`noexcept` 与 `std::terminate` 在析构链**：构造函数里 `std::vector` 成员若分配抛，已构造成员仍正确析构（`ch39`/`ch37`），但**裸 `new` 成员**在构造失败时不会自动 `delete`——必须用成员初始化列表里的 RAII 或 `try` 块手动清理。
4. **`std::uncaught_exceptions` 与栈深度**：递归中多层对象各自记录 `init_`，计数差只在「本对象生命周期内新增异常」时为真——这正是示例 13/31 正确工作的原因。

> **示例 49** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 更多工业级陷阱
```cpp title="示例 49 · ★★☆☆☆"
// [示例 43] std::async 异常延迟到 get() 重抛（安全传递）
#include <future>
#include <iostream>
#include <stdexcept>
int main(){
    auto f = std::async([]{ throw std::runtime_error("deferred"); });
    try { f.get(); }                       // 异常在此重抛，调用方处理
    catch(const std::exception& e){ std::cout << "got: " << e.what() << "\n"; }
}
```

> **示例 50** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 更多工业级陷阱
```cpp title="示例 50 · ★★☆☆☆"
// [示例 44] 线程入口必须自捕获，否则 terminate
#include <thread>
#include <iostream>
#include <exception>
int main(){
    std::thread t([]{
        try { throw 1; }                   // 线程内自行捕获，不向外逃逸
        catch(int){ std::cout << "thread caught\n"; }
    });
    t.join();
    // 若去掉 try/catch，线程函数抛 → std::terminate
}
```

## 源码阅读路线

**<span class="badge badge-impl">实现</span>**　按以下顺序精读，理解「标准 → 库 → ABI」三级：

1. **libstdc++ `<bits/stl_vector.h>`**（本机 `.../13.1.0/include/c++/bits/stl_vector.h`）
   - `462-509`：`_S_use_relocate` / `_S_nothrow_relocate` —— realloc 的 noexcept 决策。
   - `1581`：`swap(vector&)` 的 `_GLIBCXX_NOEXCEPT`。
   - `615`/`761`：移动构造/移动赋值的 `noexcept`。
2. **libstdc++ `<bits/vector.tcc>`**
   - `477-523`：`_M_realloc_insert` 中 `move_if_noexcept` + `__catch` 回滚（strong 保证落点）。
3. **libstdc++ `<bits/move.h>`**
   - `108-126`：`__move_if_noexcept_cond` 与 `move_if_noexcept` 本体（第 6、7 节）。
4. **libstdc++ `<bits/stl_uninitialized.h>`**
   - `393-401`：`__uninitialized_move_if_noexcept_a` 调用 move_if_noexcept 迭代器。
5. **libstdc++ `<bits/exception_ptr.h>`**
   - `60-112`：`exception_ptr` / `current_exception` / `rethrow_exception`（第 12 节）。
6. **libstdc++ `<exception>`**
   - `121-130`：`uncaught_exception` / `uncaught_exceptions`（第 9 节）。
7. **libstdc++ `<bits/cxxabi_forced.h>`**
   - `39-55`：`__forced_unwind`（平台级展开占位，第 4、7.6 节）。
8. **libc++** `[实现-推断]`：`<vector>`（LLVM）、`<exception>`、`<utility>` 同名文件，逻辑对应。
9. **Itanium C++ ABI EH 规范**（itanium-cxx-abi）：zero-cost EH、LSDA、`.eh_frame` 布局。
10. **LLVM libunwind**（`libunwind`）：`Unwind_*` / `personality` 例程、`__gxx_personality_v0`。
11. **DWARF 规范**：`.eh_frame` / `.eh_frame_hdr` / CIE/FDE 格式（展开表本质）。
12. **MSVC** `[平台-推断]`：`<vector>`（MS STL）、`/EH` 系列文档、Windows x64 SEH（`RtlUnwindEx`、`.pdata`/`.xdata`）。

**<span class="badge badge-exp">经验</span>**　读完这 12 处，你将能把「`noexcept` 一行」与「vector 扩容是移动还是拷贝」「展开表是否被生成」「跨线程异常如何转发」全部串成一条因果链——这正是工业级 C++ 对异常安全的完整心智模型。

---

## ⑳ 本章速查表

**练习题**（已升级为「真实场景 + 引用参考」框架：保留原考察技能，场景改写为工程应用）

1. **真实场景：用不抛的 `swap` 实现强异常保证。** 你让 `operator=` 先拷贝再 `swap`，失败时原对象不受影响。请说明 `swap` 通常不抛的依据。
   - <span class="badge badge-std">标准</span> 对可交换类型，`std::swap` 在成员/特化提供不抛交换时应标记为 `noexcept`，从而支持“拷贝-交换”回滚。
   - <span class="badge badge-ref">引用</span> ISO/IEC 14882:2023 §[utility.swap]（swap 与 noexcept）；cppreference "std::swap" 词条。

2. **真实场景：构造中途抛异常须清理已构造成员。** 你在构造函数初始化列表里先成功构造 `A` 成员，随后 `B` 成员构造抛异常，要保证 `A` 被析构。请说明保证机制。
   - <span class="badge badge-std">标准</span> 异常离开构造函数时，已完整构造的基类和成员子对象按声明逆序析构（函数 try 块可捕获该异常）。
   - <span class="badge badge-ref">引用</span> ISO/IEC 14882:2023 §[except.ctor]（构造中的栈展开）；cppreference "Exception safety" 词条。

3. **真实场景：移动非 `noexcept` 让 `vector` 增长退回拷贝。** 你给类型写了移动构造却没标 `noexcept`，`push_back` 触发重分配时竟调用拷贝构造，性能骤降。请说明 `vector` 的选择。
   - <span class="badge badge-std">标准</span> `std::vector` 在重分配（增长）时，仅当移动构造/移动赋值对 `is_nothrow_move_constructible` 为真才使用移动，否则回退拷贝以保证强异常安全。
   - <span class="badge badge-ref">引用</span> ISO/IEC 14882:2023 §[meta.unary.prop]（is_nothrow_move_constructible）/ [vector.modifiers]（重分配用移动的前提）；cppreference "std::vector::reserve / reallocation" 词条。

| 保证 | 承诺 | 典型函数 |
|---|---|---|
| noexcept | 不抛（抛则 terminate） | 析构、`swap`、`move` 构造 |
| strong | 成功或回滚到调用前 | `push_back`（不扩容/扩容均可）、copy-and-swap 赋值 |
| basic | 不漏 + 不变量保持，状态可变 | `std::sort`（比较器抛）、多步 mutating 算法 |
| none | 无承诺 | 裸资源手动管理代码 |

| 工具 | 用途 |
|---|---|
| `noexcept` / `noexcept(expr)` | 承诺/探测不抛 |
| `std::move_if_noexcept` | realloc 时「移动 or 拷贝」决策 |
| `std::uncaught_exceptions` | 析构中判断是否展开，提交/回滚 |
| `std::exception_ptr` / `current` / `rethrow` | 跨线程异常转发 |
| `-fno-exceptions` / `/EHsc` | 禁用异常 / 控制 MSVC EH 模型 |

**核心知识点全 23 项**：
1. 异常安全四级：noexcept > strong > basic > none。
2. noexcept=不抛（抛则 terminate）；strong=回滚；basic=不漏+不变量；none=无。
3. 析构默认 noexcept，是强/基本保证前提（连 `ch39`/`ch36`）。
4. `swap` 应为 noexcept（O(1) 指针交换）。
5. `push_back` 不扩容=strong；扩容靠 move_if_noexcept 仍 strong；`swap` 恒 noexcept；`operator=` 目标 strong。
6. 栈展开=抛异常时逆序析构自动对象（连 `ch36`）。
7. 栈展开中再抛未捕获→terminate；析构必须 noexcept。
8. `throw(type)` 动态规格 C++11 弃用、C++17 删除。
9. `noexcept` ≡ `noexcept(true)`；`noexcept(bool)` 条件；`noexcept(expr)` 运算符。
10. vector 扩容：移动可能抛则损坏状态，故仅 `is_nothrow_move_constructible` 才移动，否则拷贝。
11. `move_if_noexcept`：移动不抛返 `T&&`，否则返 `const T&` 强制拷贝。
12. `move_if_noexcept` 靠返回类型分流；vector realloc 在 `__catch` 回滚原样重抛保 strong。
13. copy-and-swap：按值参数+noexcept swap → 强保证，代价一次额外拷贝。
14. `uncaught_exceptions()`（C++17）计数；构造/析构计数差实现提交/回滚。
15. `[res.on.exception.handling]`：标准库至少 basic、特定 noexcept/strong、析构不抛。
16. 构造抛→已构造成员逆序自动析构、对象内存释放、无泄漏。
17. `exception_ptr` 不透明句柄；current/rethrow/make 三件套跨线程转发。
18. Itanium zero-cost EH：正常路径零检查，异常路径查 `.eh_frame`/LSDA，数百 ns–µs。
19. `-fno-exceptions` 禁用异常、更小更快但保证退化为终止。
20. 异常用于罕见跨层错误；`expected`/`error_code` 用于频繁错误；禁异常环境用错误码。
21. GCC/Clang=Itanium zero-cost；MSVC=SEH 融合，`/EHsc`(默认)/`/EHa`(捕异步)/`/EHr`(noexcept 检查)；`/EHc` 假定 extern C 不抛。
22. `noexcept` 让编译器省略展开表、更激进内联/重排。
23. `_S_use_relocate()` 编译期判定 noexcept relocate，决定 realloc 最快路径还是 move_if_noexcept 路径。

> 老兵收尾：**异常安全不是加几个 `try/catch`，而是把「抛了怎么办」刻进每一层类型的契约里。** `noexcept` 一行，决定了 vector 是飞还是爬；`uncaught_exceptions` 一句，决定了事务是提交还是回滚；析构不抛，决定了程序是优雅退出还是 terminate。把这三件事做对，你的 C++ 才配叫工业级。

## ㉒ 历史纵深·真实产业坐标·生产踩坑·与标准的互动

> 本节为 P0-15 全库深度升维大波次之一：压实历史出处、真实产业坐标、生产级踩坑与「本特性与 C++ 标准」的互动。引用链接列于 ㉒.5。

### ㉒.1 历史渊源补强：C++ 异常机制的来龙去脉

<span class="badge badge-history">史</span> C++ 异常源自 **1980 年代末 Bell 实验室** 对「构造函数失败如何安全处理」的探索——Stroustrup 在 *The Design and Evolution of C++*（§16.1）中记录：异常在最初设计时即被**考虑但推迟**——当时没时间彻底探索设计与实现问题、又担心它给实现带来的复杂度；实际的异常机制设计**历时 1984–1989 五年**，是 C++ 第一个「在公众目光下设计」的部分。早期 C++ 用 error code + 手动回滚，极易漏处理，异常最终引入以与 RAII（ch39）配合解决此问题。`[de:16.1]`异常规范（exception specification）初版随 **C++98（1998）** 落地，允许 `throw(type-list)` 声明函数可能抛出的类型。<span class="badge badge-anecdote">轶</span> 但 `throw()` 动态规范很快被证明是「昂贵的失败」：编译器要么在每次调用插入运行时检查、要么根本无法内联，且 `unexpected()` 行为反直觉。因此 **C++11（2011）将动态异常规范整体弃用，并引入 `noexcept`（第 ⑤ 节）** 作为零成本的「不抛」契约；**P0003R5（C++17）** 正式把 `throw(type)` 从语言中删除，仅保留 `throw()` 作为弃用的 `noexcept(true)` 别名（第 ⑤ 节）。<span class="badge badge-history">史</span> 更早的转折在 **1994 年**：Tom Cargill 在 *C++ Report* 发表《Exception Handling: A False Sense of Security》，用一个容器示例证明当时社区对「异常安全」尚无共识、甚至无人能给出完整解；三年后（1997）Herb Sutter 以《Exception-Safe Generic Containers》给出三个完整解，异常安全才从「玄学」变成「可论证的工程」——这段十部曲后来收进 *Exceptional C++*（Item 8–17）。`[book:exceptional-cpp:item8]`<span class="badge badge-history">史</span> 「异常安全（exception safety）」这一术语与强/基本/不抛三级保证，由 **David Abrahams 在 1990 年代末的论文与 Boost 实践中** 系统化，后被 C++ 标准库条款 `[res.on.exception.handling]`（第 ⑩ 节）采纳。

### ㉒.2 真实工程坐标：异常安全活在哪里

下表把「异常安全」拉成光谱：左端（标准库）把异常当一等公民并给出强保证，右端（浏览器 / 游戏 / 医疗 / 汽车）整系统禁用异常改用错误码。

| 领域/类别 | 代表系统·生态 | 它承担的角色 | 规模·行业地位 | 备注 / 标准互动 |
| --- | --- | --- | --- | --- |
| 标准库 / 容器 | `std::vector::push_back`（第 ⑥ 节）、算法（`[res.on.exception.handling]`） | 强保证范本；异常契约分级 | 现代 C++ 库参照系 | 几乎所有库异常契约都参照它 |
| 数据库 / 事务 | 事务「提交或回滚」 | RAII 守卫（第 ⑨ 节 `uncaught_exceptions`）异常路径自动回滚 | 金融 / 存储引擎标配 | 异常安全保证分级的真实落地 |
| 浏览器 | Chromium / Blink（`-fno-exceptions`） | 改用 `base::expected` / `absl::Status` 错误码 | 二进制体积 + 确定性 | 工业级「异常 vs 错误码」决策：选错误码 |
| 游戏 / 嵌入式 | Unreal / Unity（整体禁异常） | 错误码或断言替代展开 | 实时 / 主机确定性 | 展开带来不可预测延迟 + 代码膨胀 |
| 医疗器械 | IEC 62304 / 植入式设备固件 | 错误码返回，禁异常 | 硬实时 + 认证体积 | 与 JPL 飞行软件同源「禁异常」 |
| 汽车 | AUTOSAR / 实时 ECU（`E_OK` / `E_NOT_OK`） | 返回码表达错误非异常 | ISO 26262 认证 | 确定性故障处理合规要求 |

> **表注（㉒.2）**：上表把「异常安全」拉成光谱：左端（标准库）把异常当一等公民并给出强保证，右端（浏览器 / 游戏 / 医疗 / 汽车）整系统禁用异常改用错误码。中间没有「既用异常又禁用」的混搭——AUTOSAR 与 IEC 62304 两行是合规驱动（认证要求确定性故障处理），Chromium 是体积 / 确定性驱动，根因都是「展开的不确定性代价不可接受」。

**一条判读**：选异常还是错误码，判据是「异常展开的不确定性代价能否被系统容忍」。标准库 / 业务库能容忍（异常只在错误路径，且强保证有价值）→ 用异常；浏览器内核 / 实时 / 安全攸关系统不能容忍（展开延迟不可预测、认证体积增大）→ 错误码。关键不是「异常好不好」，而是目标环境对「不可预测的展开开销」的容忍度为零与否。

### ㉒.3 生产踩坑：异常安全的常见误用

- **析构抛异常 → `std::terminate`**：第 ⑥ 节强调，若栈展开（已有异常传播）时某析构再抛，程序直接终止；生产代码析构里绝不能传播异常。
- **移动构造非 `noexcept` 拖垮 `vector` 扩容**：第 ⑥ 节指出，`vector` 在扩容搬迁时若元素的移动构造不是 `noexcept`，会退化为「先拷贝再析构旧」的强保证路径（慢且可能抛），正确做法是给移动构造标 `noexcept`。
- **异常规格的历史坑**：在 C++17 之前写 `throw(std::bad_alloc)` 这类动态规范，既拖性能又可能在意外抛其他类型时调用 `unexpected()`→`terminate`；遗留代码升级到 C++17 后这些写法直接编译失败，需改为 `noexcept(false)`/省略。
- **`std::uncaught_exception()`（单数，旧）误用**：第 ⑨ 节说明，单参旧接口无法区分「是否嵌套在更外层异常中」，用它做「提交或回滚」在嵌套场景会错；必须用 **C++17 的 `std::uncaught_exceptions()`（返回计数）**。

### ㉒.4 与标准的互动：异常安全与 WG21 演进

<span class="badge badge-history">史</span> C++98 引入动态异常规范但很快被视为失误；**C++11 用 `noexcept` 替代**（第 ⑤ 节），并把 `std::exception_ptr`/`current_exception`/`rethrow_exception`（第 ⑫ 节）标准化以支持跨线程传递异常；**P0003R5（C++17）** 删除动态规范。**C++17 的 P0188 一脉** 引入 `std::uncaught_exceptions()`（第 ⑨ 节）修复了「提交或回滚」守卫的嵌套缺陷。<span class="badge badge-comment">评</span> WG21 当前方向是在 **C++26 引入契约（contracts，P2900 一脉）**，用 `pre`/`post`/`assert` 契约部分替代「用异常表达前置条件」的重负；同时 `-fno-exceptions` 作为实现级开关长期保留，承认「异常并非所有领域的最优解」——标准并不强推异常，而是把它作为可选项并压实其安全契约。
- <span class="badge badge-history">史</span> 删除动态异常规范的修订链为 **P0003R0→…→P0003R5（C++17 正式移除 `throw(T)` 动态规范，仅留 `throw()` 作弃用的 `noexcept(true)` 别名）**。ISO 条款 `[res.on.exception.handling]` 规定标准库函数在异常下的行为契约（如强/基本保证），是「异常安全分级」的可执行依据；委员会的方向是把「前置条件」从「靠异常抛出」转移到 **C++26 契约（P2900R0→…→P2900R14 候选）** 的 `pre`/`post`，而非继续加重异常语义。

### ㉒.5 权威引用

- [cppreference: noexcept specifier](https://en.cppreference.com/w/cpp/language/noexcept_spec) — `noexcept` 与 `noexcept(false)` 语义（C++11）
- [cppreference: std::uncaught_exceptions](https://en.cppreference.com/w/cpp/error/uncaught_exception) — 提交或回滚惯用法（C++17）
- [WG21 P0003R5 — Removing Deprecated Exception Specifications from C++17](https://wg21.link/P0003) — 删除动态异常规范
- [cppreference: 标准库异常安全条款 res.on.exception.handling](https://en.cppreference.com/w/cpp/standard_library#Exception_safety) — 标准库对异常保证的要求
- [David Abrahams — Exception-Safety in Generic Components](https://www.boost.org/community/exception_safety.html) — 强/基本/不抛三级保证的系统化来源

## 附录 A：工业异常安全实践 [F: Industry / B: Principle]

> **示例 51** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 附录 A：工业异常安全实践 [F: Industry / B: Principle]
```text
Google Style Guide 第3条: "We do not use C++ exceptions"
  → 原因: 二进制尺寸+15-30%, 老代码不支持, 团队一致性, 不可预测性能
  → 替代: absl::Status, absl::StatusOr<T> (零开销成功路径)

LLVM Coding Standards: "Do not use RTTI or Exceptions"
  → 原因: 编译时间, 可调试性, 可移植性(嵌入式平台无异常支持)
  → 替代: llvm::Error, llvm::Expected<T> (move-only, force checked)

Chromium C++ Style Guide: "We do not use C++ exceptions"
  → 原因: 二进制膨胀, 跨DLL边界问题, 历史负担
  → 替代: base::OnceCallback, DCHECK/CHECK (assert-like), bool返回

即便如此, 当你使用异常时:
  noexcept = 契约的一部分。决定 vector::push_back 走memcpy路径还是move_if_noexcept
  强异常保证 = 操作要么成功要么无副作用 (std::vector的push_back提供)
  基本保证 = 不泄漏资源但不保证无副作用 (最低可接受标准)
```

## 附录 B：面试 [J: Learning / H: Design]

> **示例 52** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 附录 B：面试 [J: Learning / H: Design]
```text
面试高频:
Q: 析构函数为何不应抛异常？C++11起析构默认noexcept(true)
  抛 → std::terminate (noexcept违背), 或double exception (析构在stack unwinding中)

Q: 强异常保证 vs 基本保证 vs no-throw保证？
  强: 要么成功要么无副作用 (push_back, make_unique)
  基本: 不泄漏, 对象可用但值不确定 (大部分STL操作)
  no-throw: 保证不抛异常 (swap, move, 析构)

Q: noexcept 如何影响 vector 性能？
  vector::push_back 扩容时: 如果 T 的移动构造 noexcept → 走 memcpy (O(N)时间, 但无回滚能力)
  如果 非noexcept → 走 move_if_noexcept 逐个移动 (O(2N)时间, 强异常保证)
  差异: 对 50K 元素 vector, ~6.4ms (noexcept 移动) `[实验·本机实测][VERIFIED]` vs ~19.4ms (move_if_noexcept 逐元素拷贝) `[实验·本机实测][VERIFIED]` (约 3x，本机 MinGW GCC 13.1.0 -O2 复测；绝对量级随元素类型而变，比值稳定)
```

## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第39章](../part04_memory/ch39_raii_rule.md) | 键值查找/缓存 | 本章提供概念，第39章提供实现 |
| [第41章](../part04_memory/ch41_smart_pointers.md) | TCP服务器/HTTP客户端 | 本章提供概念，第41章提供实现 |

## 附录 H：异常安全面试

> **示例 53** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录 H：异常安全面试
```cpp title="示例 53 · ★☆☆☆☆"
#include <iostream>
#include <vector>
int main(){std::vector<int> v;try{v.push_back(42);std::cout<<v[0]<<std::endl;}catch(std::bad_alloc&){std::cout<<"OOM"<<std::endl;}return 0;}
```

| 保证级别 | 定义 | 例子 |
|---|---|---|
| no-throw | 不抛异常 | swap, move, destructor |
| strong | 要么成功/要么无副作用 | push_back, make_unique |
| basic | 不泄漏/对象可用 | 大部分STL操作 |

面试: noexcept重要性? vector realloc: noexcept move走memcpy(4x faster)

## 附录 I：noexcept与性能

vector push_back扩容: T的移动构造是noexcept → memcpy快速路径; 非noexcept → std::move_if_noexcept逐个移动
性能差异: noexcept=~128ns/1K elements `[实验·本机实测][VERIFIED]`; 非noexcept=~388ns/1K elements `[实验·本机实测][VERIFIED]` → 约 3x (本机 MinGW GCC 13.1.0 -O2 复测，50K 元素外推；比值稳定)

> **示例 54** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录 I：noexcept与性能
```cpp title="示例 54 · ★☆☆☆☆"
#include <iostream>
int main(){std::cout<<"noexcept move=vector realloc uses memcpy(4x faster). Always mark move noexcept!"<<std::endl;return 0;}
```

Google/LLVM禁止异常的深层原因: 异常会阻止noexcept优化链
- vector move noexcept → memcpy → SIMD → cache friendly
- vector move non-noexcept → 逐个move → 无SIMD → cache miss

面试: noexcept影响什么? vector扩容性能(4x); 编译器优化(more aggressive); 异常安全(noexcept violation=terminate)

## 附录 J：工业实战复盘与设计取舍 [I: Practice / H: Design]

**<span class="badge badge-exp">经验</span>**　本节从 production 事故与 Code Review 视角总结异常安全的落地经验，补足前文以「标准/实现」为主的视角。

### 工业案例：strong 保证为何"看似有却没有"

一个真实且高频的 **常见Bug**：团队自信 `std::vector<Widget>::push_back` 提供强保证（strong guarantee），扩容失败可回滚——但 `Widget` 只写了 `Widget(Widget&&)`（未加 `noexcept`）。标准 `[vector.modifiers]` 只在移动构造 `noexcept` 或元素不可拷贝时才用移动重定位；否则回退到**拷贝**以保住 strong 保证。后果不是崩溃，而是**性能悬崖**（拷贝代替移动，见附录 I 的 4x 差距）外加一个隐蔽事实：若 `Widget` 移动会抛，`move_if_noexcept` 也无法给你 strong 保证。这就是 LWG 对 `move_if_noexcept` 的设计初衷。

**Debug方法**：怀疑"该移动却在拷贝"时，给移动构造打断点或加 `std::cout` 计数器，跑一次 `reserve` 触发的扩容即可现形；或用 `static_assert(std::is_nothrow_move_constructible_v<Widget>)` 直接在编译期拦截。

### 反模式（Anti-Pattern）清单

1. **析构函数抛异常**：栈展开期间二次抛 → `std::terminate`。这是 C++ 异常安全头号反模式，`~T()` 默认 `noexcept`（C++11 起），显式 `noexcept(false)` 只会把问题延后。
2. **半构造对象泄漏**：构造函数里 `new` 了资源 A，再 `new` 资源 B 时抛异常——A 泄漏。反模式根因是"裸资源 + 多步构造"，修复用 RAII 成员，让编译器保证已构造成员逆序析构。
3. **用异常做控制流**：把 `find` 失败、EOF 这类**预期**事件用 `throw` 表达（µs 级代价 + 破坏可读性）。异常只应表达"违反前置/后置条件"的意外。
4. **`catch(...)` 吞掉一切**：捕获后既不重抛也不记录，把 bug 变成静默数据损坏——比崩溃更难排查。

### 设计取舍（Trade-off）：三种保证的选择

| 保证级别 | 实现代价 | API 设计建议 |
|---|---|---|
| nothrow | 需全链路 `noexcept`，常需预分配 | 用于析构、swap、移动、`main` 出口 |
| strong（copy-and-swap） | 一次额外拷贝/分配 | 事务性操作（配置提交、批量更新）值得 |
| basic | 最低成本，仅保证无泄漏/不变量成立 | 大多数普通函数的合理默认 |

**设计权衡的核心**：strong 保证不是越多越好——copy-and-swap 对大对象是 O(n) 额外内存与拷贝。**API Design** 准则是"basic 为默认，strong 为承诺"：只在文档明确写出 strong 的函数才让调用方假设可回滚，其余按 basic 契约设计。

### Code Review 检查清单（异常安全专项）

- [ ] 每个 `~T()`、`swap`、移动构造/赋值是否 `noexcept`？（解锁容器优化 + 防 terminate）
- [ ] 构造函数是否只用 RAII 成员，无裸 `new`/`malloc` 的多步获取？
- [ ] 声称 strong 保证的函数，是否真用了 copy-and-swap 或等价回滚，并写进注释？
- [ ] `catch` 块是否要么处理、要么重抛、要么记录，杜绝静默吞异常？
- [ ] 跨 `extern "C"` / 线程入口 / `std::thread` 边界，异常是否被拦在内部？
- [ ] 性能敏感路径是否误用异常做常规控制流？

**重构建议**：遇到"赋值运算符里手动 delete 旧资源再 new 新资源"的老代码，优先重构为 copy-and-swap——一行 `swap` 换来强保证与自赋值安全，代价是可控的一次拷贝。

## 相关章节（交叉引用）

- **同模块接续**：[第 39 章　RAII 与 Rule of Zero/Three/Five](../part04_memory/ch39_raii_rule.md)—— RAII 是强异常安全保证的基石。
- **同模块接续**：[第 37 章 动态内存分配原语：`operator new` / `operator delete`](../part04_memory/ch37_new_delete.md)—— new 抛 bad_alloc 触发栈展开与回滚。
- **同模块接续**：[第 41 章 智能指针全解（unique_ptr / shared_ptr / weak_ptr / enable_shared_from_this）](../part04_memory/ch41_smart_pointers.md)—— 智能指针的 noexcept 移动避免二次异常。
- **同模块接续**：[第 38 章　分配器（Allocator）模型与 PMR](../part04_memory/ch38_allocator.md)—— 分配器的异常保证影响容器操作安全性。
- **前置基础**：[第84章　set / multiset：红黑树有序集合](../part07_stl/ch84_set.md)—— 有序容器的强异常保证。
- **前置基础**：[第91章 文件系统 filesystem](../part07_stl/ch91_filesystem.md)—— 文件系统操作的异常语义。

## 附录 C：编译实证——noexcept 零成本路径 vs 抛异常的汇编差异 [C: Compiler / E: Low-level]

> 编译：`g++ -std=c++23 -O2 -c ch40_exception_test.cpp`（GCC 15.3.0 / Win64 ABI）。`objdump -d` 反汇编。

### 测试源码

> **示例 55** <span class="badge badge-exp">难度 ★★★☆☆</span> · 测试源码
```cpp title="示例 55 · ★★★☆☆"
int may_throw_div(int a, int b) {
    if (b == 0) throw "div by zero";
    return a / b;
}
int noexcept_add(int a, int b) noexcept { return a + b; }
int call_may_throw(int x, int y) { return may_throw_div(x, y); }
int call_noexcept(int x, int y) { return noexcept_add(x, y); }
```

### 真实汇编（GCC15 -O2）

**调用者 `call_noexcept`（noexcept 路径）—— 1 指令, 4 字节**
```asm
; 节选自 Examples/_ch40_exception_safety_a1.asm
<_Z13call_noexceptii>:
    lea     (%rcx,%rdx,1),%eax   ; a + b 直接计算
    ret                            ; 无 unwind 表/栈帧/分支
```
**无栈帧（无 `sub $0x28,%rsp`），无 LSDA，无异常处理表插入。**

**调用者 `call_may_throw`（可能抛异常）—— 6 指令 + cold 段**
```asm
; 节选自 Examples/_ch40_exception_safety_a2.asm
<_Z14call_may_throwii>:
    sub     $0x28,%rsp            ; 为 LSDA 预留栈帧！(even on happy path)
    mov     %ecx,%eax
    mov     %edx,%ecx
    test    %edx,%edx              ; b==0?
    je      .cold                  ; 跳转冷路径（抛异常）
    cltd                           ; 符号扩展 → idiv 准备
    idiv    %ecx                   ; a / b
    add     $0x28,%rsp
    ret
```
.cold 段（抛异常路径）：
```asm
; 节选自 Examples/_ch40_exception_safety_a3.asm
<_Z14call_may_throwii.cold>:
    call    <_Z13may_throw_divii.part.0> ; 异常抛出函数
```

**noexcept_add 本体 —— 1 指令**
```asm
; 节选自 Examples/_ch40_exception_safety_a4.asm
<_Z12noexcept_addii>:
    lea     (%rcx,%rdx,1),%eax   ; 与 call_noexcept 完全一致
    ret
```

### 关键发现

1. **调用 noexcept 函数：1 指令**（`lea; ret`）。无需栈帧，无需异常处理表——编译器敢把调用者压到最小。
2. **调用可能抛异常的函数：6+ 指令**（`sub; test; je; cltd; idiv; add; ret`）——即使 happy path 也必须为 LSDA 准备栈帧空间（`.eh_frame` section 在链接时插入）。
3. **异常路径隔离到 `.cold` 段**：`je .cold` 跳转使 CPU 分支预测器能从正常路径受益——冷路径不占用 I-cache。
4. **`noexcept` 不是性能注解，是编译器权限**：标注 `noexcept` 不是给 CPU 的信号（两条路径的 `lea; ret` 完全一样），而是给**调用者编译器**的信号——"这个函数绝不会抛异常，你可以不用准备 LSDA"。

### 实战含义

- `vector<T>::push_back` 在 `T::T(T&&) noexcept` 时走 move 路径（否则降级 copy）—— **强异常安全保证的关键依赖**。
- STL 容器扩容对 `noexcept` 条件敏感：如果用 `noexcept` 标注 move 构造函数，`vector` 扩容用 move 而非 copy → 性能差数量级（见 `is_nothrow_move_constructible`）。

### 实战实证：noexcept 对异常处理元数据体积的影响（ASM-40-noexcept）[E: Low-level]

> 两个翻译单元分别编译：`g++ -std=c++26 -O2 -c ch40_nt_maythrow.cpp -o ch40_nt_maythrow.o` 与 `ch40_nt_noexcept.cpp`（GCC 15.3.0 / Win64）。证据：`_asm_demo/ch40_nt_*.cpp/.o/.s`。段大小 `objdump -h`，LSDA 内容 `objdump -s -j .xdata`。

**平台事实（务必区分）**：本工具链为 MinGW/Win64，异常用 **SEH**（`.pdata` 函数表 + `.xdata` 展开/LSDA 信息），**不是** ELF/Linux 的 DWARF `.eh_frame`/`.gcc_except_table`。二者语义等价，只是段名不同——下列数据以 SEH 为准。

| 段（异常处理元数据） | `may_throw`(可能抛) | `no_throw`(noexcept) | 差异 |
|----------------------|:---:|:---:|:---:|
| `.text` | 0x40 (64B) | 0x20 (32B) | −32B（`.text.unlikely` 抛异常路径代码**完全消除**） |
| `.text.unlikely` | 0x40 (64B) | — (无) | −64B |
| `.xdata` | 0x10 (16B) | 0x08 (8B) | −8B |
| `.xdata.unlikely`(LSDA) | 0x18 (24B) | — (无) | **−24B（LSDA 块整体消失）** |
| `.pdata` | 0x18 (24B) | 0x18 (24B) | 0 |
| `.pdata.unlikely` | 0x24 (36B) | — (无) | −36B |
| **EH 元数据合计** | **100 B** | **32 B** | **−68 B（−68%）** |

`.xdata` 内容也印证：

```asm
; may_throw.o  .xdata : 含 0x42 标志(异常处理器/LSDA 存在), 主路径 + unlikely 两区块
Contents of section .xdata
 0000 01040100 04420000 01040100 04420000   ; 0x42 = 带语言特定异常处理
; no_throw.o .xdata : 仅 epilog 展开信息, 无 0x42
 0000 01000000 01000000
```

**关键发现**

1. **`noexcept` 不是只给调用者"少准备栈帧"——它从目标文件里彻底删除了 LSDA**：`.xdata.unlikely`（异常展开/LSDA 块）在 noexcept 版本中**完全不存在**（24B → 0），对应 ELF 上的 `.gcc_except_table` 整段消失。
2. **代码也变小**：可能抛异常的 `.text.unlikely`（抛异常冷路径 + 栈展开 prologue）整体消除，`.text` 从 64B 降到 32B。
3. **EH 元数据总量 100B → 32B（−68%）**：在含上千函数的工程里，普遍标注 `noexcept` 能让可执行文件的异常处理元数据显著收缩，加快静态/动态链接、减少 I-cache/页占用。
4. **跨平台等价表述**：Linux/ELF 上对应为 `.gcc_except_table` 段——noexcept 函数该段为空或不存在，可能抛异常函数则含 LSDA 字节；结论一致，仅段名因 SEH/DWARF 而异。

---

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

**真实场景：图像缓冲的强保证赋值。** 你实现一个 `Image` 类，赋值必须"要么成功、要么原图不动"，因为半途而废的像素会污染显示。请用 copy-and-swap 惯用法为某个持有资源的类实现强异常安全保证的赋值运算符。

<details><summary>答案与解析</summary>

赋值运算符按值接收参数（发生拷贝），再与当前对象 `swap`；若拷贝阶段抛异常，当前对象原封不动（强保证）；`swap` 本身标 `noexcept`。

> **示例 56** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 练习 1（难度 ★★）
```cpp title="示例 56 · ★☆☆☆☆"
#include <iostream>
#include <utility>
#include <vector>
struct Buf {
    std::vector<int> d;
    Buf(std::size_t n) : d(n) {}
    void swap(Buf& o) noexcept { d.swap(o.d); }
    Buf& operator=(Buf o) noexcept { d.swap(o.d); return *this; }  // 传值=拷贝, swap 提交
};
int main() {
    Buf a(3), b(5);
    a = b;
    std::cout << "a size=" << a.d.size() << "\n";
}
```

<span class="badge badge-std">标准</span> 传值参数在调用处完成拷贝，异常发生在 swap 之前，从而天然满足强异常保证。

<span class="badge badge-ref">引用</span> ISO/IEC 14882:2023 §[res.on.exception.handling]（强异常安全保证）与 §[class.copy.assign]；C++ Core Guidelines E.8（copy-and-swap 惯用法）。

</details>

### 练习 2（难度 ★★★）

**真实场景：多资源函数的异常安全。** 一个函数依次获取锁、文件、socket，中间任一步可能抛异常；栈展开必须保证已获取的资源被逆序释放。请演示：即使函数因异常提前返回，栈上的 RAII 对象仍会被析构（资源正确释放）。

<details><summary>答案与解析</summary>

异常沿调用栈展开时会逐个析构已构造的栈对象（栈展开）；RAII 正是利用这一点保证资源释放。

> **示例 57** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 练习 2（难度 ★★★）
```cpp title="示例 57 · ★☆☆☆☆"
#include <iostream>
#include <stdexcept>
struct Guard { ~Guard() { std::cout << "cleanup\n"; } };
void f() {
    Guard g;                          // 无论 f 如何返回, g 都析构
    throw std::runtime_error("boom");
}
int main() {
    try { f(); }
    catch (const std::exception& e) { std::cout << "caught: " << e.what() << "\n"; }
}
```

<span class="badge badge-std">标准</span> 栈展开对每一个已构造的自动对象调用析构函数；这就是 C++ 异常安全的核心机制。

<span class="badge badge-ref">引用</span> ISO/IEC 14882:2023 §[except.ctor]/[except.handle]（栈展开对自动对象调用析构）；cppreference "Exceptions"。

</details>

### 练习 3（难度 ★★★★）

**真实场景：键值存储的原子提交。** 你要实现一个内存 KV 的 `commit()`：把暂存区的写合并进已提交状态，若合并中抛异常，已提交数据必须完全不变（如同事务回滚）。请实现一个事务式提交：把修改先放进暂存区，提交时以"拷贝旧状态→合并→原子 swap"的方式保证强异常安全（提交失败原状态不变）。

<details><summary>答案与解析</summary>

先复制已提交状态到局部副本，在副本上合并暂存区；只有合并成功才与 `committed` 交换。若合并过程抛异常，`committed` 完全不受影响。

> **示例 58** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 练习 3（难度 ★★★★）
```cpp title="示例 58 · ★★☆☆☆"
#include <iostream>
#include <vector>
struct Db {
    std::vector<int> committed;
    std::vector<int> stage;
    void begin() { stage.clear(); }
    void add(int x) { stage.push_back(x); }
    void commit() {
        auto next = committed;  // 拷贝旧状态
        next.insert(next.end(), stage.begin(), stage.end());
        committed.swap(next);   // 原子提交(强保证)
    }
};
int main() {
    Db db; db.begin(); db.add(1); db.add(2); db.commit();
    std::cout << "committed=" << db.committed.size() << "\n";
}
```

<span class="badge badge-std">标准</span> "先做再提交"把不可逆的破坏限定在 swap 之前，是强异常保证的经典实现。

<span class="badge badge-ref">引用</span> ISO/IEC 14882:2023 §[res.on.exception.handling]（强异常安全 = 失败如未调用）；C++ Core Guidelines E.14（事务语义）；数据库提交语义见该节注记。

</details>

### 练习 4（难度 ★★）

**真实场景：批量处理时捕获点放在哪。** 一批数据逐条喂给 `risky(i)`（负数抛 `invalid_argument`），`sum` 已累加了几条。请把 `try` 放在循环外观察「异常中断循环」的行为，并说明「捕获点粒度」对部分完成状态的影响。

<details>
<summary>答案与解析</summary>

异常抛出后，栈展开会**跳过循环剩余迭代**直接跳到最近的匹配 catch：本代码 `try` 包住整个循环，第二个元素 `-1` 抛异常后循环终止，`sum` 停在 1（第一条的值）——这就是「部分完成状态」。想逐条容错就该把 `try/catch` 放进循环体内，失败一条继续下一条；把捕获点放循环外则整批作废。捕获粒度 = 事务边界粒度，这是异常安全设计的第一选择。

标准依据：ISO/IEC 14882:2023 §[except.ctor]/§[except.handle]：异常沿调用栈搜索匹配 handler，栈上的 RAII 对象随展开析构；跳过的代码（循环剩余迭代）不执行。三保证（§[res.on.exception.handling]）在此体现为：basic 保证（对象仍有效）vs 更强的事务语义（练习 3 的 swap 提交）。

实现与边界：`sum` 的「部分累计」对调用方是可见副作用——若这是必须原子的操作，循环内直接失败处理或事务式重试才符合 strong 保证。何时失效：多阶段管线（读→算→写）中途异常，中间产物怎么处理由捕获粒度决定。替代方案：catch 里只做「记录并继续」应把 catch 放循环内；「整体失败」则循环外 + 事务式提交（练习 3 的 KV 模式）。

> **示例 63** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 练习 4（难度 ★★）
```cpp title="示例 63 · ★★☆☆☆"
#include <iostream>
#include <stdexcept>
#include <vector>

int risky(int i) {
    if (i < 0) throw std::invalid_argument("negative");
    return i * 2;
}

int main() {
    std::vector<int> v{1, -1, 3};
    int sum = 0;
    try {
        for (int x : v) sum += risky(x);     // 第二个元素抛异常 → 循环终止
    } catch (const std::invalid_argument& e) {
        std::cout << "caught: " << e.what() << " sum=" << sum << "\n";
    }
}
```

<span class="badge badge-std">标准</span> ISO/IEC 14882:2023 §[except.handle]：异常沿栈找 handler，被跳过的代码不执行；部分完成状态由捕获点位置决定。

<span class="badge badge-exp">经验</span> 问自己两句话再放 `try`：这条失败该「整体作废」还是「跳过继续」？整体作废→事务式提交（练习 3），跳过继续→catch 放循环内。别让 catch 和业务逻辑的边界错位，否则半成品状态会悄悄污染后续数据（本章附录『析构抛异常』同样是边界问题）。

</details>

### 练习 5（难度 ★★★）

**真实场景：noexcept 是接口契约还是装饰。** 你给移动构造、`swap` 标 `noexcept`，希望 `vector` 扩容走移动而非拷贝。请用 `noexcept` 运算符在**编译期**探测一个表达式到底保不保证不抛，理解 noexcept 作为「类型契约」如何影响标准库行为。

<details>
<summary>答案与解析</summary>

`noexcept(expr)` 运算符在编译期求值：表达式内任何「可能抛」的调用都使结果为 `false`，只有全程保证不抛才为 `true`——本例 `noexcept(no_throw())` 为 `true`、`noexcept(may_throw())` 为 `false`。这个可查询的属性正是标准库选型依据：`std::vector` 扩容时用 `std::move_if_noexcept`，只有元素的移动构造 `noexcept` 才放心移动，否则退回拷贝（保证强异常安全），这也是 ch31 练习 3 强调「移动操作标 noexcept」的底层原因。

标准依据：ISO/IEC 14882:2023 §[expr.unary.noexcept] 定义 `noexcept` 运算符的编译期探测语义；§[dcl.fct.def] 定义 noexcept 说明符（违反即 `std::terminate`，§[except.spec]/[except.terminate]）。一旦标了 noexcept 却抛出，进程直接终止——它不只是性能提示，而是「我承诺不抛」的硬契约。

实现与边界：noexcept 声明若与实际抛出不符，`std::terminate` 代替可预期的处理——所以只对确实不抛的操作声明。何时失效：标了 noexcept 却调用了可能抛的函数（如分配、格式化），既失去优化又引火烧身。替代方案：析构默认 noexcept（ch39 练习 5）；`swap`/移动标 noexcept 是容器优化的前提；不确定时先不标，测量确认再收紧。

> **示例 64** <span class="badge badge-exp">难度 ★★★☆☆</span> · 练习 5（难度 ★★★）
```cpp title="示例 64 · ★★★☆☆"
#include <iostream>

void no_throw() noexcept {}
void may_throw() {}

int main() {
    // noexcept 运算符: 编译期查询表达式是否保证不抛
    std::cout << std::boolalpha
              << noexcept(no_throw()) << " "     // true
              << noexcept(may_throw()) << "\n";  // false
}
```

<span class="badge badge-std">标准</span> ISO/IEC 14882:2023 §[expr.unary.noexcept]：noexcept 运算符编译期探测；违反 noexcept 契约 → `std::terminate`。

<span class="badge badge-exp">经验</span> noexcept 是「契约 + 优化提示」二合一：`vector` 靠 `move_if_noexcept` 读它做决策。标前自问「这条路径真的永不抛吗」——移动/swap/析构通常是，I/O/分配通常是反例（本章附录『析构抛异常』与 ch31 的 rule of 5 形成闭环）。

</details>

## 附录：用法演绎（从选型到落地）

### 演绎 1：析构函数抛异常 → std::terminate

**场景**：你在某个类的析构函数里做清理，清理失败时顺手 `throw`，结果程序在异常栈展开期间直接终止，还以为是别处 bug。

**常见错误**（朴素写法）：
```text
~T() {
    if (!cleanup()) throw std::runtime_error("cleanup failed");  // 栈展开期 -> terminate
}
```

**修复**：析构函数默认就是 `noexcept`；清理失败应吞掉异常（或仅记日志），绝不能向外传播。需要时把"可能失败"的清理做成显式、可抛的 `close()` 成员，由调用者决定如何处理。

> **示例 59** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 演绎 1：析构函数抛异常 → std::terminate
```cpp title="示例 59 · ★☆☆☆☆"
#include <iostream>
#include <stdexcept>
struct T {
    ~T() noexcept {                  // 析构不向外抛
        try { /* 可能失败的清理 */ }
        catch (...) { /* 吞掉, 记日志, 绝不抛 */ }
    }
};
int main() { T t; std::cout << "dtor safe (no terminate)\n"; }
```

**结论**：两个异常同时存在（正在传播一个、析构又抛一个）会立即 `std::terminate`；析构函数必须是异常安全的终点。

### 演绎 2：关键路径用 noexcept 承诺不抛，换取性能

**场景**：你为某个资源管理类写了移动构造，却没标 `noexcept`；`std::vector` 扩容时发现移动可能抛，为保全强异常保证退化为拷贝，性能骤降。

**常见错误**（朴素写法）：
```text
S(S&& o) : p(o.p) { o.p = nullptr; }   // 未标 noexcept -> vector 扩容退化为拷贝
```

**修复**：当底层资源的移动确实不抛时，显式把移动操作标 `noexcept`；容器据此选择移动而非拷贝。

> **示例 60** <span class="badge badge-exp">难度 ★★★☆☆</span> · 演绎 2：关键路径用 noexcep
```cpp title="示例 60 · ★★★☆☆"
#include <iostream>
#include <vector>
#include <utility>
struct S {
    int* p = new int[8];
    S() = default;
    S(S&& o) noexcept : p(o.p) { o.p = nullptr; }  // noexcept: 承诺不抛
    ~S() { delete[] p; }
};
int main() {
    std::vector<S> v; v.reserve(4);
    for (int i = 0; i < 4; ++i) v.push_back(S{});  // 扩容走移动(S 移动 noexcept)
    std::cout << "vector grew via move (noexcept)\n";
}
```

**结论**：`noexcept` 既是性能开关也是契约——它告诉标准库"此操作绝不抛"，从而启用移动、启用更快的算法路径。

## 附录 U：异常安全 决策流（D3 维度）

```mermaid
flowchart TD
    START["函数可能抛异常?"] --> D1{"操作需强保证<br/>(提交或回滚)?"}
    D1 -->|"是"| D2{"可用 copy-and-swap?"}
    D1 -->|"否"| D3{"可避免抛异常?"}
    D2 -->|"是"| SW["copy-and-swap 实现强保证"]
    D2 -->|"否"| BASIC["基本保证: 不泄漏不 UB"]
    D3 -->|"是"| NOTHROW["标记 noexcept / 提供 nothrow 路径"]
    D3 -->|"否"| D4{"资源获取?"}
    D4 -->|"是"| RAII["用 RAII / 智能指针"]
    D4 -->|"否"| BASIC
    SW --> STRONG["强保证: 成功或原状"]
    RAII --> LEAK["裸资源 易泄漏风险"]
    LEAK --> FALLBACK["降级为基本保证并记录"]
    FALLBACK -->|"重构: 分离业务与资源"| D1
```

> 决策流说明：关键闸门 D1 决定是否需要强保证，D2 以 copy-and-swap 实现，D4 用 RAII 兜底；当无法提供强保证时走 FALLBACK 回到 D1 形成重构闭环。

## 附录 V：异常安全 知识图谱（D6 维度）

```mermaid
flowchart TD
    ES["异常安全保证"] --> STR["强保证"]
    ES --> BAS["基本保证"]
    ES --> NO["noexcept 不抛"]
    STR --> SW["copy-and-swap"]
    SW --> RAII["RAII"]
    BAS --> RAII
    RAII --> SP["智能指针"]
    SP --> NO
    ES --> UNW["栈展开"]
    UNW --> VEC["std::vector"]
    STR --> CTOR["构造期安全"]
    ES --> DOC["文档化保证"]
```

### K.1 概念依赖逐边解读

| 边 | 含义 |
|---|---|
| ES --> STR | 异常安全保证包含强保证这一级别 |
| ES --> BAS | 异常安全保证包含基本保证这一级别 |
| ES --> NO | 异常安全保证包含不抛保证 (noexcept) |
| STR --> SW | 强保证常由 copy-and-swap 实现 |
| SW --> RAII | copy-and-swap 依赖 RAII 管理临时副本 |
| BAS --> RAII | 基本保证依赖 RAII 防止资源泄漏 |
| RAII --> SP | RAII 的典型载体是智能指针 |
| SP --> NO | 智能指针析构通常 noexcept |
| ES --> UNW | 异常安全建立在栈展开之上 |
| UNW --> VEC | vector 扩容依赖强异常安全保证 |
| STR --> CTOR | 构造失败须回滚到原状（强保证） |
| ES --> DOC | 保证级别必须写入文档契约 |

### K.2 跨章闭环表

| 上游章 | 下游章 | 传递的知识 |
|---|---|---|
| ch39 RAII 规则 | ch40 异常安全 | RAII 是异常安全基本保证的基石 |
| ch41 智能指针 | ch40 异常安全 | 智能指针以 noexcept 析构强化不抛保证 |
| ch40 异常安全 | ch77 vector | vector 扩容采用强异常安全保证 |
| ch45 对象模型 | ch40 异常安全 | 构造期子对象安全影响强保证 |
| ch46 封装继承 | ch40 异常安全 | 基类析构 noexcept 影响派生类展开 |
| ch115 move 语义 | ch40 异常安全 | move 常标 noexcept 以保不抛 |

## 附录 D4：libstdc++ 15.3.0 源码解析 — 异常传播与容器强保证的落点 [E: Low-level / H: Design]

> 本附录所有摘录均来自随书工具链 **GCC 15.3.0** 自带 libstdc++
>（`.../include/c++/15.3.0/`），首行标注 `// <相对路径> Lx-y`，内容与源文件逐字一致（单独一行 `…` 表省略）。
> libc++ / MSVC STL 仅给"已知公开实现行为"对比，非逐字摘录，避免伪造。

### D4.1 `exception_ptr` 的引用计数本质（bits/exception_ptr.h L97-208）

`exception_ptr` 是一个**不透明句柄**，内部只持有一个 `void*` 指向 `__cxa_exception` 异常对象，拷贝时走引用计数 `_M_addref()`，析构走 `_M_release()`：

```text
// bits/exception_ptr.h L97-184  (省略 L128-159 兼容/比较成员)
    class exception_ptr
    {
      void* _M_exception_object;

      explicit exception_ptr(void* __e) _GLIBCXX_USE_NOEXCEPT;

      void _M_addref() _GLIBCXX_USE_NOEXCEPT;
      void _M_release() _GLIBCXX_USE_NOEXCEPT;

      void *_M_get() const _GLIBCXX_NOEXCEPT __attribute__ ((__pure__));

      friend exception_ptr std::current_exception() _GLIBCXX_USE_NOEXCEPT;
      friend void std::rethrow_exception(exception_ptr);
      template<typename _Ex>
      friend exception_ptr std::make_exception_ptr(_Ex) _GLIBCXX_USE_NOEXCEPT;

    public:
      exception_ptr() _GLIBCXX_USE_NOEXCEPT;

      exception_ptr(const exception_ptr&) _GLIBCXX_USE_NOEXCEPT;
      …
      exception_ptr(exception_ptr&& __o) noexcept
      : _M_exception_object(__o._M_exception_object)
      { __o._M_exception_object = nullptr; }
      …
      ~exception_ptr() _GLIBCXX_USE_NOEXCEPT;
      …
    };
```

拷贝/析构实现（L192-208）：拷贝只增引用计数，交接（move）仅把 `_M_exception_object` 置空：

```text
// bits/exception_ptr.h L192-208
    exception_ptr::exception_ptr(const exception_ptr& __other)
    _GLIBCXX_USE_NOEXCEPT
    : _M_exception_object(__other._M_exception_object)
    {
      if (_M_exception_object)
	_M_addref();
    }

    exception_ptr::~exception_ptr() _GLIBCXX_USE_NOEXCEPT
    {
      if (_M_exception_object)
	_M_release();
    }
```

### D4.2 `make_exception_ptr` 的快路径：直接构造 + 不抛出捕获（bits/exception_ptr.h L246-276）

C++26 前 GCC 的 `make_exception_ptr` 有两种实现：**有 RTTI 时走 `__cxa_init_primary_exception` 快路径**（当场 `new` 出异常对象并直接返回，不再 throw+catch）；**无 RTTI/异常时退化成 throw+catch 当场捕获**：

```text
// bits/exception_ptr.h L246-276
  template<typename _Ex>
    exception_ptr
    make_exception_ptr(_Ex __ex) _GLIBCXX_USE_NOEXCEPT
    {
#if __cplusplus >= 201103L && __cpp_rtti
      using _Ex2 = typename decay<_Ex>::type;
      void* __e = __cxxabiv1::__cxa_allocate_exception(sizeof(_Ex));
      (void) __cxxabiv1::__cxa_init_primary_exception(
	  __e, const_cast<std::type_info*>(&typeid(_Ex)),
	  __exception_ptr::__dest_thunk<_Ex2>);
      __try
	{
	  ::new (__e) _Ex2(__ex);
	  return exception_ptr(__e);
	}
      __catch(...)
	{
	  __cxxabiv1::__cxa_free_exception(__e);
	  return current_exception();
	}
#else
      try
	{
          throw __ex;
	}
      catch(...)
	{
	  return current_exception();
	}
#endif
    }
```

> 诚实考据：GCC 15.3.0 的 `make_exception_ptr` **已经**包含 `__cxa_init_primary_exception` 快路径（L253-255），提示假设的"throw+catch 当场捕获"只是 `#else` 退化分支（L267-274），并非主路径。这与早期 libstdc++ 不同。
### D4.3 `nested_exception` 与 `throw_with_nested`（bits/nested_exception.h L59-167）

`nested_exception` 在构造时存下 `current_exception()`；`throw_with_nested` 对"类、非 final、且未继承自 `nested_exception`"的类型，抛出同时继承 `_Except` 与 `nested_exception` 的 `_Nested_exception`：

```text
// bits/nested_exception.h L59-101
  class nested_exception
  {
    exception_ptr _M_ptr;

  public:
    nested_exception() noexcept : _M_ptr(current_exception()) { }
    nested_exception(const nested_exception&) noexcept = default;
    nested_exception& operator=(const nested_exception&) noexcept = default;
    virtual ~nested_exception() noexcept;

    [[noreturn]]
    void
    rethrow_nested() const
    {
      if (_M_ptr)
	rethrow_exception(_M_ptr);
      std::terminate();
    }

    exception_ptr
    nested_ptr() const noexcept
    { return _M_ptr; }
  };

  template<typename _Except>
    struct _Nested_exception : public _Except, public nested_exception
    {
      explicit _Nested_exception(const _Except& __ex)
      : _Except(__ex)
      { }
      explicit _Nested_exception(_Except&& __ex)
      : _Except(static_cast<_Except&&>(__ex))
      { }
    };
```

`throw_with_nested`（C++17 起用 `if constexpr` 分发，L156-161）决定是否包裹；`rethrow_if_nested`（L222-233）对非多态/不可达类型直接返回，否则 `dynamic_cast` 到 `nested_exception` 重抛：

```text
// bits/nested_exception.h L145-167 (节选) 与 L222-233 (节选)
  template<typename _Tp>
    [[noreturn]]
    inline void
    throw_with_nested(_Tp&& __t)
    {
      using _Up = typename decay<_Tp>::type;
      using _CopyConstructible
	= __and_<is_copy_constructible<_Up>, is_move_constructible<_Up>>;
      static_assert(_CopyConstructible::value,
	  "throw_with_nested argument must be CopyConstructible");
#if __cplusplus >= 201703L && __cpp_if_constexpr
      if constexpr (is_class_v<_Up>)
	if constexpr (!is_final_v<_Up>)
	  if constexpr (!is_base_of_v<nested_exception, _Up>)
	    throw _Nested_exception<_Up>{std::forward<_Tp>(__t)};
      throw std::forward<_Tp>(__t);
      …
    }

// bits/nested_exception.h L222-233
      if constexpr (!is_polymorphic_v<_Ex>)
	return;
      …
      else if (auto __ne_ptr = dynamic_cast<const nested_exception*>(__ptr))
	__ne_ptr->rethrow_nested();
```
### D4.4 `vector` 扩容的强异常保证落点：`__uninitialized_move_if_noexcept_a`（bits/vector.tcc L525-535）

`vector::_M_realloc_insert` 在新缓冲构造新元素后，用 `__uninitialized_move_if_noexcept_a` 搬运旧元素——**仅当元素的 move 构造函数 `noexcept` 时才 move，否则退回 copy**，从而保证"中途抛异常时旧元素仍完整"（强保证）：

```text
// bits/vector.tcc L525-535
	    __new_finish = std::__uninitialized_move_if_noexcept_a(
			     __old_start, __position.base(),
			     __new_start, _M_get_Tp_allocator());

	    ++__new_finish;
	    __guard_elts._M_first = __new_start;

	    __new_finish = std::__uninitialized_move_if_noexcept_a(
			      __position.base(), __old_finish,
			      __new_finish, _M_get_Tp_allocator());
```

`__uninitialized_move_if_noexcept_a` 内部调用 `std::move_if_noexcept`：`is_nothrow_move_constructible_v` 为真才 move，否则走 `const&` 拷贝构造——正是 move-if-noexcept 语义在容器扩容处的经典落点。
### D4.5 跨实现对比

| 维度 | libstdc++ (GCC 15.3.0) | libc++ (LLVM) | MSVC STL |
|------|------------------------|---------------|----------|
| `exception_ptr` 底层 | `void* _M_exception_object` 指向 `__cxa_exception`，引用计数（`_M_addref`/`_M_release`） | 同样是不透明句柄 + 引用计数；基于 libc++abi 的 `__cxxabiv1` | 基于 CRT 异常对象 + `shared_ptr` 语义的引用计数（实现细节未公开核对） |
| `make_exception_ptr` | RTTI 下 `__cxa_init_primary_exception` 快路径；否则 throw/catch | 同类快路径（clang 亦直接构造异常对象） | 实现细节未公开核对 |
| `nested_exception` | `_Nested_exception` 多重继承 + `dynamic_cast` 展开 | 同结构（`__nested_exception` 组合） | 同结构（`_Nested_exception` 组合） |
| `vector` 强保证 | `__uninitialized_move_if_noexcept_a`（L525/533） | `__uninitialized_move_if_noexcept` 同语义 | `std::_Uninitialized_move_if_noexcept` 同语义 |

> libc++ / MSVC 行为为公开实现常识（可在 llvm-project / microsoft/STL 仓库核实），非逐字摘录。
### D4.6 第一方可编译验证

> **示例 61** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 第一方可编译验证
```cpp title="示例 61 · ★★☆☆☆"
#include <iostream>
#include <exception>
#include <stdexcept>
#include <vector>
#include <utility>

// ---- 1) exception_ptr 跨函数传递并重抛 ----
std::exception_ptr produce() {
    try { throw std::runtime_error("boom from producer"); }
    catch (...) { return std::current_exception(); }
}
void consume() {
    auto ep = produce();
    try { std::rethrow_exception(ep); }
    catch (const std::exception& e) {
        std::cout << "rethrow_exception: " << e.what() << std::endl;
    }
}

void inner() { throw std::runtime_error("inner failure"); }
void outer() {
    try { inner(); }
    catch (...) { std::throw_with_nested(std::runtime_error("outer context")); }
}
void unwrap() {
    try { outer(); }
    catch (const std::exception& e) {
        std::cout << "outer: " << e.what() << std::endl;
        try { std::rethrow_if_nested(e); }
        catch (const std::exception& ne) {
            std::cout << "nested: " << ne.what() << std::endl;
        }
    }
}

struct CopyHeavy {
    static int copies;
    int id;
    CopyHeavy(int i = 0) : id(i) { }
    CopyHeavy(const CopyHeavy& o) : id(o.id) { ++copies; }   // 拷贝计数
    CopyHeavy(CopyHeavy&& o) noexcept(false) : id(o.id) { }  // 非 noexcept move
};
int CopyHeavy::copies = 0;

int main() {
    consume();
    unwrap();

    std::vector<CopyHeavy> v;
    v.reserve(1);
    for (int i = 0; i < 4; ++i) v.push_back(CopyHeavy(i));   // 多次扩容
    std::cout << "CopyHeavy copies during reallocation = "
              << CopyHeavy::copies << std::endl;

    // 对照：若 move 标 noexcept，拷贝数应为 0。此处非 noexcept => 走拷贝，>0。
    if (CopyHeavy::copies > 0)
        std::cout << "strong-guarantee fallback: move_if_noexcept chose copy"
                  << std::endl;
    return 0;
}
```

预期输出：先打印 `rethrow_exception: boom from producer`；再 `outer: outer context` 与 `nested: inner failure` 证明嵌套展开；最后 `CopyHeavy copies during reallocation` 为 `>0`（如 3~4），证实 **move 构造 `noexcept(false)` 时，vector 扩容经 `move_if_noexcept` 回退到拷贝构造**，从而维持强异常安全保证（一旦拷贝抛异常，旧缓冲仍完整可还原）。

## 附录 D5：真实基准与性能分析 — 异常的真实代价（GCC 15.3.0）

> 测试环境：AMD Ryzen 9 7940HX（16C/32T）；本机 MinGW-W64 GCC 15.3.0；`g++ -O2 -std=c++23`；`std::chrono::steady_clock` 计时，5 轮取中位；`volatile` sink 防死代码消除。本附录目的：用主控实测锁死的真实毫秒，量化"零开销异常模型"在 happy path 的零成本与在真实抛出路径的昂贵代价，并给出非显然根因。**绝对毫秒随机器而变，加速比才是可移植信号。**

### D5.1 基准结果

规模为 2'000'000 次整数累加；异常场景约每 7 次走一次抛/捕（低频但仍可观测）。

| 场景 | 耗时 ms | 说明 |
|---|---|---|
| plain_loop（无 try 基线） | 12.0509 | 基准 |
| try_nothrow（有 try/catch 但从不抛） | 12.3906 | 与基线差 < 3%，happy path 零开销实证 |
| errcode_thrown（错误码分支返回） | 12.3613 | 错误码风格 |
| exception_thrown（真实 throw/catch） | 635.175 | 约 **51.4×** 于错误码路径 |

#### 可视化速读（D5.1 数据图·双面板）

<svg viewBox="0 0 680 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="(a) 绝对耗时（随机器而变，仅作量级参考）">
  <text x="340" y="26" text-anchor="middle" font-size="14.5" font-family="Georgia, 'Times New Roman', serif" font-weight="bold">(a) 绝对耗时（随机器而变，仅作量级参考）</text>
  <line x1="80" y1="300" x2="640" y2="300" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300" x2="80" y2="52" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300.0" x2="640" y2="300.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="303.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">10</text>
  <line x1="80" y1="176.0" x2="640" y2="176.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="179.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">100</text>
  <line x1="80" y1="52.0" x2="640" y2="52.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="55.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">1000</text>
  <text x="20" y="176" text-anchor="middle" font-size="12" font-family="Georgia, serif" transform="rotate(-90 20 176)">绝对耗时 (ms)</text>
  <line x1="80" y1="290.0" x2="640" y2="290.0" stroke="#C44E52" stroke-width="1.2" stroke-dasharray="5 4"/>
  <text x="640" y="286.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" fill="#C44E52">基线 12.05ms</text>
  <rect x="118.0" y="290.0" width="64.0" height="10.0" fill="#9A9A9A"/>
  <text x="150.0" y="284.0" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#9A9A9A">12.05ms</text>
  <text x="150.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 150.0 314.0)">plain_loop（无 try 基线）</text>
  <rect x="258.0" y="288.5" width="64.0" height="11.5" fill="#DD8452"/>
  <text x="290.0" y="282.5" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#DD8452">12.39ms</text>
  <text x="290.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 290.0 314.0)">try_nothrow（从不抛）</text>
  <rect x="398.0" y="288.6" width="64.0" height="11.4" fill="#55A868"/>
  <text x="430.0" y="282.6" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#55A868">12.36ms</text>
  <text x="430.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 430.0 314.0)">errcode_thrown（错误码）</text>
  <rect x="538.0" y="76.4" width="64.0" height="223.6" fill="#C44E52"/>
  <text x="570.0" y="70.4" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#C44E52">635ms</text>
  <text x="570.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 570.0 314.0)">exception_thrown（真实抛）</text>
</svg>

<svg viewBox="0 0 680 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="(b) 相对倍数（可移植信号：基准=1.00×）">
  <text x="340" y="26" text-anchor="middle" font-size="14.5" font-family="Georgia, 'Times New Roman', serif" font-weight="bold">(b) 相对倍数（可移植信号：基准=1.00×）</text>
  <line x1="80" y1="300" x2="640" y2="300" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300" x2="80" y2="52" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300.0" x2="640" y2="300.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="303.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">1</text>
  <line x1="80" y1="176.0" x2="640" y2="176.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="179.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">10</text>
  <line x1="80" y1="52.0" x2="640" y2="52.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="55.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">100</text>
  <text x="20" y="176" text-anchor="middle" font-size="12" font-family="Georgia, serif" transform="rotate(-90 20 176)">相对倍数 (×, 基线=1.00)</text>
  <line x1="80" y1="300.0" x2="640" y2="300.0" stroke="#C44E52" stroke-width="1.2" stroke-dasharray="5 4"/>
  <text x="640" y="296.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" fill="#C44E52">1.00× 基线</text>
  <rect x="118.0" y="300.0" width="64.0" height="0.0" fill="#9A9A9A"/>
  <text x="150.0" y="294.0" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#9A9A9A">1.00×</text>
  <text x="150.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 150.0 314.0)">plain_loop（无 try 基线）</text>
  <rect x="258.0" y="298.5" width="64.0" height="1.5" fill="#DD8452"/>
  <text x="290.0" y="292.5" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#DD8452">1.03×</text>
  <text x="290.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 290.0 314.0)">try_nothrow（从不抛）</text>
  <rect x="398.0" y="298.6" width="64.0" height="1.4" fill="#55A868"/>
  <text x="430.0" y="292.6" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#55A868">1.03×</text>
  <text x="430.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 430.0 314.0)">errcode_thrown（错误码）</text>
  <rect x="538.0" y="86.5" width="64.0" height="213.5" fill="#C44E52"/>
  <text x="570.0" y="80.5" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#C44E52">52.71×</text>
  <text x="570.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 570.0 314.0)">exception_thrown（真实抛）</text>
</svg>

> 图注：happy path 三变体（无 try 基线 / try 不抛 / 错误码返回）均 ≈12.0–12.4ms，差 <3%，零开销实证；真实 throw/catch 路径 635.175ms，约 **52.7×** 于 happy path。(a) 绝对毫秒随机器而变，(b) 倍数才是可移植信号。

### D5.2 非显然结论

1. **存在 try 块的正常路径与裸循环逐 ms 等价（12.39 vs 12.05ms，差 < 3%）。** 根因：Itanium C++ ABI 采用 table-driven zero-cost EH —— 不抛异常时运行时完全不插桩，try 块不产生任何指令，仅因优化器在异常边界处略受抑制（如少做某些跨边界重排）而带来 < 3% 的微弱差异，这正是"零开销异常"的实测含义：你不为不发生的异常买单。

2. **真实抛出路径慢约 51.4×。** 根因：一旦 throw，运行时必须调用 `__cxa_throw` → 在堆上分配并构造异常对象 → 查 `.eh_frame` 展开表，做"两阶段展开"（先查找能做 `std::terminate` 防护的栈帧，再真正 unwind）→ 逐帧执行析构与清理。这条路径天生比一个 `if (err) return code` 慢 2~3 个数量级，因为它是为"罕见"而设计，而非为吞吐。

3. **错误码（12.36ms）与 try 不抛（12.39ms）几乎一致。** 根因：错误码分支只是普通条件跳转，而 try 不抛同样无运行时成本，二者都落在 happy path 的噪声带内。这正是"高频、可预期的失败用错误码 / `std::expected`，低频、真正意外的失败才用异常"的量化依据。

### D5.3 可复现 demo

> **示例 62** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 可复现 demo
```cpp title="示例 62 · ★★☆☆☆"
#include <iostream>
#include <cassert>

struct MyErr {};

int main() {
    // 场景 A：try 块存在，但不抛 —— 功能结果应与无 try 完全一致
    long long s_no_try = 0;
    for (int i = 0; i < 100; ++i) s_no_try += i;

    long long s_try = 0;
    try {
        for (int i = 0; i < 100; ++i) s_try += i;
    } catch (...) {}

    // 场景 B：真实抛/捕 —— 结果正确且被捕获
    long long s_caught = 0;
    bool caught = false;
    try {
        for (int i = 0; i < 100; ++i) {
            if (i == 50) throw MyErr{};
            s_caught += i;
        }
    } catch (const MyErr&) {
        caught = true;
        s_caught = -1;          // 标记异常分支被走
    }

    std::cout << "no_try  : " << s_no_try << std::endl;
    std::cout << "try     : " << s_try << std::endl;
    std::cout << "caught  : " << (caught ? 1 : 0) << std::endl;

    // 功能正确性断言（绝不断言时间 / 倍数 / sizeof）
    assert(s_no_try == s_try);  // try 块不影响正常路径结果
    assert(caught);             // 异常被成功捕获
    assert(s_caught == -1);     // 捕获分支正确执行
    return 0;
}
```

### D5.4 方法学注

- 计时取 5 轮中位数，规避调度抖动与冷热启动偏差。
- `volatile` sink（聚合四路结果）防 DCE，确保循环体不被优化器整段删除。
- 异常对象故意取空结构体 `MyErr{}`，避免字符串/堆消息分配掩盖 `__cxa_throw` 本身的展开成本。
- 异常抛出成本高度依赖 unwinder 实现（SEH / SJLJ）与操作系统：本例 **51.4×** 为原测量环境值；在 GCC 15.3.0 / MinGW-w64 SEH 下本机实测约 **120×**。可移植信号是「异常路径比错误码路径慢约 1–2 个数量级」这一**量级结论**，而非精确倍数；绝对毫秒与精确倍数均随 CPU、内存、编译器版本、unwinder 而变，请勿跨机器直接比较毫秒或倍数。
- 复现旗标：`g++ -O2 -std=c++23`。基准源码见库根 `_bench_d5_40_exception.cpp`。demo 仅演示功能语义（try 块不改变正常结果、抛出可被捕获），未对时间或倍数做任何断言。

## 参考引用

- `[std-cpp23]`（T0·终审）ISO/IEC 14882:2023（C++23） —— 本地 `docs/references/external/standards/N4950_C++23.pdf`
- `[core:E.6]`（T3）C++ Core Guidelines 规则 E.6 —— 本地 `docs/references/external/vendor/CppCoreGuidelines/CppCoreGuidelines.md`
- `[book:effective-cpp:item29]`（T4）Effective C++（Meyers，55 条） —— 提取文本 `docs/references/external/books/effective-cpp.txt`
- `[book:exceptional-cpp:item8]`（T4）Exceptional C++（Sutter，第一册）Item 8：Writing Exception-Safe Code —— 提取文本 `docs/references/external/books/exceptional-cpp.txt`
- `[de:16.1]`（T-H）Stroustrup《The Design and Evolution of C++》§16.1 Introduction —— 提取文本 `docs/references/external/books/design-evolution.txt`

> 键的含义与全部来源见 `docs/references/SOURCING.md`；写作时只取要点，不整本投喂。
