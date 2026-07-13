// _ch138_dispatch.cpp
// 第138章 ⑲：虚函数 vs std::variant+visit vs if constexpr 三种分发在 -O2 下的真实汇编对比
#include <variant>
#include <iostream>

struct Base { virtual ~Base() = default; virtual int eval() const = 0; };
struct Add : Base { int eval() const override { return 1; } };
struct Sub : Base { int eval() const override { return 2; } };

struct VAdd { int eval() const { return 1; } };
struct VSub { int eval() const { return 2; } };
using Arith = std::variant<VAdd, VSub>;

template <typename T>
int eval_if(const T&) {
    if constexpr (std::is_same_v<T, Add>) return 1;
    else if constexpr (std::is_same_v<T, Sub>) return 2;
    else return 0;
}

// 虚函数分发：类型在调用点静态可知时会被去虚拟化
int via_virtual(const Base& b) { return b.eval(); }

// std::variant + std::visit 分发
int via_variant(const Arith& v) {
    return std::visit([](const auto& x) -> int { return x.eval(); }, v);
}

// if constexpr 编译期分发
template <typename T>
int via_if(const T& t) { return eval_if<T>(t); }

int main() {
    Add a; Sub s;
    int r = 0;
    r += via_virtual(a);
    r += via_virtual(s);
    Arith v = VAdd{}; r += via_variant(v);
    v = VSub{};       r += via_variant(v);
    r += via_if(a);
    r += via_if(s);
    std::cout << r << '\n';
    return r;
}
