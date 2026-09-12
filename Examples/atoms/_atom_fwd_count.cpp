// Examples/_atom_fwd_count.cpp
// 服务 ATOM-MEM-VALUE-002：完美转发 vs 省略 std::forward 的运行时代价。
// 论断：转发链里具名右值引用形参在函数体内是左值（[basic.lval] Note 3），省略 std::forward 会把
//       右值实参当左值继续传 → 触发拷贝而非移动；std::forward<T>(x) 按推导出的 T 恢复原值类别。
// 纪律（沿用 EV-MEM-002/EV-MEM-008）：计数器 volatile + 复合写拆成 x = x + 1（C++20 起复合赋值弃用），
//       防 -O2 把计数折叠成立即数；-O0/-O2 双跑，输出逐字一致才算数。
#include <utility>
#include <iostream>

volatile long g_copies = 0;
volatile long g_moves = 0;

struct Box {
    Box() = default;
    Box(const Box&) { g_copies = g_copies + 1; }            // 拷贝：观测点
    Box(Box&&) noexcept { g_moves = g_moves + 1; }          // 移动：观测点
};

// 正确的完美转发：std::forward<T>(x) 按推导出的 T 恢复实参的值类别
template <class T>
Box wrap_forward(T&& x) { return Box(std::forward<T>(x)); }

// 省略 forward：x 是具名形参 → 函数体内是左值 → 永远走拷贝
template <class T>
Box wrap_bare(T&& x) { return Box(x); }

int main(int argc, char** argv) {
    long long seed = argc;                  // 运行时值：防常量折叠（与 EV-MEM-008 同纪律）
    (void)seed;

    // 组 1：forward 转发右值 → 移动
    Box b1;
    g_copies = 0; g_moves = 0;
    Box r1 = wrap_forward(std::move(b1));
    long fwd_rv_copies = g_copies, fwd_rv_moves = g_moves;

    // 组 2：forward 转发左值 → 拷贝（forward 不把左值变右值：保持值类别）
    Box b3;
    g_copies = 0; g_moves = 0;
    Box r3 = wrap_forward(b3);
    long fwd_lv_copies = g_copies, fwd_lv_moves = g_moves;

    // 组 3：省略 forward 转发右值 → 退化成拷贝（本卡的证伪对照/陷阱演示）
    Box b2;
    g_copies = 0; g_moves = 0;
    Box r2 = wrap_bare(std::move(b2));
    long bare_rv_copies = g_copies, bare_rv_moves = g_moves;

    volatile long sink = (&r1 != nullptr) + (&r2 != nullptr) + (&r3 != nullptr) + (long)seed;   // 强制观测，防整组消除
    (void)sink;

    std::cout << "forward rvalue: copies=" << fwd_rv_copies << " moves=" << fwd_rv_moves << "\n";
    std::cout << "forward lvalue: copies=" << fwd_lv_copies << " moves=" << fwd_lv_moves << "\n";
    std::cout << "no-forward rvalue: copies=" << bare_rv_copies << " moves=" << bare_rv_moves << "\n";
    return 0;
}
