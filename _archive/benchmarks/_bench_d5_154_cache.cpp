// _bench_d5_154_cache.cpp — ch154 缓存优化 D5 真实微基准（GCC 15.3.0, MinGW-w64）
// 编译：g++ -O2 -std=c++23 -pthread _bench_d5_154_cache.cpp -o _bench_d5_154_cache
// 场景 A：顺序 vs 随机遍历的缓存局部性（单线程，无 pthread 依赖）
// 场景 B：伪共享 false sharing（双线程，atomic relaxed，纯布局差异）
#include <atomic>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <random>
#include <thread>
#include <vector>

static double now_ms() {
    return std::chrono::duration<double, std::milli>(
               std::chrono::steady_clock::now().time_since_epoch())
        .count();
}

int main() {
    // ---------- 场景 A：顺序 vs 随机遍历 ----------
    const std::size_t N = 16'000'000;          // data 为 long long(8B) -> 128 MB > L3(64 MB)
    std::vector<long long> data(N);
    std::vector<std::size_t> order(N);
    for (std::size_t i = 0; i < N; ++i) { data[i] = static_cast<long long>(i); order[i] = i; }
    // 固定种子洗牌，保证可复现
    std::mt19937_64 rng(0x9e3779b97f4a7c15ULL);
    std::shuffle(order.begin(), order.end(), rng);

    const int ROUNDS = 5;
    double seq_best = 1e9, rnd_best = 1e9;
    volatile long long sink = 0;
    for (int r = 0; r < ROUNDS; ++r) {
        // 顺序：沿 data 连续取，预取器高效
        long long s = 0;
        double t0 = now_ms();
        for (std::size_t i = 0; i < N; ++i) s += data[i];
        double t1 = now_ms();
        // 随机：按洗牌后 order 跳访，缓存行利用率极低
        long long s2 = 0;
        double t2 = now_ms();
        for (std::size_t i = 0; i < N; ++i) s2 += data[order[i]];
        double t3 = now_ms();
        sink += s + s2;
        seq_best = std::min(seq_best, t1 - t0);
        rnd_best = std::min(rnd_best, t3 - t2);
    }
    double seq_ratio = rnd_best / seq_best;
    std::cout << "[A] 顺序遍历   : " << seq_best << " ms\n";
    std::cout << "[A] 随机遍历   : " << rnd_best << " ms\n";
    std::cout << "[A] 随机/顺序  : " << seq_ratio << " x (越大=缓存局部性越关键)\n";

    // ---------- 场景 B：伪共享 vs 缓存行对齐 ----------
    const std::size_t ITER = 200'000'000;      // 每线程自增次数
    // B1：相邻 atomic 落在同一缓存行 -> 伪共享
    struct Packed { std::atomic<long> a{0}; std::atomic<long> b{0}; };
    // B2：padding 到不同缓存行 -> 无伪共享
    struct Padded { std::atomic<long> a{0}; char pad[64]; std::atomic<long> b{0}; };

    auto run_pair = [&](auto& counters) -> double {
        double t0 = now_ms();
        std::thread t1([&]() { for (std::size_t i = 0; i < ITER; ++i) counters.a.fetch_add(1, std::memory_order_relaxed); });
        std::thread t2([&]() { for (std::size_t i = 0; i < ITER; ++i) counters.b.fetch_add(1, std::memory_order_relaxed); });
        t1.join(); t2.join();
        return now_ms() - t0;
    };

    Packed pk{};
    Padded pd{};
    double fs_best = 1e9, nf_best = 1e9;
    for (int r = 0; r < ROUNDS; ++r) {
        pk.a = pk.b = 0;
        pd.a = pd.b = 0;
        fs_best = std::min(fs_best, run_pair(pk));
        nf_best = std::min(nf_best, run_pair(pd));
    }
    double fs_ratio = fs_best / nf_best;
    std::cout << "[B] 伪共享(同缓存行) : " << fs_best << " ms\n";
    std::cout << "[B] 对齐(分缓存行)   : " << nf_best << " ms\n";
    std::cout << "[B] 伪共享/对齐      : " << fs_ratio << " x (伪共享惩罚)\n";
    std::cout << "[sanity] seq+rnd+sink=" << sink
              << " a=" << pk.a << "/" << pd.a << " b=" << pk.b << "/" << pd.b << std::endl;
    return 0;
}
