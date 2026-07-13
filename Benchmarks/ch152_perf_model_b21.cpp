// C22 最佳实践3：最小基准框架（warmup + repeat + 中位数），可复用于多函数对比
#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
template <typename F>
double bench_ns(F f, int warmup, int reps) {
    volatile long long sink = 0;
    for (int i = 0; i < warmup; ++i) sink += f();
    std::vector<double> s; s.reserve(reps);
    for (int i = 0; i < reps; ++i) {
        auto t0 = std::chrono::steady_clock::now();
        sink += f();
        auto t1 = std::chrono::steady_clock::now();
        s.push_back(std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count());
    }
    std::sort(s.begin(), s.end());
    return s[s.size() / 2];                          // 返回中位数
}
static long long task_a() { long long s = 0; for (int i = 0; i < 50000; ++i) s += i; return s; }
static long long task_b() { long long s = 0; for (int i = 0; i < 50000; ++i) s += i * 2; return s; }
int main() {
    std::cout << "A=" << bench_ns(task_a, 100, 500) << " ns\n";
    std::cout << "B=" << bench_ns(task_b, 100, 500) << " ns\n";
    return 0;
}