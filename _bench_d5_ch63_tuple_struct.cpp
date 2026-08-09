// _bench_d5_ch63_tuple_struct.cpp
// 真实基准：std::tuple 字段访问 vs 等价 struct 字段访问（-O2 下开销对比）
// 编译运行：g++ -O2 -std=c++23 _bench_d5_ch63_tuple_struct.cpp -o b63 && ./b63
#include <iostream>
#include <chrono>
#include <vector>
#include <algorithm>
#include <tuple>

struct Rec { double x, y, z, w; };
static volatile double sink = 0;

__attribute__((noinline)) double sum_struct(const Rec& r) {
    return r.x + r.y + r.z + r.w;
}
__attribute__((noinline)) double sum_tuple(const std::tuple<double,double,double,double>& t) {
    return std::get<0>(t) + std::get<1>(t) + std::get<2>(t) + std::get<3>(t);
}

int main() {
    const long N = 100'000'000L;
    const int RUNS = 5;
    Rec r{1, 2, 3, 4};
    std::tuple<double,double,double,double> t{1, 2, 3, 4};

    auto median_struct = [&]() {
        std::vector<double> ms(RUNS);
        for (int k = 0; k < RUNS; ++k) {
            auto t0 = std::chrono::steady_clock::now();
            double s = 0;
            for (long i = 0; i < N; ++i) s += sum_struct(r);
            auto t1 = std::chrono::steady_clock::now();
            ms[k] = std::chrono::duration<double, std::milli>(t1 - t0).count();
            sink = s;
        }
        std::sort(ms.begin(), ms.end());
        return ms[RUNS / 2];
    };
    auto median_tuple = [&]() {
        std::vector<double> ms(RUNS);
        for (int k = 0; k < RUNS; ++k) {
            auto t0 = std::chrono::steady_clock::now();
            double s = 0;
            for (long i = 0; i < N; ++i) s += sum_tuple(t);
            auto t1 = std::chrono::steady_clock::now();
            ms[k] = std::chrono::duration<double, std::milli>(t1 - t0).count();
            sink = s;
        }
        std::sort(ms.begin(), ms.end());
        return ms[RUNS / 2];
    };
    double s_ms = median_struct();
    double t_ms = median_tuple();
    std::cout << "N=" << N << std::endl;
    std::cout << "struct: " << s_ms << " ms" << std::endl;
    std::cout << "tuple : " << t_ms << " ms" << std::endl;
    std::cout << "tuple/struct=" << (t_ms / s_ms) << std::endl;
    return 0;
}
