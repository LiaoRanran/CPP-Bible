// RW-084 | CVE-2020-7457 | FreeBSD | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2020-7457
// project_url: https://www.freebsd.org/
// year: 2020 | severity: HIGH | source_type: cve
// mechanism: TCP 连接状态处理缺陷 —— connect() 对端在 SYN 窗口内的
//   状态迁移被错误接受（连接劫持/信息泄露面）。
// notes: 最小重构（TCP 状态机迁移判定）。
#include <cstdio>

enum TcpState { CLOSED, SYN_SENT, ESTABLISHED, FIN_WAIT };

struct Tcb {
    TcpState state;
    unsigned iss;      // initial send sequence
    bool from_known_peer;
};

// BUG: an in-window ACK during SYN_SENT transitions to ESTABLISHED without
// validating ack == iss+1 (off-by-one state acceptance).
bool on_segment(Tcb& tcb, unsigned ack, const char* src) {
    if (tcb.state == SYN_SENT) {
        // BUG: accepts ack in [iss, iss+2] instead of exactly iss+1
        if (ack >= tcb.iss && ack <= tcb.iss + 2) {
            tcb.state = ESTABLISHED;
            std::printf("accepted peer %s at ack=%u (iss=%u)\n", src, ack, tcb.iss);
            return true;
        }
    }
    return false;
}

int main() {
    Tcb tcb{SYN_SENT, 1000, false};
    bool ok = on_segment(tcb, 1002, "attacker");   // wrong ack accepted
    std::printf("hijacked state=%d\n", (int)tcb.state);
    return ok ? 0 : 0;
}
