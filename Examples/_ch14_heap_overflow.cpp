// _ch14_heap_overflow.cpp — 故意堆缓冲区溢出（ASan 取证）
#include <cstddef>

int main() {
    int* arr = new int[10];   // 合法下标 0..9
    arr[10] = 42;             // 越界写：溢出到相邻堆块头
    delete[] arr;
    return 0;
}
