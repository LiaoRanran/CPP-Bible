// ch144 ⑪ 移动语义：按值接收 + std::move 避免深拷贝
// 编译：g++ -std=c++23 -O2 -S -masm=intel _ch144_move.cpp -o _ch144_move_O2.asm
#include <vector>

std::vector<int> make_buffer() {
    std::vector<int> v(4096, 7);   // 大缓冲区
    return v;                       // NRVO / 移动，无元素拷贝
}

std::vector<int> consume() {
    auto v = make_buffer();         // ✅ 移动构造，无 4096 次 int 拷贝
    v.push_back(1);
    return v;                       // 再次移动
}

int demo() {
    auto b = consume();
    return static_cast<int>(b.size());
}
