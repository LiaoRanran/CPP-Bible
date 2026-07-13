// _ch145_overload.cpp —— 重载 vs 命名函数（g++ 编译取证，warnings clean）
#include <cstdio>

void log(int level, const char* msg) { std::printf("[%d] %s\n", level, msg); }
void log(const char* msg)            { log(0, msg); }

// 命名函数：意图更显式，无歧义
void log_error(const char* msg) { log(2, msg); }
void log_info(const char* msg)  { log(0, msg); }

int main() {
    log("hello");            // 重载解析到 (const char*)
    log(1, "warn");          // 重载解析到 (int, const char*)
    log_info("info");
    log_error("boom");
    return 0;
}
