// _ch138_state_table.cpp
// 第138章 ⑪：表驱动状态机——用数组/跳转表替代大量状态子类
#include <iostream>

enum class S { Idle, Run, Stop };
enum class E { Start, Stop, Reset };

S next(S s, E e) {
    static const S tbl[3][3] = {   // [当前状态][事件]
        /*Idle*/ {S::Run,  S::Idle,  S::Idle },
        /*Run */ {S::Run,  S::Stop,  S::Idle },
        /*Stop*/ {S::Idle, S::Stop,  S::Idle },
    };
    return tbl[static_cast<int>(s)][static_cast<int>(e)];
}

int main() {
    S s = S::Idle;
    s = next(s, E::Start); std::cout << static_cast<int>(s) << '\n';
    s = next(s, E::Stop);  std::cout << static_cast<int>(s) << '\n';
    return 0;
}
