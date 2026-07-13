// _ch148_atomic_split.cpp
// 演示「原子提交」：把一次大改动拆成「加接口」与「改实现」两个提交。
// 反模式是把重构、新功能、格式化混在同一提交（见 ⑱ 反模式）。
#include <cstdio>
#include <vector>

// 提交 A（只加接口，不改既有行为）
struct Buffer {
    std::vector<int> data;
    void reserve(size_t n) { data.reserve(n); }   // 新增接口
};

// 提交 B（只改实现，不引入新接口）
void fill(Buffer& b, int value, size_t count) {
    b.reserve(count);
    for (size_t i = 0; i < count; ++i) b.data.push_back(value);
}

int main() {
    Buffer b;
    fill(b, 7, 3);
    std::printf("size=%zu\n", b.data.size());
    return 0;
}
