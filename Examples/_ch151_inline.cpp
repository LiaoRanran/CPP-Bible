// ⑪' 内联（汇编见 _ch151_inline.asm）
// 见 Examples/_ch151_inline.cpp
#include <cstdio>
#include <chrono>

struct A { int f(int x) const { return x * 2; } };   // 非虚 → 可内联

int main() {
    const int N = 100'000'000;
    A a;
    auto t0 = std::chrono::steady_clock::now();
    volatile int r = 0;
    for (int i = 0; i < N; ++i) r += a.f(i);          // 内联展开
    auto t1 = std::chrono::steady_clock::now();
    std::printf("inline: ms=%.3f r=%d\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count(), r);
    return 0;
}
