// ⑥ 无 RVO：返回到具名对象之外的临时或显式 move 会触发拷贝/移动
#include <cstdio>

struct Big {
    long a[8];
    Big() { a[0] = 1; }
    Big(const Big& o) { std::printf("copy ctor!\n"); a[0] = o.a[0]; }
};

Big make_copy() {
    Big b;
    Big tmp = b;        // 显式制造第二个对象
    return tmp;         // 返回的是 tmp（非唯一局部），仍可能被 NRVO
}

// 强制走拷贝：把局部转成右值再返回，会抑制 NRVO
Big make_forced(const Big& src) {
    Big b = src;
    return b;           // 形参不是本函数局部对象，无法省略
}

int main() {
    Big x = make_forced(Big{});
    return (int)x.a[0];
}
