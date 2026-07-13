// 文件：Examples/_ch160_union.cpp
// 行号：1
// union 技巧：空闲节点与用户数据复用同一块内存，零额外元数据开销
#include <cstddef>
#include <cstdio>
#include <cstdlib>

union FreeNode {
    FreeNode* next;   // 块空闲时：指向下一个空闲块
    char      raw[1]; // 块使用时：用户数据首字节（仅占位，真实大小由池决定）
};

struct FreeList {
    FreeNode* head = nullptr;
    void push(void* p) {
        auto* n = static_cast<FreeNode*>(p);
        n->next = head;
        head = n;
    }
    void* pop() {
        if (!head) return nullptr;
        FreeNode* n = head;
        head = n->next;
        return n;
    }
};

int main() {
    void* chunk = std::malloc(4 * 64);
    FreeList fl;
    // 把 4 个 64 字节子块串起来
    for (int i = 0; i < 4; ++i)
        fl.push(static_cast<char*>(chunk) + i * 64);
    for (int i = 0; i < 4; ++i) {
        void* p = fl.pop();
        std::printf("pop -> %p\n", p);
    }
    std::printf("pop(empty) -> %p\n", fl.pop());
    std::free(chunk);
    return 0;
}
