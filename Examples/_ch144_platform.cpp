// ch144 ⑯ 平台相关代码隔离：用宏把所有平台差异收敛到一处
// 编译（Windows）：g++ -std=c++23 -D_PLATFORM_WIN -O2 _ch144_platform.cpp
// 编译（Linux）：  g++ -std=c++23 -D_PLATFORM_POSIX -O2 _ch144_platform.cpp
#include <cstddef>

#if defined(_PLATFORM_WIN)
    using os_socket = int;            // Windows 侧占位类型
    static const char* family() { return "win32"; }
#elif defined(_PLATFORM_POSIX)
    using os_socket = int;            // POSIX 侧占位类型
    static const char* family() { return "posix"; }
#else
    #error "unknown platform: define _PLATFORM_WIN or _PLATFORM_POSIX"
#endif

int platform_tag() {
    return static_cast<int>(family()[0]);   // 仅作编译期差异示例
}
