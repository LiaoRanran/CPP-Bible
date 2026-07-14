// UB-03 stack-use-after-scope：返回/保存局部变量地址并在其作用域外解引用
// 编译: g++ -std=c++23 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer -o sas ub_stack_after_scope.cpp
// 运行: ./sas  →  ASan 报 stack-use-after-scope
#include <cstdio>

int* leaked = nullptr;

void f() {
    int x = 5;        // 局部变量，生命周期限于 f()
    leaked = &x;      // ❌ 保存指向局部变量的指针
}                     // x 在此销毁，leaked 变为悬垂

int main() {
    f();
    *leaked = 10;     // ❌ UB：作用域外写栈内存
    std::printf("leaked = %d\n", *leaked);
    return 0;
}
