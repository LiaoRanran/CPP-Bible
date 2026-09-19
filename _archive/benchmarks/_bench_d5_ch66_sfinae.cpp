// _bench_d5_ch66_sfinae.cpp — ch66 SFINAE / if-constexpr / tag-dispatch / virtual / variant 的运行时分派开销
// GCC 15.3.0 (MinGW-W64 x86_64), g++ -O2 -std=c++23
// 编译期已知类型时，SFINAE / if-constexpr / tag-dispatch 三者都解析为同一段直接调用机器码（零分派开销）；
// 真正的运行时开销只出现在 virtual（vtable 间接）与 std::variant+visit（访问器分派）上。
#include <iostream>
#include <chrono>
#include <variant>
#include <type_traits>
#include <algorithm>

static volatile long long g_sink = 0;

struct AnimalCat { double sound() const { return 1.0; } };
struct AnimalDog { double sound() const { return 2.0; } };

// (A) if-constexpr 分派（编译期定类型）
template <class T>
double handle_ifce(T a) {
    if constexpr (std::is_same_v<T, AnimalCat>) return a.sound() * 10.0;
    else                                        return a.sound() * 20.0;
}

// (B) tag 分派（重载决议在编译期定）
template <class T> struct tag {};
double handle_tag(AnimalCat, tag<AnimalCat>) { return 10.0; }
double handle_tag(AnimalDog, tag<AnimalDog>) { return 20.0; }
template <class T> double handle_tag(T a) { return handle_tag(a, tag<T>{}); }

// (C) SFINAE 重载集（编译期定）
template <class T, std::enable_if_t<std::is_same_v<T, AnimalCat>, int> = 0>
double handle_sfinae(T) { return 10.0; }
template <class T, std::enable_if_t<std::is_same_v<T, AnimalDog>, int> = 0>
double handle_sfinae(T) { return 20.0; }

// (D) virtual（运行时多态）
struct AnimalBase { virtual double sound() const = 0; virtual ~AnimalBase() = default; };
struct Cat : AnimalBase { double sound() const override { return 10.0; } };
struct Dog : AnimalBase { double sound() const override { return 20.0; } };

// (E) std::variant + visit（运行时分派）
using AnimalVar = std::variant<AnimalCat, AnimalDog>;

int main() {
    const long long ITERS = 200'000'000LL;
    const int RUNS = 5;

    AnimalCat cat; AnimalDog dog;
    Cat g_cat; Dog g_dog;
    AnimalBase* g_arr[2] = { &g_cat, &g_dog };
    AnimalVar   g_var[2] = { AnimalCat{}, AnimalDog{} };
    static volatile int g_sel = 0;

    double r_ifce[RUNS], r_tag[RUNS], r_sf[RUNS], r_virt[RUNS], r_vis[RUNS];

    for (int r = 0; r < RUNS; ++r) {
        // (A) if-constexpr —— T 编译期已知
        { auto t0=std::chrono::steady_clock::now(); double s=0.0;
          for (long long i=0;i<ITERS;++i) s += handle_ifce(cat);
          auto t1=std::chrono::steady_clock::now(); g_sink+=(long long)s; r_ifce[r]=std::chrono::duration<double,std::milli>(t1-t0).count(); }
        // (B) tag
        { auto t0=std::chrono::steady_clock::now(); double s=0.0;
          for (long long i=0;i<ITERS;++i) s += handle_tag(dog);
          auto t1=std::chrono::steady_clock::now(); g_sink+=(long long)s; r_tag[r]=std::chrono::duration<double,std::milli>(t1-t0).count(); }
        // (C) SFINAE
        { auto t0=std::chrono::steady_clock::now(); double s=0.0;
          for (long long i=0;i<ITERS;++i) s += handle_sfinae(cat);
          auto t1=std::chrono::steady_clock::now(); g_sink+=(long long)s; r_sf[r]=std::chrono::duration<double,std::milli>(t1-t0).count(); }
        // (D) virtual —— 运行时 idx 强制 vtable 分派
        { auto t0=std::chrono::steady_clock::now(); double s=0.0;
          for (long long i=0;i<ITERS;++i){ g_sel=(g_sel+1)&1; int idx=g_sel; s += g_arr[idx]->sound(); }
          auto t1=std::chrono::steady_clock::now(); g_sink+=(long long)s; r_virt[r]=std::chrono::duration<double,std::milli>(t1-t0).count(); }
        // (E) variant + visit —— 运行时 idx 强制访问器分派
        { auto t0=std::chrono::steady_clock::now(); double s=0.0;
          for (long long i=0;i<ITERS;++i){ g_sel=(g_sel+1)&1; int idx=g_sel; s += std::visit([](auto&& a){ return a.sound(); }, g_var[idx]); }
          auto t1=std::chrono::steady_clock::now(); g_sink+=(long long)s; r_vis[r]=std::chrono::duration<double,std::milli>(t1-t0).count(); }
    }

    std::sort(r_ifce,r_ifce+RUNS); std::sort(r_tag,r_tag+RUNS); std::sort(r_sf,r_sf+RUNS);
    std::sort(r_virt,r_virt+RUNS); std::sort(r_vis,r_vis+RUNS);
    double m_ifce=r_ifce[2], m_tag=r_tag[2], m_sf=r_sf[2], m_virt=r_virt[2], m_vis=r_vis[2];
    double base = m_ifce;

    std::cout << "ch66 dispatch overhead (ITERS=" << ITERS << ")\n";
    std::cout << "if-constexpr (compile-time) median = " << m_ifce << " ms\n";
    std::cout << "tag-dispatch (compile-time) median = " << m_tag  << " ms\n";
    std::cout << "SFINAE       (compile-time) median = " << m_sf   << " ms\n";
    std::cout << "virtual       (runtime)      median = " << m_virt << " ms\n";
    std::cout << "variant+visit (runtime)      median = " << m_vis  << " ms\n";
    std::cout << "tag/ifce   = " << (m_tag/m_ifce)  << "x\n";
    std::cout << "sfinae/ifce= " << (m_sf/m_ifce)   << "x\n";
    std::cout << "virt/ifce  = " << (m_virt/m_ifce) << "x\n";
    std::cout << "visit/ifce = " << (m_vis/m_ifce)  << "x\n";
    std::cout << "sink=" << g_sink << std::endl;
    return 0;
}
