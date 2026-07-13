// 文件: Examples/_ch137_bridge_rt.cpp
// 运行期桥接：依据配置在运行时选择实现，抽象与实现两维独立变化
#include <iostream>
#include <memory>

struct Renderer { virtual ~Renderer() = default; virtual void draw() const = 0; };
struct Vector : Renderer { void draw() const override { std::cout << "Vector\n"; } };
struct Raster : Renderer { void draw() const override { std::cout << "Raster\n"; } };

std::shared_ptr<Renderer> make(bool useVector) {
    return useVector ? std::shared_ptr<Renderer>(std::make_shared<Vector>())
                      : std::shared_ptr<Renderer>(std::make_shared<Raster>());
}

int main() {
    auto r = make(true);   // 运行期才决定具体实现
    r->draw();
}
