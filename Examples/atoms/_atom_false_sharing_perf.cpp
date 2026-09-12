// ATOM-MEM-PERF-004 夹具二：伪共享的**性能倍数**（tight vs padded 布局）。
//
// 场景：kThreads 个线程各自把自己的计数器累加 kIters 次（**逻辑上完全独立**，无数据竞争）。
//   tight  —— 计数器数组相邻 ⇒ 多个计数器落在**同一缓存行** ⇒ 缓存行在核间来回弹（伪共享）
//   padded —— 每个计数器独占一条缓存行（alignas + 填充）⇒ 无伪共享
// 唯一变量 = 布局（线程数/迭代数/优化档/编译器全部相同）。
//
// 输出分层（PERF-003 教训）：
//   默认：常量 + **方向性结论**（tight 是否更慢）—— 方向由伪共享机制决定，跨机器稳定；
//   -DBENCH_FULL：逐轮耗时、中位数、比值 —— 时序数据，跨机器不可复现，只作留痕。
#include <algorithm>
#include <atomic>
#include <chrono>
#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <thread>
#include <vector>

namespace {

#ifdef __cpp_lib_hardware_interference_size
constexpr std::size_t kLine = std::hardware_destructive_interference_size;
#else
constexpr std::size_t kLine = 64;               // 回退值（并打印回退标记）
#endif

constexpr int       kThreads = 4;
constexpr long long kIters   = 10000000;        // 每线程 1e7 次累加
constexpr int       kRounds  = 7;               // 奇数 ⇒ 中位数取得到

struct Tight {
    std::atomic<long long> c[kThreads];         // 相邻 ⇒ 共享缓存行
};

struct alignas(kLine) Padded {
    std::atomic<long long> c;
    char pad[kLine - sizeof(std::atomic<long long>)]{};
};

using Clock = std::chrono::steady_clock;

template <class Launch>
long long one_round(Launch launch) {
    std::vector<std::thread> ts;
    ts.reserve(kThreads);
    const auto t0 = Clock::now();
    for (int i = 0; i < kThreads; ++i) ts.emplace_back(launch(i));
    for (auto& t : ts) t.join();
    const auto t1 = Clock::now();
    return std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count();
}

long long median_of(std::vector<long long> v) {
    std::sort(v.begin(), v.end());
    return v[v.size() / 2];
}

}  // namespace

int main() {
    Tight tight;
    std::vector<Padded> padded(kThreads);

    const auto tight_launch = [&tight](int i) {
        return std::thread([&tight, i] {
            for (long long k = 0; k < kIters; ++k)
                tight.c[i].fetch_add(1, std::memory_order_relaxed);
        });
    };
    const auto padded_launch = [&padded](int i) {
        return std::thread([&padded, i] {
            for (long long k = 0; k < kIters; ++k)
                padded[i].c.fetch_add(1, std::memory_order_relaxed);
        });
    };

    std::vector<long long> tv, pv;
    for (int r = 0; r < kRounds; ++r) {
        tv.push_back(one_round(tight_launch));
        pv.push_back(one_round(padded_launch));
    }
    const long long tmed = median_of(tv), pmed = median_of(pv);

    std::printf("threads=%d\n", kThreads);
    std::printf("iters_per_thread=%lld\n", kIters);
    std::printf("rounds=%d\n", kRounds);
    std::printf("cache_line_size=%zu\n", kLine);
    std::printf("tight_stride_bytes=%zu\n", sizeof(std::atomic<long long>));
    std::printf("padded_stride_bytes=%zu\n", sizeof(Padded));
    std::printf("tight_shares_line=%d\n", (sizeof(std::atomic<long long>) < kLine) ? 1 : 0);
    // 红队阻断 1 的修法：初版写 `(sizeof(Padded) > kLine) ? 0 : 0` —— 三元两支都是字面量 0，
    // 条件被完全忽略（工件实证为 `xor edx, edx` + 常量），"padded 侧不共享缓存行"这一**唯一变量成立的前提**
    // 当时是夹具自己写死的 0。现改为**真地址判定**。
    std::printf("padded_shares_line=%d\n",
                (reinterpret_cast<std::uintptr_t>(&padded[1]) / kLine
                 == reinterpret_cast<std::uintptr_t>(&padded[0]) / kLine) ? 1 : 0);
    // ↓↓↓ 方向性结论（断言锚：伪共享的因果方向，跨机器稳定）
    // ↓↓↓ 活性对照：四个计数器都真的被推进过（与跑了几轮无关；某线程未启动或循环被优化掉则为 0）
    //     （初版写的是 `sum == kThreads*kIters`——但 tight 对象跨 14 次调用累积，该式**必然为假**：
    //      这是"对照写错基数"的同类问题，与 EV-MEM-039 的中位数基数 bug 同源，已改为不依赖轮数的判据。）
    std::printf("sharing_is_slower=%d\n", (tmed > pmed) ? 1 : 0);
    std::printf("counters_all_advanced=%d\n",
                (tight.c[0] > 0 && tight.c[1] > 0 && tight.c[2] > 0 && tight.c[3] > 0) ? 1 : 0);

#ifdef BENCH_FULL
    std::printf("tight_samples_ns=");
    for (std::size_t i = 0; i < tv.size(); ++i) std::printf("%s%lld", i ? "," : "", tv[i]);
    std::printf("\n");
    std::printf("padded_samples_ns=");
    for (std::size_t i = 0; i < pv.size(); ++i) std::printf("%s%lld", i ? "," : "", pv[i]);
    std::printf("\n");
    std::printf("tight_median_ns=%lld\n", tmed);
    std::printf("padded_median_ns=%lld\n", pmed);
    std::printf("tight_min_ns=%lld\n", *std::min_element(tv.begin(), tv.end()));
    std::printf("tight_max_ns=%lld\n", *std::max_element(tv.begin(), tv.end()));
    std::printf("padded_min_ns=%lld\n", *std::min_element(pv.begin(), pv.end()));
    std::printf("padded_max_ns=%lld\n", *std::max_element(pv.begin(), pv.end()));
    std::printf("ratio_tight_over_padded_x1000=%lld\n", pmed ? tmed * 1000 / pmed : 0);
#else
    (void)tmed;
    (void)pmed;
#endif
    return 0;
}
