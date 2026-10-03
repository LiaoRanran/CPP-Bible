// sample_G001
// defect_type: heap_overread
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2014-0160 (https://nvd.nist.gov/vuln/detail/CVE-2014-0160) [openssl]
// (authoritative annotation in sample_G001.json)
#include <cstdio>
#include <cstring>
#include <cstdint>
// CVE-2014-0160 (Heartbleed): 未校验 payload_length 与实际请求缓冲区大小 → 堆越界读
struct HeartbeatRequest {
    uint8_t  type;         // 1 = heartbeat_request
    uint16_t payload_len;  // 声明的载荷长度
    // 载荷紧随其后（本样本实际仅 1 字节）
};

static void tls1_process_heartbeat(const uint8_t* p, size_t n) {
    if (n < 4) { std::printf("packet too small\n"); return; }
    uint16_t payload_len = (uint16_t)((p[1] << 8) | p[2]);

    uint8_t* response = new uint8_t[3 + payload_len];
    response[0] = 2;                      // heartbeat_response
    response[1] = p[1];
    response[2] = p[2];
    /* DEFECT */ std::memcpy(response + 3, p + 3, payload_len);  // 声明 65535, 实际仅 1 字节 → 堆越界读
    std::printf("hb: echo %u bytes, first=%02x\n", (unsigned)payload_len, response[3]);
    delete[] response;
}

int main() {
    // 硬编码恶意心跳请求: type=1, length=0xFFFF, 载荷实际只有 'A'
    uint8_t* req = new uint8_t[4]{ 1, 0xFF, 0xFF, 'A' };
    tls1_process_heartbeat(req, 4);
    delete[] req;
    return 0;
}
