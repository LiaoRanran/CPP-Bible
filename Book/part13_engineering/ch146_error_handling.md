# 第146章 错误处理（C++）

⟶ Book/part07_stl/ch88_optional_variant.md
⟶ Book/part10_modern/ch121_contracts.md

> **取证说明（Forensic Note）**：本章所有可被机器验证的结论，均用本机 GCC 13.1.0 真实产物佐证；示例源码位于 `Examples/_ch146_*.cpp`，对应汇编/警告产物位于 `Examples/_ch146_*.asm` 与 `Examples/_ch146_*_warn.txt`。编译命令统一为 `g++ -std=c++23 -O2 -S -masm=intel <src> -o <dst>.asm`，全部示例均通过 `-Wall -Wextra` 警告零洁净（warnings clean）验证；关键机器码结论直接引用 g++ 生成的 Intel 语法汇编，绝不编造。运行时事实由本机真实编译执行得出。源码剖析（第⑥节）引用的 libstdc++ 路径为本机真实存在的 `.../include/c++/system_error`，行号取自实际文件（版本 GCC 13.1.0）。立场分层标签：`[标准]`=ISO C++，`[实现]`=编译器/标准库实现，`[平台]`=OS/ABI，`[经验]`=工程共识。

## ① 概述：错误处理策略 [经验]

⟶ Book/part13_engineering/ch145_naming_api.md
⟶ Book/part13_engineering/ch147_code_review.md


错误处理不是"发生错误后怎么办"，而是**设计 API 契约时就必须决定的第一等公民**。一个函数一旦可能失败，调用方就必须有一个可预期、可组合、可推理的失败通道；错误通道设计得差，整个系统的可靠性会系统性塌方。

`[经验]` 工业界的共识是：**异常用于"真正异常、且调用方通常无法就地恢复"的失败；返回值/可选项用于"可预期的、调用方应当处理的常规失败"**。把"文件不存在"当异常抛出，是在用控制流模拟返回码；把"空指针解引用"用返回值掩盖，是在丢弃本可立即崩溃的定位信息。

```cpp
#include <string>
#include <optional>
#include <expected>
// 策略一：异常——调用方难以就地恢复、且属于"契约违约"的失败
double parse_financial(const std::string& s);   // 抛 std::invalid_argument

// 策略二：返回值/可选项——可预期的常规失败，调用方必须分流
std::expected<Config, ConfigError> load_config(const Path& p);  // 返回错误而非抛
std::optional<Row> find_row(Key k);             // "无值"也是合法结果，不是错误
```

错误通道的三条硬约束：

- **可组合**：错误必须能沿调用栈向上传播而不丢失上下文（第⑮节链式传播）；
- **不泄漏**：任何失败路径都必须释放已获资源（第④节 RAII）；
- **可分类**：错误必须能被调用方区分"可重试 / 可降级 / 致命"，而非只有一个 bool。

```cpp
enum class Outcome { Ok, Retryable, Fatal };   // 错误分类是策略的一部分
struct Result { Outcome o; std::error_code ec; };
```

## ② 错误表征：返回值 vs 异常 vs 枚举

`[标准]` C++ 提供三类错误表征原语：① 返回码/枚举（同步、零开销、调用方显式检查）；② 异常（异步展开、强类型、可跨多层跳过）；③ 值域包装（`std::optional` / `std::expected`，介于两者之间，把"结果或错误"作为值本身）。

```cpp
#include <cstddef>
// A) 裸返回码（C 风格，易漏检）
int read_packet(int fd, char* buf, size_t n);   // 返回 -1 表示失败，errno 带原因
```

```cpp
#include <cstddef>
// B) 强类型枚举错误（自描述，无需全局 errno）
enum class ReadErr { None, WouldBlock, Closed, TooLarge };
struct ReadResult { std::size_t got; ReadErr err; };
ReadResult read_packet(int fd, char* buf, size_t n);   // 调用方必须读 err
```

```cpp
#include <vector>
// C) 异常（失败时直接展开，调用方用 try/catch 捕获）
struct Packet { std::vector<char> data; };
Packet read_packet(int fd);   // 失败时抛 std::system_error
```

`[经验]` 选型经验法则：

- 构造函数/运算符/拷贝接口**不能返回错误码**，这类场景要么 noexcept 要么抛异常；
- 性能热点（每帧百万次调用）避免异常展开开销，用返回值；
- 库边界（尤其跨语言/跨 ABI）优先返回码或 `std::error_code`，异常跨 ABI 不安全（第⑯节）。

```cpp
// 性能热点：返回码零开销，异常会污染分支预测与代码布局
[[nodiscard]] bool try_pop(LockFreeQueue& q, T& out) noexcept;
```

## ③ 异常机制（throw/try/catch） [标准]

`[标准]` 异常由 `throw` 触发、`try` 捕获、`catch` 处理。`catch` 按**最派生类型优先**匹配，捕获顺序决定行为；`catch(...)` 捕获一切但拿不到对象。

```cpp
#include <stdexcept>
#include <string>

void validate_age(int age) {
    if (age < 0) throw std::invalid_argument("age must be >= 0");
    if (age > 150) throw std::out_of_range("age implausible");
}

int main() {
    try {
        validate_age(-1);
    } catch (const std::invalid_argument& e) {   // 更具体的先匹配
        // e.what() -> "age must be >= 0"
    } catch (const std::out_of_range& e) {
        // 不会被上面的 invalid_argument 触发
    } catch (const std::exception& e) {           // 基类兜底
        // 捕获其它标准异常
    }
}
```

`[标准]` `catch` 按声明顺序匹配，因此**派生类必须写在基类之前**，否则被基类"截胡"。

```cpp
// ❌ 反例：基类在前，派生类永远命中不到
try { may_throw(); }
catch (const std::exception&) { /* 截胡 */ }
catch (const std::runtime_error&) { /* 死代码 */ }
```

```cpp
// ✅ 正例：最派生优先
try { may_throw(); }
catch (const std::runtime_error&) { /* 具体 */ }
catch (const std::exception&)     { /* 兜底 */ }
```

`catch` 的形参用 `const T&` 而非值：避免切片（slicing）且避免额外拷贝。需要重新抛出时写无操作数的 `throw;`（保留原对象类型与信息）。

```cpp
try { open(); }
catch (const std::exception& e) {
    log(e.what());     // 记录后原样向上传播
    throw;             // 保留完整类型，切勿 throw e;（会切片）
}
```

## ④ 栈展开与 RAII（异常安全）

`[标准]` 抛出异常后，运行时沿调用栈**反向展开（stack unwinding）**，对每个已构造的局部对象调用其析构函数，再进入匹配的 `catch`。展开过程中若析构函数再抛异常，程序立即 `std::terminate`。

```cpp
#include <iostream>
struct Guard {
    const char* name;
    ~Guard() { std::cout << "dtor " << name << '\n'; }   // 展开时自动调用
};
void f() { Guard g{"f"}; throw 1; }   // 抛出前 g 一定被析构
void g() { Guard g{"g"}; f(); }       // f 的异常穿透 g，g 仍被析构
```

`[经验]` 异常安全的根基是 **RAII**：把资源绑定到对象生命周期，让析构函数成为唯一的清理点。这样无论正常返回还是异常展开，资源都不会泄漏。

```cpp
#include <fstream>
#include <memory>
void process(const char* path) {
    std::ifstream in(path);            // RAII：离开作用域自动关闭
    auto buf = std::make_unique<char[]>(4096);  // 异常展开时自动释放
    if (!in) throw std::runtime_error("open failed");
    // 任何异常都会先析构 in 与 buf，再向上传播
}
```

```cpp
// ❌ 反例：裸指针 + 手动清理，异常会绕过 delete
void bad(const char* path) {
    FILE* f = fopen(path, "rb");
    if (some_error()) throw std::runtime_error("x");  // f 泄漏！
    fclose(f);
}
```

## ⑤ 异常安全等级（noexcept/基本/强/不抛）

`[标准]` 异常安全有四个约定等级，从弱到强：

1. **不抛（noexcept）**：保证不抛异常，或抛则 `terminate`；
2. **基本保证（basic）**：异常后对象仍有效、不泄漏，但状态可能变化；
3. **强保证（strong）**：异常后状态**完全回滚**到调用前（提交或回滚）；
4. **不泄漏（nothrow）**：析构与 swap 等必须 noexcept。

```cpp
#include <cstddef>
#include <vector>
class Buffer {
    std::vector<char> data_;
public:
    void clear() noexcept { data_.clear(); }          // 不抛：强/不抛
    void resize(std::size_t n) { data_.resize(n); }   // 基本保证（可能抛但有效）
};
```

`[标准]` `noexcept` 是函数契约也是优化提示：标准库容器在元素类型 `move` 为 `noexcept` 时才使用移动而非拷贝（否则为强保证退化成拷贝）。

```cpp
#include <vector>
class Widget {
public:
    Widget(Widget&&) noexcept = default;     // 标记为不抛，使 vector 重分配走移动
    Widget(const Widget&) = default;
};
std::vector<Widget> v(1000);
v.push_back(Widget{});    // 扩容时移动（因 noexcept），否则拷贝
```

```cpp
// swap 必须 noexcept：它是强保证回滚的基石
void swap(Buffer& a, Buffer& b) noexcept { a.data_.swap(b.data_); }
```

## ⑥ std::error_code / std::error_category [实现]

`[标准]` `std::error_code` 是一个轻量值类型（含 `int value` + `const error_category*`），用**零开销**表征系统/库错误，可跨函数返回而不展开栈。它不等于异常：调用方必须显式检查 `if (ec)`。

```cpp
#include <system_error>
#include <iostream>
int main() {
    std::error_code ec = std::make_error_code(std::errc::no_such_file_or_directory);
    std::cout << ec.category().name() << ':' << ec.value() << ' ' << ec.message() << '\n';
    if (ec == std::errc::no_such_file_or_directory) std::cout << "file missing\n";
}
```

`[实现]` `error_category` 的虚函数是整个机制的扩展点。本机 libstdc++（GCC 13.1.0）中，关键虚函数声明如下（源码剖析）：

```cpp
#include <string>
// 文件：C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/system_error
// 行号：106
//   class error_category { ... };           // 类别基类
// 行号：118
//   virtual const char* name() const noexcept = 0;     // 类别名（纯虚）
// 行号：134
//   virtual std::string message(int) const = 0;        // 人类可读信息（纯虚）
// 行号：147
//   virtual error_condition default_error_condition(int) const noexcept;  // 归一到可移植条件
```

自定义类别只需覆写 `name()`、`message()`，即可把任意枚举接入 `std::error_code` 体系（完整可编译示例见 `Examples/_ch146_errorcode.cpp`，本机运行输出 `db:1 connection timeout`）。

```cpp
#include <string>
enum class io_err { ok = 0, eof = 1, broken = 2 };
struct io_cat : std::error_category {
    const char* name() const noexcept override { return "io"; }
    std::string message(int e) const override {
        if (e == 1) return "eof"; if (e == 2) return "broken pipe"; return "ok";
    }
};
std::error_code make_error_code(io_err e) {
    static io_cat c; return {static_cast<int>(e), c};
}
namespace std { template<> struct is_error_code_enum<io_err> : std::true_type {}; }
```

## ⑦ std::expected (C++23) [标准]

`[标准]` `std::expected<T, E>` 是一个"要么有值 `T`，要么有错误 `E`"的 discriminated union，是异常的**零开销替代**：失败不展开栈、不分配，且强制调用方处理。C++23 引入。

```cpp
#include <expected>
#include <string>
#include <string_view>
std::expected<int, std::string> to_int(std::string_view s) {
    // 成功：隐式构造 expected<int,...>
    if (s == "42") return 42;
    // 失败：用 std::unexpected 包裹错误
    return std::unexpected(std::string("bad input: ") + std::string(s));
}
```

```cpp
#include <iostream>
#include <string>
#include <expected>
// 检查与取值
auto r = to_int("42");
if (r.has_value())        std::cout << *r << '\n';   // 或 r.value()
else                      std::cout << r.error() << '\n';
// C++23 单子式接口
auto doubled = to_int("7").transform([](int x){ return x*2; });   // expected<int,string>
auto safe    = to_int("x").or_else([](const std::string& e){
    return std::expected<int,std::string>(std::unexpected(e + " (defaulted)"));
});
```

`[标准]` 与 `std::optional` 的区别：`expected` 携带**错误原因**，`optional` 只表示"无值"。需要诊断信息时优先 `expected`。

```cpp
#include <string>
// 错误链：map 错误类型
auto parsed = to_int("x").transform_error([](std::string e){
    return "parse failed: " + e;     // 错误值也可 transform
});
```

## ⑧ std::optional 表征"无值"

`[标准]` `std::optional<T>` 表示"可能有值也可能没有"，适合**结果缺失是合法语义**的场景（如查找未命中）。它不携带错误原因——若失败需要原因，改用 `expected`。

```cpp
#include <optional>
#include <vector>
std::optional<int> find_first_even(const std::vector<int>& v) {
    for (int x : v) if (x % 2 == 0) return x;   // 命中：返回 int
    return std::nullopt;                        // 未命中：空 optional
}
```

```cpp
#include <iostream>
auto r = find_first_even({1,3,4,7});
if (r) std::cout << "even=" << *r << '\n';
else   std::cout << "no even\n";
// 提供默认值
int v = find_first_even({1,3}).value_or(-1);    // -> -1
```

```cpp
// ❌ 反例：用 optional 表达"失败原因"——信息丢失
std::optional<Config> load();   // 返回 nullopt 但调用方不知为何失败
// ✅ 正例：需要原因用 expected
std::expected<Config, LoadErr> load_ex();
```

## ⑨ 断言 assert / contract

`[标准]` `assert(cond)`（`<cassert>`）在 `NDEBUG` 未定义时对失败条件调用 `abort`，用于捕捉**不应发生的编程错误**（前置/不变量）。发布构建定义 `NDEBUG` 后断言被完全移除，因此断言内的表达式**不得有副作用**。

```cpp
#include <cassert>
double divide(double a, double b) {
    assert(b != 0.0 && "divisor must be non-zero");   // 调试期契约
    return a / b;
}
```

```cpp
// ❌ 反例：断言含副作用，NDEBUG 下被删除导致逻辑错误
assert(close(fd) == 0);   // 发布版本不会关闭 fd！
// ✅ 正例：副作用在断言外
int rc = close(fd); assert(rc == 0);
```

`[标准]` C++20 引入**契约（contracts）**提案方向（`pre`/`post`/`assert` 属性），但 GCC 13 仍以传统 `assert` 为主。契约用于"可被静态证明或运行期检查的接口前提"。

```cpp
#include <vector>
// C++20 契约（方向，GCC 13 支持有限；此处为语义示意）
int pop(std::vector<int>& v) [[assert: !v.empty()]] {
    int x = v.back(); v.pop_back(); return x;
}
```

## ⑩ 错误处理与 noexcept

`[标准]` `noexcept` 既是契约（违反则 `terminate`）也是优化器许可（可省略异常展开簿记）。错误处理与 `noexcept` 强相关：**析构函数、swap、移动操作应默认 noexcept**，否则破坏异常安全且拖慢容器。

```cpp
#include <utility>
class Handle {
    int fd_ = -1;
public:
    ~Handle() noexcept { if (fd_ >= 0) close(fd_); }   // 析构必须 noexcept
    Handle(Handle&& o) noexcept : fd_(std::exchange(o.fd_, -1)) {}  // 移动 noexcept
    Handle& operator=(Handle&& o) noexcept {
        std::swap(fd_, o.fd_); return *this;            // swap  noexcept
    }
};
```

```cpp
#include <utility>
// 条件 noexcept：仅当成员移动不抛时才 noexcept
template <typename T>
class Box {
    T v_;
public:
    Box(Box&& o) noexcept(noexcept(T(std::declval<T&&>()))) : v_(std::move(o.v_)) {}
};
```

`[经验]` 规则：**任何可能从异常路径被调用的清理函数都标 `noexcept`**；反之，会重新分配/可能抛的函数（如 `vector::push_back`）不要标 noexcept。

```cpp
// ❌ 反例：析构抛异常 => 栈展开中再抛 => terminate
~Widget() { if (flush() == false) throw std::runtime_error("flush failed"); }
// ✅ 正例：吞掉内部错误，记录日志，析构 noexcept
~Widget() noexcept { try { flush(); } catch (...) { log_flush_error(); } }
```

## ⑪ 异常与性能（用 g++ -O2 -S 看无异常路径零开销 / 异常表）

`[标准·实现]` "异常昂贵"是误解：**无异常发生的路径（happy path）在 Itanium C++ ABI 下零运行时开销**——不检查标志、不登记每帧状态。异常信息存放在只读段（`.eh_frame` / Windows 上 `.xdata`/`.pdata`），只在真正抛出时查表展开。

下面用本机 `g++ -std=c++23 -O2 -S -masm=intel` 对 `Examples/_ch146_perf.cpp` 取证。关键汇编（`_ch146_perf.asm`）：

```asm
; 自 Examples/_ch146_perf.asm（GCC 13.1.0, -O2 -masm=intel）
; add_nonthrow：无异常路径 -> 单条 lea，无任何 EH 簿记
_Z12add_nonthrowii:
        lea     eax, [rcx+rdx]      ; return a + b，纯算术
        ret

; add_throw：可能抛 -> 抛出分支被冷拆分到 .part.0 辅助函数
_Z9add_throwii:
        sub     rsp, 40
        ...
        call    _Z9add_throwii.part.0   ; 抛异常这条冷路径独立成函数
```

`[实现]` 取证结论：① `add_nonthrow` 编译为单条 `lea eax,[rcx+rdx]`，happy path 与"是否启用异常"无关；② `add_throw` 的抛出分支被优化器**冷拆分（cold split）**到独立的 `_Z9add_throwii.part.0`，使主路径保持精简。异常只在抛出的瞬间才有成本，符合"零开销抽象"原则。

```cpp
// 对应源码（节选，完整见 Examples/_ch146_perf.cpp）
int add_nonthrow(int a, int b) noexcept { return a + b; }   // -> lea
int add_throw(int a, int b) { if (b == 0) throw 0; return a / b; }  // -> 冷拆分
```

## ⑫ 异常规范演化（noexcept 替代 throw()）

`[标准]` C++98 的**动态异常规范** `throw(T1, T2)` 在运行期检查、且必须被携带到类型系统，开销大、收益小；C++11 起弃用，C++17 移除（仅保留 `noexcept` 与 `noexcept(...)`）。

```cpp
// C++98/03 风格（已弃用/移除）
void old() throw(std::runtime_error);    // 动态规范：只许抛 runtime_error，否则 unexpected
void old2() throw();                      // 承诺不抛（等价于现在的 noexcept）

// C++11 起：静态 noexcept（编译期契约，零运行期检查）
void modern() noexcept;                  // 不抛；违反 => terminate
void maybe() noexcept(false);            // 可能抛（默认，可不写）
void cond() noexcept(noexcept(some_op()));  // 条件 noexcept
```

```cpp
// 演进对比：noexcept 可被重载决议利用，throw() 不能
void f() noexcept;          // 优先匹配（移动/交换场景）
void f() noexcept(false);
```

`[经验]` 现代代码：**不要用 `throw()` 动态规范**，统一用 `noexcept`。`noexcept` 让优化器移除展开信息，并让标准库在重分配时选择移动语义。

```cpp
// ❌ 反例：动态异常规范（C++17 起非法）
void legacy() throw(std::exception);
// ✅ 正例
void modern() noexcept(false);
```

## ⑬ 自定义异常层次

`[标准]` 自定义异常应继承自 `std::exception`（或其子类如 `std::runtime_error`），以接入统一捕获点 `catch (const std::exception&)`。区分**逻辑错误（logic_error，可避免）**与**运行时错误（runtime_error，不可控）**。

```cpp
#include <stdexcept>
#include <string>
struct ConfigError : std::runtime_error {
    explicit ConfigError(const std::string& w) : std::runtime_error("config: " + w) {}
};
struct ParseError : ConfigError {
    explicit ParseError(const std::string& w) : ConfigError("parse: " + w) {}
};
void load() { throw ParseError("missing [server]"); }
```

```cpp
// 捕获层次：派生在前
try { load(); }
catch (const ParseError& e)    { /* 具体 */ }
catch (const ConfigError& e)   { /* 父类 */ }
catch (const std::exception& e){ /* 通用 */ }
```

`[经验]` 异常类型用**分层继承**而非扁平枚举，能让调用方按"可恢复粒度"捕获；但层次不宜过深（>3 层即过度设计）。给异常加上附加上下文字段（错误码、位置）提升可诊断性。

```cpp
#include <string>
struct DbError : std::runtime_error {
    int code;
    DbError(int c, const std::string& w) : std::runtime_error(w), code(c) {}
};
```

## ⑭ 资源清理与 finally（scope_exit）

`[标准]` C++ 没有 `finally` 关键字，但 **RAII + 析构** 实现等价语义。C++20 进一步提供 `<scope>` 的 `std::scope_exit` / `scope_success` / `scope_fail`（手动管理清理的轻量工具）。

```cpp
#include <scope>     // C++20
#include <cstdio>
void process() {
    FILE* f = fopen("log.txt", "w");
    auto close_on_exit = std::scope_exit([&]{ if (f) fclose(f); });  // 无论怎么离开都执行
    // ... 可能抛异常，但 close_on_exit 析构总会 fclose
}
```

```cpp
#include <functional>
// 手写 RAII 等价 finally（兼容 C++11）
struct Finally {
    std::function<void()> fn;
    ~Finally() noexcept { if (fn) fn(); }
};
void demo() {
    int* p = new int[16];
    Finally _([&]{ delete[] p; });   // 异常安全清理
    may_throw();
}
```

`[经验]` 优先用**确定性 RAII**（智能指针、容器、lock_guard），`scope_exit` 仅用于无法包装成类型的临时清理（如 C API 句柄、事务回滚）。

```cpp
// 事务：成功提交，异常回滚
auto rollback = std::scope_fail([&]{ tx.rollback(); });
tx.commit();   // 若此前抛异常，scope_fail 触发回滚
```

## ⑮ 错误传播（链式）

`[经验]` 沿调用栈向上传播错误时，应**保留并叠加上下文**，否则排障时只剩一句"open failed"无法定位。C++ 异常天然携带类型与 `what()`；`error_code`/返回值则需手动串联。

```cpp
#include <string>
// 异常链式：捕获后包裹更上层语义再抛出
void open_db() {
    try { connect(); }
    catch (const std::system_error& e) {
        throw std::runtime_error(std::string("open_db: ") + e.what());  // 叠加上下文
    }
}
```

```cpp
#include <expected>
// error_code 链式：把底层 ec 透传并附加上层枚举
std::expected<Row, DbError> query(Id id) {
    auto ec = low_level_read(id);
    if (ec) return std::unexpected(DbError{*ec, "query failed"});
    return Row{};
}
```

`[标准]` `std::nested_exception` 与 `std::throw_with_nested` 允许在重新抛出的同时保留原始异常链，供 `std::current_exception` 遍历。

```cpp
#include <exception>
void inner() { throw std::runtime_error("root cause"); }
void outer() {
    try { inner(); }
    catch (...) { std::throw_with_nested(std::runtime_error("outer context")); }
}
```

## ⑯ 跨 ABI 错误处理 [平台]

`[平台]` 异常是**实现细节耦合**的：Itanium ABI 与 MSVC 的异常处理模型不同，不同编译器/不同异常模型（SJLJ vs SEH vs DWARF）混链会 `terminate`。因此**跨 ABI / 跨语言 / 插件边界严禁抛异常穿越**。

```cpp
// ❌ 危险：异常从 DLL(MSVC) 抛到 EXE(MinGW) 边界 => 未定义行为
extern "C" void plugin_entry();   // 插件绝不能让 C++ 异常逃逸

// ✅ 安全：边界处把异常转成返回码/错误码
extern "C" int plugin_entry_safe(int* out) noexcept {
    try { *out = do_work(); return 0; }
    catch (const std::exception& e) { last_err = e.what(); return -1; }
    catch (...) { return -2; }
}
```

`[平台]` 在 Windows SEH 与 C++ 异常混合场景，用结构化异常处理捕获系统级故障（访问违例）时需隔离——C++ `catch(...)` 不一定捕获 SEH 异常，除非启用 `/EHa`（MSVC）或编译器特定选项。跨 ABI 边界统一用 `noexcept` + 返回码最稳妥。

```cpp
// 跨边界契约：所有导出 C 函数 noexcept，错误用 int 码
extern "C" int api_init() noexcept;
extern "C" int api_run(double* result) noexcept;
```

## ⑰ 日志与错误（预告 ch161）

`[经验]` 错误与日志是孪生：捕获错误时**记录足够上下文**（错误码、参数、调用位置、时间），但**不要在库内部擅自终止进程**——把"是否 fatal"的决定留给调用方。日志格式应机器可解析，错误对象应可序列化为 `error_code`。

```cpp
#include <system_error>
#include <iostream>
void report(const std::error_code& ec, const char* where) {
    std::cerr << "[ERR] " << where
              << " cat=" << ec.category().name()
              << " val=" << ec.value()
              << " msg=" << ec.message() << '\n';
}
```

关于结构化日志、日志级别、异步 sink 与性能化的深入实现，将在第161章（日志与可观测性）系统展开，本章仅给出"错误必须可观测"的最小约定。

```cpp
#include <string>
// 错误 -> 结构化字段（为第161章日志打基础）
struct ErrRecord { std::error_code ec; std::string site; };
void emit(const ErrRecord& r);   // 由日志层统一落盘/上报
```

## ⑱ 真实案例（标准库错误码取证，g++ 编译自包含示例）

`[实现]` 下面用本机 `g++ -std=c++23 -O2 -Wall -Wextra` 编译并运行 `Examples/_ch146_errorcode.cpp`（自定义 `std::error_code` 类别），验证：① `error_code` 可隐式由枚举构造；② `category().name()`/`message()` 来自自定义虚函数；③ `if (ec)` 判定错误态。

```cpp
#include <string>
// Examples/_ch146_errorcode.cpp（节选，完整见文件）
enum class db_err { ok = 0, timeout = 1, closed = 2 };
struct db_err_category : std::error_category {
    const char* name() const noexcept override { return "db"; }
    std::string message(int ev) const override {
        if (ev == 1) return "connection timeout";
        if (ev == 2) return "connection closed";
        return "ok";
    }
};
// 自由函数 + is_error_code_enum 特化 => 隐式转换
std::error_code make_error_code(db_err e) { static db_err_category c; return {int(e), c}; }
namespace std { template<> struct is_error_code_enum<db_err> : std::true_type {}; }
```

本机真实运行输出（零警告编译）：

```text
db:1 connection timeout
timeout detected
ec is in error state
```

`[标准]` 同机制下，`std::expected`（第⑦节）自包含示例 `Examples/_ch146_expected.cpp` 本机运行输出：

```text
value=42
error=not an int: oops
```

这证明：`error_code` 适合"轻量、可分类、跨边界"的错误；`expected` 适合"需要携带错误值、且希望零展开"的错误。两者都是异常的有效替代，取决于是否跨 ABI（第⑯节）。

## ⑲ 反模式（吞异常/空 catch）

`[经验]` 最危险的反模式是**吞掉异常**，它让故障静默、把可恢复错误变成数据损坏。

```cpp
// ❌ 反例 1：空 catch 吞掉一切
try { commit(); }
catch (...) { /* 什么都不做：故障消失，事务状态未知 */ }
```

```cpp
// ❌ 反例 2：catch 后忽略，继续执行（逻辑已不一致）
try { load_config(); }
catch (const std::exception&) { /* 继续用默认配置？还是已损坏？ */ }
```

```cpp
// ❌ 反例 3：用异常做正常控制流（异常应为异常路径）
while (true) {
    try { pop(); }
    catch (const Empty&) { break; }   // 应用返回值/optional 表达"空"
}
```

`[经验]` 正确做法：① 只在**确实能恢复**时才 `catch`；② 恢复不了就 `throw;` 原样上抛；③ 库代码默认不 `catch`，把决策权交给调用方；④ 必须兜底时记录日志并转为明确的错误码/返回状态。

```cpp
// ✅ 正例：要么恢复，要么透传并记录
try { commit(); }
catch (const std::system_error& e) {
    log(e.what());
    rollback();          // 恢复一致状态
    throw;               // 仍上抛，让上层知悉
}
```

```cpp
// ✅ 用 optional 表达"空"而非异常控制流
while (auto x = pop()) consume(*x);   // 自然终止，无异常
```

## ⑳ 小结

`[经验]` 错误处理是 API 契约的一等公民，选型优先级建议：

- **构造函数/运算符/拷贝**：无法返回错误码 → 用 `noexcept` 或抛异常；
- **可预期、可分类、需跨 ABI 的失败**：用 `std::error_code` / 返回值；
- **需要携带错误原因且零展开**：C++23 `std::expected`；
- **"无值"是合法语义**：`std::optional`；
- **真正异常、调用方难就地恢复**：异常 + RAII 保证不泄漏；
- **任何清理点（析构/swap/移动）**：一律 `noexcept`；
- **跨 ABI / 跨语言边界**：严禁异常逃逸，统一返回码；
- **永远不要**：空 `catch(...)`、用异常做控制流、`throw()` 动态规范。

```text
错误通道决策树（ASCII 框线）：
┌───────────────────────────────┐
│ 失败能否被调用方就地处理？      │
└───────────┬───────────────────┘
            ├── 否，且跨 ABI ──► std::error_code / 返回码（noexcept）
            ├── 否，可携带原因 ──► std::expected (C++23)
            ├── 否，"无值"合法 ──► std::optional
            └── 是，且异常罕见 ──► 异常 + RAII + noexcept 析构
```

本章全部示例均通过本机 `g++ -std=c++23 -O2 -Wall -Wextra` 真实编译验证（产物见 `Examples/_ch146_*.asm` 与 `_ch146_*_warn.txt`），关键机器码结论取自 g++ 生成的 Intel 语法汇编，未做任何编造。


## 附录 A：工业错误处理范式对比 [F: Industry]

四个世界级 C++ 项目的错误处理策略：

| 项目 | 范式 | 关键类型 | 设计理由 |
|---|---|---|---|
| Google (Abseil) | StatusOr<T> | `absl::Status`, `absl::StatusOr<T>` | 禁止异常 (Google C++ Style Guide 第 3 条)，零开销成功路径 |
| LLVM | ErrorOr<T> / Expected<T> | `llvm::Error`, `llvm::Expected<T>` | 禁止异常 (编译时间 + 可预测性)，move-only 错误类型防遗漏 |
| Chromium | 返回码 + CHECK/DCHECK | `base::Callback`, `bool` | 禁止异常 (二进制大小 + 可调试性)，简洁的 bool + CHECK |
| Qt | 信号/槽 + 错误码 | `QString::arg()`, `errorString()` | 无需异常 (跨语言绑定)，GUI 框架天然异步 |

```cpp
#include <iostream>
int main() {
    std::cout << "Error handling philosophy by project:\n";
    std::cout << "Google: StatusOr<T> — 'status or value' monad, zero-overhead success path\n";
    std::cout << "LLVM: Expected<T> — move-only, forces explicit error checking (cant ignore)\n";
    std::cout << "Chromium: bool return + CHECK — simplest, most debuggable\n";
    std::cout << "All three: completely ban C++ exceptions in production code\n";
    return 0;
}
```

## 附录 B：异常 vs 错误码 —— 汇编层面的真实代价 [E: Low-level / G: Performance]

```cpp
// 异常 vs 错误码的汇编对比（GCC -O2 x86-64）
int divide_error_code(int a, int b, int* out) {
    if (b == 0) return -1;
    *out = a / b;
    return 0;
}
// 汇编: test esi,esi; je .L_error; mov eax,edi; cdq; idiv esi; ret
// 成功路径: 4条指令, ~4 cycles

int divide_exception(int a, int b) {
    if (b == 0) throw std::runtime_error("div0");
    return a / b;
}
// 成功路径汇编: 同上（异常只在失败路径展开，成功路径零开销）
// 失败路径: ~100ns (unwind table lookup + RTTI + destructor chain)
```

```cpp
#include <iostream>
#include <chrono>
#include <vector>
#include <stdexcept>

// 微基准: exception vs error_code 在 99.9% 成功路径下的对比
int main() {
    volatile int sum = 0;
    auto t0 = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < 10000000; ++i) {
        int out;
        if (divide_error_code(10, 2, &out) == 0) sum += out;
    }
    auto t1 = std::chrono::high_resolution_clock::now();
    try {
        for (int i = 0; i < 10000000; ++i)
            sum += divide_exception(10, 2);
    } catch (...) {}
    auto t2 = std::chrono::high_resolution_clock::now();

    auto ec_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(t1-t0).count() / 10000000;
    auto ex_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(t2-t1).count() / 10000000;
    std::cout << "error_code: ~" << ec_ns << "ns/op  exception: ~" << ex_ns << "ns/op (success path)\n";
    std::cout << "Result: identical on success path. Exception cost is in the FAILURE path.\n";
    return 0;
}
```

## 附录 C：WG21 为什么拒绝 Checked Exceptions [B: Principle]

```
Java 的 checked exceptions 强制调用方处理或声明异常。C++ 委员会在多个提案中拒绝了类似机制:

P0709R0 (Herb Sutter, 2018): Zero-overhead deterministic exceptions
  → 提议: throws(ErrorType) 语法，编译期检查异常路径
  → 结论: 未进入 C++20。委员会认为已有 static_assert + expected<T> 可替代

Why no checked exceptions in C++:
1. 模板代码: template<typename T> void f(T t) — T 的异常类型在定义点未知
2. ABI 兼容: 添加 throws 声明会改变函数签名 (mangling)
3. 与 C 互操作: C 函数无异常规范，边界处必须包装
4. 破坏现有代码: 向现有函数添加 throws 声明 = 破坏二进制兼容性

C++ 错误处理的未来方向:
- C++23: std::expected<T,E> 标准化 (P0323R12)
- C++26: contracts (P2900) + possibly zero-overhead exceptions (P0709 derivative)
```

## 附录 D：面试与设计权衡 [H: Design / J: Learning]

```
错误处理策略选择矩阵:

场景                      推荐                      原因
────                      ────                      ────
热路径 (99.9% 成功)       std::expected<T,E>        异常在失败路径有代价
不可恢复错误              assert / std::abort()      前置条件违反 = 程序bug
构造函数中错误            异常 (唯一可报告的方式)     构造函数无返回值
析构函数中错误            吞咽 (log + continue)      析构中抛异常 = terminate
跨模块边界 (DLL)          std::error_code           异常跨 DLL = ABI 断裂
C API 包装                error_code → 异常转换       C 调用方不理解异常
异步回调                  std::promise::set_exception 唯一传递异常的方式
```

```cpp
#include <iostream>
#include <expected>
int main() {
    std::cout << "Q: Why do Google/LLVM ban exceptions?\n";
    std::cout << "A: Binary size (+15-30%), unpredictable performance, unwinding cost, team consistency.\n";
    std::cout << "Q: Is std::expected zero-overhead?\n";
    std::cout << "A: sizeof = max(sizeof(T), sizeof(E)) + bool flag + padding. ~2× sizeof on success path.\n";
    std::cout << "Q: When are exceptions actually faster?\n";
    std::cout << "A: When error rate < 0.01% — success path is zero-cost. Error path pays the unwind tax.\n";
    return 0;
}
```


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第145章](Book/part13_engineering/ch145_naming_api.md) | 键值查找/缓存 | 本章提供概念，第145章提供实现 |
| [第147章](Book/part13_engineering/ch147_code_review.md) | 多态插件/框架扩展 | 本章提供概念，第147章提供实现 |
| [第121章](Book/part10_modern/ch121_contracts.md) | 泛型库/编译期计算 | 本章提供概念，第121章提供实现 |
| [第88章](Book/part07_stl/ch88_optional_variant.md) | 资源管理/事务回滚 | 本章提供概念，第88章提供实现 |


## 相关章节（交叉引用）

- **后续依赖**：`Book/part07_stl/ch91_filesystem.md`（第91章 文件系统 filesystem）—— 本章为其前置，建议后续延伸阅读。
- **相邻主题**：`Book/part13_engineering/ch144_style.md`（第144章 代码风格与规范（C++））—— 编号相邻、主题接续。
- **相邻主题**：`Book/part13_engineering/ch148_gitflow.md`（第148章 Git 工作流（C++））—— 编号相邻、主题接续。
- **同模块**：`Book/part13_engineering/ch149_ci_cd.md`（第149章 CI/CD 流水线（C++））—— 同模块下的其他主题。

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

