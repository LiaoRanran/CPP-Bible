// RW-013 | CVE-2021-33574 | glibc | defect_type: use_after_free
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-33574
// project_url: https://www.gnu.org/software/libc/
// year: 2021 | severity: HIGH | source_type: cve
// mechanism: mq_notify 通知线程结束后，通知注册结构在注销路径被再次访问（释放后使用）。
// notes: 最小重构（用户态消息队列通知模型）。ASan 应报 heap-use-after-free。
#include <cstdio>
#include <cstring>
#include <thread>
#include <vector>

struct NotifyReg {
    int mqdes;
    char payload[24];
    bool freed;
};

// BUG: worker frees the registration after delivering, but the cleanup path
// (run at thread join) touches the freed pointer again.
void notify_worker(NotifyReg* reg) {
    std::memcpy(reg->payload, "notification", 12);
    delete reg;                          // freed on delivery
}

int main() {
    NotifyReg* reg = new NotifyReg{7, {}, false};
    std::thread t(notify_worker, reg);
    t.join();
    reg->freed = true;                   // use-after-free: touches freed memory
    std::printf("cleanup touched reg->mqdes=%d\n", reg->mqdes);
    return 0;
}
