// RW-021 | CVE-2019-5482 | curl | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2019-5482
// project_url: https://curl.se/
// year: 2019 | severity: HIGH | source_type: cve
// mechanism: TFTP 协议栈处理对端 OACK/DATA 包时，块尺寸字段来自网络且未校验，
//   拷贝进固定栈缓冲时越界写。
// notes: 最小重构。ASan 应报 stack-buffer-overflow write。
#include <cstdint>
#include <cstdio>
#include <cstring>

struct TftpPacket {
    uint16_t opcode;
    uint16_t blksize_field;   // attacker-controlled: claims N bytes of payload
    const char* payload;      // actual payload pointer
};

// BUG: copies blksize_field bytes regardless of the real packet length.
size_t tftp_recv_into(const TftpPacket& pkt, char* buf512) {
    std::memset(buf512, 0, 512);
    std::memcpy(buf512, pkt.payload, pkt.blksize_field); // >512 -> overflow
    return pkt.blksize_field;
}

int main() {
    static char net_payload[700];
    std::memset(net_payload, 'D', sizeof(net_payload));
    TftpPacket pkt{3, 700, net_payload}; // DATA packet claiming 700 bytes
    char stack_buf[512];
    std::printf("recv %zu bytes\n", tftp_recv_into(pkt, stack_buf));
    return 0;
}
