// [redacted]
// [redacted]
// [redacted]
#include <cstdint>
#include <cstdio>

int main() {
    char buffer[8] = {0};
    // [redacted]
    void* mis = static_cast<void*>(buffer + 1);
    int* p = static_cast<int*>(mis);
    *p = 0xDEADBEEF;   // [redacted]
    std::printf("written via misaligned ptr\n");
    return 0;
}
