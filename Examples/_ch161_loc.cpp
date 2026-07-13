// 文件：Examples/_ch161_loc.cpp
// 取证：g++ -std=c++20 -O2 真实编译运行（本机）
#include <cstdio>

// ⑪ 源码定位：__FILE__ / __LINE__ / __func__ 提供调用现场信息
// 用内联 + 完整路径处理，避免宏展开路径问题
inline void log_loc(const char* file, int line, const char* func, const char* msg) {
    std::printf("%s:%d %s : %s\n", file, line, func, msg);
}

#define LOG_LOC(msg) log_loc(__FILE__, __LINE__, __func__, msg)

void deep_call() {
    LOG_LOC("inside deep_call");
}

int main() {
    LOG_LOC("main start");
    deep_call();
    return 0;
}
