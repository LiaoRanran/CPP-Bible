// sample_G018
// defect_type: stack_overflow_write
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2022-3602 (https://nvd.nist.gov/vuln/detail/CVE-2022-3602) [openssl]
// (authoritative annotation in sample_G018.json)
#include <cstdio>
#include <cstring>
#include <cstdint>
// CVE-2022-3602: punycode 解码输出循环缺少边界检查 → 栈缓冲溢出
static int punycode_decode(const char* in, size_t inlen, unsigned int* out, size_t out_cap) {
    size_t out_count = 0;
    size_t i = 0;
    // 1) literal 前缀: 复制到第一个 '-' 为止
    while (i < inlen && in[i] != '-') {
        /* DEFECT */ out[out_count++] = (unsigned char)in[i];   // 缺少 out_count < out_cap 检查
        ++i;
    }
    if (i < inlen) ++i;   // 跳过分隔符
    // 2) 编码数字部分(简化: 只计数)
    for (; i < inlen; ++i)
        if (in[i] >= 'a' && in[i] <= 'z') ++out_count;
    return (int)out_count;
}

int main() {
    unsigned int out[8];                       // 修复版输出缓冲容量 8
    char crafted[48];                          // 攻击者 crafted 名字: 40 字节前缀 + '-' + 数字
    std::memset(crafted, 'a', 40);
    crafted[40] = '-';
    crafted[41] = 'x'; crafted[42] = '9'; crafted[43] = 'a'; crafted[44] = '\0';
    int n = punycode_decode(crafted, 44, out, 8);
    std::printf("decoded=%d first=%u\n", n, out[0]);   // 写满 8 槽后继续写 → 栈溢出
    return 0;
}
