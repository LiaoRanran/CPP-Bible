// sample_G039
// defect_type: integer_overflow
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: ubsan
// source: CVE-2016-7167 (https://nvd.nist.gov/vuln/detail/CVE-2016-7167) [curl]
// (authoritative annotation in sample_G039.json)
#include <cstdio>
// CVE-2016-7167: 转义函数分配尺寸 int 溢出
static int escape_alloc_size(int len) {
    /* DEFECT */ int alloc = len + 2 * 3 + 1;   // 最坏情况: 每字符转 3 字节 + NUL
    return alloc;
}

int main() {
    // crafted: 长度接近 0xFFFFFFFF 的待转义字符串(运行时变量绕过常量折叠)
    volatile int len = 2147483647 - 5;
    int alloc = escape_alloc_size(len);
    std::printf("escape alloc=%d (应为 %lld)\n", alloc, (long long)len + 7);
    return 0;
}
