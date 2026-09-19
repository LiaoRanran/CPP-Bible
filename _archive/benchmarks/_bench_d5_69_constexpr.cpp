// _bench_d5_69_constexpr.cpp — ch69 constexpr：编译期查表 vs 运行期计算
// g++ -O2 -std=c++23
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cmath>
#include <array>
#include <vector>
#include <algorithm>
#include <random>

static double now_ms() {
    using namespace std::chrono;
    return duration<double, std::milli>(steady_clock::now().time_since_epoch()).count();
}
template <class F>
static double bench(const char* name, F&& f) {
    std::vector<double> t;
    for (int r = 0; r < 5; ++r) { double t0 = now_ms(); f(); t.push_back(now_ms() - t0); }
    std::sort(t.begin(), t.end());
    std::printf("%-40s %10.3f ms\n", name, t[2]);
    return t[2];
}
volatile double g_dsink;
volatile std::uint64_t g_sink;

// 自实现 constexpr sin（泰勒 11 项，输入已归约到 [-pi,pi]）——std::sin 到 C++26 才 constexpr
constexpr double PI = 3.14159265358979323846;
constexpr double csin(double x) {
    double term = x, sum = x;
    for (int k = 1; k <= 10; ++k) {
        term *= -x * x / double((2 * k) * (2 * k + 1));
        sum += term;
    }
    return sum;
}
constexpr std::size_t TBL = 1024;
constexpr auto make_table() {
    std::array<double, TBL> t{};
    for (std::size_t i = 0; i < TBL; ++i)
        t[i] = csin(-PI + 2 * PI * double(i) / double(TBL));
    return t;
}
constexpr auto CT_TABLE = make_table();   // 编译期完成，进 .rodata

int main() {
    constexpr std::size_t N = 100'000'000;
    // 随机索引/角度，防闭式折叠
    std::vector<std::uint32_t> idx(1 << 20);
    std::mt19937 rng(42);
    for (auto& v : idx) v = rng() & (TBL - 1);

    // 0) 运行期构建同款表的初始化成本（constexpr 版此项为 0，表在 .rodata）
    bench("runtime table init x1000", [&] {
        double s = 0;
        for (int r = 0; r < 1000; ++r) {
            std::array<double, TBL> t{};
            for (std::size_t i = 0; i < TBL; ++i)
                t[i] = std::sin(-PI + 2 * PI * double(i) / double(TBL));
            s += t[r & (TBL - 1)];
        }
        g_dsink = s;
    });

    // 1) constexpr 表：1 亿次查表
    bench("lookup constexpr table x100M", [&] {
        double s = 0;
        for (std::size_t i = 0; i < N; ++i)
            s += CT_TABLE[idx[i & ((1 << 20) - 1)]];
        g_dsink = s;
    });

    // 2) 每次调用 std::sin
    bench("call std::sin x100M", [&] {
        double s = 0;
        for (std::size_t i = 0; i < N; ++i) {
            double x = -PI + 2 * PI * double(idx[i & ((1 << 20) - 1)]) / double(TBL);
            s += std::sin(x);
        }
        g_dsink = s;
    });

    // 3) 每次调用自写 csin（同一函数，constexpr 函数在运行期照常可调用）
    bench("call csin(taylor) x100M", [&] {
        double s = 0;
        for (std::size_t i = 0; i < N; ++i) {
            double x = -PI + 2 * PI * double(idx[i & ((1 << 20) - 1)]) / double(TBL);
            s += csin(x);
        }
        g_dsink = s;
    });

    // 精度对照：表值 vs std::sin
    double maxerr = 0;
    for (std::size_t i = 0; i < TBL; ++i) {
        double x = -PI + 2 * PI * double(i) / double(TBL);
        maxerr = std::max(maxerr, std::fabs(CT_TABLE[i] - std::sin(x)));
    }
    std::printf("max |CT_TABLE - std::sin| = %.3e\n", maxerr);
    return 0;
}
