// 文件：Examples/_ch17_align.cpp
// 演示栈与数据的 32 字节对齐（AVX 加载/存储要求 32 字节对齐地址）。
// 编译：g++ -std=c++23 -O2 -mavx -S -masm=intel Examples/_ch17_align.cpp -o Examples/_ch17_align.asm

#include <cstddef>

volatile int sink = 0;

// 局部 32 字节对齐数组 + AVX 广播存储 -> 编译器必须对栈做 and rsp, -32 对齐
extern "C" long vec_broadcast(std::size_t n, double v) {
    alignas(32) double buf[4] = {v, v, v, v};   // 期望 32 字节对齐
    long acc = 0;
    for (std::size_t i = 0; i < n; ++i) {
        buf[i & 3] += (double)i;
        acc += (long)buf[i & 3];
    }
    sink = (int)acc;
    return acc;
}

int main() { return (int)vec_broadcast(8, 2.0); }
