// _ch14_uaf.cpp — 故意释放后使用（ASan 取证）
#include <cstddef>

int main() {
    int* p = new int(7);
    delete p;                 // 释放
    *p = 1;                   // use-after-free：写已释放内存
    return 0;
}
