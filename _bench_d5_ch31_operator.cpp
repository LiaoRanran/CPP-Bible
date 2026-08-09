// Wave8 D5 bench: 运算符重载代价 —— 链式 operator+ 临时对象 vs 原地 operator+=
// 编译: g++ -O2 -std=c++23 _bench_d5_ch31_operator.cpp -o _bench_d5_ch31_operator.exe
// 运行: ./_bench_d5_ch31_operator.exe  (输出毫秒, 不断言时间/倍数)
#include <cstdio>
#include <cstdint>
#include <chrono>

struct Vec { double x, y, z; };
Vec operator+(const Vec& a, const Vec& b) { return { a.x + b.x, a.y + b.y, a.z + b.z }; }
Vec& operator+=(Vec& a, const Vec& b) { a.x += b.x; a.y += b.y; a.z += b.z; return a; }

static volatile double g_sink = 0;

int main() {
    constexpr int N = 50'000'000;
    Vec a{ 1, 2, 3 }, b{ 4, 5, 6 }, c{ 7, 8, 9 }, d{ 1, 1, 1 };

    auto t0 = std::chrono::steady_clock::now();
    double s = 0;
    for (int i = 0; i < N; ++i) { Vec v = a; v = v + b + c + d; s += v.x + v.y + v.z; }
    auto t1 = std::chrono::steady_clock::now();
    std::printf("chained operator+: %.3f ms\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count());

    auto t2 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) { Vec v = a; v += b; v += c; v += d; s += v.x + v.y + v.z; }
    auto t3 = std::chrono::steady_clock::now();
    std::printf("in-place operator+=: %.3f ms\n",
                std::chrono::duration<double, std::milli>(t3 - t2).count());

    g_sink = s;
    return 0;
}
