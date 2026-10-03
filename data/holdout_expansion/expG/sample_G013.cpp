// sample_G013
// defect_type: pointer_overflow
// severity: high
// planted: false
// expected_verdict: miss
// expected_detectors: ubsan
// source: CVE-2016-2177 (https://nvd.nist.gov/vuln/detail/CVE-2016-2177) [openssl]
// (authoritative annotation in sample_G013.json)
#include <cstdio>
#include <cstdint>
// CVE-2016-2177: p + len 形式的边界检查在 len 极端时指针回绕(检查被绕过)
static bool within_bounds(const unsigned char* p, size_t plen, long long len) {
    // 原始模式: if (p + len > p + plen) reject —— len 来自攻击者的包长字段
    /* DEFECT */ return (p + len) <= (p + plen);
}

int main() {
    unsigned char* heap_buf = new unsigned char[64];
    // crafted 包长字段: LLONG_MAX → p + len 指针算术回绕(未定义行为)
    volatile long long len = 0x7FFFFFFFFFFFFFFFLL;
    bool pass = within_bounds(heap_buf, 64, len);
    std::printf("in_bounds=%d (回绕使越界长度通过边界检查)\n", (int)pass);
    delete[] heap_buf;
    return 0;
}
