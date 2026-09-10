// 灰色地带对照（unspecified）：函数实参的求值顺序
// 标准态度：f(g(), h()) 中 g 与 h 的求值顺序**未指定（unspecified）**——
// 不是未定义行为（两种顺序都合法，程序不会崩），但**不可依赖**。
// 证伪条件：任何一次运行出现 UB 征兆（崩溃/非确定输出）即证伪"它是未指定而非 UB"。
// 对照维度：编译器（GCC 15.3 / GCC 13.1 本机可得；Clang/MSVC 交 CI）+ 优化级别。
//
// 复现：
//   g++ -std=c++23 -O2 Examples/_atom_eval_order.cpp -o /tmp/e.exe && /tmp/e.exe

#include <cstdio>

int g() { std::printf("g"); return 1; }
int h() { std::printf("h"); return 2; }
void f(int a, int b) { std::printf("|f(%d,%d)\n", a, b); }

int main() {
    f(g(), h());          // 观察输出是 "gh|f(1,2)" 还是 "hg|f(1,2)"
    return 0;
}
