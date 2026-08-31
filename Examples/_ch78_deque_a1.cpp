#include <deque>
#include <vector>
#include <iostream>
#include <cassert>

int main() {
    // deque 双端 O(1) 均摊：头尾都能高效插入
    std::deque<int> d;
    for (int i = 0; i < 5; ++i) d.push_back(i);   // 0..4
    d.push_front(-1);                              // 头部插入
    std::cout << "deque front : " << d.front() << std::endl;
    std::cout << "deque back  : " << d.back() << std::endl;
    std::cout << "deque size  : " << d.size() << std::endl;
    assert(d.front() == -1);
    assert(d.back() == 4);
    assert(d.size() == 6);

    // vector 同样数据（仅尾部插入）：验证功能等价
    std::vector<int> v;
    v.push_back(-1);
    for (int i = 0; i < 5; ++i) v.push_back(i);
    std::cout << "vector front: " << v.front() << std::endl;
    std::cout << "vector back : " << v.back() << std::endl;
    std::cout << "vector size : " << v.size() << std::endl;
    assert(v.front() == -1);
    assert(v.back() == 4);
    assert(v.size() == d.size());

    // 稳定语义：deque 头插后元素序列与 vector 一致
    bool same = true;
    for (std::size_t i = 0; i < d.size(); ++i) {
        if (d[i] != v[i]) { same = false; break; }
    }
    std::cout << "sequence equal: " << std::boolalpha << same << std::endl;
    assert(same);
    return 0;
}