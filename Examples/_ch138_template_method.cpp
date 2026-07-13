// _ch138_template_method.cpp
// 第138章 ⑦：模板方法——在基类固定算法骨架，子类覆写步骤钩子
#include <iostream>

struct Game {
    virtual ~Game() = default;
    void run() {            // 不变骨架
        start();
        for (int i = 0; i < rounds(); ++i) step();
        end();
    }
    virtual void start() = 0;
    virtual void step()  = 0;
    virtual void end()   = 0;
    virtual int  rounds() const { return 3; }   // 钩子（可覆写，也可不覆写）
};

struct Chess : Game {
    void start() override { std::cout << "chess start\n"; }
    void step()  override { std::cout << "chess move\n"; }
    void end()   override { std::cout << "chess end\n"; }
};

int main() { Chess{}.run(); return 0; }
