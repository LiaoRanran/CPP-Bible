// ASM-122-pmr: std::pmr 多态分配器 vs 默认 operator new —— GCC 15.3.0 真机实证
// 关键：pmr vector 在栈缓冲够用时完全不走 operator new；但每次分配仍需经
//       资源对象的虚函数 do_allocate（多态分配器自身的派发开销）。
#include <memory_resource>
#include <vector>
#include <cstdint>

// 默认 vector：增长走全局 operator new / operator delete
[[gnu::noinline]] void default_push() {
    std::vector<int> v;
    for (int i = 0; i < 16; ++i) v.push_back(i);
}

// pmr vector：monotonic 栈缓冲（1024B），16 个 int(≤64B) 必落在缓冲内
[[gnu::noinline]] void pmr_push() {
    char buf[1024];
    std::pmr::monotonic_buffer_resource res{buf, sizeof(buf)};
    std::pmr::vector<int> v{&res};
    for (int i = 0; i < 16; ++i) v.push_back(i);
}

int main() {
    default_push();
    pmr_push();
    return 0;
}
