// 文件：Examples/_ch12_sum.cpp
// 行号：1
// 累加 1..n；分别用 -O0 与 -O2 编译看汇编
extern int sink;
int sum_to(int n) {
    int s = 0;
    for (int i = 1; i <= n; ++i) s += i;
    sink = s;
    return s;
}