// 文件: Examples/_ch137_proxy.cpp
// Proxy：std::unique_ptr 是最常用的代理——封装所有权并对真实对象转发访问
#include <iostream>
#include <memory>

struct Resource {
    Resource() { std::cout << "Resource()\n"; }
    ~Resource() { std::cout << "~Resource()\n"; }
    void use() const { std::cout << "use\n"; }
};

int main() {
    std::unique_ptr<Resource> p = std::make_unique<Resource>();   // 代理对象
    p->use();                 // 通过代理转发到真实对象
}                            // 离开作用域自动释放（RAII）
