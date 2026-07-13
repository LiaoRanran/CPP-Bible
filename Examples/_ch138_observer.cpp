// _ch138_observer.cpp
// 第138章 ④⑤：观察者模式——signal/slot 式与现代 std::function 列表两种实现
#include <functional>
#include <iostream>
#include <string>
#include <vector>

// 经典接口式
struct Listener { virtual ~Listener() = default; virtual void on(const std::string&) = 0; };
struct Logger : Listener { void on(const std::string& s) override { std::cout << "[log] " << s << '\n'; } };

// 现代 std::function 列表
struct Subject {
    std::vector<std::function<void(const std::string&)>> slots;
    void subscribe(std::function<void(const std::string&)> f) { slots.push_back(std::move(f)); }
    void emit(const std::string& s) { for (auto& f : slots) f(s); }
};

int main() {
    Subject sub;
    sub.subscribe([](const std::string& s) { std::cout << "got: " << s << '\n'; });
    sub.emit("hello");
    return 0;
}
