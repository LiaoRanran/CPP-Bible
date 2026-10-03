// sample_G029
// defect_type: heap_overread
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2018-16890 (https://nvd.nist.gov/vuln/detail/CVE-2018-16890) [curl]
// (authoritative annotation in sample_G029.json)
#include <cstdio>
#include <cstring>
#include <cstdint>
// CVE-2018-16890: ntlm_decode_type2_target 未校验 target 长度/偏移 → 堆越界读
static int ntlm_decode_type2_target(const unsigned char* buffer, size_t size) {
    unsigned short target_info_len = (unsigned short)(buffer[12] | (buffer[13] << 8));
    unsigned int   target_info_off = (unsigned int)(buffer[16] | (buffer[17] << 8));
    unsigned char  target[1024];
    /* DEFECT */ // 原始缺陷: 未检查 target_info_off + target_info_len <= size
    std::memcpy(target, buffer + target_info_off, target_info_len);
    return target[0];
}

int main() {
    // crafted NTLM type-2 消息: 32 字节, 声明 target_info_len=1000, offset=20
    unsigned char* msg = new unsigned char[32]();
    msg[12] = 0xE8; msg[13] = 0x03;    // len = 1000
    msg[16] = 20;                      // offset = 20
    std::printf("target[0]=%d\n", ntlm_decode_type2_target(msg, 32));   // 读 20..1020 → 越界
    delete[] msg;
    return 0;
}
