// 文件: Examples/_ch137_bridge_ct.cpp
// 编译期桥接：把 Renderer 作为模板实参，分发在编译期完成（无 vptr/堆分配）
#include <iostream>

struct VectorRenderer {
    static void renderCircle(float r) { std::cout << "Vector 圆 r=" << r << '\n'; }
};

struct RasterRenderer {
    static void renderCircle(float r) { std::cout << "Raster 圆 r=" << r << '\n'; }
};

template <typename R>
struct Circle {
    float radius_;
    void draw() const { R::renderCircle(radius_); }   // 静态分发，可被内联
};

int main() {
    Circle<VectorRenderer> c{5.0f};
    c.draw();
}
