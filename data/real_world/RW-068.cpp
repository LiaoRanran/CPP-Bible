// RW-068 | CVE-2021-22569 | protobuf | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-22569
// project_url: https://protobuf.dev/
// year: 2022 | severity: MEDIUM | source_type: cve
// mechanism: Java 端为主的解析歧义（同一字节流两种解析）在 C++ 侧的对应形态：
//   未知字段编码歧义导致签名校验与解析结果不一致。
// notes: 最小重构（"同字节流两解"的核心逻辑）。
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <vector>

// Two field encodings that yield identical parsed maps but different raw bytes:
// varint 0x80 0x01 vs canonical 0x01 (non-canonical varint acceptance).
struct ParsedField {
    int key;
    long long value;
};

long long read_varint_nc(const uint8_t* p, size_t n, size_t* consumed) {
    long long v = 0;
    int shift = 0;
    size_t i = 0;
    while (i < n) {
        v |= (long long)(p[i] & 0x7F) << shift;
        shift += 7;
        if ((p[i] & 0x80) == 0) { *consumed = i + 1; return v; }
        ++i;
    }
    *consumed = i;
    return v;
}

int main() {
    // canonical "1":  01
    // non-canonical: 81 00  -> also parses as 1 but different bytes (ambiguity)
    uint8_t canonical[1] = {0x01};
    uint8_t noncanon[2] = {0x81, 0x00};
    size_t c1, c2;
    long long v1 = read_varint_nc(canonical, 1, &c1);
    long long v2 = read_varint_nc(noncanon, 2, &c2);
    std::printf("values equal: %s, bytes differ: %s -> downstream divergence\n",
                v1 == v2 ? "yes" : "no",
                (c1 != c2) ? "yes" : "no");
    return 0;
}
