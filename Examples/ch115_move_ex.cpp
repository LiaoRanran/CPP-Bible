// ②-1 前置：右值引用绑定到临时（独立可编译）
#include <iostream>
#include <utility>

void take_rref(int&& x) { std::cout << x << "\n"; }

int main() {
    take_rref(42);                  // ✅ 字面量是 prvalue，可绑定到 int&&
    // int a = 1; take_rref(a);     // ❌ a 是 lvalue，不能绑定到 int&&
    int b = 1; take_rref(std::move(b));   // ✅ std::move 把 b 当右值
    return 0;
}