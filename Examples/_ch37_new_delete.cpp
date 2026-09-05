// ch37 真机实证：new[]/delete[] 配对、RAII 自动释放与 vector 扩容的分配成本
//
// 取证方式：替换全局 operator new/delete 做计数（分配次数 / 字节 / 未释放数）。
// 这是 ch37 主题（operator new/delete 原语）自带的、最直接的观测手段：
// 不用任何外部工具，就能让"配对是否正确""RAII 是否真的释放了"变成可验证数字。
//
// 编译：g++ -std=c++23 -O2 -Wall -Wextra _ch37_new_delete.cpp -o _ch37_new_delete.exe

#include <cstdio>
#include <cstdlib>
#include <memory>
#include <vector>
#include <new>

static long g_new = 0, g_del = 0, g_live = 0;
static std::size_t g_bytes = 0;

void* operator new(std::size_t sz) {
    void* p = std::malloc(sz ? sz : 1);
    if (!p) throw std::bad_alloc();
    ++g_new; ++g_live; g_bytes += sz;
    return p;
}
void* operator new[](std::size_t sz) { return operator new(sz); }

void operator delete(void* p, std::size_t) noexcept {
    if (p) { ++g_del; --g_live; }
    std::free(p);
}
void operator delete(void* p) noexcept {
    if (p) { ++g_del; --g_live; }
    std::free(p);
}
void operator delete[](void* p, std::size_t sz) noexcept { operator delete(p, sz); }
void operator delete[](void* p) noexcept { operator delete(p); }

static void reset() { g_new = g_del = g_live = 0; g_bytes = 0; }

// 先取快照再 printf：避免 report 自身的分配污染被测计数
static void report(const char* tag) {
    long n = g_new, d = g_del, l = g_live;
    std::size_t b = g_bytes;
    std::printf("%-26s 分配=%ld 释放=%ld live=%ld 字节=%zu\n", tag, n, d, l, b);
}

int main() {
    std::printf("=== ch37 实证：new[]/delete[] 配对与 RAII（GCC %d.%d） ===\n",
                __GNUC__, __GNUC_MINOR__);

    reset();
    { int* a = new int[10]; delete[] a; }
    report("裸 new[] + delete[]");

    reset();
    { int* leak = new int[10]; (void)leak; }   // 故意不释放：观察 live
    report("裸 new[] 忘记释放");

    reset();
    { auto u = std::make_unique<int[]>(10); (void)u; }
    report("unique_ptr<int[]>");

    reset();
    { std::vector<int> v(10); }
    report("vector<int>(10)");

    reset();
    {
        std::vector<int> v;
        for (int i = 0; i < 1000; ++i) v.push_back(i);   // 触发多次扩容
    }
    report("vector push_back x1000");

    std::printf("\n结论：live=0 表示分配与释放配对；忘记释放时 live 保持 1（泄漏可见）。\n"
                "push_back 的分配次数远多于一次性构造 —— 这就是 reserve() 的意义。\n");
    return 0;
}
