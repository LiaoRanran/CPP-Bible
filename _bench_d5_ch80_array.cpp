// _bench_d5_ch80_array.cpp
// ch80 std::array — 真实基准
// 编译: g++ -O2 -std=c++23 _bench_d5_ch80_array.cpp -o bench_ch80
// 维度:
//   1) 顺序遍历求和: C 数组 vs std::array vs std::vector (同容量, 运行期随机数据)
//   2) operator[] vs .at() (边界检查成本)
//   3) 小 array 按值传参 vs 按 const 引用传参 (跨 noinline 边界)
//   4) 每次迭代新建 栈上 std::array vs 堆上 std::vector (创建+销毁成本)
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <random>
#include <vector>

using Clock = std::chrono::steady_clock;

static volatile std::uint64_t g_sink = 0;

template <typename F>
double run_median_ms(const char* name, F&& f) {
    double times[5];
    for (int r = 0; r < 5; ++r) {
        auto t0 = Clock::now();
        std::uint64_t result = f();
        auto t1 = Clock::now();
        g_sink = g_sink + result;
        times[r] = std::chrono::duration<double, std::milli>(t1 - t0).count();
    }
    std::sort(times, times + 5);
    std::cout << name << ": [";
    for (int r = 0; r < 5; ++r) std::cout << times[r] << (r < 4 ? " " : "");
    std::cout << "] median=" << times[2] << " ms" << std::endl;
    return times[2];
}

constexpr std::size_t N = 4'000'000;
constexpr int REP = 25;

// 大数组放静态存储, 避免爆栈
static std::uint32_t c_arr[N];
static std::array<std::uint32_t, N> std_arr;

// ---- 维度 3: 按值 vs 按引用 (noinline 制造真实调用边界) ----
using Small = std::array<std::uint32_t, 16>; // 64 字节
__attribute__((noinline)) std::uint64_t sum_by_value(Small a) {
    std::uint64_t s = 0;
    for (auto v : a) s += v;
    return s;
}
__attribute__((noinline)) std::uint64_t sum_by_ref(const Small& a) {
    std::uint64_t s = 0;
    for (auto v : a) s += v;
    return s;
}

int main() {
    std::mt19937 rng(80808080);

    std::cout << "=== ch80 std::array bench (N=" << N << ", REP=" << REP
              << ") ===" << std::endl;

    std::vector<std::uint32_t> vec(N);
    for (std::size_t i = 0; i < N; ++i) {
        std::uint32_t x = rng();
        c_arr[i] = x;
        std_arr[i] = x;
        vec[i] = x;
    }

    // ---- 维度 1: 顺序求和 ----
    double t_c = run_median_ms("1a C array sum        ", [&] {
        std::uint64_t s = 0;
        for (int rep = 0; rep < REP; ++rep)
            for (std::size_t i = 0; i < N; ++i) s += c_arr[i];
        return s;
    });
    double t_a = run_median_ms("1b std::array sum     ", [&] {
        std::uint64_t s = 0;
        for (int rep = 0; rep < REP; ++rep)
            for (std::size_t i = 0; i < N; ++i) s += std_arr[i];
        return s;
    });
    double t_v = run_median_ms("1c std::vector sum    ", [&] {
        std::uint64_t s = 0;
        for (int rep = 0; rep < REP; ++rep)
            for (std::size_t i = 0; i < N; ++i) s += vec[i];
        return s;
    });

    // ---- 维度 2: operator[] vs .at() ----
    double t_idx = run_median_ms("2a array operator[]   ", [&] {
        std::uint64_t s = 0;
        for (int rep = 0; rep < REP; ++rep)
            for (std::size_t i = 0; i < N; ++i) s += std_arr[i];
        return s;
    });
    double t_at = run_median_ms("2b array .at()        ", [&] {
        std::uint64_t s = 0;
        for (int rep = 0; rep < REP; ++rep)
            for (std::size_t i = 0; i < N; ++i) s += std_arr.at(i);
        return s;
    });

    // ---- 维度 3: 按值 vs 按引用 ----
    constexpr std::size_t CALLS = 20'000'000;
    Small small{};
    for (auto& v : small) v = rng();

    double t_byval = run_median_ms("3a pass by value 64B  ", [&] {
        std::uint64_t s = 0;
        for (std::size_t c = 0; c < CALLS; ++c) {
            small[0] = static_cast<std::uint32_t>(c); // 每次变化防缓存结果
            s += sum_by_value(small);
        }
        return s;
    });
    double t_byref = run_median_ms("3b pass by const ref  ", [&] {
        std::uint64_t s = 0;
        for (std::size_t c = 0; c < CALLS; ++c) {
            small[0] = static_cast<std::uint32_t>(c);
            s += sum_by_ref(small);
        }
        return s;
    });

    // ---- 维度 4: 栈 array vs 堆 vector 创建+销毁 ----
    constexpr std::size_t CREATE_CALLS = 2'000'000;
    constexpr std::size_t SZ = 64;
    std::vector<std::uint32_t> seed(SZ);
    for (auto& v : seed) v = rng();

    double t_stack = run_median_ms("4a stack std::array   ", [&] {
        std::uint64_t s = 0;
        for (std::size_t c = 0; c < CREATE_CALLS; ++c) {
            std::array<std::uint32_t, SZ> a;
            for (std::size_t i = 0; i < SZ; ++i) a[i] = seed[i] + static_cast<std::uint32_t>(c);
            for (std::size_t i = 0; i < SZ; ++i) s += a[i];
        }
        return s;
    });
    double t_heap = run_median_ms("4b heap std::vector   ", [&] {
        std::uint64_t s = 0;
        for (std::size_t c = 0; c < CREATE_CALLS; ++c) {
            std::vector<std::uint32_t> v(SZ);
            for (std::size_t i = 0; i < SZ; ++i) v[i] = seed[i] + static_cast<std::uint32_t>(c);
            for (std::size_t i = 0; i < SZ; ++i) s += v[i];
        }
        return s;
    });

    std::cout << "--- summary (medians, ms) ---" << std::endl;
    std::cout << "carr=" << t_c << " array=" << t_a << " vector=" << t_v << std::endl;
    std::cout << "idx=" << t_idx << " at=" << t_at << std::endl;
    std::cout << "byval=" << t_byval << " byref=" << t_byref << std::endl;
    std::cout << "stack_array=" << t_stack << " heap_vector=" << t_heap << std::endl;
    std::cout << "sink=" << g_sink << std::endl;
    return 0;
}
