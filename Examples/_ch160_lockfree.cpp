// 文件：Examples/_ch160_lockfree.cpp
// 行号：1
// 无锁池：Treiber 栈（std::atomic + CAS）实现无互斥的 free list
#include <cstddef>
#include <cstdio>
#include <vector>
#include <new>
#include <atomic>
#include <thread>

class LockFreePool {
    struct FreeNode { std::atomic<FreeNode*> next; };
    std::atomic<FreeNode*> head_{nullptr};
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
            FreeNode* expected = head_.load(std::memory_order_relaxed);
            do { node->next.store(expected, std::memory_order_relaxed); }
            while (!head_.compare_exchange_weak(expected, node,
                                                std::memory_order_release,
                                                std::memory_order_relaxed));
        }
    }
public:
    explicit LockFreePool(size_t block, size_t per_chunk = 4096)
        : block_size_((std::max(block, sizeof(FreeNode)) + kAlign - 1) & ~(kAlign - 1)),
          per_chunk_(per_chunk) {}
    ~LockFreePool() { for (void* c : chunks_) ::operator delete(c); }
    void* allocate() {
        FreeNode* old = head_.load(std::memory_order_relaxed);
        do {
            if (!old) { grow(); old = head_.load(std::memory_order_relaxed); }
        } while (old && !head_.compare_exchange_weak(old, old->next.load(std::memory_order_relaxed),
                                                     std::memory_order_acquire,
                                                     std::memory_order_relaxed));
        return old;
    }
    void deallocate(void* p) {
        auto* node = static_cast<FreeNode*>(p);
        FreeNode* expected = head_.load(std::memory_order_relaxed);
        do { node->next.store(expected, std::memory_order_relaxed); }
        while (!head_.compare_exchange_weak(expected, node,
                                            std::memory_order_release,
                                            std::memory_order_relaxed));
    }
};

int main() {
    LockFreePool pool(sizeof(double));
    std::vector<std::thread> ts;
    for (int t = 0; t < 4; ++t) {
        ts.emplace_back([&pool] {
            std::vector<void*> v;
            for (int i = 0; i < 200000; ++i) v.push_back(pool.allocate());
            for (void* p : v) pool.deallocate(p);
        });
    }
    for (auto& th : ts) th.join();
    std::printf("LockFreePool OK (4 threads x 200k)\n");
    return 0;
}
