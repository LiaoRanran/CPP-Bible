// _bench_d5_ch100_ranges.cpp — 附录 D5 基准：Ranges 算法与视图管道的真实开销（ch100）
// 编译:
//   C:/Qt/Tools/mingw1530_64/bin/g++.EXE -O2 -std=c++23 _bench_d5_ch100_ranges.cpp -o _bench_d5_ch100_ranges.exe
// 方法学:
//   - 每个场景跑 5 轮取中位数，单轮 >= 数十 ms
//   - 数据用运行期随机数填充，防止编译器闭式折叠
//   - 结果累加到 volatile sink，防止 DCE
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <numeric>
#include <random>
#include <ranges>
#include <vector>

using Clock = std::chrono::steady_clock;

static volatile std::uint64_t g_sink = 0;

static double ms_since(Clock::time_point t0) {
    return std::chrono::duration<double, std::milli>(Clock::now() - t0).count();
}

static double median5(double a[5]) {
    std::sort(a, a + 5);
    return a[2];
}

int main() {
    std::mt19937 rng(std::random_device{}());

    // ---------- 场景 1：ranges::sort vs std::sort（4M int，每轮重新洗牌相同序列） ----------
    constexpr std::size_t NS = 1u << 22; // 4M
    std::vector<int> base(NS);
    std::uniform_int_distribution<int> dist(0, 1 << 30);
    for (auto& v : base) v = dist(rng);

    double t_rsort[5], t_ssort[5];
    for (int r = 0; r < 5; ++r) {
        std::vector<int> a = base;               // 拷贝不计时? 计时含拷贝会掩盖差异 -> 拷贝后再计时
        auto t0 = Clock::now();
        std::ranges::sort(a);
        t_rsort[r] = ms_since(t0);
        g_sink += static_cast<std::uint64_t>(a[NS / 2]);
    }
    for (int r = 0; r < 5; ++r) {
        std::vector<int> a = base;
        auto t0 = Clock::now();
        std::sort(a.begin(), a.end());
        t_ssort[r] = ms_since(t0);
        g_sink += static_cast<std::uint64_t>(a[NS / 2]);
    }

    // ---------- 场景 2：filter|transform 管道 vs 手写循环 vs copy_if+transform ----------
    constexpr std::size_t NP = 1u << 24; // 16M
    std::vector<int> data(NP);
    std::uniform_int_distribution<int> d2(0, 100);
    for (auto& v : data) v = d2(rng);

    auto even = [](int x) { return x % 2 == 0; };
    auto sq   = [](int x) { return static_cast<std::uint64_t>(x) * x; };

    double t_pipe[5], t_hand[5], t_eager[5];
    for (int r = 0; r < 5; ++r) {
        auto t0 = Clock::now();
        std::uint64_t s = 0;
        for (auto v : data | std::views::filter(even) | std::views::transform(sq))
            s += v;
        g_sink += s;
        t_pipe[r] = ms_since(t0);
    }
    for (int r = 0; r < 5; ++r) {
        auto t0 = Clock::now();
        std::uint64_t s = 0;
        for (int x : data)
            if (x % 2 == 0) s += static_cast<std::uint64_t>(x) * x;
        g_sink += s;
        t_hand[r] = ms_since(t0);
    }
    for (int r = 0; r < 5; ++r) {
        auto t0 = Clock::now();
        std::vector<int> tmp;
        tmp.reserve(data.size());
        std::copy_if(data.begin(), data.end(), std::back_inserter(tmp), even);
        std::vector<std::uint64_t> tmp2(tmp.size());
        std::transform(tmp.begin(), tmp.end(), tmp2.begin(), sq);
        std::uint64_t s = std::accumulate(tmp2.begin(), tmp2.end(), std::uint64_t{0});
        g_sink += s;
        t_eager[r] = ms_since(t0);
    }

    // ---------- 场景 3：views::iota 惰性序列 vs 预填充 vector ----------
    constexpr std::uint64_t NI = 200'000'000; // 2e8
    volatile std::uint64_t vlimit = NI;       // 运行期才知道上界, 防闭式折叠
    double t_iota[5], t_vecfill[5];
    for (int r = 0; r < 5; ++r) {
        const std::uint64_t lim = vlimit;
        auto t0 = Clock::now();
        std::uint64_t s = 0;
        for (auto v : std::views::iota(std::uint64_t{0}, lim))
            s += v ^ (v >> 3);
        g_sink += s;
        t_iota[r] = ms_since(t0);
    }
    {
        // 预填充放在计时外只做一次? 不—对比目标是"预填充 + 遍历"整体成本
    }
    for (int r = 0; r < 5; ++r) {
        const std::uint64_t lim = vlimit;
        auto t0 = Clock::now();
        std::vector<std::uint64_t> seq(lim);
        std::iota(seq.begin(), seq.end(), std::uint64_t{0});
        std::uint64_t s = 0;
        for (auto v : seq) s += v ^ (v >> 3);
        g_sink += s;
        t_vecfill[r] = ms_since(t0);
    }

    auto report = [](const char* name, double t[5]) {
        double c[5] = { t[0], t[1], t[2], t[3], t[4] };
        std::printf("%-36s rounds: %8.3f %8.3f %8.3f %8.3f %8.3f  median: %8.3f ms\n",
                    name, t[0], t[1], t[2], t[3], t[4], median5(c));
    };
    std::printf("-- scenario 1: sort 4M random int --\n");
    report("std::ranges::sort", t_rsort);
    report("std::sort", t_ssort);
    std::printf("\n-- scenario 2: filter+transform over 16M int --\n");
    report("views::filter|transform (lazy)", t_pipe);
    report("hand-written loop", t_hand);
    report("copy_if + transform (eager, tmp)", t_eager);
    std::printf("\n-- scenario 3: iota 0..2e8, sum of v^(v>>3) --\n");
    report("views::iota (lazy)", t_iota);
    report("vector prefill + iota + loop", t_vecfill);

    std::printf("\nsink=%llu\n", static_cast<unsigned long long>(g_sink));
    return 0;
}
