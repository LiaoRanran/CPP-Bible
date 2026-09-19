// _bench_d5_ch38_allocator.cpp — ch38 分配器：默认 allocator vs PMR 资源
// g++ -O2 -std=c++23 _bench_d5_ch38_allocator.cpp -o bench38
//
// 方法学：每个子基准跑 5 轮取中位；volatile sink 防 DCE；
// 元素值取自运行期随机种子，防常量折叠。
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <list>
#include <memory_resource>
#include <random>
#include <vector>

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
    std::printf("%-46s median %9.3f ms   raw:", name, t[2]);
    for (double v : raw) std::printf(" %.3f", v);
    std::printf("\n");
    return t[2];
}

volatile std::uint64_t g_sink;

struct Small {   // 24B 小对象，pool_resource 的典型客户
    long long a, b, c;
};

int main() {
    constexpr int VEC_N = 200'000;   // 每个 vector 的元素数
    constexpr int VEC_R = 200;       // 重复构建次数
    constexpr int LST_N = 200'000;   // 每个 list 的节点数
    constexpr int LST_R = 20;        // 重复构建次数
    constexpr int OBJ_N = 1'000'000; // 小对象个数
    constexpr int OBJ_R = 8;         // 重复轮数

    std::mt19937 rng(std::random_device{}());
    const int seed = static_cast<int>(rng() & 0xFFFF);

    std::printf("== ch38 allocator / pmr benchmark ==\n");

    // ---------- A. vector<int>：默认 allocator vs monotonic_buffer ----------
    double a1 = bench("A1 std::vector<int> default alloc", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < VEC_R; ++r) {
            std::vector<int> v;
            for (int i = 0; i < VEC_N; ++i) v.push_back(seed + i);
            s += static_cast<std::uint64_t>(v[VEC_N / 2]);
        }
        g_sink = s;
    });

    std::vector<unsigned char> arena(VEC_N * sizeof(int) * 4);
    double a2 = bench("A2 pmr::vector<int> monotonic_buffer", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < VEC_R; ++r) {
            std::pmr::monotonic_buffer_resource mbr(arena.data(), arena.size(),
                                                    std::pmr::null_memory_resource());
            std::pmr::vector<int> v(&mbr);
            for (int i = 0; i < VEC_N; ++i) v.push_back(seed + i);
            s += static_cast<std::uint64_t>(v[VEC_N / 2]);
        }
        g_sink = s;
    });

    // ---------- B. list<int>：默认 allocator vs pmr 资源（节点容器甜点区） ----------
    double b1 = bench("B1 std::list<int> default alloc", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < LST_R; ++r) {
            std::list<int> l;
            for (int i = 0; i < LST_N; ++i) l.push_back(seed + i);
            s += static_cast<std::uint64_t>(l.back());
        }
        g_sink = s;
    });

    std::vector<unsigned char> larena(static_cast<std::size_t>(LST_N) * 64);
    double b2 = bench("B2 pmr::list<int> monotonic_buffer", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < LST_R; ++r) {
            std::pmr::monotonic_buffer_resource mbr(larena.data(), larena.size());
            std::pmr::list<int> l(&mbr);
            for (int i = 0; i < LST_N; ++i) l.push_back(seed + i);
            s += static_cast<std::uint64_t>(l.back());
        }
        g_sink = s;
    });

    double b3 = bench("B3 pmr::list<int> unsync_pool_resource", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < LST_R; ++r) {
            std::pmr::unsynchronized_pool_resource pool;
            std::pmr::list<int> l(&pool);
            for (int i = 0; i < LST_N; ++i) l.push_back(seed + i);
            s += static_cast<std::uint64_t>(l.back());
        }
        g_sink = s;
    });

    // ---------- C. 大量小对象：new/delete vs pool_resource ----------
    double c1 = bench("C1 many small objs: new/delete", [&] {
        std::uint64_t s = 0;
        std::vector<Small*> ps(OBJ_N);
        for (int r = 0; r < OBJ_R; ++r) {
            for (int i = 0; i < OBJ_N; ++i) {
                Small* p = new Small{seed + i, i, r};
                ps[i] = p;
            }
            for (int i = 0; i < OBJ_N; ++i) {
                s += static_cast<std::uint64_t>(ps[i]->a);
                delete ps[i];
            }
        }
        g_sink = s;
    });

    double c2 = bench("C2 many small objs: unsync_pool_resource", [&] {
        std::uint64_t s = 0;
        std::vector<Small*> ps(OBJ_N);
        for (int r = 0; r < OBJ_R; ++r) {
            std::pmr::unsynchronized_pool_resource pool;
            for (int i = 0; i < OBJ_N; ++i) {
                void* raw = pool.allocate(sizeof(Small), alignof(Small));
                ps[i] = ::new (raw) Small{seed + i, i, r};
            }
            for (int i = 0; i < OBJ_N; ++i) {
                s += static_cast<std::uint64_t>(ps[i]->a);
                ps[i]->~Small();
                pool.deallocate(ps[i], sizeof(Small), alignof(Small));
            }
        }
        g_sink = s;
    });

    double c3 = bench("C3 many small objs: monotonic_buffer", [&] {
        std::uint64_t s = 0;
        std::vector<Small*> ps(OBJ_N);
        for (int r = 0; r < OBJ_R; ++r) {
            std::pmr::monotonic_buffer_resource mbr;
            for (int i = 0; i < OBJ_N; ++i) {
                void* raw = mbr.allocate(sizeof(Small), alignof(Small));
                ps[i] = ::new (raw) Small{seed + i, i, r};
            }
            for (int i = 0; i < OBJ_N; ++i) {
                s += static_cast<std::uint64_t>(ps[i]->a);
                ps[i]->~Small();
            }
            // mbr 析构一次性归还全部内存，无逐块 deallocate
        }
        g_sink = s;
    });

    std::printf("\n-- ratios --\n");
    std::printf("A vector : default %.3f / pmr-mono %.3f  => %.2fx\n", a1, a2, a1 / a2);
    std::printf("B list   : default %.3f / pmr-mono %.3f  => %.2fx\n", b1, b2, b1 / b2);
    std::printf("B list   : default %.3f / pmr-pool %.3f  => %.2fx\n", b1, b3, b1 / b3);
    std::printf("C objs   : new     %.3f / pmr-pool %.3f  => %.2fx\n", c1, c2, c1 / c2);
    std::printf("C objs   : new     %.3f / pmr-mono %.3f  => %.2fx\n", c1, c3, c1 / c3);
    return 0;
}
