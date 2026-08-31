// _bench_unv_mem.cpp — 真实微基准：用于核验 ch41/ch36/ch37/ch44 的性能声明 (GCC 13.1.0 MinGW)
// 复现旗标：g++ -O2 -std=c++20 -Wall -Wextra
#include <iostream>
#include <memory>
#include <vector>
#include <chrono>
#include <cstdlib>
#include <cstdint>
#include <random>

volatile int64_t g_sink = 0;
int* g_esc[4096];   // 强制分配“逃逸”，防止编译器把 new/delete/malloc 优化掉

double ns_per_op(void (*f)(int), int N, int R) {
    double best = 1e18;
    for (int r = 0; r < R; ++r) {
        auto a = std::chrono::steady_clock::now();
        f(N);
        auto b = std::chrono::steady_clock::now();
        double us = std::chrono::duration<double, std::micro>(b - a).count();
        double per = us * 1000.0 / N;          // µs -> ns per op
        if (per < best) best = per;
    }
    return best;
}

// ch41: unique_ptr 解引用（一次额外间接）
void f_unique_deref(int N) {
    auto p = std::make_unique<int>(42);
    for (int i = 0; i < N; ++i) g_sink += *p;
}
// ch41: shared_ptr 拷贝（原子引用计数 inc/dec）
void f_shared_copy(int N) {
    auto p = std::make_shared<int>(42);
    for (int i = 0; i < N; ++i) { std::shared_ptr<int> q = p; g_sink += q.use_count(); }
}
// ch41: make_shared（一次 operator new 分配对象+控制块）
void f_make_shared(int N) {
    for (int i = 0; i < N; ++i) { auto p = std::make_shared<int>(i); g_sink += *p; }
}
// ch41: shared_ptr(new T)（两次 operator new）
void f_shared_new(int N) {
    for (int i = 0; i < N; ++i) { std::shared_ptr<int> p(new int(i)); g_sink += *p; }
}
// ch37/ch36: raw new/delete（指针逃逸到 g_esc，阻止分配被优化消除）
void f_raw_newdel(int N) {
    for (int i = 0; i < N; ++i) { int* p = new int(i); g_esc[i & 4095] = p; g_sink += *p; delete p; }
}
// ch37: malloc/free（同上，强制真实分配）
void f_malloc_free(int N) {
    for (int i = 0; i < N; ++i) { int* p = (int*)std::malloc(sizeof(int)); *p = i; g_esc[i & 4095] = p; g_sink += *p; std::free(p); }
}
// ch36: 栈上局部变量（应被优化为寄存器运算）
void f_stack_local(int N) {
    for (int i = 0; i < N; ++i) { int x = i; g_sink += x; }
}

// ch44: 极简内存池 vs 默认 new/delete（固定大小块）
struct Pool {
    static const int CAP = 1 << 16;
    int buf[CAP];
    int free_list[CAP];
    int head = 0;
    Pool() { for (int i = 0; i < CAP; ++i) free_list[i] = i; }
    int* alloc() { return &buf[free_list[head++]]; }
    void free(int* p) { free_list[--head] = (int)(p - buf); }
};
void f_pool(int N) {
    static Pool pool;  // 仅构造一次；alloc/free 本身不走系统分配
    for (int i = 0; i < N; ++i) { int* p = pool.alloc(); *p = i; g_sink += *p; pool.free(p); }
}

int main() {
    const int N = 30'000'000, R = 15;
    std::cout << "unique_deref : " << ns_per_op(f_unique_deref, N, R) << " ns/op\n";
    std::cout << "shared_copy  : " << ns_per_op(f_shared_copy,  N, R) << " ns/op\n";
    std::cout << "make_shared  : " << ns_per_op(f_make_shared,  N, R) << " ns/op\n";
    std::cout << "shared_new   : " << ns_per_op(f_shared_new,   N, R) << " ns/op\n";
    std::cout << "raw_newdel   : " << ns_per_op(f_raw_newdel,   N, R) << " ns/op\n";
    std::cout << "malloc_free  : " << ns_per_op(f_malloc_free,  N, R) << " ns/op\n";
    std::cout << "stack_local  : " << ns_per_op(f_stack_local,  N, R) << " ns/op\n";
    std::cout << "pool_alloc   : " << ns_per_op(f_pool,         N, R) << " ns/op\n";
    return 0;
}
