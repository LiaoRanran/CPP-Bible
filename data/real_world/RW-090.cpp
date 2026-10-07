// RW-090 | CVE-2016-8655 | Linux kernel | defect_type: data_race
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2016-8655
// project_url: https://www.kernel.org/
// year: 2016 | severity: HIGH | source_type: pwn
// mechanism: AF_PACKET 的 setsockopt(PACKET_RX_RING) 与 packet_set_ring 之间的
//   竞态：TPACKET_V3 环形缓冲重配置时释放后使用（本地提权，chocobo1 原型）。
// notes: 最小重构 —— **用户态线程复刻**环形缓冲重配置竞态。
#include <cstdio>
#include <cstdlib>
#include <thread>
#include <atomic>

struct RxRing {
    void* blocks;
    unsigned block_nr;
    std::atomic<bool> closing;
};

void setsockopt_enable_rx_ring(RxRing* r) {
    // re-configures the ring while another thread closes it
    for (int i = 0; i < 100000; ++i) {
        if (!r->closing.load()) {
            r->block_nr = 128;                 // rewrite config raced with close
        }
    }
}

void close_ring(RxRing* r) {
    r->closing.store(true);
    void* blocks = r->blocks;
    r->blocks = nullptr;
    free(blocks);                              // frees while config path rewrites
}

int main() {
    RxRing ring{};
    ring.blocks = malloc(4096);
    ring.block_nr = 64;
    ring.closing = false;
    std::thread t1(setsockopt_enable_rx_ring, &ring);
    std::thread t2(close_ring, &ring);
    t1.join();
    t2.join();
    std::printf("rx ring reconfigure race exercised\n");
    return 0;
}
