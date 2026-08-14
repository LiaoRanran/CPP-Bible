// _bench_d5_146_error.cpp  (GCC 15.3.0, g++ -O2 -std=c++23)
// 真实基准：错误处理路径的成本——error-code 返回 vs 异常抛出。
// 测两类路径：成功路径（不触发错误）与失败路径（每次都触发错误）。
// 注意：循环内用 asm volatile fence 阻止编译器把等差数列求和闭式化（否则 DCE 会让耗时≈0）。
#include <chrono>
#include <iostream>
#include <stdexcept>

static long long sink = 0;

int compute_ec(int x, int& out) {
    if (x == 0) return -1;   // “错误”
    out = x * 2;
    return 0;
}
int compute_ex(int x) {
    if (x == 0) throw std::runtime_error("zero");
    return x * 2;
}

int main() {
    const int N = 10'000'000;

    // 成功路径（永不触发错误）
    {
        auto t0 = std::chrono::steady_clock::now();
        long long s = 0;
        for (int i = 0; i < N; ++i) { int o; if (compute_ec(i + 1, o) == 0) s += o;
            asm volatile("" : "+r"(s) :: "memory"); }
        auto t1 = std::chrono::steady_clock::now();
        sink += s;
        std::cout << "error-code success : " << (t1 - t0).count() / 1e6 << " ms" << std::endl;
    }
    {
        auto t0 = std::chrono::steady_clock::now();
        long long s = 0;
        for (int i = 0; i < N; ++i) { try { s += compute_ex(i + 1); } catch (...) {}
            asm volatile("" : "+r"(s) :: "memory"); }
        auto t1 = std::chrono::steady_clock::now();
        sink += s;
        std::cout << "exception success  : " << (t1 - t0).count() / 1e6 << " ms" << std::endl;
    }
    // 失败路径（每次都触发错误）
    {
        auto t0 = std::chrono::steady_clock::now();
        long long s = 0; int o;
        for (int i = 0; i < N; ++i) { if (compute_ec(0, o) != 0) s += 1;
            asm volatile("" : "+r"(s) :: "memory"); }
        auto t1 = std::chrono::steady_clock::now();
        sink += s;
        std::cout << "error-code failure : " << (t1 - t0).count() / 1e6 << " ms" << std::endl;
    }
    {
        auto t0 = std::chrono::steady_clock::now();
        long long s = 0;
        for (int i = 0; i < N; ++i) { try { s += compute_ex(0); } catch (const std::exception&) { s += 1; }
            asm volatile("" : "+r"(s) :: "memory"); }
        auto t1 = std::chrono::steady_clock::now();
        sink += s;
        std::cout << "exception failure  : " << (t1 - t0).count() / 1e6 << " ms" << std::endl;
    }
    std::cout << "sink=" << sink << std::endl;
    return 0;
}
