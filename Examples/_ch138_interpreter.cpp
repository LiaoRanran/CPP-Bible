// _ch138_interpreter.cpp
// 第138章 ⑰：解释器——为简单文法构建抽象语法树并求值
#include <iostream>
#include <memory>

struct Expr { virtual ~Expr() = default; virtual int eval() const = 0; };
struct Num : Expr { int v; explicit Num(int v) : v(v) {} int eval() const override { return v; } };
struct Add : Expr { std::unique_ptr<Expr> l, r; Add(std::unique_ptr<Expr> a, std::unique_ptr<Expr> b):l(std::move(a)),r(std::move(b)){} int eval() const override { return l->eval()+r->eval(); } };

int main() {
    auto e = std::make_unique<Add>(std::make_unique<Num>(2), std::make_unique<Num>(3));
    std::cout << e->eval() << '\n';
    return 0;
}
