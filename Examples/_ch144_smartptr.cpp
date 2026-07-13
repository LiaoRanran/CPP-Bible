// ch144 ⑨ 智能指针：unique_ptr 表达独占所有权，move 转移所有权
// 编译：g++ -std=c++23 -O2 -S -masm=intel _ch144_smartptr.cpp -o _ch144_smartptr_O2.asm
#include <memory>
#include <utility>

struct Connection {
    int fd;
    explicit Connection(int f) : fd(f) {}
    ~Connection() { /* 关闭 fd */ }
};

std::unique_ptr<Connection> open(int fd) {
    return std::make_unique<Connection>(fd);   // ✅ 工厂返回独占所有权
}

void transfer() {
    auto a = open(3);
    auto b = std::move(a);   // ✅ 所有权从 a 转移到 b，a 置空
    // 离开作用域时 b 析构，Connection 被释放
}
