// _ch14_double_free.cpp — 故意双重释放（ASan 取证）
#include <cstddef>

int main() {
    int* p = new int(7);
    delete p;                 // 第一次释放
    delete p;                 // double free：第二次释放同一指针
    return 0;
}
