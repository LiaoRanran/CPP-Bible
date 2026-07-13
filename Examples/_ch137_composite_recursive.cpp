// 文件: Examples/_ch137_composite_recursive.cpp
// Composite 递归遍历：统计整棵树的叶子数量
#include <cstddef>
#include <memory>
#include <vector>

struct Node {
    virtual ~Node() = default;
    virtual std::size_t leafCount() const = 0;
};

struct Leaf : Node {
    std::size_t leafCount() const override { return 1; }
};

struct Branch : Node {
    void add(std::unique_ptr<Node> n) { kids_.push_back(std::move(n)); }
    std::size_t leafCount() const override {
        std::size_t s = 0;
        for (auto& k : kids_) s += k->leafCount();   // 递归聚合
        return s;
    }
private:
    std::vector<std::unique_ptr<Node>> kids_;
};

int main() {
    Branch root;
    root.add(std::make_unique<Leaf>());
    auto b = std::make_unique<Branch>();
    b->add(std::make_unique<Leaf>());
    b->add(std::make_unique<Leaf>());
    root.add(std::move(b));
    return root.leafCount() == 3 ? 0 : 1;
}
