// 文件：Examples/_ch161_platform.cpp
// 取证：g++ -std=c++20 -O2 真实编译运行（本机）；演示 Windows/Linux 路径与行尾差异
#include <cstdio>
#include <string>

// ⑭ 平台差异：路径分隔符、默认行尾、控制台句柄在不同 OS 上不同
std::string separator() {
#ifdef _WIN32
    return "\\";      // Windows 用反斜杠
#else
    return "/";       // 类 Unix 用正斜杠
#endif
}

std::string line_ending() {
#ifdef _WIN32
    return "\r\n";    // Windows 文本模式默认 CRLF
#else
    return "\n";      // 类 Unix 用 LF
#endif
}

const char* platform_name() {
#ifdef _WIN32
    return "windows";
#elif defined(__linux__)
    return "linux";
#else
    return "other";
#endif
}

int main() {
    std::printf("platform=%s sep=%s eol_is_crlf=%d\n",
                platform_name(),
                separator().c_str(),
                line_ending().size() == 2);
    return 0;
}
