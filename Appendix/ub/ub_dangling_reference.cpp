// UB-L1 dangling reference：返回/持有已销毁对象的地址（指针版，可编译运行）
// 编译: g++ -std=c++23 -O2 -Wall -o dref ub_dangling_reference.cpp
#include <cstdio>

int* dangling() {
    int x = 5;            // 局部变量，dangling() 返回即销毁
    return &x;            // ❌ 返回局部变量地址 → 悬垂指针（-Wreturn-local-addr）
}

int main() {
    int* p = dangling();
    *p = 10;              // ❌ 写已销毁的栈槽
    std::printf("value = %d\n", *p);
    return 0;
}
