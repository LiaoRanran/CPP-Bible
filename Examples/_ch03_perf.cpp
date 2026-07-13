// Examples/_ch03_perf.cpp
// 真实基准：ch03_cpp98_03.md 附录性能对比的实测替换
// 编译: g++ -O2 -std=c++23 -m64 _ch03_perf.cpp -o _ch03_perf
//
// 目的：为 ch03 的"实证替换"提供本机真值，替换 ~N 估算：
//   - move vs copy（vector<int> 1M）：copy ~500us / move ~3ns
//   - 虚函数调用延迟 ~5ns
//   - typeid ~1ns / dynamic_cast ~50-200ns
//   - std::sort(1M int) ~450ms
// 平台：MinGW GCC 13.1.0 -O2，TSC 2.395 GHz（本机校准，见 _ch120_coroutine_perf）。
//
// 不可在本机干净测项（保留量级 + 来源标注，不编单点假数）：
//   - cout vs printf (~3-5x)：依赖 iostream 与 C stdio 的 locale/mutex/sync 耦合，
//     受 std::ios::sync_with_stdio 状态影响大，无单一真值；
//   - std::print vs cout (10x / ~50us)：<print> 为 C++23，本 Qt MinGW 13.1 含该头但
//     std::print 实现依赖 system_category 等，benchmark 噪音大，标 [C++23; 来源 cppreference]；
//   - bind1st vs lambda：bind1st 已在 C++17 移除、C++20 删除，无法在本机 -std=c++23 编译。
#include <iostream>
#include <vector>
#include <algorithm>
#include <random>
#include <chrono>
#include <typeinfo>
#include <cstdint>
#include <x86intrin.h>

static inline uint64_t rdtsc() { return __rdtsc(); }
static const double TSC_GHZ = 2.395;

// ---- move vs copy ----
[[gnu::noinline]] std::vector<int> copy_vec(const std::vector<int>& a) { return a; }
[[gnu::noinline]] std::vector<int> move_vec(std::vector<int>&& a) { return std::move(a); }

// ---- 虚函数调用 ----
struct Base { virtual int f(int x) { return x + 1; } virtual ~Base() = default; };
struct Der : Base { int f(int x) override { return x * 2; } };
[[gnu::noinline]] int virt_call(Base& b, int x) { return b.f(x); }

// ---- typeid / dynamic_cast ----
[[gnu::noinline]] const char* get_tname(const Base& b) { return typeid(b).name(); }
[[gnu::noinline]] Der* dyn_down(Base& b) { return dynamic_cast<Der*>(&b); }

int main() {
    const int N = 1'000'000;
    std::mt19937 rng(20240703);
    std::uniform_int_distribution<int> dist(0, 1'000'000'000);
    std::vector<int> data(N);
    for (auto& v : data) v = dist(rng);

    volatile int sink = 0;
    uint64_t t0, t1;

    // 1) copy vs move（vector<int> 1M）
    t0 = rdtsc(); auto c = copy_vec(data); t1 = rdtsc();
    double copy_ns = (double)(t1 - t0) / TSC_GHZ;            // 含返回值构造+分配(编译器可能 NRVO，故测 copy_vec 内部)
    std::vector<int> mv_src = data;                          // 复制一份供 move（避免破坏 data）
    t0 = rdtsc(); auto m = move_vec(std::move(mv_src)); t1 = rdtsc();
    double move_ns = (double)(t1 - t0) / TSC_GHZ;            // 指针交换，亚纳秒级但含调用开销
    sink += c[0] + m[0];

    // 2) 虚函数调用（1M 次，经 Base&）
    Der d;
    Base& br = d;
    t0 = rdtsc(); for (int i = 0; i < N; ++i) sink += virt_call(br, i); t1 = rdtsc();
    double virt_ns = (double)(t1 - t0) / N / TSC_GHZ;

    // 3) typeid（1M 次）
    t0 = rdtsc(); for (int i = 0; i < N; ++i) sink += (int)(get_tname(br)[0]); t1 = rdtsc();
    double typeid_ns = (double)(t1 - t0) / N / TSC_GHZ;

    // 4) dynamic_cast 成功下转（1M 次，Der*）
    t0 = rdtsc(); for (int i = 0; i < N; ++i) { Der* p = dyn_down(br); sink += (p != nullptr); } t1 = rdtsc();
    double dyncast_ns = (double)(t1 - t0) / N / TSC_GHZ;

    // 5) std::sort(1M int)（steady_clock）
    std::vector<int> sdata = data;
    auto sa = std::chrono::steady_clock::now();
    std::sort(sdata.begin(), sdata.end());
    auto sb = std::chrono::steady_clock::now();
    double sort_ms = std::chrono::duration<double, std::milli>(sb - sa).count();
    sink += sdata[0];

    std::cout << "\n=== 实测（GCC 13.1 -O2, TSC " << TSC_GHZ << "GHz, N=" << N << ") ===" << std::endl;
    std::cout << "copy_vec_1M_ns  : " << copy_ns  << "  (深拷贝 1M int)" << std::endl;
    std::cout << "move_vec_1M_ns  : " << move_ns  << "  (指针交换, 含调用开销)" << std::endl;
    std::cout << "virtual_call_ns : " << virt_ns  << std::endl;
    std::cout << "typeid_ns       : " << typeid_ns << std::endl;
    std::cout << "dynamic_cast_ns : " << dyncast_ns << std::endl;
    std::cout << "sort_1M_ms      : " << sort_ms  << std::endl;
    std::cout << "[sink] " << sink << std::endl;
    return 0;
}
