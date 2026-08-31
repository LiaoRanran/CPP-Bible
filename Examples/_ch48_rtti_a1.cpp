#include <iostream>
#include <typeinfo>
#include <cassert>

struct Base { virtual ~Base() = default; virtual int op(int x) const { return x; } };
struct Derived : Base { int op(int x) const override { return x + 1; } };
struct Other : Base { int op(int x) const override { return x * 2; } };

int main() {
    Derived d;
    Base* pb = &d;

    // dynamic_cast 成功：指针确实指向 Derived
    Derived* pd = dynamic_cast<Derived*>(pb);
    assert(pd != nullptr);
    assert(pd->op(10) == 11);

    // dynamic_cast 失败：跨兄弟类型转型返回 nullptr（指针版不抛异常）
    Other* po = dynamic_cast<Other*>(pb);
    assert(po == nullptr);

    // typeid 精确比较：只判"精确同型"，不判 is-a
    const std::type_info& td = typeid(Derived);
    assert((typeid(*pb) == td));
    assert(!(typeid(*pb) == typeid(Other)));

    // 注意：typeid 不能替代 is-a 判定
    Base b;
    assert(!(typeid(b) == td));

    std::cout << "dynamic_cast ok : " << (pd != nullptr) << std::endl;
    std::cout << "cross cast null : " << (po == nullptr) << std::endl;
    std::cout << "all functional checks passed" << std::endl;
    return 0;
}