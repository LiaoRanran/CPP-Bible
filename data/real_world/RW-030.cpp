// RW-030 | CVE-2022-29824 | libxml2 | defect_type: integer_overflow
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2022-29824
// project_url: https://gitlab.gnome.org/GNOME/libxml2
// year: 2022 | severity: MEDIUM | source_type: cve
// mechanism: 缓冲区长度累加（int）溢出为负/回绕，后续写入越界（xmlBuf 增长路径）。
// notes: 最小重构。UBSan 应报 signed integer overflow；溢出后 ASan 报越界写。
#include <cstdio>
#include <cstdlib>
#include <cstring>

// BUG: `total` is int; two large lengths overflow into a small allocation.
char* grow_buffer_and_append(int len_a, int len_b) {
    int total = len_a + len_b;                  // signed overflow (UB)
    char* buf = static_cast<char*>(std::malloc(total > 0 ? static_cast<size_t>(total) : 16));
    if (!buf) return nullptr;
    std::memset(buf, 'a', static_cast<size_t>(len_a)); // writes len_a bytes into tiny buf
    std::printf("allocated %d, wrote %d\n", total, len_a);
    return buf;
}

int main() {
    // crafted XML with declared lengths near INT_MAX
    char* b = grow_buffer_and_append(0x7FFFFFF0, 0x20); // INT_MAX-15 + 32 -> overflow
    std::free(b);
    return 0;
}
