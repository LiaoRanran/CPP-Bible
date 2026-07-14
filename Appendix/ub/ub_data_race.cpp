// UB-C1 data race：两个线程无同步地读写同一非原子变量 → 数据竞争（UB）
// 编译: g++ -std=c++23 -O2 -pthread -o dr ub_data_race.cpp
// 复现 TSan: g++ -std=c++23 -O1 -g -fsanitize=thread -pthread -o dr_tsan ub_data_race.cpp
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
