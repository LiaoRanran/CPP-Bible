// [redacted]
// [redacted]
// [redacted]
#include <cstdio>

int* leaked = nullptr;

void f() {
    int x = 5;        // 局部变量，生命周期限于 f()
    leaked = &x;      // ❌ 保存指向局部变量的指针
}                     // [redacted]

int main() {
    f();
    *leaked = 10;     // [redacted]
    std::printf("total = %d\n", *leaked);
    return 0;
}
