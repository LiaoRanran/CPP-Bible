// Wave8 D5 bench: 格式化吞吐 std::format vs snprintf vs std::ostringstream
// 编译: g++ -O2 -std=c++23 _bench_d5_ch131_fmt_spdlog.cpp -o _bench_d5_ch131_fmt_spdlog.exe
// 运行: ./_bench_d5_ch131_fmt_spdlog.exe  (输出毫秒, 不断言时间/倍数)
#include <cstdio>
#include <cstdint>
#include <chrono>
#include <string>
#include <format>
#include <sstream>

static volatile std::uint64_t g_sink = 0;

int main() {
    constexpr int N = 2'000'000;
    const int a = 12345, b = 67890, c = -42;
    char buf[64];

    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) {
        int n = std::snprintf(buf, sizeof buf, "%d-%d-%d", a, b, c);
        g_sink += static_cast<std::uint64_t>(n);
    }
    auto t1 = std::chrono::steady_clock::now();
    std::printf("snprintf %.3f ms\n", std::chrono::duration<double, std::milli>(t1 - t0).count());

    auto t2 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) {
        std::string s = std::format("{}-{}-{}", a, b, c);
        g_sink += static_cast<std::uint64_t>(s.size());
    }
    auto t3 = std::chrono::steady_clock::now();
    std::printf("std_format %.3f ms\n", std::chrono::duration<double, std::milli>(t3 - t2).count());

    auto t4 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) {
        std::ostringstream os;
        os << a << '-' << b << '-' << c;
        g_sink += static_cast<std::uint64_t>(os.str().size());
    }
    auto t5 = std::chrono::steady_clock::now();
    std::printf("ostringstream %.3f ms\n", std::chrono::duration<double, std::milli>(t5 - t4).count());

    std::printf("g_sink=%llu\n", static_cast<unsigned long long>(g_sink));
    return 0;
}
