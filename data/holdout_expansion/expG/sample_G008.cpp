// sample_G008
// defect_type: heap_overread
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2015-1789 (https://nvd.nist.gov/vuln/detail/CVE-2015-1789) [openssl]
// (authoritative annotation in sample_G008.json)
#include <cstdio>
#include <cstring>
// CVE-2015-1789: X509_cmp_time 按固定位数解析时间, crafted 长度字段导致越界读
static int x509_parse_int(const char* buf, int* a) {
    // 原始缺陷: 不校验实际可用长度, 固定读 4 位数字
    for (int i = 0; i < 4; ++i) {
        if (buf[i] < '0' || buf[i] > '9') return -1;
        *a = *a * 10 + (buf[i] - '0');
    }
    return 0;
}

static int X509_cmp_time(const char* asn1time, int /*crafted_len*/) {
    int year = 0, mon = 0;
    if (x509_parse_int(asn1time, &year) != 0) return -2;      // 读 [0..4)
    /* DEFECT */ if (x509_parse_int(asn1time + 4, &mon) != 0) return -2;  // 读 [4..8): crafted_len=2 时只有 2 字节合法
    return year * 12 + mon;
}

int main() {
    // 攻击者 crafted: ASN1_TIME 缓冲实际 6 字节(YYMMDD), 长度字段声明 2
    char* t = new char[6]{ '9', '9', '0', '1', '0', '1' };
    std::printf("cmp=%d\n", X509_cmp_time(t, 2));   // 第二段解析读 [4..8) → 越界 2 字节
    delete[] t;
    return 0;
}
