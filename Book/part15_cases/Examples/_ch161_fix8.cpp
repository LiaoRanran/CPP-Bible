// 文件：Examples/_ch161_fix8.cpp
// 主题：⑨ 零开销关闭级别 —— 模板参数 + if constexpr 在编译期消除低级别
#include <cstdio>

constexpr int THR = 4;  // 4 == error：低于 error 的全部编译期消失

template <int L>
inline void log_at(const char* msg) {
    if constexpr (L >= THR) {
        std::printf("[lvl%d] %s\n", L, msg);
    }
    // else 分支：不产生任何指令
}

int main() {
    log_at<0>("compiled out");    // 编译期消除
    log_at<2>("compiled out");    // 编译期消除
    log_at<4>("critical kept");   // 仅此行保留
    return 0;
}
