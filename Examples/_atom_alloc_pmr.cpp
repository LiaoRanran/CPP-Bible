// Examples/_atom_alloc_pmr.cpp
// 服务 ATOM-MEM-ALLOC-001：std::pmr 多态分配器 + monotonic_buffer_resource。
// 论断：pmr 把"内存策略"变成运行时多态（memory_resource 虚接口）；monotonic_buffer_resource
//       用一块栈上缓冲区伺候所有分配——pmr::vector 全程未触碰上游（零堆分配）；对照组把同一
//       容器接到"计数+委托堆"资源上，扩容路径可见。
// 观测通路说明（本机实测）：MinGW 的 libstdc++ 为动态 DLL，new_delete_resource 内部的 operator
// new 调用不经过 exe 的替换版本（DLL 内符号自绑定）——因此计数必须放在**虚资源层**（我们的
// do_allocate 在 exe 内实例化，虚调用必达），不能用全局 operator new 重载观测 pmr 路径。
// 计数纪律：volatile 计数器 + 拆写复合赋值。
#include <memory_resource>
#include <vector>
#include <iostream>
#include <cstddef>

volatile long g_upstream_calls = 0;   // 上游资源被触碰次数（monotonic 组的"零堆"判据）
volatile long g_res_calls = 0;        // 计数资源自身被容器调用次数
volatile long long g_res_bytes = 0;

struct TrackUpstream : std::pmr::memory_resource {   // monotonic 的上游：被调用即"溢出到堆"
    void* do_allocate(std::size_t bytes, std::size_t align) override {
        g_upstream_calls = g_upstream_calls + 1;
        return std::pmr::new_delete_resource()->allocate(bytes, align);
    }
    void do_deallocate(void* p, std::size_t b, std::size_t a) override {
        std::pmr::new_delete_resource()->deallocate(p, b, a);
    }
    bool do_is_equal(const std::pmr::memory_resource& o) const noexcept override {
        return this == &o;
    }
};

struct CountDelegating : std::pmr::memory_resource {  // 对照组：计数后委托堆（new_delete_resource）
    void* do_allocate(std::size_t bytes, std::size_t align) override {
        g_res_calls = g_res_calls + 1;
        g_res_bytes = g_res_bytes + (long long)bytes;
        return std::pmr::new_delete_resource()->allocate(bytes, align);
    }
    void do_deallocate(void* p, std::size_t b, std::size_t a) override {
        std::pmr::new_delete_resource()->deallocate(p, b, a);
    }
    bool do_is_equal(const std::pmr::memory_resource& o) const noexcept override {
        return this == &o;
    }
};

int main() {
    alignas(16) static char buf[1024];
    TrackUpstream track;

    {
        std::pmr::monotonic_buffer_resource mono(buf, sizeof buf, &track);
        std::pmr::vector<int> v(&mono);
        for (int i = 0; i < 16; ++i) v.push_back(i);   // 全部由栈缓冲伺候
    }                                                  // monotonic 析构：释放（对缓冲是空操作）

    {
        CountDelegating del;
        std::pmr::vector<int> w(&del);                 // 对照：计数层 + 委托堆
        for (int i = 0; i < 16; ++i) w.push_back(i);
    }

    std::cout << "monotonic: upstream_allocs=" << g_upstream_calls
              << " (zero heap: buffer served everything)\n";
    std::cout << "delegating: res_calls=" << g_res_calls << " bytes=" << g_res_bytes
              << " (growth path, heap-backed)\n";
    return 0;
}
