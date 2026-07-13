// ⑧ 不能总是省略：多分支返回不同对象，编译器无法合并到同一栈槽
#include <cstdio>

struct Big {
    long a[8];
    Big() {}
    Big(const Big& o) { std::printf("copy!\n"); a[0] = o.a[0]; }
};

Big pick(bool cond) {
    Big a, b;                  // 两个可能的返回值
    if (cond) return a;        // 可能拷贝 a
    else      return b;        // 可能拷贝 b（不同栈槽，无法统一省略）
}

int main() {
    Big x = pick(true);
    return (int)x.a[0];
}
