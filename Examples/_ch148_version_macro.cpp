// _ch148_version_macro.cpp
// 语义化版本宏：编译期常量 + 构建期注入 Git commit。
// 编译：g++ -std=c++23 -O2 -DGIT_COMMIT=\"$(git rev-parse --short HEAD)\" _ch148_version_macro.cpp -o _ch148_version_macro
#include <cstdio>

#define PROJECT_MAJOR  2
#define PROJECT_MINOR  4
#define PROJECT_PATCH  1

#define STRINGIFY(x)      STRINGIFY_IMPL(x)
#define STRINGIFY_IMPL(x) #x

#define PROJECT_VERSION_STRING \
    "v" STRINGIFY(PROJECT_MAJOR) "." STRINGIFY(PROJECT_MINOR) "." STRINGIFY(PROJECT_PATCH)

#ifndef GIT_COMMIT
#define GIT_COMMIT "unknown"
#endif

int main() {
    std::printf("version=%s commit=%s\n", PROJECT_VERSION_STRING, GIT_COMMIT);
}
