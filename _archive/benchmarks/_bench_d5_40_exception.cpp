// D5 Wave 3 benchmark: ch40 异常安全 — 异常的真实开销
// 编译: g++ -O2 -std=c++23 -o bench.exe _bench_d5_40_exception.cpp
// 目的:
//  (1) 不抛异常时, try/catch 相对纯循环的零开销(零开销异常模型);
//  (2) 错误真实发生时, 抛/捕 相比 错误码返回 的真实倍数代价.
#include <iostream>
#include <chrono>
#include <random>
#include <cstdint>

static volatile int64_t g_esc = 0;

struct MyErr {};  // 轻量异常, 避免字符串分配干扰

int main() {
    const int N = 2'000'000;
    std::mt19937 rng(12345);
    std::uniform_int_distribution<int> dist(0, 1'000'000);

    // 场景1: 纯循环(基线, 无错误处理)
    auto t0 = std::chrono::steady_clock::now();
    int64_t s0 = 0;
    for (int i = 0; i < N; ++i) s0 += (dist(rng) * 3 + 1);
    auto t1 = std::chrono::steady_clock::now();

    // 场景2: try/catch 但从不抛(测零开销)
    int64_t s1 = 0;
    auto t2 = std::chrono::steady_clock::now();
    try {
        for (int i = 0; i < N; ++i) s1 += (dist(rng) * 3 + 1);
    } catch (...) {}
    auto t3 = std::chrono::steady_clock::now();

    // 场景3: 错误码风格(1/7 走错误分支)
    auto t4 = std::chrono::steady_clock::now();
    int64_t s2 = 0;
    for (int i = 0; i < N; ++i) {
        int v = dist(rng) * 3 + 1;
        if (i % 7 == 0) s2 -= i; else s2 += v;
    }
    auto t5 = std::chrono::steady_clock::now();

    // 场景4: 异常风格(1/7 抛/捕)
    int64_t s3 = 0;
    auto t6 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) {
        try {
            int v = dist(rng) * 3 + 1;
            if (i % 7 == 0) throw MyErr{};
            s3 += v;
        } catch (...) {
            s3 -= i;
        }
    }
    auto t7 = std::chrono::steady_clock::now();

    g_esc = s0 + s1 + s2 + s3;
    auto ms = [](auto a, auto b) { return std::chrono::duration<double, std::milli>(b - a).count(); };
    std::cout << "plain_loop     " << ms(t0, t1) << " ms\n";
    std::cout << "try_nothrow    " << ms(t2, t3) << " ms\n";
    std::cout << "errcode_thrown " << ms(t4, t5) << " ms\n";
    std::cout << "exception_thrown " << ms(t6, t7) << " ms\n";
    std::cout << "esc=" << g_esc << "\n";
    return 0;
}
