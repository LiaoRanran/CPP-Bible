// sample_G014
// defect_type: heap_overread
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2017-3731 (https://nvd.nist.gov/vuln/detail/CVE-2017-3731) [openssl]
// (authoritative annotation in sample_G014.json)
#include <cstdio>
#include <cstring>
#include <cstdint>
// CVE-2017-3731: 截断 AEAD 包 → tag 指针计算越过缓冲区起点 → 前向越界读
static const size_t TAG_LEN = 16;

static int aead_decrypt(const unsigned char* in, size_t len, unsigned char* out) {
    // 原始缺陷: 在校验 len >= TAG_LEN 之前就计算 tag 位置
    /* DEFECT */ const unsigned char* tag = in + len - TAG_LEN;
    for (size_t i = 0; i < TAG_LEN; ++i)
        out[i] = (unsigned char)(in[i] ^ tag[i]);   // len=5 时读 in[-11..] → 越界
    return 0;
}

int main() {
    unsigned char* truncated = new unsigned char[5]{ 0x17, 0x03, 0x03, 0x00, 0x01 };
    unsigned char out[32];
    std::memset(out, 0, sizeof(out));
    aead_decrypt(truncated, 5, out);
    std::printf("decrypt done, out[0]=%02x\n", out[0]);
    delete[] truncated;
    return 0;
}
