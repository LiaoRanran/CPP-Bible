// 文件：Examples/_ch161_fix1.cpp
// 主题：② 级别过滤 —— 阈值运行时可调，低级别静默丢弃
#include <cstdio>
#include <string_view>

enum class Level : int { trace = 0, debug = 1, info = 2, warn = 3, error = 4, off = 5 };

const char* to_cstr(Level l) {
    switch (l) {
        case Level::trace: return "trace";
        case Level::debug: return "debug";
        case Level::info:  return "info";
        case Level::warn:  return "warn";
        case Level::error: return "error";
        default:           return "off";
    }
}

struct Filter { Level threshold = Level::info; };

bool should_log(const Filter& f, Level msg) {
    return static_cast<int>(msg) >= static_cast<int>(f.threshold);
}

int main() {
    Filter f{Level::warn};   // 运行时把门槛提到 warn
    Level msgs[] = {Level::info, Level::warn, Level::error};
    int printed = 0;
    for (Level m : msgs)
        if (should_log(f, m)) {
            std::printf("[%s] event\n", to_cstr(m));
            ++printed;
        }
    std::printf("printed=%d (info 被过滤)\n", printed);
    return 0;
}
