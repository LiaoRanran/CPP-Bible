// [redacted]
// [redacted]
// [redacted]
#include <cstdlib>

int main() {
    int* p = static_cast<int*>(std::malloc(sizeof(int)));
    std::free(p);          // 第一次释放，合法
    std::free(p);          // [redacted]
    return 0;
}
