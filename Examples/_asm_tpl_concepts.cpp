// Concepts：requires 约束，汇编层与 SFINAE 等价（同样发射 _ZN... 受约束实例化）
// 编译：g++ -std=c++23 -O2 -S -masm=intel _asm_tpl_concepts.cpp -o _asm_tpl_concepts.asm
#include <concepts>

template <std::integral T>
T concept_f(T x) { return x * 2; }

template <typename T>
requires (!std::integral<T>)
T concept_f(T x) { return x; }

// 自定义 concept 折叠为编译期 bool 谓词
template <typename T>
concept Addable = requires(T a, T b) { a + b; };

template <Addable T>
T add_twice(T x) { return x + x; }

int use_concepts() {
    volatile int    a = concept_f(21);     // 选 concept_f<int>
    volatile double b = concept_f(2.5);    // 选 concept_f<double>
    volatile int    c = add_twice(7);       // Addable 约束命中
    return a + static_cast<int>(b) + c;
}
