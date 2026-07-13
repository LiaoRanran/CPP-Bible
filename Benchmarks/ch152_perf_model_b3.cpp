// C4 错误示范（被优化的基准）：结果未使用，编译器可删掉 work
#include <iostream>
#include <chrono>
static long long work(long long n) { long long s = 0; for (long long i = 0; i < n; ++i) s += i; return s; }
int main() {
    auto t0 = std::chrono::steady_clock::now();
    work(1'000'000);                  // ❌ 返回值被丢弃 → -O2 可整段删除
    auto t1 = std::chrono::steady_clock::now();
    std::cout << "us=" << std::chrono::duration_cast<std::chrono::microseconds>(t1 - t0).count() << "\n";
    return 0;
}