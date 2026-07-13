// _ch135_factory.cpp
// 取证目标（第②⑬节）：工厂模式 + 现代 C++ 用 unique_ptr 返回所有权。
#include <cstdio>
#include <memory>

struct Product { virtual ~Product() = default; virtual const char* name() const = 0; };
struct A : Product { const char* name() const override { return "A"; } };
struct B : Product { const char* name() const override { return "B"; } };

std::unique_ptr<Product> make(const char k) {
    if (k == 'A') return std::make_unique<A>();
    return std::make_unique<B>();
}

int main() {
    auto p = make('A');
    std::printf("%s\n", p->name());
}
