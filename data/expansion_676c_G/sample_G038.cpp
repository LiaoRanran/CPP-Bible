// sample_G038
// defect_type: heap_overread
// severity: low
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2017-7407 (https://nvd.nist.gov/vuln/detail/CVE-2017-7407) [curl]
// (authoritative annotation in sample_G038.json)
#include <cstdio>
// CVE-2017-7407: --write-out 变量解析缺少终止检查 → 越界读
static void tool_writeout(const char* wrd, size_t len) {
    const char* p = wrd;
    const char* end = wrd + len;
    while (p < end) {
        if (*p == '%' && p + 1 < end && p[1] == '{') {
            const char* q = p + 2;
            /* DEFECT */ while (*q && *q != '}') ++q;   // 原始缺陷: 未检查 q < end
            std::printf("var=%.*s\n", (int)(q - (p + 2)), p + 2);
            p = q + 1;
        } else {
            ++p;
        }
    }
}

int main() {
    // crafted write-out: 堆上 5 字节, 以未闭合的 %{ 结尾且无 NUL
    char* w = new char[5]{ '%', '{', 's', 'i', 'z' };
    tool_writeout(w, 5);    // while(*q...) 走过堆缓冲末尾 → 越界读
    delete[] w;
    return 0;
}
