// C++23 <generator> — 真实可编译实证 (GCC 15.3.0, -std=c++26 -O2)
// 目的：验证 std::generator 协程帧与 co_yield 状态机生成的指令。
#include <generator>
#include <cstdio>

std::generator<int> iota(int n) {
    for (int i = 0; i < n; ++i)
        co_yield i;
}

int main() {
    int sum = 0;
    for (int v : iota(5))
        sum += v;
    std::printf("%d\n", sum);
    return 0;
}
