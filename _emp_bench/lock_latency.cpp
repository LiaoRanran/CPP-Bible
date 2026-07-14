// lock_latency.cpp —— 实测原子 / 互斥锁 / futex 量级（ch93 §底层视角 声称）
// 编译: g++ -std=c++23 -O2 -pthread lock_latency.cpp -o lock_latency && ./lock_latency
// 测量目标:
//   atomic fetch_add(relaxed)     每迭代 ns
//   mutex 无争用 lock/unlock       每迭代 ns
//   （futex 争用等待在 Windows 无对应 syscall，标注为 Linux 量级，不本机编造）
#include <cstdio>
#include <cstddef>
#include <atomic>
#include <mutex>
#include <thread>
#include <chrono>
#include <vector>

static inline double per_op_ns(std::chrono::nanoseconds total, long long iters) {
    return total.count() / static_cast<double>(iters);
}

int main() {
    const long long N = 50'000'000LL;
    std::atomic<long long> cnt{0};
    std::mutex mtx;

    // ① atomic fetch_add relaxed
    {
        auto t0 = std::chrono::high_resolution_clock::now();
        for (long long i = 0; i < N; ++i) cnt.fetch_add(1, std::memory_order_relaxed);
        auto t1 = std::chrono::high_resolution_clock::now();
        std::printf("atomic fetch_add(relaxed) : %.3f ns/op  (x%lld 累加)\n",
                    per_op_ns(t1 - t0, N), N);
    }

    // ② mutex 无争用 lock/unlock
    {
        long long sink = 0;
        auto t0 = std::chrono::high_resolution_clock::now();
        for (long long i = 0; i < N; ++i) { std::lock_guard<std::mutex> lk(mtx); sink += i; }
        auto t1 = std::chrono::high_resolution_clock::now();
        std::printf("mutex 无争用 lock/unlock : %.3f ns/op  (x%lld, sink=%lld)\n",
                    per_op_ns(t1 - t0, N), N, sink);
    }

    // ③ 双线程争用下的 atomic fetch_add（测量争用退化，非 futex 但体现一致性流量）
    {
        cnt.store(0);
        const long long M = 20'000'000LL;
        auto worker = [&]() {
            for (long long i = 0; i < M; ++i) cnt.fetch_add(1, std::memory_order_relaxed);
        };
        auto t0 = std::chrono::high_resolution_clock::now();
        std::thread a(worker), b(worker);
        a.join(); b.join();
        auto t1 = std::chrono::high_resolution_clock::now();
        std::printf("atomic fetch_add(争用, 2线程) : %.3f ns/op  (x%lld/线程, 结果=%lld)\n",
                    per_op_ns(t1 - t0, M * 2), M, cnt.load());
    }

    // ④ 线程创建开销（clone + 栈分配，粗略量级）
    {
        const int K = 1000;
        auto t0 = std::chrono::high_resolution_clock::now();
        std::vector<std::thread> ts;
        ts.reserve(K);
        for (int i = 0; i < K; ++i) ts.emplace_back([]{ volatile int x = 0; x += 1; });
        for (auto& t : ts) t.join();
        auto t1 = std::chrono::high_resolution_clock::now();
        std::printf("std::thread 创建+join : %.1f us/线程  (x%d)\n",
                    per_op_ns(t1 - t0, K) / 1000.0, K);
    }
    return 0;
}
