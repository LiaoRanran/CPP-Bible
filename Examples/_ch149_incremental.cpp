// 见 Examples/_ch149_incremental.cpp
// ⑮ 增量构建：依据 mtime 判断源是否变化
#include <cstdio>
#include <sys/stat.h>
int main() {
    struct stat st;
    if (stat("main.cpp", &st) == 0)
        std::printf("main.cpp mtime=%lld\n", (long long)st.st_mtime);
    else
        std::printf("main.cpp not found -> force full build\n");
    return 0;
}
