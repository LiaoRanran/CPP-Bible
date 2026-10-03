// sample_G084
// defect_type: race_condition
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// source: CVE-2016-5195 (https://nvd.nist.gov/vuln/detail/CVE-2016-5195) [linux-kernel]
// (authoritative annotation in sample_G084.json)
#include <cstdio>
#include <thread>
// CVE-2016-5195 (用户态等价): 写线程与 COW 失效线程竞争页状态
struct Page {
    bool readonly;      // 页状态(应由锁保护)
    int  content;
};

static Page g_page{ true, 0 };

static void attacker_write_thread() {
    for (int i = 0; i < 300000; ++i) {
        /* DEFECT */ // 原始缺陷: GUP 取到的页在写入前可被 COW 失效, 无一致性检查
        if (!g_page.readonly)
            g_page.content = 0x1337;    // 写"只读"映射
        else
            g_page.content = 1;
    }
}

static void cow_invalidate_thread() {
    for (int i = 0; i < 300000; ++i) {
        g_page.readonly = true;         // COW 失效: 置只读(与写线程竞争)
        g_page.readonly = false;
    }
}

int main() {
    std::thread a(attacker_write_thread);
    std::thread b(cow_invalidate_thread);
    a.join();
    b.join();
    std::printf("content=%d\n", g_page.content);
    return 0;
}
