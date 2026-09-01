// a4_flow.cpp — A4 控制流示例
// sum: 数组累加循环（展示 cmp + 条件跳转 + 索引寻址）
// max2: 分支（展示 cmp + jle）
// 用 -O0 保留清晰的控制流结构
// 编译: g++ -std=c++23 -O0 -c -o a4_flow.o a4_flow.cpp
// 反汇编: objdump -d -M intel a4_flow.o
__attribute__((noinline))
long sum(const long* a, long n) {
    long s = 0;
    for (long i = 0; i < n; ++i)
        s += a[i];
    return s;
}

__attribute__((noinline))
long max2(long x, long y) {
    return x > y ? x : y;
}
