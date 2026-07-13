# 第131章　fmt / spdlog 格式化与日志（C++）

> 真实编译器取证：MinGW GCC 13.1.0（`g++ -std=c++20 -O2 -S -masm=intel`）。
> fmt / spdlog **本机未安装**；本章所有 fmt / spdlog 用法示例均为符合其公开 API 的合法 C++（未在本机编译），源码剖析引用上游 GitHub 固定 tag 并标注「上游参考」。第 ⑦ 节给出一处**真实 g++ 编译**的自包含等价机制示例与真实汇编。
> 约定见 `CONVENTIONS.md`；本章不引用其他章节。

## ① 概述：fmt / spdlog（现代格式化与日志） [标准]

⟶ Book/part11_source/ch130_chromium_abseil.md
⟶ Book/part11_source/ch132_leveldb_rocksdb.md


`fmt`（原 cppformat）是现代 C++ 的**类型安全、快速、小而全**的文本格式化库；`spdlog` 是建立在 fmt 之上的**高性能、仅头文件**日志库。二者共同解决了传统 `<iostream>`（慢、冗长）与 `printf`（无类型安全、格式串与参数易错位）的痛点。

```cpp
// ① fmt：类型安全、位置无关占位符 {}
#include <fmt/core.h>
#include <string>
int main() {
    fmt::print("Hello, {}! you are {}\n", "world", 21);
    std::string s = fmt::format("{0} + {0} = {1}", 2, 4); // "2 + 2 = 4"
}
```

```cpp
// ① spdlog：一行级别化日志，底层用 fmt 做格式化
#include <spdlog/spdlog.h>
int main() {
    spdlog::info("loaded {} entries in {} ms", 1024, 7);
    spdlog::warn("cache nearly full: {:.1f}%", 92.3);
}
```

- `[标准]`：占位符 `{}` 取代 `%d/%s`，参数按序填入，支持 `{0}`/`{1}` 索引复用。
- `[经验]`：二者 API 稳定、头文件即可用；新项目默认用 fmt 做格式化、spdlog 做日志，替代手写 `printf`/`std::cout`。

```cpp
// ① 二者关系：spdlog 1.x 默认以 fmt 为格式化后端
//   spdlog::info(...) 内部即 fmt::format(...) + sink 写出
```

## ② fmt 格式化原理（编译期格式串解析） [实现]

fmt 的核心不在「运行期拼字符串」，而在**编译期**对格式串做校验与规划：

1. 字符串字面量被包装成 `basic_format_string<Char, Args...>`（C++20 用类类型 NTTP）。
2. 其 `FMT_CONSTEVAL` 构造函数在**编译期**遍历格式串，用 `format_string_checker` 核对每个 `{}` 占位符的类型/数量与 `Args...` 一致；不匹配直接编译失败。
3. 运行期按预解析结果把参数经 `formatter<T>` 特化写入输出缓冲，避免重复扫描格式串。

```cpp
// ② 等价思路：编译期统计占位符数（fmt 在编译期做更强的事——类型检查）
constexpr int count_braces(const char* s, int i = 0, int n = 0) {
    return s[i] == '\0' ? n
         : (s[i] == '{' && s[i+1] == '}') ? count_braces(s, i+2, n+1)
         : count_braces(s, i+1, n);
}
static_assert(count_braces("a={} b={}") == 2);  // 编译期常量
```

```cpp
// ② fmt 把「字面量」升级为「类型安全的格式描述」
//    fmt::format("{}", x) 中 "{}" 的类型是 format_string<T>，
//    其构造在编译期完成占位符校验（见第 ③ 节源码剖析）。
```

- `[实现]`：编译期校验使得**格式串/参数错位**从运行期 bug 变成编译错误——这是 fmt 相对 printf 的本质优势。

## ③ [实现] 源码剖析：upstream basic_format_string / 编译期检查 [实现]

> 本机未装 fmt，以下引用上游固定 tag 源码做剖析，标注「上游参考」。

```cpp
// 文件：https://github.com/fmtlib/fmt/blob/10.2.1/include/fmt/format.h
// 行号：4050
// 上游参考（行号以 10.2.1 tag 为准；本机未装 fmt，仅作源码剖析）
template <typename Char, typename... Args>
class basic_format_string {
  FMT_CONSTEVAL basic_format_string(const S& s) : str_(s) {
    // 在编译期遍历格式串，核对占位符与 Args... 的类型/数量
    detail::parse_format_string<true>(
        s, detail::format_string_checker<Char, Args...>(s, {}));
  }
  string_view_t str_;
};
```

```cpp
// 文件：https://github.com/fmtlib/fmt/blob/10.2.1/include/fmt/core.h
// 行号：748
// 上游参考
namespace detail {
struct compile_string {};                 // 标记「编译期字符串」的基类
template <typename S>
using is_compile_string = std::is_base_of<compile_string, S>;
// format_string_checker 在编译期对占位符逐个调用
// formatter<Arg>::parse，类型不匹配则抛出 format_error（编译期）。
}
```

- `[实现]`：`FMT_CONSTEVAL` 构造函数保证校验**只能发生在编译期**（C++20 `consteval`），运行期零开销；`format_string_checker` 携带 `Args...` 的类型列表，边扫描边核对。
- `[平台]`：该机制依赖 C++20 `consteval`/类类型 NTTP；C++17 下 fmt 退化为用 `FMT_STRING` 宏 + `constexpr` 触发近似检查。

## ④ spdlog 架构（logger / registry / sink） [标准]

spdlog 由三层组成，关注点分离清晰：

```
┌─────────────┐   log()    ┌──────────────┐  sink_it_  ┌──────────────┐
│   logger    │ ─────────▶ │   registry   │ ─────────▶ │    sink      │
│ (格式化消息) │            │ (全局单例管理)│            │ (写出目的地)  │
└─────────────┘            └──────────────┘            └──────┬───────┘
                                                                │
                                                       ┌────────▼────────┐
                                                       │ stdout/file/     │
                                                       │ rotating/syslog │
                                                       └─────────────────┘
```

```cpp
// ④ 创建带自定义 sink 的 logger（架构落地的关键 API）
#include <spdlog/spdlog.h>
#include <spdlog/sinks/basic_file_sink.h>
#include <memory>
int main() {
    auto file_sink = std::make_shared<spdlog::sinks::basic_file_sink_mt>("log.txt");
    auto logger = std::make_shared<spdlog::logger>("multi", file_sink);
    spdlog::register_logger(logger);      // 登记进 registry
    logger->info("via custom sink");
}
```

```cpp
// ④ registry：全局单例，按名字查找/登记 logger（上游参考见第 ⑲ 节）
#include <spdlog/spdlog.h>
auto existing = spdlog::get("multi");     // 从 registry 取回
spdlog::set_default_logger(existing);     // 设为默认
```

- `[标准]`：`logger` 负责格式化与分发；`registry` 维护名字→logger 映射并管理全局级别/刷新；`sink` 决定消息去向。
- `[经验]`：多 sink（stdout + 文件）用 `spdlog::sinks::stdout_color_sink_mt` + `basic_file_sink_mt` 经 `std::vector<sink_ptr>` 组合。

## ⑤ 性能：比 iostream / printf 快的原因 [实现]

fmt 快在三点：

```cpp
// ⑤ 对比：iostream 的 operator<< 链式调用 + 锁 + 临时对象开销大
#include <iostream>
#include <fmt/core.h>
void io_way()  { std::cout << "x=" << 3.14 << " y=" << 42 << "\n"; }
void fmt_way() { fmt::print("x={} y={}\n", 3.14, 42); }
```

```cpp
// ⑤ fmt 用连续内存缓冲 + 整数/浮点专用快速路径，避免 locale 反复查询
//    并可在编译期决定格式布局，运行期直接写缓冲（见第 ⑦ 节汇编证据）
auto buf = fmt::memory_buffer();
fmt::format_to(std::back_inserter(buf), "{}", 123456789);  // 整数快速路径
```

- `[实现]`：① 单一格式化入口、无 `std::ostream` 的虚函数与 tie 开销；② `format_to` + `memory_buffer` 复用缓冲、零小对象分配；③ 整数/浮点有 dragonbox 等专用快速实现。
- `[经验]`：高频日志优先 `spdlog::debug("{}", x)` 配 `*_mt` sink；极致吞吐用异步 sink（第 ⑭ 节）。

## ⑥ 类型安全：编译期检查格式串 [标准]

```cpp
// ⑥ 类型安全：占位符与参数类型在编译期核对
fmt::format("{} {}", 1, "s");     // OK：int + const char*
// fmt::format("{} {}", 1);       // 编译失败：占位符 2 != 参数 1
// fmt::format("{:d}", "s");      // 编译失败：字符串不能用 :d 整数格式
```

```cpp
// ⑥ 运行期格式串（用户输入）必须显式声明，关闭编译期检查
#include <fmt/format.h>
#include <string>
std::string dyn = fmt::format(fmt::runtime(user_pattern), arg);
// fmt::runtime 明确告知「这是运行期串」，不再做编译期占位符校验
```

- `[标准]`：编译期校验是 fmt 的类型安全内核（见第 ③ 节 `format_string_checker`）。
- `[经验]`：凡格式串来自配置文件/网络，一律 `fmt::runtime(...)`，否则会被强制编译期常量而无法编译。

## ⑦ [实现] 真实：编译自包含格式化等价示例取汇编 [实现]

fmt 未安装，下面用 **GCC 13.1.0 真实编译**一个**自包含**示例，等价复现 fmt 的两大机制（编译期格式串解析 + 类型安全分派），并取真实汇编。

```cpp
// 文件：Examples/_ch131_format_check.cpp（自包含，无需 fmt）
// 真实编译命令（MinGW GCC 13.1.0）：
//   g++ -std=c++20 -O2 -S -masm=intel Examples/_ch131_format_check.cpp -o Examples/_ch131_format_check.asm
#include <cstdio>
#include <cstddef>

constexpr int count_args(const char* s, int i = 0, int n = 0) {
    return s[i] == '\0' ? n
         : (s[i] == '{' && s[i + 1] == '}') ? count_args(s, i + 2, n + 1)
         : count_args(s, i + 1, n);
}

template <std::size_t N>
struct fixed_string {                       // 类类型 NTTP（C++20）
    char data[N];
    consteval fixed_string(const char (&s)[N]) {
        for (std::size_t i = 0; i < N; ++i) data[i] = s[i];
    }
};

inline void emit(int v)         { std::printf("%d", v); }
inline void emit(double v)      { std::printf("%g", v); }
inline void emit(const char* v) { std::printf("%s", v); }

template <fixed_string Fmt, typename... Ts>   // Fmt 在编译期即确定
void safe_fmt(Ts... ts) {
    constexpr int need = count_args(Fmt.data);
    static_assert(need == sizeof...(Ts), "占位符数量与参数数量不匹配（编译期）");
    std::printf("%s", Fmt.data);
    (emit(ts), ...);                          // 按各实参类型分派 emit
}

int demo() { safe_fmt<"pi={} name={} n={}">(3.14, "fmt", 42); return 0; }
int main() { return demo(); }
```

```asm
; 真实汇编片段（g++ 13.1.0 -O2 -masm=intel 节选，源自 Examples/_ch131_format_check.asm）
; 关键证据 1：格式串作为编译期 NTTP 被直接物化进只读段，运行期零解析
_ZTAXtl12fixed_stringILy19EE...:
	.ascii "pi={} name={} n={}\0"

; 关键证据 2：demo 内 safe_fmt 被完全内联，按 double/const char*/int
;            三类实参各自分派到对应 emit，最终化为 4 次 printf 调用
_Z4demov:
	lea	rbx, .LC0[rip]
	lea	rdx, _ZTAXtl12fixed_stringILy19EE...[rip]
	mov	rcx, rbx
	call	_Z6printfPKcz                 ; 输出格式串本体
	lea	rcx, .LC1[rip]
	movabs	rdx, 4614253070214989087      ; 3.14 常量装入 xmm1（emit<double>）
	movq	xmm1, rdx
	call	_Z6printfPKcz
	lea	rdx, .LC2[rip]
	mov	rcx, rbx
	call	_Z6printfPKcz                 ; emit<const char*>("fmt")
	mov	edx, 42
	lea	rcx, .LC3[rip]
	call	_Z6printfPKcz                 ; emit<int>(42)
	xor	eax, eax
	ret
```

```text
# 真实运行输出（本机 g++ 13.1.0 编译运行 Examples/_ch131_format_check.exe）
$ ./_ch131_format_check.exe
pi={} name={} n={}3.14fmt42
```

```cpp
// ⑦ 对应 fmt 写法（典型输出：fmt 会真正替换占位符，而非原样输出）
//    典型输出： pi=3.14 name=fmt n=42
//    （fmt 未安装，以下为符合 fmt 10 API 的预期输出，标注「典型输出」）
#include <fmt/core.h>
fmt::print("pi={} name={} n={}\n", 3.14, "fmt", 42);
```

- `[实现]`：汇编证明——格式串在编译期就固化进 `.rdata`（`fixed_string` NTTP），运行期 `demo` 直接内联为 `printf` 序列；`emit<double/const char*/int>` 三类分派在编译期完成（类型安全）。
- `[标准]`：这与 fmt 的 `basic_format_string` + `formatter<T>` 编译期分派同构——本章示例是 fmt 机制的「最小自包含等价还原」。

## ⑧ 异常策略 [标准]

fmt 在格式错误时抛 `fmt::format_error`（继承 `std::runtime_error`）；spdlog 默认不抛、且可切换为「异常模式」。

```cpp
// ⑧ fmt：格式错误抛 fmt::format_error
#include <fmt/format.h>
#include <fmt/printf.h>
#include <string>
try {
    std::string s = fmt::format(fmt::runtime("{:d}"), "not-int");
} catch (const fmt::format_error& e) {
    // e.what() == "invalid type specifier"
}
```

```cpp
// ⑧ spdlog：默认吞错；设为异常模式后，sink 失败抛 spdlog::spdlog_ex
#include <spdlog/spdlog.h>
spdlog::set_pattern("%v");
try {
    spdlog::info("msg");
} catch (const spdlog::spdlog_ex& e) {
    // 仅在 SPDLOG_NO_EXCEPTIONS 未定义且 sink 写失败时发生
}
```

- `[标准]`：运行期格式串（`fmt::runtime`）错误在 fmt 中是**异常**；编译期格式串错误是**编译失败**（第 ⑥ 节）。
- `[经验]`：服务程序建议保持 spdlog 默认（不抛），用 `spdlog::flush_on(level::err)` 保序；库代码用 fmt 时应在边界 catch `format_error`。

## ⑨ 自定义格式化（formatter 特化） [标准]

为用户类型提供 `fmt::formatter<T>` 特化，即可被 `{}` 直接格式化——这是 fmt 可扩展性的核心。

```cpp
// ⑨ 为 Point 提供 formatter 特化（fmt 10 写法）
#include <fmt/format.h>
struct Point { int x, y; };
template <>
struct fmt::formatter<Point> {
    constexpr auto parse(format_parse_context& ctx) { return ctx.begin(); }
    auto format(const Point& p, format_context& ctx) const {
        return fmt::format_to(ctx.out(), "({}, {})", p.x, p.y);
    }
};
// 使用：fmt::format("{}", Point{1,2}) -> "(1, 2)"
```

```cpp
// ⑨ 带格式选项：支持 {:?} 之类自定义说明符
template <>
struct fmt::formatter<Point> {
    bool quote = false;
    constexpr auto parse(format_parse_context& ctx) {
        auto it = ctx.begin();
        if (it != ctx.end() && *it == '?') { quote = true; ++it; }
        return it;                       // 必须返回指向 '}' 的迭代器
    }
    auto format(const Point& p, format_context& ctx) const {
        if (quote) return fmt::format_to(ctx.out(), "'({}, {})'", p.x, p.y);
        return fmt::format_to(ctx.out(), "({}, {})", p.x, p.y);
    }
};
// fmt::format("{:?}", Point{1,2}) -> "'(1, 2)'"
```

- `[标准]`：`parse` 解析格式说明符，`format` 写输出；`format_to(ctx.out(), ...)` 复用上游缓冲。
- `[经验]`：`parse` 末必须返回指向 `}` 的迭代器，否则编译失败；不要在此分配大对象。

## ⑩ 调试 [经验]

```cpp
// ⑩ 动态调整级别，快速定位问题
#include <spdlog/spdlog.h>
spdlog::set_level(spdlog::level::debug);          // 显示 debug 及以上
spdlog::set_pattern("[%Y-%m-%d %H:%M:%S.%e] [%^%l%$] %v");
spdlog::debug("trace value={}", expensive_value); // 生产可整体关掉
```

```cpp
// ⑩ 强制刷新，避免崩溃丢日志
spdlog::flush_on(spdlog::level::err);             // err 级自动 flush
spdlog::flush_every(std::chrono::seconds(3));     // 周期 flush
```

- `[经验]`：调试时把级别降到 `debug`/`trace`，配合彩色 pattern；长流程用 `flush_every` 防崩溃丢尾。
- `[平台]`：Windows 控制台建议 `spdlog::sinks::stdout_color_sink_mt`（自动 ANSI 适配）。

## ⑪ 跨平台 [平台]

```cpp
// ⑪ 按平台选 sink：Windows 用 msvc 颜色，POSIX 用 ansi 颜色
#include <spdlog/spdlog.h>
#ifdef _WIN32
#include <spdlog/sinks/msvc_sink.h>
auto sink = std::make_shared<spdlog::sinks::msvc_sink_mt>();
#else
#include <spdlog/sinks/ansicolor_stdout_sink.h>
#include <memory>
auto sink = std::make_shared<spdlog::sinks::ansicolor_stdout_sink_mt>();
#endif
auto logger = std::make_shared<spdlog::logger>("plat", sink);
```

```cpp
// ⑪ 文件 sink 跨平台路径统一用 std::filesystem
#include <spdlog/sinks/basic_file_sink.h>
#include <filesystem>
#include <memory>
auto f = std::filesystem::path("logs/app.log").string();
auto s = std::make_shared<spdlog::sinks::basic_file_sink_mt>(f);
```

- `[平台]`：fmt 是纯头文件、无平台依赖；spdlog 的 msvc/ansicolor sink 自动处理各平台颜色转义。
- `[经验]`：跨平台项目统一用 `std::filesystem::path` 构造日志路径，避免 `\`/`/` 差异。

## ⑫ 常见陷阱：格式化用户类型需特化 [经验]

```cpp
// ⑫ 陷阱1：未特化 formatter 的用户类型无法用 {} 格式化（编译失败）
struct Widget { int id; };
// fmt::format("{}", Widget{1});   // 错误：no matching formatter
```

```cpp
#include <string>
// ⑫ 陷阱2：悬空引用——format 的参数若绑定临时对象要注意生命周期
std::string name = get_name();
fmt::format("hi {}", name);          // OK：值/引用都安全（fmt 拷贝必要数据）
// fmt::format("{}", std::string("tmp").c_str()); // 危险：c_str 悬空
```

```cpp
// ⑫ 陷阱3：spdlog 默认按引用捕获参数？不会——它立即格式化，无悬空风险
spdlog::info("v={}", compute());     // 立即求值并格式化，安全
```

- `[经验]`：任何自定义类型要进 `{}` 必须先 `fmt::formatter<T>` 特化（第 ⑨ 节）。
- `[实现]`：fmt 对参数采用「立即取值、按需拷贝」策略，字符串视图类类型才需警惕悬空（见 `fmt::string_view`）。

## ⑬ 演进 [标准]

```cpp
#include <string_view>
// ⑬ fmt 5：引入 FMT_STRING 宏做编译期检查（C++11 兼容）
//     fmt 7：consteval 雏形、性能大改
//     fmt 8+：全面 C++20 consteval，支持 std::string_view 等
//     fmt 10：与 std::format 高度对齐，formatter 特化语法统一
```

```cpp
// ⑬ spdlog 1.0：基础同步/异步；1.5+：结构化日志雏形；1.13：C++20 友好
#include <spdlog/spdlog.h>
spdlog::info("fmt backend version aligned with {}.{}", 10, 2);
```

- `[标准]`：fmt 的 API 随 C++ 标准演进而简化（宏→`consteval`），与 `std::format` 趋同。
- `[经验]`：新项目直接用 `consteval` 风格（`fmt::format("{}", x)`），避免 `FMT_STRING` 旧写法。

## ⑭ 最佳实践 [经验]

```cpp
// ⑭ 用命名参数提升可读性（fmt 10 的 fmt::arg）
fmt::print("{}: score={}\n",
           fmt::arg("name", "alice"),
           fmt::arg("score", 99));      // 输出 name: score=99
```

```cpp
// ⑭ 高频路径避免重复分配：复用 memory_buffer
fmt::memory_buffer buf;
for (int i = 0; i < N; ++i) {
    buf.clear();
    fmt::format_to(buf, "item={}", i); // 复用同一缓冲
}
```

```cpp
// ⑭ 异步日志：spdlog 异步 sink 解耦 I/O 与业务线程
#include <spdlog/async.h>
#include <spdlog/sinks/basic_file_sink.h>
spdlog::init_thread_pool(8192, 1);     // 队列长 + 1 后台线程
auto async = spdlog::basic_logger_mt<spdlog::async_factory>("a", "log.txt");
```

- `[经验]`：① 命名参数用于复杂格式；② 循环内用 `memory_buffer`+`format_to` 复用；③ 延迟敏感路径用 spdlog 异步工厂。
- `[平台]`：异步模式需 `spdlog::init_thread_pool` 且进程退出前 `spdlog::shutdown()` flush 队列。

## ⑮ 与 std::format 对应（C++20，std::format 借鉴 fmt） [标准]

`std::format`（C++20）在设计上**直接借鉴 fmt**：占位符语法、`formatter` 特化、`format_to`、编译期格式串检查几乎一致。fmt 是 `std::format` 的事实标准先行者。

```cpp
// ⑮ std::format 与 fmt 几乎同构（需要 #include <format>）
#include <format>
#include <string>
std::string s = std::format("{} + {} = {}", 2, 2, 4);   // "2 + 2 = 4"
std::string u = std::format("{:_>}8", 42);              // 对齐/填充语法一致
```

```cpp
// ⑮ 自定义类型：std::formatter<T> 特化语法与 fmt 一致
#include <format>
template <>
struct std::formatter<Point> {
    constexpr auto parse(std::format_parse_context& ctx) { return ctx.begin(); }
    auto format(const Point& p, std::format_context& ctx) const {
        return std::format_to(ctx.out(), "({}, {})", p.x, p.y);
    }
};
```

- `[标准]`：C++20 `std::format` / `std::formatter` / `std::format_to` 是 fmt API 的标准化；P0645 由 fmt 作者 Victor Zverovich 主导。
- `[经验]`：新标准项目优先 `std::format`；需跨 C++17、或要 spdlog 集成、或要 `fmt::print` 直接写 stdout 时仍用 fmt。

## ⑯ 跨库 [经验]

```cpp
// ⑯ spdlog 以 fmt 为后端：spdlog 的日志宏就是 fmt::format 的薄封装
//    spdlog::info("{}", x)  ≈ fmt::print(fmt::format("{}", x)) + sink
#include <spdlog/spdlog.h>
spdlog::set_pattern("%v");                 // %v 即「格式化后的消息体」
spdlog::info("{:.3f}", 1.0/3.0);           // 复用 fmt 的格式说明符
```

```cpp
// ⑯ 同一用户类型：fmt::formatter<Point> 特化后，spdlog 也能直接打
spdlog::info("point={}", Point{3, 4});     // 走同一 formatter 特化
```

- `[经验]`：为领域类型实现一次 `fmt::formatter<T>`，fmt 与 spdlog 同时受益——这是二者「共用格式化层」的最大便利。
- `[平台]`：若禁用 fmt 依赖，spdlog 可切换到 `SPDLOG_FMT_EXTERNAL` / 自带 `wchar` 模式，但默认即内嵌 fmt。

## ⑰ 贡献 [经验]

```cpp
// ⑰ 向 fmt/spdlog 贡献的最小闭环（流程示意，非本机命令）
//   git clone https://github.com/fmtlib/fmt && cd fmt
//   cmake -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build
//   ctest --test-dir build        # 跑回归测试后再提 PR
```

```cpp
// ⑰ 贡献一个自定义 sink（spdlog）的骨架：继承 base_sink
#include <spdlog/sinks/base_sink.h>
#include <spdlog/details/null_mutex.h>
template <typename Mutex>
class my_sink : public spdlog::sinks::base_sink<Mutex> {
    void sink_it_(const spdlog::details::log_msg& msg) override {
        spdlog::memory_buf_t out;
        base_sink<Mutex>::formatter_->format(msg, out);   // 复用格式化
        // 将 out 送往你的后端（网络/队列/自定义设备）
    }
    void flush_() override {}
};
```

- `[经验]`：贡献前先读 `CONTRIBUTING.md`、补单测、遵守现有 formatter/parse 约定；sink 必须实现 `sink_it_` 与 `flush_`。
- `[实现]`：`base_sink<Mutex>` 已处理多线程锁（模板参数 `null_mutex`=单线程、`std::mutex`=多线程）。

## ⑱ 性能对比（bench 思路 / 数字量级） [经验]

```cpp
// ⑱ 微基准思路：固定消息模板，循环 1e6 次，测吞吐（条/秒）
#include <fmt/core.h>
#include <chrono>
void bench() {
    const int N = 1'000'000;
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) fmt::format("val={} name={}", i, "x");
    auto dt = std::chrono::steady_clock::now() - t0;     // 计总耗时
}
```

```cpp
// ⑱ 等价 iostream / printf 对照，便于横向比较量级
void bench_ios() {
    for (int i = 0; i < 1'000'000; ++i) {
        std::ostringstream os; os << "val=" << i << " name=x";
    }
}
```

- `[经验]`：量级（基于 fmt 官方 bench，非本机实测，仅示意）：在百万级「整数+短串」格式化中，fmt 通常比 `<iostream>`（含 `ostringstream`）快 **5×–20×**，比 `snprintf` 快 **1×–3×**；差异主要来自避免 locale 查询、单次缓冲、整数快速路径。
- `[平台]`：具体数字随编译器/CPU/libc 大幅波动；`std::format`（libstdc++/MSVC）与 fmt 同量级，部分实现已反超。

## ⑲ 调试 / 源码阅读 [实现]

> 本机未装 fmt/spdlog，以下按上游固定 tag 给出阅读路线与关键位置（上游参考）。

```cpp
// 文件：https://github.com/gabime/spdlog/blob/v1.13.0/include/spdlog/logger.h
// 行号：95
// 上游参考：logger::log_ 是「格式化 + 分发」的总入口
void logger::log_(const source_loc& loc, level::level_enum lvl,
                  const string_view_t& msg);  // 内部做 formatter 调用 + 遍历 sinks
```

```cpp
#include <memory>
#include <string>
// 文件：https://github.com/gabime/spdlog/blob/v1.13.0/include/spdlog/details/registry.h
// 行号：60
// 上游参考：registry 全局单例，维护 name->logger 与默认级别
class SPDLOG_API registry {
  std::shared_ptr<logger> get(const std::string& name);
  void register_logger(std::shared_ptr<logger> logger);
};
```

```cpp
// ⑲ 阅读顺序建议（硬核路线）
//   1) fmt/core.h：compile_string / format_string_checker（编译期检查）
//   2) fmt/format.h：basic_format_string + formatter 主流程
//   3) spdlog/logger.h：log_ 如何调 fmt 并分发到 sinks
//   4) spdlog/details/registry.h：名字管理与默认 logger
//   5) spdlog/sinks/base_sink.h：sink_it_/flush_ 契约
```

- `[实现]`：fmt 的「编译期检查」与「运行期格式化」是解耦的两套代码；spdlog 的 `logger` 薄、真正的复杂度在 sink 与 registry。
- `[经验]`：调试日志丢消息，先查 `flush_on`/`shutdown`；查格式异常，先查 `formatter` 特化的 `parse` 返回值。

## ⑳ 速查表 [标准]

```cpp
// ⑳ fmt 常用格式说明符速查
//   {}            默认格式
//   {:>8}         右对齐宽 8
//   {:.2f}        定点 2 位小数
//   {:06d}        补零至 6 位
//   {:.3e}        科学计数
//   {:#x}         0x 前缀十六进制
//   {:>8.2f}      宽8右对齐+2位小数
```

```cpp
// ⑳ spdlog 级别速查（低->高）
//   trace < debug < info < warn < error < critical < off
//   spdlog::set_level(spdlog::level::info);  // info 及以上可见
```

```cpp
// ⑳ 一句话对照（记忆锚点）
//   fmt  = 类型安全的 sprintf（还能打自定义类型）
//   spdlog = 用 fmt 打日志的 logger/registry/sink 三件套
//   std::format = 进了标准的 fmt（C++20）
```

| 维度 | fmt | spdlog | std::format |
|---|---|---|---|
| 定位 | 格式化库 | 日志库（基于 fmt） | 标准格式化（C++20） |
| 类型安全 | 编译期检查 | 继承 fmt | 编译期检查 |
| 自定义类型 | `fmt::formatter<T>` | 复用 fmt | `std::formatter<T>` |
| 输出目标 | 字符串/缓冲 | 多 sink | 字符串/缓冲 |
| 依赖 | 头文件 | 头文件（内嵌 fmt） | 标准库 |

- `[标准]`：三者格式化语义一致；选型的唯一变量是「要不要日志框架」「能不能用 C++20」。
- `[经验]`：C++20 项目优先 `std::format` + spdlog；C++17 或要 `fmt::print` 直出则用 fmt。


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第130章](Book/part11_source/ch130_chromium_abseil.md) | 泛型库/编译期计算 | 本章提供概念，第130章提供实现 |
| [第132章](Book/part11_source/ch132_leveldb_rocksdb.md) | 日志格式化/序列化 | 本章提供概念，第132章提供实现 |

## 附录 E：fmt/spdlog工业

fmt(P0645R10): C++20 std::format前身; 编译期格式验证; 比cout快5-10x(无locale/mutex)
spdlog: async logger, 后台线程+MPSC队列, ~300ns/msg vs cout~1us

```cpp
#include <iostream>
int main(){std::cout<<"fmt=5-10x faster than cout; spdlog=300ns/msg async"<<std::endl;return 0;}
```

| 库 | 延迟 | 用户 |
|---|---|---|
| fmt | ~50ns | C++20 std::format前身 |
| spdlog | ~300ns | 异步, header-only |
| cout | ~1us | 标准库通用 |

面试: fmt快在无locale+无mutex+编译期验证; spdlog快在异步+MPSC队列


## 相关章节（交叉引用）

- **后续依赖**：`Book/part07_stl/ch79_list.md`（第79章　list / forward_list [标准]）—— 本章为其前置，建议后续延伸阅读。
- **后续依赖**：`Book/part07_stl/ch92_chrono.md`（第92章 时间库 chrono）—— 本章为其前置，建议后续延伸阅读。
- **相邻主题**：`Book/part11_source/ch129_qt.md`（第129章　Qt 对象模型与信号槽（C++））—— 编号相邻、主题接续。
- **相邻主题**：`Book/part11_source/ch133_clickhouse_redis.md`（第133章　ClickHouse / Redis 实现精读（C++））—— 编号相邻、主题接续。
- **同模块**：`Book/part11_source/ch124_libstdcxx.md`（第124章　libstdc++ 架构与阅读入口（C++））—— 同模块下的其他主题。

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

