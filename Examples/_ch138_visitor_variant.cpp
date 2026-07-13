// _ch138_visitor_variant.cpp
// 第138章 ⑭：用 std::variant + std::visit 实现无虚函数的访问者
#include <iostream>
#include <variant>

struct Circle { double r = 1; };
struct Square { double a = 1; };
using Shape = std::variant<Circle, Square>;

struct Area {
    double operator()(const Circle& c) const { return 3.14 * c.r * c.r; }
    double operator()(const Square& s) const { return s.a * s.a; }
};

int main() {
    Shape s = Square{};
    std::cout << std::visit(Area{}, s) << '\n';
    s = Circle{2};
    std::cout << std::visit(Area{}, s) << '\n';
    return 0;
}
