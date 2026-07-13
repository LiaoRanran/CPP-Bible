// ⑪ NRVO（具名返回值优化）：具名对象在 -O2 下复用调用者栈槽
#include <cstdio>

struct Big {
    long a[8];
    Big() { a[0] = 7; }
    Big(const Big& o) { std::printf("copy!\n"); a[0] = o.a[0]; }
};

Big compute(int sel) {
    Big result;                 // 具名返回值
    result.a[0] = sel;
    return result;              // NRVO：result 直接落在调用者返回槽
}

int main() {
    Big x = compute(7);
    return (int)x.a[0];
}
