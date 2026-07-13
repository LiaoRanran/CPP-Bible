// ch51 CRTP 真实汇编提取源（impl 非平凡，凸显内联/零 vtable）
// 编译：g++ -std=c++23 -O2 -S -masm=intel _asm_crtp.cpp -o _asm_crtp.asm
template <class Derived>
struct CrtpBase {
    int interface() { return static_cast<Derived*>(this)->impl() + 1; }
};

struct Vec3 : CrtpBase<Vec3> {
    int v = 0;
    int impl() { return v * 3; }   // 非平凡：读取成员并运算
};

int use_crtp(Vec3& b) { return b.interface(); }   // 应内联为 b.v*3 + 1

// 对照：虚函数版本
struct VBase { virtual int impl() = 0; virtual ~VBase() = default; };
struct VVec3 : VBase {
    int v = 0;
    int impl() override { return v * 3; }
};
int use_virtual(VBase& b) { return b.impl() + 1; }   // 走 vtable
