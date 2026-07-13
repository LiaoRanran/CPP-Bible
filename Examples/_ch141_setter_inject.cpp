// Examples/_ch141_setter_inject.cpp
// setter 注入（Setter Injection）：依赖可在对象构造后替换，适合可选/可热插拔依赖。
#include <iostream>
#include <string>

struct Renderer { virtual ~Renderer() = default; virtual void draw() = 0; };
struct OpenGLRenderer : Renderer { void draw() override { std::cout << "OpenGL\n"; } };
struct VulkanRenderer : Renderer { void draw() override { std::cout << "Vulkan\n"; } };

class Window {
    Renderer* renderer_ = nullptr;     // 允许为空（可选依赖）
public:
    void setRenderer(Renderer* r) { renderer_ = r; }   // ✅ setter 注入
    void render() const { if (renderer_) renderer_->draw(); }
};

int main() {
    Window w;
    OpenGLRenderer gl;
    w.setRenderer(&gl);
    w.render();
    VulkanRenderer vk;
    w.setRenderer(&vk);                // 运行时热替换
    w.render();
}
