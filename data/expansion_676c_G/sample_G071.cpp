// sample_G071
// defect_type: heap_underflow
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2018-1000001 (https://nvd.nist.gov/vuln/detail/CVE-2018-1000001) [glibc]
// (authoritative annotation in sample_G071.json)
#include <cstdio>
#include <cstring>
// CVE-2018-1000001: realpath 写到目的缓冲区之前 → 堆缓冲下溢
static const char* k_cwd_prefix = "/very/deeply/nested/directory/prefix/that/is/quite/long/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";

static char* realpath_mirror(const char* rel_path, char* resolved, size_t dest_cap) {
    size_t prefix_len = std::strlen(k_cwd_prefix);
    size_t rel_len = std::strlen(rel_path);
    char* dest_end = resolved + dest_cap;
    /* DEFECT */ // 原始缺陷: 前缀+路径超长时指针越过起点而未中止
    char* p = dest_end - rel_len - 1 - prefix_len;
    std::memcpy(p, k_cwd_prefix, prefix_len);        // 向 resolved 之前写入 → 下溢
    std::memcpy(p + prefix_len, rel_path, rel_len);
    return p;
}

int main() {
    char* resolved = new char[256];
    realpath_mirror("/etc/passwd", resolved, 256);   // 前缀 300 字节 → 起点前移 ~265 字节
    delete[] resolved;
    return 0;
}
