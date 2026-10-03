// sample_G083
// defect_type: race_condition
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// source: CVE-2017-2636 (https://nvd.nist.gov/vuln/detail/CVE-2017-2636) [linux-kernel]
// (authoritative annotation in sample_G083.json)
#include <cstdio>
#include <thread>
// CVE-2017-2636 (用户态等价): n_hdlc flip buffer 无锁竞争释放
struct HdlcBuf {
    bool busy;
    int  len;
};

static HdlcBuf* g_active = new HdlcBuf{ true, 128 };
static HdlcBuf* g_free_list = 0;

static void n_hdlc_flush(bool writer) {
    /* DEFECT */ // 原始缺陷: busy 标志的检查与释放无锁
    if (g_active->busy && writer) {
        HdlcBuf* b = g_active;
        g_active = 0;
        delete b;                          // 线程 A 释放
    } else if (g_active) {
        delete g_active;                   // 线程 B 也释放同一对象 → double free / UAF
        g_active = 0;
    }
}

int main() {
    std::thread a([]{ for (int i = 0; i < 100000; ++i) if (!g_active) g_active = new HdlcBuf{ true, 128 }; n_hdlc_flush(true); });
    std::thread b([]{ for (int i = 0; i < 100000; ++i) { if (g_active) n_hdlc_flush(false); } });
    a.join();
    b.join();
    std::printf("done\n");
    return 0;
}
