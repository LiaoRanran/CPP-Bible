// 文件: Examples/_ch137_decorator_stack.cpp
// 容器适配器 std::stack 本质是一种 Decorator：在底层序列容器上裁剪出栈语义
#include <deque>
#include <iostream>
#include <stack>
#include <vector>

int main() {
    std::stack<int, std::vector<int>> s;   // 用 vector 作底层容器
    s.push(1);
    s.push(2);
    std::cout << "top=" << s.top() << " size=" << s.size() << '\n';
    s.pop();
    std::cout << "after pop top=" << s.top() << '\n';
}
