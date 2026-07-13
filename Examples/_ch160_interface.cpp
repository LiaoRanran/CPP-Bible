// 文件：Examples/_ch160_interface.cpp
// 行号：1
// 内存分配器接口：重载 class 专属 operator new/delete
#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <new>

struct Widget {
    int id;
    double data[4];
    static std::size_t alloc_count;   // 统计分配次数
    static void* operator new(std::size_t n) {
        ++alloc_count;
        void* p = std::malloc(n);
        if (!p) throw std::bad_alloc{};
        return p;
    }
    static void operator delete(void* p, std::size_t) noexcept {
        std::free(p);
    }
};
std::size_t Widget::alloc_count = 0;

int main() {
    Widget* w = new Widget{1, {1,2,3,4}};
    std::printf("Widget id=%d alloc_count=%zu\n", w->id, Widget::alloc_count);
    delete w;
    return 0;
}
