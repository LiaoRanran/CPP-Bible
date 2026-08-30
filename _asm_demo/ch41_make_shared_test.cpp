// P1-GAP-1: make_shared 单次分配 vs shared_ptr(new) 两次分配
// 揭示的底层事实：
//   - make_shared<T>(...) 把对象与控制块分配在同一块连续内存（单次 operator new），
//     分配大小 = sizeof(T) + 控制块大小；
//   - shared_ptr<T>(new T) 分两次分配：一次 new T（对象），一次内部 new 控制块。
// 验证方式：objdump 对比两函数中 operator new 的调用次数与分配字节数立即数。
#include <memory>

struct Widget {
    int a, b, c;
    explicit Widget(int x) : a(x), b(x + 1), c(x + 2) {}
};

std::shared_ptr<Widget> via_make_shared(int x) {
    return std::make_shared<Widget>(x);
}

std::shared_ptr<Widget> via_new(int x) {
    return std::shared_ptr<Widget>(new Widget(x));
}