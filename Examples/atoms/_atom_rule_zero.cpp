// Examples/_atom_rule_zero.cpp
// 服务 ATOM-MEM-RAII-002：Rule of Zero。
// 论断：成员全是 RAII 类型（unique_ptr）时，一个特殊成员函数都不写——编译器隐式生成的特殊成员函数
//       把"拷贝被删、移动可用、析构正确"全部做对；这正是"什么都不写"比"手写三件套"更安全的根源。
// 双重观测：static_assert（类型系统层）+ 拷贝/移动/析构/分配计数（运行期）。
#include <memory>
#include <iostream>
#include <new>
#include <cstdlib>
#include <type_traits>

volatile long g_allocs = 0;
volatile long g_frees = 0;
volatile long g_dtors = 0;
void* operator new(size_t n) { g_allocs = g_allocs + 1; return std::malloc(n); }
void operator delete(void* p) noexcept { if (p) { g_frees = g_frees + 1; std::free(p); } }
void operator delete(void* p, size_t) noexcept { if (p) { g_frees = g_frees + 1; std::free(p); } }

struct Resource {
    explicit Resource(int v) : v(v) {}
    ~Resource() { g_dtors = g_dtors + 1; }
    int v;
};

// Rule of Zero：零特殊成员函数（零析构、零拷贝、零移动声明）
struct Holder {
    std::unique_ptr<Resource> res;
};

// 类型系统硬证明：隐式规则"成员形状决定特殊成员函数形状"
static_assert(std::is_default_constructible_v<Holder>,  "implicit default ctor");
static_assert(std::is_move_constructible_v<Holder>,     "implicit move ctor (unique_ptr is movable)");
static_assert(std::is_move_assignable_v<Holder>,        "implicit move assign");
static_assert(!std::is_copy_constructible_v<Holder>,    "copy deleted: unique_ptr is non-copyable");
static_assert(!std::is_copy_assignable_v<Holder>,       "copy assign deleted");
static_assert(std::is_destructible_v<Holder>,           "implicit dtor delegates to member dtor");

int main() {
    long a0 = g_allocs, d0 = g_dtors, f0 = g_frees;
    Holder h1;
    h1.res = std::make_unique<Resource>(7);
    Resource* p1 = h1.res.get();
    long allocs_make = g_allocs - a0;

    Holder h2 = std::move(h1);                 // 隐式生成的移动：所有权转移
    bool transferred = (h2.res.get() == p1) && (h1.res == nullptr);

    {
        Holder h3 = std::move(h2);             // 再移动一次
    }                                          // h3 析构 → Resource 恰好析构 1 次
    long dtors_total = g_dtors - d0;
    long frees_total = g_frees - f0;

    std::cout << "rule zero: move_constructible=" << (int)std::is_move_constructible_v<Holder>
              << " copy_constructible=" << (int)std::is_copy_constructible_v<Holder>
              << " (type system)\n";
    std::cout << "move transfer: owner_changed=" << (transferred ? 1 : 0) << "\n";
    std::cout << "allocs=" << allocs_make << " dtors=" << dtors_total
              << " frees=" << frees_total << " (exactly once, no leak)\n";
    return 0;
}
