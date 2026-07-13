// ⑩ (const T&) 与 (T&&) 重载：返回值优化（prvalue）改变实参的"值类别"，影响重载决议
#include <cstdio>

struct Wrapper {
    int v;
    Wrapper(int x) : v(x) {}
};

void f(const Wrapper&) { std::printf("bind-to-const-ref\n"); }  // 左值走这条
void f(Wrapper&&)      { std::printf("rvalue/move-overload\n"); }  // prvalue 走这条

Wrapper make_w() { return Wrapper(5); }   // prvalue -> guaranteed copy elision

int main() {
    f(make_w());   // prvalue 直接构造实参，选中 (Wrapper&&) 重载（零拷贝）
    Wrapper w(6);
    f(w);          // 左值 -> 选中 (const Wrapper&) 重载
    return 0;
}
