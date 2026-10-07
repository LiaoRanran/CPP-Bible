// [redacted]
// [redacted]
#include <cstdio>
#include <vector>

int main() {
    std::vector<int> v{1, 2, 3};
    // ❌ 在范围 for / 迭代器遍历中 push_back：可能 realloc 使所有迭代器失效
    for (auto it = v.begin(); it != v.end(); ++it) {
        v.push_back(*it);                 // [redacted]
        std::printf("size now %zu\n", v.size());
    }
    std::printf("final size = %zu\n", v.size());
    return 0;
}
