// sample_G079
// defect_type: use_after_free
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2017-11176 (https://nvd.nist.gov/vuln/detail/CVE-2017-11176) [linux-kernel]
// (authoritative annotation in sample_G079.json)
#include <cstdio>
// CVE-2017-11176 (用户态等价): mq_notify 重试路径未置空 sock → UAF
struct NetlinkSock {
    int fd;
    int state;
};

struct Notify {
    NetlinkSock* sock;   // 原始缺陷: 进入重试逻辑时未置 NULL
    bool retrying;
};

static void netlink_sock_close(Notify* n) {
    delete n->sock;      // 用户态 close: 释放 socket 对象
    std::printf("sock closed\n");
}

static void mq_notify_retry(Notify* n) {
    /* DEFECT */ if (n->sock->fd >= 0)        // sock 已释放仍解引用 → UAF
        n->sock->state = 1;
    std::printf("retry done, state=%d\n", n->sock->state);
}

int main() {
    Notify n{ new NetlinkSock{ 7, 0 }, true };
    netlink_sock_close(&n);    // 关闭 socket
    mq_notify_retry(&n);       // 重试路径仍使用已释放的 sock
    return 0;
}
