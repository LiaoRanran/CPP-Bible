// Examples/_atom_leak_two_node.cpp
// 服务 ATOM-MEM-LEAK-001（检测侧标定）：**极简两节点环**——用来标定"LSan 在什么结构上能报泄漏"。
// 与 _atom_leak_tree_bug.cpp（树形三节点 + vector 子节点 + 导航边）的差别只有**结构复杂度**，
// 两者构成"同一类泄漏、不同结构 → 检测结果不同"的标定对。
// 预期：LSan 报 Indirect/Direct leak；若本夹具也不报，则"LSan 漏报"的结论要改为"本环境整体不报"。
#include <cstddef>
#include <cstdio>
#include <memory>

struct Link {
    std::shared_ptr<Link> next;          // 唯一的边：互指成环
    int tag = 0;
};

__attribute__((noinline)) static void build_cycle() {
    auto a = std::make_shared<Link>();
    auto b = std::make_shared<Link>();
    a->tag = 1;
    b->tag = 2;
    a->next = b;
    b->next = a;                         // 环
}

__attribute__((noinline)) static void scrub_stack() {
    volatile unsigned char buf[8192];
    for (std::size_t i = 0; i < sizeof(buf); ++i) {
        buf[i] = 0;
    }
}

int main() {
    build_cycle();
    scrub_stack();
    std::printf("two-node cycle built, blocks=2\n");
    return 0;                            // 泄漏时仍正常退出
}
