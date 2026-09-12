// Examples/_atom_rule_three_bug.cpp
// 服务 ATOM-MEM-RAII-002：违反 Rule of Three 的后果（对照实验）。
// 论断：只写析构函数、不写拷贝构造 → 编译器隐式生成**浅拷贝** → 两个对象共享同一块资源 →
//       同一块资源被析构两次（若析构函数释放资源即为 double free）。
// 观测纪律：析构为观测型（只计数，不真正释放），使 double-destruct 成为可重复、不崩溃的确定观制；
//           真实 double-free 的 ASan 捕获在 WSL 单独复现（见 EV-MEM-024 卡内说明）。
// 对照组：Rule of Three 全写的 Correct（深拷贝），证明实验有区分力。
#include <iostream>
#include <cstdlib>

volatile long g_allocs = 0;
volatile long g_dtors = 0;
void* operator new(size_t n) { g_allocs = g_allocs + 1; return std::malloc(n); }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, size_t) noexcept { std::free(p); }

struct Buggy {                    // 违反 Rule of Three：只写析构（拷贝交给编译器 → 浅拷贝）
    int* data;
    Buggy() : data(new int(42)) {}
    ~Buggy() { g_dtors = g_dtors + 1; }    // 观测型析构：真实版本此处会 delete data
};

struct Correct {                  // Rule of Three 对照：析构/拷贝构造/拷贝赋值三件套齐（深拷贝）
    int* data;
    Correct() : data(new int(42)) {}
    ~Correct() { g_dtors = g_dtors + 1; }  // 同为观测型析构（口径一致，唯一变量是拷贝语义）
    Correct(const Correct& o) : data(new int(*o.data)) {}
    Correct& operator=(const Correct& o) { *data = *o.data; return *this; }
};

int main() {
    long a0 = g_allocs, d0 = g_dtors;
    bool same_buggy = false;
    long allocs_buggy = 0, dtors_buggy = 0;
    {
        Buggy a;
        Buggy b = a;                       // 隐式拷贝 = 浅拷贝
        same_buggy = (b.data == a.data);
        allocs_buggy = g_allocs - a0;
    }                                      // a、b 各析构一次 → 同一块资源两次析构
    dtors_buggy = g_dtors - d0;

    bool same_correct = false;
    long allocs_correct = 0, dtors_correct = 0;
    {
        Correct c;
        Correct d = c;                     // 手写深拷贝
        same_correct = (d.data == c.data);
        allocs_correct = g_allocs - a0 - allocs_buggy;
        long dd0 = g_dtors;
        (void)dd0;
        // 作用域结束时 c、d 各析构一次（各自独享资源）
    }
    dtors_correct = g_dtors - d0 - dtors_buggy;

    std::cout << "buggy  : allocs=" << allocs_buggy << " same_ptr=" << (same_buggy ? 1 : 0)
              << " dtor_runs=" << dtors_buggy << " (one buffer, two dtors)\n";
    std::cout << "correct: allocs=" << allocs_correct << " same_ptr=" << (same_correct ? 1 : 0)
              << " dtor_runs=" << dtors_correct << " (two buffers, two dtors)\n";
    return 0;
}
