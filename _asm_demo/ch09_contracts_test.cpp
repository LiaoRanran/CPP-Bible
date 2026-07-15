// C++26 contracts (P2900) — 真实可编译实证 (GCC 15.3.0, -std=c++26 -O2 -fcontracts)
// 目的：验证 [[pre]]/[[post]] 断言检查在调用点的指令插入。
[[nodiscard]] int clamp(int x, int lo, int hi)
    [[pre: lo <= hi]]
    [[post r: r >= lo && r <= hi]]
{
    if (x < lo) return lo;
    if (x > hi) return hi;
    return x;
}

int main() {
    return clamp(5, 0, 10);
}
