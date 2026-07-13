struct Base {
    virtual int foo() { return 1; }
    Base() { foo(); }          // 构造期内虚调用：调 Base::foo
};
struct Derived : Base {
    int foo() override { return 2; }
    Derived() : Base() {}
};
int main() { Derived d; return d.foo(); }
