// [redacted]
//
// 三个场景（每个都用 volatile 析构计数这个确定性信号量出来）：
//   scoped  —— 局部对象，正常析构                     ⇒ 对照组，析构数 = 1
// [redacted]
//   owned   —— 堆对象被**全局容器**持有（有意为之）    ⇒ 析构数 = 0，但语义与 cycle **完全不同**
//
// [redacted]
// [redacted]
// [redacted]
// 本夹具因此对 contrast 类 claim 提供一手观测：**同一个"析构=0"信号，在工具侧有不同去向**，
// [redacted]
//
// 输出纪律：默认只打印**确定性**读数；不重载 operator new/delete。
#include <cstdio>
#include <memory>
#include <vector>

namespace {
volatile int g_scoped_dtor = 0;
volatile int g_cycle_dtor  = 0;
volatile int g_owned_dtor  = 0;
// 红队 H2 修复：**构造计数** —— 证明"分配真的发生了"，把
// [redacted]
//   （仓内实测：同一夹具的 Scoped 构造在 -O2 下已被整体消除，只剩计数器自增）。
volatile int g_cycle_ctor  = 0;

struct Scoped {
    int id = 0;
    ~Scoped() { g_scoped_dtor = g_scoped_dtor + 1; }
};
struct Node {                                   // 循环引用用的节点
    std::shared_ptr<Node> next;
    Node() { g_cycle_ctor = g_cycle_ctor + 1; }   // H2：构造计数（证明分配真发生）
    ~Node() { g_cycle_dtor = g_cycle_dtor + 1; }
};
struct Owned {
    int id = 0;
    ~Owned() { g_owned_dtor = g_owned_dtor + 1; }
};

std::vector<std::shared_ptr<Owned>>& registry() {   // 全局注册表（进程级持有）
    static std::vector<std::shared_ptr<Owned>> r;
    return r;
}

__attribute__((noinline)) void run_scoped() { Scoped s{1}; (void)s; }

__attribute__((noinline)) void run_cycle() {
    auto a = std::make_shared<Node>();
    auto b = std::make_shared<Node>();
    a->next = b;                                 // a → b
    b->next = a;                                 // b → a ⇒ 引用计数闭环，两个对象都不可达但计数非零
}

__attribute__((noinline)) void run_owned() {
    registry().push_back(std::make_shared<Owned>());   // 全局持有 ⇒ 退出时仍可达
}
}  // namespace

int main() {
    run_scoped();
    run_cycle();
    run_owned();

    std::printf("scoped_dtor_count=%d\n", static_cast<int>(g_scoped_dtor));
    std::printf("cycle_dtor_count=%d\n", static_cast<int>(g_cycle_dtor));
    std::printf("owned_dtor_count=%d\n", static_cast<int>(g_owned_dtor));
    std::printf("owned_registry_size=%zu\n", registry().size());
    // [redacted]
    //   **一 bit 两计**；现改为两条**不同计算**的独立指标：
    //   ① `cycle_allocated`（构造计数，兼作 H2 的"分配真发生"证据）
    //   ② `cycle_live_objects`（构造 − 析构 = 未回收对象数）
    // [redacted]
    std::printf("scoped_is_clean=%d\n", g_scoped_dtor == 1 ? 1 : 0);
    std::printf("cycle_allocated=%d\n", static_cast<int>(g_cycle_ctor));
    std::printf("cycle_destroyed=%d\n", static_cast<int>(g_cycle_dtor));
    std::printf("cycle_live_objects=%d\n", static_cast<int>(g_cycle_ctor - g_cycle_dtor));
    return 0;
}
