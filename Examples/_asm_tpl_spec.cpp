// 类模板特化与偏特化：取成员函数地址强制发射各特化的 mangled 符号
// 编译：g++ -std=c++23 -O2 -S -masm=intel _asm_tpl_spec.cpp -o _asm_tpl_spec.asm
#include <cstddef>

template <typename T>
struct Wrapper {                      // 主模板
    static const char* kind();
};
template <typename T> const char* Wrapper<T>::kind() { return "primary"; }

template <>                           // 全特化 T=int
struct Wrapper<int> { static const char* kind(); };
const char* Wrapper<int>::kind() { return "full-int"; }

template <typename U>                 // 偏特化 指针
struct Wrapper<U*> { static const char* kind(); };
template <typename U> const char* Wrapper<U*>::kind() { return "partial-ptr"; }

template <typename V>                 // 偏特化 const
struct Wrapper<const V> { static const char* kind(); };
template <typename V> const char* Wrapper<const V>::kind() { return "partial-const"; }

// 取地址：强制实例化各特化的 kind() 符号
using KF = const char* (*)();
KF a = &Wrapper<double>::kind;        // 主模板        _ZN7WrapperIdE4kindEv
KF b = &Wrapper<int>::kind;           // 全特化 int    _ZN7WrapperIiE4kindEv
KF c = &Wrapper<int*>::kind;          // 偏特化 指针   _ZN7WrapperIPiE4kindEv
KF d = &Wrapper<const double>::kind;  // 偏特化 const  _ZN7WrapperIKdE4kindEv

int main() {
    return (a() && b() && c() && d()) ? 0 : 1;
}
