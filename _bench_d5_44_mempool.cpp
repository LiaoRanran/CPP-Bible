// D5 Wave 3 benchmark: ch44 内存池 — 定长池分配器 vs malloc/free
// 编译: g++ -O2 -std=c++23 -o bench.exe _bench_d5_44_mempool.cpp
// 目的: 量化 手撸 free-list 池(无锁/无系统调用) 相比通用 malloc/free 的吞吐优势.
#include <iostream>
#include <chrono>
#include <vector>
#include <cstdint>
#include <cstdlib>

static volatile long long g_esc = 0;

template <class F>
double bench(const char* name, F f, int rounds = 5) {
    double best = 1e18;
    for (int r = 0; r < rounds; ++r) {
        auto t0 = std::chrono::steady_clock::now();
        long long res = f();
        auto t1 = std::chrono::steady_clock::now();
        g_esc += res;
        double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
        if (ms < best) best = ms;
    }
    std::cout << name << ": " << best << " ms\n";
    return best;
}

struct Node { Node* next; };

struct Pool {
    Node* free_list = nullptr;
    std::vector<void*> blocks;
    Pool(size_t count, size_t obj) {
        blocks.reserve(count);
        for (size_t i = 0; i < count; ++i) {
            void* p = std::malloc(obj > sizeof(Node) ? obj : sizeof(Node));
            blocks.push_back(p);
            Node* n = static_cast<Node*>(p);
            n->next = free_list;
            free_list = n;
        }
    }
    void* alloc() {
        Node* n = free_list;
        if (n) free_list = n->next;
        return n;
    }
    void dealloc(void* p) {
        Node* n = static_cast<Node*>(p);
        n->next = free_list;
        free_list = n;
    }
    ~Pool() { for (void* p : blocks) std::free(p); }
};

int main() {
    const int N = 2'000'000;
    const size_t OBJ = 32;

    bench("malloc_free", [&] {
        int64_t sum = 0;
        std::vector<void*> ptrs;
        ptrs.reserve(N);
        for (int i = 0; i < N; ++i) {
            void* p = std::malloc(OBJ);
            volatile char* vp = static_cast<volatile char*>(p);
            *vp = (char)(i & 0xFF);
            ptrs.push_back(p);
            sum += (int64_t)p;
        }
        for (void* p : ptrs) std::free(p);
        return sum;
    });

    Pool pool(N, OBJ);
    bench("pool_alloc", [&] {
        int64_t sum = 0;
        std::vector<void*> ptrs;
        ptrs.reserve(N);
        for (int i = 0; i < N; ++i) {
            void* p = pool.alloc();
            volatile char* vp = static_cast<volatile char*>(p);
            *vp = (char)(i & 0xFF);
            ptrs.push_back(p);
            sum += (int64_t)p;
        }
        for (void* p : ptrs) pool.dealloc(p);
        return sum;
    });

    std::cout << "esc=" << g_esc << "\n";
    return 0;
}
