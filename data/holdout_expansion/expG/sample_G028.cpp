// sample_G028
// defect_type: integer_overflow
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: ubsan
// source: CVE-2017-8816 (https://nvd.nist.gov/vuln/detail/CVE-2017-8816) [curl]
// (authoritative annotation in sample_G028.json)
#include <cstdio>
// CVE-2017-8816: NTLM 长度按 int 累加(32 位平台) → 溢出
static int ntlm_encode_size(int userlen, int domlen, int passwdlen) {
    /* DEFECT */ int total = 2 * (userlen + domlen + passwdlen) + 64;   // int 溢出
    return total;
}

int main() {
    // crafted: 超长用户名/域/密码(各 2^29), 运行时变量绕过常量折叠
    volatile int ul = 0x20000000, dl = 0x20000000, pl = 0x20000000;
    int total = ntlm_encode_size(ul, dl, pl);
    std::printf("ntlm total=%d (应为 %lld)\n", total, 2LL * (ul + dl + pl) + 64);
    return 0;
}
