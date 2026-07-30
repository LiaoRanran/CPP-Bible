// _bench_d5_36_stackheap.cpp — ch36 栈 vs 堆：分配成本的真实差距
// g++ -O2 -std=c++23
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <vector>
#include <algorithm>

static double now_ms() {
    using namespace std::chrono;
    return duration<double, std::milli>(steady_clock::now().time_since_epoch()).count();
}
template <class F>
static double bench(const char* name, F&& f) {
    std::vector<double> t;
    for (int r = 0; r < 5; ++r) { double t0 = now_ms(); f(); t.push_back(now_ms() - t0); }
    std::sort(t.begin(), t.end());
    std::printf("%-36s %10.3f ms\n", name, t[2]);
    return t[2];
}
volatile std::uint64_t g_sink;
volatile int* g_escape; // 指针逃逸，防堆分配被优化

int main() {
    constexpr int M = 10'000'000;   // 单对象分配次数
    constexpr int K = 200'000;      // 数组分配次数
    constexpr int ASZ = 1024;

    // 1) 每次迭代 new/delete 单个 int（堆分配器成本）
    bench("heap: new/delete int x10M", [&] {
        std::uint64_t s = 0;
        for (int i = 0; i < M; ++i) {
            int* p = new int(i);
            g_escape = p;           // 逃逸，禁止折叠
            s += *p;
            delete p;
        }
        g_sink = s;
    });

    // 2) 栈上单个 int（预期被 -O2 折叠为寄存器运算——诚实标注）
    bench("stack: local int x10M", [&] {
        std::uint64_t s = 0;
        for (int i = 0; i < M; ++i) {
            int x = i;
            s += x;
        }
        g_sink = s;
    });

    // 3) 每次迭代 new[]/delete[] 1024-int 数组并写入
    bench("heap: new[1024]+write x200K", [&] {
        std::uint64_t s = 0;
        for (int i = 0; i < K; ++i) {
            int* a = new int[ASZ];
            for (int j = 0; j < ASZ; ++j) a[j] = i + j;
            g_escape = a;
            s += a[ASZ / 2];
            delete[] a;
        }
        g_sink = s;
    });

    // 4) 栈上 1024-int 数组并写入（同样写满）
    bench("stack: int[1024]+write x200K", [&] {
        std::uint64_t s = 0;
        for (int i = 0; i < K; ++i) {
            int a[ASZ];
            for (int j = 0; j < ASZ; ++j) a[j] = i + j;
            g_escape = a;
            s += a[ASZ / 2];
        }
        g_sink = s;
    });

    // 5) vector 每次新建 vs 复用（clear 不释放容量）
    bench("vector: fresh(1024) x200K", [&] {
        std::uint64_t s = 0;
        for (int i = 0; i < K; ++i) {
            std::vector<int> v(ASZ, i);
            s += v[ASZ / 2];
        }
        g_sink = s;
    });
    bench("vector: reused assign x200K", [&] {
        std::uint64_t s = 0;
        std::vector<int> v;
        for (int i = 0; i < K; ++i) {
            v.assign(ASZ, i);
            s += v[ASZ / 2];
        }
        g_sink = s;
    });

    std::printf("sink=%llu\n", (unsigned long long)g_sink);
    return 0;
}
