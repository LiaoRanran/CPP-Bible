// RW-066 | CVE-2021-22570 | protobuf | defect_type: null_pointer_deref
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-22570
// project_url: https://protobuf.dev/
// year: 2022 | severity: HIGH | source_type: cve
// mechanism: 解析重复出现的空包名（含多个 '.' 的畸形 descriptor）时
//   字符串切分产生空段，后续按空指针/NULL 字符串处理（DoS）。
// notes: 最小重构。ASan/UBSan 命中 NULL 解引用。
#include <cstdio>
#include <cstring>
#include <string>

// BUG: splitting "a..b" yields an empty segment; the code then strchr()s the
// (null) segment data from an out-of-range iterator.
int parse_package_name(const std::string& name) {
    size_t start = 0;
    int dots = 0;
    while (start <= name.size()) {
        size_t dot = name.find('.', start);
        size_t end = (dot == std::string::npos) ? name.size() : dot;
        const char* seg = name.c_str() + start;
        size_t seg_len = end - start;
        if (seg_len == 0) {
            // empty segment: real code path calls descriptor lookup with a null
            // Substring; here: dereference a null returned pointer
            const char* p = nullptr;
            dots += (int)std::strlen(p);   // NULL deref (crafted "a..b" name)
        }
        if (dot == std::string::npos) break;
        start = dot + 1;
    }
    return dots;
}

int main() {
    int r = parse_package_name("com..example");   // crafted double dot
    std::printf("parsed %d\n", r);
    return 0;
}
