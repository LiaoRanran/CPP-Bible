// Wave8 D5 bench: 同一计算核在 -O0 / -O2 / -O3 下的运行期差异（Debug vs Release）
// 本文件被以不同优化级别分别编译 4 次，每次运行打印自身耗时（毫秒）。
// 编译示例:
//   g++ -O0 -std=c++23 _bench_d5_ch18_buildconfig.cpp -o b18_o0.exe
//   g++ -O2 -std=c++23 _bench_d5_ch18_buildconfig.cpp -o b18_o2.exe
//   g++ -O3 -std=c++23 _bench_d5_ch18_buildconfig.cpp -o b18_o3.exe
//   g++ -O2 -flto -std=c++23 _bench_d5_ch18_buildconfig.cpp -o b18_lto.exe
// 运行示例: ./b18_o2.exe
#include <cstdio>
#include <cstdint>
#include <chrono>
#include <vector>
#include <cmath>

static volatile double g_sink = 0;

int main() {
    constexpr int N = 16'000'000;
    std::vector<double> a(N), b(N), c(N);
    for (int i = 0; i < N; ++i) { a[i] = i * 0.001; b[i] = 1.0 / (i + 1); }

    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) c[i] = std::sqrt(a[i] * a[i] + b[i] * b[i]);
    auto t1 = std::chrono::steady_clock::now();

    double chk = 0;
    for (int i = 0; i < N; i += 1009) chk += c[i];
    g_sink = chk;

    std::printf("kernel N=%d  %.3f ms  chk=%.6f\n",
                N, std::chrono::duration<double, std::milli>(t1 - t0).count(), chk);
    return 0;
}
