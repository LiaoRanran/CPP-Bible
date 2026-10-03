// sample_G016
// defect_type: null_deref
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2020-1971 (https://nvd.nist.gov/vuln/detail/CVE-2020-1971) [openssl]
// (authoritative annotation in sample_G016.json)
#include <cstdio>
#include <cstring>
// CVE-2020-1971: GENERAL_NAME_cmp 缺少 EDIPartyName 分支 → NULL 解引用
enum GenNameType { GEN_DNS = 2, GEN_OTHERNAME = 4, GEN_EDIPARTY = 5 };

struct OtherName { int name_len; };

struct GENERAL_NAME {
    GenNameType type;
    union {
        OtherName*   otherName;   // GEN_OTHERNAME / GEN_EDIPARTY 共用
        const char*  dNSName;
    } d;
};

static int GENERAL_NAME_cmp(const GENERAL_NAME* a, const GENERAL_NAME* b) {
    if (a->type != b->type) return -1;
    switch (a->type) {
    case GEN_OTHERNAME:
        return a->d.otherName->name_len - b->d.otherName->name_len;
    case GEN_DNS:
        return std::strcmp(a->d.dNSName, b->d.dNSName);
    default:
        break;
    }
    /* DEFECT */ // 原始缺陷: EDIPARTYNAME 无 case, 落到这里仍按 otherName(从未分配) 比较
    return a->d.otherName->name_len - b->d.otherName->name_len;   // NULL 解引用
}

int main() {
    GENERAL_NAME a{ GEN_EDIPARTY, {0} };   // otherName 从未分配
    GENERAL_NAME b{ GEN_EDIPARTY, {0} };
    std::printf("cmp=%d\n", GENERAL_NAME_cmp(&a, &b));
    return 0;
}
