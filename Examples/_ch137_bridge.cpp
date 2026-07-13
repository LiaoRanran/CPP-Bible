// 文件: Examples/_ch137_bridge.cpp
// Bridge：抽象（Shape）与实现（Renderer）解耦，运行时通过组合选择实现
#include <iostream>
#include <memory>

struct Renderer {
    virtual ~Renderer() = default;
    virtual void renderCircle(float r) const = 0;
};

struct VectorRenderer : Renderer {
    void renderCircle(float r) const override {
        std::cout << "Vector 画圆 r=" << r << '\n';
    }
};

struct RasterRenderer : Renderer {
    void renderCircle(float r) const override {
        std::cout << "Raster 画圆 r=" << r << '\n';
    }
};

struct Shape {
    explicit Shape(std::shared_ptr<Renderer> r) : renderer_(std::move(r)) {}
    virtual ~Shape() = default;
    virtual void draw() const = 0;
protected:
    std::shared_ptr<Renderer> renderer_;
};

struct Circle : Shape {
    Circle(float r, std::shared_ptr<Renderer> rp) : Shape(std::move(rp)), radius_(r) {}
    void draw() const override { renderer_->renderCircle(radius_); }
private:
    float radius_;
};

int main() {
    auto vector = std::make_shared<VectorRenderer>();
    Circle c{5.0f, vector};
    c.draw();
}
