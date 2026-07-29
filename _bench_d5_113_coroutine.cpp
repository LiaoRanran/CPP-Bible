// _bench_d5_113_coroutine.cpp  — C++20 协程帧开销 vs 普通函数 (GCC 15.3.0)
// 对比：普通函数(零开销) vs 协程 co_return(每次调用堆分配协程帧)
// 参数随循环变化，防编译器把整个循环求成常量
#include <iostream>
#include <vector>
#include <chrono>
#include <coroutine>

volatile int64_t g_sink = 0;

struct Task {
    struct promise_type {
        int v = 0;
        auto get_return_object() { return Task{this}; }
        auto initial_suspend() noexcept { return std::suspend_always{}; }
        auto final_suspend() noexcept { return std::suspend_always{}; }
        void return_value(int x) { v = x; }
        void unhandled_exception() { throw; }
    };
    using handle = std::coroutine_handle<promise_type>;
    promise_type* p;
    ~Task() { if (p) handle::from_promise(*p).destroy(); }
};

__attribute__((noinline)) Task coro_sum(int n) {
    int s = 0;
    for (int i = 1; i <= n; ++i) s += i;
    co_return s;
}
__attribute__((noinline)) int plain_sum(int n) {
    int s = 0;
    for (int i = 1; i <= n; ++i) s += i;
    return s;
}
int main() {
    const int N = 200'000;     // 调用次数
    const int R = 5;
    auto med = [](auto f) -> double {
        std::vector<double> t;
        for (int r = 0; r < R; ++r) {
            auto a = std::chrono::steady_clock::now();
            int64_t s = f();
            auto b = std::chrono::steady_clock::now();
            g_sink = s;
            t.push_back(std::chrono::duration<double, std::milli>(b - a).count());
        }
        std::sort(t.begin(), t.end());
        return t[R / 2];
    };
    double t_plain = med([&] {
        int64_t tot = 0;
        for (int k = 0; k < N; ++k) tot += plain_sum((k % 97) + 1);  // 变化参数
        return tot;
    });
    double t_coro = med([&] {
        int64_t tot = 0;
        for (int k = 0; k < N; ++k) {
            Task t = coro_sum((k % 97) + 1);
            tot += t.p->v;
        }
        return tot;
    });
    std::cout << "plain function : " << t_plain << " ms  (baseline)\n";
    std::cout << "coroutine      : " << t_coro  << " ms  (" << t_coro / t_plain << "x)\n";
    std::cout << "coroutine 单次调用 ≈ " << (t_coro / N * 1e6) << " ns/call\n";
    return (int)g_sink;
}
