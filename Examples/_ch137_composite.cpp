// 文件: Examples/_ch137_composite.cpp
// Composite：叶子节点与容器节点统一接口，客户端无差别对待
#include <iostream>
#include <memory>
#include <vector>

struct Component {
    virtual ~Component() = default;
    virtual void operation() const = 0;
};

struct Leaf : Component {
    void operation() const override { std::cout << "Leaf\n"; }
};

struct Composite : Component {
    void add(std::unique_ptr<Component> c) { children_.push_back(std::move(c)); }
    void operation() const override {
        for (auto& c : children_) c->operation();   // 递归作用于子节点
    }
private:
    std::vector<std::unique_ptr<Component>> children_;
};

int main() {
    Composite root;
    root.add(std::make_unique<Leaf>());
    auto sub = std::make_unique<Composite>();
    sub->add(std::make_unique<Leaf>());
    root.add(std::move(sub));
    root.operation();
}
