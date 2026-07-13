// ② 微基准 vs 宏基准：微基准只测单个函数，宏基准测真实工作负载
// 见 Examples/_ch151_micro_macro.cpp
#include <cstdio>
#include <vector>
#include <chrono>
#include <numeric>

static long long micro_sum(const std::vector<long long>& v) {  // 微基准对象
    long long s = 0;
    for (auto x : v) s += x;
    return s;
}

int main() {
    std::vector<long long> v(10'000'000);
    std::iota(v.begin(), v.end(), 1);

    // 微基准：只计累加
    auto t0 = std::chrono::steady_clock::now();
    volatile long long r = micro_sum(v);
    auto t1 = std::chrono::steady_clock::now();
    std::printf("micro: sum_ms=%.3f\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count());

    // 宏基准：含真实建表+处理（更接近生产）
    auto t2 = std::chrono::steady_clock::now();
    std::vector<long long> w = v;            // 拷贝（真实 I/O/分配的一部分）
    volatile long long r2 = micro_sum(w);
    (void)r2; (void)r;
    auto t3 = std::chrono::steady_clock::now();
    std::printf("macro: incl_copy_ms=%.3f\n",
                std::chrono::duration<double, std::milli>(t3 - t2).count());
    return 0;
}
