// ASM-117-nrvo : 拷贝省略 vs 未省略 指令数对比（扩展 ASM-117-elision）
// 编译: g++ -std=c++26 -O2 -c ch117_nrvo_test.cpp -o ch117_nrvo_test.o
// 反汇编: objdump -d -M intel -C ch117_nrvo_test.o
#include <cstdio>

struct Tracer {
    int v;
    Tracer(int x) : v(x) {}
    Tracer(const Tracer& o) : v(o.v) { puts("copy"); }            // 若被调用 -> call puts
    Tracer(Tracer&& o) noexcept     : v(o.v) { puts("move"); }    // 若被调用 -> call puts
};

// ① 强制消除（prvalue）：C++17 必须省略，不应出现任何 call puts
[[gnu::noinline]] Tracer make_prvalue() { return Tracer(42); }

// ② NRVO（具名单一返回对象）：GCC -O2 通常消除，零 move
[[gnu::noinline]] Tracer make_nrvo() { Tracer t(7); return t; }

// ③ NRVO 失效：不同返回路径返回不同具名对象 -> 编译器无法合并返回槽 -> 触发 move
[[gnu::noinline]] Tracer make_nrvo_fail(bool b) {
    Tracer a(1);
    Tracer c(2);
    if (b) return a;   // 两条路径返回不同对象
    else    return c;
}
