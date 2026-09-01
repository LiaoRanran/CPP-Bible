// a3_call.cpp — A3 函数调用约定示例
// 8 个整数参数：前 6 走寄存器 rdi..r9，第 7、8 走栈
// 用 __attribute__((noinline)) 强制不内联，保留真实调用框
// 编译(保留调用框): g++ -std=c++23 -O0 -c -o a3_call.o a3_call.cpp
// 反汇编: objdump -d -M intel a3_call.o
__attribute__((noinline))
long compute(long a, long b, long c, long d, long e, long f, long g, long h) {
    long local = a + b + c + d + e + f + g + h;
    return local * 2;
}

int caller() {
    return (int)compute(1, 2, 3, 4, 5, 6, 7, 8);
}
