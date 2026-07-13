// 文件：Examples/_ch160_benchmark.cpp
// 行号：1
// 真实基准：自实现固定块池 vs std::malloc，使用 std::chrono 计时（本机 g++ -O2）
#include <cstddef>
#include <cstdint>
#include <vector>
#include <new>
#include <cstdlib>
#include <cstdio>
#include <chrono>

class FixedPool {
    struct FreeNode { FreeNode* next; };
    FreeNode* free_list_ = nullptr;
    std::vector<void*> chunks_;
    size_t block_size_;
    size_t per_chunk_;
    static constexpr size_t kAlign = alignof(std::max_align_t);
    void grow() {
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
    explicit FixedPool(size_t block, size_t per_chunk = 8192)
        : block_size_((std::max(block, sizeof(FreeNode)) + kAlign - 1) & ~(kAlign - 1)),
          per_chunk_(per_chunk) {}
    ~FixedPool() { for (void* c : chunks_) ::operator delete(c); }
    void* allocate() {
        if (!free_list_) grow();
        FreeNode* n = free_list_; free_list_ = n->next; return n;
    }
    void deallocate(void* p) noexcept {
        auto* n = static_cast<FreeNode*>(p);
        n->next = free_list_; free_list_ = n;
    }
};

static double bench_pool(size_t n, size_t blk) {
    FixedPool pool(blk);
    std::vector<void*> v; v.reserve(n);
    auto t0 = std::chrono::high_resolution_clock::now();
    for (size_t i = 0; i < n; ++i) v.push_back(pool.allocate());
    for (void* p : v) pool.deallocate(p);
    v.clear();
    auto t1 = std::chrono::high_resolution_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}

static double bench_malloc(size_t n, size_t blk) {
    std::vector<void*> v; v.reserve(n);
    auto t0 = std::chrono::high_resolution_clock::now();
    for (size_t i = 0; i < n; ++i) v.push_back(std::malloc(blk));
    for (void* p : v) std::free(p);
    v.clear();
    auto t1 = std::chrono::high_resolution_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}

int main() {
    const size_t N = 2'000'000;
    const size_t BLK = 64;
    // 预热
    bench_pool(1000, BLK); bench_malloc(1000, BLK);
    double pool_t = bench_pool(N, BLK);
    double malc_t = bench_malloc(N, BLK);
    std::printf("N=%zu BLK=%zu\n", N, BLK);
    std::printf("FixedPool : %.3f ms\n", pool_t);
    std::printf("std::malloc: %.3f ms\n", malc_t);
    std::printf("speedup   : %.2fx\n", malc_t / pool_t);
    return 0;
}
