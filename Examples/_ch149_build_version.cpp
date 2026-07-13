// ⑨ 制品版本注入：通过 -DBUILD_TAG 在编译期嵌入
#include <cstdio>
#ifndef BUILD_TAG
#define BUILD_TAG "local"
#endif
#ifndef GIT_SHA
#define GIT_SHA "unknown"
#endif

int main() {
    std::printf("artifact version=%s sha=%s\n", BUILD_TAG, GIT_SHA);
    return 0;
}
