// 文件：Examples/_ch161_fix9.cpp
// 主题：⑩ 宏设计 —— 完整 LOG_TRACE/DEBUG/INFO 家族，自动注入文件行号
#include <cstdio>

enum class Lv { trace = 0, debug = 1, info = 2, warn = 3, error = 4 };
constexpr Lv G_THR = Lv::debug;

#define LOG_LEVEL(lv_enum, tag, ...)                                       \
    do {                                                                    \
        if (static_cast<int>(lv_enum) >= static_cast<int>(G_THR)) {        \
            std::printf("[%s] %s:%d ", tag, __FILE__, __LINE__);           \
            std::printf(__VA_ARGS__);                                       \
        }                                                                   \
    } while (0)

#define LOG_TRACE(...) LOG_LEVEL(Lv::trace, "trace", __VA_ARGS__)
#define LOG_DEBUG(...) LOG_LEVEL(Lv::debug, "debug", __VA_ARGS__)
#define LOG_INFO(...)  LOG_LEVEL(Lv::info,  "info",  __VA_ARGS__)

int main() {
    LOG_TRACE("t=%d\n", 1);   // 被过滤（阈值 debug）
    LOG_DEBUG("d=%d\n", 2);   // 保留
    LOG_INFO("i=%d\n", 3);    // 保留
    return 0;
}
