#include <iostream>

struct Big { double a[8]; };

double by_value(Big b) { double s = 0; for (double x : b.a) s += x; return s; }
double by_cref(const Big& b) { double s = 0; for (double x : b.a) s += x; return s; }

int main() {
    Big b{1, 2, 3, 4, 5, 6, 7, 8};
    double s1 = by_value(b);   // 调用点发生 64 字节栈拷贝
    double s2 = by_cref(b);    // 仅传指针
    std::cout << "by_value sum = " << s1 << ", by_cref sum = " << s2 << std::endl;
    return 0;
}