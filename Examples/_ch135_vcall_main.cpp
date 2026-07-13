// _ch135_vcall_main.cpp
#include "_ch135_vcall.h"
#include <cstdio>
int main() {
    Dog d;
    volatile int s = via_virtual(d); // 真实虚调用走 vtable
    (void)s;
}
