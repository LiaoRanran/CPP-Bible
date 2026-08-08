// _bench_d5_ch65_type_traits.cpp — ch65 type_traits：编译期分发对运行时性能的影响
// g++ -O2 -std=c++23 _bench_d5_ch65_type_traits.cpp -o bench_ch65
//
// 方法学：每个子基准跑 5 轮取中位；volatile sink 防 DCE；
// 循环体用依赖链使 sum 无闭式解，编译器无法把循环折叠成常数。
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <memory>
#include <random>
#include <string>
#include <type_traits>
#include <vector>

#if defined(_WIN32)
  #include <malloc.h>
#else
  #include <cstdlib>
#endif

// ── 计时工具 ──────────────────────────────────────────────
static double now_ms() {
    using namespace std::chrono;
    return duration<double, std::milli>(steady_clock::now().time_since_epoch()).count();
}

template <class F>
static double bench(const char* name, F&& f) {
    std::vector<double> t;
    for (int r = 0; r < 5; ++r) {
        double t0 = now_ms();
        f();
        t.push_back(now_ms() - t0);
    }
    std::vector<double> raw = t;
    std::sort(t.begin(), t.end());
    std::printf("%-52s median %9.3f ms   raw:", name, t[2]);
    for (double v : raw) std::printf(" %.3f", v);
    std::printf("\n");
    return t[2];
}

volatile std::uint64_t g_sink;
volatile void* g_escape;

// ── 场景 1 类型：is_trivially_copyable 分发 ────────────────
struct TrivialPod {            // trivially copyable
    int a;
    int b;
    long long c;
    long long d;
};
static_assert(std::is_trivially_copyable_v<TrivialPod>);

struct NonTrivial {            // 非平凡拷贝：自定义 copy ctor
    int a;
    int b;
    long long c;
    long long d;
    NonTrivial() = default;
    NonTrivial(const NonTrivial& o) : a(o.a), b(o.b), c(o.c), d(o.d) {}
    NonTrivial& operator=(const NonTrivial& o) {
        a = o.a; b = o.b; c = o.c; d = o.d;
        return *this;
    }
};
static_assert(!std::is_trivially_copyable_v<NonTrivial>);

// trait 驱动的通用 copy：trivially copyable → memcpy，否则逐元素
template <class T>
void trait_copy(T* dst, const T* src, std::size_t n) {
    if constexpr (std::is_trivially_copyable_v<T>) {
        std::memcpy(dst, src, n * sizeof(T));
    } else {
        for (std::size_t i = 0; i < n; ++i) dst[i] = src[i];
    }
}

// ── 场景 2：if constexpr vs runtime if ────────────────────
// runtime if 版本：条件是 volatile bool，编译器无法折叠
template <class T>
void runtime_if_copy(T* dst, const T* src, std::size_t n, bool use_memcpy) {
    if (use_memcpy) {
        std::memcpy(dst, src, n * sizeof(T));
    } else {
        for (std::size_t i = 0; i < n; ++i) dst[i] = src[i];
    }
}

// ── 场景 3：conditional_t 选择不同类型 ────────────────────
struct CompactPod {            // 8 bytes
    int a;
    int b;
};
struct PaddedPod {             // 64 bytes (alignas padding)
    alignas(64) int a;
    int b;
};
static_assert(sizeof(CompactPod) == 8);
static_assert(sizeof(PaddedPod) == 64);

// conditional_t 根据 trivially copyable 选择值存储或指针存储
template <class T>
using smart_storage_t = std::conditional_t<std::is_trivially_copyable_v<T>,
                                           T,
                                           std::shared_ptr<T>>;

// ── 场景 4：is_nothrow_move_constructible 与 vector 扩容 ──
struct NoexceptMove {
    int* data;
    std::size_t n;
    explicit NoexceptMove(std::size_t sz = 4) : data(new int[sz]), n(sz) {}
    ~NoexceptMove() { delete[] data; }
    NoexceptMove(const NoexceptMove& o) : data(new int[o.n]), n(o.n) {
        std::memcpy(data, o.data, n * sizeof(int));
    }
    NoexceptMove(NoexceptMove&& o) noexcept : data(o.data), n(o.n) {
        o.data = nullptr; o.n = 0;
    }
    NoexceptMove& operator=(const NoexceptMove& o) {
        if (this != &o) { delete[] data; data = new int[o.n]; n = o.n; std::memcpy(data, o.data, n * sizeof(int)); }
        return *this;
    }
    NoexceptMove& operator=(NoexceptMove&& o) noexcept {
        if (this != &o) { delete[] data; data = o.data; n = o.n; o.data = nullptr; o.n = 0; }
        return *this;
    }
};
static_assert(std::is_nothrow_move_constructible_v<NoexceptMove>);

struct ThrowingMove {
    int* data;
    std::size_t n;
    explicit ThrowingMove(std::size_t sz = 4) : data(new int[sz]), n(sz) {}
    ~ThrowingMove() { delete[] data; }
    ThrowingMove(const ThrowingMove& o) : data(new int[o.n]), n(o.n) {
        std::memcpy(data, o.data, n * sizeof(int));
    }
    ThrowingMove(ThrowingMove&& o) : data(o.data), n(o.n) {   // NOT noexcept
        o.data = nullptr; o.n = 0;
    }
    ThrowingMove& operator=(const ThrowingMove& o) {
        if (this != &o) { delete[] data; data = new int[o.n]; n = o.n; std::memcpy(data, o.data, n * sizeof(int)); }
        return *this;
    }
    ThrowingMove& operator=(ThrowingMove&& o) {
        if (this != &o) { delete[] data; data = o.data; n = o.n; o.data = nullptr; o.n = 0; }
        return *this;
    }
};
static_assert(!std::is_nothrow_move_constructible_v<ThrowingMove>);

// ── 主函数 ────────────────────────────────────────────────
int main() {
    constexpr int N = 1'000'000;       // 场景 1-3 的元素数
    constexpr int VN = 200'000;        // 场景 4 的 push_back 次数

    std::mt19937 rng(std::random_device{}());
    const std::uint64_t seed = static_cast<std::uint64_t>(rng());

    std::printf("== ch65 type_traits benchmark ==\n");
    std::printf("N=%d (copy elems), VN=%d (vector push_back)\n", N, VN);
    std::printf("sizeof TrivialPod=%zu NonTrivial=%zu CompactPod=%zu PaddedPod=%zu\n",
                sizeof(TrivialPod), sizeof(NonTrivial), sizeof(CompactPod), sizeof(PaddedPod));
    std::printf("is_trivially_copyable: TrivialPod=%d NonTrivial=%d\n",
                (int)std::is_trivially_copyable_v<TrivialPod>,
                (int)std::is_trivially_copyable_v<NonTrivial>);
    std::printf("is_nothrow_move_constructible: NoexceptMove=%d ThrowingMove=%d\n",
                (int)std::is_nothrow_move_constructible_v<NoexceptMove>,
                (int)std::is_nothrow_move_constructible_v<ThrowingMove>);
    std::printf("\n");

    // ═════════ 场景 1: is_trivially_copyable 分发 ═════════

    // 准备源数组
    std::vector<TrivialPod> src_tc(N);
    std::vector<NonTrivial> src_nt(N);
    for (int i = 0; i < N; ++i) {
        src_tc[i] = {i, i + 1, (long long)i * 2, (long long)i * 3};
        NonTrivial tmp;
        tmp.a = i; tmp.b = i + 1; tmp.c = (long long)i * 2; tmp.d = (long long)i * 3;
        src_nt[i] = tmp;
    }

    std::vector<TrivialPod> dst_tc(N);
    std::vector<NonTrivial> dst_nt(N);

    std::printf("--- Scenario 1: is_trivially_copyable dispatch ---\n");

    double t1_memcpy = bench("1a trivial POD + trait_copy (->memcpy)", [&] {
        trait_copy(dst_tc.data(), src_tc.data(), N);
        std::uint64_t s = seed;
        for (int i = 0; i < N; ++i) {
            s = s * 1315423911ull + static_cast<std::uint64_t>(dst_tc[i].a);
        }
        g_sink = s;
        g_escape = dst_tc.data();
    });

    double t1_elem = bench("1b non-trivial + trait_copy (->element loop)", [&] {
        trait_copy(dst_nt.data(), src_nt.data(), N);
        std::uint64_t s = seed;
        for (int i = 0; i < N; ++i) {
            s = s * 1315423911ull + static_cast<std::uint64_t>(dst_nt[i].a);
        }
        g_sink = s;
        g_escape = dst_nt.data();
    });

    double t1_hard = bench("1c trivial POD + hardcoded memcpy (control)", [&] {
        std::memcpy(dst_tc.data(), src_tc.data(), N * sizeof(TrivialPod));
        std::uint64_t s = seed;
        for (int i = 0; i < N; ++i) {
            s = s * 1315423911ull + static_cast<std::uint64_t>(dst_tc[i].a);
        }
        g_sink = s;
        g_escape = dst_tc.data();
    });

    // 对比：非平凡类型用 memcpy 强转拷贝（语义正确因为内部只是 int/long long）
    double t1_nt_memcpy = bench("1d non-trivial + raw memcpy (same layout)", [&] {
        std::memcpy(dst_nt.data(), src_nt.data(), N * sizeof(NonTrivial));
        std::uint64_t s = seed;
        for (int i = 0; i < N; ++i) {
            s = s * 1315423911ull + static_cast<std::uint64_t>(dst_nt[i].a);
        }
        g_sink = s;
        g_escape = dst_nt.data();
    });

    std::printf("\n--- Scenario 2: if constexpr vs runtime if ---\n");

    // ═════════ 场景 2: if constexpr vs runtime if ═════════

    double t2_constexpr = bench("2a if constexpr dispatch (compile-time)", [&] {
        trait_copy(dst_tc.data(), src_tc.data(), N);
        std::uint64_t s = seed;
        for (int i = 0; i < N; ++i) {
            s = s * 1315423911ull + static_cast<std::uint64_t>(dst_tc[i].a);
        }
        g_sink = s;
        g_escape = dst_tc.data();
    });

    double t2_runtime = bench("2b runtime if dispatch (volatile bool)", [&] {
        volatile bool vb = true;
        runtime_if_copy(dst_tc.data(), src_tc.data(), N, vb);
        std::uint64_t s = seed;
        for (int i = 0; i < N; ++i) {
            s = s * 1315423911ull + static_cast<std::uint64_t>(dst_tc[i].a);
        }
        g_sink = s;
        g_escape = dst_tc.data();
    });

    // 用 random flags：不可预测分支
    std::vector<unsigned char> flags(N);
    for (int i = 0; i < N; ++i) flags[i] = static_cast<unsigned char>(rng() & 1);

    double t2_unpred = bench("2c runtime if unpredictable (random 50/50)", [&] {
        std::uint64_t s = seed;
        for (int i = 0; i < N; ++i) {
            if (flags[i]) {
                dst_tc[i] = src_tc[i];
            } else {
                std::memcpy(&dst_tc[i], &src_tc[i], sizeof(TrivialPod));
            }
            s = s * 1315423911ull + static_cast<std::uint64_t>(dst_tc[i].a);
        }
        g_sink = s;
        g_escape = dst_tc.data();
    });

    std::printf("\n--- Scenario 3: conditional_t type selection ---\n");

    // ═════════ 场景 3: conditional_t 选择不同类型 ═════════

    // conditional_t<true, CompactPod, PaddedPod> → CompactPod (8B)
    // conditional_t<false, CompactPod, PaddedPod> → PaddedPod (64B)
    using SelectedCompact = std::conditional_t<std::is_trivially_copyable_v<CompactPod>,
                                               CompactPod, PaddedPod>;
    using SelectedPadded = std::conditional_t<!std::is_trivially_copyable_v<CompactPod>,
                                              CompactPod, PaddedPod>;
    static_assert(std::is_same_v<SelectedCompact, CompactPod>);
    static_assert(std::is_same_v<SelectedPadded, PaddedPod>);
    static_assert(sizeof(SelectedCompact) == 8);
    static_assert(sizeof(SelectedPadded) == 64);

    std::printf("conditional_t selected: compact=%zuB padded=%zuB (ratio %zu:1)\n",
                sizeof(SelectedCompact), sizeof(SelectedPadded),
                sizeof(SelectedPadded) / sizeof(SelectedCompact));

    constexpr int NC = N;  // 同样元素数
    std::vector<SelectedCompact> src_c(NC);
    std::vector<SelectedPadded> src_p(NC);
    for (int i = 0; i < NC; ++i) {
        src_c[i] = {i, i + 1};
        src_p[i] = {i, i + 1};
    }
    std::vector<SelectedCompact> dst_c(NC);
    std::vector<SelectedPadded> dst_p(NC);

    double t3_compact = bench("3a copy 1M compact (8B, conditional_t->CompactPod)", [&] {
        std::memcpy(dst_c.data(), src_c.data(), NC * sizeof(SelectedCompact));
        std::uint64_t s = seed;
        for (int i = 0; i < NC; ++i) {
            s = s * 1315423911ull + static_cast<std::uint64_t>(dst_c[i].a);
        }
        g_sink = s;
        g_escape = dst_c.data();
    });

    double t3_padded = bench("3b copy 1M padded (64B, conditional_t->PaddedPod)", [&] {
        std::memcpy(dst_p.data(), src_p.data(), NC * sizeof(SelectedPadded));
        std::uint64_t s = seed;
        for (int i = 0; i < NC; ++i) {
            s = s * 1315423911ull + static_cast<std::uint64_t>(dst_p[i].a);
        }
        g_sink = s;
        g_escape = dst_p.data();
    });

    // 证明 conditional_t 本身零开销：与直接用 CompactPod 比较
    double t3_direct = bench("3c copy 1M CompactPod directly (zero overhead check)", [&] {
        std::memcpy(dst_c.data(), src_c.data(), NC * sizeof(CompactPod));
        std::uint64_t s = seed;
        for (int i = 0; i < NC; ++i) {
            s = s * 1315423911ull + static_cast<std::uint64_t>(dst_c[i].a);
        }
        g_sink = s;
        g_escape = dst_c.data();
    });

    std::printf("\n--- Scenario 4: is_nothrow_move_constructible & vector growth ---\n");

    // ═════════ 场景 4: vector 扩容时 move vs copy ═════════
    // push_back VN 个元素，vector 多次扩容
    // NoexceptMove: is_nothrow_move_constructible → vector 用 move 扩容
    // ThrowingMove: !is_nothrow_move_constructible → vector 用 copy 扩容

    double t4_noexcept = bench("4a vector<NoexceptMove> push_back (move on grow)", [&] {
        std::vector<NoexceptMove> v;
        v.reserve(16);
        for (int i = 0; i < VN; ++i) {
            v.emplace_back(static_cast<std::size_t>(4));
        }
        std::uint64_t s = seed;
        for (int i = 0; i < VN; ++i) {
            s = s * 1315423911ull + static_cast<std::uint64_t>(v[i].n);
        }
        g_sink = s;
        g_escape = v.data();
    });

    double t4_throwing = bench("4b vector<ThrowingMove> push_back (copy on grow)", [&] {
        std::vector<ThrowingMove> v;
        v.reserve(16);
        for (int i = 0; i < VN; ++i) {
            v.emplace_back(static_cast<std::size_t>(4));
        }
        std::uint64_t s = seed;
        for (int i = 0; i < VN; ++i) {
            s = s * 1315423911ull + static_cast<std::uint64_t>(v[i].n);
        }
        g_sink = s;
        g_escape = v.data();
    });

    std::printf("\n--- Scenario 5: trait overhead = zero (compile cost vs runtime benefit) ---\n");

    // ═════════ 场景 5: 类型特性编译开销 vs 运行时收益 ═════════
    // trait 分发 vs 硬编码 memcpy：应当性能等价（零运行时开销）

    double t5_trait = bench("5a trait-dispatched copy (is_trivially_copyable)", [&] {
        trait_copy(dst_tc.data(), src_tc.data(), N);
        std::uint64_t s = seed;
        for (int i = 0; i < N; ++i) {
            s = s * 1315423911ull + static_cast<std::uint64_t>(dst_tc[i].a);
        }
        g_sink = s;
        g_escape = dst_tc.data();
    });

    double t5_hardcoded = bench("5b hardcoded memcpy (no trait involved)", [&] {
        std::memcpy(dst_tc.data(), src_tc.data(), N * sizeof(TrivialPod));
        std::uint64_t s = seed;
        for (int i = 0; i < N; ++i) {
            s = s * 1315423911ull + static_cast<std::uint64_t>(dst_tc[i].a);
        }
        g_sink = s;
        g_escape = dst_tc.data();
    });

    // trait 组合验证：conjunction 短路 + is_trivially_copyable
    double t5_combo = bench("5c trait chain (conjunction+is_trivially_copyable) copy", [&] {
        if constexpr (std::conjunction_v<std::is_trivially_copyable<TrivialPod>,
                                         std::is_standard_layout<TrivialPod>>) {
            std::memcpy(dst_tc.data(), src_tc.data(), N * sizeof(TrivialPod));
        } else {
            for (int i = 0; i < N; ++i) dst_tc[i] = src_tc[i];
        }
        std::uint64_t s = seed;
        for (int i = 0; i < N; ++i) {
            s = s * 1315423911ull + static_cast<std::uint64_t>(dst_tc[i].a);
        }
        g_sink = s;
        g_escape = dst_tc.data();
    });

    // ── 汇总 ──────────────────────────────────────────────
    std::printf("\n=== Summary (ratios) ===\n");
    std::printf("S1: trait memcpy vs trait element-loop   %6.2fx\n", t1_elem / t1_memcpy);
    std::printf("S1: trait memcpy vs hardcoded memcpy     %6.2fx\n", t1_hard / t1_memcpy);
    std::printf("S1: non-trivial raw memcpy vs elem loop  %6.2fx\n", t1_nt_memcpy / t1_elem);
    std::printf("S2: if constexpr vs runtime if (true)    %6.2fx\n", t2_runtime / t2_constexpr);
    std::printf("S2: if constexpr vs unpredictable if     %6.2fx\n", t2_unpred / t2_constexpr);
    std::printf("S3: padded(64B) vs compact(8B) copy      %6.2fx\n", t3_padded / t3_compact);
    std::printf("S3: conditional_t vs direct (zero ovhd)  %6.2fx\n", t3_direct / t3_compact);
    std::printf("S4: throwing(copy) vs noexcept(move)     %6.2fx\n", t4_throwing / t4_noexcept);
    std::printf("S5: trait copy vs hardcoded memcpy       %6.2fx\n", t5_hardcoded / t5_trait);
    std::printf("S5: trait chain vs hardcoded memcpy      %6.2fx\n", t5_hardcoded / t5_combo);
    return 0;
}
