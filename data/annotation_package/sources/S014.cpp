// [redacted]
#include <cstddef>

int main() {
    int* arr = new int[10];   // 合法下标 0..9
    arr[10] = 42;             // [redacted]
    delete[] arr;
    return 0;
}
