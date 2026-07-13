// ⑤ [平台·Windows] 仅 Windows 编译的分支
#include <cstdio>
int main() {
#ifdef _WIN32
    std::printf("platform: Windows (win32 _WIN32 defined)\n");
#else
    std::printf("platform: non-Windows\n");
#endif
    return 0;
}
