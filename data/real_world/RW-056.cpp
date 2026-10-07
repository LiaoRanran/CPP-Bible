// RW-056 | CVE-2021-37975 | Chromium | defect_type: use_after_free
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-37975
// project_url: https://www.chromium.org/
// year: 2021 | severity: HIGH | source_type: cve
// mechanism: Blink 渲染树中某元素在动画/布局清理时被释放，异步任务仍持有引用
//   （释放后使用，在野利用 0-day）。
// notes: 最小重构。ASan 应报 heap-use-after-free。
#include <cstdio>
#include <deque>
#include <cstring>

struct LayoutNode {
    int id;
    char tag[16];
};

std::deque<LayoutNode*> g_async_tasks;    // pending microtasks hold node refs

void schedule_async_cleanup(LayoutNode* n) {
    g_async_tasks.push_back(n);           // async task captures the node ...
}

void detach_and_free(LayoutNode* n) {
    delete n;                             // ... element destroyed by style change
}

void run_microtasks() {
    for (LayoutNode* n : g_async_tasks) {
        std::strcpy(n->tag, "cleaned");   // use-after-free write
        std::printf("task touched node id=%d\n", n->id);
    }
    g_async_tasks.clear();
}

int main() {
    LayoutNode* node = new LayoutNode{42, {0}};
    std::strcpy(node->tag, "div");
    schedule_async_cleanup(node);
    detach_and_free(node);                // freed before the microtask runs
    run_microtasks();
    return 0;
}
