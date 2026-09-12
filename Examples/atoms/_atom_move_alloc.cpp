// 受控实验 ATOM-MEM-MOVE（机制类）：移动构造是否分配堆内存
// 控制变量：同一类型 Buf、同一编译器、-O2；唯一变量 = 拷贝构造 vs 移动构造。
// 观测：全局 operator new 调用次数（运行层）+ 汇编里是否有 call operator new（汇编层）。
// 证伪条件：若"移动"也产生 1 次分配，则本论断被证伪。
//
// 复现：
//   g++ -std=c++23 -O2 Examples/_atom_move_alloc.cpp -o /tmp/a.exe && /tmp/a.exe
//   g++ -std=c++23 -O2 -S -masm=intel Examples/_atom_move_alloc.cpp -o Examples/_atom_move_alloc.asm

#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <utility>

// volatile 是必需的，不是风格问题：分配"次数"与块大小无关，编译器在 -O2 下能静态
// 推出 1/1/0 并把计数折叠成常量（连 argc 都救不了）。volatile 强制每次分配产生可观测
// 副作用，计数才是运行时事实。这是 S3 伪证据检测的头号样本。
static volatile long g_allocs = 0;

// 注意：Buf 用 new int[n]（数组形式），走的是 operator new[]；
// 首版只替换了 operator new，导致计数恒为 0——"移动分配=0"看似证实论断，
// 实则是空测试（S3 伪证据检测的典型样本），故数组版本必须一并替换。
void* operator new(std::size_t n) {
    g_allocs = g_allocs + 1;          // 不用 ++：C++20 起 volatile 复合赋值已弃用
    return std::malloc(n);
}
void* operator new[](std::size_t n) {
    g_allocs = g_allocs + 1;
    return std::malloc(n);
}
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }
void operator delete[](void* p) noexcept { std::free(p); }
void operator delete[](void* p, std::size_t) noexcept { std::free(p); }

struct Buf {
    int* p = nullptr;
    std::size_t n = 0;

    explicit Buf(std::size_t n_) : n(n_) { p = new int[n]; }          // 构造：1 次
    ~Buf() { delete[] p; }

    Buf(const Buf& o) : n(o.n) {                                       // 拷贝：再分配 1 次
        p = new int[n];
        for (std::size_t i = 0; i < n; ++i) p[i] = o.p[i];
    }
    Buf(Buf&& o) noexcept : p(o.p), n(o.n) {                           // 移动：偷指针，0 次
        o.p = nullptr;
        o.n = 0;
    }
};

// 证伪对照：把"移动"实现成也分配（常见错误写法）。若本实验有区分力，
// 这一路必须产出"移动分配=1"；若它也输出 0，说明实验是恒真的空测试（伪证据）。
struct BadBuf {
    int* p = nullptr;
    std::size_t n = 0;
    explicit BadBuf(std::size_t n_) : n(n_) { p = new int[n]; }
    ~BadBuf() { delete[] p; }
    BadBuf(BadBuf&& o) : n(o.n) { p = new int[n]; }   // 假移动：又分配了一次
};

int main(int argc, char**) {
    // 大小取运行时值（argc），阻断编译期常量折叠：
    // 首版用字面量 64，在 -O2 下 GCC 直接把计数折叠成常量（汇编里 main 无 call _Znay，
    // 只剩 mov edx,1），运行输出看似"证实"论断，实则零观测——典型伪证据。
    const std::size_t n = static_cast<std::size_t>(argc) * 8 + 8;
    long base = 0, copy_allocs = 0, move_allocs = 0;
    {
        g_allocs = 0;
        Buf a(n);
        base = g_allocs;

        g_allocs = 0;
        Buf b = a;                    // 拷贝构造
        copy_allocs = g_allocs;

        g_allocs = 0;
        Buf c = std::move(a);         // 移动构造
        move_allocs = g_allocs;

        g_allocs = 0;
        BadBuf bad(n);
        g_allocs = 0;
        BadBuf bad2 = std::move(bad);          // 假移动
        long bad_move = g_allocs;
        std::printf("证伪对照(假移动)分配=%ld\n", bad_move);
    }

    std::printf("构造分配=%ld 拷贝分配=%ld 移动分配=%ld\n", base, copy_allocs, move_allocs);
    //@ 构造分配=1 拷贝分配=1 移动分配=0
    //@ 证伪对照(假移动)分配=1
    return 0;
}
