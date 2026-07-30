// _bench_d5_ch70_tag_dispatch.cpp
// ch70 标签分发 — 真实基准（附录 D5 基准源码）
// 编译: C:/Qt/Tools/mingw1530_64/bin/g++.EXE -O2 -std=c++23 _bench_d5_ch70_tag_dispatch.cpp -o bench_ch70.exe
//
// 同一工作负载（按迭代器类别选 advance 策略）下对比四种"选路"机制:
//   T  = tag dispatch      (重载决议, 编译期)
//   C  = if constexpr      (编译期丢弃分支)
//   Rh = 运行期 if, 标志在内层循环外读取 (允许 loop unswitching)
//   Rv = 运行期 if, 每元素从 volatile 读标志 (禁止外提)
//   F  = 函数指针表分发    (运行期间接调用, 无法内联)
// 另用 vector(random_access) 与 list(bidirectional) 对照, 量化"选对策略"本身的收益。
//
// 方法学: 每子基准 5 轮取中位; volatile sink 逃逸结果防 DCE;
//         数据来自运行期 mt19937, 防止编译期折叠。
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <iterator>
#include <list>
#include <random>
#include <type_traits>
#include <vector>

using Clock = std::chrono::steady_clock;

static volatile std::uint64_t g_sink = 0;
static volatile int g_ra_flag = 1;   // 运行期才知道的"是否随机访问"
static volatile int g_tbl_idx = 1;   // 运行期才知道的函数指针表下标
static volatile std::ptrdiff_t g_stride = 64; // 运行期才知道的步长

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
    std::cout << name << ": [";
    for (int r = 0; r < 5; ++r) std::cout << times[r] << (r < 4 ? " " : "");
    std::cout << "] ";
    std::sort(times, times + 5);
    std::cout << "median=" << times[2] << " ms" << std::endl;
    return times[2];
}

// ---------------- 策略实现（两条真实策略，供运行期分发选用） ----------------
template <class It>
struct Ops {
    using cat = typename std::iterator_traits<It>::iterator_category;
    static constexpr bool is_ra =
        std::is_base_of_v<std::random_access_iterator_tag, cat>;

    // "最优"策略：随机访问一步到位，否则退化为逐步
    static void jump(It& it, std::ptrdiff_t n) {
        if constexpr (is_ra) { it += n; }
        else { while (n-- > 0) ++it; }
    }
    // "保守"策略：永远逐步 ++
    static void step(It& it, std::ptrdiff_t n) {
        while (n-- > 0) ++it;
    }
};

// ---------------- T: tag dispatch（经典重载 + 迭代器标签） ----------------
template <class It>
void adv_tag_impl(It& it, std::ptrdiff_t n, std::random_access_iterator_tag) {
    it += n;
}
template <class It>
void adv_tag_impl(It& it, std::ptrdiff_t n, std::input_iterator_tag) {
    while (n-- > 0) ++it;
}
template <class It>
inline void adv_tag(It& it, std::ptrdiff_t n) {
    adv_tag_impl(it, n, typename std::iterator_traits<It>::iterator_category{});
}

// ---------------- C: if constexpr ----------------
template <class It>
inline void adv_ce(It& it, std::ptrdiff_t n) {
    using cat = typename std::iterator_traits<It>::iterator_category;
    if constexpr (std::is_base_of_v<std::random_access_iterator_tag, cat>) {
        it += n;
    } else {
        while (n-- > 0) ++it;
    }
}

// ---------------- R: 运行期 if ----------------
template <class It>
inline void adv_rt(It& it, std::ptrdiff_t n, bool ra) {
    if (ra) Ops<It>::jump(it, n);
    else    Ops<It>::step(it, n);
}

// ---------------- F: 函数指针表 ----------------
template <class It>
using AdvFn = void (*)(It&, std::ptrdiff_t);

template <class It>
AdvFn<It> pick_fn(int idx) {
    static AdvFn<It> tbl[2] = { &Ops<It>::step, &Ops<It>::jump };
    return tbl[idx & 1];
}

int main() {
    std::mt19937 rng(777);

    // ===================== A: 分发机制自身开销（vector, 步长 1）=====================
    constexpr std::size_t NV = 1u << 20;   // 1M ints = 4MB
    constexpr int REPA = 60;
    std::vector<int> v(NV);
    for (auto& x : v) x = static_cast<int>(rng() & 0xFFFF);

    std::cout << "=== A: dispatch overhead, vector<int> N=" << NV
              << " stride=1 REP=" << REPA << " ===" << std::endl;

    double a_tag = run_median_ms("A-T  tag dispatch     ", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < REPA; ++r) {
            auto it = v.begin();
            for (std::size_t k = 0; k < NV; ++k) { s += *it; adv_tag(it, 1); }
        }
        return s;
    });
    double a_ce = run_median_ms("A-C  if constexpr     ", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < REPA; ++r) {
            auto it = v.begin();
            for (std::size_t k = 0; k < NV; ++k) { s += *it; adv_ce(it, 1); }
        }
        return s;
    });
    double a_rh = run_median_ms("A-Rh runtime if(hoist)", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < REPA; ++r) {
            bool ra = (g_ra_flag != 0);          // 每轮读一次，内层循环可 unswitch
            auto it = v.begin();
            for (std::size_t k = 0; k < NV; ++k) { s += *it; adv_rt(it, 1, ra); }
        }
        return s;
    });
    double a_rv = run_median_ms("A-Rv runtime if(vol)  ", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < REPA; ++r) {
            auto it = v.begin();
            for (std::size_t k = 0; k < NV; ++k) {
                s += *it;
                adv_rt(it, 1, g_ra_flag != 0);   // 每元素读 volatile，禁止外提
            }
        }
        return s;
    });
    double a_fp = run_median_ms("A-F  function ptr tbl ", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < REPA; ++r) {
            auto fn = pick_fn<std::vector<int>::iterator>(g_tbl_idx);
            auto it = v.begin();
            for (std::size_t k = 0; k < NV; ++k) { s += *it; fn(it, 1); }
        }
        return s;
    });

    // ===================== B: 选对策略的算法收益（vector, 步长 64）=====================
    constexpr std::ptrdiff_t STRIDE = 64;
    constexpr int REPB = 3000;
    const std::size_t steps = NV / STRIDE;

    std::cout << "=== B: strategy payoff, vector<int> stride=" << STRIDE
              << " steps/pass=" << steps << " REP=" << REPB << " ===" << std::endl;

    double b_tag = run_median_ms("B-T  tag dispatch -> += ", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < REPB; ++r) {
            auto it = v.begin();
            for (std::size_t k = 0; k < steps; ++k) { s += *it; adv_tag(it, STRIDE); }
        }
        return s;
    });
    double b_step = run_median_ms("B-S  forced ++ stepping ", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < REPB; ++r) {
            auto it = v.begin();
            for (std::size_t k = 0; k < steps; ++k) {
                s += *it;
                Ops<std::vector<int>::iterator>::step(it, STRIDE);
            }
        }
        return s;
    });

    // B2: 步长改为运行期未知（volatile），观察逐步循环能否仍被强度削减
    double b_step_dyn = run_median_ms("B-D  forced ++ (runtime n)", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < REPB; ++r) {
            const std::ptrdiff_t n = g_stride;   // 运行期才知道
            auto it = v.begin();
            for (std::size_t k = 0; k < steps; ++k) {
                s += *it;
                Ops<std::vector<int>::iterator>::step(it, n);
            }
        }
        return s;
    });

    // ===================== C: 弱迭代器对照（list, 步长 64）=====================
    constexpr std::size_t NL = 256u * 1024u;
    constexpr int REPC = 120;
    std::list<int> lst;
    for (std::size_t i = 0; i < NL; ++i) lst.push_back(static_cast<int>(rng() & 0xFFFF));
    const std::size_t lsteps = NL / STRIDE;

    std::cout << "=== C: list<int> (bidirectional) N=" << NL
              << " stride=" << STRIDE << " REP=" << REPC << " ===" << std::endl;

    double c_tag = run_median_ms("C-T  tag dispatch     ", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < REPC; ++r) {
            auto it = lst.begin();
            for (std::size_t k = 0; k < lsteps; ++k) { s += *it; adv_tag(it, STRIDE); }
        }
        return s;
    });
    double c_ce = run_median_ms("C-C  if constexpr     ", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < REPC; ++r) {
            auto it = lst.begin();
            for (std::size_t k = 0; k < lsteps; ++k) { s += *it; adv_ce(it, STRIDE); }
        }
        return s;
    });
    double c_rv = run_median_ms("C-Rv runtime if(vol)  ", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < REPC; ++r) {
            auto it = lst.begin();
            for (std::size_t k = 0; k < lsteps; ++k) {
                s += *it;
                adv_rt(it, STRIDE, g_ra_flag != 0);
            }
        }
        return s;
    });
    double c_fp = run_median_ms("C-F  function ptr tbl ", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < REPC; ++r) {
            auto fn = pick_fn<std::list<int>::iterator>(g_tbl_idx);
            auto it = lst.begin();
            for (std::size_t k = 0; k < lsteps; ++k) { s += *it; fn(it, STRIDE); }
        }
        return s;
    });

    std::cout << "--- summary (medians, ms) ---" << std::endl;
    std::cout << "A tag=" << a_tag << " ce=" << a_ce << " rt_hoist=" << a_rh
              << " rt_vol=" << a_rv << " fnptr=" << a_fp << std::endl;
    std::cout << "B tag_jump=" << b_tag << " forced_step=" << b_step
              << " forced_step_dyn=" << b_step_dyn << std::endl;
    std::cout << "C tag=" << c_tag << " ce=" << c_ce << " rt_vol=" << c_rv
              << " fnptr=" << c_fp << std::endl;
    std::cout << "sink=" << g_sink << std::endl;
    return 0;
}
