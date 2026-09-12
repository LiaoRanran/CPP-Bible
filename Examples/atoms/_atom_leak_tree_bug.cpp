// Examples/_atom_leak_tree_bug.cpp
// 服务 ATOM-MEM-LEAK-001（对照的**缺陷侧**）：与 _atom_leak_tree_ok.cpp 同一棵树，
// **唯一变量 = parent 的引用强度**（shared 而非 weak）⇒ root ↔ child 互相强引用成环，
// 整棵树（3 节点）在构树函数返回后一个都不析构（泄漏）。
// 本夹具的泄漏是**有意演示**：ASan/LSan 命中属于预期内反向证据（卡内声明 expected_sanitizer: [leak]）。
// 构树移到**独立函数**并随后擦洗栈帧：否则构树栈槽里残留的裸指针会让 LSan 把泄漏对象判为"仍可达"
// 而**不报**（实测踩坑：同结构写在 main 作用域内时 LSan 静默；移到独立函数 + 擦栈后才稳定报 leak）。
#include <cstddef>
#include <cstdio>
#include <memory>
#include <vector>

static volatile int g_constructed = 0;
static volatile int g_destroyed = 0;

struct Node {
    int id = 0;
    std::vector<std::shared_ptr<Node>> children;
    std::shared_ptr<Node> parent;                  // ← 唯一变量：强引用，与子节点成环
    explicit Node(int i) : id(i) { g_constructed = g_constructed + 1; }
    ~Node() { g_destroyed = g_destroyed + 1; }
};

// noinline + 独立函数：让"构树栈帧"在返回后真正失效，泄漏对象对 LSan 才可能不可达
// （红队实证：不加 noinline 时 -O2 会把本函数整体内联进 main，堆指针留在 callee-saved 寄存器里，
//   LSan 判其可达 ⇒ 不是"LSan 漏报"，而是"隔离没做成"。三种隔离档的实测见 EV-MEM-037 边界说明）
__attribute__((noinline)) static void build_tree() {
    auto root = std::make_shared<Node>(1);
    for (int i = 2; i <= 3; ++i) {
        auto child = std::make_shared<Node>(i);
        child->parent = root;                      // 强引用：成环
        root->children.push_back(child);
    }
    std::printf("root children=%d\n", (int)root->children.size());
    std::printf("root use_count=%ld\n", (long)root.use_count());
}

// 用全新栈帧覆盖上一步的残留指针，使堆上的环对 LSan 真正"不可达"
static void scrub_stack() {
    volatile unsigned char buf[8192];
    for (std::size_t i = 0; i < sizeof(buf); ++i) {
        buf[i] = 0;
    }
}

int main() {
    build_tree();
    scrub_stack();
    std::printf("constructed=%d\n", (int)g_constructed);
    std::printf("destroyed after scope=%d\n", (int)g_destroyed);
    return 0;                                      // 注意：泄漏时程序仍**正常退出**
}
