// 具名右值引用是左值：同一个形参 x，直接初始化走拷贝，std::move(x) 才走移动。
// 证伪对照：若"形参是 T&& 就会自动移动"成立，两组计数应相同；实测不同即推翻。
#include <cstdio>
#include <utility>

// 🔴 计数器必须 **volatile**：-O2 下若用普通 static int，编译器能静态推出两组结果
//    并把计数常量折叠成立即数——输出"看起来完全正确"，但运行时**一次构造都没发生**
//    （零观测伪证据）。这是本项目第三次踩同一形态（EV-MEM-002 初版、本卡初版），
//    规则见 M2 §5：计数类实验计数器必须 volatile、-O0 与 -O2 双跑。
// 🔴 自增写成 `x = x + 1` 而非 `++x`：C++20 起 volatile 的复合赋值已弃用。
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

// ① 形参是具名右值引用；函数体内 x 是**左值**（有名字、可取地址）
static void sink_as_is(Probe&& x) { Probe local = x; (void)local; }
// ② 显式 std::move(x) 把 x 转回 xvalue，才选中移动构造
static void sink_moved(Probe&& x) { Probe local = std::move(x); (void)local; }

int main() {
    Probe::copies = 0;
    Probe::moves = 0;
    sink_as_is(Probe(1));
    const int c1 = Probe::copies;
    const int m1 = Probe::moves;

    Probe::copies = 0;
    Probe::moves = 0;
    sink_moved(Probe(2));
    const int c2 = Probe::copies;
    const int m2 = Probe::moves;

    // 一行输出（复算契约：一条 command 的 stdout ↔ 一组 run_*）。
    // 分隔符用 `/` 而**不用 `|`**：`|` 在证据卡里是字段/行分隔符，会让 expected 被切成两行
    // → refute:run_mismatch（B 样板踩过，2026-09-10 G5 又踩一次，记住）。
    printf("as_is copy=%d move=%d / moved copy=%d move=%d\n", c1, m1, c2, m2);
    return 0;
}
