// [redacted]
// 规则：信号处理函数内只允许读写 `volatile sig_atomic_t` 或恰当次序的 std::atomic，
// [redacted]
// [redacted]
// [redacted]
#include <cstdio>
#include <csignal>

int counter = 0;                 // [redacted]

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
