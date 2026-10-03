// sample_G011
// defect_type: integer_overflow
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: ubsan
// source: CVE-2016-2106 (https://nvd.nist.gov/vuln/detail/CVE-2016-2106) [openssl]
// (authoritative annotation in sample_G011.json)
#include <cstdio>
// CVE-2016-2106: EVP_EncryptUpdate 的 inl + bl 无溢出检查
static const int BLK = 16;

static bool evp_encrypt_check(int inl) {
    /* DEFECT */ int padded = inl + BLK;   // 修复版加的是 if (inl + bl < inl) 检查
    return padded > 0;
}

int main() {
    // 运行时构造的输入长度: 距 INT_MAX 差 15, 加块大小 16 → 有符号溢出
    volatile int inl = 2147483647 - 15;
    std::printf("check=%d\n", (int)evp_encrypt_check(inl));
    return 0;
}
