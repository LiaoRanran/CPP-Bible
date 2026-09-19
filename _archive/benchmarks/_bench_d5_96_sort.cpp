// _bench_d5_96_sort.cpp — ch96 D5: sort/stable_sort/partial_sort/nth_element 实测
// g++ -O2 -std=c++17
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <random>
#include <vector>

using Clock = std::chrono::steady_clock;
static double ms(Clock::time_point a, Clock::time_point b) {
    return std::chrono::duration<double, std::milli>(b - a).count();
}
template <class F> static double median5(F f) {
    std::vector<double> t;
    for (int i = 0; i < 5; ++i) t.push_back(f());
    std::sort(t.begin(), t.end());
    return t[2];
}
volatile long long g_sink = 0;

int main() {
    std::mt19937 rng(42);
    const int N = 4'000'000;
    std::vector<int> base(N);
    for (auto& x : base) x = (int)rng();

    auto run = [&](const char* tag, const std::vector<int>& src, auto&& algo) {
        double t = median5([&] {
            std::vector<int> v = src;  // 拷贝在计时外? 不——统一含拷贝会掩盖差异。
            auto a = Clock::now();
            algo(v);
            auto b = Clock::now();
            g_sink = v[N / 2];
            return ms(a, b);
        });
        std::printf("%s,%.3f\n", tag, t);
        return t;
    };

    // ---- 随机数据 ----
    double t_sort = run("random,sort", base, [](std::vector<int>& v) { std::sort(v.begin(), v.end()); });
    double t_stab = run("random,stable_sort", base, [](std::vector<int>& v) { std::stable_sort(v.begin(), v.end()); });
    double t_part = run("random,partial_sort_top1000", base, [](std::vector<int>& v) { std::partial_sort(v.begin(), v.begin() + 1000, v.end()); });
    double t_nth  = run("random,nth_element_mid", base, [](std::vector<int>& v) { std::nth_element(v.begin(), v.begin() + v.size() / 2, v.end()); });
    double t_heap = run("random,make+sort_heap", base, [](std::vector<int>& v) { std::make_heap(v.begin(), v.end()); std::sort_heap(v.begin(), v.end()); });
    std::printf("ratios,stable=%.2f,partial=%.2f,nth=%.2f,heap=%.2f\n",
                t_stab / t_sort, t_sort / t_part, t_sort / t_nth, t_heap / t_sort);

    // ---- 已排序 / 逆排序 / 少量乱序（introsort 的适应性）----
    std::vector<int> asc = base;
    std::sort(asc.begin(), asc.end());
    std::vector<int> desc = asc;
    std::reverse(desc.begin(), desc.end());
    std::vector<int> nearly = asc;
    for (int i = 0; i < 100; ++i) {  // 0.0025% 扰动
        std::swap(nearly[rng() % N], nearly[rng() % N]);
    }
    double t_asc  = run("sorted_asc,sort", asc, [](std::vector<int>& v) { std::sort(v.begin(), v.end()); });
    double t_desc = run("sorted_desc,sort", desc, [](std::vector<int>& v) { std::sort(v.begin(), v.end()); });
    double t_near = run("nearly_sorted,sort", nearly, [](std::vector<int>& v) { std::sort(v.begin(), v.end()); });
    std::printf("adaptivity,asc_speedup=%.2f,desc_speedup=%.2f,nearly_speedup=%.2f\n",
                t_sort / t_asc, t_sort / t_desc, t_sort / t_near);

    // ---- 大元素（64B）：比较便宜/搬运贵 → stable_sort 的 buffer 策略差异 ----
    struct Big { int key; char pad[60]; };
    const int NB = 1'000'000;
    std::vector<Big> bigs(NB);
    for (auto& b : bigs) b.key = (int)rng();
    double b_sort = median5([&] {
        std::vector<Big> v = bigs;
        auto a = Clock::now();
        std::sort(v.begin(), v.end(), [](const Big& l, const Big& r) { return l.key < r.key; });
        auto e = Clock::now();
        g_sink = v[NB / 2].key;
        return ms(a, e);
    });
    double b_stab = median5([&] {
        std::vector<Big> v = bigs;
        auto a = Clock::now();
        std::stable_sort(v.begin(), v.end(), [](const Big& l, const Big& r) { return l.key < r.key; });
        auto e = Clock::now();
        g_sink = v[NB / 2].key;
        return ms(a, e);
    });
    std::printf("big64B_1M,sort,%.3f\n", b_sort);
    std::printf("big64B_1M,stable_sort,%.3f,ratio=%.2f\n", b_stab, b_stab / b_sort);
    return 0;
}
