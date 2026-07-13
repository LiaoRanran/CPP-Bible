// 文件：Examples/_ch160_global_new.cpp
// 行号：1
// 全局替换 operator new/delete（演示，注意风险：见正文⑨）
#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <new>

// 极简全局替换：把所有分配转到 malloc/free（仅作演示，无池化）
void* operator new(std::size_t n) {
    void* p = std::malloc(n);
    if (!p) throw std::bad_alloc{};
    return p;
}
void operator delete(void* p) noexcept {
    if (p) std::free(p);
}
void operator delete(void* p, std::size_t) noexcept {
    if (p) std::free(p);
}

int main() {
    int* a = new int(42);
    double* b = new double[10];
    std::printf("global new/delete: a=%d b[0]=%f\n", *a, b[0]);
    delete a;
    delete[] b;
    return 0;
}
