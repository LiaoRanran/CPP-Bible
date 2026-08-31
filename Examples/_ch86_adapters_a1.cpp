#include <iostream>
#include <queue>
#include <stack>
#include <set>
#include <vector>
#include <deque>
#include <cassert>

int main() {
    std::vector<int> data{5, 3, 8, 1, 9, 2, 7};

    // priority_queue：连续内存上的隐式二叉堆（大顶堆）
    std::priority_queue<int> pq(std::less<int>(), data);
    std::vector<int> from_pq;
    while (!pq.empty()) { from_pq.push_back(pq.top()); pq.pop(); }

    // multiset：红黑树，每次取最大（--end）并删除
    std::multiset<int> ms(data.begin(), data.end());
    std::vector<int> from_ms;
    while (!ms.empty()) {
        auto it = ms.end(); --it;
        from_ms.push_back(*it);
        ms.erase(it);
    }

    std::cout << "priority_queue max-seq size: " << from_pq.size() << std::endl;
    std::cout << "multiset    max-seq size: " << from_ms.size() << std::endl;
    assert(from_pq.size() == from_ms.size());
    for (std::size_t i = 0; i < from_pq.size(); ++i) {
        std::cout << "k=" << i << " pq=" << from_pq[i]
                  << " ms=" << from_ms[i] << std::endl;
        assert(from_pq[i] == from_ms[i]);   // 同序列降序最大（绝不断言时间）
    }

    // stack<vector> 与 stack<deque> 的 LIFO 行为一致
    std::stack<int, std::vector<int>> sv;
    std::stack<int, std::deque<int>> sd;
    for (int v : {1, 2, 3}) { sv.push(v); sd.push(v); }
    std::cout << "stack<vector> top: " << sv.top() << std::endl;
    std::cout << "stack<deque>  top: " << sd.top() << std::endl;
    assert(sv.top() == sd.top());
    while (!sv.empty()) { assert(sv.top() == sd.top()); sv.pop(); sd.pop(); }
    return 0;
}