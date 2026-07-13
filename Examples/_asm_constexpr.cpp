// constexpr / consteval 编译期计算取证
// 编译：g++ -std=c++23 -O2 -S -masm=intel _asm_constexpr.cpp -o _asm_constexpr.asm
#include <type_traits>

constexpr int sq(int x) { return x * x; }
constexpr int fact(int n) { return n <= 1 ? 1 : n * fact(n - 1); }

template <typename T>
constexpr auto pick() {
    if constexpr (std::is_integral_v<T>) return T{42};
    else return 2.5;
}

consteval int ce_pow2(int n) { return 1 << n; }

constinit int g_global = 100;

int use_constexpr() {
    volatile int    a = sq(7);            // 49
    volatile int    b = fact(5);          // 120
    volatile int    c = pick<int>();      // 42
    volatile double d = pick<double>();   // 2.5
    volatile int    e = ce_pow2(4);       // 16
    return a + b + c + static_cast<int>(d) + e + g_global; // 329
}
