// _bench_d5_ch37_new_delete.cpp — ch37 new/delete：分配路径的真实成本
// g++ -O2 -std=c++23 _bench_d5_ch37_new_delete.cpp -o bench37
//
// 方法学：每个子基准跑 5 轮取中位；volatile sink 防 DCE；
// 循环体用"写入后立即回读并混入下一次写入值"的依赖链，
// 使 sum 无闭式解，编译器无法把整个循环折叠成常数。
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <new>
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
    std::printf("%-44s median %9.3f ms   raw:", name, t[2]);
    for (double v : raw) std::printf(" %.3f", v);
    std::printf("\n");
    return t[2];
}

volatile std::uint64_t g_sink;
volatile void* g_escape;   // 指针逃逸，禁止 allocation elision

struct Node {              // 32B，与 ch41 附录同规格便于横向对照
    long long v[4];
};

struct alignas(64) Node64 {   // 触发 over-aligned operator new
    long long v[4];
};

// 依赖链：先写后读，读出值参与下一次写入 —— 无闭式解，不可折叠
#define TOUCH(p, i)                                                        \
    do {                                                                   \
        (p)->v[0] = seed + (i) + static_cast<long long>(s & 15);           \
        s = s * 1315423911ull + static_cast<std::uint64_t>((p)->v[0]);     \
    } while (0)

int main() {
    constexpr int N = 2'000'000;      // 单对象分配次数
    constexpr int ASZ = 64;           // 数组元素数
    constexpr int AN = N / ASZ;       // 数组次数，使总对象数与 N 相等

    // 运行期随机种子，防止编译器折叠写入值
    std::mt19937 rng(std::random_device{}());
    const long long seed = static_cast<long long>(rng() & 0xFFFF);

    std::printf("== ch37 new/delete benchmark, N=%d ==\n", N);

    // 1) 逐对象 new / delete
    double t_single = bench("single new/delete Node x2M", [&] {
        std::uint64_t s = 1;
        for (int i = 0; i < N; ++i) {
            Node* p = new Node;
            g_escape = p;
            TOUCH(p, i);
            delete p;
        }
        g_sink = s;
    });

    // 2) 批量 new[] / delete[]：同样构造并触碰 2M 个 Node，但只有 N/ASZ 次分配
    double t_array = bench("bulk new[64]/delete[] (same 2M objs)", [&] {
        std::uint64_t s = 1;
        for (int i = 0; i < AN; ++i) {
            Node* a = new Node[ASZ];
            g_escape = a;
            for (int j = 0; j < ASZ; ++j) {
                Node* p = a + j;
                TOUCH(p, i + j);
            }
            delete[] a;
        }
        g_sink = s;
    });

    // 3) nothrow new / delete
    double t_nothrow = bench("nothrow new/delete Node x2M", [&] {
        std::uint64_t s = 1;
        for (int i = 0; i < N; ++i) {
            Node* p = new (std::nothrow) Node;
            if (!p) break;
            g_escape = p;
            TOUCH(p, i);
            delete p;
        }
        g_sink = s;
    });

    // 4) placement new：一块预分配缓冲区反复复用，零堆分配
    alignas(Node) static unsigned char buf[sizeof(Node)];
    double t_place = bench("placement new on reused buffer x2M", [&] {
        std::uint64_t s = 1;
        for (int i = 0; i < N; ++i) {
            Node* p = ::new (static_cast<void*>(buf)) Node;
            g_escape = p;
            TOUCH(p, i);
            p->~Node();
        }
        g_sink = s;
    });

    // 5) 对齐 new：alignas(64) 走 operator new(size_t, align_val_t)
    double t_align = bench("aligned new/delete alignas(64) x2M", [&] {
        std::uint64_t s = 1;
        for (int i = 0; i < N; ++i) {
            Node64* p = new Node64;
            g_escape = p;
            p->v[0] = seed + i + static_cast<long long>(s & 15);
            s = s * 1315423911ull + static_cast<std::uint64_t>(p->v[0]);
            delete p;
        }
        g_sink = s;
    });

    // 6) 对照：栈上局部对象（无堆交互，纯寄存器/栈槽）
    double t_stack = bench("stack local Node x2M (control)", [&] {
        std::uint64_t s = 1;
        for (int i = 0; i < N; ++i) {
            Node local;
            Node* p = &local;
            g_escape = p;
            TOUCH(p, i);
        }
        g_sink = s;
    });

    std::printf("\n-- ratios (single new/delete = 1.00x) --\n");
    std::printf("single new/delete      %6.2fx\n", t_single / t_single);
    std::printf("bulk new[64]           %6.2fx\n", t_array / t_single);
    std::printf("nothrow new            %6.2fx\n", t_nothrow / t_single);
    std::printf("placement new          %6.2fx\n", t_place / t_single);
    std::printf("aligned new(64)        %6.2fx\n", t_align / t_single);
    std::printf("stack local            %6.2fx\n", t_stack / t_single);
    return 0;
}
