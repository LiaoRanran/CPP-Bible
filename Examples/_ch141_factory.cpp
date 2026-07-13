// Examples/_ch141_factory.cpp
// 工厂注入：当依赖的创建需要参数/配置时，注入工厂而非具体实例（惰性构建）。
#include <iostream>
#include <memory>

struct Connection { int id; Connection(int i):id(i){} };
class ConnectionFactory {
    int seq_ = 0;
public:
    std::unique_ptr<Connection> make() { return std::make_unique<Connection>(++seq_); }
};

class Pool {
    ConnectionFactory& factory_;
public:
    explicit Pool(ConnectionFactory& f) : factory_(f) {}
    void lease() { auto c = factory_.make(); std::cout << c->id << "\n"; }
};

int main() {
    ConnectionFactory f;
    Pool p(f);                    // ✅ 注入工厂，按需创建连接
    p.lease(); p.lease();
}
