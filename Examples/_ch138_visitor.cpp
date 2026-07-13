// _ch138_visitor.cpp
// 第138章 ⑬：访问者——double dispatch，对异构元素施加操作而不修改其类
#include <iostream>
#include <memory>
#include <vector>

struct Visitor;
struct Element { virtual ~Element() = default; virtual void accept(Visitor& v) = 0; };
struct Circle; struct Square;

struct Visitor {
    virtual void visit(Circle&) = 0;
    virtual void visit(Square&) = 0;
};

struct Circle : Element { double r = 1; void accept(Visitor& v) override; };
struct Square : Element { double a = 1; void accept(Visitor& v) override; };

void Circle::accept(Visitor& v) { v.visit(*this); }
void Square::accept(Visitor& v) { v.visit(*this); }

struct Area : Visitor {
    double out = 0;
    void visit(Circle& c) override { out += 3.14 * c.r * c.r; }
    void visit(Square& s) override { out += s.a * s.a; }
};

int main() {
    std::vector<std::unique_ptr<Element>> v;
    v.push_back(std::make_unique<Circle>());
    v.push_back(std::make_unique<Square>());
    Area a; for (auto& e : v) e->accept(a);
    std::cout << a.out << '\n';
    return 0;
}
