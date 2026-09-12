// ATOM-MEM-PERF-003 夹具二：小对象分配器基准（三种分配策略，同一工作量）。
//
// 三种策略（全部来自标准库，不手写分配器 ⇒ 结论可被任何读者用同一标准复现）：
//   global    —— std::allocator（每次走全局 ::operator new / ::operator delete）
//   monotonic —— std::pmr::monotonic_buffer_resource（bump 指针，不回收）
//   pool      —— std::pmr::unsynchronized_pool_resource（定长块池，回收复用）
//
// 方法论纪律（PERF 类原子的通用准则）：
//   * 多轮（rounds）+ 每轮多次（iters）⇒ 取**中位数**，并报 min/max 显示方差；
//   * **输出分两层**：默认只打印「跨机器稳定」的量（常量 + 对比结论）——它们才是断言锚；
//     绝对纳秒、比值、逐轮样本是**时序数据、跨机器不可复现**，只在 `-DBENCH_FULL` 下打印
//     （供人读留痕；若混进默认输出，run_match 的逐字比对必然失败——本卡初版即栽在此处）；
//   * 每次分配都写入并读回（volatile 累加）⇒ 防止 -O2 把整个循环优化掉；
//   * 本夹具**不重载** operator new/delete（观测不改变被观测对象；也避开 P4 自证断言）。
//
// 输出纪律：每行 `标签=值`，值运行时算出，不写死期望（S3 会拦）。
#include <cstdio>
#include <chrono>
#include <cstddef>
#include <memory_resource>
#include <new>
#include <vector>

namespace {

constexpr std::size_t kIters  = 10000;      // 每轮分配/释放次数
constexpr std::size_t kRounds = 7;          // 轮数（奇数 ⇒ 中位数取得到）
constexpr std::size_t kBlock  = 64;         // 小对象尺寸（落在典型池块量级）

using Clock = std::chrono::steady_clock;

volatile std::size_t g_sink = 0;            // 防止优化掉

// 一轮：跑 kIters 次「分配 → 写 → 读回 → 释放」，返回耗时（纳秒）
template <class Alloc>
long long one_round(Alloc&& alloc) {
    const auto t0 = Clock::now();
    for (std::size_t i = 0; i < kIters; ++i) {
        void* p = alloc.allocate();
        auto* bytes = static_cast<unsigned char*>(p);
        bytes[0] = static_cast<unsigned char>(i);
        g_sink += bytes[0];
        alloc.deallocate(p);
    }
    const auto t1 = Clock::now();
    return std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count();
}

struct GlobalAlloc {
    void* allocate() { return ::operator new(kBlock); }
    void  deallocate(void* p) { ::operator delete(p); }
};

struct MonotonicAlloc {
    std::pmr::monotonic_buffer_resource r{1024 * 1024};
    void* allocate() { return r.allocate(kBlock, alignof(std::max_align_t)); }
    void  deallocate(void*) {}                    // bump 不回收：真实语义
};

struct PoolAlloc {
    std::pmr::unsynchronized_pool_resource r{};
    void* allocate() { return r.allocate(kBlock, alignof(std::max_align_t)); }
    void  deallocate(void* p) { r.deallocate(p, kBlock, alignof(std::max_align_t)); }
};

// 稳定性分层：`stable=true` 的那些读数在任何合理实现上都成立（常量 + 对比结论）；
// 其余（绝对耗时/比值/样本）是时序数据，只作留痕。
template <class A>
void run(const char* tag, A&& alloc, std::vector<long long>& out, long long& median) {
    for (std::size_t r = 0; r < kRounds; ++r) out.push_back(one_round(alloc));
    std::vector<long long> sorted = out;
    for (std::size_t i = 0; i < sorted.size(); ++i)
        for (std::size_t j = i + 1; j < sorted.size(); ++j)
            if (sorted[j] < sorted[i]) { const long long t = sorted[i]; sorted[i] = sorted[j]; sorted[j] = t; }
    // 断言（对比读数）与比值必须用**同一个基数**：排序后的中位数。
    // （初版把原始插入序的第 4 个样本当作 median 传给对比，而打印的 _median_ns 是排序后的中位数
    //   ⇒ 卡里的比值与"快 N 倍"用的是两套数，读者用卡里列的中位数永远算不出卡里引的比值。
    //   红队阻断 1 的修法即此。详见 EV-MEM-039 修订记录。）
    median = sorted[sorted.size() / 2];
#ifdef BENCH_FULL
    std::printf("%s_median_ns=%lld\n", tag, sorted[sorted.size() / 2]);
    std::printf("%s_min_ns=%lld\n", tag, sorted.front());
    std::printf("%s_max_ns=%lld\n", tag, sorted.back());
    std::printf("%s_samples_ns=", tag);
    for (std::size_t i = 0; i < out.size(); ++i)
        std::printf("%s%lld", i ? "," : "", out[i]);
    std::printf("\n");
#else
    (void)tag;
    (void)sorted;
#endif
}

}  // namespace

int main() {
    std::printf("iters_per_round=%zu\n", kIters);
    std::printf("rounds=%zu\n", kRounds);
    std::printf("block_bytes=%zu\n", kBlock);

    std::vector<long long> g, m, p;
    long long gmed = 0, mmed = 0, pmed = 0;
    run("global", GlobalAlloc{}, g, gmed);
    run("monotonic", MonotonicAlloc{}, m, mmed);
    run("pool", PoolAlloc{}, p, pmed);

#ifdef BENCH_FULL
    std::printf("ratio_monotonic_over_global_x1000=%lld\n", mmed * 1000 / gmed);
    std::printf("ratio_pool_over_global_x1000=%lld\n", pmed * 1000 / gmed);
    std::printf("ratio_pool_over_monotonic_x1000=%lld\n", pmed * 1000 / (mmed ? mmed : 1));
    const char* order = (gmed <= mmed && gmed <= pmed) ? "global"
                      : (mmed <= pmed)                   ? "monotonic"
                                                         : "pool";
    std::printf("fastest_median=%s\n", order);
    std::printf("monotonic_beats_pool=%d\n", (mmed < pmed) ? 1 : 0);
    // 对比结论**不是**跨环境稳定量：同一夹具实测在 MinGW/libstdc++ 上两种资源都胜过全局 new，
    // 而在 Linux/glibc 上三者**全部翻转**（glibc 的 tcache 让全局 new 极快）⇒ 只作留痕，不作断言锚。
    std::printf("both_pools_beat_global=%d\n", (mmed < gmed && pmed < gmed) ? 1 : 0);
    std::printf("monotonic_beats_global=%d\n", (mmed < gmed) ? 1 : 0);
    std::printf("pool_beats_global=%d\n", (pmed < gmed) ? 1 : 0);
#endif

    // ↓↓↓ 稳定层：只留跨环境真正稳定的量（常量 + 观测通路活性对照）
    //     断言锚必须窄：混入任何平台相关结论，都会让证据卡在另一个平台上 refute
    //     ——本卡初版与第二版都在此处栽过（先是时序数据、后是对比结论），见 EV-MEM-039 修订记录。
    std::printf("sink_nonzero=%d\n", g_sink != 0 ? 1 : 0);
    return 0;
}
