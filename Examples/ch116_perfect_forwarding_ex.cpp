// ④-a 万能引用 vs 右值引用：推导结果一目了然
#include <type_traits>
#include <iostream>
template <class T>
void probe(T&&) {
    if constexpr (std::is_lvalue_reference_v<T>) std::cout << "lvalue" << std::endl;
    else std::cout << "rvalue" << std::endl;
}
void sink(int&&) {}            // 这是右值引用（不是模板 T&&）
int main() {
    int x = 0;
    probe(x);                  // T = int&  → 左值引用
    probe(42);                 // T = int   → 右值引用
    sink(42);                  // 右值引用绑右值
    return 0;
}