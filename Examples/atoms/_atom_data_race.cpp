// Examples/atoms/_atom_data_race.cpp
// CONC-003 夹具：数据竞争是未定义行为（UB），TSan 可检测但有边界。
//
// 唯一变量 = 是否存在数据竞争（有竞争 vs 无竞争对照）；活性对照 = 单线程基线。
// 打印口径：只输出确定性 key=value（循环上界决定的操作数），绝不打印数据竞争的
// 非确定终值——终值的"错"由 TSan（手动 WSL 复算，见证据卡 drill_note）证明，而非
// 由 stdout 断言（非确定值会让 replay 双平台失配）。
//
// -DBENCH_FULL：额外打印诊断行（scenario= / kIters=），不影响 run_match_keys。

#include <atomic>
#include <cstdio>
#include <chrono>
#include <thread>
#include <vector>

static const int kIters = 100000;

// 数据竞争载体：非原子 int，两个线程无同步并发读写 => 教科书式 data race。
static int g_shared = 0;
// 无竞争对照载体：原子 int，语义等价但受 happens-before 保护。
static std::atomic<int> g_atomic{0};

// 场景1：单线程基线（无竞争），确定性 local 累加。
// __attribute__((noinline))：防止 -O2 把负载内联进 main 而让其在工件中"消失"
// （符号断言需稳定命中），不改变任何竞争语义。
__attribute__((noinline)) void bench_single() {
    int local = 0;
    for (int i = 0; i < kIters; ++i) local += 1;
    std::printf("single_total=%d\n", local);
}

// 场景2：有数据竞争——两线程并发写 g_shared，零同步原语。
// 起手 1ms 延迟拉宽并发窗口，确保 TSan 稳定观测到竞争（而非偶发错开）。
__attribute__((noinline)) void bench_race() {
    g_shared = 0;
    std::thread a([]() {
        for (int i = 0; i < kIters; ++i) g_shared += 1;
    });
    std::thread b([]() {
        std::this_thread::sleep_for(std::chrono::milliseconds(1));
        for (int i = 0; i < kIters; ++i) g_shared += 1;
    });
    a.join();
    b.join();
    // 不打印 g_shared 终值（数据竞争 => 非确定），只打印确定性操作数。
    std::printf("race_ops_total=%d\n", 2 * kIters);
}

// 场景3：无数据竞争——同一语义用 std::atomic 保护（happens-before 成立）。
__attribute__((noinline)) void bench_safe() {
    g_atomic.store(0, std::memory_order_relaxed);
    std::thread a([]() {
        for (int i = 0; i < kIters; ++i)
            g_atomic.fetch_add(1, std::memory_order_relaxed);
    });
    std::thread b([]() {
        for (int i = 0; i < kIters; ++i)
            g_atomic.fetch_add(1, std::memory_order_relaxed);
    });
    a.join();
    b.join();
    std::printf("safe_ops_total=%d\n", 2 * kIters);
    std::printf("safe_final=%d\n", g_atomic.load());   // 确定性 = 2*kIters
}

int main() {
    bench_single();
    bench_race();
    bench_safe();
#ifdef BENCH_FULL
    std::printf("scenario=single|race|safe\n");
    std::printf("kIters=%d\n", kIters);
#endif
    return 0;
}
