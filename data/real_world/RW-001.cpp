// RW-001 | CVE-2014-0160 | OpenSSL | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2014-0160
// project_url: https://www.openssl.org/
// year: 2014 | severity: HIGH | source_type: cve
// mechanism: Heartbleed —— TLS heartbeat 响应长度取自攻击者声明的字段，
//   未与请求实际载荷长度校验，导致越界读取（信息泄露）。
// notes: 最小重构（source-derived，非原始项目代码）。ASan 应报 heap-buffer-overflow read。
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <vector>

struct HeartbeatRequest {
    uint16_t claimed_len;          // attacker-controlled: "echo this many bytes"
    std::vector<uint8_t> payload;  // actual payload received
};

// BUG: copies `claimed_len` bytes from the request instead of min(claimed_len, actual)
std::vector<uint8_t> build_heartbeat_response(const uint8_t* req_buf, size_t req_len) {
    uint16_t claimed = 0;
    std::memcpy(&claimed, req_buf, sizeof(claimed));  // payload_length field
    std::vector<uint8_t> resp(3 + claimed);
    resp[0] = 0x02;                                   // heartbeat response
    std::memcpy(&resp[1], &claimed, sizeof(claimed)); // echo claimed length
    std::memcpy(&resp[3], req_buf + 3, claimed);      // <-- OOB read when claimed > req_len - 3
    (void)req_len;
    return resp;
}

int main() {
    // Attacker sends 1-byte payload but claims 64 bytes ("heartbleed" primitive)
    uint8_t request[4] = {0x40, 0x00, 0x41};  // claimed_len = 0x0040 = 64, payload = "A"
    std::vector<uint8_t> resp = build_heartbeat_response(request, 4);
    std::printf("response size = %zu\n", resp.size());
    return 0;
}
