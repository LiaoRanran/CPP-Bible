// ⑥ 静态分析替身：clang-tidy 会标记裸 new/裸循环，这里用 -Wall 复现
#include <cstdio>
#include <vector>

void leaky() {
    int* p = new int[10];          // ❌ 裸 new，tidy 报 modernize-make_unique
    std::printf("%d\n", p[0]);
    // 故意不 delete，作为"门禁该拦下"的样例
}

int main() {
    std::vector<int> v(3, 7);
    for (auto it = v.begin(); it != v.end(); ++it)   // ❌ 可改用 range-for
        std::printf("%d ", *it);
    std::printf("\n");
    leaky();
    return 0;
}
