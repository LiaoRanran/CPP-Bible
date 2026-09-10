// 受控实验 ATOM-MEM-MOVE（反例导向）：移动的收益来自"掏空源对象"——没有间接资源可掏时，
// 移动退化为拷贝，且源对象分毫未动。
//
// 控制变量：同一 TU、同一编译器、同一 -O2；唯一变量 = 被移动类型是否持有**间接资源**。
//   ① HeapBuf   —— 持堆指针：移动 = 指针转移（掏空源），分配 0 次（拷贝 1 次）
//   ② FixedBuf  —— 纯值成员（std::array<int,8>）：无间接资源，移动 = 逐元素拷贝，源**未被掏空**
//   ③ std::array<int,8> —— 标准库纯值类型：同上（标准明文：移动构造对元素逐个 move，int 即拷贝）
//
// 证伪条件：若 ① 的移动也产生分配（对照 BadHeapBuf），说明计数没接上，实验作废；
//           若 ②③ 显示"源被掏空"，说明我把结论写反了，实验作废。
//
// 复现：
//   g++ -std=c++23 -O2 Examples/_atom_move_no_gain.cpp -o build/_replay_nogain.exe && build/_replay_nogain.exe
//   g++ -std=c++23 -O2 -S -masm=intel Examples/_atom_move_no_gain.cpp -o Examples/_atom_move_no_gain.asm

#include <array>
#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <utility>

// volatile 必需（同 _atom_move_alloc.cpp 的教训）：计数是"运行时事实"，-O2 能把它折叠成常量。
static volatile long g_allocs = 0;

void* operator new(std::size_t n) {
    g_allocs = g_allocs + 1;
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

// ① 持间接资源：移动可以把源"掏空"，因此有收益
struct HeapBuf {
    int* p = nullptr;
    explicit HeapBuf(std::size_t n) : p(new int[n]) { p[0] = 42; }
    ~HeapBuf() { delete[] p; }
    HeapBuf(const HeapBuf& o) : p(new int[8]) { p[0] = o.p ? o.p[0] : 0; }   // 拷贝：再分配一次
    HeapBuf(HeapBuf&& o) noexcept : p(o.p) { o.p = nullptr; }               // 移动：偷指针
};

// ② 纯值成员：没有可掏空的间接资源，编译器生成的移动构造 = 逐元素 move（int 即拷贝）
struct FixedBuf {
    std::array<int, 8> v{};
    explicit FixedBuf(int s) { for (int& x : v) x = s; }
};

// 反常量折叠（第一版踩坑留痕）：初版把内容写成编译期常量（42），-O2 直接把三组的构造、
// 移动、读回**整体消除**——main 里没有任何 8-int 搬运指令，"源完好=是" 是编译期常量，
// 属于零观测的伪证据（与 _atom_move_alloc.cpp 的折叠坑同型）。对策双管齐下：
//   ① 初值改由 argc 派生（运行时值，不可常量折叠）；
//   ② 移动后用 **volatile 指针**读回源内容——volatile 访问是标准明文的可观测行为，
//      编译器必须真实发射读指令，比较结果不可静态推定。
int main(int argc, char**) {
    const int seed = argc * 7 + 1;           // 运行时初值
    long heap_copy = 0, heap_move = 0;
    long fix_copy = 0, fix_move = 0;
    long arr_copy = 0, arr_move = 0;
    int heap_src_emptied = 0, fix_src_intact = 0, arr_src_intact = 0;

    {
        HeapBuf a(8);
        g_allocs = 0;
        HeapBuf b = a;                       // 拷贝构造
        heap_copy = g_allocs;

        g_allocs = 0;
        HeapBuf c = std::move(a);            // 移动构造
        heap_move = g_allocs;
        int* volatile ps = a.p;              // volatile 读：强制真实取值
        heap_src_emptied = (ps == nullptr) ? 1 : 0;
        (void)b; (void)c;
    }
    {
        FixedBuf a(seed);
        g_allocs = 0;
        FixedBuf b = a;
        fix_copy = g_allocs;

        g_allocs = 0;
        FixedBuf c = std::move(a);
        fix_move = g_allocs;
        int* volatile pf = &a.v[0];          // volatile 读回源内容
        fix_src_intact = (*pf == seed) ? 1 : 0;
        (void)b; (void)c;
    }
    {
        std::array<int, 8> a{};
        for (int& x : a) x = seed;
        g_allocs = 0;
        std::array<int, 8> b = a;
        arr_copy = g_allocs;

        g_allocs = 0;
        std::array<int, 8> c = std::move(a);
        arr_move = g_allocs;
        int* volatile pa = &a[0];
        arr_src_intact = (*pa == seed) ? 1 : 0;
        (void)b; (void)c;
    }

    std::printf("HeapBuf  拷贝分配=%ld 移动分配=%ld 移动后源被掏空=%s\n",
                heap_copy, heap_move, heap_src_emptied ? "是" : "否");
    std::printf("FixedBuf 拷贝分配=%ld 移动分配=%ld 移动后源完好=%s\n",
                fix_copy, fix_move, fix_src_intact ? "是" : "否");
    std::printf("array    拷贝分配=%ld 移动分配=%ld 移动后源完好=%s\n",
                arr_copy, arr_move, arr_src_intact ? "是" : "否");
    //@ HeapBuf  拷贝分配=1 移动分配=0 移动后源被掏空=是
    //@ FixedBuf 拷贝分配=0 移动分配=0 移动后源完好=是
    //@ array    拷贝分配=0 移动分配=0 移动后源完好=是
    return 0;
}
