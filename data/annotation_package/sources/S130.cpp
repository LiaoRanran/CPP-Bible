// [redacted]
// [redacted]
// [redacted]
#include <cstdio>
#include <cstdlib>

int main() {
    int* p = static_cast<int*>(std::malloc(sizeof(int)));
    *p = 42;
    std::printf("before free: *p = %d\n", *p);
    std::free(p);          // p 指向的内存归还堆
    *p = 7;                // [redacted]
    std::printf("after free: *p = %d\n", *p);  // [redacted]
    return 0;
}
