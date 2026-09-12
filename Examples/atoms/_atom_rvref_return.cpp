// 版本边界：`return x;`（x 是 T&& 形参）在 C++11/14/17 与 C++20/23 下分别触发拷贝还是移动？
//
// 为什么单开一个夹具：红队指出"返回形参必须写 std::move"是**前 C++20** 的规则
// （P0527R1 提出、P1825R0 合并措辞把右值引用形参纳入 return 的隐式移动）。
// 与其凭印象写死，不如五档实测——能实测的不口头声称。
#include <cstdio>
#include <utility>

struct Probe {
    int id;
    static volatile int copies;
    static volatile int moves;
    explicit Probe(int i) : id(i) {}
    Probe(const Probe& o) : id(o.id) { copies = copies + 1; }
    Probe(Probe&& o) noexcept : id(o.id) { moves = moves + 1; }
};
volatile int Probe::copies = 0;
volatile int Probe::moves = 0;

// ① 直接返回具名右值引用形参
static Probe ret_plain(Probe&& x) { return x; }
// ② 显式 std::move
static Probe ret_moved(Probe&& x) { return std::move(x); }

int main() {
    Probe::copies = 0;
    Probe::moves = 0;
    { Probe a = ret_plain(Probe(1)); (void)a; }
    const int c1 = Probe::copies;
    const int m1 = Probe::moves;

    Probe::copies = 0;
    Probe::moves = 0;
    { Probe b = ret_moved(Probe(2)); (void)b; }
    const int c2 = Probe::copies;
    const int m2 = Probe::moves;

    printf("ret_plain copy=%d move=%d / ret_moved copy=%d move=%d\n", c1, m1, c2, m2);
    return 0;
}
