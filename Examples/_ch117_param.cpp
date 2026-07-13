// ⑫ 参数传递优化（构造省略）：把临时对象直接构造到 by-value 形参
#include <cstdio>

struct Big {
    long a[8];
    Big() { a[0] = 3; }
    Big(const Big& o) { std::printf("copy!\n"); a[0] = o.a[0]; }
};

void sink(Big b) {            // 按值取参
    (void)b;
}

int main() {
    sink(Big{});               // ✅ 临时 Big 直接构造进形参 b，无拷贝
    return 0;
}
