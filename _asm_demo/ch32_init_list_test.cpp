// ASM-32-init_list : std::initializer_list 实证（GCC 15.3.0, C++26, -O2）
// 目标：证明 initializer_list 仅是一对 {const T* ptr, size_t len}（两寄存器传递，零分配、零拷贝）；
//       range-for 退化为指针自增循环；并指出致命陷阱：底层临时数组的生命周期仅限完整表达式。
#include <initializer_list>
#include <iostream>

// (1) 求和：init list 以 (ptr, len) 两寄存器传入；range-for 退化为指针循环
int sum_il(std::initializer_list<int> il) {
    int s = 0;
    for (auto x : il) s += x;
    return s;
}

// (2) begin() 即返回底层数组指针
const int* il_begin(std::initializer_list<int> il) {
    return il.begin();
}

// (3) 生命周期陷阱原型：返回 initializer_list 时，底层临时数组已在 ; 处销毁 —— 悬垂指针
std::initializer_list<int> dangling_il() {
    return {1, 2, 3};  // 底层数组为栈上临时，函数返回后失效
}

int main() {
    volatile int sink = 0;
    sink = sum_il({10, 20, 30, 40});   // 期望：调用点构造栈上临时数组，传 ptr+len
    sink += *il_begin({1, 2, 3});      // 期望：返回该栈数组首地址
    return (int)sink;
}
