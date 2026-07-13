// _ch139_counter.cpp
// 取证目的：CRTP 实现编译期「每派生类独立」的实例计数器。
#include <iostream>

template <typename T>
struct Counter {
    static inline int count = 0;
    Counter() { ++count; }
    Counter(const Counter&) { ++count; }
    ~Counter() { --count; }
    static int live() { return count; }
};

struct Widget : Counter<Widget> {
    int id;
    Widget(int i) : id(i) {}
};
struct Gadget : Counter<Gadget> {
    int id;
    Gadget(int i) : id(i) {}
};

int main() {
    Widget w1(1), w2(2);
    Gadget g1(1);
    std::cout << "Widget live=" << Widget::live()
              << " Gadget live=" << Gadget::live() << "\n";
}
