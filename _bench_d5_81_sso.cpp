// _bench_d5_81_sso.cpp — ch81 D5: SSO 边界（15/16 字符）构造/拷贝断崖
// g++ -O2 -std=c++17
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <string>
#include <vector>

using Clock = std::chrono::steady_clock;
static double ms(Clock::time_point a, Clock::time_point b) {
    return std::chrono::duration<double, std::milli>(b - a).count();
}
template <class F> static double median5(F f) {
    std::vector<double> t;
    for (int i = 0; i < 5; ++i) t.push_back(f());
    std::sort(t.begin(), t.end());
    return t[2];
}
volatile size_t g_sink = 0;

static double bench_ctor(const char* src, int reps) {
    return median5([&] {
        auto a = Clock::now();
        size_t s = 0;
        for (int i = 0; i < reps; ++i) {
            std::string str(src);
            s += str.size() + (size_t)str[0];
        }
        g_sink = s;
        return ms(a, Clock::now());
    });
}

static double bench_copy_vec(size_t len, int n) {
    std::string proto(len, 'x');
    std::vector<std::string> v(n, proto);
    return median5([&] {
        auto a = Clock::now();
        std::vector<std::string> c = v;  // 逐元素拷贝
        g_sink = c.back().size();
        return ms(a, Clock::now());
    });
}

int main() {
    const int R = 2'000'000;
    // libstdc++: 内部 buffer 15 chars + '\0'（_S_local_capacity=15）
    std::printf("ctor_2M,len7,%.3f\n", bench_ctor("abcdefg", R));
    double t15 = bench_ctor("abcdefghijklmno", R);       // 15 = SSO 上限
    double t16 = bench_ctor("abcdefghijklmnop", R);      // 16 = 首个堆分配
    double t32 = bench_ctor("abcdefghijklmnopqrstuvwxyz012345", R);
    std::printf("ctor_2M,len15_sso,%.3f\n", t15);
    std::printf("ctor_2M,len16_heap,%.3f,ratio_vs15=%.2f\n", t16, t16 / t15);
    std::printf("ctor_2M,len32_heap,%.3f,ratio_vs15=%.2f\n", t32, t32 / t15);

    const int N = 1'000'000;
    double c15 = bench_copy_vec(15, N);
    double c16 = bench_copy_vec(16, N);
    double c64 = bench_copy_vec(64, N);
    std::printf("copy_vec1M,len15_sso,%.3f\n", c15);
    std::printf("copy_vec1M,len16_heap,%.3f,ratio=%.2f\n", c16, c16 / c15);
    std::printf("copy_vec1M,len64_heap,%.3f,ratio=%.2f\n", c64, c64 / c15);

    // move：SSO 移动 = memcpy 16B（不比拷贝快多少）；堆串移动 = 偷指针
    double m15 = median5([&] {
        std::vector<std::string> v(N, std::string(15, 'x'));
        auto a = Clock::now();
        std::vector<std::string> d;
        d.reserve(N);
        for (auto& s : v) d.push_back(std::move(s));
        g_sink = d.back().size();
        return ms(a, Clock::now());
    });
    double m64 = median5([&] {
        std::vector<std::string> v(N, std::string(64, 'x'));
        auto a = Clock::now();
        std::vector<std::string> d;
        d.reserve(N);
        for (auto& s : v) d.push_back(std::move(s));
        g_sink = d.back().size();
        return ms(a, Clock::now());
    });
    std::printf("move_1M,len15_sso,%.3f\n", m15);
    std::printf("move_1M,len64_heap,%.3f,ratio=%.2f\n", m64, m64 / m15);
    return 0;
}
