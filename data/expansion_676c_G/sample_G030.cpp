// sample_G030
// defect_type: heap_overflow
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2019-5436 (https://nvd.nist.gov/vuln/detail/CVE-2019-5436) [curl]
// (authoritative annotation in sample_G030.json)
#include <cstdio>
#include <cstring>
#include <cstdint>
// CVE-2019-5436: TFTP 接收 blksize 大于接收缓冲 → 堆越界写
static const size_t TFTP_RECV_BUF = 512;

static void tftp_receive_packet(const unsigned char* pkt, size_t pktlen) {
    // pkt: [opcode(2)][blksize 选项值(2)][数据...]
    unsigned short blksize = (unsigned short)((pkt[2] << 8) | pkt[3]);   // 服务器可任意声明
    unsigned char* rbuf = new unsigned char[TFTP_RECV_BUF];
    /* DEFECT */ std::memcpy(rbuf, pkt + 4, blksize);   // blksize=1024 > 512 → 越界写
    std::printf("tftp received blksize=%u\n", blksize);
    delete[] rbuf;
}

int main() {
    // crafted 服务器响应: blksize 选项 = 1024, 数据足够长
    unsigned char* pkt = new unsigned char[1032]();
    pkt[2] = 0x04; pkt[3] = 0x00;      // blksize = 1024
    std::memset(pkt + 4, 'D', 1028);
    tftp_receive_packet(pkt, 1032);
    delete[] pkt;
    return 0;
}
