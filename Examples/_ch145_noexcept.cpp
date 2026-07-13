// _ch145_noexcept.cpp —— noexcept 与异常规范（g++ -O2 -S 取证）
#include <cstdio>

void fragile() { throw 1; }                 // 可能抛异常
void solid() noexcept { std::printf("ok\n"); }  // 承诺不抛

void call_fragile() { fragile(); }          // 需异常展开框架 / 落地 pad
void call_solid()   { solid(); }            // 直接 call，无 EH 负担

int main() { call_solid(); return 0; }
