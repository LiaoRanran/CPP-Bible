// 文件：Examples/_ch161_macro.cpp
// 取证：g++ -std=c++20 -O2 真实编译运行（本机）
#include <cstdio>

// ⑩ 宏设计：LOG_<LEVEL> 自动捕获文件/行/级别，并做级别门控
enum class Lv { info = 2, warn = 3, error = 4 };
constexpr Lv g_thr = Lv::info;

#define LOG_LOG(level_enum, tag, ...)                                      \
    do {                                                                   \
        if (static_cast<int>(level_enum) >= static_cast<int>(g_thr)) {     \
            std::printf("[%s] %s:%d: ", tag, __FILE__, __LINE__);          \
            std::printf(__VA_ARGS__);                                      \
        }                                                                  \
    } while (0)

#define LOG_INFO(...)  LOG_LOG(Lv::info,  "info",  __VA_ARGS__)
#define LOG_WARN(...)  LOG_LOG(Lv::warn,  "warn",  __VA_ARGS__)
#define LOG_ERROR(...) LOG_LOG(Lv::error, "error", __VA_ARGS__)

int main() {
    LOG_INFO("user %d login ok\n", 7);
    LOG_WARN("latency %d ms\n", 120);
    LOG_ERROR("db unreachable\n");
    return 0;
}
