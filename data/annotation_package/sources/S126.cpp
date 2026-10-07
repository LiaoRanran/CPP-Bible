// [redacted]
// [redacted]
#include <cstdio>

const int G = 5;                 // 真正 const 对象，可能置于只读段

int main() {
    const_cast<int&>(G) = 10;   // [redacted]
    std::printf("G = %d\n", G);
    return 0;
}
