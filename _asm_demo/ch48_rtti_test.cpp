// ch48 RTTI 汇编实证
// 编译: g++ -std=c++23 -O2 -c ch48_rtti_test.cpp && objdump -dC ch48_rtti_test.o
#include <typeinfo>

struct Base    { virtual ~Base(); virtual void f(); };
struct Derived : Base { void f() override; };

// ① typeid(多态对象) —— 读 vtable[-1] 槽的 type_info 指针
const std::type_info& who(Base& b) {
    return typeid(b);          // 运行期: *(vptr - 8) 得 type_info*
}

// ② dynamic_cast 下行 —— 调用 __dynamic_cast 运行期函数
Derived* down(Base* b) {
    return dynamic_cast<Derived*>(b);
}

// ③ typeid 静态类型（非多态表达式）—— 编译期解析，无运行期开销
const std::type_info& static_who() {
    return typeid(Derived);    // 编译期常量 type_info 地址
}
