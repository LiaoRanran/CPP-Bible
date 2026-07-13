// 文件：Examples/_ch161_zerooverhead.cpp
// 取证：g++ -std=c++20 -O2 -S -masm=intel 提取汇编（产物 _ch161_asm.asm）
// ⑨ 零开销关闭级别：编译期把低于阈值的日志整体消除，运行时零成本

#include <cstdio>

// 编译期阈值（设为 off 时，低于 off 的日志在编译期被丢弃）
constexpr int COMPILE_THRESHOLD = 6;  // 6 == Level::off

// 编译期门控：不满足时函数体被优化消除
template <int L>
inline void log_if(int /*dummy*/, const char* msg) {
    if constexpr (L >= COMPILE_THRESHOLD) {
        std::printf("[lvl%d] %s\n", L, msg);
    }
    // else 分支不存在 -> 完全不生成任何指令
}

int main() {
    // 调用 trace/debug/info：编译期 L < 6 -> 不产生任何代码
    log_if<0>(0, "trace message (compiled out)");
    log_if<2>(0, "info message (compiled out)");
    // 只有 L >= 6（off/强制）才会落地
    log_if<6>(0, "forced critical message");
    return 0;
}
