// _ch139_static_downcast.cpp
// 取证目的：基类如何无虚函数地把 this 静态下转而调用派生类方法。
#include <iostream>

template <typename Derived>
struct Base {
    void interface() {
        // 关键：static_cast<Derived*>(this) 在实例化时已知 Derived
        static_cast<Derived*>(this)->impl();
    }
};

struct DerivedA : Base<DerivedA> {
    void impl() { std::cout << "DerivedA::impl\n"; }
};
struct DerivedB : Base<DerivedB> {
    void impl() { std::cout << "DerivedB::impl\n"; }
};

int main() {
    DerivedA a;
    DerivedB b;
    a.interface();
    b.interface();
}
