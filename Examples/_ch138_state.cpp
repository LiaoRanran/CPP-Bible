// _ch138_state.cpp
// 第138章 ⑩：状态模式——用对象封装状态及在该状态下的行为
#include <iostream>
#include <memory>

struct Context;
struct State {
    virtual ~State() = default;
    virtual void handle(Context& c) = 0;
};

struct Context {
    std::unique_ptr<State> st;
    void request();
};

struct On : State { void handle(Context& c) override; };
struct Off : State { void handle(Context& c) override; };

void On::handle(Context& c)  { std::cout << "switch -> off\n";  c.st = std::make_unique<Off>(); }
void Off::handle(Context& c) { std::cout << "switch -> on\n";   c.st = std::make_unique<On>(); }
void Context::request() { st->handle(*this); }

int main() {
    Context c{std::make_unique<Off>()};
    c.request(); c.request();
    return 0;
}
