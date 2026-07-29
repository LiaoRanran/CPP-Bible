// _bench_d5_115_move.cpp  — 移动语义 vs 深拷贝 (GCC 15.3.0)
// 对比：vector<string>/vector<int> 的拷贝(O(n)深拷贝) vs 移动(O(1)指针交换)
// 用 volatile 逃逸 + 读内容，逼出真实拷贝开销
#include <iostream>
#include <vector>
#include <string>
#include <chrono>

static constexpr int N = 2'000'000;
volatile int64_t g_sink = 0;
void* volatile g_esc = nullptr;

__attribute__((noinline)) int64_t bench_copy_vec() {
    int64_t s = 0;
    for (int i = 0; i < N; ++i) {
        std::vector<int> a(64, i);
        std::vector<int> b = a;  // 深拷贝 64 ints
        g_esc = &b;
        s += b[0];
    }
    return s;
}
__attribute__((noinline)) int64_t bench_move_vec() {
    int64_t s = 0;
    for (int i = 0; i < N; ++i) {
        std::vector<int> a(64, i);
        std::vector<int> b = std::move(a);  // O(1) 指针交换
        g_esc = &b;
        s += b[0];
    }
    return s;
}
__attribute__((noinline)) int64_t bench_copy_str() {
    int64_t s = 0;
    for (int i = 0; i < N; ++i) {
        std::string a(128, 'x');
        std::string b = a;  // 深拷贝(>SSO 阈值)
        g_esc = &b;
        s += b[0];
    }
    return s;
}
__attribute__((noinline)) int64_t bench_move_str() {
    int64_t s = 0;
    for (int i = 0; i < N; ++i) {
        std::string a(128, 'x');
        std::string b = std::move(a);  // O(1)
        g_esc = &b;
        s += b[0];
    }
    return s;
}
int main() {
    const int R = 5;
    auto med = [](auto f) -> double {
        std::vector<double> t;
        for (int r = 0; r < R; ++r) {
            auto a = std::chrono::steady_clock::now();
            int64_t s = f();
            auto b = std::chrono::steady_clock::now();
            g_sink = s;
            t.push_back(std::chrono::duration<double, std::milli>(b - a).count());
        }
        std::sort(t.begin(), t.end());
        return t[R / 2];
    };
    double cv = med(bench_copy_vec), mv = med(bench_move_vec);
    double cs = med(bench_copy_str), ms = med(bench_move_str);
    std::cout << "vector copy : " << cv << " ms\n";
    std::cout << "vector move : " << mv << " ms  (" << cv / mv << "x)\n";
    std::cout << "string copy : " << cs << " ms\n";
    std::cout << "string move : " << ms << " ms  (" << cs / ms << "x)\n";
    return (int)g_sink;
}
