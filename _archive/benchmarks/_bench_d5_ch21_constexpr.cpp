// _bench_d5_ch21_constexpr.cpp
// 真实基准：constexpr 在「编译期已知实参」下被折叠为零成本 vs 运行期实参下与运行期函数等价
// 编译运行：g++ -O2 -std=c++23 _bench_d5_ch21_constexpr.cpp -o b21 && ./b21
// 注：MinGW 下 long 为 32 位，统一用 long long 计数避免累加溢出（UB）。
#include <iostream>
#include <chrono>
#include <vector>
#include <algorithm>

constexpr long long ct_sum(long long n) { long long s = 0; for (long long i = 0; i < n; ++i) s += i; return s; }
long long rt_sum(long long n)           { long long s = 0; for (long long i = 0; i < n; ++i) s += i; return s; }

static volatile long long sink = 0;

int main() {
    constexpr long long K = 64;
    constexpr long long C = ct_sum(K);            // 编译期折叠为 2016（sum 0..63）
    volatile long long kv = 64;                   // 运行期实参（volatile 防折叠）
    const long long ITERS = 10'000'000LL;
    const int RUNS = 5;

    auto median_constexpr = [&]() {
        std::vector<double> ms(RUNS);
        for (int r = 0; r < RUNS; ++r) {
            auto t0 = std::chrono::steady_clock::now();
            long long s = 0;
            for (long long i = 0; i < ITERS; ++i) s += C;   // 加编译期常数
            auto t1 = std::chrono::steady_clock::now();
            ms[r] = std::chrono::duration<double, std::milli>(t1 - t0).count();
            sink = s;
        }
        std::sort(ms.begin(), ms.end());
        return ms[RUNS / 2];
    };
    auto median_runtime = [&]() {
        std::vector<double> ms(RUNS);
        for (int r = 0; r < RUNS; ++r) {
            auto t0 = std::chrono::steady_clock::now();
            long long s = 0;
            for (long long i = 0; i < ITERS; ++i) s += rt_sum(kv);   // 每次运行期求值
            auto t1 = std::chrono::steady_clock::now();
            ms[r] = std::chrono::duration<double, std::milli>(t1 - t0).count();
            sink = s;
        }
        std::sort(ms.begin(), ms.end());
        return ms[RUNS / 2];
    };
    double a_ms = median_constexpr();
    double b_ms = median_runtime();
    std::cout << "ITERS=" << ITERS << " K=" << K << std::endl;
    std::cout << "constexpr(folded): " << a_ms << " ms" << std::endl;
    std::cout << "runtime(evaluated): " << b_ms << " ms" << std::endl;
    std::cout << "runtime/constexpr=" << (b_ms / a_ms) << std::endl;
    return 0;
}
