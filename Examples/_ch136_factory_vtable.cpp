// Examples/_ch136_factory_vtable.cpp
// 抽象工厂通过虚函数分派：观察 -O2 下生成的虚表（_ZTV）与虚调用 thunk。
#include <memory>

struct Widget {
    virtual ~Widget() = default;
    virtual int area() const = 0;
};
struct Button : Widget {
    int area() const override { return 10; }
};
struct Window : Widget {
    int area() const override { return 100; }
};
std::unique_ptr<Widget> make(const char* kind) {
    if (kind[0] == 'B') return std::make_unique<Button>();
    return std::make_unique<Window>();
}
int run() {
    auto w = make("Button");
    return w->area();   // 虚调用
}
