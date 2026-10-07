// [redacted]
#include <cstddef>

int main() {
    int* p = new int(7);
    delete p;                 // 第一次释放
    delete p;                 // [redacted]
    return 0;
}
