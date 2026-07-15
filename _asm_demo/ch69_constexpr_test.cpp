// ASM-69-constexpr : GCC 15.3.0 x86-64 下 constexpr 编译期求值的"运行时零痕迹"实证
// 编译: g++ -std=c++26 -O2 -c ch69_constexpr_test.cpp -o ch69_constexpr_test.o
// 反汇编: objdump.exe -d -M intel -C ch69_constexpr_test.o
#include <cstdint>

constexpr int fib_cx(int n) {
    return n <= 1 ? n : fib_cx(n - 1) + fib_cx(n - 2);
}
int fib_rt(int n) {
    return n <= 1 ? n : fib_rt(n - 1) + fib_rt(n - 2);
}

// ① constexpr 配【编译期常量】参数 → 递归在编译期全消，运行时仅一条 mov
[[gnu::noinline]] int use_constexpr() {
    return fib_cx(20);          // 6765 = 0x1A6D，编译期折叠为常数
}

// ② 非 constexpr 双生函数 → 运行时真实递归调用
[[gnu::noinline]] int use_runtime() {
    return fib_rt(20);
}

// ③ constexpr 配【运行时变量】参数 → 退化为真实递归（证明 constexpr ≠ 永远零成本）
[[gnu::noinline]] int use_constexpr_runtime_arg(int k) {
    return fib_cx(k);           // k 非编译期常量，必须在运行时求值
}
