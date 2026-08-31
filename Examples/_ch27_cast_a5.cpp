// _asm_demo/ch27_cast_test.cpp
#include <cstdint>
struct Base { virtual ~Base() = default; virtual void f() {} };
struct Derived : Base { void f() override {} };

int       static_cast_double_to_int(double d) { return static_cast<int>(d); }
const int* const_cast_remove(const int* p)     { return const_cast<int*>(p); }
uintptr_t reinterpret_cast_ptr_to_int(void* p){ return reinterpret_cast<uintptr_t>(p); }
void*     static_cast_to_void(int* p)           { return static_cast<void*>(p); }
Derived*  dynamic_cast_down(Base* p)            { return dynamic_cast<Derived*>(p); }
int       implicit_int_from_double(double d)    { return d; }