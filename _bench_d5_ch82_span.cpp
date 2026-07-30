// _bench_d5_ch82_span.cpp — 附录 D5 基准：std::span 的真实开销（ch82）
// 编译:
//   C:/Qt/Tools/mingw1530_64/bin/g++.EXE -O2 -std=c++23 _bench_d5_ch82_span.cpp -o _bench_d5_ch82_span.exe
// 方法学:
//   - 每个场景跑 5 轮取中位数，单轮 >= 数十 ms
//   - 数据用运行期随机数填充（mt19937 + random_device 种子），防止编译器闭式折叠
//   - 结果累加到 volatile sink，防止 DCE
//   - 接口函数标记 __attribute__((noinline)) 模拟跨 TU 非内联调用边界
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <random>
#include <span>
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

// ---------- 场景 1：三种只读视图接口，跨调用边界求和 ----------
__attribute__((noinline))
std::uint64_t sum_span(std::span<const int> sp) {
    std::uint64_t s = 0;
    for (int v : sp) s += static_cast<std::uint32_t>(v);
    return s;
}

__attribute__((noinline))
std::uint64_t sum_vecref(const std::vector<int>& v) {
    std::uint64_t s = 0;
    for (int x : v) s += static_cast<std::uint32_t>(x);
    return s;
}

__attribute__((noinline))
std::uint64_t sum_ptr(const int* p, std::size_t n) {
    std::uint64_t s = 0;
    for (std::size_t i = 0; i < n; ++i) s += static_cast<std::uint32_t>(p[i]);
    return s;
}

// ---------- 场景 2：subspan 切片链 vs 手工指针偏移 ----------
__attribute__((noinline))
std::uint64_t consume_span32(std::span<const int> sp) {
    std::uint64_t s = 0;
    for (int v : sp) s += static_cast<std::uint32_t>(v);
    return s;
}

__attribute__((noinline))
std::uint64_t consume_ptr32(const int* p, std::size_t n) {
    std::uint64_t s = 0;
    for (std::size_t i = 0; i < n; ++i) s += static_cast<std::uint32_t>(p[i]);
    return s;
}

// ---------- 场景 3：静态 extent span<int,16> vs 动态 extent span<int> ----------
__attribute__((noinline))
std::uint64_t sum_fixed16(std::span<const int, 16> sp) {
    std::uint64_t s = 0;
    for (int v : sp) s += static_cast<std::uint32_t>(v);
    return s;
}

__attribute__((noinline))
std::uint64_t sum_dyn16(std::span<const int> sp) {
    std::uint64_t s = 0;
    for (int v : sp) s += static_cast<std::uint32_t>(v);
    return s;
}

int main() {
    std::printf("sizeof(span<const int>)    = %zu\n", sizeof(std::span<const int>));
    std::printf("sizeof(span<const int,16>) = %zu\n", sizeof(std::span<const int, 16>));

    constexpr std::size_t N = 1u << 24;   // 16M int = 64 MB
    std::vector<int> data(N);
    std::mt19937 rng(std::random_device{}());
    std::uniform_int_distribution<int> dist(0, 1000);
    for (auto& v : data) v = dist(rng);

    constexpr int REPS_BIG = 12;          // 场景 1：整块扫 12 遍/轮

    // --- 场景 1 ---
    // 注意: 每次调用前对数组做一次 volatile 写（值不变），
    // 否则 GCC 的 IPA pure-const 会把 12 次同参纯函数调用 CSE 成 1 次（实测被折叠过）。
    auto touch = [&data](int k) {
        volatile int* p = &data[static_cast<std::size_t>(k)];
        *p = *p;
    };
    double t_span[5], t_vec[5], t_ptr[5];
    for (int r = 0; r < 5; ++r) {
        auto t0 = Clock::now();
        std::uint64_t s = 0;
        for (int k = 0; k < REPS_BIG; ++k) { touch(k); s += sum_span(std::span<const int>(data)); }
        g_sink += s;
        t_span[r] = ms_since(t0);
    }
    for (int r = 0; r < 5; ++r) {
        auto t0 = Clock::now();
        std::uint64_t s = 0;
        for (int k = 0; k < REPS_BIG; ++k) { touch(k); s += sum_vecref(data); }
        g_sink += s;
        t_vec[r] = ms_since(t0);
    }
    for (int r = 0; r < 5; ++r) {
        auto t0 = Clock::now();
        std::uint64_t s = 0;
        for (int k = 0; k < REPS_BIG; ++k) { touch(k); s += sum_ptr(data.data(), data.size()); }
        g_sink += s;
        t_ptr[r] = ms_since(t0);
    }

    // --- 场景 2：对 64 元素窗口做 3 级切片链，取中间 32 个求和 ---
    // 切片链: subspan(16) -> first(48) -> subspan(0,32)... 等价手工: p+base+16, 长度 32
    constexpr std::size_t WIN = 64;
    const std::size_t nwin = N / WIN;
    double t_chain[5], t_manual[5];
    for (int r = 0; r < 5; ++r) {
        auto t0 = Clock::now();
        std::uint64_t s = 0;
        std::span<const int> whole(data);
        for (std::size_t w = 0; w < nwin; ++w) {
            auto sp = whole.subspan(w * WIN, WIN)   // 级 1
                           .subspan(16)             // 级 2: 去头 16
                           .first(32);              // 级 3: 取前 32
            s += consume_span32(sp);
        }
        g_sink += s;
        t_chain[r] = ms_since(t0);
    }
    for (int r = 0; r < 5; ++r) {
        auto t0 = Clock::now();
        std::uint64_t s = 0;
        const int* base = data.data();
        for (std::size_t w = 0; w < nwin; ++w) {
            s += consume_ptr32(base + w * WIN + 16, 32);
        }
        g_sink += s;
        t_manual[r] = ms_since(t0);
    }

    // --- 场景 3：按 16 元素块扫全数组，静态 extent vs 动态 extent ---
    const std::size_t nblk = N / 16;
    double t_fix[5], t_dyn[5];
    for (int r = 0; r < 5; ++r) {
        auto t0 = Clock::now();
        std::uint64_t s = 0;
        const int* base = data.data();
        for (std::size_t b = 0; b < nblk; ++b) {
            s += sum_fixed16(std::span<const int, 16>(base + b * 16, 16));
        }
        g_sink += s;
        t_fix[r] = ms_since(t0);
    }
    for (int r = 0; r < 5; ++r) {
        auto t0 = Clock::now();
        std::uint64_t s = 0;
        const int* base = data.data();
        for (std::size_t b = 0; b < nblk; ++b) {
            s += sum_dyn16(std::span<const int>(base + b * 16, 16));
        }
        g_sink += s;
        t_dyn[r] = ms_since(t0);
    }

    auto report = [](const char* name, double t[5]) {
        double c[5] = { t[0], t[1], t[2], t[3], t[4] };
        std::printf("%-34s rounds: %8.3f %8.3f %8.3f %8.3f %8.3f  median: %8.3f ms\n",
                    name, t[0], t[1], t[2], t[3], t[4], median5(c));
    };
    std::printf("\n-- scenario 1: whole-array sum via call boundary (12 passes/round, 16M int) --\n");
    report("span<const int>", t_span);
    report("const vector<int>&", t_vec);
    report("raw ptr + len", t_ptr);
    std::printf("\n-- scenario 2: 3-level subspan chain vs manual ptr offset (%zu windows) --\n", nwin);
    report("subspan chain (3 levels)", t_chain);
    report("manual ptr + offset", t_manual);
    std::printf("\n-- scenario 3: 16-elem blocks, static vs dynamic extent (%zu blocks) --\n", nblk);
    report("span<const int,16> (static)", t_fix);
    report("span<const int>    (dynamic)", t_dyn);

    std::printf("\nsink=%llu\n", static_cast<unsigned long long>(g_sink));
    return 0;
}
