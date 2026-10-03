// sample_G009
// defect_type: heap_overread
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2016-2176 (https://nvd.nist.gov/vuln/detail/CVE-2016-2176) [openssl]
// (authoritative annotation in sample_G009.json)
#include <cstdio>
#include <cstring>
// CVE-2016-2176: X509_NAME_oneline 对高位字节(转义分支)向前多读 1 字节 → 越界读
static int X509_NAME_oneline(const unsigned char* name, size_t len, char* out, size_t out_cap) {
    size_t o = 0;
    for (size_t i = 0; i < len && o + 8 < out_cap; ++i) {
        unsigned char c = name[i];
        if (c & 0x80) {
            // 转义分支: 组合下一个字节
            /* DEFECT */ unsigned char next = name[i + 1];   // i+1 可达 len → 越界读 1 字节
            out[o++] = '?';
            (void)next;
        } else {
            out[o++] = (char)c;
        }
    }
    out[o] = '\0';
    return (int)o;
}

int main() {
    // crafted 名字: 最后一个字节是高位字节(0x80) → 转义分支读 name[len] → 堆越界
    unsigned char* name = new unsigned char[8]{ 'C', 'N', '=', 'A', 'B', 0xC4, 0xE9, 0x80 };
    char out[64];
    X509_NAME_oneline(name, 8, out, sizeof(out));
    std::printf("oneline=%s\n", out);
    delete[] name;
    return 0;
}
