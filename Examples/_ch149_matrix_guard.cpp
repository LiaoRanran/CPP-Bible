// 见 Examples/_ch149_matrix_guard.cpp
// ⑤ 平台门禁：不支持的编译器直接编译失败，矩阵尽早暴露不兼容
#include <cstdio>
#if !defined(__GNUC__) && !defined(_MSC_VER)
#error "unsupported compiler in matrix"
#endif
int main() {
    std::printf("matrix guard passed\n");
    return 0;
}
