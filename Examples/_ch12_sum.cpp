// ⑰ 文件：Examples/_ch12_sum.cpp，行号：1
// 用于演示 -O0 与 -O2 汇编差异：累加循环
extern int sink;
int sum_to(int n) {
    int s = 0;
    for (int i = 1; i <= n; ++i)
        s += i;
    sink = s;
    return s;
}
