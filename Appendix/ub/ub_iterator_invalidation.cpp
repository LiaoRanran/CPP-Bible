// UB-L2 iterator invalidation：遍历中修改容器使迭代器失效
// 编译: g++ -std=c++23 -O2 -Wall -o itinv ub_iterator_invalidation.cpp
#include <cstdio>
#include <vector>

int main() {
    std::vector<int> v{1, 2, 3};
    // ❌ 在范围 for / 迭代器遍历中 push_back：可能 realloc 使所有迭代器失效
    for (auto it = v.begin(); it != v.end(); ++it) {
        v.push_back(*it);                 // 扩容时 it/end 指向旧缓冲 → 悬垂
        std::printf("size now %zu\n", v.size());
    }
    std::printf("final size = %zu\n", v.size());
    return 0;
}
