// [redacted]
// [redacted]
#include <cstdio>

int* dangling() {
    int x = 5;            // [redacted]
    return &x;            // [redacted]
}

int main() {
    int* p = dangling();
    *p = 10;              // ❌ 写已销毁的栈槽
    std::printf("value = %d\n", *p);
    return 0;
}
