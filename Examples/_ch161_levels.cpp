// 文件：Examples/_ch161_levels.cpp
// 取证：g++ -std=c++20 -O2 -Wall -Wextra 真实编译运行（本机）
#include <iostream>
#include <string_view>

// ① 日志级别：trace < debug < info < warn < error < critical
enum class Level : int {
    trace = 0,
    debug = 1,
    info  = 2,
    warn  = 3,
    error = 4,
    critical = 5,
    off   = 6   // 全部关闭
};

constexpr std::string_view to_str(Level l) {
    switch (l) {
        case Level::trace:    return "trace";
        case Level::debug:    return "debug";
        case Level::info:     return "info";
        case Level::warn:     return "warn";
        case Level::error:    return "error";
        case Level::critical: return "critical";
        case Level::off:      return "off";
    }
    return "?";
}

// 级别门控：只有 >= 当前阈值才输出
inline bool enabled(Level msg, Level threshold) {
    return static_cast<int>(msg) >= static_cast<int>(threshold);
}

int main() {
    const Level threshold = Level::info;  // 生产中通常 info 起步
    Level msgs[] = {Level::trace, Level::debug, Level::info,
                    Level::warn, Level::error, Level::critical};
    for (Level m : msgs) {
        if (enabled(m, threshold)) {
            std::cout << "[" << to_str(m) << "] event\n";
        }
    }
    return 0;
}
