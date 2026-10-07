// RW-101 | CVE-2021-22946 | curl | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-22946
// project_url: https://curl.se/
// year: 2021 | severity: MEDIUM | source_type: cve
// mechanism: 协议降级允许 —— 服务器可强制 client 在 STARTTLS/加密逻辑前
//   切换到明文（信息泄露）。
// notes: 最小重构（协议状态判定）。
#include <cstdio>
#include <string>

struct ProtoSession {
    std::string proto;      // "imaps", "pop3s", ...
    bool tls_active;
    bool server_allows_downgrade;
};

// BUG: a "starttls not available" reply leaves the session running without TLS
// instead of aborting (downgrade attack).
bool ensure_tls(ProtoSession& s) {
    if (s.proto == "imaps") {
        s.tls_active = true;
        return true;
    }
    // Real shape: for plain protocols curl tries STARTTLS; if refused, some
    // paths continued *unencrypted* (CVE-2021-22946).
    if (!s.tls_active && s.server_allows_downgrade) {
        std::printf("server refused STARTTLS; continuing in cleartext (bug)\n");
        return true;         // BUG: should abort
    }
    s.tls_active = true;
    return true;
}

int main() {
    ProtoSession s{"imap", false, true};
    bool ok = ensure_tls(s);
    std::printf("session tls=%s (downgraded)\n", s.tls_active ? "on" : "OFF");
    return ok ? 0 : 0;
}
