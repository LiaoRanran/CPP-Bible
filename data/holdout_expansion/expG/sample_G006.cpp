// sample_G006
// defect_type: type_confusion
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2015-0286 (https://nvd.nist.gov/vuln/detail/CVE-2015-0286) [openssl]
// (authoritative annotation in sample_G006.json)
#include <cstdio>
#include <cstring>
#include <cstdint>
// CVE-2015-0286: ASN1_TYPE_cmp 对 boolean 的比较路径类型混淆 → 无效读
enum Asn1Type { V_ASN1_BOOLEAN = 1, V_ASN1_OCTET_STRING = 4 };

struct ASN1_TYPE {
    Asn1Type type;
    union {
        int             boolean;      // BOOLEAN: 值是 0/0xFF 小整数, 不是指针
        unsigned char*  octet_string; // OCTET STRING: 值是堆指针
    } value;
};

static int ASN1_TYPE_cmp(const ASN1_TYPE* a, const ASN1_TYPE* b) {
    /* DEFECT */ // 原始缺陷: BOOLEAN 分支缺失, type 相同即按 octet_string(指针) 比较
    return std::memcmp(a->value.octet_string, b->value.octet_string, 4);
}

int main() {
    ASN1_TYPE t1{ V_ASN1_BOOLEAN, {0} };
    ASN1_TYPE t2{ V_ASN1_BOOLEAN, {0} };
    t1.value.boolean = 0x41414141;   // crafted 证书里的 boolean 字段值(非指针)
    t2.value.boolean = 0x41414141;
    std::printf("cmp=%d\n", ASN1_TYPE_cmp(&t1, &t2));   // 把整数当指针 memcmp → 无效读 → 崩溃
    return 0;
}
