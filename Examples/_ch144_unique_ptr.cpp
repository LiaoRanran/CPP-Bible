#include <memory>

struct Node {
    int val;
    Node* next;
};

// 裸指针访问
int read_raw(Node* p) {
    return p->val;
}

// unique_ptr 访问：应当折叠为同样的指针解引用
int read_unique(const std::unique_ptr<Node>& p) {
    return p->get()->val;
}
