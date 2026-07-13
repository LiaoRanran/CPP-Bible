// 文件：Examples/_ch17_callconv.cpp
// 演示 x86-64 System V AMD64 ABI 调用约定（在 64 位 Linux/Windows 子系统通用，此处由本机 MinGW GCC 13.1.0 编译取证）。
// 编译：g++ -std=c++23 -O2 -S -masm=intel Examples/_ch17_callconv.cpp -o Examples/_ch17_callconv.asm

struct Point { long x, y; };

// 6 个整数参数：前 6 个用寄存器 RDI, RSI, RDX, RCX, R8, R9
long sum6(long a, long b, long c, long d, long e, long f) {
    return a + b + c + d + e + f;
}

// 16 字节结构按值传递：仍走寄存器（RDX:RAX 拆成两个 8 字节）
long manhattan(Point p) { return p.x + p.y; }

// 返回 >16 字节的结构：调用方提供隐式返回缓冲指针，参数整体右移一个寄存器
Point make_point(long x, long y) { return {x, y}; }

int main() {
    volatile long r = sum6(1, 2, 3, 4, 5, 6);
    Point p{10, 20};
    r += manhattan(p);
    Point q = make_point(7, 8);
    r += q.x + q.y;
    return (int)r;
}
