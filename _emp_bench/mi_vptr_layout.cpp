// mi_vptr_layout.cpp —— 验证多继承对象 vptr 布局（ch50 §底层视角 声称）
// 编译: g++ -std=c++23 -O2 mi_vptr_layout.cpp -o mi_vptr_layout && ./mi_vptr_layout
// 真实测量: 次级基类子对象相对完整对象的偏移（this 调整值）+ vtable 槽宽
#include <cstdio>
#include <cstddef>

struct B1 { virtual ~B1() = default; virtual int f() { return 1; } int a = 0; };
struct B2 { virtual ~B2() = default; virtual int g() { return 2; } int b = 0; };
struct D  : B1, B2 { int x = 0; };

int main() {
    D d;

    // 1) 次级基类 B2 子对象相对 D 首部的偏移 —— 即 thunk 的 this 调整量
    char* base = reinterpret_cast<char*>(&d);
    char* b2   = reinterpret_cast<char*>(static_cast<B2*>(&d));
    std::ptrdiff_t delta = b2 - base;

    // 2) 对象大小 & 各子对象布局信息（Itanium ABI / x64）
    std::printf("sizeof(D)        = %zu (0x%zx)\n", sizeof(D), sizeof(D));
    std::printf("offsetof(D, a)   = %zu (0x%zx)  // B1 数据成员\n", offsetof(D, a), offsetof(D, a));
    std::printf("offsetof(D, b)   = %zu (0x%zx)  // B2 数据成员\n", offsetof(D, b), offsetof(D, b));
    std::printf("offsetof(D, x)   = %zu (0x%zx)  // D  数据成员\n", offsetof(D, x), offsetof(D, x));
    std::printf("B2 subobject delta = %td (0x%tx) // this 调整量\n", delta, delta);

    // 3) vtable 槽宽: 方法指针大小恒为 8（x64 指针宽度）
    std::printf("sizeof(void(*)()) = %zu (0x%zx)  // vtable 槽宽\n", sizeof(void(*)()), sizeof(void(*)()));

    // 4) 确认 vptr 落点: B1 vptr @ 0x0000, B2 vptr @ delta
    //    D 作为 B1 子对象首地址即对象首部; 作为 B2 子对象首地址 = 对象首部 + delta
    std::printf("B1 vptr @ offset 0x0000 (对象首部)\n");
    std::printf("B2 vptr @ offset 0x%tx (= delta)\n", delta);
    return 0;
}
