// RW-070 | CVE-2023-34410 | Qt | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2023-34410
// project_url: https://www.qt.io/
// year: 2023 | severity: LOW | source_type: cve
// mechanism: QSslSocket/TLS 后端在特定配置下跳过主机名验证（策略判定错误），
//   接受本应拒绝的证书。
// notes: 最小重构（验证策略逻辑）。
#include <cstdio>
#include <string>

struct TlsConfig {
    bool verify_peer;          // user set "verify the peer"
    bool verify_hostname;      // ... but hostname flag left default-false
    std::string expected_host;
    std::string cert_host;
};

// BUG: treats verify_peer as implying hostname verification; the hostname flag
// default (false) silently disables the strongest check.
bool validate_peer(const TlsConfig& c) {
    if (!c.verify_peer) return true;                  // intentionally insecure (ok)
    if (c.verify_hostname) {
        return c.cert_host == c.expected_host;
    }
    // BUG: hostname not checked; any CA-signed cert for another host is accepted
    return true;
}

int main() {
    TlsConfig c{true, false, "bank.example", "attacker.example"};
    bool ok = validate_peer(c);
    std::printf("wrong-host cert accepted = %s\n", ok ? "YES (bug)" : "no");
    return 0;
}
