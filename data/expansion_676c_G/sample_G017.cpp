// sample_G017
// defect_type: heap_overread
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2021-3712 (https://nvd.nist.gov/vuln/detail/CVE-2021-3712) [openssl]
// (authoritative annotation in sample_G017.json)
#include <cstdio>
#include <cstring>
// CVE-2021-3712: ASN1_STRING 不以 NUL 结尾, 误用 strlen → 越界读
struct ASN1_STRING {
    unsigned char* data;
    int            length;   // 真实长度(不含 NUL)
};

static int ASN1_STRING_cmp(const ASN1_STRING* a, const ASN1_STRING* b) {
    /* DEFECT */ int la = (int)std::strlen((const char*)a->data);  // 原始缺陷: 应使用 a->length
    int lb = (int)std::strlen((const char*)b->data);
    return la - lb;
}

int main() {
    // crafted 证书字段: 4 字节可打印内容, 无 NUL
    ASN1_STRING s1{ new unsigned char[4]{ 'A', 'B', 'C', 'D' }, 4 };
    ASN1_STRING s2{ new unsigned char[4]{ 'A', 'B', 'C', 'E' }, 4 };
    std::printf("cmp=%d\n", ASN1_STRING_cmp(&s1, &s2));   // strlen 越过 4 字节堆缓冲
    delete[] s1.data;
    delete[] s2.data;
    return 0;
}
