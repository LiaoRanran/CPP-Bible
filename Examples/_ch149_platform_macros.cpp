// 见 Examples/_ch149_platform_macros.cpp
// ⑫ 平台宏：CI 矩阵据此选择工具链与依赖
#include <cstdio>
int main() {
#ifdef _WIN32
    std::printf("target=windows\n");
#elif __linux__
    std::printf("target=linux\n");
#elif __APPLE__
    std::printf("target=macos\n");
#else
    std::printf("target=unknown\n");
#endif
    std::printf("ptr_size=%zu\n", sizeof(void*));
    return 0;
}
