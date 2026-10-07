// RW-009 | CVE-2015-1793 | OpenSSL | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2015-1793
// project_url: https://www.openssl.org/
// year: 2015 | severity: HIGH | source_type: cve
// mechanism: 证书链验证中"替代链"处理缺陷——中间 CA 用合法链进入信任判断后，
//   错误的回退让攻击者证书被接受（验证逻辑绕过，非内存错误）。
// notes: 最小重构。逻辑错误类：静态/告警资产通常全盲（真实盲区案例素材）。
#include <cstdio>
#include <string>
#include <vector>

struct Cert {
    std::string subject;
    std::string issuer;
    bool self_signed;
};

// Simplified chain walk. BUG: after a failed intermediate check the loop falls
// back to the *trusted pool by issuer name only*, skipping signature/policy checks.
bool verify_chain(const std::vector<Cert>& chain, const std::vector<Cert>& trusted) {
    if (chain.empty()) return false;
    for (const Cert& c : chain) {
        bool ok = false;
        for (const Cert& t : trusted) {
            if (c.issuer == t.subject) {
                ok = true; // BUG: name match only; no signature/policy verification here
                break;
            }
        }
        if (!ok && !c.self_signed) {
            // fallback intended for "alternative chain" — accepts too much
            for (const Cert& t : trusted) {
                if (t.subject.find(c.issuer) != std::string::npos) return true;
            }
            return false;
        }
    }
    return true;
}

int main() {
    std::vector<Cert> trusted = {{"Real Root CA", "Real Root CA", true}};
    std::vector<Cert> evil = {{"evil.com", "Real Root CA ", false}}; // note trailing space
    bool accepted = verify_chain(evil, trusted);
    std::printf("crafted chain accepted = %s\n", accepted ? "YES (bug)" : "no");
    return 0;
}
