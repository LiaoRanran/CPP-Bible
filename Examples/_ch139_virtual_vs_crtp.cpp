// _ch139_virtual_vs_crtp.cpp
// 取证目的：对比「虚函数动态分派」与「CRTP 静态分派」在 -O2 下的汇编差异。
#include <iostream>

struct ShapeV {
    virtual double area() const = 0;
    virtual ~ShapeV() = default;
};
struct CircleV : ShapeV {
    double r;
    CircleV(double r_) : r(r_) {}
    double area() const override { return 3.141592653589793 * r * r; }
};

template <typename Derived>
struct ShapeC {
    double area() const { return static_cast<const Derived*>(this)->area_impl(); }
};
struct CircleC : ShapeC<CircleC> {
    double r;
    CircleC(double r_) : r(r_) {}
    double area_impl() const { return 3.141592653589793 * r * r; }
};

// 动态分派：经过虚表，无法在编译期内联（除非 LTO + 单一定点）
double process_v(const ShapeV& s) { return s.area() * 2.0; }

// 静态分派：area_impl 在编译期已知，可被完全内联展开
double process_c(const ShapeC<CircleC>& s) { return s.area() * 2.0; }

int main() {
    CircleV cv{2.0};
    CircleC cc{2.0};
    double a = process_v(cv) + process_c(cc);
    std::cout << a << "\n";
}
