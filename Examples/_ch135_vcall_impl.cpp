// _ch135_vcall_impl.cpp
#include "_ch135_vcall.h"
int Dog::speak() const { return 42; }
int via_virtual(const Animal& a) { return a.speak(); } // 此处无法去虚化
