// 文件: Examples/_ch137_adapter_class.cpp
// 类适配器：用 private 继承复用被适配者实现，public 继承目标接口
#include <iostream>

class Adaptee {
public:
    void specificRequest() const { std::cout << "Adaptee::specificRequest\n"; }
};

class Target {
public:
    virtual ~Target() = default;
    virtual void request() const = 0;
};

class ClassAdapter : public Target, private Adaptee {
public:
    void request() const override { specificRequest(); }  // 直接复用继承来的实现
};

int main() {
    ClassAdapter a;
    Target& t = a;
    t.request();
}
