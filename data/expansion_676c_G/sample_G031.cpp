// sample_G031
// defect_type: heap_overflow
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2023-38545 (https://nvd.nist.gov/vuln/detail/CVE-2023-38545) [curl]
// (authoritative annotation in sample_G031.json)
#include <cstdio>
#include <cstring>
#include <string>
// CVE-2023-38545: SOCKS5 握手把超长主机名整段拷贝进固定缓冲 → 堆越界写
static const size_t SOCKS5_REQ_MAX = 16 * 1024;   // 请求缓冲上限

static void socks5_send_hostname(const std::string& host) {
    unsigned char* req = new unsigned char[SOCKS5_REQ_MAX + 8]();
    req[0] = 5; req[1] = 1; req[2] = 0; req[3] = 3;   // VER/CMD/RSV/ATYP=domain
    size_t hlen = host.size();                        // 20000
    /* DEFECT */ // 原始缺陷: 慢速路径未检查 hlen 是否超过缓冲容量即整段拷贝
    std::memcpy(req + 5, host.c_str(), hlen);
    std::printf("socks5 req sent, host_len=%zu\n", hlen);
    delete[] req;
}

int main() {
    socks5_send_hostname(std::string(20000, 'h'));   // 超长主机名
    return 0;
}
