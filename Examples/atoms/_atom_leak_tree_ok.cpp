// Examples/_atom_leak_tree_ok.cpp
// 服务 ATOM-MEM-LEAK-001（对照的**正确侧**）：树形结构的 owner/observer 模式——
// 父节点用 shared_ptr 拥有子节点（下行强引用），子节点只持 weak_ptr 指向父（上行导航，不拥有）。
// 所有权单向下行、反向导航不延长寿命 ⇒ 整棵树在构树函数返回时正常析构。
// 与 _atom_leak_tree_bug.cpp 的唯一变量 = parent 的引用强度（weak vs shared）；
// 两者的结构（独立函数构树 + 栈擦洗）逐行对齐，避免结构差异污染对照。
// 检测手段两条腿：① 手动析构计数（运行层，确定、本机可复算）；② ASan/LSan（WSL/Linux 侧，
// 本场景应**零报错**——与缺陷侧的 leak 报告构成检测灵敏度对照）。
#include <cstddef>
#include <cstdio>
#include <memory>
#include <vector>

static volatile int g_constructed = 0;
static volatile int g_destroyed = 0;

struct Node {
    int id = 0;
    std::vector<std::shared_ptr<Node>> children;   // 下行：强引用（拥有）
    std::weak_ptr<Node> parent;                    // 上行：弱引用（导航，不拥有）
    explicit Node(int i) : id(i) { g_constructed = g_constructed + 1; }
    ~Node() { g_destroyed = g_destroyed + 1; }
};

// noinline：与缺陷侧逐行对齐（唯一变量仍只有 parent 的引用强度）
__attribute__((noinline)) static void build_tree() {
    auto root = std::make_shared<Node>(1);
    for (int i = 2; i <= 3; ++i) {
        auto child = std::make_shared<Node>(i);
        child->parent = root;                      // 弱引用：不成环
        root->children.push_back(child);
    }
    std::printf("root children=%d\n", (int)root->children.size());
    auto up = root->children[0]->parent.lock();    // 反向导航可用
    std::printf("parent reachable=%d\n", (int)(up != nullptr));
}

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
    return 0;
}
