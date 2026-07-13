// ⑮ DCE 实证：结果未消费 -> 循环被 -O2 消除；用 volatile 下沉则保留
#include <cstdio>
#include <chrono>
static int compute() { int s = 0; for (int i = 0; i < 200'000'000; ++i) s += i; return s; }
int main() {
    // A: 结果未使用，编译器在 -O2 下可消除整个循环
    auto a0 = std::chrono::steady_clock::now();
    int ra = compute(); (void)ra;  // (void) 仍可能被 DCE？此处演示：naive 版
    auto a1 = std::chrono::steady_clock::now();
    double ma = std::chrono::duration<double, std::milli>(a1 - a0).count();

    // B: 用 volatile 强制消费结果，循环必须保留
    auto b0 = std::chrono::steady_clock::now();
    int rb = compute(); volatile int sink = rb; (void)sink;
    auto b1 = std::chrono::steady_clock::now();
    double mb = std::chrono::duration<double, std::milli>(b1 - b0).count();

    std::printf("dce: A(no-sink)=%.3f ms  B(volatile-sink)=%.3f ms\n", ma, mb);
    return 0;
}
