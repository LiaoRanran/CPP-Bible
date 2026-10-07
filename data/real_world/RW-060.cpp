// RW-060 | CVE-2022-35737 | SQLite | defect_type: integer_overflow
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2022-35737
// project_url: https://sqlite.org/
// year: 2022 | severity: MEDIUM | source_type: cve
// mechanism: printf 风格 %lld 角标处理在超大字符串参数（>2GB，或特定平台
//   size 截断）下整数溢出，导致越界/崩溃。
// notes: 最小重构（以 32 位截断复现，无需真分配 2GB）。UBSan 命中溢出。
#include <cstdint>
#include <cstdio>
#include <string>

// BUG: index of a conversion spec computed/stored in int; a giant width/precision
// value overflows it and the buffer index wraps.
char* sqlite_printf_offset(const char* fmt, int blob_len) {
    static char out[64];
    int consumed = 0;
    for (const char* p = fmt; *p; ++p) {
        if (*p == '%') {
            // crafted: "%9999999999999999999d" -> strtol result overflows int when
            // stored (real code used ints for width/precision bookkeeping)
            long long width = 0;
            const char* q = p + 1;
            while (*q >= '0' && *q <= '9') { width = width * 10 + (*q - '0'); ++q; }
            consumed += (int)width;            // narrowing overflow (UB path)
            p = q - 1;
        } else {
            if (consumed >= 0 && consumed < 64) out[consumed] = *p;
            ++consumed;
        }
    }
    out[63] = '\0';
    (void)blob_len;
    return out;
}

int main() {
    const char* crafted_fmt = "%9999999999999999999d-suffix"; // absurd width
    char* s = sqlite_printf_offset(crafted_fmt, 16);
    std::printf("offset result: %.20s\n", s);
    return 0;
}
