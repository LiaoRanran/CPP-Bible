// _ch18_opt.cpp —— 优化级别对比示例
// 函数 add/mul3/caller 在 -O0 与 -O2 下生成截然不同的汇编。

int add(int a, int b) { return a + b; }

int mul3(int x) { return x * 3; }

int caller() {
    // -O2 会把 add(4,5) 常量折叠为 9，mul3(2) 折叠为 6，caller 直接返回 15。
    // -O0 则逐个求值、真实调用 add / mul3。
    return add(4, 5) + mul3(2);
}

int sum_arr(const int* p, int n) {
    int s = 0;
    for (int i = 0; i < n; ++i) s += p[i];
    return s;
}
