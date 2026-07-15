// Phase 5 批 A·ASM-108-memory_order：内存序在 x86-64 下的真实指令屏障
// 编译: g++ -std=c++26 -O2 -c ch108_memory_order_test.cpp -o ch108_memory_order_test.o
// 反汇编: objdump -d -M intel -C ch108_memory_order_test.o
#include <atomic>

std::atomic<int> g{0};

[[gnu::noinline]] void store_relaxed() { g.store(1, std::memory_order_relaxed); }
[[gnu::noinline]] void store_release() { g.store(1, std::memory_order_release); }
[[gnu::noinline]] void store_seqcst() { g.store(1, std::memory_order_seq_cst); }
[[gnu::noinline]] int  load_acquire()  { return g.load(std::memory_order_acquire); }
[[gnu::noinline]] int  load_seqcst()  { return g.load(std::memory_order_seq_cst); }
[[gnu::noinline]] int  fadd_relaxed() { return g.fetch_add(1, std::memory_order_relaxed); }
[[gnu::noinline]] int  fadd_seqcst() { return g.fetch_add(1, std::memory_order_seq_cst); }

int main() {
    store_relaxed(); store_release(); store_seqcst();
    (void)load_acquire(); (void)load_seqcst();
    (void)fadd_relaxed(); (void)fadd_seqcst();
    return 0;
}
