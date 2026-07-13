#include <cstdio>

struct B { int b = 1; virtual void f() {} };
struct M1 : virtual B { int m1 = 2; };
struct M2 : virtual B { int m2 = 3; };
struct D : M1, M2 { int d = 4; };

// 经派生 D 访问共享虚基类 B 的成员 b —— 需经 vbptr + vbase offset 调整
int read_vbase(const D& x) {
    return x.b;          // 访问虚基类子对象
}

// 跨菱形 dynamic_cast：M1* -> B*（虚基类）
B* cross_cast(M1* p) {
    return dynamic_cast<B*>(p);
}

int main() {
    D d;
    std::printf("%d %d\n", read_vbase(d), cross_cast(&d)->b);
    return 0;
}
