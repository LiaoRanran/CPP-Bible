// 文件：Examples/_ch160_threadsafe.cpp
// 行号：1
// 线程安全池：用 std::mutex 保护 free list（简单、正确、但存在锁竞争）
#include <cstddef>
#include <cstdio>
#include <vector>
#include <new>
#include <mutex>
#include <thread>

class ThreadSafePool {
    struct FreeNode { FreeNode* next; };
    FreeNode* free_list_ = nullptr;
    std::vector<void*> chunks_;
    size_t block_size_;
    size_t per_chunk_;
    std::mutex mtx_;
    static constexpr size_t kAlign = alignof(std::max_align_t);
    void grow() {
        void* mem = ::operator new(block_size_ * per_chunk_);
        chunks_.push_back(mem);
        auto* base = static_cast<std::byte*>(mem);
        for (size_t i = 0; i < per_chunk_; ++i) {
            auto* node = reinterpret_cast<FreeNode*>(base + i * block_size_);
            node->next = free_list_;
            free_list_ = node;
        }
    }
public:
    explicit ThreadSafePool(size_t block, size_t per_chunk = 4096)
        : block_size_((std::max(block, sizeof(FreeNode)) + kAlign - 1) & ~(kAlign - 1)),
          per_chunk_(per_chunk) {}
    ~ThreadSafePool() { for (void* c : chunks_) ::operator delete(c); }
    void* allocate() {
        std::lock_guard<std::mutex> lk(mtx_);
        if (!free_list_) grow();
        FreeNode* n = free_list_; free_list_ = n->next; return n;
    }
    void deallocate(void* p) {
        std::lock_guard<std::mutex> lk(mtx_);
        auto* n = static_cast<FreeNode*>(p);
        n->next = free_list_; free_list_ = n;
    }
};

int main() {
    ThreadSafePool pool(sizeof(long long));
    std::vector<std::thread> ts;
    for (int t = 0; t < 4; ++t) {
        ts.emplace_back([&pool] {
            std::vector<void*> v;
            for (int i = 0; i < 200000; ++i) v.push_back(pool.allocate());
            for (void* p : v) pool.deallocate(p);
        });
    }
    for (auto& th : ts) th.join();
    std::printf("ThreadSafePool OK (4 threads x 200k)\n");
    return 0;
}
