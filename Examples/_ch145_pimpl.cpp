// _ch145_pimpl.cpp —— Pimpl 惯用法 + 间接调用模型（g++ -O2 -S 取证）
#include <memory>
#include <cstdio>

// Pimpl：接口类只持有一个指向实现的指针，实现细节完全隐藏
class Widget {
    struct Impl;                      // 前向声明，impl 类型对调用方不可见
    std::unique_ptr<Impl> impl_;
public:
    Widget();
    ~Widget();
    void draw();                      // 调用方只在头文件看到声明
    int  metric() const;
};

// 间接调用模型：通过函数指针进入实现，等价于 Pimpl 经指针进入 Impl
using draw_fn = void(*)(int);
void draw_impl(int n) { std::printf("%d\n", n); }

void use_indirect(draw_fn f, int n) { f(n); }   // 间接调用 f（call rax）
void use_direct(int n)            { draw_impl(n); }  // 直接调用（可内联）

int main() {
    Widget w;
    w.draw();
    use_indirect(&draw_impl, 7);
    use_direct(7);
    return w.metric();
}
