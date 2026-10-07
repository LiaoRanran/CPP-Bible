// RW-089 | CVE-2021-26708 | Linux kernel | defect_type: data_race
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-26708
// project_url: https://www.kernel.org/
// year: 2021 | severity: HIGH | source_type: pwn
// mechanism: vsock 传输层多线程竞态（Virtio）—— 一个线程释放 vsk 结构时另一
//   线程仍在写其字段（释放后使用 + 数据竞争，CTF 提权常用原型）。
// notes: 最小重构 —— **用户态线程复刻**（不调用内核 vsock）。
#include <cstdio>
#include <thread>
#include <vector>
#include <cstring>

struct VskTransport {
    int state;
    char queue[32];
    bool released;
};

std::vector<VskTransport*> g_loop;   // transport list walked by "loopback" path

void loopback_thread(VskTransport* v) {
    for (int i = 0; i < 100000; ++i) {
        if (!v->released) {
            v->state += 1;                 // concurrent write vs. free below
            std::strcpy(v->queue, "loopback");
        }
    }
}

void release_thread(VskTransport* v) {
    // frees the transport while the loopback path may still write state
    v->released = true;
    delete v;                              // racing delete
}

int main() {
    VskTransport* v = new VskTransport{0, {0}, false};
    g_loop.push_back(v);
    std::thread t1(loopback_thread, v);
    std::thread t2(release_thread, v);
    t2.join();
    t1.join();                             // loopback may touch freed memory
    std::printf("vsock transport race exercised\n");
    return 0;
}
