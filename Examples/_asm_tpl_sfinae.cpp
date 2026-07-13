// SFINAE：enable_if 让两个重载在实例化时二选一（不报错，剔除失败候选）
// 编译：g++ -std=c++23 -O2 -S -masm=intel _asm_tpl_sfinae.cpp -o _asm_tpl_sfinae.asm
#include <type_traits>

// 重载 A：仅当 T 是 integral 时该模板参与重载集
template <typename T, std::enable_if_t<std::is_integral_v<T>, int> = 0>
T sfinae_f(T x) { return x * 2; }

// 重载 B：仅当 T 不是 integral 时参与（! 取反）
template <typename T, std::enable_if_t<!std::is_integral_v<T>, int> = 0>
T sfinae_f(T x) { return x; }

int use_sfinae() {
    volatile int    a = sfinae_f(21);    // 选 A：sfinae_f<int>
    volatile double b = sfinae_f(2.5);   // 选 B：sfinae_f<double>
    return a + static_cast<int>(b);
}
