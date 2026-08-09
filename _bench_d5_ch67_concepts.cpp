// _bench_d5_ch67_concepts.cpp — ch67 Concepts / SFINAE / if-constexpr / virtual 的运行时分派开销
// GCC 15.3.0 (MinGW-W64 x86_64), g++ -O2 -std=c++23
// Concepts 是纯编译期约束：被 concepts 选中的重载在运行时与 SFINAE / if-constexpr 选中的重载
// 编译出完全相同的机器码（零额外指令）。运行时开销只来自 virtual（vtable 间接）。
#include <iostream>
#include <chrono>
#include <type_traits>
#include <algorithm>

static volatile long long g_sink = 0;

struct Small { double v() const { return 1.0; } };
struct Big  { double v() const { return 2.0; } };

// (A) concepts 约束重载
template <class T> requires std::is_same_v<T, Small>
double handle_cpp(T) { return 10.0; }
template <class T> requires std::is_same_v<T, Big>
double handle_cpp(T) { return 20.0; }

// (B) SFINAE 约束重载
template <class T, std::enable_if_t<std::is_same_v<T, Small>, int> = 0>
double handle_sf(T) { return 10.0; }
template <class T, std::enable_if_t<std::is_same_v<T, Big>, int> = 0>
double handle_sf(T) { return 20.0; }

// (C) if-constexpr
template <class T>
double handle_ifce(T) { if constexpr (std::is_same_v<T, Small>) return 10.0; else return 20.0; }

// (D) virtual
struct Base { virtual double v() const = 0; virtual ~Base() = default; };
struct S : Base { double v() const override { return 10.0; } };
struct B : Base { double v() const override { return 20.0; } };

int main() {
    const long long ITERS = 200'000'000LL;
    const int RUNS = 5;

    Small small; Big big;
    S g_s; B g_b;
    Base* g_arr[2] = { &g_s, &g_b };
    static volatile int g_sel = 0;

    double r_cpp[RUNS], r_sf[RUNS], r_ifce[RUNS], r_virt[RUNS];

    for (int r = 0; r < RUNS; ++r) {
        // (A) concepts —— T 编译期已知
        { auto t0=std::chrono::steady_clock::now(); double s=0.0;
          for (long long i=0;i<ITERS;++i) s += handle_cpp(small);
          auto t1=std::chrono::steady_clock::now(); g_sink+=(long long)s; r_cpp[r]=std::chrono::duration<double,std::milli>(t1-t0).count(); }
        // (B) SFINAE
        { auto t0=std::chrono::steady_clock::now(); double s=0.0;
          for (long long i=0;i<ITERS;++i) s += handle_sf(big);
          auto t1=std::chrono::steady_clock::now(); g_sink+=(long long)s; r_sf[r]=std::chrono::duration<double,std::milli>(t1-t0).count(); }
        // (C) if-constexpr
        { auto t0=std::chrono::steady_clock::now(); double s=0.0;
          for (long long i=0;i<ITERS;++i) s += handle_ifce(small);
          auto t1=std::chrono::steady_clock::now(); g_sink+=(long long)s; r_ifce[r]=std::chrono::duration<double,std::milli>(t1-t0).count(); }
        // (D) virtual —— 运行时 idx 强制 vtable 分派
        { auto t0=std::chrono::steady_clock::now(); double s=0.0;
          for (long long i=0;i<ITERS;++i){ g_sel=(g_sel+1)&1; int idx=g_sel; s += g_arr[idx]->v(); }
          auto t1=std::chrono::steady_clock::now(); g_sink+=(long long)s; r_virt[r]=std::chrono::duration<double,std::milli>(t1-t0).count(); }
    }

    std::sort(r_cpp,r_cpp+RUNS); std::sort(r_sf,r_sf+RUNS); std::sort(r_ifce,r_ifce+RUNS); std::sort(r_virt,r_virt+RUNS);
    double m_cpp=r_cpp[2], m_sf=r_sf[2], m_ifce=r_ifce[2], m_virt=r_virt[2];

    std::cout << "ch67 concepts vs sfinae vs virtual (ITERS=" << ITERS << ")\n";
    std::cout << "concepts   (compile-time) median = " << m_cpp  << " ms\n";
    std::cout << "SFINAE     (compile-time) median = " << m_sf   << " ms\n";
    std::cout << "if-constexpr(compile-time) median = " << m_ifce << " ms\n";
    std::cout << "virtual     (runtime)      median = " << m_virt << " ms\n";
    std::cout << "sf/concepts   = " << (m_sf/m_cpp)    << "x\n";
    std::cout << "ifce/concepts = " << (m_ifce/m_cpp)  << "x\n";
    std::cout << "virt/concepts = " << (m_virt/m_cpp)  << "x\n";
    std::cout << "sink=" << g_sink << std::endl;
    return 0;
}
