// _ch138_memento.cpp
// 第138章 ⑯：备忘录——捕获并外部化对象内部状态以便恢复
#include <iostream>
#include <string>

struct Memento {
    explicit Memento(std::string s) : state(std::move(s)) {}
    std::string state;
};

struct Originator {
    std::string text;
    Memento save() const { return Memento{text}; }
    void restore(const Memento& m) { text = m.state; }
};

int main() {
    Originator o;
    o.text = "v1"; auto m = o.save();
    o.text = "v2";
    std::cout << o.text << '\n';
    o.restore(m);
    std::cout << o.text << '\n';
    return 0;
}
