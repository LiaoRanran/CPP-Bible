// _ch135_virtual_dispatch.cpp
// 取证目标（第⑮节）：对比「虚调用」与「直接调用」在 -O2 下的汇编差异。
#include <cstdio>

struct Animal {
    virtual ~Animal() = default;
    virtual int speak() const = 0;
};

struct Dog : Animal {
    int speak() const override { return 42; }
};

// 直接调用：编译期已知类型为 Dog，可被内联/常量折叠
int direct(const Dog& d) { return d.speak(); }

// 虚调用：经过基类引用，必须查 vtable
int via_virtual(const Animal& a) { return a.speak(); }

int main() {
    Dog d;
    volatile int sink = direct(d) + via_virtual(d);
    (void)sink;
}
