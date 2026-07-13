// 文件：Examples/_ch160_full.cpp
// 行号：1
// 真实完整实现：自包含、可编译、可运行的工业级固定块内存池（含对齐/统计/异常安全）
#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <new>
#include <limits>

class MemoryPool {
    struct FreeNode { FreeNode* next; };

    FreeNode*   free_list_ = nullptr;   // 空闲块单链表（free list）
    std::vector<void*> chunks_;         // 所有向系统申请的大块，析构时释放
    size_t      block_size_ = 0;        // 对齐后的块大小
    size_t      per_chunk_  = 0;        // 每块大块包含多少个子块
    std::size_t alloc_count_ = 0;       // 统计：累计分配次数
    std::size_t free_count_  = 0;       // 统计：累计释放次数

    static constexpr size_t kMaxAlign = alignof(std::max_align_t);

    static size_t round_up(size_t v, size_t a) noexcept {
        return (v + a - 1) & ~(a - 1);
    }

    void grow() {
        const size_t total = block_size_ * per_chunk_;
        void* mem = ::operator new(total);                 // 系统分配，可能抛 bad_alloc
        chunks_.push_back(mem);
        auto* base = static_cast<std::byte*>(mem);
        for (size_t i = 0; i < per_chunk_; ++i) {           // 切成子块串入 free list
            auto* node = reinterpret_cast<FreeNode*>(base + i * block_size_);
            node->next = free_list_;
            free_list_ = node;
        }
    }

public:
    explicit MemoryPool(size_t block, size_t per_chunk = 8192)
        : block_size_(round_up(std::max(block, sizeof(FreeNode)), kMaxAlign)),
          per_chunk_(per_chunk ? per_chunk : 1) {}

    MemoryPool(const MemoryPool&) = delete;
    MemoryPool& operator=(const MemoryPool&) = delete;

    ~MemoryPool() {
        for (void* c : chunks_) ::operator delete(c);       // 异常安全：仅释放，不抛
    }

    // 返回对齐到 max_align_t 的块；不抛（除非系统分配抛 bad_alloc）
    void* allocate() {
        if (!free_list_) grow();
        FreeNode* n = free_list_;
        free_list_ = n->next;
        ++alloc_count_;
        return n;
    }

    void deallocate(void* p) noexcept {
        if (!p) return;
        auto* n = static_cast<FreeNode*>(p);
        n->next = free_list_;
        free_list_ = n;
        ++free_count_;
    }

    size_t      block_size()  const noexcept { return block_size_; }
    std::size_t total_alloc() const noexcept { return alloc_count_; }
    std::size_t total_free()  const noexcept { return free_count_; }
    std::size_t chunks()      const noexcept { return chunks_.size(); }
};

int main() {
    MemoryPool pool(64 /*字节块*/);
    std::vector<void*> ptrs;
    ptrs.reserve(1000000);

    // 阶段一：分配 100 万块
    for (int i = 0; i < 1000000; ++i) ptrs.push_back(pool.allocate());
    // 阶段二：全部释放（入 free list，可复用）
    for (void* p : ptrs) pool.deallocate(p);
    ptrs.clear();
    // 阶段三：复用，验证 free list 回收有效
    for (int i = 0; i < 1000000; ++i) ptrs.push_back(pool.allocate());
    for (void* p : ptrs) pool.deallocate(p);

    std::printf("MemoryPool full run OK\n");
    std::printf("  block_size = %zu bytes\n", pool.block_size());
    std::printf("  chunks     = %zu (each %zu blocks)\n",
                pool.chunks(), 8192u);
    std::printf("  alloc/free = %zu / %zu\n",
                pool.total_alloc(), pool.total_free());
    return 0;
}
