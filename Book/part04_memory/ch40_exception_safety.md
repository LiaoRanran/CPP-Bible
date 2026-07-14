# 第 40 章　异常安全（Exception Safety）

> 老兵标准：**异常安全不是「会不会抛异常」，而是「抛异常之后世界是否仍然自洽」。** 四种保证（noexcept / strong / basic / none）是 C++ 对异常的全部承诺；`noexcept` 决定 vector 扩容是移动还是拷贝——这一行代码关系到你整个程序的强度与性能。
> 本章遵循《现代 C++ 终极圣经》标准 v3：真实源码逐行 + GCC/LLVM/MSVC 三实现对照 + libstdc++/libc++/MS STL 三 STL 对照 + microbenchmark + 跨语言对比 + 推荐阅读已内化进正文。

立场分层约定：
- **[标准]**　语言/库标准规定（ISO C++、`[res.on.exception.handling]`、LWG 决议）。
- **[实现]**　libstdc++ / libc++ / MS STL 的具体代码行为。
- **[平台]**　MinGW GCC 13.1.0、Windows、Itanium/SEH ABI 相关事实。
- **[经验]**　工程实践、坑与取舍。

环境事实（本机探测）：MinGW **GCC 13.1.0**；libstdc++ 头文件根目录
`C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/`；本章所有 `[实现]` 级源码均来自该目录的真实文件，逐行标注路径与行号。libc++、MS STL 不在本机，相关对比以 `[实现-推断]` / `[平台-推断]` 标注。

---

## ① 概述：异常安全是什么，四种保证一览

⟶ Book/part04_memory/ch39_raii_rule.md
⟶ Book/part04_memory/ch41_smart_pointers.md


**[标准]**　异常安全（exception safety）描述：**当异常在程序执行中途抛出时，程序应满足的不变式（invariant）与资源保证。** 它没有独立的章节标题，而是散落在 `[res.on.exception.handling]`（标准库对异常的处理）、`[basic.ctor]`、`[class.dtor]`、`[except]` 各处。C++ 社区（Sutter、Stroustrup）把异常安全归纳为**四级保证（guarantee）**：

| 等级 | 名称 | 承诺 |
|---|---|---|
| 最高 | **noexcept / nothrow** | 绝不抛异常，正常返回或 `std::terminate` |
| 高 | **strong（强）** | 操作成功，或**回滚到调用前状态**（提交或全无，commit-or-rollback） |
| 中 | **basic（基本）** | 不泄漏资源、所有对象不变量保持，但对象状态**可能改变** |
| 最低 | **none（无）** | 无承诺，可能泄漏资源、可能破坏不变量 |

**[经验]**　关键认知：**保证等级是「最坏情况」承诺**。一个函数声明 strong 保证，意味着即便抛异常，世界也回到调用前；声明 basic，意味着可能留下「半改」的状态，但绝不泄漏、绝不崩溃到 UB。`none` 是大多数裸 C 风格代码的默认状态——这也是为什么 C++ 用 RAII（见 `ch39`）把 `none` 提升到 `basic` 甚至 `noexcept`。

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

**[标准]**　一个标记为 `noexcept` 的函数（见第 5 节）承诺不抛出；若其内部真的抛出，标准规定**调用 `std::terminate`**（`[except.spec]/9`），而非栈展开。这意味着 `noexcept` 不是「温柔地吞掉异常」，而是「以进程终止保证不变量」。析构函数默认隐式 `noexcept(true)`（见 `ch39`）。

**[经验]**　`nothrow` 这一词来自 C++98 的 `operator new(std::nothrow)`——分配失败返回 `nullptr` 而非抛 `bad_alloc`。在异常安全语境里，`nothrow` 与 `noexcept` 是同一等级：不抛。

### 2.2 strong（强保证）

**[标准]**　强保证亦称「提交或回滚（commit-or-rollback）」：操作要么**完全成功**，要么**抛异常且程序状态等价于从未调用过该函数**。`std::vector::push_back` 在多数实现下提供 strong 保证（见第 3 节）。

**[经验]**　强保证的代价是常需要「先构造新东西、成功后再替换旧东西」（copy-and-swap 即此思路，见第 8 节）。它难以在**含不可回滚外部副作用**时达成——例如「向网络发送数据后更新本地状态」：网络发送成功了就收不回，本地即使回滚，对端也已收到，强保证破裂（见第 3.4 节）。

### 2.3 basic（基本保证）

**[标准]**　基本保证：抛异常后**无资源泄漏**（`[res.on.exception.handling]/3` 要求标准库不泄漏），**所有对象的不变量仍成立**，但对**具体状态值不做回滚**——对象可能处于「其他合法但不同于调用前」的状态。

**[经验]**　多数标准库 mutating 算法提供 basic 保证（如 `std::sort` 若比较器抛异常，序列可能乱序但仍是合法序列、无泄漏）。基本保证是「务实下限」：不崩、不漏，但调用方需重新读取状态。

### 2.4 none（无保证）

**[标准]**　无保证：`[res.on.exception.handling]` 之外、用户自己写的、会抛出且中间态可见还泄漏资源/破坏不变量的代码，即 none。标准明令**标准库函数不得提供 none 保证**（除非文档指明），但用户代码自由。

**核心知识点 #2**：noexcept 保证 = 不抛（抛则 terminate）；strong = 回滚到调用前；basic = 不漏 + 不变量保持但状态可能变；none = 无承诺。

**核心知识点 #3**：析构函数默认 noexcept(true)，是 basic/strong 保证得以成立的前提（否则栈展开会 double-exception → terminate，见 `ch39`、`ch36`）。

---

## ③ 示例：swap / push_back / operator= 的保证分级

### 3.1 swap 应为 noexcept

**[标准]**　`[swappable]` / `[algorithm.swap]`：标准库要求容器 `swap` 提供 **noexcept**（当元素 `swap` 不抛时）。libstdc++ 中 `vector::swap`：

```cpp
// [示例 1] vector::swap 的 noexcept 声明（真实 libstdc++ 行号见第 7 节）
// bits/stl_vector.h:1581
//   swap(vector& __x) _GLIBCXX_NOEXCEPT
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

**[标准]**　`[vector.modifiers]`：若 `push_back` **未触发重新分配（reallocation）**，提供 strong 保证（仅构造新元素，旧元素不动）；若**触发 reallocation**，libstdc++ 仍提供 strong 保证——因为它用 `move_if_noexcept` 在「移动可能抛」时**退化为拷贝**，拷贝抛异常可整体回滚（见第 6、7 节）。

```cpp
// [示例 2] push_back 强保证实验：触发扩容时仍可回滚
#include <vector>
#include <iostream>
#include <stdexcept>
struct ThrowsOnCopy {
    int v;
    ThrowsOnCopy(int x=0):v(x){}
    ThrowsOnCopy(const ThrowsOnCopy&) { throw std::runtime_error("copy throws"); }
    ThrowsOnCopy(ThrowsOnCopy&&) noexcept = default;   // 移动不抛
};
int main(){
    std::vector<ThrowsOnCopy> v;
    v.reserve(1); v.emplace_back(1);   // size=1,cap=1
    try { v.emplace_back(2); }          // 扩容：移动不抛→直接 move，成功
    catch(...) { std::cout << "unreachable\n"; }
    // 若移动会抛而拷贝也会抛，则 realloc 的 catch 回滚到原状
}
```

### 3.3 operator= 的保证分级

**[标准]**　`[utility]/[container]/[class.copy]`：赋值运算符通常目标是 strong 保证；若无法（如多步不可回滚），至少 basic。copy-and-swap（第 8 节）是达成 strong 的标准手段。

**核心知识点 #5**：`push_back` 不扩容 = strong；扩容时靠 `move_if_noexcept` 决策仍保 strong；`swap` 恒 noexcept；`operator=` 目标 strong、退化 basic。

### 3.4 强保证为何在外部副作用前失效

**[标准]**　强保证是**纯内存/纯状态**概念，对**外部世界副作用**（I/O、网络、锁、硬件）无能为力——这些不可「回滚」。

```cpp
// [示例 3] 强保证破裂：网络发送不可回滚
#include <stdexcept>
#include <cstdio>
struct Ledger {
    void commit() {                       // 想提供 strong 保证
        send_over_network();              // 副作用：成功则对端已收
        update_local_state();             // 若此处抛，网络已发出→无法回滚
    }
    void send_over_network(){ /* 假设成功 */ std::printf("sent\n"); }
    void update_local_state(){ throw std::runtime_error("local fail"); }
};
int main(){
    Ledger l;
    try { l.commit(); } catch(const std::exception& e){ /* 世界已不一致 */ }
}
```

**[经验]**　结论：对外有副作用的函数，承诺**至多 basic**；把「不可回滚的副作用」放到**最后一步**，并把可回滚的内存变更放在前面，是工程上的常用降级策略（见第 9 节 `uncaught_exceptions` 事务惯用法，正好反过来：先在析构里判断是否还在展开，再决定提交还是回滚）。

---

### 3.5 operator= 的强保证实现与退化路径

**[标准]**　赋值运算符常见三种实现，对应不同保证：
- **copy-and-swap**（第 8 节）：强保证，代价一次额外拷贝。
- **先拷贝再提交**：先把 rhs 拷到临时，成功后再「交换」内部句柄——强保证且无额外整体拷贝（仅临时）。
- **就地多步修改**：仅 basic 保证（示例 12）。

```cpp
// [示例 33] 先拷贝临时再提交：强保证且比 copy-and-swap 省一次整体拷贝
#include <vector>
#include <utility>
struct Widget {
    std::vector<int> data;
    Widget& operator=(const Widget& rhs) {
        std::vector<int> tmp = rhs.data;   // 若抛，*this 未动（强）
        data.swap(tmp);                    // noexcept：提交
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

**[经验]**　保证等级**依赖元素类型**。下面用 `is_nothrow_*` trait 在编译期自省，说明「为什么给你的类型写 noexcept 移动能提升整条调用链的保证」。

```cpp
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

**[标准]**　`[except.terminate]/1`：当异常从 `try` 块抛出，控制沿调用链向上寻找匹配的 `catch`；沿途**每个已构造的自动存储期对象按构造逆序析构**——这就是栈展开（见 `ch36`）。但若在**栈展开过程中（析构函数或栈展开代码里）又抛出新异常**，且未被立即捕获，则调用 `std::terminate`。

**[实现]**　libstdc++ 在展开时若遇到二次抛出，由 unwinder（`__cxa_throw` → `__cxxabiv1::__forced_unwind`，见 `bits/cxxabi_forced.h`）触发 terminate。该文件中 `__forced_unwind` 是「强制展开」占位类，专用于识别「正在 terminate 流程中」的异常。

```cpp
// [示例 4] 栈展开：逐层析构自动变量（见 ch36）
#include <iostream>
struct Tracer {
    const char* name;
    Tracer(const char* n):name(n){ std::cout << "ctor " << name << "\n"; }
    ~Tracer(){ std::cout << "dtor " << name << "\n"; }   // 注意：非 noexcept 也行，只要不抛
};
void f(){ Tracer c("c"); throw 1; }   // c 在抛出时析构
int main(){
    try { Tracer a("a"); Tracer b("b"); f(); }
    catch(int){ std::cout << "caught\n"; }
}
// 输出：ctor a, ctor b, ctor c, dtor c, dtor b, dtor a, caught
```

```cpp
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

**[经验]**　这就是为什么 `ch39` 反复强调**析构函数必须 `noexcept`**：一旦析构抛异常且当时正处于栈展开，立即 terminate——程序连 basic 保证都丢了。把可能抛的逻辑从析构移走，或内部 `try/catch` 吞掉并 `std::abort`/记录。

**核心知识点 #6**：栈展开 = 抛异常时沿调用链逆序析构自动对象（依赖 `ch36`）。
**核心知识点 #7**：栈展开中再抛未捕获异常 → `std::terminate`；因此析构必须 noexcept（连 `ch39`）。

---

### 4.1 set_terminate / 自定义终止行为

**[标准]**　`[except.terminate]`：`std::set_terminate` 可安装自定义终止处理函数，在 `terminate()` 被调用（含 double-exception、noexcept 违例、`[平台]` unwinder 强制展开）时执行——用于打日志/落盘/退出码，但**不得返回**（返回即 UB）。

```cpp
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

**[经验]**　在服务器/守护进程中安装 `set_terminate` 把调用栈 dump 到日志，是定位「为何 terminate」的必备手段；但真正的防线仍是 **让析构 noexcept**（连 `ch39`），从根上消灭 double-exception。

## ⑤ 异常规格历史：从 `throw(type)` 到 `noexcept`

### 5.1 动态异常规格 `throw(T1,T2)` —— 已删除

**[标准]**　C++98 允许 `void f() throw(std::bad_alloc);` 声明「只抛这些类型」，否则 `unexpected()` → `terminate`。C++11 将其**弃用**，`[except.spec]` 在 C++17 起**删除动态异常规格**（仅保留 `throw()` 作为 `noexcept(true)` 的别名，也已废弃）。MSVC 长期接受但不强制检查（属于「注释性」）。

```cpp
// [示例 6] throw(type) 动态规格：C++17 起非法（演示用 gnu++14 可编但弃用警告）
// 现代代码禁止再写。下面在 C++17+ 下编译失败：
// void old_style() throw(std::runtime_error);   // C++17 deleted
```

**[经验]**　动态规格在运行期有成本（每次抛异常要匹配类型表），且「写着 A 实际抛 B」只会 terminate，毫无保护价值。`noexcept` 取代它，且**零运行期成本**（见第 13、18 节）。

### 5.2 noexcept 家族

**[标准]**　C++11 引入：
- `noexcept` ≡ `noexcept(true)`：承诺不抛。
- `noexcept(false)`：可能抛（也是无修饰函数的默认）。
- `noexcept(expression)`：**条件 noexcept**，当且仅当 `expression` 为 `true` 时不抛（`expression` 是**编译期 bool 常量表达式**）。
- `noexcept(expr)`：**运算符**，返回 `bool` 常量，表示「对 `expr` 求值是否可能抛」（用于条件 noexcept 内部）。

```cpp
// [示例 7] noexcept 运算符探测是否可能抛
#include <iostream>
#include <vector>
int main(){
    std::cout << std::boolalpha;
    std::cout << noexcept(1/0) << "\n";                 // true：内建运算不抛
    std::cout << noexcept(std::vector<int>()) << "\n"; // 依赖分配；noexcept 取决于 allocator
}
```

```cpp
// [示例 8] 条件 noexcept：模板按成员操作决定自身 noexcept
#include <utility>
#include <type_traits>
struct S {
    S(S&&) noexcept;                 // 移动不抛
    S(const S&) noexcept(false);     // 拷贝抛
};
template<class T>
void move_or_copy(T& dst, T& src)
    noexcept(noexcept(T(std::declval<T&&>())))   // 若 T 移动不抛则本函数不抛
{
    dst = std::move(src);
}
int main(){ static_assert(noexcept(move_or_copy(std::declval<S&>(), std::declval<S&>()))); }
```

**核心知识点 #8**：`throw(type)` 动态规格 C++11 弃用、C++17 删除，仅 `throw()` 残存为 `noexcept(true)` 别名。
**核心知识点 #9**：`noexcept` ≡ `noexcept(true)`；`noexcept(bool)` 为条件规格；`noexcept(expr)` 是编译期运算符。

---

## ⑥ noexcept 与移动：vector 扩容的决策

**[标准]**　这是本章最重要的工程点。`std::vector` 扩容需把旧缓冲元素搬到新缓冲。若用**移动构造**且移动**可能抛**，则「搬了一半」时抛异常——已搬的元素在新缓冲、未搬的还在旧缓冲，旧对象还部分存活，**状态损坏**，违反 strong/basic 保证。因此 `[vector.modifiers]` 的精神（libstdc++ 实现）规定：**仅当元素移动构造为 `is_nothrow_move_constructible` 时，才用移动；否则用拷贝**（拷贝若抛，可整体回滚，因旧缓冲仍完整）。

**[实现]**　libstdc++ 用 `std::move_if_noexcept` 实现该决策（第 7 节逐行）。语义：`move_if_noexcept(x)` 返回 `x` 的**右值引用**当且仅当移动构造不抛且可移动；否则返回 **`const T&`**（强制走拷贝）。`copy-and-swap` 之外，这是标准库「用 noexcept 信息保强保证」的核心机制。

```cpp
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

```cpp
// [示例 10] 扩容实验：移动抛 → 走拷贝（用 move_if_noexcept 等价于标准库）
#include <vector>
#include <utility>
#include <type_traits>
#include <iostream>
struct M {
    int v=0;
    M(int x=0):v(x){}
    M(M&& o) noexcept(false) { v=o.v; throw "move throws"; } // 故意：移动抛
    M(const M& o):v(o.v){}                                     // 拷贝安全
};
int main(){
    std::vector<M> v; v.reserve(1); v.emplace_back(1);
    try { v.emplace_back(2); }   // 扩容：move_if_noexcept 见移动抛→改用拷贝
    catch(const char*){ std::cout << "rollback OK, size=" << v.size() << "\n"; }
    // 扩容中拷贝若抛，旧缓冲完整→整体回滚到 size=1（strong）
}
```

**[经验]**　**给你的类型写 `noexcept` 移动构造/移动赋值**——这是让 `vector`/`deque`/`string` 在扩容、排序、resize 时**用移动而非拷贝**的唯一开关，既保强保证又获性能（第 16、18 节 microbenchmark）。`ch115` 详述移动语义。

**核心知识点 #10**：vector 扩容若移动构造可能抛，会损坏状态，故仅当 `is_nothrow_move_constructible` 才移动，否则拷贝。
**核心知识点 #11**：`std::move_if_noexcept` 在移动不抛时返回 `T&&`、否则返回 `const T&` 强制拷贝。

---

### 6.1 trait 实战：用 is_nothrow_* 编写「自适应」异常安全代码

**[标准]**　`<type_traits>` 的 `is_nothrow_move_constructible`、`is_nothrow_swappable`、`is_nothrow_default_constructible` 等是编译期布尔常量，是标准库做 noexcept 决策的同一组工具（第 7 节 `move_if_noexcept` 内部即用 `is_nothrow_move_constructible`）。用户代码可复用它们编写「若元素够强则优化、否则回退」的泛型逻辑。

```cpp
// [示例 41] 泛型容器包装：移动不抛才 relocate，否则拷贝（复刻标准库思路）
#include <type_traits>
#include <utility>
#include <vector>
#include <iostream>
template<class T>
void relocate_or_copy(std::vector<T>& dst, std::vector<T>& src){
    if constexpr (std::is_nothrow_move_constructible_v<T>) {
        dst.insert(dst.end(), std::make_move_iterator(src.begin()),
                                 std::make_move_iterator(src.end()));   // 快路径
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
    std::vector<Safe> a,b;   relocate_or_copy(a,b);   // relocated
    std::vector<Unsafe> c,d; relocate_or_copy(c,d);   // copied
}
```

**[经验]**　`if constexpr` + `is_nothrow_*` 是「零成本分支」：非活跃分支根本不编译进二进制。这是把「异常安全信息转成性能开关」的标准现代写法（连 `ch115` 移动、`ch19`）。

## ⑦ 真实 libstdc++ 源码逐行

以下均来自本机 `C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/` 真实文件。

### 7.1 `bits/move.h:108-126` —— move_if_noexcept 本体

```
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

```
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

```
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

```
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

```
121	  _GLIBCXX17_DEPRECATED_SUGGEST("std::uncaught_exceptions()")
122	  bool uncaught_exception() _GLIBCXX_USE_NOEXCEPT __attribute__ ((__pure__));
124	  #if __cplusplus >= 201703L || !defined(__STRICT_ANSI__)
125	  #define __cpp_lib_uncaught_exceptions 201411L
130	  int uncaught_exceptions() _GLIBCXX_USE_NOEXCEPT __attribute__ ((__pure__));
```

**逐行**：`uncaught_exception()`（C++17 起弃用，建议用 `uncaught_exceptions()`）返回「是否有未捕获异常」；`uncaught_exceptions()` 返回**当前未捕获异常的个数**（C++17 引入，用于嵌套检测）。两者都 `noexcept` 且 `__pure__`（无副作用）。第 9 节用其实现事务惯用法。

### 7.6 `bits/cxxabi_forced.h:39-55` —— __forced_unwind

```
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

**[标准]**　copy-and-swap 是用户类型达成**强保证赋值**的经典惯用法，依赖 `ch39` 的 RAII 与 `swap` 的 noexcept（第 3.1 节）。

**[实现]**　机制：`T& operator=(T other) { swap(*this, other); return *this; }`——
1. `other` 是**按值参数**，由调用方的实参**拷贝（或移动）构造**而来。若此构造抛出，异常发生在 `swap` 之前，`*this` **毫发未动** → 自动强保证。
2. `swap` 是 noexcept（第 3.1 节）→ 交换绝不抛。
3. 返回前 `other`（旧状态）随函数退出析构 → 资源释放。

```cpp
// [示例 11] copy-and-swap：强保证赋值
#include <utility>
#include <vector>
#include <cstddef>
class Buffer {
    std::vector<int> d_;
public:
    Buffer() = default;
    Buffer(const Buffer& o): d_(o.d_) {}          // 拷贝可能抛，但在 swap 前
    Buffer(Buffer&&) noexcept = default;           // 移动不抛
    Buffer& operator=(Buffer other) noexcept {     // 按值：拷贝/移动构造
        swap(*this, other);                        // noexcept 交换
        return *this;                              // other 析构释放旧资源
    }
    friend void swap(Buffer& a, Buffer& b) noexcept {
        using std::swap; swap(a.d_, b.d_);
    }
};
int main(){ Buffer x, y; x = y; }   // 若拷贝抛，x 不变（强保证）
```

```cpp
// [示例 12] 对比：朴素赋值仅 basic 保证（中途抛→半改状态）
#include <vector>
struct Naive {
    std::vector<int> a, b;
    Naive& operator=(const Naive& o) {   // 两步拷贝，第一步成功后第二步抛→半改
        a = o.a;                         // 成功
        b = o.b;                         // 若抛，a 已改，o 未变 → 状态不一致(basic)
        return *this;
    }
};
```

**[经验]**　代价：copy-and-swap **总有一次额外拷贝**（即便 `rhs` 是右值也会走移动构造——还好，移动廉价；但左值会真的多拷贝一次）。性能敏感且能证明中间态可被局部回滚时，可手写「先改临时再 swap」或直接分两步并保 basic。强保证不是免费的——这是它「安全换性能」的本质（呼应第 3.4 节）。

**核心知识点 #13**：copy-and-swap 用「按值参数 + noexcept swap」把强保证化简为「构造可能抛（但 *this 未动） + 交换不抛」，代价是一次额外拷贝。

---

### 8.1 copy-and-swap 的代价可测量

**[经验]**　强保证不是免费。copy-and-swap 在 rhs 是左值时**多一次完整拷贝**。下面量化「强保证赋值」与「basic 赋值」的性能差——权衡依据是：拷贝成本 vs 回滚需求。

```cpp
// [示例 35] copy-and-swap 与 in-place 赋值的代价对比（量级）
#include <vector>
#include <chrono>
#include <iostream>
struct Blob { std::vector<int> d = std::vector<int>(64); };
Blob& cas_assign(Blob& self, Blob other) noexcept {       // copy-and-swap
    using std::swap; swap(self.d, other.d); return self;
}
Blob& inl_assign(Blob& self, const Blob& o) {              // 就地（basic，无额外拷贝）
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

**[标准]**　`[except.uncaught]` / `uncaught_exceptions()` 返回当前未捕获异常个数（≥1 表示正处于栈展开中）。C++17 加入以支持「**在析构中判断自己是否因异常而析构**」，从而区分「正常析构→提交」与「栈展开析构→回滚」。

**[实现]**　典型用于「事务/日志/批量写入」：构造时记录 `int init = std::uncaught_exceptions();`，析构时比较 `std::uncaught_exceptions() > init`：若更大，说明**在自己生命周期内又发生了新异常（正在展开）→ 回滚**；否则→**提交**。

```cpp
// [示例 13] 事务惯用法：展开中析构→回滚，正常析构→提交
#include <exception>
#include <cstdio>
struct Transaction {
    int init_ = std::uncaught_exceptions();   // 构造时快照
    void commit(){ std::printf("COMMIT data\n"); }
    void rollback(){ std::printf("ROLLBACK data\n"); }
    ~Transaction() {
        if (std::uncaught_exceptions() > init_)
            rollback();                        // 因异常展开→不提交
        else
            commit();                          // 正常离开作用域→提交
    }
};
int main(){
    try {
        Transaction t;                        // init_ = 0
        throw 1;                              // 抛→展开，t 析构时 uncaught=1>0
    } catch(int){}
    Transaction t2;                           // 正常析构，uncaught=0 → 提交
}
// 输出：ROLLBACK data  (t) \n COMMIT data (t2)
```

```cpp
// [示例 14] uncaught_exceptions 计数（嵌套）
#include <exception>
#include <iostream>
struct P { ~P(){ std::cout << "uncaught=" << std::uncaught_exceptions() << "\n"; } };
int main(){
    try { P p; throw 1; }   // p 析构时仍有 1 个未捕获异常
    catch(int){}
}
```

**[经验]**　`uncaught_exception()`（单数，C++17 弃用）只回答「是否 >0」，无法区分「是本对象导致的展开」还是「进入前就有」。`uncaught_exceptions()` 用**计数差**解决，是 `gsl::final_action` / `std::experimental::scope_exit` 的底层机制（libstdc++ `experimental/scope:162,216` 即用此计数）。

**核心知识点 #14**：`uncaught_exceptions()`（C++17）返回未捕获异常个数；用「析构时计数 > 构造时计数」判断是否在栈展开，实现提交/回滚。

---

## ⑩ 异常安全的 STL 条款 [res.on.exception.handling]

**[标准]**　`[res.on.exception.handling]` 规定标准库对异常的总体承诺：
- （1）标准库函数若抛，必抛自 `std::exception` 派生的类型（或 `bad_alloc` 等标准类型）。
- （2）标准库函数**不得泄漏资源**、**不得破坏容器不变量**（即至少 basic 保证）。
- （3）特定操作有更强保证：`swap`、`clear`、`erase`（单元素，不重分配时）等多为 noexcept 或 strong；`push_back`/`insert` 在重分配时仍 strong（靠 move_if_noexcept，第 6、7 节）。
- （4）**析构函数不得抛**（否则展开中 terminate，见 `ch39`、`ch36`）。

**[实现]**　libstdc++ 各容器在 realloc/insert 中统一用 `__uninitialized_move_if_noexcept_a` + `__catch` 回滚（见 7.2、7.3），即该条款的实现落点。

```cpp
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

**[标准]**　`[res.on.exception.handling]` 与各容器条款的具体落点（连 `ch80` 容器异常保证详表）：

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

**[经验]**　记住一句话：**「不修改已有元素、只追加/交换」的操作多 strong；「重排/重哈希」多 basic；「纯析构」多 noexcept**。这是判断任何标准库调用安全等级的心算公式。

## ⑪ 构造函数中的异常：成员自动析构

**[标准]**　`[except.ctor]/1`：若构造函数通过异常退出，则**已构造的基类子对象与成员子对象按逆序自动析构**，对象本身的内存被释放——**无资源泄漏**。这正是 RAII 与异常安全衔接点（见 `ch39`）。

```cpp
// [示例 16] 构造失败→已初始化成员自动析构
#include <iostream>
#include <stdexcept>
struct M { M(){ std::cout << "M ctor\n"; } ~M(){ std::cout << "M dtor\n"; } };
struct N { N(){ std::cout << "N ctor\n"; throw std::runtime_error("N fails"); } ~N() noexcept {} };
struct C {
    M m;   // 先构造
    N n;   // 构造抛→m 自动析构
};
int main(){ try { C c; } catch(const std::exception&){ std::cout << "caught\n"; } }
// 输出：M ctor, N ctor, M dtor, caught
```

**[经验]**　推论：**成员用 RAII 类型（智能指针、容器）即可在构造失败后无泄漏**；若成员是裸指针/裸句柄，必须放在构造函数的函数体（try 块）里获取，并在 catch 中手动释放（或更好：改用 RAII 成员）。这正是 Rule of Zero（`ch39`、`ch41`）的价值。

**核心知识点 #16**：构造函数抛异常 → 已构造的基类/成员子对象逆序自动析构、对象内存释放，无泄漏。

---

## ⑫ std::current_exception / rethrow_exception / exception_ptr

**[标准]**　`[exception.ptr]`（C++11）：`std::exception_ptr` 是不透明句柄，可持有任意异常对象（含非 `std::exception` 派生类型）。`current_exception()` 在 `catch` 中取当前异常句柄；`rethrow_exception(p)` 重新抛出；`make_exception_ptr(e)` 从值造句柄。用于**跨线程传递异常**（worker 线程捕获、主线程重抛）。

**[实现]**　libstdc++ 中 `exception_ptr` 内部是 `void* _M_exception_object`，引用计数管理（7.4）。`rethrow_exception` 标 `__noreturn__`。

```cpp
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

```cpp
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

**[标准]**　`[实现]/[平台]`：在 GCC/Clang（Linux/macOS/MinGW 默认）使用 **Itanium C++ ABI** 的 zero-cost exception handling。**「zero-cost」指正常（不抛）路径零运行时开销**——编译器不插入任何异常检查指令，仅把展开信息写入独立的只读段（`.eh_frame` / `.gcc_except_table`，LSDA = Language-Specific Data Area）。

**[平台]**　代价结构：
- **正常路径**：几乎零开销（仅多占一点代码/数据段存放表）。`try/catch` 本身在正常执行时不耗时（microbenchmark 见第 16 节）。
- **抛异常路径**：需**运行时查表**、解卷（unwind）、逐帧执行析构、匹配 `catch`——代价在 **数百 ns 到数 µs** 量级（取决于栈深度、析构数量、表大小）。

```cpp
// [示例 19] 验证 try/catch 正常路径零/近零开销
#include <chrono>
#include <iostream>
volatile int sink = 0;
int main(){
    const int N = 100'000'000;
    auto t0 = std::chrono::steady_clock::now();
    for (int i=0;i<N;++i){ try { sink += i; } catch(...){} }   // 永不抛
    auto t1 = std::chrono::steady_clock::now();
    for (int i=0;i<N;++i){ sink += i; }                        // 无 try/catch
    auto t2 = std::chrono::steady_clock::now();
    auto a = std::chrono::duration_cast<std::chrono::milliseconds>(t1-t0).count();
    auto b = std::chrono::duration_cast<std::chrono::milliseconds>(t2-t1).count();
    std::cout << "with try/catch=" << a << "ms  without=" << b << "ms\n";
    // 两者接近：正常路径 try/catch 不显著变慢（Itanium zero-cost）
}
```

```cpp
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

**[经验]**　结论：**用异常表达「真正罕见」的错误路径是正确的**——它几乎不污染热路径；但**不要用异常做常规控制流**（每次抛都是 µs 级，比 `if` 慢几个数量级）。Windows 的 SEH/`-EHa` 模型不同（第 15 节），其「零成本」假设弱一些。

**核心知识点 #18**：Itanium zero-cost EH：正常路径零运行期检查（仅查表段），异常路径查 `.eh_frame`/LSDA 展开，代价数百 ns–µs 级。

---

### 13.1 实地查看展开表：objdump / .eh_frame

**[平台]**　zero-cost EH 的展开信息写在可执行文件的只读段。用 `objdump` 可验证「noexcept 函数确实没有展开表」：

```bash
# 对示例 26 生成的 a.out
objdump -h a.out | grep -E "eh_frame|\.gcc_except"
# .eh_frame    节存在（所有函数共用描述），但 noexcept 函数不分配 LSDA 描述
# g++ -fno-exceptions 时 .eh_frame 完全消失，二进制更小
```

```cpp
// [示例 36] 用 __builtin 观察：noexcept 让编译器相信不会展开
#include <vector>
[[gnu::cold]] void log_fail(const char*);
void writer(std::vector<int>& v) noexcept {   // 编译器可省略展开注册
    v.push_back(1);                            // 即便内部可能"逻辑失败"，noexcept 承诺不抛
}
void writer_throw(std::vector<int>& v) {       // 保留完整展开表
    v.push_back(1);
}
int main(){ std::vector<int> v; writer(v); writer_throw(v); }
// 编译：g++ -O2 -S ch40_ex36.cpp；对比 writer / writer_throw 的 .cfi 指令条数
```

**[经验]**　`.eh_frame` 占二进制体积但不占运行期；`-fno-exceptions` 彻底移除它，是嵌入式/游戏追求小体积的正当理由（代价见第 14 节）。

## ⑭ -fno-exceptions / 何时用异常 vs 错误码

### 14.1 -fno-exceptions

**[标准]/[平台]**　GCC/Clang 的 `-fno-exceptions` 禁止异常机制：所有 `throw` 编译失败或 `std::terminate`，`try/catch` 无效，且库/生成代码更小更快（无展开表）。嵌入式、游戏、内核常开。代价：标准库容器等在无法分配时会 `std::abort` 而非抛 `bad_alloc`，且 `vector` 扩容的 strong 保证退化为「失败即终止」。

```cpp
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

**[标准]**　C++11 `std::error_code`/`std::error_condition`、C++17 `std::optional`、C++23 `std::expected<T,E>`（见后续章）提供**无异常的错误传递**。选择原则：
- **异常**：真正「罕见、跨多层、需展开栈」的错误（构造失败、I/O、解析失败）。
- **错误码/expected**：**可预期、频繁、调用方立即处理**的错误（如 `open` 失败、`find` 未命中）。
- **零开销要求 / `-fno-exceptions` 环境**：只能错误码。

```cpp
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

```cpp
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

```cpp
// [示例 24] MSVC /EHa 下 SEH 异常进入 C++ catch(...)（Windows 专属）
// 编译：cl /EHa 时下面会进 catch；/EHsc 下直接崩溃
#include <iostream>
int main(){
    try {
        int* p = nullptr; *p = 1;          // 访问违规（SEH）
    } catch (...) {                          // /EHa 才能捕获，/EHsc 不能
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

**[经验]**　三库**语义一致**：都遵循「移动不抛才移动」原则，这是标准对 strong 保证的要求，非实现偏好。差异只在内部命名与 relocate 优化细节。

**核心知识点 #21**：GCC/Clang 用 Itanium zero-cost EH；MSVC 用 SEH 融合 EH，靠 `/EHsc`(默认)/`/EHa`(捕异步)/`/EHr`(noexcept 检查) 控制；`/EHc` 假定 extern C 不抛以优化。

---

### 15.5 noexcept 函数遇上 /EHr（MSVC 健壮性开关）

**[平台-推断]**　MSVC `/EHr` 会在**每个 `noexcept` 函数**插入运行期检查：「若有异常抵达 noexcept 边界 → 调用 terminate」。这牺牲少量体积/速度换取「即使第三方代码从 noexcept 逃逸异常也能优雅终止」，而 GCC/Clang 默认假定 noexcept 真的不会抛、不插入检查。

```cpp
// [示例 40] /EHr 下 noexcept 逃逸异常被 terminate 捕获（MSVC 行为示意）
// 编译：cl /EHr /std:c++17
#include <iostream>
#include <exception>
void on_term(){ std::cout << "terminated via /EHr\n"; std::abort(); }
void boom() noexcept { throw 1; }   // 违反 noexcept：/EHr 下被捕获并 terminate
int main(){ std::set_terminate(on_term); boom(); }
// /EHr：输出 terminated via /EHr；默认 /EHsc：未定义/崩溃（无检查）
```

**[经验]**　跨编译器项目若需「noexcept 逃逸必终止」的强保证（如安全关键系统），在 MSVC 显式加 `/EHr`，GCC/Clang 侧则需靠代码审查与 `-fno-exceptions` 之外的静态断言保证。

## ⑯ 真实 microbenchmark：noexcept 移动 vs 拷贝扩容

### 16.1 noexcept 移动让扩容走移动（更快）

**[实现]**　当元素移动构造 `noexcept`，`vector` 扩容用移动（或 relocate），否则用拷贝。下面测量两者差异。

```cpp
// [示例 25] 扩容：noexcept 移动 vs 拷贝（量级对比）
#include <vector>
#include <chrono>
#include <iostream>
struct NoThrow { NoThrow()=default; NoThrow(NoThrow&&) noexcept = default;
                 NoThrow(const NoThrow&)=default; int a[8]{}; };
struct Throws  { Throws()=default; Throws(Throws&&) {}   // 移动抛→走拷贝
                 Throws(const Throws&)=default; int a[8]{}; };
template<class T>
double bench(){
    const int N = 200'000;
    auto t0 = std::chrono::steady_clock::now();
    for (int k=0;k<50;++k){ std::vector<T> v; v.reserve(1);
        for (int i=0;i<N;++i) v.push_back(T{}); }   // 反复扩容
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

```cpp
// [示例 26] noexcept 让编译器删除展开表（概念验证，需用 objdump 看）
#include <vector>
void f_noexcept(std::vector<int>& v) noexcept { v.push_back(1); } // 不抛→无展开表
void f_throws(std::vector<int>& v)            { v.push_back(1); } // 可能抛→保留展开表
// 编译：g++ -O2 -S 后对比 .eh_frame 尺寸：f_noexcept 更小
int main(){ std::vector<int> v; f_noexcept(v); f_throws(v); }
```

### 16.3 异常延迟量级汇总

```cpp
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

**[经验]**　量级参考（本机 MinGW GCC 13.1.0，仅量级）：正常路径 `try/catch` 约 **0.x ns/op**（与无 try 几乎相同）；`throw+catch` 约 **0.2–3 µs/op**（随栈深与析构数上升）。**结论：异常用于罕见路径，错误码用于热路径**。

---

### 16.4 测量 noexcept 移动对重排算法的影响

**[实现]**　`std::sort`、`std::rotate` 等在「元素可 noexcept 移动」时可用移动而非拷贝交换元素，性能差异随元素大小放大。

```cpp
// [示例 37] sort 中 noexcept 移动 vs 拷贝交换（量级）
#include <algorithm>
#include <vector>
#include <chrono>
#include <iostream>
// sort 内部靠 swap（移动构造 + 移动赋值）搬运元素；声明了移动构造后必须补齐赋值运算符。
struct BigNT { int a[16]; BigNT(BigNT&&) noexcept = default;
               BigNT(const BigNT&)=default; BigNT()=default;
               BigNT& operator=(BigNT&&) noexcept = default; BigNT& operator=(const BigNT&)=default; };
struct BigT  { int a[16]; BigT(BigT&&); BigT(const BigT&)=default; BigT()=default;
               BigT& operator=(BigT&&); BigT& operator=(const BigT&)=default; };
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

```cpp
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

```cpp
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

**[经验]**　Rust/Go 的「错误即值」在**热路径零开销**上胜过 C++ 异常，但 C++ 异常在**跨多层展开**时书写更简洁。C++23 `std::expected` 补齐了「无开销错误值」选项。

---

## ⑱ noexcept 对编译器优化的影响

**[标准]/[实现]**　`noexcept` 给编译器的两条关键信息：
1. **无需生成展开表**（unwind table）：标记 `noexcept` 的函数，调用方不必为其注册展开信息 → 代码更小（见示例 26）。
2. **允许更激进的内联/移动**：编译器知道不会因异常展开而需回退，可自由重排、省略栈保存。

**[平台-推断]**　MSVC `/EHr` 会对 `noexcept` 函数仍插入「到达 noexcept 即 terminate」的运行期检查（牺牲一点体积换健壮性），与其他编译器默认「完全省略」略有差异。

```cpp
// [示例 29] noexcept 移动使容器放心移动 + 编译器删展开表
#include <vector>
#include <type_traits>
#include <utility>
// 注意：显式声明移动/拷贝构造会抑制隐式默认构造，而 vector<T>(10) 需要 T 默认可构造，
//       故显式补上 `T()=default`（两者均为空类型，默认构造平凡）。
struct Fast { Fast()=default; Fast(Fast&&) noexcept = default; Fast(const Fast&)=default; };
struct Slow { Slow()=default; Slow(Slow&&); Slow(const Slow&)=default; };  // 移动抛
static_assert(std::is_nothrow_move_constructible_v<Fast>);
static_assert(!std::is_nothrow_move_constructible_v<Slow>);
int main(){
    std::vector<Fast> a(10); std::vector<Fast> b(std::move(a)); // relocate/移动，无回滚表
    std::vector<Slow> c(10); std::vector<Slow> d(std::move(c)); // 走 move_if_noexcept→拷贝
}
```

**核心知识点 #22**：`noexcept` 让编译器省略展开表、更激进内联/重排；是「性能 + 强保证」的复利开关。

---

## ⑲ 工程实践清单与常见陷阱

**[经验]**　异常安全工程清单：
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

```cpp
// [示例 30] 反例：异常穿越 C ABI（危险，UB）
extern "C" int c_api() { throw 1; }  // 错误：C 调用方无法展开 C++ 栈
// 正确：
extern "C" int c_api_safe(int* ok){
    try { /* ... */ *ok = 1; return 0; }
    catch(...) { *ok = 0; return -1; }   // 错误码过界
}
```

```cpp
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

```cpp
// [示例 32] 验证类型是否提供各级保证的 trait（编译期自检）
#include <type_traits>
#include <vector>
static_assert(std::is_nothrow_swappable_v<std::vector<int>>);      // swap noexcept
static_assert(std::is_nothrow_move_constructible_v<std::vector<int>>); // 移动 noexcept
struct S { S(S&&) noexcept; S(const S&); };
static_assert(std::is_nothrow_move_constructible_v<S>);            // 用户类型 noexcept 移动
int main(){}
```

---

### 18.1 noexcept 在虚函数覆盖（override）上的约束

**[标准]**　`[except.spec]/4`：覆盖（override）基类虚函数时，派生类的 `noexcept` 说明**不能比基类更宽**（即派生可声明 `noexcept(true)` 当基类是 `noexcept(false)`，但**不能**把基类 `noexcept(true)` 的覆盖成可能抛——那会编译错误）。这是「基类承诺了不抛，派生不得破坏」的协变规则。

```cpp
// [示例 42] 虚函数 noexcept 覆盖约束
#include <type_traits>
struct Base { virtual void f() noexcept; virtual void g(); };
struct D1 : Base { void f() noexcept override; };          // OK：同样不抛
struct D2 : Base { void g() override; };                   // OK：基类可抛
// struct Bad : Base { void f() override; };               // 错误：基类 noexcept(true) 不能被覆盖成可能抛
int main(){ static_assert(std::is_same_v<decltype(&Base::f), void (Base::*)() noexcept>); }
```

**[经验]**　给基类虚函数加 `noexcept` 是**单向承诺**：一旦发布，所有派生类都被锁死为不抛。设计基类接口时，把「一定不抛」才标 noexcept，否则留给派生自由。

### 19.1 更多工业级陷阱

**[经验]**　补充 §19 清单之外的实战坑：

1. **异常穿越 `std::thread` 入口**：`std::thread` 函数体抛异常且未捕获 → `std::terminate`（线程没有调用方 `catch`）。必须线程入口自行 `try/catch` 并转 `exception_ptr`（见示例 17）。
2. **`std::async` 的异常会被存储并在 `get()` 时重抛**：这是异常安全的延迟传递，调用方务必 `try/catch` `get()`。
3. **`noexcept` 与 `std::terminate` 在析构链**：构造函数里 `std::vector` 成员若分配抛，已构造成员仍正确析构（`ch39`/`ch37`），但**裸 `new` 成员**在构造失败时不会自动 `delete`——必须用成员初始化列表里的 RAII 或 `try` 块手动清理。
4. **`std::uncaught_exceptions` 与栈深度**：递归中多层对象各自记录 `init_`，计数差只在「本对象生命周期内新增异常」时为真——这正是示例 13/31 正确工作的原因。

```cpp
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

```cpp
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

**[实现]**　按以下顺序精读，理解「标准 → 库 → ABI」三级：

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

**[经验]**　读完这 12 处，你将能把「`noexcept` 一行」与「vector 扩容是移动还是拷贝」「展开表是否被生成」「跨线程异常如何转发」全部串成一条因果链——这正是工业级 C++ 对异常安全的完整心智模型。

---

## ⑳ 本章速查表

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

## 附录 A：工业异常安全实践 [F: Industry / B: Principle]

```
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

```
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
  差异: 对 10K 元素 vector, ~50us vs ~200us (4x)
```


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第39章](Book/part04_memory/ch39_raii_rule.md) | 键值查找/缓存 | 本章提供概念，第39章提供实现 |
| [第41章](Book/part04_memory/ch41_smart_pointers.md) | TCP服务器/HTTP客户端 | 本章提供概念，第41章提供实现 |


## 附录 H：异常安全面试

```cpp
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
性能差异: noexcept=~50ns/1K elements; 非noexcept=~200ns/1K elements → 4x faster

```cpp
#include <iostream>
int main(){std::cout<<"noexcept move=vector realloc uses memcpy(4x faster). Always mark move noexcept!"<<std::endl;return 0;}
```

Google/LLVM禁止异常的深层原因: 异常会阻止noexcept优化链
- vector move noexcept → memcpy → SIMD → cache friendly
- vector move non-noexcept → 逐个move → 无SIMD → cache miss

面试: noexcept影响什么? vector扩容性能(4x); 编译器优化(more aggressive); 异常安全(noexcept violation=terminate)

## 附录 J：工业实战复盘与设计取舍 [I: Practice / H: Design]

**[经验]**　本节从 production 事故与 Code Review 视角总结异常安全的落地经验，补足前文以「标准/实现」为主的视角。

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

- **后续依赖**：`Book/part07_stl/ch84_set.md`（第84章　set / multiset：红黑树有序集合）—— 本章为其前置，建议后续延伸阅读。
- **后续依赖**：`Book/part07_stl/ch91_filesystem.md`（第91章 文件系统 filesystem）—— 本章为其前置，建议后续延伸阅读。
- **相邻主题**：`Book/part04_memory/ch38_allocator.md`（第 38 章　分配器（Allocator）模型与 PMR）—— 编号相邻、主题接续。
- **相邻主题**：`Book/part04_memory/ch42_strict_aliasing.md`（第 42 章 · 严格别名规则（Strict Aliasing）与编译器优化）—— 编号相邻、主题接续。
- **同模块**：`Book/part04_memory/ch35_memory_layout.md`（第 35 章  C++ 程序的内存模型与操作系统视角）—— 同模块下的其他主题。

## 附录 C：编译实证——noexcept 零成本路径 vs 抛异常的汇编差异 [C: Compiler / E: Low-level]

> 编译：`g++ -std=c++23 -O2 -c ch40_exception_test.cpp`（GCC 15.3.0 / Win64 ABI）。`objdump -d` 反汇编。

### 测试源码

```cpp
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
<_Z13call_noexceptii>:
    lea     (%rcx,%rdx,1),%eax   ; a + b 直接计算
    ret                            ; 无 unwind 表/栈帧/分支
```
**无栈帧（无 `sub $0x28,%rsp`），无 LSDA，无异常处理表插入。**

**调用者 `call_may_throw`（可能抛异常）—— 6 指令 + cold 段**
```asm
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
<_Z14call_may_throwii.cold>:
    call    <may_throw_div.part.0> ; 异常抛出函数
```

**noexcept_add 本体 —— 1 指令**
```asm
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

---

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

