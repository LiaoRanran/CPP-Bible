// _bench_d5_ch20_passval.cpp
// 真实基准：大对象按值传递 vs const 引用传递 的调用开销
// 编译运行：g++ -O2 -std=c++23 _bench_d5_ch20_passval.cpp -o b20 && ./b20
#include <iostream>
#include <chrono>
#include <vector>
#include <algorithm>

struct Big { double a[8]; };            // 64 字节
static volatile double sink = 0;

__attribute__((noinline)) double by_value(Big b) {
    double s = 0; for (double x : b.a) s += x; return s;
}
__attribute__((noinline)) double by_cref(const Big& b) {
    double s = 0; for (double x : b.a) s += x; return s;
}

int main() {
    const long N = 20'000'000L;
    const int RUNS = 5;
    Big init; for (int i = 0; i < 8; ++i) init.a[i] = i + 1;

    auto median_value = [&]() {
        std::vector<double> ms(RUNS);
        for (int r = 0; r < RUNS; ++r) {
            auto t0 = std::chrono::steady_clock::now();
            Big b = init;
            double s = 0;
            for (long i = 0; i < N; ++i) {
                b.a[0] = (double)(i & 1023);   // 每轮改变实参 → 强制按值拷贝
                s += by_value(b);
            }
            auto t1 = std::chrono::steady_clock::now();
            ms[r] = std::chrono::duration<double, std::milli>(t1 - t0).count();
            sink = s;
        }
        std::sort(ms.begin(), ms.end());
        return ms[RUNS / 2];
    };
    auto median_cref = [&]() {
        std::vector<double> ms(RUNS);
        for (int r = 0; r < RUNS; ++r) {
            auto t0 = std::chrono::steady_clock::now();
            Big b = init;
            double s = 0;
            for (long i = 0; i < N; ++i) {
                b.a[0] = (double)(i & 1023);   // 与 by_value 路径等代价的前置写入
                s += by_cref(b);
            }
            auto t1 = std::chrono::steady_clock::now();
            ms[r] = std::chrono::duration<double, std::milli>(t1 - t0).count();
            sink = s;
        }
        std::sort(ms.begin(), ms.end());
        return ms[RUNS / 2];
    };
    double v_ms = median_value();
    double r_ms = median_cref();
    std::cout << "N=" << N << std::endl;
    std::cout << "by_value: " << v_ms << " ms" << std::endl;
    std::cout << "by_cref : " << r_ms << " ms" << std::endl;
    std::cout << "value/cref=" << (v_ms / r_ms) << std::endl;
    return 0;
}
