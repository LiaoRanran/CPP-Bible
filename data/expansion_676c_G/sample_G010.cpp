// sample_G010
// defect_type: integer_overflow
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: ubsan
// source: CVE-2016-2105 (https://nvd.nist.gov/vuln/detail/CVE-2016-2105) [openssl]
// (authoritative annotation in sample_G010.json)
#include <cstdio>
// CVE-2016-2105: EVP_EncodeUpdate 输出长度按 int 计算 → 5*n 溢出
static int evp_encode_size(int in_len) {
    // 原始代码: 每组 3 字节编码为 4 字符, 输出上界按 5*n/4+1 预留
    /* DEFECT */ int total = 5 * in_len / 4 + 1;   // in_len 由攻击者数据量决定 → 乘法溢出
    return total;
}

int main() {
    // 运行时给出的输入长度(绕过常量折叠), 模拟攻击者构造的超大二进制数据
    volatile int n = 0x20000000;          // 2^29
    int total = evp_encode_size(n);
    std::printf("encode size=%d (应为 %lld)\n", total, ((long long)n * 5) / 4 + 1);
    return 0;
}
