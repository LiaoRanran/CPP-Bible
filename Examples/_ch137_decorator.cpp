// 文件: Examples/_ch137_decorator.cpp
// Decorator：用组合而非继承，运行时动态叠加职责
#include <iostream>
#include <memory>

struct Coffee {
    virtual ~Coffee() = default;
    virtual double cost() const = 0;
    virtual const char* desc() const = 0;
};

struct Simple : Coffee {
    double cost() const override { return 2.0; }
    const char* desc() const override { return "Coffee"; }
};

struct Decorator : Coffee {
    explicit Decorator(std::unique_ptr<Coffee> c) : wrapped_(std::move(c)) {}
protected:
    std::unique_ptr<Coffee> wrapped_;
};

struct Milk : Decorator {
    using Decorator::Decorator;
    double cost() const override { return wrapped_->cost() + 0.5; }
    const char* desc() const override { return "Milk+Coffee"; }
};

struct Sugar : Decorator {
    using Decorator::Decorator;
    double cost() const override { return wrapped_->cost() + 0.2; }
    const char* desc() const override { return "Sugar+Milk+Coffee"; }
};

int main() {
    auto c = std::make_unique<Sugar>(std::make_unique<Milk>(std::make_unique<Simple>()));
    std::cout << c->desc() << ' ' << c->cost() << '\n';
}
