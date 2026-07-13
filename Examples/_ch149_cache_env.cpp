// 见 Examples/_ch149_cache_env.cpp
// ④ ccache 环境变量注入（上游参考 ccache 的 CCACHE_* 系列变量）
#include <cstdio>
int main() {
    std::printf("CCACHE_DIR=/ci/cache/ccache\n");
    std::printf("CCACHE_MAXSIZE=5G\n");
    std::printf("CCACHE_BASEDIR=/ci/src\n");
    std::printf("CCACHE_COMPILERCHECK=content\n");
    return 0;
}
