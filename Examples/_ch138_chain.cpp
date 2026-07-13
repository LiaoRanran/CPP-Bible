// _ch138_chain.cpp
// 第138章 ⑫：责任链——请求沿处理器链传递，直到被处理
#include <iostream>
#include <memory>

struct Handler {
    std::unique_ptr<Handler> next;
    virtual ~Handler() = default;
    virtual bool handle(int level) = 0;
    bool pass(int level) { return next && next->handle(level); }
};

struct Low : Handler  { bool handle(int l) override { return l <= 1 ? (std::cout << "low\n", true)  : pass(l); } };
struct High : Handler { bool handle(int l) override { return l <= 9 ? (std::cout << "high\n", true) : pass(l); } };

int main() {
    auto h = std::make_unique<Low>();
    h->next = std::make_unique<High>();
    h->handle(0); h->handle(5); h->handle(99);
    return 0;
}
