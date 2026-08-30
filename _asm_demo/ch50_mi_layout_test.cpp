// P1-GAP-2: 多继承对象布局（多 vptr、基类子对象顺序、非虚 MI this 调整 thunk）
// 揭示的底层事实：
//   - 多继承下对象含多个 vptr（每个多态基类一个），基类子对象按声明序排列；
//   - 调用"第二个及其后基类"的虚函数时，GCC 生成非虚 thunk，
//     把 this 从子对象指针固定减去偏移调回派生类（非运行时查表）。
#include <cstddef>

struct B1 { int b1; virtual ~B1() {} virtual int f1() { return 1; } };
struct B2 { int b2; virtual ~B2() {} virtual int f2() { return 2; } };
struct D : B1, B2 {
    int d;
    explicit D(int v) : d(v) {}
    int f1() override { return 11; }
    int f2() override;  // out-of-line key function，强制生成 vtable + thunk
};

int D::f2() { return d + 22; }  // 访问成员 d（经 this 寻址），逼出 thunk 的 this 调整

// 通过 B2*（第二个基类）调用 f2 —— 触发 non-virtual thunk 的 this 调整
int call_f2_via_b2(B2* b2) { return b2->f2(); }

// 对象布局探测：B2 子对象相对 D 基址的偏移
long long b2_offset() {
    D d(0);
    B2* pb2 = &d;
    return reinterpret_cast<char*>(pb2) - reinterpret_cast<char*>(&d);
}

// 对象总大小探测（用于对照 deleting destructor 传给 operator delete 的 size）
long long sizeof_D() { return sizeof(D); }