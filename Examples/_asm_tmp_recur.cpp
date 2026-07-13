// 展示 TMP 递归在 -O0 下生成 N 个独立函数符号（编译期递归的 ABI 落地）
// 编译：g++ -std=c++23 -O0 -S -masm=intel _asm_tmp_recur.cpp -o _asm_tmp_recur.asm
template <int N>
struct Fib {
    static int compute() { return Fib<N - 1>::compute() + Fib<N - 2>::compute(); }
};
template <>
struct Fib<0> { static int compute() { return 0; } };
template <>
struct Fib<1> { static int compute() { return 1; } };

int use_fib() { return Fib<10>::compute(); }   // 触发 Fib<0>..Fib<10> 共 11 个实例化符号
