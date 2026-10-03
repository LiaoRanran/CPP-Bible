// sample_G015
// defect_type: stack_overflow
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2018-0739 (https://nvd.nist.gov/vuln/detail/CVE-2018-0739) [openssl]
// (authoritative annotation in sample_G015.json)
#include <cstdio>
// CVE-2018-0739: ASN.1 递归构造类型无深度限制 → 栈耗尽
struct Asn1Obj {
    int               tag;     // 0x30 = SEQUENCE (constructed)
    const Asn1Obj*    child;   // 递归定义
};

static int asn1_parse_constructed(const Asn1Obj* o) {
    unsigned char pad[8];                    // 每层栈帧开销
    pad[0] = (unsigned char)o->tag;
    if (o->child)
        /* DEFECT */ return 1 + asn1_parse_constructed(o->child) + pad[0];   // 无深度限制
    return 0;
}

int main() {
    // crafted 输入: 200 万层嵌套的 SEQUENCE
    const int DEPTH = 2000000;
    Asn1Obj* head = new Asn1Obj{ 0x30, 0 };
    for (int i = 0; i < DEPTH; ++i)
        head = new Asn1Obj{ 0x30, head };
    std::printf("parse=%d\n", asn1_parse_constructed(head));
    return 0;
}
