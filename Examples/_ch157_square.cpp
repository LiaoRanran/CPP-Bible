// _ch157_square.cpp
// Compiler Explorer 实战附录（ch157）真实复现源
// 由 MinGW GCC 15.3.0 提取 -O0 / -O2 汇编对照，替换原书中编造的 GCC 13.2 / Clang 18 片段。
// 编译（须从 Examples/ 内相对路径编译，保证 .file 指令为基名）：
//   g++ -std=c++23 -O0 -S -masm=intel _ch157_square.cpp -o _ch157_square_o0.asm
//   g++ -std=c++23 -O2 -S -masm=intel _ch157_square.cpp -o _ch157_square_o2.asm
#include <cstdio>

int square(int x) {
    return x * x;
}

int main() {
    int s = square(5);   // -O0: 真实调用 square；-O2: 内联 + 常量折叠为 25
    std::printf("%d\n", s);
    return 0;
}
