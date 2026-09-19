// _bench_d5_98_heap.cpp — ch98 堆算法：Top-K 的四种策略与堆排序
// g++ -O2 -std=c++23
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <vector>
#include <queue>
#include <algorithm>
#include <functional>
#include <random>

static double now_ms() {
    using namespace std::chrono;
    return duration<double, std::milli>(steady_clock::now().time_since_epoch()).count();
}
template <class F>
static double bench(const char* name, F&& f) {
    std::vector<double> t;
    for (int r = 0; r < 5; ++r) { double t0 = now_ms(); f(); t.push_back(now_ms() - t0); }
    std::sort(t.begin(), t.end());
    std::printf("%-40s %10.3f ms\n", name, t[2]);
    return t[2];
}
volatile std::uint64_t g_sink;

int main() {
    constexpr std::size_t N = 10'000'000;
    constexpr std::size_t K = 100;

    std::vector<int> base(N);
    std::mt19937 rng(42);
    for (auto& v : base) v = int(rng());

    std::uint64_t k1 = 0, k2 = 0, k3 = 0, k4 = 0;
    auto sumTopK = [&](const std::vector<int>& top) {
        std::uint64_t s = 0;
        for (std::size_t i = 0; i < K; ++i) s += std::uint64_t(std::uint32_t(top[i]));
        return s;
    };

    // 1) 全量 sort 后取前 K —— O(N log N)
    bench("topK: full std::sort", [&] {
        auto v = base;
        std::sort(v.begin(), v.end(), std::greater<>());
        v.resize(K);
        k1 = sumTopK(v); g_sink = k1;
    });
    // 2) nth_element 分区 + 对 K 个排序 —— O(N)+O(K log K)
    bench("topK: nth_element + sort K", [&] {
        auto v = base;
        std::nth_element(v.begin(), v.begin() + K, v.end(), std::greater<>());
        std::sort(v.begin(), v.begin() + K, std::greater<>());
        v.resize(K);
        k2 = sumTopK(v); g_sink = k2;
    });
    // 3) partial_sort（内部即堆算法）—— O(N log K)
    bench("topK: std::partial_sort", [&] {
        auto v = base;
        std::partial_sort(v.begin(), v.begin() + K, v.end(), std::greater<>());
        v.resize(K);
        k3 = sumTopK(v); g_sink = k3;
    });
    // 4) 流式 K-小顶堆（priority_queue<greater>）—— 单遍，内存 O(K)
    bench("topK: streaming K-min-heap", [&] {
        std::priority_queue<int, std::vector<int>, std::greater<>> pq;
        for (int v : base) {
            if (pq.size() < K) pq.push(v);
            else if (v > pq.top()) { pq.pop(); pq.push(v); }
        }
        std::vector<int> top;
        while (!pq.empty()) { top.push_back(pq.top()); pq.pop(); }
        std::sort(top.begin(), top.end(), std::greater<>());
        k4 = sumTopK(top); g_sink = k4;
    });
    std::printf("topK checksums: %llu %llu %llu %llu (must equal)\n",
                (unsigned long long)k1, (unsigned long long)k2,
                (unsigned long long)k3, (unsigned long long)k4);

    // 5) 手工堆排序（make_heap + 逐个 pop_heap） vs introsort
    bench("heapsort: make_heap+pop_heap", [&] {
        auto v = base;
        std::make_heap(v.begin(), v.end());
        for (auto it = v.end(); it != v.begin(); --it) std::pop_heap(v.begin(), it);
        g_sink = std::uint64_t(std::uint32_t(v[N / 2]));
    });
    bench("introsort: std::sort", [&] {
        auto v = base;
        std::sort(v.begin(), v.end());
        g_sink = std::uint64_t(std::uint32_t(v[N / 2]));
    });
    return 0;
}
