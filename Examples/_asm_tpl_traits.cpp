// 类型特性 Type Traits：编译期求值，零运行期开销
// 编译：g++ -std=c++23 -O2 -S -masm=intel _asm_tpl_traits.cpp -o _asm_tpl_traits.asm
#include <type_traits>

// 手写 is_same
template <typename, typename> struct MyIsSame : std::false_type {};
template <typename T> struct MyIsSame<T, T> : std::true_type {};
template <typename A, typename B>
inline constexpr bool my_is_same_v = MyIsSame<A, B>::value;

// 手写 integral_constant 风格 tag
template <typename T, T V>
struct MyIntegralConstant { static constexpr T value = V; };

// 编译期根据 trait 派发（if constexpr）
template <typename T>
int classify(T) {
    if constexpr (my_is_same_v<T, int>)      return 1;
    else if constexpr (std::is_pointer_v<T>) return 2;
    else if constexpr (std::is_floating_point_v<T>) return 3;
    else return 0;
}

int use_traits() {
    // 编译期谓词直接折叠为常量
    static_assert(my_is_same_v<int, int>);
    static_assert(!my_is_same_v<int, double>);
    MyIntegralConstant<int, 42> ic;
    volatile auto v = ic.value;            // 期望 42 编译期常量
    return classify(5) + classify(1.0) + classify("s") + static_cast<int>(v);
}
