// ⑤ [平台·POSIX] 仅类 Unix 编译的分支
#include <cstdio>
int main() {
#ifdef __unix__
    std::printf("platform: POSIX (__unix__ defined)\n");
#else
    std::printf("platform: non-POSIX build\n");
#endif
    return 0;
}
