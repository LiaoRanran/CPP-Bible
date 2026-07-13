// _ch14_opt.cpp — -O0 与 -O2 汇编对比（性能陷阱取证）
int sum_to(int n) {
    int s = 0;
    for (int i = 1; i <= n; ++i) s += i;
    return s;
}
