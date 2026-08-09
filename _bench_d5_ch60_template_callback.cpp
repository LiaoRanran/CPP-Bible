// _bench_d5_ch60_template_callback.cpp
// D5 角度: 模板回调单态化(内联) vs std::function 类型擦除间接调用
// 实测: AMD Ryzen 9 7940HX, g++ 15.3.0 -O2 -std=c++23
#include <chrono>
#include <cstdio>
#include <functional>
#include <vector>

static volatile long long g_sink = 0;

// ---- A. 模板回调：F 被单态化并内联，无间接调用 ----
template <typename F>
long long run_template(std::vector<int> const& v, F f) {
    long long acc = 0;
    for (int x : v) acc += f(x);
    return acc;
}

// ---- B. std::function 类型擦除：每次调用经间接函数指针间接调用 ----
long long run_stdfunction(std::vector<int> const& v, std::function<int(int)> f) {
    long long acc = 0;
    for (int x : v) acc += f(x);
    return acc;
}

int main() {
    const long long N = 20000000LL;        // 2e7
    std::vector<int> v(N);
    for (long long i = 0; i < N; ++i) v[i] = static_cast<int>(i & 0xFF);

    auto lambda = [](int x) { return x * 3 + 1; };

    double best_t = 1e18, worst_t = 0;
    long long medians[5];
    for (int trial = 0; trial < 5; ++trial) {
        auto t0 = std::chrono::steady_clock::now();
        long long r1 = run_template(v, lambda);
        auto t1 = std::chrono::steady_clock::now();
        long long r2 = run_stdfunction(v, lambda);
        auto t2 = std::chrono::steady_clock::now();
        g_sink = r1 + r2;
        double dt_t = std::chrono::duration<double, std::milli>(t1 - t0).count();
        double dt_s = std::chrono::duration<double, std::milli>(t2 - t1).count();
        if (dt_t < best_t) best_t = dt_t;
        if (dt_t > worst_t) worst_t = dt_t;
        medians[0] = (long long)dt_t;
        medians[1] = (long long)dt_s;
        // 打印每次 trial 的 ms 值，外层脚本取中位
        std::printf("trial %d: template_callback=%.3f ms  std::function=%.3f ms  ratio=%.2fx\n",
                    trial, dt_t, dt_s, dt_s / dt_t);
    }
    // 打印 5 trial 的 template/ms 值（供外层取中位）
    std::printf("SUMMARY template_ms median-of-5-trials\n");
    return 0;
}
