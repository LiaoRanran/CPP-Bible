// RW-008 | CVE-2022-3602 | OpenSSL | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2022-3602
// project_url: https://www.openssl.org/
// year: 2022 | severity: HIGH | source_type: cve
// mechanism: X.509 名称约束检查中，punycode 解码到固定 4 字节栈缓冲，越界写 1 字节。
// notes: 最小重构。ASan 应报 stack-buffer-overflow write。
#include <cstdint>
#include <cstdio>
#include <cstring>

// Fixed 4-byte stack buffer as in the vulnerable helper.
int punycode_decode_one(const char* label, size_t label_len, char* out4) {
    size_t n = label_len;
    if (n > 4) {
        n = 4; // bounds "check" applied to the input, not the copy target size
    }
    // BUG: decode writes u32 as 1..4 bytes; a 4th byte plus terminator overflows out4
    for (size_t i = 0; i < n; ++i) {
        out4[i] = label[i];
    }
    out4[n] = '\0'; // one past the end when n == 4
    return (int)n;
}

int main() {
    const char* label = "abcd"; // 4-char punycode label (attacker "xn--" name)
    char stack_buf[4];
    punycode_decode_one(label, std::strlen(label), stack_buf);
    std::printf("decoded: %s\n", stack_buf);
    return 0;
}
