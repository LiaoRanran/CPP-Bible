// P1-GAP-4: 虚析构 deleting destructor（析构链 + operator delete 合体）
// 揭示的底层事实：
//   - 有虚析构的类，vtable 前两个槽是 complete( D1 ) / deleting( D0 ) 析构；
//   - delete 基类指针：经虚表间接调用派生 deleting destructor（D0），
//     D0 = 完整析构链（派生 D1 内联调用基类 D1） + operator delete(this, sizeof(Derived))。
#include <cstddef>

long long g_calls;

struct Base {
    virtual ~Base();          // out-of-line key function，强制 vtable
    int b;
};

struct Derived : Base {
    ~Derived();               // out-of-line
    int d;
};

Base::~Base() { g_calls += 1; }
Derived::~Derived() { g_calls += 2; }

// delete 经基类指针：虚表间接调用派生 D0（析构链 + 传 sizeof 给 operator delete）
void destroy_base(Base* p) { delete p; }

// delete 直接派生指针：同样走虚表 D0（比较二者是否同一条间接调用）
void destroy_derived(Derived* p) { delete p; }

long long sizeof_base() { return sizeof(Base); }
long long sizeof_derived() { return sizeof(Derived); }