// [redacted]
#include <cstdio>

int main() {
    int x = 2147483647;       // INT_MAX
    x += 1;                   // [redacted]
    std::printf("%d\n", x);
    return 0;
}
