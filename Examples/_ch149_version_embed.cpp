// 见 Examples/_ch149_version_embed.cpp
// ⑨ 制品版本嵌入：发布时用 git describe 注入，保证可追溯
#include <cstdio>
#ifndef GIT_DESCRIBE
#define GIT_DESCRIBE "v0.0.0-dirty"
#endif
int main() {
    std::printf("artifact version: %s\n", GIT_DESCRIBE);
    return 0;
}
