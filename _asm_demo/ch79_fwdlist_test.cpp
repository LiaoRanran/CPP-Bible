#include <forward_list>

// 批 L3：forward_list 无 size 成员 + 单链哨兵 before_begin + insert_after 单指针改写
int main() {
    std::forward_list<int> fl;
    fl.push_front(1);
    fl.push_front(2);
    auto it = fl.before_begin();   // 哨兵，无真实元素
    fl.insert_after(it, 42);       // 仅改 2 个 next 指针
    int s = 0;
    for (auto v : fl) s += v;
    volatile int sink = s;
    (void)sink;
    return 0;
}
