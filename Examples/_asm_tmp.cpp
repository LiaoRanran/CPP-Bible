// TMP 基础：值计算 / 类型分支 / 编译期判定 / integer_sequence
// 编译：g++ -std=c++23 -O2 -S -masm=intel _asm_tmp.cpp -o _asm_tmp.asm
#include <type_traits>
#include <utility>

// ① 编译期阶乘（值计算，部分特化终止递归）
template <int N>
struct Fact { static constexpr int value = N * Fact<N - 1>::value; };
template <>
struct Fact<0> { static constexpr int value = 1; };

// ② 编译期 GCD（递归值计算）
template <int A, int B>
struct Gcd { static constexpr int value = Gcd<B, A % B>::value; };
template <int A>
struct Gcd<A, 0> { static constexpr int value = A; };

// ③ 编译期素数判定（递归 + 部分特化基例）
template <int N, int D = N - 1>
struct IsPrime { static constexpr bool value = (N % D != 0) && IsPrime<N, D - 1>::value; };
template <int N>
struct IsPrime<N, 1> { static constexpr bool value = true; };
template <>
struct IsPrime<1> { static constexpr bool value = false; };
template <>
struct IsPrime<0> { static constexpr bool value = false; };

// ④ 类型分支：bool 参数 + 特化选择类型
template <bool B>
struct SelectT { using type = int; };
template <>
struct SelectT<false> { using type = double; };

// ⑤ integer_sequence 展开求和
template <int... Is>
int sum_seq(std::integer_sequence<int, Is...>) {
    return (0 + ... + Is);
}

int use_tmp() {
    volatile int a = Fact<5>::value;                              // 120
    volatile int b = Gcd<48, 36>::value;                          // 12
    volatile int c = IsPrime<17>::value;                          // 1（素数）
    volatile int d = IsPrime<15>::value;                          // 0（非素数）
    using T = SelectT<(sizeof(int) > 1)>::type;                   // 命中 SelectT<true> -> int
    volatile int e = (sizeof(T) == sizeof(int)) ? 1 : 0;          // 1
    volatile int f = sum_seq(std::make_integer_sequence<int, 6>{}); // 0+1+2+3+4+5 = 15
    return a + b + static_cast<int>(c) - static_cast<int>(d) + e + f; // 149
}
