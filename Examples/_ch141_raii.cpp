// Examples/_ch141_raii.cpp
// DI 生命周期管理（RAII）：依赖资源由拥有者（容器/unique_ptr）在析构时自动释放。
#include <iostream>
#include <memory>

struct Connection { ~Connection() { std::cout << "close\n"; } void query() { std::cout << "query\n"; } };

class Repository {
    std::unique_ptr<Connection> conn_;  // 拥有连接，析构即关闭（RAII）
public:
    explicit Repository(std::unique_ptr<Connection> c) : conn_(std::move(c)) {}
    void use() { conn_->query(); }
};

int main() {
    Repository repo(std::make_unique<Connection>());
    repo.use();                        // 离开作用域自动 close（无需手动 dispose）
}
