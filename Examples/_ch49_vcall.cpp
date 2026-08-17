// _ch49_vcall.cpp
// ch49 虚继承章·附录 G 真实复现源（MinGW GCC 15.3.0, Windows x64 ABI, this=rcx）
// 编译（须从 Examples/ 内相对路径编译，保证 .file 指令为基名）：
//   g++ -std=c++23 -O2 -S -masm=intel _ch49_vcall.cpp -o _ch49_vcall.asm
struct Base {
    virtual int foo() { return 42; }
    int pad = 0;
};
struct Derived : Base {
    int foo() override { return 7; }
};
// 虚调用点：this 经 rcx 传入（Windows x64 ABI）；vptr 取址 + vtable 槽间接跳转
int call_foo(Base* p) {
    return p->foo();
}
