// ⑬ constexpr 上下文中的拷贝消除：常量求值阶段不调用可观察拷贝
#include <cstdio>

struct Lit {
    int v;
    constexpr Lit(int x) : v(x) {}
    constexpr Lit(const Lit& o) : v(o.v) {}   // 即使有拷贝，constexpr 求值可省略
};

constexpr Lit make_lit() {
    Lit a(99);
    return a;                  // guaranteed copy elision（prvalue）
}

constexpr int probe() {
    Lit x = make_lit();        // 编译期构造，不发生运行期拷贝
    return x.v;
}

int main() {
    static_assert(probe() == 99);
    std::printf("v=%d\n", probe());
    return 0;
}
