// ⑦ std::move 陷阱：对局部返回值用 move 会抑制 NRVO，反而触发移动构造
#include <cstdio>
#include <utility>

struct Big {
    long a[8];
    Big() { a[0] = 1; }
    Big(const Big& o) { std::printf("copy!\n");  a[0] = o.a[0]; }
    Big(Big&& o)      { std::printf("move!\n");  a[0] = o.a[0]; }
};

Big bad() {
    Big b;
    return std::move(b);   // ❌ 抑制 NRVO -> 走到移动构造
}

Big good() {
    Big b;
    return b;              // ✅ 允许 NRVO -> 零拷贝零移动
}

int main() {
    Big x = bad();
    Big y = good();
    return (int)(x.a[0] + y.a[0]);
}
