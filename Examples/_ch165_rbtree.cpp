// _ch165_rbtree.cpp : 红黑树节点骨架 + BST 序插入（平衡旋转为练习，见第159章 数据结构）
#include <cassert>
#include <iostream>

enum Color { RED, BLACK };

struct Node {
    int key;
    Color color;
    Node* left = nullptr;
    Node* right = nullptr;
    Node* parent = nullptr;
    Node(int k) : key(k), color(RED) {}
};

// 左旋/右旋是红黑树核心，此处仅给签名，练习时补全
void left_rotate(Node*& root, Node* x);
void right_rotate(Node*& root, Node* y);

// 按 BST 序插入（未做着色平衡，练习补全 fixup）
Node* bst_insert(Node* root, int k) {
    Node* n = new Node(k);
    if (!root) return n;
    Node* cur = root;
    while (true) {
        if (k < cur->key) {
            if (!cur->left) { cur->left = n; n->parent = cur; break; }
            cur = cur->left;
        } else if (k > cur->key) {
            if (!cur->right) { cur->right = n; n->parent = cur; break; }
            cur = cur->right;
        } else { delete n; break; }   // 去重
    }
    return root;
}

void inorder(Node* r) {
    if (!r) return;
    inorder(r->left); std::cout << r->key << " "; inorder(r->right);
}

int main() {
    Node* root = nullptr;
    for (int k : {10, 20, 5, 6, 15, 30}) root = bst_insert(root, k);
    inorder(root); std::cout << "\n";   // 5 6 10 15 20 30
    (void)left_rotate; (void)right_rotate;
    return 0;
}
