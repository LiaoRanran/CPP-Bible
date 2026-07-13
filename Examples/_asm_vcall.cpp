struct Base {
    virtual ~Base() {}
    virtual int foo() const { return 1; }
    int bar() const { return 2; }   // 非虚
};
struct Derived : Base {
    int foo() const override { return 3; }
};
int call_virtual(const Base& b) { return b.foo(); }   // 虚调用
int call_nonvirtual(const Base& b) { return b.bar(); } // 非虚调用
int main() {
    Derived d;
    return call_virtual(d) + call_nonvirtual(d);
}
