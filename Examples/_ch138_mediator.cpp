// _ch138_mediator.cpp
// 第138章 ⑮：中介者——让一组对象通过中介者通信，降低耦合
#include <functional>
#include <iostream>
#include <string>
#include <vector>

struct Mediator {
    std::vector<std::function<void(const std::string&)>> peers;
    void reg(std::function<void(const std::string&)> f) { peers.push_back(std::move(f)); }
    void broadcast(const std::string& msg) { for (auto& f : peers) f(msg); }
};

int main() {
    Mediator m;
    m.reg([](const std::string& s) { std::cout << "A recv: " << s << '\n'; });
    m.reg([](const std::string& s) { std::cout << "B recv: " << s << '\n'; });
    m.broadcast("hi");
    return 0;
}
