#include <iostream>
#include <cassert>
#include <cstdlib>
#include <vector>

struct Node { Node* next; int tag; };

struct Pool {
    Node* free_list = nullptr;
    std::vector<void*> blocks;
    Pool(std::size_t n) {
        blocks.reserve(n);
        for (std::size_t i = 0; i < n; ++i) {
            Node* p = static_cast<Node*>(std::malloc(sizeof(Node)));
            p->next = free_list; free_list = p;
            blocks.push_back(p);
        }
    }
    void* alloc() { Node* n = free_list; if (n) free_list = n->next; return n; }
    void dealloc(void* p) { Node* n = static_cast<Node*>(p); n->next = free_list; free_list = n; }
    ~Pool() { for (void* p : blocks) std::free(p); }
};

int main() {
    const int N = 1000;
    Pool pool(N);
    std::vector<void*> ptrs; ptrs.reserve(N);
    for (int i = 0; i < N; ++i) {
        void* p = pool.alloc();
        assert(p != nullptr);              // 池内仍有空闲节点
        static_cast<Node*>(p)->tag = i;    // 写入可观测内容
        ptrs.push_back(p);
    }
    assert(pool.free_list == nullptr);     // 全部分配后空闲链表清空

    for (int i = 0; i < N; ++i)            // 内容正确：tag 仍可逐条读回
        assert(static_cast<Node*>(ptrs[i])->tag == i);

    for (void* p : ptrs) pool.dealloc(p);  // 回收后地址复用
    assert(pool.free_list != nullptr);
    void* reused = pool.alloc();
    bool ok = false;
    for (void* p : ptrs) if (p == reused) { ok = true; break; }
    assert(ok);                            // 地址被真实复用
    std::cout << "pool reused addr : " << ok << std::endl;
    std::cout << "all functional checks passed" << std::endl;
    return 0;
}