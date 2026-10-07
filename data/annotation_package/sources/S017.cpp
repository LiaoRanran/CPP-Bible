// [redacted]
#include <cstddef>

int main() {
    int* p = new int[100];    // 分配后永不释放
    (void)p;                  // 防止“未使用”告警
    return 0;                 // [redacted]
}
