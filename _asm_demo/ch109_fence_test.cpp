// ASM-109-fence : GCC 15.3.0 x86-64 下显式内存屏障指令实证
// 编译: g++ -std=c++26 -O2 -c ch109_fence_test.cpp -o ch109_fence_test.o
// 反汇编: objdump.exe -d -M intel -C ch109_fence_test.o
#include <atomic>

// ① 顺序一致全屏障：在 x86-64 通常生成 mfence 或 lock orq $0,(%rsp)（二者等价全屏障）
[[gnu::noinline]] void fence_seqcst() {
    std::atomic_thread_fence(std::memory_order_seq_cst);
}

// ② acquire 屏障：x86-64 TSO 下天然零成本 → 空函数（无 mfence/dmb）
[[gnu::noinline]] void fence_acquire() {
    std::atomic_thread_fence(std::memory_order_acquire);
}

// ③ release 屏障：同上，x86-64 下空
[[gnu::noinline]] void fence_release() {
    std::atomic_thread_fence(std::memory_order_release);
}

// ④ acq_rel 屏障：等价 seq_cst 全屏障（x86 下与 seq_cst fence 同指令）
[[gnu::noinline]] void fence_acq_rel() {
    std::atomic_thread_fence(std::memory_order_acq_rel);
}

// ⑤ 编译器屏障（signal fence）：纯编译期重排阻止，零运行时指令（无 CPU 屏障）
[[gnu::noinline]] void fence_signal() {
    std::atomic_signal_fence(std::memory_order_seq_cst);
}
