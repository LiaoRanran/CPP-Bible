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
B2* as_b2(D& d) { return &d; }
int read_x(D* p) { return p->x; }