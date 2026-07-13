// ⑤ 矩阵构建：同一源码在不同架构旗标下编译
#include <cstdio>
int main() {
#if defined(__x86_64__) || defined(_M_X64)
    std::printf("matrix: x86-64\n");
#elif defined(__aarch64__)
    std::printf("matrix: aarch64\n");
#else
    std::printf("matrix: unknown-arch\n");
#endif
    return 0;
}
