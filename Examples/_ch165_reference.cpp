// _ch165_reference.cpp : 引用/const/移动语义练习（中级）
#include <iostream>
#include <utility>
#include <vector>

void inc(int& r) { r++; }                 // 左值引用：别名，必绑对象

int main() {
    int a = 5;
    inc(a);
    std::cout << a << "\n";                // 6

    const int& cr = 10;                    // const 引用可绑临时量
    std::cout << cr << "\n";

    std::vector<int> v = {1, 2, 3};
    std::vector<int> w = std::move(v);      // 移动：v 被掏空，w 接管
    std::cout << w.size() << "\n";          // 3
    std::cout << v.size() << "\n";          // 0
    return 0;
}
