// _ch139_interface_check.cpp
// 取证目的：用 static_assert + requires 在编译期强制派生类满足接口契约。
#include <iostream>
#include <concepts>

template <typename D>
struct Drawable {
    void draw() const {
        static_assert(requires(const D d) { d.render(); },
                      "CRTP 派生类必须实现 render()");
        static_cast<const D*>(this)->render();
    }
};

struct Circle : Drawable<Circle> {
    void render() const { std::cout << "render circle\n"; }
};

// struct Bad : Drawable<Bad> {};  // 取消注释 -> 编译失败（缺 render）

int main() { Circle{}.draw(); }
