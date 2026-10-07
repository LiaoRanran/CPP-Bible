// RW-027 | CVE-2024-6387 | OpenSSH | defect_type: data_race
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2024-6387
// project_url: https://www.openssh.com/
// year: 2024 | severity: HIGH | source_type: cve
// mechanism: regreSSHion —— SIGALRM 处理器中调用非 async-signal-safe 的
//   syslog()（内部加锁），与主线程竞争导致内存破坏（远程未认证 RCE 面）。
// notes: 最小重构：用真实线程复现"信号处理器异步不安全调用"的竞争窗口。
//   TSan 应报 data race。
#include <cstdio>
#include <csignal>
#include <thread>
#include <atomic>
#include <cstring>

// Simplified syslog state: a lock + buffer shared with the "handler" path.
static char logbuf[64];
static std::atomic<int> log_writes{0};

void syslog_like(const char* msg) {          // not async-signal-safe (takes lock)
    std::strncpy(logbuf, msg, sizeof(logbuf) - 1);  // unsynchronized shared write
    log_writes.fetch_add(1, std::memory_order_relaxed);
}

extern "C" void alarm_handler(int) {
    syslog_like("timeout before auth");       // BUG: called from signal handler
}

int main() {
    // CVE-2024-6387 原机制用 SIGALRM（Linux 专属）；本 PoC 用 SIGINT 保持跨平台
    // （MinGW 无 SIGALRM），演示的缺陷本质（信号处理器中调用非 async-signal-safe 函数）不变。
    std::signal(SIGINT, alarm_handler);
    std::thread racer([] {
        for (int i = 0; i < 2000; ++i) {
            syslog_like("main path log line"); // concurrent unsynchronized access
        }
    });
    for (int i = 0; i < 2000; ++i) {
        std::raise(SIGINT);                    // drive the handler concurrently
    }
    racer.join();
    std::printf("log writes = %d, last = %.16s\n", log_writes.load(), logbuf);
    return 0;
}
