// 文件：Examples/_ch160_allocator.cpp
// 行号：1
// 与 std::allocator 对接：自定义 Allocator 让 STL 容器使用内存池
#include <cstddef>
#include <cstdio>
#include <vector>
#include <new>
#include <memory>

class FixedPool {
    struct FreeNode { FreeNode* next; };
    FreeNode* free_list_ = nullptr;
    std::vector<void*> chunks_;
    size_t block_size_;
    size_t per_chunk_;
    static constexpr size_t kAlign = alignof(std::max_align_t);
    void grow() {
        void* mem = ::operator new(block_size_ * per_chunk_);
        chunks_.push_back(mem);
        auto* base = static_cast<std::byte*>(mem);
        for (size_t i = 0; i < per_chunk_; ++i) {
            auto* node = reinterpret_cast<FreeNode*>(base + i * block_size_);
            node->next = free_list_; free_list_ = node;
        }
    }
public:
    explicit FixedPool(size_t block, size_t per_chunk = 4096)
        : block_size_((std::max(block, sizeof(FreeNode)) + kAlign - 1) & ~(kAlign - 1)),
          per_chunk_(per_chunk) {}
    ~FixedPool() { for (void* c : chunks_) ::operator delete(c); }
    void* allocate() { if (!free_list_) grow(); FreeNode* n = free_list_; free_list_ = n->next; return n; }
    void deallocate(void* p) { auto* n = static_cast<FreeNode*>(p); n->next = free_list_; free_list_ = n; }
    size_t block_size() const { return block_size_; }
};

template <class T>
struct PoolAllocator {
    FixedPool* pool_;
    using value_type = T;
    explicit PoolAllocator(FixedPool& p) noexcept : pool_(&p) {}
    template <class U> PoolAllocator(const PoolAllocator<U>& o) noexcept : pool_(o.pool_) {}
    T* allocate(std::size_t n) {
        // 仅当请求恰好等于块大小（单元素）才走池；数组/超大请求回退系统分配
        size_t need = n * sizeof(T);
        if (n == 1 && need <= pool_->block_size())
            return static_cast<T*>(pool_->allocate());
        return static_cast<T*>(::operator new(need));
    }
    void deallocate(T* p, std::size_t n) noexcept {
        if (n != 1 || sizeof(T) > pool_->block_size()) { ::operator delete(p); return; }
        pool_->deallocate(p);
    }
    template <class U> bool operator==(const PoolAllocator<U>& o) const noexcept { return pool_ == o.pool_; }
    template <class U> bool operator!=(const PoolAllocator<U>& o) const noexcept { return pool_ != o.pool_; }
};

int main() {
    FixedPool pool(sizeof(int));
    std::vector<int, PoolAllocator<int>> v{PoolAllocator<int>(pool)};
    for (int i = 0; i < 100000; ++i) v.push_back(i);
    std::printf("PoolAllocator vector size=%zu front=%d back=%d\n",
                v.size(), v.front(), v.back());
    return 0;
}
