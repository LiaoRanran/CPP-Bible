// UB-02 double-free：同一指针释放两次
// 编译: g++ -std=c++23 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer -o df ub_double_free.cpp
// 运行: ./df  →  ASan 报 double-free
#include <cstdlib>

int main() {
    int* p = static_cast<int*>(std::malloc(sizeof(int)));
    std::free(p);          // 第一次释放，合法
    std::free(p);          // ❌ UB：第二次释放同一指针
    return 0;
}
