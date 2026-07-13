// 折叠表达式 codegen：一元左折叠展开为单条加法链（无递归调用开销）
// 编译：g++ -std=c++23 -O2 -S -masm=intel _asm_tpl_fold.cpp -o _asm_tpl_fold.asm
#include <utility>

template <typename... Ts>
auto fold_add(Ts... ts) {
    return (0 + ... + ts);             // 一元左折叠
}

template <typename... Ts>
auto fold_mul(Ts... ts) {
    return (1 * ... * ts);             // 一元左折叠（乘法）
}

template <typename... Ts>
auto fold_and(Ts... ts) {
    return (... && ts);                // 一元右折叠（逻辑与，短路语义）
}

int use_fold() {
    auto a = fold_add(1, 2, 3, 4, 5);   // 期望 15：单链 add
    auto b = fold_mul(2, 3, 4);         // 期望 24
    auto c = fold_and(true, true, false); // 期望 false
    return static_cast<int>(a + b) + (c ? 1 : 0);
}
