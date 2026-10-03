// sample_G087
// defect_type: logic_error
// severity: medium
// planted: false
// expected_verdict: miss
// expected_detectors: ubsan
// source: CVE-2022-2097 (https://nvd.nist.gov/vuln/detail/CVE-2022-2097) [openssl]
// (authoritative annotation in sample_G087.json)
#include <cstdio>
#include <cstring>
#include <cstdint>
// CVE-2022-2097: OCB 加密对非完整块尾部未加密
static const size_t BLK = 16;

static void evp_ocb_encrypt(const unsigned char* in, unsigned char* out, size_t len) {
    size_t full = len - (len % BLK);
    for (size_t i = 0; i < full; ++i)
        out[i] = (unsigned char)(in[i] ^ 0x5A);    // 逐块加密(简化)
    /* DEFECT */ // 原始缺陷: 尾部不完整块被跳过, 明文原样保留在 out
}

int main() {
    unsigned char in[20] = "TOPSECRET-DATA-999";
    unsigned char out[20];
    evp_ocb_encrypt(in, out, 20);
    std::printf("out[0..3]=%c%c%c%c (encrypted)\n", out[0], out[1], out[2], out[3]);
    std::printf("out[16..19]=%c%c%c%c (应为密文, 实为明文残留)\n", out[16], out[17], out[18], out[19]);
    std::printf("(正确行为: 20 字节应全部被加密)\n");
    return 0;
}
