// 文件: Examples/_ch137_crtp_decorator.cpp
// CRTP Decorator：编译期静态组合装饰，零虚函数、可被完全内联
#include <iostream>

template <typename Base>
struct Logger : Base {
    void draw() const {
        std::cout << "[log] before\n";
        Base::draw();
        std::cout << "[log] after\n";
    }
};

struct Basic {
    void draw() const { std::cout << "basic draw\n"; }
};

using Decorated = Logger<Basic>;    // 编译期静态装饰，无运行期开销

int main() {
    Decorated d;
    d.draw();
}
