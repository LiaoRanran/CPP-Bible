// ch50 多重继承真实汇编提取源（虚函数体引用 this 成员，暴露 thunk 的 this 调整）
// 编译：g++ -std=c++23 -O2 -S -masm=intel _asm_mi.cpp -o _asm_mi.asm
struct B1 { virtual void f(); virtual ~B1(); };
struct B2 { virtual void g(); virtual ~B2(); };
struct D : B1, B2 {
    int x = 1;
    void f() override;
    void g() override;
};
void D::f() { x = 7; }     // this 指向 D 头（B1 在偏移0）
void D::g() { x = 9; }     // 经 B2* 调用时 this 指向 D+8，thunk 需 this-=8

void call_b2_g(B2* p) { p->g(); }
void call_d_f(D* p)  { p->f(); }
B2* as_b2(D& d) { return &d; }
int read_x(D* p) { return p->x; }
