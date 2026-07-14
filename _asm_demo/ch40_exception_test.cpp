// ch40 exception_safety 汇编实证 —— noexcept 零成本路径
#include <cstdint>
#include <type_traits>
#include <utility>

// 观测 1: noexcept 函数 vs 可能抛异常的函数
// 编译器在调用 noexcept 函数时不做 unwinding 准备（零管理费）
int may_throw_div(int a, int b) {
    if (b == 0) throw "division by zero";
    return a / b;
}

int noexcept_add(int a, int b) noexcept {
    return a + b;                                     // 绝无异常 → 编译器不插 unwind 表
}

// 观测 2: 调用者——noexcept vs 可能抛异常
int call_may_throw(int x, int y) {
    return may_throw_div(x, y);                       // 编译插入 LSDA (Language-Specific Data Area) 异常处理表
}

int call_noexcept(int x, int y) {
    return noexcept_add(x, y);                        // 无 LSDA 插入!
}

// 观测 3: move_if_noexcept 的编译期分支
template <typename T>
typename std::enable_if_t<std::is_nothrow_move_constructible_v<T>, T>
safe_move(T&& t) {
    return std::forward<T>(t);                        // 编译器知道 noexcept → 安心 move
}

// 测试: Big 标记 noexcept 后 vs 无标记
struct BigNoExcept {
    int* data; size_t sz;
    BigNoExcept(BigNoExcept&& other) noexcept : data(other.data), sz(other.sz) {
        other.data = nullptr;
    }
};

void test_strong_guarantee(BigNoExcept&& b) {
    BigNoExcept local(std::move(b));                   // noexcept move → 强异常安全
}
