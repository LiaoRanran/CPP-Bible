// UB-C3 non-atomic signal handler：在信号处理函数中修改非原子全局变量
// 规则：信号处理函数内只允许读写 `volatile sig_atomic_t` 或恰当次序的 std::atomic，
//       其余非原子读写与外部代码构成数据竞争（UB）。
// 编译: g++ -std=c++23 -O2 -o sig ub_signal_handler.cpp
// 复现 TSan: g++ -std=c++23 -O1 -g -fsanitize=thread -o sig_tsan ub_signal_handler.cpp
#include <cstdio>
#include <csignal>

int counter = 0;                 // ❌ 非原子，handler 与主流程并发访问 → UB

void handler(int) {
    ++counter;                   // ❌ 在信号上下文中修改非原子全局
}

int main() {
    std::signal(SIGINT, handler);
    for (int i = 0; i < 5; ++i) {
        std::raise(SIGINT);      // 同步投送信号，handler 内改 counter
    }
    std::printf("counter = %d\n", counter);
    return 0;
}
