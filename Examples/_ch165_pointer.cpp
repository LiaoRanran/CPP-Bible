// _ch165_pointer.cpp : 指针/数组/函数指针练习（初级→中级）
// 编译: g++ -std=c++23 -O2 -Wall -Wextra _ch165_pointer.cpp -o _ch165_pointer
#include <iostream>

int add(int a, int b) { return a + b; }

int main() {
    int x = 10;
    int* p = &x;                 // 取地址
    std::cout << *p << "\n";     // 解引用

    int arr[5] = {1, 2, 3, 4, 5};
    int* q = arr;                // 数组退化成指针
    std::cout << *(q + 2) << "\n"; // 指针算术: 等价于 arr[2]

    int (*fp)(int, int) = &add;  // 函数指针
    std::cout << fp(3, 4) << "\n";

    // const 指针 vs 指向 const 的指针
    const int* cp = &x;          // 指向的内容不可改
    int* const pc = &x;          // 指针本身不可改
    (void)cp; (void)pc;
    return 0;
}
