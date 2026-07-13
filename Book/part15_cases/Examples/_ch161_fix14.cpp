// 文件：Examples/_ch161_fix14.cpp
// 主题：⑱ 与错误处理衔接 —— 异常负责控制流，日志只留痕
#include <cstdio>
#include <stdexcept>
#include <string>
#include <string_view>

void log_error(std::string_view msg) {
    std::printf("[error] %s\n", std::string(msg).c_str());
}

int divide(int a, int b) {
    if (b == 0) throw std::runtime_error("divide by zero");
    return a / b;
}

int main() {
    try {
        int r = divide(10, 0);
        std::printf("r=%d\n", r);
    } catch (const std::exception& e) {
        log_error(e.what());   // 错误仍向上抛，日志仅旁观留痕
    }
    return 0;
}
