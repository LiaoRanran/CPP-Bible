// ch117 复制消除 (copy elision) 汇编实证
// 编译: g++ -std=c++23 -O2 -c ch117_elision_test.cpp && objdump -dC ch117_elision_test.o
#include <cstdio>

// 追踪型: 拷贝/移动都留下 puts 痕迹, 便于在汇编里数 call
struct Tracer {
    int v;
    Tracer(int x) : v(x) { }
    Tracer(const Tracer& o) : v(o.v) { puts("copy"); }
    Tracer(Tracer&& o) noexcept : v(o.v) { puts("move"); }
};

// ① 强制复制消除 (C++17): prvalue 直接在返回槽构造, 零 copy/move 调用
Tracer make_prvalue() {
    return Tracer(42);          // 无 puts("copy")/puts("move") —— 直接构造到返回槽
}

// ② NRVO: 具名局部变量返回, 编译器可消除(非强制, GCC -O2 通常实现)
Tracer make_nrvo() {
    Tracer t(7);
    return t;                   // NRVO: 通常也零 move
}

// ③ 移动被删除仍能编译 —— 证明强制消除不经过移动构造
struct NoMove {
    NoMove() = default;
    NoMove(const NoMove&) = delete;
    NoMove(NoMove&&) = delete;
};
NoMove make_nomove() {
    return NoMove{};            // C++17 强制消除: 即便 move 被删也合法
}
