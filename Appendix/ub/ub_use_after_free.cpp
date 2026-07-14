// UB-01 use-after-free：释放后继续读写堆内存
// 编译: g++ -std=c++23 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer -o uaf ub_use_after_free.cpp
// 运行: ./uaf  →  ASan 报 heap-use-after-free
#include <cstdio>
#include <cstdlib>

int main() {
    int* p = static_cast<int*>(std::malloc(sizeof(int)));
    *p = 42;
    std::printf("before free: *p = %d\n", *p);
    std::free(p);          // p 指向的内存归还堆
    *p = 7;                // ❌ UB：释放后写
    std::printf("after free: *p = %d\n", *p);  // ❌ UB：释放后读
    return 0;
}
