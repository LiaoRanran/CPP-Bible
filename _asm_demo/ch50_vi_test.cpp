// ASM-50-vi : GCC 15.3.0 真机实证 —— 虚继承(virtual inheritance)的 this 调整 thunk 与 vbptr 布局
// 编译: g++ -std=c++26 -O2 ch50_vi_test.cpp -o ch50_vi_test.exe
// 反汇编: objdump.exe -d -M intel -C ch50_vi_test.exe
//
// 设计要点：让虚函数 f 真正访问成员(this->b / this->d)，迫使经虚基类指针 B* 调用 f 时
// 必须先把 this 从 B 子对象调整到完整 D 对象 —— 编译器为此生成"虚 this 调整 thunk"
// (符号形如 _ZTv0_nXX_N1D1fEv)。同时 B 作为虚基类不再按固定偏移内嵌，D 对象通过 vbptr/vbtable 寻址。
#include <cstdio>

struct B {
    int b = 100;
    virtual int f() { return b; }            // 用 this->b
};

struct D : virtual B {                        // B 为虚基类
    int d = 7;
    int f() override { return b + d; }        // 用 this->b 与 this->d，需完整 D 的 this
};

[[gnu::noinline]] int callD(D* pd) { return pd->f(); }   // 经最派生类指针：无 this 调整
[[gnu::noinline]] int callB(B* pb) { return pb->f(); }   // 经虚基类指针：需 this 调整到最派生对象

int main() {
    D d;
    int r = callD(&d) + callB(&d);
    std::printf("%d\n", r);
    return 0;
}
