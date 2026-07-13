// 见 Examples/_ch149_matrix.cpp
// ⑤ 矩阵构建：探测编译器与 OS，驱动多维度组合
#include <cstdio>
int main() {
#if defined(__GNUC__) && !defined(__clang__)
    std::printf("compiler=gcc-%d.%d\n", __GNUC__, __GNUC_MINOR__);
#elif defined(_MSC_VER)
    std::printf("compiler=msvc-%d\n", _MSC_VER);
#else
    std::printf("compiler=other\n");
#endif
#ifdef __linux__
    std::printf("os=linux\n");
#elif defined(_WIN32)
    std::printf("os=windows\n");
#endif
    return 0;
}
