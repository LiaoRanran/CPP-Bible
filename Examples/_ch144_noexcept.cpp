// ch144 ⑩ noexcept 影响 std::vector 重分配策略：移动构造非 noexcept 时走拷贝，noexcept 时走移动
// 编译：g++ -std=c++23 -O2 -S -masm=intel _ch144_noexcept.cpp -o _ch144_noexcept_O2.asm
#include <vector>

struct CopyOnly {            // 移动构造显式非 noexcept → vector 重分配时拷贝
    int x;
    CopyOnly(int v) : x(v) {}
    CopyOnly(CopyOnly&&) noexcept(false) = default;
    CopyOnly(const CopyOnly&) = default;
};

struct NoexceptMove {        // 移动构造 noexcept → vector 重分配时移动
    int x;
    NoexceptMove(int v) : x(v) {}
    NoexceptMove(NoexceptMove&&) noexcept = default;
    NoexceptMove(const NoexceptMove&) = default;
};

std::vector<CopyOnly> fill_copy() {
    std::vector<CopyOnly> v;
    for (int i = 0; i < 16; ++i) v.push_back(CopyOnly{i});   // 多次重分配，走拷贝
    return v;
}

std::vector<NoexceptMove> fill_move() {
    std::vector<NoexceptMove> v;
    for (int i = 0; i < 16; ++i) v.push_back(NoexceptMove{i}); // 多次重分配，走移动
    return v;
}
