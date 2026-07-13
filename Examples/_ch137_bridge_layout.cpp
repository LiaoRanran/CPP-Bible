// 文件: Examples/_ch137_bridge_layout.cpp
// Bridge 内存布局取证：Shape 持有一个指向 Renderer 的指针（双指针间接）
#include <memory>

struct Renderer {
    virtual ~Renderer() = default;
    virtual void render() const = 0;
};

struct VectorRenderer : Renderer {
    void render() const override {}
};

struct Shape {
    explicit Shape(std::shared_ptr<Renderer> r) : r_(std::move(r)) {}
    void draw() const { r_->render(); }          // 一次指针间接 + 一次虚调用
private:
    std::shared_ptr<Renderer> r_;                 // 控制块指针 + 目标 vptr
};

int main() {
    auto r = std::make_shared<VectorRenderer>();
    Shape s{r};
    s.draw();
}
