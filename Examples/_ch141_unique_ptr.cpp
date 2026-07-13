// Examples/_ch141_unique_ptr.cpp
// DI 与 std::unique_ptr 所有权：容器拥有依赖生命周期，注入后所有权转移，无共享、无拷贝。
#include <iostream>
#include <memory>

struct ICache { virtual ~ICache() = default; virtual int get() = 0; };
struct MemCache : ICache { int get() override { return 7; } };

class Handler {
    std::unique_ptr<ICache> cache_;    // 独占所有权
public:
    explicit Handler(std::unique_ptr<ICache> c) : cache_(std::move(c)) {}
    int run() const { return cache_->get(); }
};

int main() {
    // ✅ unique_ptr 表达“转移所有权”的注入语义
    Handler h(std::make_unique<MemCache>());
    std::cout << h.run() << "\n";
}
