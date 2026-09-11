// Examples/_atom_value_xvalue.cpp
// 服务 ATOM-MEM-VALUE-001：证伪卡"std::move(x) 产生 prvalue"。
// 关键区分（运行期可观测）：xvalue 有身份——它指代**特定对象 x**，移动后 x 被改动；
// prvalue 是"纯值"，不指代任何命名对象，移动/拷贝它不会影响任何已有对象。
// 若 std::move(x) 真是 prvalue（即"x 的一份临时副本"），则从它移动应**不动 x**；
// 实测 x 被改动 => 表达式 std::move(x) 指代真实对象 x => 它是 xvalue，不是 prvalue。
#include <utility>
#include <iostream>

struct Box {
    int v;
    Box(int i = 0) : v(i) {}
    Box(Box&& o) noexcept : v(o.v) { o.v = -1; }   // 移动后把源置 -1（让"身份"可观测）
};

int main() {
    Box a(7);
    Box b = std::move(a);        // xvalue：从真实对象 a 移动；a.v 被移动构造置 -1
    Box c = Box(7);              // prvalue：从临时初始化；没有任何命名对象被改动
    std::cout << "after move from xvalue(std::move(a)): source a.v = " << a.v << "\n";
    std::cout << "b.v = " << b.v << "  c.v = " << c.v << "\n";
    return 0;
}
