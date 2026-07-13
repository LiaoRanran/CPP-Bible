// 文件: Examples/_ch137_proxy_lazy.cpp
// Virtual Proxy：延迟加载昂贵资源，仅在首次使用时创建真实对象
#include <iostream>
#include <memory>

struct Image {
    virtual ~Image() = default;
    virtual void show() const = 0;
};

struct RealImage : Image {
    RealImage() { std::cout << "加载大图(昂贵)...\n"; }
    void show() const override { std::cout << "显示图\n"; }
};

struct ProxyImage : Image {
    void show() const override {
        if (!real_) real_ = std::make_unique<RealImage>();   // 首次用时才建
        real_->show();
    }
private:
    mutable std::unique_ptr<RealImage> real_;
};

int main() {
    ProxyImage img;          // 构造很轻
    img.show();              // 此刻才真正加载
    img.show();
}
