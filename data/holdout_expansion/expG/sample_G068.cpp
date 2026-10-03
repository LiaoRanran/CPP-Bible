// sample_G068
// defect_type: info_leak
// severity: high
// planted: false
// expected_verdict: miss
// expected_detectors: asan
// source: CVE-2016-0777 (https://nvd.nist.gov/vuln/detail/CVE-2016-0777) [openssh]
// (authoritative annotation in sample_G068.json)
#include <cstdio>
#include <cstring>
// CVE-2016-0777: resend_bytes 重传整个缓冲区 → 泄露已确认部分(含私钥残留)
static const size_t SEND_BUF = 64;

static void resend_bytes(const unsigned char* buf, size_t confirmed_offset) {
    // 原始缺陷: 应从 buf+confirmed_offset 只发剩余字节
    /* DEFECT */ size_t resend_len = SEND_BUF;          // 发送了整个缓冲区
    std::printf("resend: 发送 %zu 字节 (confirmed_offset=%zu, 应仅发送 %zu 字节)\n",
                resend_len, confirmed_offset, SEND_BUF - confirmed_offset);
    // 缓冲内 [0, confirmed_offset) 为已确认历史数据 —— 含此前写入的私钥残留
}

int main() {
    unsigned char send_buf[SEND_BUF];
    std::memcpy(send_buf, "-----BEGIN OPENSSH PRIVATE KEY-----", 35);   // 模拟私钥残留(恰为字面量长度)
    resend_bytes(send_buf, 48);   // 恶意 roaming 服务器请求重传
    std::printf("(正确行为: 只重传 offset 之后的 16 字节)\n");
    return 0;
}
