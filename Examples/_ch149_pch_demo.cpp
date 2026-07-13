// ⑮ 增量构建：预编译头（PCH）缩短反复编译
#include "ch149_pch.h"   // 实际工程中由 CMake target_precompile_headers 生成

int main() {
    std::printf("pch demo: %zu\n", sizeof(std::vector<int>));
    return 0;
}
