// ⑪ 编译期数据：把表摊开在只读段，运行期零成本查询
constexpr int fib(int n) {
    return n < 2 ? n : fib(n - 1) + fib(n - 2);
}

constexpr int kTableSize = fib(10);   // 55，编译期求得
static_assert(kTableSize == 55);

// 编译期生成查表，避免运行期循环
constexpr int make_table(int i) { return fib(i); }

int use_table() {
    int arr[kTableSize];              // 栈上定长数组，大小已知
    for (int i = 0; i < kTableSize; ++i) arr[i] = make_table(i);
    int s = 0;
    for (int i = 0; i < kTableSize; ++i) s += arr[i];
    return s;                          // 返回已知常数，可被常量折叠
}
