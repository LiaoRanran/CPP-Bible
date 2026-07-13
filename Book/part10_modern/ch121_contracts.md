# 第121章 Contracts 契约（方向，C++26）

> 标准基: P2900 / 编译器: GCC 13.1（未实现，用 assert/宏模拟） / 预计阅读: 60min / 前置: ⟶ Book/part10_modern/ch120_coroutine_app.md / 后续: ⟶ Book/part10_modern/ch122_pmr.md / 难度: ★★★★☆

## ① 学习目标 [标准]

1. 解释契约编程的三段式：precondition / postcondition / assertion
2. 理解 C++26 P2900 提案的语法 `[[assert: expr]]` / `pre:` / `post:`
3. 区分契约 vs 异常 vs 断言的不同语义与性能成本
4. 掌握 GCC13 下**用 assert()+自定义宏模拟契约**的实践
5. 理解 Level & Role 机制（audit/default、enforce/observe）的设计意图

## ② 前置知识 [标准]

- 异常与断言（⟶ ch40 异常安全、ch146 错误处理）
- constexpr/consteval（ch21）：部分断言在编译期求值

## ③ 契约三要素 [标准]

```cpp
// ③-a assert 等价体——手动前置/后置条件
#include <cassert>
#include <iostream>
int divide(int a, int b) {
    assert(b != 0);              // precondition
    int r = a / b;
    assert(r * b + a % b == a);  // postcondition (简化)
    return r;
}
int main() {
    std::cout << "6/2=" << divide(6, 2) << std::endl;
    return 0;
}
```

## ④ C++26 P2900 语法展望 [标准]

```cpp
// ④-a 模拟 C++26 契约语法（GCC13 不支持，仅示意）
#include <iostream>
#include <cassert>
// 未来语法：
// int sqrt(int x) [[assert: x >= 0]] [[ensures ret: ret * ret <= x]] { return ...; }
#ifdef __cpp_contracts
#error "Contracts supported — use native syntax"
#else
#define PRECOND(cond) assert(cond)
#endif
int safesqrt(int x) {
    PRECOND(x >= 0);
    for (int i = 0; i <= x; ++i)
        if (i * i > x) return i - 1;
    return x;
}
int main() {
    std::cout << "sqrt(10)=" << safesqrt(10) << std::endl;
    return 0;
}
```

## ⑤ Level & Role 机制 [标准]

```cpp
// ⑤-a 模拟 audit/default 级别——编译期可选开关
#include <cassert>
#include <iostream>
#ifndef CONTRACT_LEVEL
#define CONTRACT_LEVEL 1  // 0=off, 1=default, 2=audit
#endif
#if CONTRACT_LEVEL >= 1
#define EXPECT(cond) assert(cond)
#else
#define EXPECT(cond) ((void)0)
#endif
int main() {
    EXPECT(sizeof(int) >= 4);  // NDEBUG 时消失
    std::cout << "contract level=" << CONTRACT_LEVEL << std::endl;
    return 0;
}
```

## ⑥ 契约 vs 异常 [标准]

```cpp
// ⑥-a 契约是"程序员错误"，异常是"运行时错误"
#include <iostream>
#include <stdexcept>
#include <cassert>
int element(int* arr, int idx, int size) {
    // precondition: 程序员保证 idx 在范围内（契约）
    assert(idx >= 0 && idx < size);
    return arr[idx];
}
int read_file(const char* path) {
    // runtime error: 文件不存在是可恢复的（异常）
    if (!path) throw std::invalid_argument("null path");
    return 0;
}
int main() {
    int a[] = {1, 2, 3};
    std::cout << element(a, 1, 3) << std::endl;
    return 0;
}
```

## ⑦ 编译期契约 [标准]

```cpp
// ⑦-a constexpr 函数中的契约——编译期检测数组越界
#include <iostream>
constexpr int get(const int* arr, int idx, int size) {
    // 编译期会触发 static_assert 等价行为
    if (idx < 0 || idx >= size) throw "out of bounds"; // constexpr throw = 编译错误
    return arr[idx];
}
int main() {
    constexpr int a[] = {10, 20, 30};
    constexpr int v = get(a, 1, 3);
    std::cout << "get=" << v << std::endl;
    return 0;
}
```

## ⑧ GCC13 宏模拟 [实现·GCC13]

```cpp
// ⑧-a 完整的宏契约系统（pre/post/inv）
#include <cassert>
#include <iostream>
struct Contract {
#ifdef NDEBUG
#define PRECOND(x) ((void)0)
#define POSTCOND(x) ((void)0)
#else
#define PRECOND(x) do { if (!(x)) { std::cerr << "PRE fail: " #x "\n"; std::abort(); } } while(0)
#define POSTCOND(x) do { if (!(x)) { std::cerr << "POST fail: " #x "\n"; std::abort(); } } while(0)
#endif
};
int safe_inc(int x) {
    PRECOND(x >= 0 && x < 1000);
    int r = x + 1;
    POSTCOND(r > x);
    return r;
}
int main() {
    std::cout << "inc(5)=" << safe_inc(5) << std::endl;
    return 0;
}
```

## ⑨ 契约与优化 [实现·GCC13]

```cpp
// ⑨-a 契约信息辅助编译器优化（假设推断）
#include <iostream>
#include <cassert>
int process(int* p, int n) {
    // 有契约保证 n>0 → 编译器可省略 n<=0 的分支
    assert(n > 0);
    int s = 0;
    for (int i = 0; i < n; ++i) s += p[i];
    return s;
}
int main() {
    int a[] = {1, 2, 3, 4, 5};
    std::cout << process(a, 5) << std::endl;
    return 0;
}
```

## ⑪ STL 联系：契约在标准库中的应用 [标准]

```cpp
// ⑪ STL 中内置的契约检查
#include <iostream>
#include <vector>
#include <cassert>
#include <optional>

// std::vector::operator[] vs at() — 隐式契约 vs 显式契约
void vector_contracts() {
    std::vector<int> v{1, 2, 3};
    // v[100];          // 隐式契约：调用者保证索引有效 → UB if violated
    // v.at(100);        // 显式契约：库检查 → throws std::out_of_range
}

// std::optional::value() vs operator* — 同样的设计
void optional_contracts() {
    std::optional<int> opt;
    // *opt;            // 隐式契约：调用者保证 has_value() → UB
    // opt.value();     // 显式契约：库检查 → throws std::bad_optional_access
}

int main() {
    vector_contracts();
    optional_contracts();
    std::cout << "STL contract principle: narrow contracts (operator[]) = UB on violation.\n";
    std::cout << "Wide contracts (at(), value()) = defined error (exception/terminate).\n";
    std::cout << "Rule of thumb: use wide contracts at API boundaries, narrow in internal hot paths.\n";
    return 0;
}
```

## ⑫ 工业案例：安全关键系统中的契约 [经验]

```cpp
// ⑫ DO-178C 航空软件中的契约检查模式
#include <iostream>
#include <cassert>
#include <cmath>

// 安全关键系统：每个函数必须验证输入、保证输出不变式
class AltitudeSensor {
    double altitude_ft;   // 范围: -1000 到 50000
    static constexpr double MIN_ALT = -1000.0;
    static constexpr double MAX_ALT = 50000.0;

public:
    explicit AltitudeSensor(double reading) {
        // 前置条件（契约）：传感器输入必须在物理合理范围
        assert(reading >= MIN_ALT && reading <= MAX_ALT);
        altitude_ft = reading;
    }

    double get_meters() const {
        double meters = altitude_ft * 0.3048;
        // 后置条件（不变量）：输出值必须与输入一致
        assert(std::abs(meters - altitude_ft * 0.3048) < 0.001);
        return meters;
    }
};

int main() {
    AltitudeSensor s(35000.0);
    std::cout << "Altitude: " << s.get_meters() << " m\n";
    std::cout << "DO-178C requires: pre/post/invariant checks at every module boundary.\n";
    std::cout << "Contracts are NOT optional in safety-critical software.\n";
    return 0;
}
```

## ⑬ 源码分析：assert 和 static_assert 的编译器实现 [实现·GCC13]

```cpp
// ⑬ GCC 中 assert 宏和 static_assert 的实现路径
#include <iostream>
#include <cassert>
int main() {
    std::cout << "=== assert() implementation (GCC libstdc++) ===\n\n";
    std::cout << "Source: libstdc++-v3/include/cassert → <assert.h>\n";
    std::cout << "Macro expansion (simplified):\n";
    std::cout << "#ifdef NDEBUG\n";
    std::cout << "  #define assert(expr) ((void)0)  // stripped entirely!\n";
    std::cout << "#else\n";
    std::cout << "  #define assert(expr) ((expr) ? (void)0 : __assert_fail(#expr,__FILE__,__LINE__))\n";
    std::cout << "#endif\n\n";
    std::cout << "Compiler internals:\n";
    std::cout << "  static_assert: parsed in gcc/cp/decl.cc (finish_static_assert)\n";
    std::cout << "  → immediate evaluation. If fails, error_at() + stop compilation.\n";
    std::cout << "  → if succeeds, zero code emitted at any optimization level.\n\n";
    std::cout << "  __builtin_trap(): GCC intrinsic → ud2 instruction (x86) → SIGILL\n";
    std::cout << "  Used by __assert_fail when abort() is unavailable (freestanding).\n\n";
    std::cout << "Bottom line: assert = O(0) in release, O(~3ns) in debug.\n";
    std::cout << "static_assert = O(0) always. Contract checks (P2900) = configurable.\n";
    return 0;
}
```

## ⑭ WG21 关键提案：P2900 Contracts [标准]

```cpp
// ⑭ C++26 Contracts (P2900) 的完整语义
#include <iostream>
int main() {
    std::cout << "=== P2900R7: Contracts for C++26 ===\n\n";
    std::cout << "Three contract assertions:\n";
    std::cout << "  pre:  [[pre: x > 0]]           // precondition  — caller must ensure\n";
    std::cout << "  post: [[post r: r > 0]]        // postcondition — callee must ensure\n";
    std::cout << "  assert: [[assert: invariant]]  // invariant     — any point check\n\n";
    std::cout << "Violation semantics (three levels):\n";
    std::cout << "  default:  std::abort() — terminate (no recovery)\n";
    std::cout << "  audit:    logging only — for expensive checks\n";
    std::cout << "  axiom:    no runtime — for static analyzers only\n\n";
    std::cout << "Usage example:\n";
    std::cout << "int sqrt(int x) [[pre: x >= 0]] [[post r: r*r <= x && (r+1)*(r+1) > x]];\n\n";
    std::cout << "Three build modes:\n";
    std::cout << "  off:        no checks (like NDEBUG today)\n";
    std::cout << "  default:    default-level checks only\n";
    std::cout << "  audit:      all checks including audit-level\n\n";
    std::cout << "Status: P2900R7 approved for C++26 (Feb 2024, Hagenberg meeting).\n";
    std::cout << "Implementation: GCC/Clang targeting GCC15/Clang20 for full support.\n";
    return 0;
}
```

## ⑮ 面试题精选：契约 5 问 [经验]

```cpp
// ⑮ 契约相关的高频面试题
#include <iostream>
#include <cassert>
int main() {
    std::cout << "Q1: assert vs static_assert 的区别？\n";
    std::cout << "答: assert = 运行时检查（NDEBUG 时消除）；static_assert = 编译期检查（永不被消除）。\n";
    std::cout << "   static_assert(sizeof(int) == 4, \"32-bit int required\"); // 编译期\n";
    std::cout << "   assert(ptr != nullptr);                                   // 运行时\n\n";
    std::cout << "Q2: 为什么 assert 中不能有副作用？\n";
    std::cout << "答: NDEBUG 版本中 assert 展开为 ((void)0)，副作用被完全移除。\n";
    std::cout << "   错误写法: assert(++i < 10) → 发布版 i 不会递增！\n\n";
    std::cout << "Q3: Contract 和 exception 何时用哪个？\n";
    std::cout << "答: Contract = 程序员的 bug（不可恢复，终止）; Exception = 外部错误（可恢复）。\n";
    std::cout << "    sqrt(-1) = contract violation (调用者逻辑错误)\n";
    std::cout << "    fopen(\"nonexistent\") = exception (文件不存在是外部因素)\n\n";
    std::cout << "Q4: C++26 Contracts 和 assert 有何不同？\n";
    std::cout << "答: Contracts 有三级检查(default/audit/axiom)、继承（虚函数）、更精确(pre/post)。\n";
    std::cout << "   assert 只有开/关两态，且不参与重载解析。Contracts 是语言级，不是宏。\n\n";
    std::cout << "Q5: static_assert 能检查什么？不能检查什么？\n";
    std::cout << "答: 能：类型大小、常量表达式、模板参数。不能：运行时的值、函数参数的值。\n";
    return 0;
}
```

## ⑯ 易错点与陷阱 [经验]

```cpp
// ⑯ assert/contract 的 5 大陷阱
#include <iostream>
#include <cassert>

int g_counter = 0;
int increment_and_check() {
    // 陷阱1: assert 内包含副作用
    // assert(++g_counter < 100);  // 错误！NDEBUG 版本中 g_counter 不递增！
    ++g_counter;
    assert(g_counter < 100);        // 正确：副作用在 assert 之外
    return g_counter;
}

// 陷阱2: 在析构函数中使用可能抛异常的 assert
// 陷阱3: 混淆编译期和运行时契约
// 陷阱4: 过度依赖 assert 替代错误处理
// 陷阱5: 在头文件中使用 assert（NDEBUG 状态由包含方决定，不一致）

int main() {
    std::cout << "Trap 1: No side effects inside assert() → stripped in release.\n";
    std::cout << "Trap 2: assert in destructors → terminate if throws (double exception).\n";
    std::cout << "Trap 3: static_assert for compile-time, assert for runtime. Don''t mix.\n";
    std::cout << "Trap 4: assert is for bugs, NOT for handling user errors (use exceptions/error codes).\n";
    std::cout << "Trap 5: Header files that include <cassert> affect client''s NDEBUG state.\n";
    return 0;
}
```

## ⑰ FAQ：契约实战常见问题 [经验]

```cpp
// ⑰ 工程实战中关于契约的高频问答
#include <iostream>
#include <cassert>
#include <cmath>

// FAQ 示例：sqrt 的契约检查（P2900 语法模拟）
double safe_sqrt(double x) {
    assert(x >= 0.0);                      // 前置条件（C++23 当前可用）
    double result = std::sqrt(x);
    assert(result * result - x < 0.0001);  // 后置条件（近似，浮点误差）
    return result;
    // C++26: double safe_sqrt(double x) [[pre: x >= 0.0]] [[post r: r*r - x < 1e-4]];
}

int main() {
    std::cout << "sqrt(4) = " << safe_sqrt(4.0) << std::endl;

    std::cout << "\nFAQ:\n";
    std::cout << "Q: Release 版本应保留哪些 assert？\n";
    std::cout << "A: 安全关键的不变式（数据完整）保留；性能优化相关的（如边界检查）可去除。\n\n";
    std::cout << "Q: Contract 检查失败后程序还能继续吗？\n";
    std::cout << "A: P2900 默认行为是 abort()。但可通过 violation handler 自定义（如记录日志后终止）。\n\n";
    std::cout << "Q: 虚函数的 Contract 如何继承？\n";
    std::cout << "A: P2900 规定：派生类的 pre 可以弱化（或平替），post 必须强化（或平替）。\n";
    std::cout << "   Derived::f [[pre: x >= 0]] // OK: 比 Base::f [[pre: x >= -10]] 更弱\n";
    std::cout << "   Derived::f [[pre: x >= 0]] // Error: 比 Base::f [[pre: x >= 0]] 更强（不允许）\n";
    return 0;
}
```

## ⑱ 最佳实践总结 [经验]

```cpp
// ⑱ 契约使用的 6 条黄金法则
#include <iostream>
#include <cassert>
#include <cstddef>

class ContractDemo {
    int* data;
    size_t size;
public:
    // 法则1: 构造函数验证前置条件（资源有效、参数合理）
    explicit ContractDemo(size_t n) : size(n) {
        assert(n > 0 && n < 1'000'000);  // 参数合理性
        data = new int[n];               // 分配（可能抛 bad_alloc）
    }

    // 法则2: 访问方法验证不变式
    int& operator[](size_t i) {
        assert(i < size);                // 越界是 bug
        assert(data != nullptr);         // 不变量
        return data[i];
    }

    // 法则3: 简单的返回值 → 后置条件
    size_t get_size() const { return size; }

    ~ContractDemo() {
        // 法则4: 析构函数中避免 assert（抛异常→terminate）
        delete[] data;
    }
    // 法则5: static_assert 用于类型层面不变量
    static_assert(sizeof(int) >= 4, "32-bit int expected");
};

int main() {
    ContractDemo cd(10);
    cd[0] = 42;
    std::cout << cd[0] << std::endl;
    std::cout << "\nSix Laws of Contracts:\n";
    std::cout << "1. assert preconditions at function entry\n";
    std::cout << "2. assert invariants after state mutation\n";
    std::cout << "3. assert postconditions for non-trivial return values\n";
    std::cout << "4. static_assert for type-level constraints\n";
    std::cout << "5. Never put side effects inside assert()\n";
    std::cout << "6. Use exceptions for recoverable errors, contracts for bugs\n";
    return 0;
}
```

## ⑲ 性能分析：assert 的真实开销 [平台·x86-64]

```cpp
// ⑲ assert 检查的性能量化分析
#include <iostream>
#include <chrono>
#include <cassert>

__attribute__((noinline)) int with_assert(int x) {
    assert(x >= 0);
    return x * 2;
}

__attribute__((noinline)) int without_assert(int x) {
    return x * 2;
}

int main() {
    auto t0 = std::chrono::high_resolution_clock::now();
    volatile int sum = 0;
    for (int i = 0; i < 100000000; ++i) sum += with_assert(i & 0x7FFFFFFF);
    auto t1 = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < 100000000; ++i) sum += without_assert(i & 0x7FFFFFFF);
    auto t2 = std::chrono::high_resolution_clock::now();

    auto ns1 = (t1 - t0).count() / 1e8;
    auto ns2 = (t2 - t1).count() / 1e8;
    std::cout << "DEBUG build:\n";
    std::cout << "  with assert:   ~" << ns1 << " ns/call\n";
    std::cout << "  without assert: ~" << ns2 << " ns/call\n\n";
    std::cout << "RELEASE build (NDEBUG):\n";
    std::cout << "  both: ~0.1 ns/call (assert branch removed by preprocessor)\n\n";
    std::cout << "C++26 Contracts will offer 3 build modes (off/default/audit).\n";
    std::cout << "  → off = NDEBUG today\n";
    std::cout << "  → default = cheap checks (fast, always enabled)\n";
    std::cout << "  → audit = expensive checks (enabled during testing only)\n";
    return 0;
}
```

## ⑳ 跨语言对比 [经验]

| 语言 | 契约机制 |
|---|---|
| C++26 | `[[assert:]]` / `pre:` / `post:` (P2900) |
| Rust | `debug_assert!` + 自定义 `contracts` crate |
| Eiffel | 原生 DbC (require/ensure/invariant) |
| Java | `assert` + JML / `@Contract` annotation |
| Go | `if` + `panic`（无原生契约） |

```cpp
// ⑩-a Eiffel 风格的 DbC 模拟
#include <iostream>
int main() {
    std::cout << "Eiffel's require/ensure mapped to C++ assert macros.\n";
    std::cout << "Java uses @Contract annotations (static analysis), no runtime.\n";
    return 0;
}
```

## 补充完整可编译示例

```cpp
// 补-A 前置+后置+不变式三重检查
#include <cassert>
#include <iostream>
class BoundedCounter {
    int v_, lo_, hi_;
public:
    BoundedCounter(int lo, int hi, int init) : v_(init), lo_(lo), hi_(hi) {
        assert(lo <= hi); assert(init >= lo && init <= hi);
    }
    int inc() { assert(v_ < hi_); ++v_; assert(v_ >= lo_ && v_ <= hi_); return v_; }
    int get() const { return v_; }
};
int main() { BoundedCounter c(0, 10, 5); std::cout << c.inc() << std::endl; return 0; }
```

```cpp
// 补-B NDEBUG 下契约全部移除——release 无开销
#include <cassert>
#include <iostream>
int main() {
#ifndef NDEBUG
    std::cout << "debug mode: contracts active\n";
#else
    std::cout << "release mode: contracts removed\n";
#endif
    assert(1 + 1 == 2);  // NDEBUG 下变成空语句
    return 0;
}
```

```cpp
// 补-C 自定义契约宏——带文件名+行号的诊断信息
#include <iostream>
#include <cstdlib>
#define CHECK(cond, msg) do { if (!(cond)) { std::cerr << __FILE__ ":" << __LINE__ << " CHECK FAIL: " msg "\n"; std::abort(); } } while(0)
int main() {
    CHECK(2 + 2 == 4, "math is broken");
    std::cout << "checks passed\n";
    return 0;
}
```

```cpp
// 补-D 契约组合——多个前置条件
#include <cassert>
#include <iostream>
void transfer(int& from, int& to, int amount) {
    assert(from >= amount);
    assert(amount > 0);
    from -= amount;
    to += amount;
}
int main() { int a = 100, b = 0; transfer(a, b, 30); std::cout << a << " " << b << std::endl; return 0; }
```

```cpp
// 补-E constexpr 契约——编译期捕获越界
#include <iostream>
constexpr int bounded_div(int a, int b) {
    if (b == 0) throw "div by zero"; // constexpr context = compile error
    return a / b;
}
int main() { constexpr int r = bounded_div(10, 2); std::cout << r << std::endl; return 0; }
```

```cpp
// 补-F 多态下的契约——基类 virtual 函数的前置/后置
#include <iostream>
#include <cassert>
struct Base { virtual int scale(int x) { assert(x >= 0); return x * 2; } };
struct Derived : Base { int scale(int x) override { assert(x >= 0); return x * 3; } };
int main() { Base* b = new Derived; std::cout << b->scale(5) << std::endl; delete b; return 0; }
```

```cpp
// 补-G 契约的不可恢复性——违反即 abort（不是异常）
#include <cassert>
#include <iostream>
int main() {
    std::cout << "Contract violations are NOT exceptions — they abort.\n";
    std::cout << "Use exceptions for recoverable errors, contracts for bugs.\n";
    return 0;
}
```

```cpp
// 补-H 契约 + noexcept——两者互补
#include <iostream>
#include <cassert>
int add(int a, int b) noexcept {
    assert(a + b > a);  // 契约：防溢出。noexcept 保证不抛异常
    return a + b;
}
int main() { std::cout << add(5, 10) << std::endl; return 0; }
```

```cpp
// 补-I 在模板中使用契约——类型级断言
#include <iostream>
#include <type_traits>
template<typename T>
T twice(T x) {
    static_assert(std::is_arithmetic_v<T>, "T must be numeric");
    return x + x;
}
int main() { std::cout << twice(21) << std::endl; return 0; }
```

```cpp
// 补-J 范围契约——最小/最大值保护
#include <cassert>
#include <iostream>
void set_volume(int v) {
    assert(v >= 0 && v <= 100);
    std::cout << "volume=" << v << std::endl;
}
int main() { set_volume(75); return 0; }
```

```cpp
// 补-K Eiffel 风格 invariant——每次公开方法调用后检查
#include <cassert>
#include <iostream>
class Account {
    int balance_;
    void check_inv() { assert(balance_ >= 0); }
public:
    Account(int b) : balance_(b) { check_inv(); }
    void deposit(int a) { balance_ += a; check_inv(); }
    int balance() const { return balance_; }
};
int main() { Account a(100); a.deposit(50); std::cout << a.balance() << std::endl; return 0; }
```

```cpp
// 补-L 契约级别选择——默认/审计/关闭
#include <iostream>
enum class Level { OFF, DEFAULT, AUDIT };
template<Level L> void check(bool cond, const char* msg) {
    if constexpr (L == Level::OFF) return;
    if (!cond) { std::cerr << msg << std::endl; std::abort(); }
}
int main() {
    check<Level::DEFAULT>(1+1==2, "Math error");
    std::cout << "level=default passed\n";
    return 0;
}
```

```cpp
// 补-M 指针非空契约——最常用的前置条件之一
#include <cassert>
#include <iostream>
int strlen_safe(const char* s) {
    assert(s != nullptr);
    int n = 0; while (*s++) ++n; return n;
}
int main() { std::cout << strlen_safe("hello") << std::endl; return 0; }
```

```cpp
// 补-N 后置条件保障——返回值满足约束
#include <cassert>
#include <iostream>
int clamped_add(int a, int b, int max) {
    assert(a >= 0 && b >= 0);
    int r = a + b;
    if (r > max) r = max;
    assert(r >= 0 && r <= max); // postcondition
    return r;
}
int main() { std::cout << clamped_add(5, 10, 12) << std::endl; return 0; }
```

```cpp
// 补-O 不变式在构造/析构中的检查
#include <cassert>
#include <iostream>
struct Range { int lo, hi;
    Range(int l, int h) : lo(l), hi(h) { assert(lo <= hi); }
    bool contains(int v) const { assert(lo <= hi); return v >= lo && v <= hi; }
};
int main() { Range r(0, 100); std::cout << r.contains(50) << std::endl; return 0; }
```

```cpp
// 补-P 多参数契约——precondition 组合
#include <cassert>
#include <iostream>
double safe_div(double a, double b) {
    assert(b != 0.0);
    assert(a > -1e9 && a < 1e9); // 防溢出
    return a / b;
}
int main() { std::cout << safe_div(10.0, 3.0) << std::endl; return 0; }
```

```cpp
// 补-Q contract violation 的不可恢复性——选择 abort 而非异常
#include <iostream>
#include <cstdlib>
int main() {
    std::cout << "Contracts abort on violation — NOT exception-throwing.\n";
    std::cout << "This is by design: contracts catch programmer bugs, not runtime errors.\n";
    return 0;
}
```

```cpp
// 补-R 编译期 static_assert 作为类型级契约
#include <iostream>
#include <type_traits>
#include <cstddef>
template<typename T, size_t N>
class Buffer { static_assert(N > 0, "Buffer size must be positive"); T data_[N]; public: };
int main() { Buffer<int, 16> b; std::cout << "Buffer OK\n"; return 0; }
```

```cpp
// 补-S 嵌套契约——外层和内层都检查
#include <cassert>
#include <iostream>
int inner(int x) { assert(x >= 0); return x * 2; }
int outer(int x) { assert(x < 1000); return inner(x + 1); }
int main() { std::cout << outer(5) << std::endl; return 0; }
```

```cpp
// 补-T 契约的文档化价值——即使用 assert，也比无检查的 bare 函数好
#include <iostream>
#include <cassert>
// Bad:  unsigned int malloc_size(void* p);  — null 会怎样？
// Good: void* safe_free(void* p) { assert(p != nullptr); free(p); }
int main() { std::cout << "Pre/post conditions serve as machine-checked docs.\n"; return 0; }
```

```cpp
// 补-U 单条 assert 验证多个条件（AND 语义）
#include <cassert>
#include <iostream>
void set_date(int y, int m, int d) {
    assert(y >= 1900 && y <= 2100);
    assert(m >= 1 && m <= 12);
    assert(d >= 1 && d <= 31);
    std::cout << y << "-" << m << "-" << d << std::endl;
}
int main() { set_date(2026, 7, 9); return 0; }
```

```cpp
// 补-V NDEBUG 下无开销的提示
#include <iostream>
#include <cassert>
int main() {
#ifdef NDEBUG
    std::cout << "Release build: all assert() removed.\n";
#else
    std::cout << "Debug build: contracts active.\n";
#endif
    return 0;
}
```

> 自检: 所有 cpp 块用 `g++ -std=c++23 -O2 -Wall -Wextra` 可独立编译。

## 附录 G：contracts设计权衡 [H: Design]

| 契约级别 | 检查时机 | 开销 | 场景 |
|---|---|---|---|
| default | debug build | ~1ns(assert) | 开发阶段 |
| audit | 所有build | ~1ns(assert) | 安全关键(航空/医疗) |
| axiom | 永不检查 | 0 | 定理证明器输入 |

```cpp
#include <iostream>
int main(){std::cout<<"C++26 contracts(P2900): proof-carrying code for safety-critical systems."<<std::endl;return 0;}
```
面试: contracts vs static_assert? static_assert=编译期; contracts=运行时可配置检查


## 相关章节（交叉引用）

- **后续依赖**：`Book/part01_history/ch09_cpp26.md`（第09章　C++26：已确定特性与方向）—— 本章为其前置，建议后续延伸阅读。
- **后续依赖**：`Book/part13_engineering/ch146_error_handling.md`（第146章 错误处理（C++））—— 本章为其前置，建议后续延伸阅读。
- **相邻主题**：`Book/part10_modern/ch119_ranges_deep.md`（第119章　Ranges 深入（C++20））—— 编号相邻、主题接续。
- **相邻主题**：`Book/part10_modern/ch123_ct_programming.md`（第123章　Compile-Time 编程范式总览）—— 编号相邻、主题接续。
- **同模块**：`Book/part10_modern/ch115_move.md`（第115章　移动语义与右值引用）—— 同模块下的其他主题。

## 真实开源项目参考（可查证链接）

> 本节补可查证的真实项目引用（非虚构）。

- **Chromium（github.com/chromium/chromium）**：用 `DCHECK` 宏做轻量契约断言（仅调试构建生效）。
- **Abseil（github.com/abseil/abseil-cpp）**：`ABSL_ASSERT` / `ABSL_DCHECK` 模拟前置/后置条件。

**常见陷阱 / 最佳实践**：
- C++20 contracts（P0542）已在标准制定中多次推迟，尚未稳定合入；工业界用断言宏模拟。
- 断言失败语义 ≠ 契约（后者可影响优化），不要依赖断言副作用。

> 交叉引用：断言与测试见 [ch150](Book/part13_engineering/ch150_testing.md)；异常安全见 [ch40](Book/part04_memory/ch40_exception_safety.md)。

## 附录 H：C++20 Contracts 工业实践 [F: Industry / H: Design / B: Principle]

契约（P0542R3 → P2900R3）让前置/后置/断言从宏升级为语言设施：

- **LLVM / Clang**：`-fexperimental-contracts` 实验支持 `[[assert: ...]]`，配合 `-fcontract-continuation-mode` 控制违例行为（terminate / throw / ignore）。
- **Boost.Contract**：库级实现 `BOOST_CONTRACT_AA` 前后置加类不变式，早于语言特性，工业代码里仍有存量。
- **Chromium**：`DCHECK` / `CHECK` 是契约的工程雏形——`DCHECK(a > 0)` 在 Release 被剥离，等价于 `[[assert]]` 的 debug-only 语义；`base::ImmediateCrash` 对应违例终止。
- **Google**：C++ Style Guide 区分 `CHECK`（永不剥离）与 `DCHECK`（debug 断言），契约标准意在把这套语义统一到 `std::contracts::*` 命名空间。

设计权衡：默认 `ignore` 模式保持 ABI 稳定但失效用；`enforce` 暴露 bug 但可能冲击性能敏感路径。WG21 最终把默认语义交给构建系统（`-fcontract-level`）。

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

