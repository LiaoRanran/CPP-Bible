// Examples/_atom_rule_five_noexcept.cpp
// 服务 ATOM-MEM-RAII-002：Rule of Five 的 noexcept 细节。
// 论断：vector 扩容搬迁元素用 move_if_noexcept——移动构造标了 noexcept 才用移动；
//       写了移动构造但漏了 noexcept，扩容退化为逐个拷贝（性能静默损失，编译器不告警）。
// 计数纪律：volatile 计数器 + x = x + 1 拆写（C++20 起复合赋值弃用）。
#include <vector>
#include <iostream>
#include <type_traits>

volatile long g_copy = 0;
volatile long g_move = 0;

struct Noex {                               // Rule of Five：五件套中移动标 noexcept
    Noex() = default;
    Noex(const Noex&) { g_copy = g_copy + 1; }
    Noex(Noex&&) noexcept { g_move = g_move + 1; }
};
struct Throwing {                           // 唯一差异：移动构造不标 noexcept
    Throwing() = default;
    Throwing(const Throwing&) { g_copy = g_copy + 1; }
    Throwing(Throwing&&) { g_move = g_move + 1; }
};

static_assert(std::is_nothrow_move_constructible_v<Noex>,     "noexcept marked");
static_assert(!std::is_nothrow_move_constructible_v<Throwing>, "noexcept missing");

int main() {
    std::vector<Noex> v1;
    v1.resize(4);                              // 4 个默认构造（不计入搬迁观测）
    long c0 = g_copy, m0 = g_move;
    v1.reserve(64);                            // 扩容搬迁 4 个已有元素
    long cp_noex = g_copy - c0, mv_noex = g_move - m0;

    std::vector<Throwing> v2;
    v2.resize(4);
    long c1 = g_copy, m1 = g_move;
    v2.reserve(64);                            // 同样扩容搬迁 4 个元素
    long cp_throw = g_copy - c1, mv_throw = g_move - m1;

    std::cout << "noexcept move: relocation copies=" << cp_noex << " moves=" << mv_noex << "\n";
    std::cout << "throwing move: relocation copies=" << cp_throw << " moves=" << mv_throw << "\n";
    return 0;
}
