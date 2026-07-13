// 文件：Examples/_ch160_stl.cpp
// 行号：1
// 与 STL 容器结合 + tcmalloc/jemalloc 上游参考说明（非本机依赖，仅接口对照）
#include <cstddef>
#include <cstdio>
#include <unordered_map>
#include <string>
#include <new>
#include <vector>

// 单线程高性能池（与 allocator 章节同理，内联实现便于独立编译）
class Pool {
    struct FN { FN* next; };
    FN* head_ = nullptr;
    std::vector<void*> chunks_;
    size_t bs_;
    void grow() {
        void* m = ::operator new(bs_ * 4096);
        chunks_.push_back(m);
        auto* b = static_cast<std::byte*>(m);
        for (size_t i = 0; i < 4096; ++i) {
            auto* n = reinterpret_cast<FN*>(b + i * bs_);
            n->next = head_; head_ = n;
        }
    }
public:
    explicit Pool(size_t bs) : bs_((std::max(bs, sizeof(FN)) + 15) & ~size_t(15)) {}
    ~Pool() { for (void* c : chunks_) ::operator delete(c); }
    void* alloc() { if (!head_) grow(); FN* n = head_; head_ = n->next; return n; }
    void free(void* p) { auto* n = static_cast<FN*>(p); n->next = head_; head_ = n; }
    size_t block_size() const { return bs_; }
};

template <class T>
struct PAlloc {
    Pool* pool_;
    using value_type = T;
    explicit PAlloc(Pool& p) noexcept : pool_(&p) {}
    template <class U> PAlloc(const PAlloc<U>& o) noexcept : pool_(o.pool_) {}
    T* allocate(std::size_t n) {
        // 仅当请求恰好等于块大小（单节点）才走池；数组/超大节点回退系统分配
        size_t need = n * sizeof(T);
        if (n == 1 && need <= pool_->block_size())
            return static_cast<T*>(pool_->alloc());
        return static_cast<T*>(::operator new(need));
    }
    void deallocate(T* p, std::size_t n) noexcept {
        if (n != 1) { ::operator delete(p); return; }
        pool_->free(p);
    }
    template <class U> bool operator==(const PAlloc<U>& o) const noexcept { return pool_ == o.pool_; }
    template <class U> bool operator!=(const PAlloc<U>& o) const noexcept { return pool_ != o.pool_; }
};

int main() {
    Pool pool(sizeof(std::pair<const std::string, int>));
    std::unordered_map<std::string, int, std::hash<std::string>,
                       std::equal_to<>, PAlloc<std::pair<const std::string, int>>>
        m{PAlloc<std::pair<const std::string, int>>(pool)};
    for (int i = 0; i < 10000; ++i)
        m[std::to_string(i)] = i;
    std::printf("pool-backed unordered_map size=%zu\n", m.size());
    return 0;
}
