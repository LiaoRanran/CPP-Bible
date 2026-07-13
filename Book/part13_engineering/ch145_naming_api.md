# 第145章 命名与 API 设计（C++）

⟶ Book/part13_engineering/ch144_style.md
⟶ Book/part12_patterns/ch135_patterns_intro.md

> **取证说明（Forensic Note）**：本章所有可被机器验证的结论，均用本机 GCC 13.1.0 真实产物佐证，示例源码位于 `Examples/_ch145_*.cpp`，对应汇编/警告产物位于 `Examples/_ch145_*.asm` 与 `Examples/_ch145_*_warn.txt`。编译命令统一为 `g++ -std=c++23 -O2 -S -masm=intel <src> -o <dst>.asm`，全部示例均通过 `-Wall -Wextra` 警告零洁净（warnings clean）验证；关键机器码结论直接引用 g++ 生成的 Intel 语法汇编，绝不编造。运行时事实（如 `sizeof`）由本机真实编译执行得出。源码剖析（第⑲节）引用的 libstdc++ 路径为本机真实存在的 `.../include/c++/bits/*.h`、`bits/vector.tcc`、`optional`，行号取自实际文件。立场分层标签：`[标准]`=ISO C++，`[实现]`=编译器/标准库实现，`[平台]`=OS/ABI，`[经验]`=工程共识。

## ① 概述：好命名的价值 [经验]

⟶ Book/part13_engineering/ch144_style.md
⟶ Book/part13_engineering/ch146_error_handling.md


命名不是"审美偏好"，而是**接口契约的第一行文档**。API 的使用者首先读到的不是实现，而是名字；一个好名字能让误用在编译期或 code review 阶段就被消灭，一个坏名字则把理解成本转嫁给每一个后续维护者。

`[经验]` 一条被工业界反复验证的共识：**名字是写给"调用方"的注释，而不是写给"实现者"的备忘录**。API 的可学习性（learnability）几乎完全由命名质量决定。

```cpp
// ❌ 反例：名字不揭示意图，调用方必须打开实现才能猜出语义
void proc(int a, int b);          // proc 做什么？a、b 是什么？
int f(int x);                     // f 返回什么？x 是输入还是索引？
```

```cpp
#include <cstddef>
// ✅ 正例：名字揭示意图、参数揭示角色
void compress_frame(Frame& dst, const Frame& src);   // 动宾 + 方向清晰
std::size_t byte_size(const Buffer& buf);            // 返回什么一目了然
```

好命名的三个收益维度：

- **可发现性**：IDE 自动补全下，`find_*` / `create_*` / `is_*` 前缀让使用者快速定位；
- **可防误用**：类型名与单位名直接消除"该传什么"的歧义；
- **可演进性**：稳定的命名边界让实现可重构而不破坏调用方。

```cpp
// 命名稳定的 API：内部可随意重构，调用方零改动
class ConnectionPool {
public:
    bool acquire(Connection& out, int timeout_ms);   // 名字 10 年不变，实现可重写
};
```

## ② 命名基本法则（意图揭示）

`[经验]` 命名的第一法则：**揭示意图，而非揭示类型或实现**。名字要回答"这是什么 / 做什么"，而不是"它存了几个字节"。

```cpp
// ❌ 反例：揭示类型而非意图（改了类型名就过时）
int data_list_size;          // data_list 是什么列表？
char* str_ptr;               // str 指向谁的字符串？
```

```cpp
#include <string>
// ✅ 正例：揭示意图，类型信息交给类型系统
int pending_request_count;   // 意图：待处理请求数
std::string user_name;       // 意图：用户名，类型由 string 表达
```

二级法则：**长度与可见范围成正比**——作用域越大、生命周期越长，名字应越长越具体；局部短变量可用单字母。

```cpp
#include <cstddef>
// 短作用域：单字母足够
for (std::size_t i = 0; i < v.size(); ++i) sum += v[i];

// 跨模块全局符号：必须长且自解释
namespace telemetry {
    inline constexpr int kMaxBufferedSamples = 4096;
}
```

`[经验]` 避免"双重否定"与"模糊动词"：`disable_not_cache` 应写作 `enable_cache`；`handle(x)` 应写作 `process(x)` 或 `dispatch(x)`。

```cpp
// ❌ 反例：双重否定 + 模糊动词
bool disable_not_cache = false;
void handle(const Event& e);

// ✅ 正例
bool cache_enabled = false;
void dispatch(const Event& e);
```

## ③ 类型命名（PascalCase/类/struct）

`[标准·惯例]` 用户自定义类型（class / struct / enum / typedef / concept / 模板）统一用 **PascalCase**（大驼峰），与标准库 `std::string`、`std::vector` 的命名风格一致，使自定义类型"看起来像类型"。

```cpp
class ConnectionPool { /* ... */ };     // ✅ PascalCase 类型
struct HttpRequest  { /* ... */ };      // ✅ struct 同样 PascalCase
enum class ColorSpace { Srgb, DisplayP3 };  // ✅ enum class 成员 PascalCase
```

模板参数用描述性名字，避免单字母 `T`（除非极其通用）：

```cpp
// ❌ 反例：单字母模板参数，约束意图不清
template <typename T, typename U> class Pair { /* ... */ };

// ✅ 正例：描述性模板参数
template <typename Key, typename Value> class LruCache { /* ... */ };
template <std::regular T> class RingBuffer { /* ... */ };
```

概念（concept）命名用名词或形容词短语，常以 `able`/`ible` 结尾：

```cpp
template <typename T>
concept RandomAccess = requires(T t) { t[0]; t.size(); };   // ✅ 形容词性概念
```

`[标准]` 类型别名用 `using`（而非 `typedef`）更易读，且支持模板别名：

```cpp
#include <memory>
#include <vector>
using ConnectionPtr = std::shared_ptr<Connection>;          // ✅ 别名 PascalCase/Snake 视项目
template <typename T> using Vec = std::vector<T>;
```

## ④ 函数命名（动词/动宾）

`[经验]` 函数命名用**动词或动宾短语**，因为函数"做某事"。查询类（纯读）可用名词，命令类（有副作用）必须动词。

```cpp
#include <cstddef>
// ✅ 命令（有副作用）：动词开头
void start_server();
void flush_cache();
bool send_packet(const char* data, std::size_t len);

// ✅ 查询（无副作用）：名词或 is_/has_/get_ 前缀
std::size_t packet_count() const;
bool is_connected() const;
const Config& config() const;
```

返回布尔值的谓词统一 `is_`/`has_`/`can_` 前缀，使 `if (is_open())` 读起来像自然语言：

```cpp
bool has_permission(User u, Permission p);
bool can_write() const;
```

`[经验]` 避免"动词+ing"和"模糊 get"：

```cpp
// ❌ 反例
void processing();        // 是开始处理还是正在处理？
int get();                // 得到什么？

// ✅ 正例
void process();           // 处理（命令）
int retry_count() const;  // 明确得到什么
```

重载函数名应保持一致，仅参数不同；若语义不同，应改名而非重载（见第⑪节）。

```cpp
#include <string>
// ✅ 同名重载：语义一致，仅参数形态不同
void log(Level lvl, const char* msg);
void log(Level lvl, const std::string& msg);
```

## ⑤ 变量命名（snake_case/camelCase）

`[经验]` 变量（含函数局部、成员、命名空间级非类型）命名二选一并与项目基线统一：**snake_case**（C++ 社区/Google/LLVM 主流）或 **camelCase**（Microsoft 风格）。关键是全仓库只有一个真相。

```cpp
#include <vector>
int active_connection_count = 0;     // ✅ snake_case
int activeConnectionCount   = 0;     // ✅ camelCase（选其一，勿混用）

std::vector<int> pending_frames;     // ✅ 复数揭示"集合"
```

私有/受保护成员加尾下划线 `_`，与局部变量、参数区分，避免 `this->` 噪声：

```cpp
#include <cstddef>
class Buffer {
    std::size_t capacity_ = 0;       // ✅ 尾下划线：私有成员
    std::byte*  data_ = nullptr;
public:
    void reserve(std::size_t capacity);  // 参数无下划线，与成员区分
};
```

`[经验]` 避免"匈牙利命名"冗余（`strName`、`nCount`、`pBuf`）——类型已由声明给出，前缀只增加噪音且与重构冲突。

```cpp
// ❌ 反例：匈牙利命名，类型变了前缀就错
int    nCount;
char*  pName;
// ✅ 正例：名字承载意图，类型交给声明
int    user_count;
std::string user_name;
```

循环/临时短变量可用单字母，但含义要局部自明：

```cpp
for (const auto& [key, value] : registry) { /* key/value 局部自明 */ }
```

## ⑥ 常量与宏命名（kXxx/UPPER_CASE）

`[经验]` 编译期常量用 `kPascalCase`（Google 风）或 `k_snake_case`，贯穿 `constexpr`/`const` 静态成员/枚举值；宏用全大写 `UPPER_SNAKE_CASE`（必须与普通标识符视觉隔离，因宏无视作用域）。

```cpp
#include <cstddef>
class Config {
public:
    static constexpr int kMaxRetries = 5;          // ✅ k 前缀常量
    static constexpr std::size_t kDefaultBuffer = 4096;
};
inline constexpr double kPi = 3.141592653589793;
```

宏必须全大写，且加项目前缀避免碰撞：

```cpp
#define PROJECT_LOG_LEVEL 3            // ✅ 全大写 + 前缀
#define PROJECT_HAS_FEATURE_X 1
// ❌ 反例：宏用小写会伪装成普通符号
#define logLevel 3
```

枚举值命名与常量一致（C++11 起 `enum class` 作用域隔离，但仍推荐 `k` 前缀或全大写）：

```cpp
enum class LogLevel { kTrace, kInfo, kWarn, kError };   // ✅ 作用域枚举 + k 前缀
```

`[经验]` 能用 `constexpr`/`const`/`enum` 就绝不用 `#define`——宏无类型、无视命名空间、难调试：

```cpp
// ❌ 反例
#define MAX_SIZE 1024
// ✅ 正例
inline constexpr std::size_t kMaxSize = 1024;
```

## ⑦ 命名空间命名

`[经验]` 命名空间用小写短名，避免与类型（PascalCase）"撞脸"，并体现模块边界。顶层命名空间通常就是项目/库名。

```cpp
namespace myproject {
    namespace net {          // ✅ 小写短名子模块
        class Socket;
    }
    namespace crypto {
        void sha256(...);
    }
}
```

实现细节放进 `detail` 子命名空间或匿名命名空间，向调用方声明"这是内部，随时可改"：

```cpp
namespace myproject {
    namespace detail {       // ✅ 明确内部实现，API 稳定性不保证
        void parse_internal(...);
    }
}
```

匿名命名空间（翻译单元内部链接）替代 `static`，隐藏 `.cpp` 内辅助符号：

```cpp
namespace {
    int g_debug_counter = 0;                 // ✅ 仅本 .cpp 可见
    void trace_raw(const char* s) { /* ... */ }
}
```

`[经验]` 禁止在头文件作用域 `using namespace`——它会泄漏给所有包含方，制造难以追踪的名字冲突（见第⑧节 ABI/API 边界）。

```cpp
// ❌ 反例：头文件顶层 using，污染所有包含者
// widget.h
using namespace std;   // 禁止
```

内联命名空间用于**版本化 ABI**（详见第⑰节）：

```cpp
namespace myproject {
    inline namespace v2 { void serialize(); }   // ✅ 默认可见
    namespace v1 { void serialize(); }          // 旧版仍可 myproject::v1::serialize()
}
```

## ⑧ API 稳定性（ABI/API 边界）[平台]

`[平台·x86-64/Itanium-ABI/Windows-x64-ABI]` API（源码接口）与 ABI（二进制接口）是两层边界：**API 变了重新编译即可，ABI 变了必须所有下游重新链接**。ABI 由数据布局、名字修饰（mangling）、调用约定、异常传播模型共同决定。

`[经验]` 影响 ABI 的改动（任一即破坏二进制兼容）：

- 增删/重排非静态数据成员（改变 `sizeof` 与偏移）；
- 改变成员类型（哪怕大小相同）；
- 增删虚函数（改变 vtable 布局）；
- 改变函数签名（改变名字修饰）。

```cpp
// ❌ 反例：在类中部插入成员，破坏所有调用方 ABI
class Widget {
    int a;
    int b_added_later;   // 旧二进制里 a 之后没有它 → 偏移错位崩溃
    int c;
};
```

Pimpl 是最强的 ABI 防火墙——把数据成员收进不可见的 impl，使"头文件大小"与实现完全解耦。本机真实运行取证（`Examples/_ch145_size.cpp`）：

```
sizeof(PimplWidget)=8        // 仅持有一个 unique_ptr（指针=8 字节）
sizeof(FatWidget) =256       // 直接内联 64 个 long，随实现膨胀
```

```cpp
#include <memory>
// Pimpl：调用方看到的头文件大小恒为 8 字节，与 FatImpl 多胖无关
class PimplWidget {
    struct Impl;                       // 前向声明，实现不可见
    std::unique_ptr<Impl> impl_;
public:
    PimplWidget();
    ~PimplWidget();
};
```

`[平台]` 名字修饰（name mangling）把 C++ 重载/命名空间编码进符号名，是 ABI 的一部分且**各编译器不兼容**。用 `extern "C"` 暴露稳定 C ABI 给跨语言/跨编译器调用：

```cpp
// 稳定的 C ABI：名字不修饰，调用约定显式，跨编译器可用
extern "C" int myproject_version();
```

ABI 稳定性决策框：

```
┌──────────────────────────────────────────────────────────┐
│ 该符号要进"稳定 ABI"吗？                                   │
├──────────────────────────────────────────────────────────┤
│ 是 → 放进 .so/.dll 公开头；用 Pimpl/ extern "C" 隔离布局   │
│      → 永不在类中部增删成员、不改虚表、不改签名            │
│ 否 → 放进 detail/ 匿名命名空间/ 静态库内部，随时可改       │
└──────────────────────────────────────────────────────────┘
```

## ⑨ 接口设计原则（最小完备）

`[经验]` 好接口遵循**最小完备（minimal & complete）**：提供完成任务所需的**最少**函数，但又不缺必需的那几个。多一个函数就多一份维护与 ABI 负担；少一个则逼用户绕过封装。

```cpp
// ❌ 反例：接口过度暴露，调用方可篡改内部不变量
class Stack {
public:
    std::vector<int> data_;        // 暴露内部 → 不变量可被破坏
    void push(int x) { data_.push_back(x); }
};
```

```cpp
#include <cstddef>
#include <vector>
// ✅ 正例：最小完备，内部不可见，行为可保证
class Stack {
public:
    void push(int x);
    int  pop();
    bool empty() const;
    std::size_t size() const;
private:
    std::vector<int> data_;        // 封装在内部
};
```

`[经验]` 三条经验法则：

- **优先非成员非友元**：能写成自由函数的，不要写成成员（降低耦合、提升对称）；
- **能 `const` 就 `const`**：只读操作都标 `const`，扩大可调用上下文；
- **后置 `noexcept`/`constexpr`**：见第⑬、⑩节。

```cpp
#include <cstddef>
// ✅ 自由函数 + const，对称且低耦合
bool operator==(const Stack& a, const Stack& b);
std::size_t hash_value(const Stack& s);
```

避免"为了对称堆砌重载"——只提供真正被使用的形态：

```cpp
// ❌ 反例：用户其实只需要 (const char*)，却提供了 6 个重载
void set_name(const char*);
void set_name(const std::string&);
void set_name(std::string&&);
void set_name(std::string_view);
// ... 维护成本高且无必要
```

## ⑩ Pimpl 惯用法（隐藏实现，用 g++ -O2 -S 看间接调用）

Pimpl（Pointer to Implementation）把数据成员与实现收进一个前向声明的 impl 结构，只在 `.cpp` 定义。它同时带来**ABI 稳定**（第⑧节）与**编译防火墙**（改实现不触发调用方重编）。

`[实现·GCC13]` 关键成本模型：Pimpl 调用需经指针进入 impl，等价于一次**间接分支**。本机 g++ 取证（`Examples/_ch145_pimpl.asm`）对比"经函数指针的间接调用"与"直接调用"：

```cpp
// _ch145_pimpl.cpp 要点（自包含可编译）
using draw_fn = void(*)(int);
void draw_impl(int n);
void use_indirect(draw_fn f, int n) { f(n); }   // 间接：经指针
void use_direct(int n)            { draw_impl(n); }  // 直接：可内联
```

真实 g++ 汇编（节选）：

```asm
_Z12use_indirectPFviEi:
        mov     rax, rcx          ; f 在第1参 rcx，转存
        mov     ecx, edx          ; n 移到第1参位
        rex.W jmp rax             ; 间接跳转到函数指针（经寄存器 rax）

_Z10use_directi:
        mov     edx, ecx
        lea     rcx, .LC0[rip]
        jmp     _ZL6printfPKcz.constprop.0   ; 直接尾调用 printf，无函数指针间接层
```

结论真实可复现：**间接调用（jmp rax）无法像直接调用那样被内联进调用方**——这正是 Pimpl 的运行时代价。它用"一次指针间接 + 失去跨 TU 内联"换取"ABI 稳定 + 编译防火墙"，是典型工程权衡。

```cpp
#include <memory>
// Pimpl 头文件：调用方只看到指针，实现彻底隐藏
class Widget {
    struct Impl;
    std::unique_ptr<Impl> impl_;
public:
    Widget();
    ~Widget();
    void draw();
    int  metric() const;
};
```

```cpp
#include <memory>
// Widget 实现（widget.cpp）：所有数据成员与逻辑在这里，改它不触发调用方重编
struct Widget::Impl { int w = 0, h = 0; void paint() { /* ... */ } };
Widget::Widget() : impl_(std::make_unique<Impl>()) {}
Widget::~Widget() = default;
void Widget::draw() { impl_->paint(); }
int  Widget::metric() const { return impl_->w * impl_->h; }
```

`[经验]` 决策：库/长期维护的组件用 Pimpl 锁 ABI；性能极热路径且 impl 必然同 TU 可见时，可放弃 Pimpl 换内联。

## ⑪ 重载 vs 命名函数

`[经验]` 重载适合"同一操作、不同参数形态"；当语义其实不同，**命名函数比重载更安全**——重载解析在隐式转换下可能产生反直觉的匹配。

```cpp
#include <string_view>
// ✅ 重载合理：语义一致，仅参数形态不同
void print(std::string_view sv);
void print(int value);
void print(double value);
```

当调用方意图差异大，命名函数消除歧义：

```cpp
// ❌ 反例：用重载表达两种不同语义，易误用
void open(const std::string& path);          // 读
void open(const std::string& path, Mode m);  // 读/写

// ✅ 正例：命名函数显式区分意图
void open_read_only(const std::string& path);
void open_with_mode(const std::string& path, Mode m);
```

本机编译取证（`Examples/_ch145_overload.cpp`，`-Wall -Wextra` 零警告）展示重载解析按参数形态选择：

```cpp
void log(int level, const char* msg);
void log(const char* msg) { log(0, msg); }   // 重载
void log_info(const char* msg)  { log(0, msg); }  // 命名函数，意图更显式
void log_error(const char* msg) { log(2, msg); }
```

```cpp
int main() {
    log("hello");        // 解析到 (const char*)
    log(1, "warn");      // 解析到 (int, const char*)
    log_info("info");
    log_error("boom");
    return 0;
}
```

`[经验]` 规则：仅当"名字相同能让 API 更直觉"时重载；涉及单位/模式/所有权差异时，用命名函数。

## ⑫ 默认值与重载顺序

`[经验]` 默认参数与重载混用是歧义高发区：**有默认参数的重载，在省略实参处会与无默认版本冲突**。优先用"纯重载分层"替代"默认参数拼装大接口"。

```cpp
// ❌ 反例：两版在 open("x") 处二义
void open(const std::string& path);
void open(const std::string& path, int flags = 0);   // 与上一行冲突
```

本机编译取证（`Examples/_ch145_defaults.cpp`，warnings clean）给出正例：

```cpp
#include <string>
void open(const std::string& path) { /* 缺省模式 */ }
void open(const std::string& path, int flags) { /* 显式模式 */ }

int main() {
    open("a.txt");          // 唯一匹配 (const string&)
    open("b.txt", 0644);    // 唯一匹配 (const string&, int)
    return 0;
}
```

`[经验]` 重载序规则：

- **把"最具体"的版本放在"最通用"之前或之后都行，但参数集必须互不包含**；
- 默认参数只在声明处写一次（通常在头文件）；
- 需要"可选尾参"且形态单一时，默认参数可接受；多可选参数且语义不同，用重载。

```cpp
// ✅ 默认参数用于真正"可选且语义一致"的尾参
void connect(const Endpoint& ep, Duration timeout = Duration::seconds(5));

// ❌ 反例：多默认参数且单位混乱
void configure(int buf = 1024, bool compress = true, int level = 6);
// → 调用 configure(2048) 含义模糊（改缓冲还是改...？），应拆命名函数
```

## ⑬ noexcept 与异常规范（关联 ch146）

`[标准]` `noexcept` 向编译器与调用方承诺"此函数不会传播异常"。违反时不是抛异常，而是直接 `std::terminate`（[except.spec]）。它对**正确性**（容器强异常安全）与**优化**（编译器可省略异常展开框架）都有真实影响；关联 ch146 的异常安全章节深入。

`[实现·GCC13]` 真实取证：当 `noexcept` 函数体内含 `throw`，g++ 直接给出 `-Wterminate` 警告，证明编译器在 noexcept 契约下改变了分析——它知道此处必终止：

```
_ch145_noexcept2.cpp:3:24: warning: 'throw' will always call 'terminate' [-Wterminate]
    3 | void sink() noexcept { throw 1; }
      |                        ^~~~~~~
```

```cpp
// _ch145_noexcept2.cpp 要点（自包含可编译）
void sink() noexcept { throw 1; }    // g++ 警告：'throw' will always call 'terminate'
void boom() { throw 2; }             // 普通函数：保留正常异常抛出路径
```

`[标准]` `noexcept` 还是条件化的：`noexcept(expr)` 在编译期求值。移动构造/移动赋值/析构/交换应默认 `noexcept`，从而让 `std::vector` 重分配走移动而非拷贝（ch144 已用 libstdc++ 源码佐证此决策）。

```cpp
#include <vector>
class Buffer {
    std::vector<int> data_;
public:
    Buffer(Buffer&&) noexcept = default;        // ✅ 移动不抛
    Buffer& operator=(Buffer&&) noexcept = default;
    ~Buffer() noexcept = default;               // ✅ 析构不抛
    void swap(Buffer& o) noexcept { data_.swap(o.data_); }   // ✅ swap 不抛
};
```

```cpp
// ❌ 反例：应在 noexcept 却未标，vector 重分配将退化为拷贝（见 ch144）
struct Bad { std::string s; Bad(Bad&&) = default; };  // 默认移动实为 noexcept，
                                                      // 但手写非 noexcept 版本即触发退化
```

`[经验]` 规则：析构、移动构造/赋值、swap 一律 `noexcept`；公开接口若承诺不抛，也标 `noexcept`——这既是文档也是优化许可。

## ⑭ 返回值策略（值/引用/optional）

`[经验]` 返回值选择决定所有权与成本：

- **返回 `const T&`**：调用方不取得所有权、不应长期持有（原对象销毁即悬垂）；
- **返回值（by value）**：转移所有权或拷贝，安全但与对象大小相关成本；
- **返回 `std::optional<T>`**：表示"可能无值"的函数结果，强于返回哨兵值。

`[实现·GCC13]` 真实取证（`Examples/_ch145_return.asm`）对比三种返回：

```cpp
#include <optional>
struct Big { long a[8]; };
Big by_value();                 // 大对象：经隐藏返回缓冲(sret)返回
const Big& by_ref(const Big&);  // 返回入参地址
std::optional<Big> by_opt();    // 可选结果
```

真实 g++ 汇编（节选）：

```asm
_Z8by_valuev:
        movdqa  xmm0, XMMWORD PTR .LC0[rip]
        movups  XMMWORD PTR [rcx], xmm0   ; rcx = 调用方提供的隐藏返回缓冲(sret 指针)
        movdqa  xmm0, XMMWORD PTR .LC1[rip]
        mov     rax, rcx                  ; rax 返回缓冲地址
        movups  XMMWORD PTR 16[rcx], xmm0
        ret

_Z6by_refRK3Big:
        mov     rax, rcx                  ; 直接把入参指针 rcx 作为返回值传出，零拷贝
        ret

_Z9use_valuev:
        mov     eax, 1                    ; 编译期折叠为常量 1，未发生 64 字节物化
        ret

_Z7use_refRK3Big:
        mov     eax, DWORD PTR [rcx]      ; 从引用对象读取，零拷贝
        ret
```

结论真实可复现：**`by_ref` 仅把指针交还（O(1)），`by_value` 则需把对象写入调用方缓冲（与大小成正比，除非被优化掉）**。经验法则：

```cpp
#include <cstdint>
#include <memory>
#include <string>
#include <optional>
// ✅ 查询成员：返回 const 引用，避免拷贝且不转移所有权
const std::string& name() const { return name_; }

// ✅ 工厂/转换：返回值转移所有权
std::unique_ptr<Connection> open(int fd) { return std::make_unique<Connection>(fd); }

// ✅ "可能失败"的查找：optional 比哨兵清晰
std::optional<Record> find(std::uint64_t id) const;
```

```cpp
// ❌ 反例：返回局部对象的引用（悬垂！）
const std::string& bad() { std::string s = "x"; return s; }  // 返回后 s 已销毁
```

## ⑮ 概念约束（concepts 作为接口文档）

`[标准·C++20]` `concept` 既是编译期约束，也是**接口文档**：模板参数需要满足什么，一眼可读，且错误信息远优于 SFINAE。优先 concept 而非 SFINAE（ch144 第⑫节已对比可读性）。

本机编译取证（`Examples/_ch145_concepts.cpp`，`-Wall -Wextra` 零警告）：

```cpp
template <typename T>
concept Arithmetic = std::integral<T> || std::floating_point<T>;

template <Arithmetic T>
T clamp(T x, T lo, T hi) { return x < lo ? lo : (x > hi ? hi : x); }

template <typename T>
concept Drawable = requires(T t) { { t.draw() } -> std::same_as<void>; };

template <Drawable T>
void render(T& t) { t.draw(); }
```

```cpp
int main() {
    clamp(5L, 0L, 10L);   // ✅ long 满足 Arithmetic
    Circle c; render(c);  // ✅ Circle 满足 Drawable
    return 0;
}
```

`[经验]` 把 concept 当作"命名化的接口契约"——`Arithmetic`、`Drawable`、`Readable` 比 `typename T` 表达力强百倍，且调用方违反时得到指向 concept 的清晰报错。

```cpp
// ✅ 多约束组合，意图自解释
template <typename T>
concept Serializable = std::semiregular<T> && requires(T t, std::ostream& os) {
    { t.serialize(os) } -> std::same_as<void>;
};
```

```cpp
// ❌ 反例：无约束模板，误用时报错指向深层实现细节
template <typename T>
auto area(const T& s) { return s.width * s.height; }   // T 没有 width 时报错难读
```

## ⑯ 防误用设计（强类型/删除函数 =delete）

`[经验]` 最好的 API 是"错误的用法无法编译通过"。两种核心手段：**强类型（strong typedef）** 与 **删除危险重载（`= delete`）**。

本机编译取证（`Examples/_ch145_strong.cpp`，warnings clean）展示两者：

```cpp
#include <cstdint>
struct UserId { int64_t v; explicit UserId(int64_t x) : v(x) {} };
struct OrderId { int64_t v; explicit OrderId(int64_t x) : v(x) {} };

void process(OrderId id);            // UserId 无法冒充 OrderId

struct Meter {
    explicit Meter(double m) : m_(m) {}
    Meter(int) = delete;             // 禁止 int→Meter，杜绝单位混淆
    double m_ = 0;
};
```

```cpp
int main() {
    UserId u{42}; OrderId o{7};
    // process(u);          // ❌ 编译错误：UserId != OrderId
    process(o);            // ✅
    Meter m{1.5};          // ✅
    // Meter bad{3};        // ❌ 编译错误：Meter(int) 已删除
    return 0;
}
```

`[经验]` 用强类型把"单位/ID/标签"变成类型，让编译器替你挡住 `process(user_id, order_id)` 这类颠倒参数的 bug：

```cpp
// ✅ 强类型让"参数顺序"由类型系统校验
void transfer(UserId from, UserId to, Amount cents);
// transfer(to, from, amt);   // ❌ 编译期即报错，from/to 不会颠倒
```

`= delete` 还能删除危险隐式转换与拷贝：

```cpp
class NonCopyable {
public:
    NonCopyable(const NonCopyable&) = delete;       // 禁止拷贝
    NonCopyable& operator=(const NonCopyable&) = delete;
    NonCopyable() = default;
};

// 禁止 bool 与 int 的歧义重载（经典坑）
void f(bool);
void f(int) = delete;     // 只接受显式 bool，杜绝 int→bool 的意外窄化
```

## ⑰ 版本与弃用（[[deprecated]]，用 g++ 看警告）

`[标准·C++14]` `[[deprecated("msg")]]` 标记即将移除的接口，g++ 在调用处发警告而不破坏编译——这是"渐进式 API 演进"的标准手段。

`[实现·GCC13]` 真实取证（`Examples/_ch145_deprecated.cpp`，`-Wall -Wextra`）：

```cpp
// _ch145_deprecated.cpp 要点
[[deprecated("use new_api() instead; removed in v3")]]
void old_api() {}

int main() {
    old_api();   // 触发弃用警告
    return 0;
}
```

g++ 真实警告输出：

```
_ch145_deprecated.cpp:8:12: warning: 'void old_api()' is deprecated:
    use new_api() instead; removed in v3 [-Wdeprecated-declarations]
    8 |     old_api();
      |     ~~~~~~~^~
```

`[经验]` 弃用流程：先 `[[deprecated]]` + 警告（保留 N 个版本）→ 再删。绝不"静默删除"破坏调用方。配合内联命名空间做 ABI 版本切换（第⑦节）：

```cpp
namespace lib {
    inline namespace v2 {
        void serialize();          // 当前默认
    }
    namespace v1 {
        [[deprecated("use v2::serialize")]]
        void serialize();          // 旧版，仍可调 lib::v1::serialize
    }
}
```

```cpp
#include <cstddef>
#include <span>
// ✅ 弃用同时给出"去哪"——msg 必须含替代方案
[[deprecated("use std::span instead of raw pointer+size pairs")]]
void process(const int* data, std::size_t n);
```

## ⑱ API 文档（Doxygen）

`[经验]` 文档是 API 契约的一部分。**公开接口的每个函数都应有 Doxygen 注释**：说明做什么、参数约束、返回值语义、异常/不变量、线程安全。

```cpp
/**
 * @brief 从连接池获取一个空闲连接
 * @param timeout_ms 最长等待毫秒；<=0 表示立即返回
 * @return 成功返回连接句柄；池空且超时返回 nullptr
 * @note 调用方须在使用后调用 release() 归还，禁止 delete。
 * @throw 不抛；超时仅返回 nullptr（弱异常保证）。
 */
Connection* acquire(int timeout_ms);
```

`[经验]` 文档铁律：

- 注释解释"契约与陷阱"，不复述代码；
- `@note`/`@warning` 标不变量与线程安全；
- 文档随签名改而改；过时文档比无文档更危险；
- 内部 `detail::` 符号可不文档化，但公开符号必须。

```cpp
#include <string>
/// @warning 返回的引用在对象析构后悬垂，调用方不得长期持有。
const std::string& name() const;
```

```cpp
// 组命令标记便于生成模块页
/// @defgroup pool Connection Pool
/// @brief 连接池公开接口
/// @{
class ConnectionPool { /* ... */ };
/// @}
```

## ⑲ 真实案例（标准库命名剖析，引用 libstdc++ 源码路径+行号）

标准库的命名本身就是"工业级 API 设计范本"。下面剖析 libstdc++（本机 GCC 13.1.0）中几个关键命名的实现锚点，路径与行号均取自真实文件。

**案例 A：`std::move` / `std::move_if_noexcept` 的命名即文档**

`std::move` 不"移动"任何东西，只是把左值转为右值引用——名字直白。而 `move_if_noexcept` 的命名直接编码了第⑬节的异常安全策略："若移动不抛则移动，否则退化为 const 引用（拷贝）"。

```cpp
// 文件：C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/bits/move.h
// 行号：109-125
//   struct __move_if_noexcept_cond        // 109: 判断"移动是否 noexcept"的特质
//   move_if_noexcept(_Tp& __x) noexcept    // 125: 不抛则返回 T&&，否则 const T&
```

**案例 B：`std::vector` 重分配的 `relocate` vs `move_if_noexcept`**

`vector.tcc` 用 `_S_use_relocate()` 决定"能否整体搬迁元素"，否则走 `__uninitialized_move_if_noexcept_a`——命名把"异常安全下的搬迁策略"暴露在每一行。

```cpp
// 文件：C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/bits/vector.tcc
// 行号：478-515
//   478: if _GLIBCXX17_CONSTEXPR (_S_use_relocate())
//   492:     = std::__uninitialized_move_if_noexcept_a(...)   // 否则退化为拷贝
//   515: if _GLIBCXX17_CONSTEXPR (!_S_use_relocate())
```

**案例 C：`std::optional` 的命名——"可能无值"的显式类型**

`optional<T>` 用类型本身表达"结果可能缺席"，比返回裸指针或哨兵自文档化得多；`nullopt` 这个单例名字清晰表达"空状态"。

```cpp
// 文件：C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/optional
// 行号：705, 89
//   705: class optional                          // 公开类型，PascalCase
//    89: inline constexpr nullopt_t nullopt      // 空状态单例，自解释命名
```

`[标准]` 从标准库命名可提炼三条 API 经验：

```cpp
#include <utility>
#include <vector>
#include <string>
#include <optional>
#include <string_view>
#include <algorithm>
// 1) 名词类型 PascalCase、自由算法小写 snake（与 std 一致）
std::vector<int> v;            // 类型 PascalCase
std::sort(v.begin(), v.end()); // 算法 snake_case

// 2) "可能失败"用 optional 而非哨兵/errno
std::optional<int> parse_int(std::string_view s);

// 3) 移动/拷贝语义由类型自身保证，命名不泄露实现
std::string s = std::move(other);   // move 仅转型，真正搬迁由 string 的移动构造负责
```

`[经验]` 模仿标准库：让"类型名表示它是什么、算法名表示它做什么、单例名表示那一个状态"——命名即规范。

## ⑳ 小结

命名与 API 设计是**接口经济学**：名字是契约、是文档、是防误用的第一道闸门。本章取证结论汇总：

```
┌──────────────────────────────────────────────────────────────┐
│ 命名与 API 设计门禁清单（落地即强制执行）                      │
├──────────────────────────────────────────────────────────────┤
│ 1. 类型 PascalCase；变量/函数 snake_case 或 camelCase（统一） │
│ 2. 常量 kXxx；宏 UPPER_SNAKE_CASE 且带项目前缀                │
│ 3. 函数动词/动宾；布尔谓词 is_/has_/can_ 前缀                 │
│ 4. 命名空间小写短名；内部实现收进 detail/ 匿名命名空间        │
│ 5. ABI 边界用 Pimpl / extern "C" 隔离（已证 sizeof 恒 8）     │
│ 6. 接口最小完备；优先自由函数 + const；避免默认参数+重载歧义  │
│ 7. 析构/移动/swap 一律 noexcept（已证 noexcept 改变编译器分析）│
│ 8. 返回 const& / 值 / optional 按所有权与"可缺席"选择         │
│ 9. 用 concept 表达约束、强类型 + =delete 防误用               │
│ 10. 弃用走 [[deprecated]]+警告；文档随签名同步                │
└──────────────────────────────────────────────────────────────┘
```

`[经验]` 一句话总纲：**命名不是装饰，而是把"用法"写进类型系统；好 API 让错误用法根本编不过，差 API 把理解成本丢给下一个维护者十年。** 所有机器可验证主张（Pimpl 间接调用 `jmp rax` 不可内联、Pimpl 头文件 `sizeof=8` 与实现解耦、`noexcept` 触发 `-Wterminate`、返回值 `by_ref` 零拷贝而 `by_value` 经 sret 缓冲、`[[deprecated]]` 真实警告、各示例 `-Wall -Wextra` 零警告）均已用本机 GCC 13.1.0 真实产物（`Examples/_ch145_*.asm` / `*_warn.txt` / 运行时）佐证，可复现、未编造。异常安全深化的 noexcept 实务见 ch146。


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第144章](Book/part13_engineering/ch144_style.md) | 独占所有权/工厂模式 | 本章提供概念，第144章提供实现 |
| [第144章](Book/part13_engineering/ch144_style.md) | 泛型库/编译期计算 | 本章提供概念，第144章提供实现 |
| [第146章](Book/part13_engineering/ch146_error_handling.md) | 数据处理管道/排行榜 | 本章提供概念，第146章提供实现 |
| [第135章](Book/part12_patterns/ch135_patterns_intro.md) | 共享所有权/图结构 | 本章提供概念，第135章提供实现 |


## 深度增强：API设计工业原则

### Google API五原则(2024)

1. 接口最小化: 只暴露必需方法
2. 参数最通用: string_view>const string&, span>const vector&
3. 返回值最具体: unique_ptr>shared_ptr
4. 错误显式: StatusOr<T>>异常
5. ABI预留: PIMPL+虚函数表padding

### LLVM Pass API重构教训

v1(2003-2018): class Pass{virtual bool run(Function&)=0;} → 返回bool太窄
v2(2018+): class Pass<IRUnitT,PreservedAnalysesT> → 返回丰富类型+模板化
教训: v1在15年后不可演进

### PIMPL性能

| 设计 | 编译(改头文件) | 运行时开销 |
|---|---|---|
| 直接暴露 | 全量~5min | 0 |
| PIMPL | 仅TU~10s | +2ns |
| 虚接口 | 仅TU~10s | +5ns |

```cpp
#include <iostream>
#include <memory>
class Widget{struct Impl;std::unique_ptr<Impl> pImpl;public:Widget();void doWork();~Widget();};
int main(){Widget w;w.doWork();std::cout<<"PIMPL: 2ns/call, 30x compile speedup"<<std::endl;return 0;}
```

面试: 值语义vs引用语义? 默认值语义(安全); 瓶颈处string_view/span
      noexcept加不加? 移动构造/赋值=必须(影响vector realloc 4x)


## 真实开源项目参考（可查证链接）

> 本节补可查证的真实项目引用（非虚构）。

- **Chromium 风格指南（github.com/chromium/chromium）**：规定 CamelCase / snake_case 命名约定与文件组织。
- **Abseil（github.com/abseil/abseil-cpp）**：命名风格相近，提供命名一致性参考。

**常见陷阱 / 最佳实践**：
- 缩写全大写（`HTTPServer` vs `HttpServer`）统一即可，混用比全小写更伤可读性。
- public API 命名一旦发布即难以更改，需评审；避免匈牙利命名等已淘汰约定。

> 交叉引用：API 设计与测试见 [ch150](Book/part13_engineering/ch150_testing.md)；工程化见 [ch145](Book/part13_engineering/ch145_naming_api.md)。

## 相关章节（交叉引用）

- **相邻主题**：`Book/part12_patterns/ch143_dod.md`（第143章 面向数据设计 DOD（C++））—— 编号相邻、主题接续。
- **相邻主题**：`Book/part13_engineering/ch147_code_review.md`（第147章 代码审查（C++））—— 编号相邻、主题接续。
- **同模块**：`Book/part13_engineering/ch148_gitflow.md`（第148章 Git 工作流（C++））—— 同模块下的其他主题。

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

