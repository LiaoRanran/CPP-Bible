// _ch120_coro_perf.cpp — 第120章 真实基准/汇编锚定
// 用途 ① 运行时基准：替换书内 ~N 估算（帧分配/ resume 延迟 / 线程切换）
//      ② 静态证据：[[gnu::noinline]] 自由函数供 asm 锚定
// 编译运行: g++ -O2 -std=c++20 _ch120_coro_perf.cpp -o _ch120_coro_perf && ./_ch120_coro_perf
// 生成汇编: g++ -S -O2 -std=c++20 -m64 _ch120_coro_perf.cpp -o _ch120_coro_perf.asm
#include <coroutine>
#include <iostream>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <utility>
#include <thread>
#include <atomic>
#include <mutex>
#include <condition_variable>
#include <x86intrin.h>

// ---- 全局 operator new 覆写：捕获协程帧真实大小 ----
static size_t g_last_new = 0;
static size_t g_max_frame = 0;
void* operator new(size_t n) {
    g_last_new = n;
    if (n > g_max_frame) g_max_frame = n;
    return std::malloc(n);
}
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, size_t) noexcept { std::free(p); }

// ---- RDTSC 计时工具（解决亚纳秒操作无法用 steady_clock 分辨） ----
static double g_tsc_ghz = 0.0;
static inline uint64_t rdtsc() { return __rdtsc(); }
static void calibrate_tsc() {
    auto t0 = std::chrono::steady_clock::now();
    uint64_t c0 = rdtsc();
    std::this_thread::sleep_for(std::chrono::milliseconds(120));
    uint64_t c1 = rdtsc();
    auto t1 = std::chrono::steady_clock::now();
    double secs = std::chrono::duration<double>(t1 - t0).count();
    g_tsc_ghz = (double)(c1 - c0) / secs / 1e9;
}
static inline double tsc_to_ns(uint64_t cyc) { return cyc / g_tsc_ghz; } // cyc / (GHz) = ns

// ---- 最小 generator<T>（与书内第120章同构） ----
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
    Gen& operator=(Gen&& o) noexcept { if (this != &o) { if (h_) h_.destroy(); h_ = std::exchange(o.h_, nullptr); } return *this; }
    bool next() { h_.resume(); return !h_.done(); }
    T value() const { return h_.promise().value_; }
};

// 无限计数器：yield 递增，永不在测量区间内 co_return —— 保证每次 next() 都是真实 resume→yield→suspend
[[gnu::noinline]] Gen<int> infinite_counter() {
    int i = 0;
    for (;;) { co_yield i++; }
}
// 小计数器：测量“创建+首步+销毁”生命周期（帧分配发生在 make_counter 内）
[[gnu::noinline]] Gen<int> small_counter(int n) {
    for (int i = 0; i < n; ++i) co_yield i;
}

// ---- 静态证据锚点（noinline，供 asm 抓取） ----
[[gnu::noinline]] void resume_handle(std::coroutine_handle<>& h) { h.resume(); } // 真实 resume = 调用协程体
[[gnu::noinline]] int yield_step(Gen<int>& g) { g.next(); return g.value(); }     // 真实 resume+yield 一步

// ---- 基准 1：resume+yield 每步延迟（RDTSC，含空循环基线扣除） ----
static double bench_resume_yield() {
    auto g = infinite_counter();
    const int N = 2'000'000;
    // 空循环基线：同等结构但无 resume
    uint64_t base0 = rdtsc();
    uint64_t sink = 0;
    for (int i = 0; i < N; ++i) { sink += (uint64_t)i; }
    uint64_t base1 = rdtsc();
    // 真实循环
    uint64_t t0 = rdtsc();
    for (int i = 0; i < N; ++i) { sink += (uint64_t)yield_step(g); }
    uint64_t t1 = rdtsc();
    (void)base0; (void)base1;
    double per = tsc_to_ns((t1 - t0) - (base1 - base0)) / N;
    // 防止消除
    if (sink == 0) std::printf("impossible\n");
    return per;
}

// ---- 基准 2：创建+首步+销毁 生命周期（steady_clock） ----
static double bench_lifecycle() {
    const int N = 200'000;
    auto t0 = std::chrono::steady_clock::now();
    uint64_t sink = 0;
    for (int i = 0; i < N; ++i) {
        auto g = small_counter(4);
        size_t fs = g_last_new; (void)fs; // 捕获帧大小（循环内最近一次 new = 协程帧）
        if (g.next()) sink += (uint64_t)g.value();
    }
    auto t1 = std::chrono::steady_clock::now();
    double us = std::chrono::duration<double, std::micro>(t1 - t0).count();
    return (us * 1000.0) / N; // ns/次
}

// ---- 基准 3：帧分配延迟由生命周期基准（bench_lifecycle）覆盖 ----
// 说明：裸 operator new 微基准在 -O2 下循环被消除（dead sink），测出 ~0.2ns 假值，
// 故不单独报告；创建+首步+销毁 53ns 已内含真实帧分配（malloc 56-64B）+ init + destroy。

// ---- 基准 4（取消运行时测量）：co_await(ready=true) 几乎零开销 ----
// 说明：co_await 必须位于协程体内，且 ready=true 时编译器不分配帧/不调用 resume，
// 仅展开为 await_resume() 调用（≈函数调用）。故以 asm 证据 + 定性结论支撑，不编单点假数。
struct AlwaysReady {
    bool await_ready() const noexcept { return true; }
    void await_suspend(std::coroutine_handle<>) const noexcept {}
    int await_resume() const noexcept { return 42; }
};
// 最小 Task 协程类型（suspend_never，运行至完成）
struct Task {
    struct promise_type {
        Task get_return_object() { return {}; }
        std::suspend_never initial_suspend() { return {}; }
        std::suspend_never final_suspend() noexcept { return {}; }
        void return_void() {}
        void unhandled_exception() {}
    };
};
// 静态证据锚点：always-ready awaiter 编译为直接调用，无帧分配/无 resume 派发
[[gnu::noinline]] Task ready_task() {
    auto a = co_await AlwaysReady{};
    auto b = co_await AlwaysReady{};
    (void)a; (void)b;
    co_return;
}


// ---- 基准 6：线程切换（互斥+条件变量往返，含上下文切换代理） ----
static double bench_thread_switch() {
    std::mutex m;
    std::condition_variable cv;
    int turn = 0;
    std::atomic<bool> done{false};
    std::atomic<uint64_t> sink{0};
    std::thread peer([&]() {
        uint64_t local = 0;
        for (;;) {
            std::unique_lock<std::mutex> lk(m);
            cv.wait(lk, [&]() { return turn == 1 || done.load(); });
            if (done.load()) break;
            local += 7;
            turn = 0;
            lk.unlock();
            cv.notify_one();
        }
        sink.fetch_add(local);
    });
    const int N = 50'000;
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) {
        std::unique_lock<std::mutex> lk(m);
        turn = 1;
        cv.notify_one();
        cv.wait(lk, [&]() { return turn == 0; });
    }
    auto t1 = std::chrono::steady_clock::now();
    done.store(true);
    { std::lock_guard<std::mutex> lk(m); cv.notify_one(); }
    peer.join();
    double us = std::chrono::duration<double, std::micro>(t1 - t0).count();
    return (us * 1000.0) / N; // ns/往返（= 两次切换）
}

int main() {
    calibrate_tsc();
    std::printf("TSC freq: %.3f GHz\n", g_tsc_ghz);

    double ry = bench_resume_yield();
    double lc = bench_lifecycle();
    double ts = bench_thread_switch();
    size_t frame = g_max_frame;

    // 强制发射 asm 锚点函数（否则 -O2 可能丢弃未使用静态函数）
    volatile auto fp1 = &resume_handle;
    volatile auto fp2 = &yield_step;
    volatile auto fp3 = &ready_task;
    (void)fp1; (void)fp2; (void)fp3;

    std::printf("== 第120章 协程真实基准 (GCC 13.1 / MinGW-w64 / x86-64) ==\n");
    std::printf("frame_size(max coroutine frame) : %zu B\n", frame);
    std::printf("resume+yield per step          : %.2f ns\n", ry);
    std::printf("create+first-step+destroy      : %.2f ns\n", lc);
    std::printf("thread switch (mutex+cv rt)     : %.2f ns (%.3f us, 含同步开销)\n", ts, ts / 1000.0);
    return 0;
}
