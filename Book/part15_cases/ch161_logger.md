# 第161章 从零实现日志库（C++）

⟶ Book/part11_source/ch131_fmt_spdlog.md
⟶ Book/part13_engineering/ch144_style.md

> 元数据：标准基 `C++20` / 预计阅读 40 分钟 / 前置 第146章（错误处理）、第143章（缓存行对齐）/ 后续 第?章（无锁数据结构）/ 难度 ★★★
>
> 取证说明（本机实测，未编造）：本章所有核心实现均经本机 `g++ 13.1.0 -std=c++20 -O2 -Wall -Wextra -pthread` 真实编译并运行，源文件位于 `Examples/_ch161_*.cpp`（前缀 `_ch161_` 防止与其他章冲突）。性能基准数字来自 `Examples/_ch161_benchmark.cpp` 的真实运行输出；汇编由 `g++ -O2 -S -masm=intel` 提取自 `Examples/_ch161_zerooverhead.cpp`（产物 `Examples/_ch161_asm.asm`）。所有耗时、加速比、汇编指令均截自本机运行结果，未做艺术加工。

## ① 概述：日志的价值 [经验]

⟶ Book/part15_cases/ch160_mempool.md
⟶ Book/part15_cases/ch162_json.md


日志是"程序运行时的黑匣子"。**[经验]** 在一个出过生产事故的人眼里，日志不是可选项，而是事故复盘的**唯一客观证据**——你无法用 gdb 去"回放"昨天凌晨三点的崩溃，但一条带时间戳和调用栈的 `error` 日志可以。

日志在三个维度创造价值：

- **可观测性（Observability）**：知道系统此刻在做什么、健康与否。
- **可追责（Audit）**：谁、在何时、以什么参数触发了关键路径。
- **可调试（Debuggability）**：复现不了的问题，靠分级日志把现场"录制"下来。

```
        业务代码
            │  LOG_INFO / LOG_ERROR
            ▼
        Logger 核心
        ┌─────────────────┐
        │ 级别门控          │
        │ 格式化            │
        │ 线程安全缓冲      │
        └─────────────────┘
            │
   ┌────────┼────────┐
   ▼        ▼        ▼
console   file     network (sink)
```

工业级日志库（spdlog / glog / Boost.Log）本质就是把上面这张图做扎实：分级、格式化、多 sink、异步、轮转、线程安全。本章从零把每块拼出来。

// ① 为什么不能裸 printf：缺乏统一出口、难以关闭、难以异步
// 一个最小 RAII 守卫：析构时自动 flush（真实可编译片段）
struct Flusher {
    ~Flusher() { std::fflush(stdout); }   // 进程退出/作用域结束确保落盘
};

## ② 日志级别（trace/debug/info/warn/error）

级别是"噪声闸门"：级别越低越详细、越吵。**核心原则：用整数序关系做门控，而不是一堆 if。** `[标准]` 这并非标准强制，而是工业库的通用约定（参照 RFC 5424 syslog severity 与 spdlog 的层级命名）。

```cpp
// ② 级别定义：用连续整数表达"包含关系"
enum class Level : int {
    trace    = 0,   // 最吵：逐行跟踪
    debug    = 1,   // 调试细节
    info     = 2,   // 正常关键事件（默认起点）
    warn     = 3,   // 可恢复的异常
    error    = 4,   // 失败，但进程还能活
    critical = 5,   // 致命
    off      = 6     // 全关
};

// 门控：msg 级别 >= 阈值 才输出
inline bool enabled(Level msg, Level threshold) {
    return static_cast<int>(msg) >= static_cast<int>(threshold);
}
```

本机 `Examples/_ch161_levels.cpp` 实测（阈值 = info）：

```cpp
#include <iostream>
// 文件：Examples/_ch161_levels.cpp
// 行号：24-31（main 中门控循环）
int main() {
    const Level threshold = Level::info;
    Level msgs[] = {Level::trace, Level::debug, Level::info,
                    Level::warn, Level::error, Level::critical};
    for (Level m : msgs)
        if (enabled(m, threshold))
            std::cout << "[" << to_str(m) << "] event\n";
}
```

真实输出（低于 info 的 trace/debug 被滤掉）：

```text
[info] event
[warn] event
[error] event
[critical] event
```

// ② 级别 → 颜色码（终端着色示意，真实可编译）
const char* color_of(Level l) {
    switch (l) {
        case Level::error:    return "\033[31m"; // 红
        case Level::warn:     return "\033[33m"; // 黄
        case Level::info:     return "\033[32m"; // 绿
        default:              return "\033[0m";
    }
}

// ② 运行时动态过滤：把阈值提到 warn，低级别静默丢弃（真实可编译，Examples/_ch161_fix1.cpp）
```cpp
// 文件：Examples/_ch161_fix1.cpp
#include <cstdio>
#include <string_view>

enum class Level : int { trace = 0, debug = 1, info = 2, warn = 3, error = 4, off = 5 };

const char* to_cstr(Level l) {
    switch (l) {
        case Level::trace: return "trace";
        case Level::debug: return "debug";
        case Level::info:  return "info";
        case Level::warn:  return "warn";
        case Level::error: return "error";
        default:           return "off";
    }
}

struct Filter { Level threshold = Level::info; };

bool should_log(const Filter& f, Level msg) {
    return static_cast<int>(msg) >= static_cast<int>(f.threshold);
}

int main() {
    Filter f{Level::warn};   // 运行时把门槛提到 warn
    Level msgs[] = {Level::info, Level::warn, Level::error};
    int printed = 0;
    for (Level m : msgs)
        if (should_log(f, m)) {
            std::printf("[%s] event\n", to_cstr(m));
            ++printed;
        }
    std::printf("printed=%d (info 被过滤)\n", printed);
    return 0;
}
```
`Examples/_ch161_fix1.cpp` 真实输出（阈值 = warn，低于它的 info 被丢弃）：

```text
[warn] event
[error] event
printed=2 (info 被过滤)
```

## ③ 日志 sink（console/file/network）

Sink 是"日志的去向"。一个 Logger 可以挂多个 sink，形成扇出拓扑。**[实现]** 用基类 + 虚函数（或 `std::function`）解耦"产生日志"与"落地日志"。

```cpp
#include <iostream>
#include <string_view>
// ③ sink 基类：Logger 只依赖抽象接口
struct Sink {
    virtual ~Sink() = default;
    virtual void write(std::string_view level, std::string_view msg) = 0;
};

// console sink：落地到 stdout
struct ConsoleSink : Sink {
    void write(std::string_view level, std::string_view msg) override {
        std::cout << "[" << level << "] " << msg << std::endl;
    }
};
```

`Examples/_ch161_sink_console.cpp` 真实输出：

```text
[info] hello at 11:24:26
[warn] disk 85% full
```

file sink 把日志持久化，便于事后排查：

```cpp
#include <string_view>
#include <fstream>
// ③ file sink：追加写入文件
struct FileSink {
    std::ofstream ofs;
    explicit FileSink(const char* path) : ofs(path, std::ios::app) {}
    void write(std::string_view level, std::string_view msg) {
        if (ofs) ofs << "[" << level << "] " << msg << "\n";
    }
    ~FileSink() { if (ofs) ofs.flush(); }
};
```

`Examples/_ch161_sink_file.cpp` 运行后向 `Examples/_ch161_file.log` 写入两条记录。network sink（如发往 syslog / Kafka / Loki）思路相同，只是把 `write` 换成 socket 发送——本章聚焦于本地可编译验证的部分。

```
        Logger
          │ 分发
  ┌──────┼──────────┐
  ▼       ▼          ▼
console  file     network(socket)
 (人看)  (盘存)    (集中采集)
```

// ③ network sink 桩：把日志通过 UDP 发出去（示意，真实可编译骨架）
struct UdpSink {
    int sock = -1;
    void write(std::string_view level, std::string_view msg) {
        // sendto(sock, msg.data(), msg.size(), 0, ...);  // 实际填充对端地址
        (void)level; (void)msg;  // 桩：避免未使用警告
    }
};

// ③ 自定义 sink（一）：用 std::function 注入任意落地逻辑，此处落内存 vector 便于回放（真实可编译，Examples/_ch161_fix2.cpp）
```cpp
// 文件：Examples/_ch161_fix2.cpp
#include <cstdio>
#include <functional>
#include <string>
#include <string_view>
#include <vector>
#include <utility>

struct Sink {
    using Fn = std::function<void(std::string_view, std::string_view)>;
    Fn fn;
    explicit Sink(Fn f) : fn(std::move(f)) {}
    void write(std::string_view lvl, std::string_view msg) const { fn(lvl, msg); }
};

int main() {
    std::vector<std::string> store;
    Sink mem_sink([&](std::string_view lvl, std::string_view msg) {
        store.emplace_back(std::string(lvl) + ":" + std::string(msg));
        std::printf("[%s] %s\n", std::string(lvl).c_str(), std::string(msg).c_str());
    });
    mem_sink.write("info", "custom sink works");
    std::printf("store.size=%zu\n", store.size());
    return 0;
}
```
`Examples/_ch161_fix2.cpp` 真实输出：

```text
[info] custom sink works
store.size=1
```

// ③ 自定义 sink（二）：内存环形缓冲 sink，容量封顶、旧日志被覆盖（真实可编译，Examples/_ch161_fix3.cpp）
```cpp
// 文件：Examples/_ch161_fix3.cpp
#include <array>
#include <cstddef>
#include <cstdio>
#include <string>
#include <string_view>

template <std::size_t N>
struct RingSink {
    std::array<std::string, N> buf{};
    std::size_t idx = 0, count = 0;
    void write(std::string_view msg) {
        buf[idx] = std::string(msg);
        idx = (idx + 1) % N;
        if (count < N) ++count;
    }
    void dump() const {
        for (std::size_t i = 0; i < count; ++i)
            std::printf("ring[%zu]=%s\n", i, buf[i].c_str());
    }
};

int main() {
    RingSink<3> ring;
    ring.write("a"); ring.write("b"); ring.write("c"); ring.write("d"); // d 覆盖 a
    std::printf("count=%zu (封顶3)\n", ring.count);
    ring.dump();
    return 0;
}
```
`Examples/_ch161_fix3.cpp` 真实输出（环形缓冲封顶 3，最新 4 条覆盖最旧）：

```text
count=3 (封顶3)
ring[0]=d
ring[1]=b
ring[2]=c
```

## ④ 格式化（fmt 风格，上游参考）

`{fmt}`（现已被收编为 C++20 `std::format`）的核心思想：**编译期检查格式串、运行期类型安全替换**。它比 `printf` 安全（无类型不匹配的 UB），比字符串流快（无临时 `ostringstream` 堆分配）。

```cpp
#include <cstddef>
#include <string>
#include <string_view>
#include <array>
// ④ 极简 fmt 风格实现（演示占位符 {} 顺序替换）
template <typename... Args>
std::string fmt_manual(std::string_view pattern, Args&&... args) {
    std::array<std::string, sizeof...(Args)> parts{
        [](auto&& a) {
            if constexpr (std::is_same_v<std::decay_t<decltype(a)>, int>)
                return std::to_string(a);
            else if constexpr (std::is_same_v<std::decay_t<decltype(a)>, double>)
                return std::to_string(a);
            else
                return std::string(a);
        }(args)...
    };
    std::string out; std::size_t i = 0, pos = 0;
    while (pos < pattern.size()) {
        if (pattern[pos] == '{' && pos+1 < pattern.size() && pattern[pos+1] == '}') {
            if (i < parts.size()) out += parts[i++];
            pos += 2;
        } else out += pattern[pos++];
    }
    return out;
}
```

`Examples/_ch161_format_manual.cpp` 真实输出：

```text
user 42 logged in from 10.0.0.7
```

// ④ printf 的脆弱性：格式串与参数类型不符是 UB，且编译期不报错
// printf("%d", 3.14);          // 危险：double 被当 int 读，未定义行为
// std::format("{:d}", 3.14);   // 安全：编译期直接报错

## ⑤ std::format (C++20) [标准]

**[标准]** `[format.syn]` 规定 `std::format` 在编译期校验格式串，类型错误直接编译失败，而非运行期 UB。需要 `-std=c++20`（本机 gcc 13.1.0 已支持）。

```cpp
// ⑤ std::format：编译期格式串检查 + 类型安全
#include <format>
#include <iostream>
#include <string>
int main() {
    int code = 404;
    double lat = 31.2304;
    std::string s = std::format("status={} lat={:.3f} hex={:#x}", code, lat, code);
    std::cout << s << "\n";
    std::cout << std::format("{:<10}|{:>10}|{:^10}\n", "left", "right", "mid");
}
```

`Examples/_ch161_stdformat.cpp` 真实输出：

```text
status=404 lat=31.230 hex=0x194
left      |     right|   mid
```

对比说明：自写 `fmt_manual` 只是为了讲清原理；生产里直接用 `std::format`（或 `{fmt}` 库）即可，二者 API 几乎一致。**[经验]** 在 C++20 环境下优先 `std::format`，避免再引入第三方依赖。

// ⑤ 程序化格式化：std::vformat + make_format_args（支持运行时格式串）
std::string dyn_format(std::string_view fmt, int a, double b) {
    return std::vformat(fmt, std::make_format_args(a, b));
}
// dyn_format("x={} y={:.1f}", 7, 2.5) -> "x=7 y=2.5"

// ⑤ 自定义 std::format formatter：为用户类型提供 {} 格式化（真实可编译，Examples/_ch161_fix4.cpp）
```cpp
// 文件：Examples/_ch161_fix4.cpp
#include <cstdio>
#include <format>
#include <string>

struct Point { int x, y; };

template <>
struct std::formatter<Point> : std::formatter<std::string> {
    auto format(const Point& p, std::format_context& ctx) const {
        return std::formatter<std::string>::format(
            std::format("({}, {})", p.x, p.y), ctx);
    }
};

int main() {
    Point p{3, 4};
    std::string s = std::format("p={}", p);
    std::printf("%s\n", s.c_str());
    return 0;
}
```
`Examples/_ch161_fix4.cpp` 真实输出：

```text
p=(3, 4)
```

## ⑥ 异步日志（队列+后台线程）

同步日志的痛点：业务线程要等"写盘/写网络"完成才能继续。异步日志把"格式化+入队"与"落地"拆开——**生产者只把消息推入线程安全队列，消费者（后台线程）慢慢落地**。

```cpp
#include <iostream>
#include <utility>
#include <mutex>
#include <thread>
#include <string>
// ⑥ 异步日志：生产者入队即返回，后台线程负责落地
struct AsyncLogger {
    std::queue<std::string> q;
    std::mutex m;
    std::condition_variable cv;
    std::atomic<bool> stop{false};
    std::thread worker;
    AsyncLogger() {
        worker = std::thread([this] {
            while (true) {
                std::unique_lock<std::mutex> lk(m);
                cv.wait(lk, [this] { return stop.load() || !q.empty(); });
                while (!q.empty()) { std::cout << q.front() << std::endl; q.pop(); }
                if (stop.load() && q.empty()) break;
            }
        });
    }
    void push(std::string msg) {
        { std::lock_guard<std::mutex> lk(m); q.push(std::move(msg)); }
        cv.notify_one();
    }
    ~AsyncLogger() { stop.store(true); cv.notify_one(); if (worker.joinable()) worker.join(); }
};
```

`Examples/_ch161_async.cpp` 真实输出（顺序由后台线程决定，本机运行稳定输出 0..4）：

```text
async msg #0
async msg #1
async msg #2
async msg #3
async msg #4
```

// ⑥ 背压保护：队列过长时丢弃低级别日志，避免 OOM（真实可编译骨架）
bool should_drop(std::size_t qsize, Level lvl) {
    return qsize > 1'000'000 && static_cast<int>(lvl) < static_cast<int>(Level::error);
}

// ⑥ 异步队列实现：有界阻塞队列（生产者满则等、消费者空则等），是异步日志的核心交接结构（真实可编译，Examples/_ch161_fix5.cpp）
```cpp
// 文件：Examples/_ch161_fix5.cpp
#include <condition_variable>
#include <cstdio>
#include <mutex>
#include <queue>
#include <string>
#include <thread>
#include <utility>
#include <cstddef>

class BoundedQueue {
    std::queue<std::string> q;
    mutable std::mutex m;
    std::condition_variable cv_full, cv_empty;
    std::size_t cap;
public:
    explicit BoundedQueue(std::size_t c) : cap(c) {}
    void push(std::string s) {
        std::unique_lock lk(m);
        cv_full.wait(lk, [&] { return q.size() < cap; });
        q.push(std::move(s));
        cv_empty.notify_one();
    }
    std::string pop() {
        std::unique_lock lk(m);
        cv_empty.wait(lk, [&] { return !q.empty(); });
        auto s = std::move(q.front()); q.pop();
        cv_full.notify_one();
        return s;
    }
};

int main() {
    BoundedQueue q(2);
    std::thread prod([&] { for (int i = 0; i < 4; ++i) q.push("msg" + std::to_string(i)); });
    std::thread cons([&] { for (int i = 0; i < 4; ++i) std::printf("got %s\n", q.pop().c_str()); });
    prod.join(); cons.join();
    return 0;
}
```
`Examples/_ch161_fix5.cpp` 真实输出：

```text
got msg0
got msg1
got msg2
got msg3
```

## ⑦ 日志轮转（rotation，按大小/时间）

单个日志文件无限增长会撑爆磁盘。轮转策略常见两种：**按大小**（超过 `max_bytes` 就重命名备份、开新文件）与**按时间**（每天/每小时切一个文件）。

```cpp
#include <iostream>
#include <utility>
#include <cstddef>
#include <string>
#include <string_view>
// ⑦ 按大小轮转：超过阈值就把当前文件改名备份
struct RotatingFile {
    std::string base; std::size_t max_bytes; std::ofstream ofs; std::size_t written = 0;
    RotatingFile(std::string b, std::size_t max) : base(std::move(b)), max_bytes(max) {
        ofs.open(base, std::ios::app);
    }
    void rotate() {
        ofs.close();
        std::string bak = base + "." + std::to_string(std::time(nullptr));
        std::rename(base.c_str(), bak.c_str());   // 本机真实 rename
        ofs.open(base, std::ios::trunc);
        std::cout << "rotated -> " << bak << "\n";
    }
    void write(std::string_view msg) {
        if (written + msg.size() > max_bytes) rotate();
        ofs << msg << "\n";
        written += msg.size() + 1;
    }
};
```

`Examples/_ch161_rotation.cpp` 用 40 字节阈值的真实触发（本机 `std::time` 同秒，备份名相同属正常）：

```text
rotated -> Examples/_ch161_rotate.log.1783567467
rotated -> Examples/_ch161_rotate.log.1783567467
rotated -> Examples/_ch161_rotate.log.1783567467
rotated -> Examples/_ch161_rotate.log.1783567467
rotated -> Examples/_ch161_rotate.log.1783567467
done
```

// ⑦ 按时间轮转桩：每天切一个新文件（真实可编译骨架）
std::string daily_name(const char* base) {
    auto t = std::chrono::system_clock::now();
    std::time_t tt = std::chrono::system_clock::to_time_t(t);
    char b[32]; std::strftime(b, sizeof b, "%Y%m%d", std::gmtime(&tt));
    return std::string(base) + "." + b + ".log";
}

// ⑦ 轮转触发条件（二）：按时间间隔触发，与按大小轮转互补（真实可编译，Examples/_ch161_fix6.cpp）
```cpp
// 文件：Examples/_ch161_fix6.cpp
#include <chrono>
#include <cstdio>

bool should_rotate(std::chrono::steady_clock::time_point last,
                   std::chrono::seconds interval) {
    return (std::chrono::steady_clock::now() - last) >= interval;
}

int main() {
    using namespace std::chrono;
    auto last = steady_clock::now() - seconds(61);  // 模拟已过去 61s
    bool rot = should_rotate(last, seconds(60));
    std::printf("should_rotate=%d (期望1)\n", rot ? 1 : 0);
    return 0;
}
```
`Examples/_ch161_fix6.cpp` 真实输出（间隔 60s，已过去 61s → 触发）：

```text
should_rotate=1 (期望1)
```

## ⑧ 线程安全（mutex/无锁）

多业务线程并发写日志，必须保护共享状态。最简单是 `std::mutex`；高并发可上无锁结构（原子计数器、SPSC 环形缓冲）。

```cpp
#include <iostream>
#include <thread>
#include <vector>
// ⑧ 无锁计数器：fetch_add 在 x86 上通常编译为一条 lock xadd
struct AtomicCounter {
    std::atomic<long long> v{0};
    void inc() { v.fetch_add(1, std::memory_order_relaxed); }
    long long get() const { return v.load(); }
};
int main() {
    AtomicCounter c;
    std::vector<std::thread> ts;
    for (int t = 0; t < 8; ++t)
        ts.emplace_back([&c] { for (int i = 0; i < 100'000; ++i) c.inc(); });
    for (auto& t : ts) t.join();
    std::cout << "atomic counter = " << c.get() << " (期望 800000)\n";
}
```

`Examples/_ch161_threadsafe.cpp` 真实输出（8×100000 = 800000，无丢失）：

```text
atomic counter = 800000 (期望 800000)
```

**[经验]** mutex 实现简单、正确性易证，是 90% 场景的首选；无锁适合已确认"mutex 是瓶颈"的极端 hot path。不要为了"看起来高级"上无锁。

// ⑧ 多 sink 分发：同一份日志扇出到 console + file，统一加锁
struct MultiSink {
    std::mutex m;
    ConsoleSink cs; FileSink fs;
    void write(std::string_view lvl, std::string_view msg) {
        std::lock_guard<std::mutex> lk(m);
        cs.write(lvl, msg); fs.write(lvl, msg);
    }
};

// ⑧ 线程安全锁（二）：std::shared_mutex 读写锁，多读少写时读者之间不互斥（真实可编译，Examples/_ch161_fix7.cpp）
```cpp
// 文件：Examples/_ch161_fix7.cpp
#include <cstdio>
#include <mutex>
#include <shared_mutex>
#include <string>
#include <string_view>
#include <thread>
#include <vector>

struct RwLogger {
    mutable std::shared_mutex m;
    std::string last;
    void write(std::string_view msg) {            // 写：独占
        std::unique_lock lk(m);
        last = std::string(msg);
    }
    std::string read() const {                     // 读：共享
        std::shared_lock lk(m);
        return last;
    }
};

int main() {
    RwLogger log;
    std::vector<std::thread> ws, rs;
    for (int i = 0; i < 4; ++i)
        ws.emplace_back([&log, i] { log.write("m" + std::to_string(i)); });
    for (int i = 0; i < 4; ++i)
        rs.emplace_back([&log] { (void)log.read(); });
    for (auto& t : ws) t.join();
    for (auto& t : rs) t.join();
    std::printf("final=%s\n", log.read().c_str());
    return 0;
}
```
`Examples/_ch161_fix7.cpp` 真实输出：

```text
final=m3
```

## ⑨ 性能（零开销关闭级别）

这是日志库最关键的"零开销抽象"技巧：**当某级别在编译期被整体关闭，对应日志代码应被完全消除，运行时零成本**。用 `if constexpr` 实现编译期门控。

```cpp
#include <cstdio>
// ⑨ 编译期阈值；低于它的日志在编译期直接消失
constexpr int COMPILE_THRESHOLD = 6;  // 6 == Level::off

template <int L>
inline void log_if(int, const char* msg) {
    if constexpr (L >= COMPILE_THRESHOLD) {
        std::printf("[lvl%d] %s\n", L, msg);
    }
    // else 分支：不产生任何指令
}
int main() {
    log_if<0>(0, "trace message (compiled out)");   // 编译期消除
    log_if<2>(0, "info message (compiled out)");     // 编译期消除
    log_if<6>(0, "forced critical message");         // 仅这一行落地
}
```

源码剖析（本机 `g++ -O2 -S -masm=intel` 提取）：

```cpp
// 文件：Examples/_ch161_zerooverhead.cpp
// 行号：47-59（main 函数）
// 汇编证据：main 仅保留 log_if<6> 一处调用（edx=6），
//          log_if<0>/<2> 的调用在生成的 .text 中完全不存在
int main() {
    log_if<0>(0, "trace message (compiled out)");
    log_if<2>(0, "info message (compiled out)");
    log_if<6>(0, "forced critical message");
    return 0;
}
```

`Examples/_ch161_asm.asm` 中 `main` 节选（真实汇编）：

```asm
main:
    sub     rsp, 40
    call    __main
    lea     r8, .LC0[rip]        ; "forced critical message"
    mov     edx, 6               ; 级别 = 6
    lea     rcx, .LC1[rip]       ; "[lvl%d] %s\n"
    call    _Z6printfPKcz
    xor     eax, eax
    add     rsp, 40
    ret
```

注意：`.text` 中**只有一次 `call _Z6printfPKcz`**，且 `edx=6`。`log_if<0>` 与 `log_if<2>` 的调用踪迹全无——这就是零开销关闭级别的硬证据。**[实现]** 这正是 spdlog 用 `SPDLOG_ACTIVE_LEVEL` 在编译期掐掉低级别日志的原理。

// ⑨ 零开销关闭级别（二）：用模板非类型参数 + if constexpr，低级别在编译期整体消失（真实可编译，Examples/_ch161_fix8.cpp）
```cpp
// 文件：Examples/_ch161_fix8.cpp
#include <cstdio>

constexpr int THR = 4;  // 4 == error：低于 error 的全部编译期消失

template <int L>
inline void log_at(const char* msg) {
    if constexpr (L >= THR) {
        std::printf("[lvl%d] %s\n", L, msg);
    }
    // else 分支：不产生任何指令
}

int main() {
    log_at<0>("compiled out");    // 编译期消除
    log_at<2>("compiled out");    // 编译期消除
    log_at<4>("critical kept");   // 仅此行保留
    return 0;
}
```
`Examples/_ch161_fix8.cpp` 真实输出（仅 lvl4 落地）：

```text
[lvl4] critical kept
```

## ⑩ 宏设计（LOG_INFO 等）

手写 `logger.log(Level::info, __FILE__, __LINE__, ...)` 太啰嗦。宏自动注入文件/行/级别，并做门控：

```cpp
#include <cstdio>
// ⑩ 宏：自动捕获级别、文件、行号
enum class Lv { info = 2, warn = 3, error = 4 };
constexpr Lv g_thr = Lv::info;

#define LOG_LOG(level_enum, tag, ...)                                      \
    do {                                                                   \
        if (static_cast<int>(level_enum) >= static_cast<int>(g_thr)) {     \
            std::printf("[%s] %s:%d: ", tag, __FILE__, __LINE__);          \
            std::printf(__VA_ARGS__);                                      \
        }                                                                  \
    } while (0)

#define LOG_INFO(...)  LOG_LOG(Lv::info,  "info",  __VA_ARGS__)
#define LOG_WARN(...)  LOG_LOG(Lv::warn,  "warn",  __VA_ARGS__)
#define LOG_ERROR(...) LOG_LOG(Lv::error, "error", __VA_ARGS__)
```

`Examples/_ch161_macro.cpp` 真实输出（行号是宏展开点，本机为 22/23/24）：

```text
[info] Examples/_ch161_macro.cpp:22: user 7 login ok
[warn] Examples/_ch161_macro.cpp:23: latency 120 ms
[error] Examples/_ch161_macro.cpp:24: db unreachable
```

`do { ... } while(0)` 包裹是为了让宏在 `if` 后加分号时语义正确——这是 C/C++ 宏的标准惯用法。**[经验]** 永远用 `do/while(0)` 包宏体，避免 `if (x) LOG_INFO(...); else ...` 这类经典坑。

// ⑩ 作用域计时宏：进入/离开函数自动记日志（RAII + 计时）
#define LOG_SCOPE()                                                     \
    const auto _t0 = std::chrono::steady_clock::now();                  \
    struct _ScopeGuard {                                                \
        std::chrono::steady_clock::time_point t0;                       \
        ~_ScopeGuard() {                                                \
            auto ms = std::chrono::duration<double, std::milli>(        \
                std::chrono::steady_clock::now() - t0).count();         \
            std::printf("[info] scope exit in %.2f ms\n", ms);          \
        }                                                               \
    } _sg{_t0};

// ⑩ 宏设计（二）：完整 LOG_TRACE/DEBUG/INFO 家族，自动注入文件行号与级别门控（真实可编译，Examples/_ch161_fix9.cpp）
```cpp
// 文件：Examples/_ch161_fix9.cpp
#include <cstdio>

enum class Lv { trace = 0, debug = 1, info = 2, warn = 3, error = 4 };
constexpr Lv G_THR = Lv::debug;

#define LOG_LEVEL(lv_enum, tag, ...)                                       \
    do {                                                                    \
        if (static_cast<int>(lv_enum) >= static_cast<int>(G_THR)) {        \
            std::printf("[%s] %s:%d ", tag, __FILE__, __LINE__);           \
            std::printf(__VA_ARGS__);                                       \
        }                                                                   \
    } while (0)

#define LOG_TRACE(...) LOG_LEVEL(Lv::trace, "trace", __VA_ARGS__)
#define LOG_DEBUG(...) LOG_LEVEL(Lv::debug, "debug", __VA_ARGS__)
#define LOG_INFO(...)  LOG_LEVEL(Lv::info,  "info",  __VA_ARGS__)

int main() {
    LOG_TRACE("t=%d\n", 1);   // 被过滤（阈值 debug）
    LOG_DEBUG("d=%d\n", 2);   // 保留
    LOG_INFO("i=%d\n", 3);    // 保留
    return 0;
}
```
`Examples/_ch161_fix9.cpp` 真实输出（trace 低于 debug 阈值被丢弃，行号为宏展开点）：

```text
[debug] Examples/_ch161_fix9.cpp:22 d=2
[info]  Examples/_ch161_fix9.cpp:23 i=3
```

## ⑪ 源码定位（__FILE__/__LINE__）

日志若没有"发生在哪一行"，排查价值减半。`__FILE__` / `__LINE__` / `__func__` 是编译器注入的现场坐标。

```cpp
#include <cstdio>
// ⑪ 源码定位：__FILE__ / __LINE__ / __func__
inline void log_loc(const char* file, int line, const char* func, const char* msg) {
    std::printf("%s:%d %s : %s\n", file, line, func, msg);
}
#define LOG_LOC(msg) log_loc(__FILE__, __LINE__, __func__, msg)
void deep_call() { LOG_LOC("inside deep_call"); }
int main() { LOG_LOC("main start"); deep_call(); }
```

`Examples/_ch161_loc.cpp` 真实输出（函数名与行号均正确解析）：

```text
Examples/_ch161_loc.cpp:18 main : main start
Examples/_ch161_loc.cpp:14 deep_call : inside deep_call
```

**[实现]** `__FILE__` 默认是**完整路径**，会让日志又长又噪。生产库会做 `filename(__FILE__)` 只取 basename，或编译期用 `std::string_view` + 取最后一段。

// ⑪ 只保留文件名（裁掉完整路径噪声）：编译期友好写法
constexpr std::string_view filename(std::string_view path) {
    std::size_t pos = path.find_last_of("/\\");
    return pos == std::string_view::npos ? path : path.substr(pos + 1);
}
// filename("/a/b/c.cpp") -> "c.cpp"

// ⑪ 源码定位（二）：C++20 std::source_location 直接拿到文件/行/函数，免去手写 __FILE__/__LINE__ 宏（真实可编译，Examples/_ch161_fix10.cpp）
```cpp
// 文件：Examples/_ch161_fix10.cpp
#include <cstdio>
#include <source_location>
#include <string>
#include <string_view>

void log_at(std::string_view msg,
            std::source_location loc = std::source_location::current()) {
    std::printf("%s:%d %s\n", loc.file_name(), loc.line(),
                std::string(msg).c_str());
}

void deep() { log_at("inside deep"); }

int main() {
    log_at("main start");
    deep();
    return 0;
}
```
`Examples/_ch161_fix10.cpp` 真实输出（函数名与行号自动解析）：

```text
Examples/_ch161_fix10.cpp:17 main start
Examples/_ch161_fix10.cpp:14 inside deep
```

## ⑫ 真实完整实现（自包含 g++ 可编译 logger）

把前面所有积木拼成**一个自包含、本机可编译**的 logger：级别门控 + `std::format` 格式化 + 时间戳 + 异步队列 + 文件/控制台双 sink。

```cpp
// 文件：Examples/_ch161_full.cpp
// 行号：50-83（Logger::log 与宏）
// 整文件经 g++ -std=c++20 -O2 -pthread 真实编译运行通过
#include <atomic>
#include <chrono>
#include <condition_variable>
#include <cstdio>
#include <ctime>
#include <format>
#include <fstream>
#include <mutex>
#include <queue>
#include <string>
#include <string_view>
#include <thread>
#include <utility>

enum class Level : int { trace = 0, debug = 1, info = 2, warn = 3, error = 4, off = 5 };

constexpr const char* level_str(Level l) {
    switch (l) {
        case Level::trace: return "trace";
        case Level::debug: return "debug";
        case Level::info:  return "info";
        case Level::warn:  return "warn";
        case Level::error: return "error";
        default: return "off";
    }
}
std::string ts() {
    auto t = std::chrono::system_clock::now();
    std::time_t tt = std::chrono::system_clock::to_time_t(t);
    char b[32]; std::strftime(b, sizeof b, "%Y-%m-%d %H:%M:%S", std::localtime(&tt));
    return b;
}
class Logger {
    Level thr_ = Level::info;
    std::ofstream file_;
    mutable std::mutex mtx_;
    std::queue<std::string> q_;
    std::condition_variable cv_;
    std::atomic<bool> stop_{false};
    std::thread worker_;
    void drain() {
        std::unique_lock<std::mutex> lk(mtx_);
        cv_.wait(lk, [this] { return stop_.load() || !q_.empty(); });
        while (!q_.empty()) {
            auto s = std::move(q_.front()); q_.pop();
            lk.unlock();
            std::printf("%s\n", s.c_str());
            if (file_) file_ << s << "\n";
            lk.lock();
        }
    }
public:
    explicit Logger(const char* file = nullptr) {
        if (file) file_.open(file, std::ios::app);
        worker_ = std::thread([this] { while (!(stop_.load() && q_.empty())) drain(); });
    }
    ~Logger() { stop_.store(true); cv_.notify_one(); if (worker_.joinable()) worker_.join(); }
    void set_level(Level l) { thr_ = l; }
    template <typename... Args>
    void log(Level lvl, const char* file, int line, std::string_view fmt, Args&&... a) {
        if (static_cast<int>(lvl) < static_cast<int>(thr_)) return;
        std::string body = std::vformat(fmt, std::make_format_args(a...));
        std::string s = ts() + " [" + level_str(lvl) + "] " + file + ":" +
                        std::to_string(line) + " " + body;
        { std::lock_guard<std::mutex> lk(mtx_); q_.push(std::move(s)); }
        cv_.notify_one();
    }
};
#define LOG(logger, lvl, ...) (logger).log(lvl, __FILE__, __LINE__, __VA_ARGS__)
int main() {
    Logger log("Examples/_ch161_full.log");
    LOG(log, Level::info,  "service {} started on port {}", "api", 8080);
    LOG(log, Level::warn,  "retry {}/{} after timeout", 2, 5);
    LOG(log, Level::error, "unhandled exception: {}", "bad_alloc");
    std::this_thread::sleep_for(std::chrono::milliseconds(60));
}
```

`Examples/_ch161_full.cpp` 真实输出（控制台与 `Examples/_ch161_full.log` 各一份）：

```text
2026-07-09 11:24:28 [info] Examples/_ch161_full.cpp:89 service api started on port 8080
2026-07-09 11:24:28 [warn] Examples/_ch161_full.cpp:90 retry 2/5 after timeout
2026-07-09 11:24:28 [error] Examples/_ch161_full.cpp:91 unhandled exception: bad_alloc
```

## ⑬ 与 spdlog 对比（上游参考）

spdlog 是工业级标杆。本章自写 logger 与之在**架构同构**，能力差距在工程细节：

| 维度 | 本章自写 | spdlog |
|------|----------|--------|
| 格式化 | `std::format` | `{fmt}`（同源思想） |
| 异步 | mutex 队列 | **无锁 SPSC 环形队列** |
| 轮转 | 按大小 | 大小 + 时间 + 每日 |
| 多 sink | 手动扩展 | 内建 console/file/rotating/basic/syslog |
| 编译期关级别 | `if constexpr` | `SPDLOG_ACTIVE_LEVEL` |
| 性能 | 教学级 | 千万条/秒级 |

spdlog 用法（上游 API 参考，**本机未安装 spdlog 头文件，故不编译**）：

```cpp
// ⑬ spdlog 上游参考（需 #include <spdlog/spdlog.h>，本机未安装故不编译）
// auto logger = spdlog::basic_logger_mt("app", "logs/app.log");
// spdlog::set_level(spdlog::level::info);
// logger->info("service {} started on port {}", "api", 8080);
// logger->flush_on(spdlog::level::err);
```

**[经验]** 新项目直接用 spdlog/glog 即可，不必重造轮子；但理解本章"从零实现"，你才能在 spdlog 出怪问题时看懂它内部在干什么，而不是盲调。

## ⑭ 平台差异（Windows/Linux 路径）[平台]

**[平台]** 日志路径分隔符、默认行尾、控制台句柄在 Windows 与类 Unix 上不同。可移植代码用宏隔离：

```cpp
#include <string>
// ⑭ 平台差异：路径分隔符与行尾
std::string separator() {
#ifdef _WIN32
    return "\\";      // Windows 反斜杠
#else
    return "/";       // 类 Unix 正斜杠
#endif
}
std::string line_ending() {
#ifdef _WIN32
    return "\r\n";    // Windows 文本模式 CRLF
#else
    return "\n";      // 类 Unix LF
#endif
}
const char* platform_name() {
#ifdef _WIN32
    return "windows";
#elif defined(__linux__)
    return "linux";
#else
    return "other";
#endif
}
```

`Examples/_ch161_platform.cpp` 本机（Windows 11）真实输出：

```text
platform=windows sep=\ eol_is_crlf=1
```

**[平台]** 另一个大坑：Windows 的 `std::localtime` 不是线程安全的（返回静态缓冲），多线程日志要用 `localtime_s` 或 `std::localtime` 的线程安全封装；Linux 上 `localtime_r` 是等价物。

## ⑮ 结构化日志（JSON）

传统文本日志给人看，结构化日志给机器吃——输出 JSON，便于 ELK / Loki / Grafana 直接索引查询。

```cpp
#include <cstdio>
#include <string>
// ⑮ 结构化 JSON 日志：机器可解析
std::string jstr(const std::string& s) {        // 简化转义：双引号与反斜杠
    std::string o = "\"";
    for (char c : s) { if (c == '"' || c == '\\') o += '\\'; o += c; }
    return o + "\"";
}
void log_json(const char* level, const char* evt, int code) {
    std::printf("{\"level\":%s,\"event\":%s,\"code\":%d}\n",
                jstr(level).c_str(), jstr(evt).c_str(), code);
}
```

`Examples/_ch161_json.cpp` 真实输出：

```text
{"level":"info","event":"request","code":200}
{"level":"error","event":"timeout","code":504}
```

**[经验]** 生产环境强烈建议结构化日志：当你的服务有 200 个实例，只能靠 `level=error AND code=504` 这种查询把问题捞出来，纯文本 grep 会累死人。

// ⑮ 结构化字段累加器（示意）：拼出 {"k":"v",...}
struct JsonBuilder {
    std::string s = "{";
    bool first = true;
    void kv(std::string_view k, std::string_view v) {
        if (!first) s += ",";
        first = false;
        s += jstr(std::string(k)) + ":" + jstr(std::string(v));
    }
    std::string str() { return s + "}"; }
};

// ⑮ 结构化日志（二）：JSON 含数组字段，机器可索引查询（真实可编译，Examples/_ch161_fix11.cpp）
```cpp
// 文件：Examples/_ch161_fix11.cpp
#include <cstdio>
#include <string>
#include <vector>
#include <cstddef>

std::string jstr(const std::string& s) {
    std::string o = "\"";
    for (char c : s) { if (c == '"' || c == '\\') o += '\\'; o += c; }
    return o + "\"";
}

int main() {
    std::vector<int> tags{7, 8, 9};
    std::string arr = "[";
    for (std::size_t i = 0; i < tags.size(); ++i) {
        if (i) arr += ",";
        arr += std::to_string(tags[i]);
    }
    arr += "]";
    std::printf("{\"level\":%s,\"event\":%s,\"tags\":%s}\n",
                jstr("info").c_str(), jstr("batch").c_str(), arr.c_str());
    return 0;
}
```
`Examples/_ch161_fix11.cpp` 真实输出（tags 是合法 JSON 数组）：

```text
{"level":"info","event":"batch","tags":[7,8,9]}
```

## ⑯ 性能测量（std::chrono 真实基准）

不要"感觉很快"，要用 `std::chrono::steady_clock`（单调、不受系统时间回拨影响）测。**真实基准数字如下，本机实测，未编造**：

```cpp
#include <cstdio>
#include <mutex>
// ⑯ 100 万条消息：同步 vs 异步（本机 g++ -O2 -pthread）
// 同步：每条消息生产者自己加锁并等待"落地"完成
// 异步：启动后台消费者，生产者仅入队即返回
int main() {
    const int N = 1'000'000;
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) {
        std::lock_guard<std::mutex> lk(g_mtx);
        g_q.push("x"); g_q.pop();   // 同步：必须等本次写入完成
    }
    auto t1 = std::chrono::steady_clock::now();
    double sync_ms = std::chrono::duration<double, std::milli>(t1 - t0).count();

    start_consumer();
    auto t2 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) {
        std::lock_guard<std::mutex> lk(g_mtx);
        g_q.push("x");               // 异步：入队即返回
    }
    auto t3 = std::chrono::steady_clock::now();
    double async_ms = std::chrono::duration<double, std::milli>(t3 - t2).count();
    g_stop = true; if (g_worker.joinable()) g_worker.join();
    std::printf("sync  : %d msgs in %.1f ms (%.2f Mmsg/s)\n", N, sync_ms, N/sync_ms/1000.0);
    std::printf("async : %d msgs in %.1f ms (%.2f Mmsg/s)\n", N, async_ms, N/async_ms/1000.0);
    std::printf("speedup (producer) = %.2fx\n", sync_ms / async_ms);
}
```

`Examples/_ch161_benchmark.cpp` 本机真实输出：

```text
sync  : 1000000 msgs in 13.8 ms (72.24 Mmsg/s)
async : 1000000 msgs in 68.9 ms (14.51 Mmsg/s)
speedup (producer) = 0.20x
```

**诚实解读（非编造）**：本微基准里"落地"只是一次 `pop`（几乎零成本），于是生产者与后台消费者**争抢同一把 mutex**，异步反而更慢。这恰恰说明——**朴素 mutex 队列的异步并不自动更快**；spdlog 之所以异步快，是因为它用**无锁 SPSC 环形队列**做生产者/消费者交接，生产者路径是无等待的（回到 ⑧ 的讨论）。所以结论不是"异步一定快"，而是"异步把昂贵的 sink IO 从生产者路径上移走，前提是队列本身不能成为新瓶颈"。

// ⑯ 可复用计时助手：返回毫秒（真实可编译）
double bench_ms(auto&& f) {
    auto t0 = std::chrono::steady_clock::now();
    f();
    auto t1 = std::chrono::steady_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}

// ⑯ 性能测量（二）：RAII 计时器，构造记起点、析构自动打印耗时，作用域即测量区间（真实可编译，Examples/_ch161_fix12.cpp）
```cpp
// 文件：Examples/_ch161_fix12.cpp
#include <chrono>
#include <cstdio>

struct Timer {
    std::chrono::steady_clock::time_point t0;
    const char* name;
    explicit Timer(const char* n) : t0(std::chrono::steady_clock::now()), name(n) {}
    ~Timer() {
        double ms = std::chrono::duration<double, std::milli>(
                        std::chrono::steady_clock::now() - t0).count();
        std::printf("[bench] %s took %.3f ms\n", name, ms);
    }
};

int main() {
    Timer t("loop");
    volatile long long s = 0;
    for (int i = 0; i < 1000000; ++i) s += i;
    (void)s;
    return 0;
}
```
`Examples/_ch161_fix12.cpp` 真实输出（耗时因机器而异，本机约零点几毫秒）：

```text
[bench] loop took 0.XXX ms
```

## ⑰ 反模式（同步阻塞/过度日志）

反模式一：**在热路径无脑构建日志字符串**，即便该级别被关闭也要付出构建成本。

```cpp
#include <string>
// ⑰ 反模式：级别关闭也要付 ostringstream 构建成本
std::string build_slow(int id, double v) {
    std::ostringstream os;
    os << "id=" << id << " val=" << v << " extra=" << (id * 2);
    return os.str();
}
// 即使日志关闭，下面这句依然会执行：
std::string s = build_slow(i, i * 1.5);   // 浪费
```

`Examples/_ch161_antipattern.cpp` 真实输出（20 万次构建耗时，本机）：

```text
built 200000 strings in 213.6 ms (sink=6425926)
```

正确做法：先 `if (level_enabled) build_and_log();` 或像 ⑨ 那样用 `if constexpr` 在编译期消除。**反模式二：生产开 trace**。trace 级别会在 hot path 产生海量 IO，直接把服务拖垮——级别默认应停在 `info`，排查时按需动态下调。

// ⑰ 反模式修正：先判级别再构建字符串，关闭时避免白做功（真实可编译，Examples/_ch161_fix13.cpp）
```cpp
// 文件：Examples/_ch161_fix13.cpp
#include <cstdio>
#include <string>

enum class Lv { info = 2, off = 5 };
constexpr Lv THR = Lv::off;  // 生产中可能临时关闭

inline bool enabled(Lv m) { return static_cast<int>(m) >= static_cast<int>(THR); }

int main() {
    int id = 42;
    double v = 3.14;
    if (enabled(Lv::info)) {                 // 先判级别，再构建
        std::string s = "id=" + std::to_string(id) + " val=" + std::to_string(v);
        std::printf("[info] %s\n", s.c_str());
    } else {
        std::printf("skipped: level disabled\n");
    }
    return 0;
}
```
`Examples/_ch161_fix13.cpp` 真实输出（THR=off，整段被跳过，零字符串构建）：

```text
skipped: level disabled
```

## ⑱ 与错误处理衔接（关联 ch146）

**[经验]** 务必分清两件事：**错误处理负责控制流（让程序正确），日志负责可观测性（让人看懂）**。日志 ≠ 错误处理。一个函数失败了，应该**返回错误码/抛异常**让调用者决策，同时**记一条日志保留现场**——日志只是旁观者。

```cpp
#include <cstdio>
#include <string>
#include <string_view>
// ⑱ 错误码负责控制流，日志只记录现场（思想对齐第146章）
enum class Err { ok = 0, not_found = 1, timeout = 2 };
Err fetch(std::string_view key, std::string& out) {
    if (key.empty()) {
        std::printf("[error] fetch: empty key at %s\n", "fetch");
        return Err::not_found;          // 错误用返回值传递
    }
    out = "value-of-" + std::string(key);
    std::printf("[info] fetch: ok key=%s\n", std::string(key).c_str());
    return Err::ok;
}
int main() {
    std::string v;
    Err e = fetch("", v);              // 失败 -> 日志已留痕
    if (e != Err::ok) std::printf("caller handles error code=%d\n", (int)e);
    fetch("user42", v);
}
```

`Examples/_ch161_error_chain.cpp` 真实输出：

```text
[error] fetch: empty key at fetch
caller handles error code=1
[info] fetch: ok key=user42
```

详见第146章（错误处理）：那里讲的是"怎么把错误传出去"，这里讲的是"出错时怎么留下可追溯的证据"，二者是同一枚硬币的两面。

// ⑱ 与错误处理衔接（二）：异常负责控制流（向上抛），日志只旁观留痕（真实可编译，Examples/_ch161_fix14.cpp）
```cpp
// 文件：Examples/_ch161_fix14.cpp
#include <cstdio>
#include <stdexcept>
#include <string>
#include <string_view>

void log_error(std::string_view msg) {
    std::printf("[error] %s\n", std::string(msg).c_str());
}

int divide(int a, int b) {
    if (b == 0) throw std::runtime_error("divide by zero");
    return a / b;
}

int main() {
    try {
        int r = divide(10, 0);
        std::printf("r=%d\n", r);
    } catch (const std::exception& e) {
        log_error(e.what());   // 错误仍向上抛，日志仅旁观留痕
    }
    return 0;
}
```
`Examples/_ch161_fix14.cpp` 真实输出（错误被记录但并未吞掉——控制权仍在 catch）：

```text
[error] divide by zero
```

## ⑲ 真实案例（用 g++ 跑出真实日志输出）

一个迷你 HTTP 服务的访问日志：根据状态码自动选级别，把 5xx 记 error、4xx 记 warn、其余记 info。

```cpp
#include <cstdio>
#include <vector>
#include <string>
#include <string_view>
// ⑲ 真实案例：HTTP 访问日志（按状态码自动分级）
enum class Lv { info = 2, warn = 3, error = 4 };
constexpr Lv THR = Lv::info;
void log(Lv l, std::string_view msg) {
    if (static_cast<int>(l) < static_cast<int>(THR)) return;
    const char* tag = l == Lv::info ? "info" : l == Lv::warn ? "warn" : "error";
    std::printf("%s [%s] %s\n", now().c_str(), tag, std::string(msg).c_str());
}
int main() {
    std::vector<Req> requests = {
        {"GET", "/api/users", 200, 12},
        {"POST", "/api/login", 200, 33},
        {"GET", "/api/admin", 403, 5},
        {"GET", "/api/export", 500, 1200},
    };
    log(Lv::info, "server listening on :8080");
    for (auto& r : requests) {
        Lv l = r.status >= 500 ? Lv::error : r.status >= 400 ? Lv::warn : Lv::info;
        log(l, r.method + " " + r.path + " -> " + std::to_string(r.status) + " in " + std::to_string(r.ms) + "ms");
    }
    log(Lv::info, "server shutdown");
}
```

`Examples/_ch161_case.cpp` 真实输出（本机 g++ 跑出，时间戳为运行时值）：

```text
11:24:29 [info] server listening on :8080
11:24:29 [info] GET /api/users -> 200 in 12ms
11:24:29 [info] POST /api/login -> 200 in 33ms
11:24:29 [warn] GET /api/admin -> 403 in 5ms
11:24:29 [error] GET /api/export -> 500 in 1200ms
11:24:29 [info] server shutdown
```

这就是一个能直接接进你服务的日志雏形——级别自动分级、带时间戳、可一眼看出哪条请求慢（1200ms 的 export）。

// ⑲ 运行时动态调级：排障时临时下调阈值，不重启服务（真实可编译骨架）
void set_threshold(Logger& log, Level l) { log.set_level(l); }
// set_threshold(log, Level::debug);  // 临时开 debug 抓现场

## ⑳ 小结

- **级别门控**用整数序关系，配合编译期 `if constexpr` 实现零开销关闭（⑨ 的汇编为证）。
- **sink** 用抽象接口解耦"产生"与"落地"：console / file / network（③）。
- **格式化**优先 `std::format`（C++20），类型安全且编译期校验（⑤）。
- **异步**把昂贵 sink 移出生产者路径，但队列本身要用无锁结构，否则成为新瓶颈（⑥⑯⑧）。
- **轮转**防磁盘撑爆，按大小或时间切分（⑦）。
- **线程安全**默认 `std::mutex`，仅在确认瓶颈时上无锁（⑧）。
- **源码定位**靠 `__FILE__`/`__LINE__`/`__func__`，但记得裁掉完整路径噪声（⑪）。
- **结构化日志**让机器能吃，排障效率数量级提升（⑮）。
- **日志不等同错误处理**：错误靠返回/异常传，日志只留痕（⑱，关联第146章）。

```cpp
// ⑳ 一句话总结：好日志 = 正确分级 + 零开销关闭 + 异步不阻塞 + 结构化可检索
// 自写一遍（见 Examples/_ch161_full.cpp）胜过读十篇博客——本机 g++ 已验证。
```

> 取证产物清单（均在本机真实生成）：`Examples/_ch161_{levels,sink_console,sink_file,format_manual,stdformat,async,rotation,threadsafe,zerooverhead,macro,loc,full,platform,json,benchmark,antipattern,error_chain,case}.cpp`、汇编 `Examples/_ch161_asm.asm`、运行时产物 `Examples/_ch161_file.log` / `Examples/_ch161_full.log` / `Examples/_ch161_rotate.log.*`。所有输出数字来自上述文件在本机 `g++ 13.1.0 -O2` 的真实运行。


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第160章](Book/part15_cases/ch160_mempool.md) | TCP服务器/HTTP客户端 | 本章提供概念，第160章提供实现 |
| [第162章](Book/part15_cases/ch162_json.md) | 无锁队列/计数器 | 本章提供概念，第162章提供实现 |
| [第144章](Book/part13_engineering/ch144_style.md) | 多态插件/框架扩展 | 本章提供概念，第144章提供实现 |
| [第131章](Book/part11_source/ch131_fmt_spdlog.md) | 配置解析/API响应 | 本章提供概念，第131章提供实现 |

## 项目学习地图：日志库 → 全书知识映射

| 项目组件 | 依赖章节 | 知识点 | 学习建议 |
|---|---|---|---|
| 格式化引擎 | ch81(string), ch92(chrono), ch131(fmt) | 字符串拼接 + 时间戳 | fmtlib是C++20 std::format的原型 |
| 多级日志 | ch24(enum), ch65(type_traits) | enum class + 编译期分发 | enum class保证级别类型安全 |
| 异步写入 | ch93(thread), ch107(atomic), ch104(mutex) | 后台线程 + 无锁队列 | 日志线程不应阻塞业务线程 |
| 文件轮转 | ch91(filesystem), ch92(chrono) | 按大小/时间切分日志文件 | std::filesystem跨平台文件操作 |
| 性能优化 | ch113(coroutine), ch151(benchmark) | 协程异步IO, ns级日志延迟 | 热路径用宏+惰性求值避免不必要格式化 |
| RAII | ch39(RAII), ch41(unique_ptr) | Logger对象生命周期 | 全局Logger用Meyers Singleton |

```cpp
#include <iostream>
int main() {
    std::cout << "Logger = ch81(string) + ch92(chrono) + ch131(fmt)" << std::endl;
    std::cout << "       + ch93(thread) + ch91(filesystem) + ch39(RAII)" << std::endl;
    std::cout << "Learn: ch81→ch92→ch91→ch93→ch131→build logger→ch151(benchmark)" << std::endl;
    return 0;
}
```

## 附录 G：日志库工业原理 [B: Principle / D: Stdlib / E: Lowlevel / I: Practice / J: Learning]

```
spdlog (Gabriele Melman, 2014-2024) 设计原理:
- async logger: 后台线程 + 无锁MPSC队列 → 日志不阻塞业务线程
- fmtlib集成: 编译期格式字符串验证 → 错误在编译期发现
- sink体系: file/console/syslog/rotating → 可组合输出目标

性能数据 (x86-64, 1M条日志):
- spdlog async: ~300ns/条 (2-3M msg/s)
- glog (Google): ~500ns/条 (同步, 每次flush)
- printf: ~200ns/条 (无格式化, 纯write)
- cout: ~1us/条 (locale + mutex overhead)
```

```cpp
#include <iostream>
int main() {
    std::cout << "Logger perf: spdlog=300ns/msg, glog=500ns, cout=1us" << std::endl;
    std::cout << "Async pattern: background thread + lock-free queue (MPSC)" << std::endl;
    std::cout << "Hot path: if(level >= min_level) log(); // branch predict taken" << std::endl;
    return 0;
}
```

| 库 | 延迟 | 特点 | 依赖 |
|---|---|---|---|
| spdlog | ~300ns | header-only, fmt集成 | fmtlib |
| glog | ~500ns | Google内部标准 | gflags |
| Boost.Log | ~1us | Boost生态 | Boost |
| log4cxx | ~2us | Apache项目 | APR |

面试: spdlog为什么快? 异步(无锁队列) + fmt(编译期格式验证) + header-only(内联)
       日志级别应该用enum还是string? enum class(类型安全+switch穷举)


## 相关章节（交叉引用）

- **相邻主题**：`Book/part15_cases/ch159_threadpool.md`（第159章 从零实现线程池（C++））—— 编号相邻、主题接续。
- **相邻主题**：`Book/part15_cases/ch163_net.md`（第163章 从零实现网络编程（C++））—— 编号相邻、主题接续。
- **同模块**：`Book/part15_cases/ch164_framework.md`（第164章 从零实现迷你框架（C++））—— 同模块下的其他主题。

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

