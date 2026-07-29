// _ch108_d5_store.cpp — ch108 D5 反汇编实证源：三种 memory_order 的 store 循环
// 编译: g++ -O2 -std=c++17 -c _ch108_d5_store.cpp -o _ch108_d5_store.o
// 反汇编: objdump -d -M intel -C _ch108_d5_store.o > _ch108_d5_store.asm
#include <atomic>

std::atomic<long long> g{0};

void store_relaxed(long long n) {
    for (long long i = 0; i < n; ++i) g.store(i, std::memory_order_relaxed);
}
void store_release(long long n) {
    for (long long i = 0; i < n; ++i) g.store(i, std::memory_order_release);
}
void store_seqcst(long long n) {
    for (long long i = 0; i < n; ++i) g.store(i, std::memory_order_seq_cst);
}
long long fetch_add_relaxed(long long n) {
    long long s = 0;
    for (long long i = 0; i < n; ++i) s += g.fetch_add(1, std::memory_order_relaxed);
    return s;
}
long long fetch_add_seqcst(long long n) {
    long long s = 0;
    for (long long i = 0; i < n; ++i) s += g.fetch_add(1, std::memory_order_seq_cst);
    return s;
}
