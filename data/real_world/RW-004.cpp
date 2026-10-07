// RW-004 | CVE-2021-3712 | OpenSSL | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-3712
// project_url: https://www.openssl.org/
// year: 2021 | severity: MEDIUM | source_type: cve
// mechanism: ASN1_STRING 可能不以 NUL 结尾；将 data/len 当作 C 字符串交给
//   printf 类函数时读越界（证书打印/日志路径）。
// notes: 最小重构。ASan 应报 heap-buffer-overflow read。
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <vector>

// Mirrors ASN1_STRING: length-tracked bytes that may not be NUL-terminated.
struct ASN1_String {
    std::vector<uint8_t> data;
    long length;
};

// BUG: treats the ASN1_STRING as a C string ("%s") instead of "%.*s".
void print_asn1_string(const ASN1_String& s) {
    std::printf("value = %s\n", reinterpret_cast<const char*>(s.data.data()));
}

int main() {
    ASN1_String s;
    s.data.assign(8, 'X'); // no NUL terminator (DER-encoded value)
    s.length = 8;
    print_asn1_string(s);  // reads past the 8-byte allocation
    return 0;
}
