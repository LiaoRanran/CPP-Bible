// _ch147_smartptr.cpp —— 优先使用 RAII 智能指针（坏味道对比）
#include <memory>

struct Node {
    int v = 0;
};

// 坏味道：裸 owning 指针
Node* make_bad() {
    return new Node();      // 调用方必须记得 delete
}

// 好味道：返回 unique_ptr
std::unique_ptr<Node> make_good() {
    return std::make_unique<Node>();
}
