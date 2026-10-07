// [redacted]
// [redacted]
// [redacted]
#include <cstdio>
#include <thread>

int g = 0;                       // 非原子全局

void worker() {
    for (int i = 0; i < 1'000'000; ++i) ++g;   // ❌ 与另一线程并发写，无同步
}

int main() {
    std::thread a(worker), b(worker);
    a.join(); b.join();
    std::printf("g = %d  (期望 2000000，但可能更少)\n", g);
    return 0;
}
