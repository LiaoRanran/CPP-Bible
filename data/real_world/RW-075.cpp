// RW-075 | CVE-2016-5195 | Linux kernel | defect_type: data_race
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2016-5195
// project_url: https://www.kernel.org/
// year: 2016 | severity: HIGH | source_type: cve
// mechanism: Dirty COW —— get_user_pages 与 COW 断链（FOLL_WRITE 重试）之间的
//   竞态使只读映射的私有副本被写穿。
// notes: 最小重构 —— **纯用户态线程竞态复刻**（不调用内核）。TSan 应报 data race。
#include <cstdio>
#include <thread>
#include <atomic>

struct CowPage {
    std::atomic<int> refcount{2};   // shared by "mapping" and "page cache"
    char content[32];
    bool private_copy_made{false};
};

// Writer thread: writes through the private mapping.
void writer_thread(CowPage* p) {
    for (int i = 0; i < 100000; ++i) {
        if (!p->private_copy_made) {
            p->content[0] = 'W';    // races with the COW break decision below
        }
    }
}

// Fault handler thread: decides whether to break COW (the TOCTOU window).
void fault_handler_thread(CowPage* p) {
    for (int i = 0; i < 100000; ++i) {
        // racy check-then-act: refcount drop observed, COW "not needed"
        if (p->refcount.load() < 2) {
            p->private_copy_made = false;   // write-through path enabled
        } else {
            p->private_copy_made = true;
        }
    }
}

int main() {
    CowPage page{};
    std::thread w(writer_thread, &page);
    std::thread f(fault_handler_thread, &page);
    w.join();
    f.join();
    std::printf("dirty COW race window exercised\n");
    return 0;
}
