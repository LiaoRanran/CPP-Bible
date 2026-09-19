// _bench_d5_ch95_stl_algorithms.cpp
// STL 算法选择的真实性能影响基准
// 编译: g++ -O2 -std=c++23 _bench_d5_ch95_stl_algorithms.cpp -o _bench_d5_ch95_stl_algorithms.exe
// 运行: ./_bench_d5_ch95_stl_algorithms.exe

#include <algorithm>
#include <numeric>
#include <vector>
#include <random>
#include <chrono>
#include <cstdio>
#include <cstring>
#include <cstddef>

#ifdef _WIN32
#include <windows.h>
#endif

// volatile sink — 阻止编译器优化掉计算结果
static volatile long g_sink_long = 0;
static volatile int g_sink_int = 0;
static volatile void* g_sink_ptr = nullptr;

// 随机数生成器
static std::mt19937 rng(42);

// 计时辅助
using Clock = std::chrono::steady_clock;

template<typename Func>
static double measure_ms(Func&& f, int rounds) {
    double times[64];
    for (int r = 0; r < rounds; ++r) {
        auto t0 = Clock::now();
        f();
        auto t1 = Clock::now();
        times[r] = std::chrono::duration<double, std::milli>(t1 - t0).count();
    }
    // 取中位
    std::sort(times, times + rounds);
    return times[rounds / 2];
}

// ============================================================
// 场景 1: nth_element (O(n)) vs partial_sort (O(n log k)) vs sort (O(n log n))
// 取 Top-K (k=100)，N=2,000,000
// ============================================================
static void bench1_topk() {
    constexpr int N = 2'000'000;
    constexpr int K = 100;
    constexpr int ROUNDS = 5;

    std::printf("\n=== 场景 1: nth_element vs partial_sort vs sort (N=%d, K=%d) ===\n", N, K);

    // 准备原始数据（随机打乱）
    std::vector<int> base(N);
    for (int i = 0; i < N; ++i) base[i] = rng();

    // nth_element: O(n)，仅将第 K 大放到正确位置
    double t_nth = measure_ms([&]() {
        std::vector<int> v = base;
        std::nth_element(v.begin(), v.begin() + K, v.end(), std::greater<int>());
        g_sink_int = v[K];
    }, ROUNDS);

    // partial_sort: O(n log k)，前 K 个有序
    double t_partial = measure_ms([&]() {
        std::vector<int> v = base;
        std::partial_sort(v.begin(), v.begin() + K, v.end(), std::greater<int>());
        g_sink_int = v[K - 1];
    }, ROUNDS);

    // sort: O(n log n)，全排序后取前 K
    double t_sort = measure_ms([&]() {
        std::vector<int> v = base;
        std::sort(v.begin(), v.end(), std::greater<int>());
        g_sink_int = v[K - 1];
    }, ROUNDS);

    std::printf("  nth_element  : %8.2f ms  (O(n))\n", t_nth);
    std::printf("  partial_sort : %8.2f ms  (O(n log k))\n", t_partial);
    std::printf("  sort         : %8.2f ms  (O(n log n))\n", t_sort);
    std::printf("  加速比: nth_element/sort = %.2fx, partial_sort/sort = %.2fx\n",
                t_sort / t_nth, t_sort / t_partial);
}

// ============================================================
// 场景 2: partition (O(n)) vs sort + filter (O(n log n))
// 把满足条件的元素收集到前半部分，N=2,000,000
// ============================================================
static void bench2_partition() {
    constexpr int N = 2'000'000;
    constexpr int ROUNDS = 5;

    std::printf("\n=== 场景 2: partition vs sort+filter (N=%d) ===\n", N);

    std::vector<int> base(N);
    for (int i = 0; i < N; ++i) base[i] = rng() % 1000;

    auto pred = [](int x) { return x > 500; };

    // partition: O(n)，原地分区
    double t_part = measure_ms([&]() {
        std::vector<int> v = base;
        auto it = std::partition(v.begin(), v.end(), pred);
        g_sink_long = it - v.begin();
    }, ROUNDS);

    // sort + filter: O(n log n) 排序，再 copy_if 收集
    double t_sort_filter = measure_ms([&]() {
        std::vector<int> v = base;
        std::sort(v.begin(), v.end());
        std::vector<int> out;
        out.reserve(N / 2);
        std::copy_if(v.begin(), v.end(), std::back_inserter(out), pred);
        g_sink_long = out.size();
    }, ROUNDS);

    std::printf("  partition    : %8.2f ms  (O(n))\n", t_part);
    std::printf("  sort+filter  : %8.2f ms  (O(n log n))\n", t_sort_filter);
    std::printf("  加速比: sort+filter/partition = %.2fx\n", t_sort_filter / t_part);
}

// ============================================================
// 场景 3: std::find (O(n)) vs std::lower_bound (O(log n))
// 在有序数组中查找，N=2,000,000，重复查找 200 次取总量
// ============================================================
static void bench3_search() {
    constexpr int N = 2'000'000;
    constexpr int ROUNDS = 5;
    constexpr int QUERIES = 200;

    std::printf("\n=== 场景 3: find vs lower_bound (N=%d, %d queries) ===\n", N, QUERIES);

    // 用随机数填充后排序，避免编译器推导出确定性 pattern
    std::vector<int> sorted(N);
    for (int i = 0; i < N; ++i) sorted[i] = rng();
    std::sort(sorted.begin(), sorted.end());

    // 生成 200 个查询 key（一半命中，一半未命中）
    std::vector<int> keys(QUERIES);
    for (int i = 0; i < QUERIES; ++i) {
        if (i % 2 == 0) keys[i] = sorted[rng() % N];       // 命中
        else            keys[i] = rng();                     // 可能未命中
    }

    // std::find: O(n) 线性，每次扫描整个区间
    double t_find = measure_ms([&]() {
        long found = 0;
        for (int q = 0; q < QUERIES; ++q) {
            auto it = std::find(sorted.begin(), sorted.end(), keys[q]);
            if (it != sorted.end()) ++found;
        }
        g_sink_long = found;
    }, ROUNDS);

    // std::lower_bound: O(log n) 二分
    double t_lb = measure_ms([&]() {
        long found = 0;
        for (int q = 0; q < QUERIES; ++q) {
            auto it = std::lower_bound(sorted.begin(), sorted.end(), keys[q]);
            if (it != sorted.end() && *it == keys[q]) ++found;
        }
        g_sink_long = found;
    }, ROUNDS);

    std::printf("  find         : %8.2f ms  (%d queries, O(n) each)\n", t_find, QUERIES);
    std::printf("  lower_bound  : %8.4f ms  (%d queries, O(log n) each)\n", t_lb, QUERIES);
    std::printf("  加速比: find/lower_bound = %.0fx\n", t_find / t_lb);
}

// ============================================================
// 场景 4: std::accumulate vs 手写循环
// N=10,000,000
// ============================================================
static void bench4_accumulate() {
    constexpr int N = 10'000'000;
    constexpr int ROUNDS = 5;

    std::printf("\n=== 场景 4: accumulate vs hand-loop (N=%d) ===\n", N);

    std::vector<long> data(N);
    for (int i = 0; i < N; ++i) data[i] = rng() % 1000;

    // std::accumulate
    double t_acc = measure_ms([&]() {
        long s = std::accumulate(data.begin(), data.end(), 0L);
        g_sink_long = s;
    }, ROUNDS);

    // 手写循环
    double t_hand = measure_ms([&]() {
        long s = 0;
        for (size_t i = 0; i < data.size(); ++i) s += data[i];
        g_sink_long = s;
    }, ROUNDS);

    std::printf("  accumulate   : %8.2f ms\n", t_acc);
    std::printf("  hand-loop    : %8.2f ms\n", t_hand);
    std::printf("  比值: accumulate/hand-loop = %.3fx\n", t_acc / t_hand);
}

// ============================================================
// 场景 5: std::copy vs memcpy (trivially copyable)
// N=10,000,000 ints，预分配目标缓冲，仅测拷贝本身
// ============================================================
static void bench5_copy() {
    constexpr int N = 10'000'000;
    constexpr int ROUNDS = 5;

    std::printf("\n=== 场景 5: std::copy vs memcpy (N=%d ints, pre-allocated) ===\n", N);

    std::vector<int> src(N);
    for (int i = 0; i < N; ++i) src[i] = rng();

    // 预分配目标缓冲
    std::vector<int> dst(N);

    // std::copy（目标已分配，仅测拷贝）
    double t_copy = measure_ms([&]() {
        std::copy(src.begin(), src.end(), dst.begin());
        g_sink_int = dst[N / 2];
    }, ROUNDS);

    // memcpy
    double t_memcpy = measure_ms([&]() {
        std::memcpy(dst.data(), src.data(), N * sizeof(int));
        g_sink_int = dst[N / 2];
    }, ROUNDS);

    std::printf("  std::copy    : %8.2f ms\n", t_copy);
    std::printf("  memcpy       : %8.2f ms\n", t_memcpy);
    std::printf("  比值: copy/memcpy = %.3fx\n", t_copy / t_memcpy);
}

int main() {
#ifdef _WIN32
    // Windows: 确保高精度计时器可用
    LARGE_INTEGER freq;
    QueryPerformanceFrequency(&freq);
    std::printf("=== STL 算法性能基准 (D5) ===\n");
    std::printf("平台: Windows / MinGW-w64\n");
#else
    std::printf("=== STL 算法性能基准 (D5) ===\n");
    std::printf("平台: Linux/Unix\n");
#endif
    std::printf("编译器: GCC 15.3.0, -O2 -std=c++23\n");
    std::printf("方法: 5 轮取中位, volatile sink\n");

    bench1_topk();
    bench2_partition();
    bench3_search();
    bench4_accumulate();
    bench5_copy();

    std::printf("\n=== 基准完成 ===\n");
    return 0;
}
