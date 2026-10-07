// RW-092 | CVE-2022-26691 | CUPS | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2022-26691
// project_url: https://openprinting.github.io/cups/
// year: 2022 | severity: MEDIUM | source_type: cve
// mechanism: 认证字符串比较使用非常量时间/前缀宽松匹配，本地攻击者可绕过
//   （证书比较逻辑缺陷）。
// notes: 最小重构（比较逻辑缺陷）。
#include <cstdio>
#include <string>

// BUG: compare stops at the first NUL of *either* operand and uses the length
// of the attacker-controlled input -> "abc" matches "abc\0suffix".
bool insecure_cert_compare(const std::string& expected, const std::string& given) {
    if (given.size() > expected.size()) return false;
    for (size_t i = 0; i < given.size(); ++i) {
        if (i >= expected.size()) return true;      // early-accept prefix
        if (expected[i] != given[i]) return false;
    }
    return true;                                    // given is a prefix of expected
}

int main() {
    std::string expected = "CN=admin,O=example";
    std::string given = "CN=";                      // attacker presents a prefix
    bool ok = insecure_cert_compare(expected, given);
    std::printf("prefix-only cert accepted = %s (bug)\n", ok ? "YES" : "no");
    return 0;
}
