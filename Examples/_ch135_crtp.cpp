// _ch135_crtp.cpp
// 取证目标（第⑧节）：CRTP 静态多态，零虚表、零间接调用。
#include <cstdio>

template <typename Derived>
struct ShapeBase {
    int area() const { return static_cast<const Derived*>(this)->impl_area(); }
};

struct Square : ShapeBase<Square> {
    int side;
    int impl_area() const { return side * side; }
};

int main() {
    Square s;
    s.side = 7;
    volatile int a = s.area(); // 完全在编译期解析，无 vtable
    (void)a;
}
