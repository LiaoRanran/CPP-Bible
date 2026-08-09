// _bench_d5_ch19_threadlocal.cpp
// 真实基准：三种存储期变量（函数内自动局部 / 全局 static / thread_local）的访问开销
// 编译运行：g++ -O2 -std=c++23 _bench_d5_ch19_threadlocal.cpp -o b19 && ./b19
// 注：本机 long 为 32 位，统一用 long long 计数避免溢出；三类计数器宽度一致才公平。
#include <iostream>
#include <chrono>
#include <vector>
#include <algorithm>

static volatile long long        g_counter = 0;             // 全局 static（RIP/GOT 相对寻址）
static thread_local volatile long long t_counter = 0;       // 线程局部（%gs 段相对寻址）
static volatile long long        sink     = 0;              // 防 DCE

void bench_local(long long iters) {
    volatile long long lc = 0;                              // 栈上（RSP 相对寻址）
    for (long long i = 0; i < iters; ++i) lc += (i & 1);
    sink = lc;
}
void bench_global(long long iters) {
    for (long long i = 0; i < iters; ++i) g_counter += (i & 1);
    sink = g_counter;
}
void bench_tls(long long iters) {
    for (long long i = 0; i < iters; ++i) t_counter += (i & 1);
    sink = t_counter;
}

int main() {
    const long long iters = 200'000'000LL;
    const int RUNS = 5;
    auto median = [&](void(*f)(long long)) {
        std::vector<double> ms(RUNS);
        for (int r = 0; r < RUNS; ++r) {
            auto t0 = std::chrono::steady_clock::now();
            f(iters);
            auto t1 = std::chrono::steady_clock::now();
            ms[r] = std::chrono::duration<double, std::milli>(t1 - t0).count();
        }
        std::sort(ms.begin(), ms.end());
        return ms[RUNS / 2];
    };
    double local_ms  = median(bench_local);
    double global_ms = median(bench_global);
    double tls_ms    = median(bench_tls);
    std::cout << "iters=" << iters << std::endl;
    std::cout << "local : " << local_ms  << " ms" << std::endl;
    std::cout << "global: " << global_ms << " ms" << std::endl;
    std::cout << "tls   : " << tls_ms    << " ms" << std::endl;
    std::cout << "tls/global=" << (tls_ms / global_ms)
              << "  tls/local=" << (tls_ms / local_ms) << std::endl;
    return 0;
}
