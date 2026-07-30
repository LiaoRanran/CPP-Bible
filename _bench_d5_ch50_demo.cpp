#include <iostream>
#include <cassert>
#include <cstdint>

struct L {
    long long x = 1;
    virtual ~L() = default;
    virtual long long f() const { return x + 10; }
};
struct R {
    long long y = 2;
    virtual ~R() = default;
    virtual long long g() const { return y + 20; }
};
struct M : L, R {
    long long f() const override { return x + 100; }
    long long g() const override { return y + 200; }
};

// 虚继承菱形：VB 子对象只有一份
struct VB { long long z = 3; virtual ~VB() = default; };
struct VL : virtual VB { };
struct VR : virtual VB { };
struct VD : VL, VR { };

// 非虚继承菱形：VB 子对象有两份
struct NL : VB { };
struct NR : VB { };
struct ND : NL, NR { };

int main() {
    M m;

    // 1) 第二基类子对象不在对象首地址 —— this 需要调整
    L* pl = static_cast<L*>(&m);
    R* pr = static_cast<R*>(&m);
    auto base = reinterpret_cast<std::uintptr_t>(&m);
    auto off_l = reinterpret_cast<std::uintptr_t>(pl) - base;
    auto off_r = reinterpret_cast<std::uintptr_t>(pr) - base;

    std::cout << "offset of L subobject : " << off_l << std::endl;
    std::cout << "offset of R subobject : " << off_r << std::endl;
    std::cout << "R needs this-adjust?  : " << (off_r != 0 ? "yes" : "no") << std::endl;

    assert(off_l == 0);   // 第一基类与派生类共享首地址
    assert(off_r != 0);   // 第二基类必须偏移 —— thunk 存在的根本原因

    // 2) 经第二基类指针的虚调用仍然正确分派到 M::g（thunk 把 this 调回来）
    std::cout << "pl->f() = " << pl->f() << std::endl;
    std::cout << "pr->g() = " << pr->g() << std::endl;
    assert(pl->f() == 101);
    assert(pr->g() == 202);

    // 3) 反向转换回派生类，地址复原
    M* back = static_cast<M*>(pr);
    std::cout << "static_cast<M*>(pr) == &m? : " << (back == &m ? "yes" : "no") << std::endl;
    assert(back == &m);

    // 4) 虚继承：两条路径抵达同一个 VB 子对象
    VD vd;
    VB* v_via_l = static_cast<VB*>(static_cast<VL*>(&vd));
    VB* v_via_r = static_cast<VB*>(static_cast<VR*>(&vd));
    std::cout << "virtual-inherit: same VB? : "
              << (v_via_l == v_via_r ? "yes" : "no") << std::endl;
    assert(v_via_l == v_via_r);      // 虚基类共享唯一子对象

    // 5) 非虚继承：两条路径抵达不同 VB 子对象（菱形歧义的来源）
    ND nd;
    VB* n_via_l = static_cast<VB*>(static_cast<NL*>(&nd));
    VB* n_via_r = static_cast<VB*>(static_cast<NR*>(&nd));
    std::cout << "non-virtual   : same VB? : "
              << (n_via_l == n_via_r ? "yes" : "no") << std::endl;
    assert(n_via_l != n_via_r);      // 两份独立副本

    // 6) 虚继承下改写虚基类成员，两条路径同时可见
    v_via_l->z = 77;
    std::cout << "z via VR path = " << static_cast<VR*>(&vd)->z << std::endl;
    assert(static_cast<VR*>(&vd)->z == 77);

    // 虚继承对象通常更大（多出一个 vptr），但不断言精确 sizeof
    std::cout << "sizeof(VD) >= sizeof(VB)? : "
              << (sizeof(VD) >= sizeof(VB) ? "yes" : "no") << std::endl;

    std::cout << "all assertions passed" << std::endl;
    return 0;
}