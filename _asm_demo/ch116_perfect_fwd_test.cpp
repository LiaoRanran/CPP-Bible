// ASM-116-perfect_fwd : std::forward 引用折叠零开销实证
// 编译: g++ -std=c++26 -O2 -c ch116_perfect_fwd_test.cpp -o ch116_perfect_fwd_test.o
// 反汇编: objdump -d -M intel -C ch116_perfect_fwd_test.o
#include <utility>

struct S { int a; double b; };

// 全局副作用，强制 sink 不被优化消除（否则整条转发链被 O2 抹平）
int g_l = 0, g_r = 0;

// 重载接收端：左值 / 右值各一个
[[gnu::noinline]] void sink_l(S&)  { g_l = 1; }
[[gnu::noinline]] void sink_r(S&&) { g_r = 1; }

// (1) 手写左值转发：参数已是 S&，直接调用 sink_l
[[gnu::noinline]] void fwd_lvalue(S& s) { sink_l(s); }

// (2) 手写右值转发：move 后调用 sink_r
[[gnu::noinline]] void fwd_rvalue(S&& s) { sink_r(std::move(s)); }

// (3) 完美转发模板：引用折叠使 std::forward<T> 编译为对应重载调用
//     T&  && -> T&  (左值实例化调 sink_l)
//     T&& && -> T&& (右值实例化调 sink_r)
//     forward 自身不生成额外指令，仅是寄存器/内存位置按原类型传递
template <class T>
[[gnu::noinline]] void fwd_tmpl(T&& s) {
    if constexpr (std::is_lvalue_reference_v<T>) {
        sink_l(s);
    } else {
        sink_r(std::move(s));
    }
}
template void fwd_tmpl<S&>(S&);   // 左值实例化
template void fwd_tmpl<S>(S&&);   // 右值实例化

// (4) 反例：按值传递 —— 触发一次移动/拷贝构造（相对完美转发的额外开销）
[[gnu::noinline]] void fwd_val(S s) { sink_r(std::move(s)); }
