// 取证示例：异常对"无异常路径"的零开销（g++ -O2）
// 编译：g++ -std=c++23 -O2 -S -masm=intel _ch146_perf.cpp -o _ch146_perf.asm
#include <cstdio>

// noexcept 路径：编译器可假设不抛，生成直接 add
int add_nonthrow(int a, int b) noexcept {
    return a + b;
}

// 可能抛的路径：调用点需登记异常展开信息（.eh_frame / 异常表）
int add_throw(int a, int b) {
    if (b == 0) throw 0;
    return a / b;
}

int main() {
    volatile int s = 0;
    for (int i = 0; i < 1000000; ++i)
        s += add_nonthrow(i, 1);          // 热点循环体无异常簿记
    std::printf("%d\n", static_cast<int>(s));
    return add_throw(1, 0);               // 仅此处需要异常支持
}
