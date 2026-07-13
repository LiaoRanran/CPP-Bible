// 见 Examples/_ch149_build_info.cpp
// ② 构建信息固化：版本与 commit 由 CI 注入，保证可复现
#include <cstdio>
#ifndef GIT_COMMIT
#define GIT_COMMIT "unknown"
#endif
#ifndef BUILD_TS
#define BUILD_TS "1970-01-01T00:00:00Z"
#endif
int main() {
    std::printf("commit=%s build=%s\n", GIT_COMMIT, BUILD_TS);
    return 0;
}
