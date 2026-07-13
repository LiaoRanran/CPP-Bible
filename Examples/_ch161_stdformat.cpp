// 文件：Examples/_ch161_stdformat.cpp
// 取证：g++ -std=c++20 -O2 真实编译运行（本机）；std::format 需要 C++20
#include <format>
#include <iostream>
#include <string>

// ⑤ std::format：C++20 标准格式化，编译期格式串检查，类型安全
int main() {
    int code = 404;
    double lat = 31.2304;
    std::string s = std::format("status={} lat={:.3f} hex={:#x}", code, lat, code);
    std::cout << s << "\n";

    // 对齐与填充（fmt 风格同样支持）
    std::cout << std::format("{:<10}|{:>10}|{:^10}\n", "left", "right", "mid");
    return 0;
}
