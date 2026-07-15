// ASM-77-vector_grow : push_back 触发扩容 (operator new + memmove) 实证
// 编译: g++ -std=c++26 -O2 -c ch77_vector_grow_test.cpp -o ch77_vector_grow_test.o
// 链接: g++ -std=c++26 -O2 ch77_vector_grow_test.cpp -o ch77_vector_grow_test.exe  (main 仅用于链接以显示符号名)
// 反汇编: objdump -d -M intel -C ch77_vector_grow_test.exe
#include <vector>

// 不预分配: push_back 多次触发扩容 (operator new 分配新缓冲 + memmove 搬旧元素 + operator delete 释放旧缓冲)
[[gnu::noinline]] void push_no_reserve() {
    std::vector<int> v;
    for (int i = 0; i < 8; ++i) v.push_back(i);
}

// 预分配: push_back 不触发扩容 (仅 reserve 时一次 operator new)
[[gnu::noinline]] void push_reserved() {
    std::vector<int> v;
    v.reserve(16);
    for (int i = 0; i < 8; ++i) v.push_back(i);
}

int main() {
    push_no_reserve();
    push_reserved();
    return 0;
}
