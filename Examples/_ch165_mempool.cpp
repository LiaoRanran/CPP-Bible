// _ch165_mempool.cpp : 定长内存池片段（从零项目，见第160章 内存池）
#include <cstddef>
#include <iostream>
#include <vector>

class FixedPool {
    struct Block { Block* next; };
    Block* free_ = nullptr;
    std::vector<char*> pages_;
    size_t bsize_;
public:
    explicit FixedPool(size_t bsize, size_t per_page = 1024)
        : bsize_(bsize < sizeof(Block) ? sizeof(Block) : bsize) {
        grow(per_page);
    }
    void grow(size_t n) {
        char* p = new char[bsize_ * n];
        pages_.push_back(p);
        for (size_t i = 0; i < n; ++i) {
            Block* b = reinterpret_cast<Block*>(p + i * bsize_);
            b->next = free_; free_ = b;
        }
    }
    void* alloc() {
        if (!free_) grow(1024);
        Block* b = free_; free_ = b->next; return b;
    }
    void free(void* p) { Block* b = static_cast<Block*>(p); b->next = free_; free_ = b; }
    ~FixedPool() { for (char* p : pages_) delete[] p; }
};

int main() {
    FixedPool pool(sizeof(int));
    int* a = static_cast<int*>(pool.alloc());
    int* b = static_cast<int*>(pool.alloc());
    *a = 1; *b = 2;
    std::cout << *a << " " << *b << "\n";
    pool.free(a); pool.free(b);
    return 0;
}
