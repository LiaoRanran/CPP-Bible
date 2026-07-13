// _ch148_submodule_version.cpp
// 用 `git describe` 在构建期生成带距离与 commit 的版本串（CI 注入宏）。
// 编译：g++ -std=c++23 -O2 -DGIT_DESCRIBE=\"$(git describe --tags --always)\" _ch148_submodule_version.cpp -o _ch148_submodule_version
#include <cstdio>

#ifndef GIT_DESCRIBE
#define GIT_DESCRIBE "v0.0.0-unknown"
#endif

struct Version {
    int major = 0, minor = 0, patch = 0, distance = 0;
    char commit[41] = "unknown";
};

// 解析 "v2.4.1-12-gabcdef0" 形式（git describe 默认输出）
static Version parse_describe(const char* s) {
    Version v;
    int n = std::sscanf(s, "v%d.%d.%d-%d-g%40s",
                        &v.major, &v.minor, &v.patch, &v.distance, v.commit);
    (void)n;
    return v;
}

int main() {
    Version v = parse_describe(GIT_DESCRIBE);
    std::printf("major=%d minor=%d patch=%d distance=%d commit=%s\n",
                v.major, v.minor, v.patch, v.distance, v.commit);
    return 0;
}
