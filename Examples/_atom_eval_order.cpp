// 灰色地带对照（unspecified）：函数实参的求值顺序
// 标准态度：f(g(), h()) 中 g 与 h 的求值顺序**未指定（unspecified）**——
// 不是未定义行为（两种顺序都合法，程序不会崩），但**不可依赖**。
// 证伪条件：任何一次运行出现 UB 征兆（崩溃/非确定输出）即证伪"它是未指定而非 UB"。
// 对照维度：编译器（GCC 15.3 / GCC 13.1 本机可得；Clang/MSVC 交 CI）+ 优化级别。
//
// 复现：
//   g++ -std=c++17 -O2 Examples/_atom_eval_order.cpp -o /tmp/e.exe && /tmp/e.exe
//
// 输出格式说明（2026-09-10 调整）：g/h 各自打印**独立一行**，便于机器复算逐行比对——
//   旧版把三者拼成一行 `hg|f(1,2)`，而 `|` 正是证据卡 `run_*` 字段的多行分隔符，
//   会让复算工具误判行数（实测 refute:run_match）。改多行后语义更清晰：谁先出现谁先被求值。

#include <cstdio>

int g() { std::printf("g\n"); return 1; }
int h() { std::printf("h\n"); return 2; }
void f(int a, int b) { std::printf("f(%d,%d)\n", a, b); }

int main() {
    f(g(), h());          // 观察顺序：输出 h 在前还是 g 在前（两种都合法）
    return 0;
}
