// _ch11_cconv.cpp : 多参数函数，用于观察 x86-64 Win64 调用约定的寄存器分配
// 本文件仅供 -S 取证，不链接运行
long compute(long a, long b, long c, long d, long e, long f) {
    return a + b * 2 + c * 3 + d * 4 + e * 5 + f * 6;
}
