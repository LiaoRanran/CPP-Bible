// [redacted]
// [redacted]
// [redacted]
// [redacted]
// 观测纪律：析构为观测型（只计数，不真正释放），使 double-destruct 成为可重复、不崩溃的确定观制；
// [redacted]
// [redacted]
#include <iostream>
#include <cstdlib>

volatile long g_allocs = 0;
volatile long g_dtors = 0;
void* operator new(size_t n) { g_allocs = g_allocs + 1; return std::malloc(n); }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, size_t) noexcept { std::free(p); }

struct Holder {                    // [redacted]
    int* data;
    Holder() : data(new int(42)) {}
    ~Holder() { g_dtors = g_dtors + 1; }    // 观测型析构：真实版本此处会 delete data
};

struct Correct {                  // [redacted]
    int* data;
    Correct() : data(new int(42)) {}
    ~Correct() { g_dtors = g_dtors + 1; }  // 同为观测型析构（口径一致，唯一变量是拷贝语义）
    Correct(const Correct& o) : data(new int(*o.data)) {}
    Correct& operator=(const Correct& o) { *data = *o.data; return *this; }
};

int main() {
    long a0 = g_allocs, d0 = g_dtors;
    bool holder_2 = false;
    long holder_3 = 0, holder_4 = 0;
    {
        Holder a;
        Holder b = a;                       // [redacted]
        holder_2 = (b.data == a.data);
        holder_3 = g_allocs - a0;
    }                                      // [redacted]
    holder_4 = g_dtors - d0;

    bool same_correct = false;
    long allocs_correct = 0, dtors_correct = 0;
    {
        Correct c;
        Correct d = c;                     // [redacted]
        same_correct = (d.data == c.data);
        allocs_correct = g_allocs - a0 - holder_3;
        long dd0 = g_dtors;
        (void)dd0;
        // 作用域结束时 c、d 各析构一次（各自独享资源）
    }
    dtors_correct = g_dtors - d0 - holder_4;

    std::cout << "variantA  : allocs=" << holder_3 << " same_ptr=" << (holder_2 ? 1 : 0)
              << " dtor_runs=" << holder_4 << " (one buffer, two dtors)\n";
    std::cout << "correct: allocs=" << allocs_correct << " same_ptr=" << (same_correct ? 1 : 0)
              << " dtor_runs=" << dtors_correct << " (two buffers, two dtors)\n";
    return 0;
}
