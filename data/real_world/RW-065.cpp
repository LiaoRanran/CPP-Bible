// RW-065 | CVE-2021-41099 | Redis | defect_type: integer_overflow
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-41099
// project_url: https://redis.io/
// year: 2021 | severity: HIGH | source_type: cve
// mechanism: proto-max-bulk-len / SETRANGE 偏移处理整数溢出，越界写（配置相关）。
// notes: 最小重构。UBSan 命中溢出，ASan 命中越界写。
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>

// BUG: offset + len computed in int32 for a large SETRANGE offset.
void setrange_apply(char* buf, size_t buf_cap, int32_t offset, const char* data, int32_t len) {
    int32_t end = offset + len;                  // overflow for crafted values
    if (end < 0) end = len;                      // "guard" that re-enables the OOB path
    std::memcpy(buf + offset, data, (size_t)len); // writes at attacker offset unchecked
    (void)buf_cap;
}

int main() {
    char* buf = static_cast<char*>(std::malloc(1024));
    const char* payload = "AAAAAAAAAAAAAAAA";
    // crafted SETRANGE key 0 2147483640 <16 bytes>  (offset+len overflows int32)
    setrange_apply(buf, 1024, 2147483640 - 15, payload, 16);
    std::printf("setrange applied\n");
    std::free(buf);
    return 0;
}
