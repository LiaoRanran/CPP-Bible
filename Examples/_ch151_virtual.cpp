// ⑪ 虚函数分派（汇编见 _ch151_virtual.asm）
// 见 Examples/_ch151_virtual.cpp
#include <cstdio>
#include <chrono>

struct Base { virtual ~Base() = default; virtual int f(int x) const = 0; };
struct A : Base { int f(int x) const override { return x * 2; } };
struct B : Base { int f(int x) const override { return x + 7; } };

int main() {
    const int N = 100'000'000;
    A a; B b;
    Base* p = &a;
    auto t0 = std::chrono::steady_clock::now();
    volatile int r = 0;
    for (int i = 0; i < N; ++i) r += p->f(i);     // 虚调用
    auto t1 = std::chrono::steady_clock::now();
    std::printf("virtual: ms=%.3f r=%d\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count(), r);
    return 0;
}
