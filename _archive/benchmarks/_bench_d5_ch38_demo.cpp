#include <iostream>
#include <memory_resource>
#include <vector>
#include <list>
#include <array>
#include <cassert>
#include <cstddef>
#include <cstdint>

// 统计上游 new/delete 次数的 memory_resource，用来证明 PMR 到底有没有碰堆
class CountingResource : public std::pmr::memory_resource {
public:
    long long allocs = 0;
    long long deallocs = 0;
private:
    void* do_allocate(std::size_t bytes, std::size_t align) override {
        ++allocs;
        return std::pmr::new_delete_resource()->allocate(bytes, align);
    }
    void do_deallocate(void* p, std::size_t bytes, std::size_t align) override {
        ++deallocs;
        std::pmr::new_delete_resource()->deallocate(p, bytes, align);
    }
    bool do_is_equal(const std::pmr::memory_resource& o) const noexcept override {
        return this == &o;
    }
};

int main() {
    constexpr int N = 1000;

    // ---- 1) monotonic_buffer_resource 挂在栈上数组，上游一次都不用碰 ----
    std::array<std::byte, 64 * 1024> arena{};
    CountingResource upstream;
    {
        std::pmr::monotonic_buffer_resource mbr(arena.data(), arena.size(), &upstream);
        std::pmr::vector<int> v(&mbr);
        v.reserve(N);
        for (int i = 0; i < N; ++i) v.push_back(i);

        // 元素确实落在栈上 arena 内部
        const std::byte* lo = arena.data();
        const std::byte* hi = lo + arena.size();
        const std::byte* elem = reinterpret_cast<const std::byte*>(v.data());
        bool inside = (elem >= lo && elem < hi);

        std::cout << "vector elems inside arena? : " << (inside ? "yes" : "no") << std::endl;
        std::cout << "upstream allocs (mono)     : " << upstream.allocs << std::endl;
        std::cout << "vector resource == &mbr?   : "
                  << (v.get_allocator().resource() == &mbr ? "yes" : "no") << std::endl;

        assert(inside);                                    // 内存来自预置缓冲区
        assert(upstream.allocs == 0);                      // 完全没有回落到堆
        assert(v.get_allocator().resource() == &mbr);      // 分配器携带资源指针
        assert(v.size() == static_cast<std::size_t>(N));
        assert(v[N / 2] == N / 2);                         // 数据正确性
    }
    // monotonic 只在析构时统一归还，逐个 deallocate 是 no-op
    std::cout << "upstream deallocs (mono)   : " << upstream.deallocs << std::endl;

    // ---- 2) 节点容器：默认逐节点一次分配，pool 则批发拿货 ----
    CountingResource direct;
    {
        std::pmr::list<int> l(&direct);
        for (int i = 0; i < N; ++i) l.push_back(i);
    }
    long long per_node = direct.allocs;

    CountingResource pooled;
    {
        std::pmr::unsynchronized_pool_resource pool(&pooled);
        std::pmr::list<int> l(&pool);
        for (int i = 0; i < N; ++i) l.push_back(i);
    }
    long long via_pool = pooled.allocs;

    std::cout << "list upstream allocs direct: " << per_node << std::endl;
    std::cout << "list upstream allocs pooled: " << via_pool << std::endl;

    assert(per_node >= N);        // 逐节点分配：至少 N 次上游请求
    assert(via_pool < per_node);  // 稳定语义：池化后上游请求次数显著变少

    // ---- 3) 分配器相等语义：PMR 靠资源指针判等，与静态类型无关 ----
    std::pmr::monotonic_buffer_resource m1, m2;
    std::pmr::polymorphic_allocator<int> a1(&m1), a2(&m1), a3(&m2);
    std::cout << "a1 == a2 (same resource)?  : " << (a1 == a2 ? "yes" : "no") << std::endl;
    std::cout << "a1 == a3 (diff resource)?  : " << (a1 == a3 ? "yes" : "no") << std::endl;
    assert(a1 == a2);
    assert(!(a1 == a3));

    std::cout << "all assertions passed" << std::endl;
    return 0;
}