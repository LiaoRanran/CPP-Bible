// _ch14_gdb_demo.cpp — 供 GDB 练习的示例（与第14章 ② 示例 3 同源，含 off-by-one 隐患）
// 编译：g++ -std=c++23 -O0 -g _ch14_gdb_demo.cpp -o _ch14_gdb_demo
// 说明：故意传入 hi=3 越界读 v[3]，用于演示 GDB 下断点 / backtrace / print 抓出隐患。
#include <cstddef>
#include <cstdio>

int sum_range(int* a, int lo, int hi) {
    int s = 0;
    for (int i = lo; i <= hi; ++i) s += a[i];   // hi 越界时读脏 / 崩溃
    return s;
}

int caller() {
    int v[3] = {10, 20, 30};
    return sum_range(v, 0, 3);                  // 传入 hi=3，越界读 v[3]
}

int main() { std::printf("%d\n", caller()); }
