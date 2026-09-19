// _bench_d5_ch61_overload_dispatch.cpp
// D5 角度: 编译期重载决议→直接内联调用 vs 运行期函数指针表间接分派
// 实测: AMD Ryzen 9 7940HX, g++ 15.3.0 -O2 -std=c++23
#include <chrono>
#include <cstdio>
#include <vector>

static volatile long long g_sink = 0;

// ---- 运算内核 (3 种操作) ----
static inline int op_add(int x)    { return x + 7; }
static inline int op_mul(int x)    { return x * 3; }
static inline int op_xor(int x)    { return x ^ 0x55; }

// ---- A. 编译期分派: if constexpr 路由到具类型 → 全部内联 ----
template <int Tag>
long long run_constexpr(std::vector<int> const& v) {
    long long acc = 0;
    for (int x : v) {
        if constexpr (Tag == 0)      acc += op_add(x);
        else if constexpr (Tag == 1) acc += op_mul(x);
        else                         acc += op_xor(x);
    }
    return acc;
}

// ---- B. 运行期分派: 函数指针表间接调用 ----
using FnPtr = int (*)(int);
static FnPtr table[3] = { &op_add, &op_mul, &op_xor };

long long run_ptrtable(std::vector<int> const& v, std::vector<int> const& tags) {
    long long acc = 0;
    for (size_t i = 0; i < v.size(); ++i) {
        acc += table[tags[i]](v[i]);
    }
    return acc;
}

int main() {
    const long long N = 20000000LL;
    std::vector<int> v(N);
    std::vector<int> tags(N);
    for (long long i = 0; i < N; ++i) {
        v[i]   = static_cast<int>(i & 0xFF);
        tags[i] = static_cast<int>(i % 3);       // 运行期动态 tag
    }

    for (int trial = 0; trial < 5; ++trial) {
        auto t0 = std::chrono::steady_clock::now();
        long long r1 = run_constexpr<0>(v) + run_constexpr<1>(v) + run_constexpr<2>(v);
        auto t1 = std::chrono::steady_clock::now();
        long long r2 = run_ptrtable(v, tags);
        auto t2 = std::chrono::steady_clock::now();
        g_sink = r1 + r2;
        double dt_c = std::chrono::duration<double, std::milli>(t1 - t0).count();
        double dt_p = std::chrono::duration<double, std::milli>(t2 - t1).count();
        std::printf("trial %d: constexpr_dispatch=%.3f ms  ptr_table=%.3f ms  ratio=%.2fx\n",
                    trial, dt_c, dt_p, dt_p / dt_c);
    }
    std::printf("SUMMARY constexpr_vs_ptrtable\n");
    return 0;
}
