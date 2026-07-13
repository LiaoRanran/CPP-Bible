// 真实汇编证据来源：本书 ch109_fence 的「附录 H：真实汇编证据」
// 目的：用 MinGW GCC 13.1.0 -O2 验证不同 memory_order 在 x86_64 下编译出的真实指令，
//       证明「seq_cst 在 x86 确实编译为 mfence / 而 relaxed 在 TSO 下免费（无屏障）」。
// 编译: g++ -S -O2 -m64 _ch109_fence_perf.cpp -o _ch109_fence_perf.asm
#include <atomic>
#include <cstdint>

// ① relaxed store/load：x86 TSO 下天然有序，编译为普通 mov（无屏障指令）
void relaxed_store(std::atomic<int>& a, int v) {
    a.store(v, std::memory_order_relaxed);
}
int relaxed_load(std::atomic<int>& a) {
    return a.load(std::memory_order_relaxed);
}

// ② seq_cst store：x86 下需保证全局总顺序，编译为带 lock 前缀的 RMW 或 mfence
void seqcst_store(std::atomic<int>& a, int v) {
    a.store(v, std::memory_order_seq_cst);
}

// ③ seq_cst fence：x86 下编译为 mfence（全屏障）
void seqcst_fence() {
    std::atomic_thread_fence(std::memory_order_seq_cst);
}

// ④ acquire fence：x86 TSO 下 load 不会与后续 load/store 重排，编译为空（无 dmb）
void acquire_fence() {
    std::atomic_thread_fence(std::memory_order_acquire);
}

// ⑤ release fence：x86 TSO 下 store 不会与之前 load/store 重排，编译为空（无 dmb）
void release_fence() {
    std::atomic_thread_fence(std::memory_order_release);
}

int main() {
    std::atomic<int> x{0};
    relaxed_store(x, 1);
    (void)relaxed_load(x);
    seqcst_store(x, 2);
    seqcst_fence();
    acquire_fence();
    release_fence();
    return x.load();
}
