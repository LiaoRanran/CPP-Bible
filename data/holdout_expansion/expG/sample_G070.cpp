// sample_G070
// defect_type: stack_overflow_write
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2015-7547 (https://nvd.nist.gov/vuln/detail/CVE-2015-7547) [glibc]
// (authoritative annotation in sample_G070.json)
#include <cstdio>
#include <cstring>
// CVE-2015-7547: send_dg 接收 crafted DNS 响应 → 栈缓冲溢出
static void send_dg(const unsigned char* response, size_t response_len) {
    unsigned char ans[512];       // 栈上接收缓冲
    /* DEFECT */ // 原始缺陷: 响应长度攻击者可控, 未按 anssiz 截断
    std::memcpy(ans, response, response_len);
    std::printf("dns answer: %02x %02x (len=%zu)\n", ans[0], ans[1], response_len);
}

int main() {
    // 恶意 DNS 服务器返回 2048 字节响应
    unsigned char* crafted = new unsigned char[2048];
    std::memset(crafted, 0x5A, 2048);
    send_dg(crafted, 2048);
    delete[] crafted;
    return 0;
}
