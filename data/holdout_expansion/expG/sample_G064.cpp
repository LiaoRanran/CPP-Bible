// sample_G064
// defect_type: heap_overflow
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2021-23017 (https://nvd.nist.gov/vuln/detail/CVE-2021-23017) [nginx]
// (authoritative annotation in sample_G064.json)
#include <cstdio>
#include <cstring>
#include <cstdint>
// CVE-2021-23017: DNS 名解压 '.'/终止符偏移差一 → 1 字节越界写
static int ngx_resolver_copy_name(const unsigned char* src, size_t src_len,
                                  char* dst, size_t dst_cap) {
    size_t n = 0;
    size_t i = 0;
    while (i < src_len) {
        unsigned char label_len = src[i++];
        if (label_len == 0) break;
        if (i + label_len > src_len) return -1;
        if (n + label_len > dst_cap) return -1;       // 仅检查标签本体(边界条件差一)
        std::memcpy(dst + n, src + i, label_len);
        n += label_len;
        i += label_len;
        if (i < src_len && src[i]) dst[n++] = '.';    // 后续还有标签 → 追加分隔符
    }
    /* DEFECT */ // 原始缺陷: 未检查 n 是否已达 dst_cap
    dst[n] = '\0';                                    // n == dst_cap 时写 dst[dst_cap] → 越界 1 字节
    return (int)n;
}

int main() {
    // forged DNS 响应: 名字 "www.example-x.com" 恰 17 字符 → dst 恰好 17 字节
    unsigned char src[32] = { 3, 'w', 'w', 'w', 9, 'e', 'x', 'a', 'm', 'p', 'l', 'e', '-', 'x',
                              3, 'c', 'o', 'm', 0 };
    char* dst = new char[17];
    ngx_resolver_copy_name(src, 19, dst, 17);
    std::printf("resolved=%s\n", dst);
    delete[] dst;
    return 0;
}
