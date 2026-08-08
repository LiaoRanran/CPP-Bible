// _bench_d5_ch120_coroutine.cpp
// D5 基准：协程 vs 回调 vs 线程的任务调度性能
// GCC 15.3.0 -O2 -std=c++23
// AMD Ryzen 9 7940HX, 5 轮取中位, volatile sink

#include <coroutine>
#include <iostream>
#include <chrono>
#include <vector>
#include <thread>
#include <future>
#include <functional>
#include <random>
#include <cstdint>
#include <utility>
#include <exception>

// ============================================================
// Generator 协程框架
// ============================================================
template <typename T>
struct Gen {
    struct promise_type {
        T value_;
        Gen get_return_object() { return Gen{std::coroutine_handle<promise_type>::from_promise(*this)}; }
        std::suspend_always initial_suspend() { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        std::suspend_always yield_value(T v) { value_ = v; return {}; }
        void return_void() {}
        void unhandled_exception() { std::terminate(); }
    };
    using handle = std::coroutine_handle<promise_type>;
    handle h_;
    explicit Gen(handle h) : h_(h) {}
    ~Gen() { if (h_) h_.destroy(); }
    Gen(const Gen&) = delete;
    Gen& operator=(const Gen&) = delete;
    Gen(Gen&& o) noexcept : h_(std::exchange(o.h_, nullptr)) {}
    bool next() { h_.resume(); return !h_.done(); }
    T value() const { return h_.promise().value_; }
};

// Task 协程框架（带 co_await 链）
struct Task {
    struct promise_type {
        Task get_return_object() { return Task{std::coroutine_handle<promise_type>::from_promise(*this)}; }
        std::suspend_always initial_suspend() { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        void return_void() {}
        void unhandled_exception() { std::terminate(); }
    };
    using handle = std::coroutine_handle<promise_type>;
    handle h_;
    explicit Task(handle h) : h_(h) {}
    ~Task() { if (h_) h_.destroy(); }
    Task(const Task&) = delete;
    Task& operator=(const Task&) = delete;
    Task(Task&& o) noexcept : h_(std::exchange(o.h_, nullptr)) {}
    void resume() { if (h_ && !h_.done()) h_.resume(); }
    bool done() const { return !h_ || h_.done(); }
};

// Awaitable：立即恢复（模拟同步 co_await 链）
struct SyncAwait {
    bool await_ready() const noexcept { return false; }
    void await_suspend(std::coroutine_handle<> h) const noexcept { h.resume(); }
    void await_resume() const noexcept {}
};

// ============================================================
// 场景 1：协程 suspend/resume vs 函数调用
// ============================================================

// 协程：每次 yield+resume 一个值
Gen<int> gen_steps(int n) {
    for (int i = 0; i < n; ++i) {
        co_yield i;
    }
}

// 普通函数调用对照（等价逻辑，无协程）
static volatile int g_sink1 = 0;
void func_steps(int n) {
    for (int i = 0; i < n; ++i) {
        g_sink1 = i;
    }
}

double bench_coro_resume(int n) {
    auto t0 = std::chrono::high_resolution_clock::now();
    auto g = gen_steps(n);
    int sum = 0;
    while (g.next()) sum += g.value();
    g_sink1 = sum;
    auto t1 = std::chrono::high_resolution_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}

double bench_func_call(int n) {
    auto t0 = std::chrono::high_resolution_clock::now();
    func_steps(n);
    auto t1 = std::chrono::high_resolution_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}

// ============================================================
// 场景 2：co_await 链 vs 回调嵌套 vs 线程池提交
// ============================================================

// 协程：10 步 co_await 链
Task coro_chain_10() {
    for (int i = 0; i < 10; ++i) {
        co_await SyncAwait{};
    }
}

// 回调嵌套：10 层回调
static volatile int g_sink2 = 0;
void callback_chain_10(int depth, std::function<void()> cb) {
    if (depth <= 0) {
        g_sink2 = 42;
        cb();
        return;
    }
    callback_chain_10(depth - 1, std::move(cb));
}

// 线程池提交（10 个短任务用 std::async）
double bench_coro_chain(int count) {
    auto t0 = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < count; ++i) {
        auto t = coro_chain_10();
        while (!t.done()) t.resume();
    }
    auto t1 = std::chrono::high_resolution_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}

double bench_callback_chain(int count) {
    auto t0 = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < count; ++i) {
        callback_chain_10(10, [](){});
    }
    auto t1 = std::chrono::high_resolution_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}

double bench_thread_pool_submit(int count) {
    auto t0 = std::chrono::high_resolution_clock::now();
    std::vector<std::future<void>> futs;
    futs.reserve(count);
    for (int i = 0; i < count; ++i) {
        futs.push_back(std::async(std::launch::async, []() {
            g_sink2 = 42;
        }));
    }
    for (auto& f : futs) f.wait();
    auto t1 = std::chrono::high_resolution_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}

// ============================================================
// 场景 3：大量短任务：协程 vs std::thread vs std::async
// ============================================================

static volatile int g_sink3 = 0;

Gen<int> coro_short_task(int id) {
    co_yield id;
    co_yield id + 1;
}

double bench_many_coros(int n) {
    auto t0 = std::chrono::high_resolution_clock::now();
    int sum = 0;
    for (int i = 0; i < n; ++i) {
        auto g = coro_short_task(i);
        while (g.next()) sum += g.value();
    }
    g_sink3 = sum;
    auto t1 = std::chrono::high_resolution_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}

double bench_many_threads(int n) {
    auto t0 = std::chrono::high_resolution_clock::now();
    int sum = 0;
    {
        std::vector<std::thread> threads;
        threads.reserve(n);
        for (int i = 0; i < n; ++i) {
            threads.emplace_back([&sum, i]() {
                sum += i + (i + 1);
                g_sink3 = sum;
            });
        }
        for (auto& t : threads) t.join();
    }
    auto t1 = std::chrono::high_resolution_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}

double bench_many_async(int n) {
    auto t0 = std::chrono::high_resolution_clock::now();
    int sum = 0;
    std::vector<std::future<int>> futs;
    futs.reserve(n);
    for (int i = 0; i < n; ++i) {
        futs.push_back(std::async(std::launch::async, [i]() {
            return i + (i + 1);
        }));
    }
    for (auto& f : futs) sum += f.get();
    g_sink3 = sum;
    auto t1 = std::chrono::high_resolution_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}

// ============================================================
// 场景 4：协程帧堆分配 vs 栈分配（await_ready=true elide）
// ============================================================

// 堆分配路径：await_ready=false，每次 co_await 都挂起+恢复
struct HeapAwait {
    bool await_ready() const noexcept { return false; }
    void await_suspend(std::coroutine_handle<> h) const noexcept { h.resume(); }
    int await_resume() const noexcept { return 1; }
};

// 栈分配路径：await_ready=true，编译器可消除帧分配
struct StackAwait {
    bool await_ready() const noexcept { return true; }
    void await_suspend(std::coroutine_handle<>) const noexcept {}
    int await_resume() const noexcept { return 1; }
};

struct HeapTask {
    struct promise_type {
        int result_ = 0;
        HeapTask get_return_object() { return HeapTask{std::coroutine_handle<promise_type>::from_promise(*this)}; }
        std::suspend_always initial_suspend() { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        void return_void() {}
        void unhandled_exception() { std::terminate(); }
    };
    using handle = std::coroutine_handle<promise_type>;
    handle h_;
    explicit HeapTask(handle h) : h_(h) {}
    ~HeapTask() { if (h_) h_.destroy(); }
    HeapTask(const HeapTask&) = delete;
    HeapTask& operator=(const HeapTask&) = delete;
    HeapTask(HeapTask&& o) noexcept : h_(std::exchange(o.h_, nullptr)) {}
    void run() { while (h_ && !h_.done()) h_.resume(); }
};

HeapTask heap_coro(int steps) {
    int sum = 0;
    for (int i = 0; i < steps; ++i) {
        sum += co_await HeapAwait{};
    }
    g_sink3 = sum;
    co_return;
}

HeapTask stack_coro(int steps) {
    int sum = 0;
    for (int i = 0; i < steps; ++i) {
        sum += co_await StackAwait{};
    }
    g_sink3 = sum;
    co_return;
}

double bench_heap_coro(int n) {
    auto t0 = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < n; ++i) {
        auto t = heap_coro(10);
        t.run();
    }
    auto t1 = std::chrono::high_resolution_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}

double bench_stack_coro(int n) {
    auto t0 = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < n; ++i) {
        auto t = stack_coro(10);
        t.run();
    }
    auto t1 = std::chrono::high_resolution_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}

// ============================================================
// 场景 5：generator 协程 vs 传统迭代器
// ============================================================

// 传统迭代器：手写迭代器类
class RangeIter {
    int current_;
    int end_;
public:
    RangeIter(int begin, int end) : current_(begin), end_(end) {}
    bool has_next() const { return current_ < end_; }
    int next() { return current_++; }
    int value() const { return current_; }
};

// 生成器协程版
Gen<int> gen_range(int n) {
    for (int i = 0; i < n; ++i) {
        co_yield i;
    }
}

double bench_gen_coro(int n) {
    auto t0 = std::chrono::high_resolution_clock::now();
    int sum = 0;
    auto g = gen_range(n);
    while (g.next()) sum += g.value();
    g_sink3 = sum;
    auto t1 = std::chrono::high_resolution_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}

double bench_traditional_iter(int n) {
    auto t0 = std::chrono::high_resolution_clock::now();
    int sum = 0;
    RangeIter it(0, n);
    while (it.has_next()) sum += it.next();
    g_sink3 = sum;
    auto t1 = std::chrono::high_resolution_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}

// ============================================================
// 场景 6：协程 vs 线程上下文切换
// ============================================================

// 线程上下文切换基准：两个线程通过 mutex+cv 交替唤醒
#ifdef _WIN32
#include <windows.h>
#else
#include <sched.h>
#endif

double bench_thread_ctx_switch(int switches) {
    auto t0 = std::chrono::high_resolution_clock::now();

    std::atomic<int> turn{0};
    std::atomic<bool> done{false};
    std::atomic<int> counter{0};

    std::thread t1([&]() {
        while (counter.load(std::memory_order_relaxed) < switches) {
            while (turn.load(std::memory_order_relaxed) != 0) {
                // spin-wait
            }
            counter.fetch_add(1, std::memory_order_relaxed);
            turn.store(1, std::memory_order_relaxed);
        }
        done.store(true);
    });

    std::thread t2([&]() {
        while (!done.load(std::memory_order_relaxed)) {
            while (turn.load(std::memory_order_relaxed) != 1) {
                if (done.load(std::memory_order_relaxed)) break;
            }
            turn.store(0, std::memory_order_relaxed);
        }
    });

    t1.join();
    t2.join();

    auto t1_end = std::chrono::high_resolution_clock::now();
    g_sink3 = counter.load();
    return std::chrono::duration<double, std::milli>(t1_end - t0).count();
}

// 协程"切换"：resume 两个协程交替
struct SwitchGen {
    struct promise_type {
        int val_;
        SwitchGen get_return_object() { return SwitchGen{std::coroutine_handle<promise_type>::from_promise(*this)}; }
        std::suspend_always initial_suspend() { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        std::suspend_always yield_value(int v) { val_ = v; return {}; }
        void return_void() {}
        void unhandled_exception() { std::terminate(); }
    };
    using handle = std::coroutine_handle<promise_type>;
    handle h_;
    explicit SwitchGen(handle h) : h_(h) {}
    ~SwitchGen() { if (h_) h_.destroy(); }
    SwitchGen(const SwitchGen&) = delete;
    SwitchGen& operator=(const SwitchGen&) = delete;
    SwitchGen(SwitchGen&& o) noexcept : h_(std::exchange(o.h_, nullptr)) {}
    bool next() { h_.resume(); return !h_.done(); }
    int value() const { return h_.promise().val_; }
};

SwitchGen alt_coro(int id, int steps) {
    for (int i = 0; i < steps; ++i) {
        co_yield id * 1000 + i;
    }
}

double bench_coro_ctx_switch(int switches) {
    auto t0 = std::chrono::high_resolution_clock::now();
    int per = switches / 2;
    auto g1 = alt_coro(1, per);
    auto g2 = alt_coro(2, per);
    int sum = 0;
    bool a = true, b = true;
    while (a || b) {
        if (a) {
            a = g1.next();
            if (a) sum += g1.value();
        }
        if (b) {
            b = g2.next();
            if (b) sum += g2.value();
        }
    }
    g_sink3 = sum;
    auto t1 = std::chrono::high_resolution_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}

// ============================================================
// 工具：取中位数
// ============================================================
double median(std::vector<double>& v) {
    std::sort(v.begin(), v.end());
    return v[v.size() / 2];
}

// ============================================================
// main
// ============================================================
int main() {
    // 运行期随机种子防止常量折叠
    std::random_device rd;
    volatile int seed = rd();

    std::cout << "=== D5 Benchmark: Coroutine vs Callback vs Thread ===" << std::endl;
    std::cout << "GCC 15.3.0, -O2 -std=c++23, AMD Ryzen 9 7940HX" << std::endl;
    std::cout << "seed=" << seed << std::endl;
    std::cout << std::endl;

    // ---- 场景 1: 协程 resume vs 函数调用 ----
    constexpr int N1 = 10'000'000;  // 10M steps
    std::cout << "--- Scene 1: Coroutine resume vs Function call (" << N1 << " steps) ---" << std::endl;
    {
        std::vector<double> coro_times, func_times;
        for (int r = 0; r < 5; ++r) {
            coro_times.push_back(bench_coro_resume(N1));
            func_times.push_back(bench_func_call(N1));
        }
        double cm = median(coro_times), fm = median(func_times);
        std::cout << "  Coroutine resume (10M yield+resume): " << cm << " ms" << std::endl;
        std::cout << "  Function call    (10M iterations) : " << fm << " ms" << std::endl;
        std::cout << "  Coroutine/Function ratio: " << (cm / fm) << "x" << std::endl;
        std::cout << "  Per-resume: " << (cm / N1 * 1000) << " ns, Per-call: " << (fm / N1 * 1000) << " ns" << std::endl;
        // raw
        std::cout << "  [raw coro]";
        for (auto t : coro_times) std::cout << " " << t;
        std::cout << std::endl;
        std::cout << "  [raw func]";
        for (auto t : func_times) std::cout << " " << t;
        std::cout << std::endl;
    }
    std::cout << std::endl;

    // ---- 场景 2: co_await 链 vs 回调嵌套 vs 线程池 ----
    constexpr int N2 = 500'000;
    std::cout << "--- Scene 2: co_await chain vs Callback nesting vs Thread pool (" << N2 << " x 10-step) ---" << std::endl;
    {
        std::vector<double> coro_times, cb_times, tp_times;
        for (int r = 0; r < 5; ++r) {
            coro_times.push_back(bench_coro_chain(N2));
            cb_times.push_back(bench_callback_chain(N2));
        }
        // 线程池只跑 5 轮（每轮 N2/10 个 std::async，避免 500K async 量过大）
        for (int r = 0; r < 5; ++r) {
            tp_times.push_back(bench_thread_pool_submit(N2 / 10));
        }
        double cm = median(coro_times), cbm = median(cb_times), tpm = median(tp_times);
        std::cout << "  Coroutine chain (500K x 10 await): " << cm << " ms" << std::endl;
        std::cout << "  Callback chain  (500K x 10 cb) : " << cbm << " ms" << std::endl;
        std::cout << "  Thread pool     (500K async)   : " << tpm << " ms" << std::endl;
        std::cout << "  Coro/CB ratio: " << (cm / cbm) << "x" << std::endl;
        std::cout << "  Coro/Thread ratio: " << (cm / tpm) << "x" << std::endl;
        std::cout << "  [raw coro]";
        for (auto t : coro_times) std::cout << " " << t;
        std::cout << std::endl;
        std::cout << "  [raw cb]";
        for (auto t : cb_times) std::cout << " " << t;
        std::cout << std::endl;
        std::cout << "  [raw tp]";
        for (auto t : tp_times) std::cout << " " << t;
        std::cout << std::endl;
    }
    std::cout << std::endl;

    // ---- 场景 3: 大量短任务 ----
    constexpr int N3 = 5'000;
    std::cout << "--- Scene 3: Many short tasks (" << N3 << " tasks) ---" << std::endl;
    {
        std::vector<double> coro_times, thread_times, async_times;
        for (int r = 0; r < 5; ++r) {
            coro_times.push_back(bench_many_coros(N3));
        }
        // std::thread 和 std::async 100K 个太多，减少轮数
        for (int r = 0; r < 5; ++r) {
            thread_times.push_back(bench_many_threads(N3));
        }
        for (int r = 0; r < 5; ++r) {
            async_times.push_back(bench_many_async(N3));
        }
        double cm = median(coro_times), tm = median(thread_times), am = median(async_times);
        std::cout << "  Coroutine  (100K x 2-yield): " << cm << " ms" << std::endl;
        std::cout << "  std::thread (100K threads) : " << tm << " ms" << std::endl;
        std::cout << "  std::async  (100K async)   : " << am << " ms" << std::endl;
        std::cout << "  Thread/Coro ratio: " << (tm / cm) << "x" << std::endl;
        std::cout << "  Async/Coro ratio : " << (am / cm) << "x" << std::endl;
        std::cout << "  [raw coro]";
        for (auto t : coro_times) std::cout << " " << t;
        std::cout << std::endl;
        std::cout << "  [raw thread]";
        for (auto t : thread_times) std::cout << " " << t;
        std::cout << std::endl;
        std::cout << "  [raw async]";
        for (auto t : async_times) std::cout << " " << t;
        std::cout << std::endl;
    }
    std::cout << std::endl;

    // ---- 场景 4: 堆分配 vs 栈分配 (await_ready) ----
    constexpr int N4 = 200'000;
    std::cout << "--- Scene 4: Heap alloc (await_ready=false) vs Stack elide (await_ready=true) (" << N4 << " x 10-step) ---" << std::endl;
    {
        std::vector<double> heap_times, stack_times;
        for (int r = 0; r < 5; ++r) {
            heap_times.push_back(bench_heap_coro(N4));
            stack_times.push_back(bench_stack_coro(N4));
        }
        double hm = median(heap_times), sm = median(stack_times);
        std::cout << "  Heap coro  (await_ready=false, 1M x 10): " << hm << " ms" << std::endl;
        std::cout << "  Stack coro (await_ready=true,  1M x 10): " << sm << " ms" << std::endl;
        std::cout << "  Heap/Stack ratio: " << (hm / sm) << "x" << std::endl;
        std::cout << "  [raw heap]";
        for (auto t : heap_times) std::cout << " " << t;
        std::cout << std::endl;
        std::cout << "  [raw stack]";
        for (auto t : stack_times) std::cout << " " << t;
        std::cout << std::endl;
    }
    std::cout << std::endl;

    // ---- 场景 5: generator 协程 vs 传统迭代器 ----
    constexpr int N5 = 10'000'000;
    std::cout << "--- Scene 5: Generator coroutine vs Traditional iterator (" << N5 << " iterations) ---" << std::endl;
    {
        std::vector<double> gen_times, iter_times;
        for (int r = 0; r < 5; ++r) {
            gen_times.push_back(bench_gen_coro(N5));
            iter_times.push_back(bench_traditional_iter(N5));
        }
        double gm = median(gen_times), im = median(iter_times);
        std::cout << "  Generator coroutine (10M yield): " << gm << " ms" << std::endl;
        std::cout << "  Traditional iterator (10M next): " << im << " ms" << std::endl;
        std::cout << "  Gen/Iter ratio: " << (gm / im) << "x" << std::endl;
        std::cout << "  [raw gen]";
        for (auto t : gen_times) std::cout << " " << t;
        std::cout << std::endl;
        std::cout << "  [raw iter]";
        for (auto t : iter_times) std::cout << " " << t;
        std::cout << std::endl;
    }
    std::cout << std::endl;

    // ---- 场景 6: 协程切换 vs 线程切换 ----
    constexpr int N6 = 100'000;
    std::cout << "--- Scene 6: Coroutine switch vs Thread context switch (" << N6 << " switches) ---" << std::endl;
    {
        std::vector<double> coro_times, thread_times;
        for (int r = 0; r < 5; ++r) {
            coro_times.push_back(bench_coro_ctx_switch(N6));
        }
        // 线程切换只跑 5 轮
        for (int r = 0; r < 5; ++r) {
            thread_times.push_back(bench_thread_ctx_switch(N6));
        }
        double cm = median(coro_times), tm = median(thread_times);
        std::cout << "  Coroutine switch (1M resume): " << cm << " ms" << std::endl;
        std::cout << "  Thread switch    (1M ping-pong): " << tm << " ms" << std::endl;
        std::cout << "  Thread/Coro ratio: " << (tm / cm) << "x" << std::endl;
        std::cout << "  Per-coro-switch: " << (cm / N6 * 1000) << " ns" << std::endl;
        std::cout << "  Per-thread-switch: " << (tm / N6 * 1000) << " ns" << std::endl;
        std::cout << "  [raw coro]";
        for (auto t : coro_times) std::cout << " " << t;
        std::cout << std::endl;
        std::cout << "  [raw thread]";
        for (auto t : thread_times) std::cout << " " << t;
        std::cout << std::endl;
    }
    std::cout << std::endl;

    std::cout << "=== Benchmark complete ===" << std::endl;
    std::cout << "volatile sink = " << g_sink1 << " " << g_sink2 << " " << g_sink3 << std::endl;
    return 0;
}
