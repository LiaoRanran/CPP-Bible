// sample_G086
// defect_type: timing_side_channel
// severity: medium
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// source: CVE-2016-2178 (https://nvd.nist.gov/vuln/detail/CVE-2016-2178) [openssl]
// (authoritative annotation in sample_G086.json)
#include <cstdio>
#include <cstdint>
// CVE-2016-2178 (等价重构): 非常量时间模乘 → 时序侧信道
static long g_op_count = 0;    // 模拟可测量的操作计数(时序)

static unsigned int mont_mul_nonct(unsigned int a, unsigned int b, unsigned int n) {
    unsigned int r = 0;
    for (int i = 0; i < 32; ++i) {
        /* DEFECT */ // 原始缺陷: 分支依赖秘密数据的位模式
        if ((b >> i) & 1u) { r = (r + a) % n; g_op_count += 3; }
        else               g_op_count += 1;
        a = (a + a) % n;
    }
    return r;
}

int main() {
    unsigned int n = 0xFFFFFFFBu;
    g_op_count = 0;
    mont_mul_nonct(1234567u, 0x55555555u, n);      // k1: 位模式稀疏
    long ops1 = g_op_count;
    g_op_count = 0;
    mont_mul_nonct(1234567u, 0xFFFFFFFFu, n);      // k2: 位模式全 1
    long ops2 = g_op_count;
    std::printf("ops(k1)=%ld ops(k2)=%ld 差异=%ld (应恒等: 常量时间缺失)\n",
                ops1, ops2, ops2 - ops1);
    return 0;
}
