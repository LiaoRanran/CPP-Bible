// _bench_vector.cpp — ch77 附录 L 的 D5 真实基准源码
// 目的：实测 std::vector<T> 扩容期间元素的"移动 vs 拷贝"次数与墙钟耗时。
//   实验 A：noexcept-move 探针类型，统计 no_reserve 的总移动次数（应 ≈2N）与重分配次数。
//   实验 B：throwing-move 探针类型（移动构造 non-noexcept），证明 move_if_noexcept
//            回退到 COPY（强异常安全），拷贝次数 ≈2N、移动次数 0。
//   实验 C：reserve(N) 消除全部扩容 → 移动/拷贝次数均为 0（仅 N 次直接构造）。
//   实验 D：重载荷类型（256B）no_reserve vs reserve 的墙钟耗时对比。
// 编译：g++ -std=c++20 -O2 _bench_vector.cpp -o _bench_vector.exe   (GCC 15.3.0 / Win64)
// 注意：探针类型带自定义 move/copy 构造 → 非平凡可重定位 → libstdc++ 走
//       __uninitialized_move_if_noexcept_a 路径（vector.tcc:525/533），故构造被真实计数。
#include <vector>
#include <cstdio>
#include <cstdint>
#include <chrono>
#include <string>

// ---- 全局计数器 ----
struct Counters { long moves=0, copies=0, ctors=0, dtors=0; };
static Counters gN;   // noexcept-move 探针
static Counters gT;   // throwing-move 探针

// 实验 A/C：移动构造标记 noexcept
struct ProbeNoexcept {
    int v;
    explicit ProbeNoexcept(int x=0) noexcept : v(x) { ++gN.ctors; }
    ProbeNoexcept(const ProbeNoexcept& o) noexcept : v(o.v) { ++gN.copies; }
    ProbeNoexcept(ProbeNoexcept&& o) noexcept : v(o.v) { ++gN.moves; }
    ~ProbeNoexcept() { ++gN.dtors; }
    ProbeNoexcept& operator=(const ProbeNoexcept&) = default;
};

// 实验 B：移动构造 NON-noexcept → move_if_noexcept 回退为拷贝
struct ProbeThrowing {
    int v;
    explicit ProbeThrowing(int x=0) : v(x) { ++gT.ctors; }
    ProbeThrowing(const ProbeThrowing& o) : v(o.v) { ++gT.copies; }
    ProbeThrowing(ProbeThrowing&& o) /*非 noexcept!*/ : v(o.v) { ++gT.moves; }
    ~ProbeThrowing() { ++gT.dtors; }
    ProbeThrowing& operator=(const ProbeThrowing&) = default;
};

// 实验 D：256 字节重载荷（noexcept move）
struct Blob256 {
    char data[256];
    Blob256() noexcept { data[0]=1; }
    Blob256(const Blob256&) noexcept = default;
    Blob256(Blob256&&) noexcept = default;
    Blob256& operator=(const Blob256&) noexcept = default;
};

template<class Probe, class Ctr>
void run_count(const char* name, int N, Ctr& c, bool do_reserve) {
    c = Ctr{};
    std::vector<Probe> v;
    if (do_reserve) v.reserve(N);
    int reallocs = 0; std::size_t last_cap = v.capacity();
    for (int i = 0; i < N; ++i) {
        v.push_back(Probe(i));            // 临时对象移动入 vector
        if (v.capacity() != last_cap) { ++reallocs; last_cap = v.capacity(); }
    }
    // push_back(Probe(i)) 会额外产生 N 次"临时→槽位"的移动，需从扩容移动中区分。
    // 我们关注的是"扩容迁移"的构造：moves/copies 里超出 N 的部分即扩容迁移。
    std::printf("  %-22s reserve=%d  N=%d  reallocs=%d  final_cap=%zu\n",
                name, (int)do_reserve, N, reallocs, v.capacity());
    std::printf("      ctors=%ld  copies=%ld  moves=%ld  (扩容迁移≈ moves-N = %ld)\n",
                c.ctors, c.copies, c.moves, c.moves - N);
}

template<class T>
double time_fill(int N, bool do_reserve) {
    using clk = std::chrono::steady_clock;
    auto t0 = clk::now();
    std::vector<T> v;
    if (do_reserve) v.reserve(N);
    for (int i = 0; i < N; ++i) v.push_back(T{});
    auto t1 = clk::now();
    // 阻止优化消除
    volatile char sink = v.empty() ? 0 : v.back().data[0];
    (void)sink;
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}

int main() {
    std::puts("=== 实验 A：noexcept-move 探针（no_reserve）— 扩容用 MOVE ===");
    run_count<ProbeNoexcept>("ProbeNoexcept", 1000000, gN, false);

    std::puts("=== 实验 B：throwing-move 探针（no_reserve）— 扩容回退 COPY ===");
    run_count<ProbeThrowing>("ProbeThrowing", 1000000, gT, false);

    std::puts("=== 实验 C：reserve(N) 消除扩容迁移 ===");
    run_count<ProbeNoexcept>("ProbeNoexcept+reserve", 1000000, gN, true);

    std::puts("=== 实验 D：256B 重载荷 墙钟耗时（多轮取中位思路，跑 5 轮）===");
    const int N = 2000000;
    for (int r = 0; r < 5; ++r) {
        double no_r = time_fill<Blob256>(N, false);
        double yes_r = time_fill<Blob256>(N, true);
        std::printf("  round %d: no_reserve=%8.2f ms   reserve=%8.2f ms   speedup=%.2fx\n",
                    r, no_r, yes_r, no_r / yes_r);
    }
    return 0;
}
