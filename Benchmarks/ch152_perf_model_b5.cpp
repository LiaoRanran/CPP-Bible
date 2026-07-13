// C6 内联汇编 black_box：强制"使用"变量且不引入真实存储（比 volatile 更狠）
#include <iostream>
#include <chrono>
static long long work(long long n) { long long s = 0; for (long long i = 0; i < n; ++i) s += i; return s; }
inline void black_box(long long v) { asm volatile("" : : "r"(v) : "memory"); }
int main() {
    auto t0 = std::chrono::steady_clock::now();
    black_box(work(1'000'000));                    // ✅ 编译期假装"用掉了"结果
    auto t1 = std::chrono::steady_clock::now();
    std::cout << "ns=" << std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count() << "\n";
    return 0;
}