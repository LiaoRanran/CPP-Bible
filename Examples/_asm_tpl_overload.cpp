// 函数模板重载决议：用 volatile 副作用强制发射被选函数符号
// 编译：g++ -std=c++23 -O2 -S -masm=intel _asm_tpl_overload.cpp -o _asm_tpl_overload.asm
#include <utility>

volatile int g_log[8];
int g_i = 0;

void f(int)  { g_log[g_i++] = 100; }          // 非模板：最高优先权  _Z1fi
template <typename T> void f(T) { g_log[g_i++] = 200; }   // 泛化模板        _Z1fIiEvT_
template <typename T> void f(T*) { g_log[g_i++] = 300; }  // 更特化的模板    _Z1fIPiEvPT_

void g(int)   { g_log[g_i++] = 11; }          // _Z1gi
template <typename T> void g(T*) { g_log[g_i++] = 22; }   // _Z1gIPiEvPT_

int main() {
    int x = 5;
    f(42);     // -> f(int)        非模板胜出     期望 100
    f(x);      // -> f(int)        非模板胜出     期望 100
    f(&x);     // -> f(int*)       模板更特化胜出 期望 300
    g(&x);     // -> g(int*)       仅模板可用     期望 22
    g(7);      // -> g(int)        非模板胜出     期望 11
    int s = 0;
    for (int k = 0; k < g_i; ++k) s += g_log[k];
    return s;  // 100+100+300+22+11 = 533
}
