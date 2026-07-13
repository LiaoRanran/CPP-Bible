// 文件：Examples/_ch99_par_bench.cpp
// 行号：见下方 main（实测并行执行策略是否真正并行）
// 编译运行：
//   g++ -std=c++23 -O2 Examples/_ch99_par_bench.cpp -o Examples/_ch99_par_bench.exe
//   Examples/_ch99_par_bench.exe
// 说明：libstdc++ 的 execution::par 需要 TBB 才能多线程；本 MinGW 未捆绑 TBB，
//       故 par 通常串行回退。本程序如实打印 seq / par 耗时与本机线程数。
#include <algorithm>
#include <numeric>
#include <execution>
#include <vector>
#include <cmath>
#include <chrono>
#include <iostream>
#include <thread>

int main() {
    const std::size_t N = 20'000'000;
    std::vector<double> a(N);
    std::iota(a.begin(), a.end(), 0.0);

    std::cout << "hardware_concurrency = " << std::thread::hardware_concurrency() << "\n";

    // ---- seq ----
    auto t0 = std::chrono::steady_clock::now();
    double s_seq = 0.0;
    s_seq = std::transform_reduce(std::execution::seq,
        a.begin(), a.end(), 0.0,
        std::plus<>(),
        [](double x) { return std::sin(x) * std::sin(x) + std::cos(x); });
    auto t1 = std::chrono::steady_clock::now();
    double ms_seq = std::chrono::duration<double, std::milli>(t1 - t0).count();

    // ---- par ----
    auto t2 = std::chrono::steady_clock::now();
    double s_par = 0.0;
    s_par = std::transform_reduce(std::execution::par,
        a.begin(), a.end(), 0.0,
        std::plus<>(),
        [](double x) { return std::sin(x) * std::sin(x) + std::cos(x); });
    auto t3 = std::chrono::steady_clock::now();
    double ms_par = std::chrono::duration<double, std::milli>(t3 - t2).count();

    std::cout << "seq  : " << ms_seq << " ms  result=" << s_seq << "\n";
    std::cout << "par  : " << ms_par << " ms  result=" << s_par << "\n";
    std::cout << "ratio(par/seq) = " << (ms_seq / ms_par) << "  (≈1 表示串行回退)\n";
    std::cout << "diff = " << (s_seq - s_par) << "  (应≈0，否则存在 FP 不确定性)\n";
    return 0;
}
