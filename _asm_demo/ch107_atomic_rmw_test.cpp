// ASM-107-atomic_rmw : GCC 15.3.0 x86-64 下原子读-修改-写(RMW)指令实证
// 编译: g++ -std=c++26 -O2 -c ch107_atomic_rmw_test.cpp -o ch107_atomic_rmw_test.o
// 反汇编: objdump.exe -d -M intel -C ch107_atomic_rmw_test.o
#include <atomic>
#include <cstdint>

std::atomic<int>     g32{0};
std::atomic<uint64_t> g64{0};

// ① 32 位 fetch_add：relaxed 与 seq_cst 逐字节相同（都付 lock xadd）
[[gnu::noinline]] int fetch_add_relaxed() {
    return g32.fetch_add(1, std::memory_order_relaxed);
}
[[gnu::noinline]] int fetch_add_seqcst() {
    return g32.fetch_add(1, std::memory_order_seq_cst);
}

// ② 64 位 fetch_add：lock xadd 的 64 位形式（rax 版本）
[[gnu::noinline]] uint64_t fetch_add64() {
    return g64.fetch_add(1, std::memory_order_seq_cst);
}

// ③ exchange：无条件写，编译为带 lock 的 xchg
[[gnu::noinline]] int exchange_seqcst() {
    return g32.exchange(99, std::memory_order_seq_cst);
}

// ④ CAS 循环（canonical pattern）：compare_exchange_weak + while 重试
// 非显然事实：x86 上 weak/strong 都生成 lock cmpxchg，编译器不模拟伪失败
[[gnu::noinline]] void cas_inc() {
    int expected = g32.load(std::memory_order_relaxed);
    while (!g32.compare_exchange_weak(expected, expected + 1,
                                      std::memory_order_acq_rel,
                                      std::memory_order_relaxed)) {
        // expected 由 compare_exchange_weak 失败路径自动刷新，重新尝试
    }
}
