// ⑭ 平台抽象层（PAL）：用编译期宏隔离平台差异（[平台]）
// 本机 Windows + MinGW 编译运行通过
#include <iostream>
#include <string>

struct PAL {
    static std::string os_name() {
#if defined(_WIN32)
        return "windows";
#elif defined(__linux__)
        return "linux";
#elif defined(__APPLE__)
        return "macos";
#else
        return "unknown";
#endif
    }
    static std::string path_sep() {
#ifdef _WIN32
        return "\\";
#else
        return "/";
#endif
    }
    static std::string sleep_ms_impl() {
#ifdef _WIN32
        return "Sleep(ms)";
#else
        return "usleep(ms*1000)";
#endif
    }
};

int main() {
    std::cout << "[pal] os      = " << PAL::os_name()   << "\n";
    std::cout << "[pal] pathsep = " << PAL::path_sep()  << "\n";
    std::cout << "[pal] sleep   = " << PAL::sleep_ms_impl() << "\n";
    return 0;
}
