#include <cstdio>
#include <cstddef>
struct B1 { virtual ~B1()=default; virtual int f(){return 1;} };          // vptr-only primary
struct B2 { virtual ~B2()=default; virtual int g(){return 2;} int b=0; };
struct D : B1, B2 { int x=0; };
int main(){
    D d; char* base=reinterpret_cast<char*>(&d); char* b2=reinterpret_cast<char*>(static_cast<B2*>(&d));
    std::ptrdiff_t delta=b2-base;
    std::printf("canonical D:B1(vptr-only),B2(vptr+int),D(int)\n");
    std::printf("B1 vptr offset = 0x0 (object head)\n");
    std::printf("B2 subobject delta = %td (0x%tx)  // this 调整量\n", delta, delta);
    std::printf("vtable slot width = %zu (0x%zx)\n", sizeof(void(*)()), sizeof(void(*)()));
    return 0;
}
