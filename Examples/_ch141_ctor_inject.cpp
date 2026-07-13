// Examples/_ch141_ctor_inject.cpp
// 构造函数注入（Constructor Injection）：依赖在构造期一次性绑定，对象不可变（const 成员）。
#include <iostream>
#include <string>

struct Config { int port{8080}; };

class Server {
    const Config& cfg_;                // const 引用：构造后不再变化
public:
    explicit Server(const Config& cfg) : cfg_(cfg) {}
    void start() const { std::cout << "listen :" << cfg_.port << "\n"; }
};

int main() {
    Config cfg; cfg.port = 9000;
    Server srv(cfg);                   // 依赖在构造时注入
    srv.start();
}
