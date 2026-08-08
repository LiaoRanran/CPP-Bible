// Wave8 D5 bench: 固定大小内存池 vs 默认 ::operator new/delete 分配吞吐
// 编译: g++ -O2 -std=c++23 _bench_d5_ch160_mempool.cpp -o _bench_d5_ch160_mempool.exe
// 运行: ./_bench_d5_ch160_mempool.exe  (输出毫秒, 不断言时间/倍数)
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <chrono>
#include <vector>
#include <new>

static std::uint64_t g_sink = 0;

struct Pool {
    static constexpr std::size_t BLOCK = 64;
    struct Node { Node* next; };
    Node* free_list = nullptr;
    std::vector<char*> pages;
    ~Pool() { for (char* p : pages) std::free(p); }
    void* alloc() {
        if (!free_list) {
            char* page = static_cast<char*>(std::malloc(BLOCK * 4096));
            pages.push_back(page);
            for (std::size_t i = 0; i + BLOCK <= BLOCK * 4096; i += BLOCK) {
                Node* n = reinterpret_cast<Node*>(page + i);
                n->next = free_list; free_list = n;
            }
        }
        Node* n = free_list; free_list = n->next; return n;
    }
    void dealloc(void* p) { Node* n = static_cast<Node*>(p); n->next = free_list; free_list = n; }
};

int main() {
    constexpr int N = 500'000;
    std::vector<void*> ptrs(N, nullptr);

    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) ptrs[i] = ::operator new(32);
    auto t1 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) ::operator delete(ptrs[i]);
    auto t2 = std::chrono::steady_clock::now();
    double ms_new = std::chrono::duration<double, std::milli>(t1 - t0).count()
                  + std::chrono::duration<double, std::milli>(t2 - t1).count();
    std::printf("new_delete %.3f ms\n", ms_new);

    Pool pool;
    auto t3 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) ptrs[i] = pool.alloc();
    auto t4 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) pool.dealloc(ptrs[i]);
    auto t5 = std::chrono::steady_clock::now();
    double ms_pool = std::chrono::duration<double, std::milli>(t4 - t3).count()
                   + std::chrono::duration<double, std::milli>(t5 - t4).count();
    std::printf("mempool %.3f ms\n", ms_pool);

    for (int i = 0; i < N; ++i) g_sink += reinterpret_cast<std::uint64_t>(ptrs[i]) & 1u;
    std::printf("ratio_new/pool=%.2f total=%.3f g_sink=%llu\n",
                ms_new / ms_pool, ms_new + ms_pool,
                static_cast<unsigned long long>(g_sink));
    return 0;
}
