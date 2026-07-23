// 真实并发基准: 高频共享计数器的 4 种实现, 在 1/2/4/8 线程下的吞吐对决
// 编译器: mingw1530 GCC 15.3.0 ; 编译: -O2 -std=c++17 -pthread -static
// 目的: 把 ch107 演绎1(计数器选型)从定性变成可量化实证:
//   (1) std::mutex + long          —— 锁保护
//   (2) std::atomic<long> seq_cst   —— fetch_add(memory_order_seq_cst) -> lock xadd
//   (3) std::atomic<long> relaxed    —— fetch_add(memory_order_relaxed)
//   (4) 分片计数(每线程独立 cache-line 对齐计数器, 读时求和) —— 零争用
//
// 所有实现完成相同的总增量数 N; 测并行段吞吐(ops/sec). 用原子 start 旗隔离线程创建开销.
#include <atomic>
#include <mutex>
#include <thread>
#include <vector>
#include <iostream>
#include <chrono>
#include <numeric>
#include <cstdio>

static double now() {
    return std::chrono::duration<double>(std::chrono::steady_clock::now().time_since_epoch()).count();
}

static const long N = 50'000'000;   // 总增量数(跨所有线程固定)

// ---- 策略1: mutex ----
void bench_mutex(int T, double& secs, long& result) {
    std::mutex m;
    long c = 0;
    std::atomic<bool> start{false};
    std::vector<std::thread> th(T);
    for (int t = 0; t < T; ++t)
        th[t] = std::thread([&, t] {
            while (!start.load(std::memory_order_acquire)) std::this_thread::yield();
            long l = 0;
            for (long i = 0; i < N / T; ++i) { std::lock_guard<std::mutex> g(m); l += 1; }
            // 避免 l 被优化: 用原子累加进 c 的副本无关, 这里直接加回 c 末态由主线程汇总
            (void)l;
            // 末态: 各线程把本地累计加进 c (仅一次, 不算热点)
            std::lock_guard<std::mutex> g(m); c += l;
        });
    double t0 = now();
    start.store(true, std::memory_order_release);
    for (auto& x : th) x.join();
    double t1 = now();
    secs = t1 - t0; result = c;
}

// ---- 策略2/3: atomic (seq_cst / relaxed) ----
void bench_atomic(int T, std::memory_order mo, double& secs, long& result) {
    std::atomic<long> c{0};
    std::atomic<bool> start{false};
    std::vector<std::thread> th(T);
    for (int t = 0; t < T; ++t)
        th[t] = std::thread([&, t] {
            while (!start.load(std::memory_order_acquire)) std::this_thread::yield();
            for (long i = 0; i < N / T; ++i) c.fetch_add(1, mo);
        });
    double t0 = now();
    start.store(true, std::memory_order_release);
    for (auto& x : th) x.join();
    double t1 = now();
    secs = t1 - t0; result = c.load();
}

// ---- 策略4: 分片计数 (每线程独立 cache-line 对齐计数器, atomic_ref 真实 RMW) ----
// 注意: 若用裸 `l += 1` 局部累加, -O2 会把循环强度削减成 `l = N/T` 单条赋值(循环被优化没),
//      导致吞吐虚高几个数量级. 用 std::atomic_ref 落在每线程私有槽, 既是真实内存 RMW
//      (不可消除), 又无跨线程缓存行争用 —— 这正是"分片"相对共享 atomic 的本质优势.
void bench_sharded(int T, double& secs, long& result) {
    struct alignas(64) Slot { long v = 0; };   // 每槽独占一条缓存行, 杜绝伪共享
    std::vector<Slot> slots(T);
    std::atomic<bool> start{false};
    std::vector<std::thread> th(T);
    for (int t = 0; t < T; ++t)
        th[t] = std::thread([&, t] {
            while (!start.load(std::memory_order_acquire)) std::this_thread::yield();
            std::atomic_ref<long> a(slots[t].v);
            for (long i = 0; i < N / T; ++i) a.fetch_add(1, std::memory_order_relaxed);
        });
    double t0 = now();
    start.store(true, std::memory_order_release);
    for (auto& x : th) x.join();
    double t1 = now();
    secs = t1 - t0;
    result = std::accumulate(slots.begin(), slots.end(), 0L,
                             [](long a, const Slot& s) { return a + s.v; });
}

int main() {
    const int Tarr[] = {1, 2, 4, 8};
    std::printf("=== 并发计数器基准: GCC 15.3.0 -O2 x86-64, N=%ld 总增量 ===\n\n", N);
    std::printf("T | mutex(M/s) | atomic_seqcst(M/s) | atomic_relaxed(M/s) | sharded(M/s)\n");
    std::printf("--+------------+-------------------+--------------------+-------------\n");
    for (int T : Tarr) {
        double s1, s2, s3, s4; long r1, r2, r3, r4;
        bench_mutex(T, s1, r1);
        bench_atomic(T, std::memory_order_seq_cst, s2, r2);
        bench_atomic(T, std::memory_order_relaxed, s3, r3);
        bench_sharded(T, s4, r4);
        auto mps = [&](double s, long r) {
            return (r == N) ? (N / s / 1e6) : -1.0;  // 校验和必须等于 N, 否则标 -1
        };
        std::printf("%d | %10.1f | %16.1f | %17.1f | %11.1f\n",
                    T, mps(s1, r1), mps(s2, r2), mps(s3, r3), mps(s4, r4));
    }
    std::printf("\n(M/s = 百万次增量/秒; 各策略末态和均应为 %ld, 否则数据竞争/优化失真)\n", N);
    return 0;
}
