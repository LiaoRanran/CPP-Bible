// ⑯ 平台相关测试：依据编译宏选择断言路径（本机为 Windows/MinGW）
#include <cstdio>
#include <cassert>
int main() {
#ifdef _WIN32
    assert(sizeof(void*) == 8);  // 本机 64 位
    std::printf("platform: _WIN32 path, LP64 pointer=%zu bytes\n", sizeof(void*));
#elif defined(__linux__)
    std::printf("platform: __linux__ path\n");
#else
    std::printf("platform: other\n");
#endif
    return 0;
}
