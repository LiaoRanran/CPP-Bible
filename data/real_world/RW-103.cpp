// RW-103 | CVE-2018-0500 | curl | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2018-0500
// project_url: https://curl.se/
// year: 2018 | severity: CRITICAL | source_type: cve
// mechanism: SMTP 发送路径中地址解析堆越界写（用户名以 '<' 结尾的畸形地址）。
// notes: 最小重构。ASan 应报 heap-buffer-overflow write。
#include <cstdio>
#include <cstdlib>
#include <cstring>

// BUG: strips angle brackets by moving data and writes a NUL one byte past
// the allocation when the address ends with '<'.
char* smtp_format_address(const char* addr) {
    size_t len = std::strlen(addr);
    char* out = static_cast<char*>(std::malloc(len));    // no room for NUL terminator
    std::memcpy(out, addr, len);
    // crafted address "user<" -> after bracket handling the terminator lands at [len]
    out[len] = '\0';                                     // one byte past the buffer
    return out;
}

int main() {
    char* a = smtp_format_address("attacker@example.com<"); // malformed SMTP address
    std::printf("formatted: %s\n", a);
    std::free(a);
    return 0;
}
