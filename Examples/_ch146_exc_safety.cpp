// _ch146_exc_safety.cpp
// ⑤ 异常安全等级：基本 / 强 / 不抛出（noexcept）保证。
#include <cstdio>
#include <vector>
#include <stdexcept>

// 不抛出保证：push_back 在容量足够时不会分配，可标 noexcept
struct NoThrow {
    int v;
    NoThrow(int x) noexcept : v(x) {}
};

// 强保证：要么成功，要么状态不变（copy-and-swap 范式）
void strong_swap(std::vector<int>& a, std::vector<int>& b) noexcept {
    a.swap(b); // std::vector::swap 是 noexcept 的
}

// 基本保证：抛出异常后对象仍处有效（可析构、可赋值）状态
void basic_append(std::vector<int>& v, int x) {
    v.push_back(x); // 若重新分配失败，v 仍有效（可能不变或已追加）
}

int main() {
    std::vector<int> a{1, 2}, b{3, 4};
    strong_swap(a, b);
    basic_append(a, 9);
    std::printf("a[0]=%d b[0]=%d a.size=%zu\n", a[0], b[0], a.size());
    return 0;
}
