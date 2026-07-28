struct Base {
    virtual int f() const { return 1; }
    virtual int g() const { return 2; }
    virtual ~Base() = default;
};
struct Derived : Base {
    int f() const override { return 10; }
};

int call_f(const Base* p) { return p->f(); }  // 虚调用点

int main() {
    Derived d;
    return call_f(&d);
}
