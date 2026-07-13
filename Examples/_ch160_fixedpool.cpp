// 文件：Examples/_ch160_fixedpool.cpp
// 行号：1
// 固定大小块内存池：free list 实现（核心，自包含可编译）
#include <cstddef>
#include <cstdint>
#include <vector>
#include <new>
#include <cstdio>
#include <cassert>

class FixedPool {
    struct FreeNode { FreeNode* next; };

    FreeNode* free_list_ = nullptr;
    std::vector<void*> chunks_;
    size_t block_size_   = 0;
    size_t per_chunk_    = 0;

    static constexpr size_t kAlign = alignof(std::max_align_t);

    void grow() {
        // 一次向堆申请一大块（chunk），切成 per_chunk_ 个等长子块并串成 free list
        size_t total = block_size_ * per_chunk_;
        void* mem = ::operator new(total);
        chunks_.push_back(mem);
        auto* base = static_cast<std::byte*>(mem);
        for (size_t i = 0; i < per_chunk_; ++i) {
            auto* node = reinterpret_cast<FreeNode*>(base + i * block_size_);
            node->next = free_list_;
            free_list_ = node;
        }
    }

public:
    explicit FixedPool(size_t block, size_t per_chunk = 4096)
        : block_size_(round_up(std::max(block, sizeof(FreeNode)), kAlign)),
          per_chunk_(per_chunk) {}

    FixedPool(const FixedPool&) = delete;
    FixedPool& operator=(const FixedPool&) = delete;

    ~FixedPool() {
        for (void* c : chunks_) ::operator delete(c);
    }

    void* allocate() {
        if (!free_list_) grow();
        FreeNode* n = free_list_;
        free_list_ = n->next;
        return n;
    }

    void deallocate(void* p) noexcept {
        auto* n = static_cast<FreeNode*>(p);
        n->next = free_list_;
        free_list_ = n;
    }

    size_t block_size() const { return block_size_; }

    static size_t round_up(size_t v, size_t a) {
        return (v + a - 1) & ~(a - 1);
    }
};

int main() {
    FixedPool pool(sizeof(double) * 8); // 64 字节块
    std::vector<void*> ptrs;
    ptrs.reserve(1000);
    for (int i = 0; i < 1000; ++i) {
        void* p = pool.allocate();
        assert(p != nullptr);
        ptrs.push_back(p);
    }
    for (void* p : ptrs) pool.deallocate(p);
    // 释放后内存可复用
    void* reuse = pool.allocate();
    pool.deallocate(reuse);
    std::printf("FixedPool OK: block_size=%zu, allocs=1000, reused=1\n",
                pool.block_size());
    return 0;
}
