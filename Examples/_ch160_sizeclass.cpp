// 文件：Examples/_ch160_sizeclass.cpp
// 行号：1
// 多级池（size class）：按请求大小映射到固定档位，平衡碎片与内部碎片
#include <cstddef>
#include <cstdio>
#include <array>
#include <vector>
#include <new>

class SizeClassPool {
    struct FreeNode { FreeNode* next; };
    static constexpr size_t kClasses[4] = {32, 64, 128, 256};
    static constexpr size_t kPerChunk = 4096;

    std::array<FreeNode*, 4> heads_{};
    std::vector<void*> chunks_;

    static int classify(size_t n) {
        for (int i = 0; i < 4; ++i)
            if (n <= kClasses[i]) return i;
        return -1; // 太大，回退到 ::operator new
    }
    void grow(int c) {
        size_t bs = kClasses[c];
        void* mem = ::operator new(bs * kPerChunk);
        chunks_.push_back(mem);
        auto* base = static_cast<std::byte*>(mem);
        for (size_t i = 0; i < kPerChunk; ++i) {
            auto* node = reinterpret_cast<FreeNode*>(base + i * bs);
            node->next = heads_[c];
            heads_[c] = node;
        }
    }
public:
    ~SizeClassPool() { for (void* c : chunks_) ::operator delete(c); }
    void* allocate(size_t n) {
        int c = classify(n);
        if (c < 0) return ::operator new(n); // [实现] 超大块直接走系统分配
        if (!heads_[c]) grow(c);
        FreeNode* node = heads_[c];
        heads_[c] = node->next;
        return node;
    }
    void deallocate(void* p, size_t n) {
        int c = classify(n);
        if (c < 0) { ::operator delete(p); return; }
        auto* node = static_cast<FreeNode*>(p);
        node->next = heads_[c];
        heads_[c] = node;
    }
};

int main() {
    SizeClassPool pool;
    void* a = pool.allocate(10);   // -> 32 档
    void* b = pool.allocate(70);   // -> 128 档
    void* c = pool.allocate(5000); // -> 回退 malloc
    std::printf("a=%p b=%p c=%p\n", a, b, c);
    pool.deallocate(a, 10);
    pool.deallocate(b, 70);
    pool.deallocate(c, 5000);
    std::printf("SizeClassPool OK\n");
    return 0;
}
