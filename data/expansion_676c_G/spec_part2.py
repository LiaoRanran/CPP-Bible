# -*- coding: utf-8 -*-
# 676c-G spec part2: OpenSSL asan/ubsan 组 (G006-G010)
PART = [
("G006", dict(
  defect_type="type_confusion", func="ASN1_TYPE_cmp", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2015-0286", url="https://nvd.nist.gov/vuln/detail/CVE-2015-0286",
           project="openssl", commit="", simplification="剥离 ASN.1 解码层，boolean/整数共用 union 的类型混淆按 CVE 描述（invalid read operation）直接构造"),
  trigger="两个 BOOLEAN 类型的 ASN1_TYPE 比较，整数按指针解释后解引用",
  notes="CVE-2015-0286: ASN1_TYPE_cmp 未正确执行 boolean 类型比较（does not properly perform boolean-type comparisons）→ 无效读/崩溃。本样本按『boolean 值被当指针解引用』镜像。",
), r'''
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
'''),

("G007", dict(
  defect_type="null_deref", func="X509_to_X509_REQ", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2015-0288", url="https://nvd.nist.gov/vuln/detail/CVE-2015-0288",
           project="openssl", commit="", simplification="剥离 X.509 解码层，『证书无 SubjectPublicKeyInfo → 公钥指针为 NULL』按 CVE 描述直接构造"),
  trigger="传入不含公钥字段的证书，转换路径未检查 NULL 即解引用",
  notes="CVE-2015-0288: X509_to_X509_REQ 用 invalid 证书时 NULL pointer dereference（CVE 描述: NULL pointer dereference and application crash via an invalid certificate）。",
), r'''
#include <cstdio>
#include <cstring>
// CVE-2015-0288: X509_to_X509_REQ 对无公钥的证书 NULL 解引用
struct X509PubKey {
    unsigned char* der;
    int            len;
};

// crafted 证书: TBS 中没有 SubjectPublicKeyInfo → 公钥解析返回 NULL
static X509PubKey* X509_get_pubkey(const unsigned char* cert, size_t cert_len) {
    (void)cert; (void)cert_len;
    return 0;
}

static int X509_to_X509_REQ(const unsigned char* cert, size_t cert_len) {
    X509PubKey* pk = X509_get_pubkey(cert, cert_len);
    /* DEFECT */ return pk->der[0] == 0x30;   // 未检查 pk 是否为 NULL → SEGV
}

int main() {
    unsigned char* cert = new unsigned char[64];
    std::memset(cert, 0x30, 64);   // 一段不含公钥的证书体
    std::printf("req=%d\n", X509_to_X509_REQ(cert, 64));
    delete[] cert;
    return 0;
}
'''),

("G008", dict(
  defect_type="heap_overread", func="X509_cmp_time", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2015-1789", url="https://nvd.nist.gov/vuln/detail/CVE-2015-1789",
           project="openssl", commit="", simplification="剥离证书时间比较外围逻辑，保留『按固定位数解析 ASN1_TIME 而不校验 crafted 长度字段』核心缺陷"),
  trigger="ASN1_TIME 长度字段被 crafted 为 2，解析仍按固定 4 位读年/月 → 读越界",
  notes="CVE-2015-1789: X509_cmp_time 对 crafted length field 的 ASN1_TIME 做 out-of-bounds read（CVE 描述: out-of-bounds read via a crafted length field in ASN1_TIME）。堆上 6 字节时间串按 4+4 位解析 → 越界 2 字节。",
), r'''
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
'''),

("G009", dict(
  defect_type="heap_overread", func="X509_NAME_oneline", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2016-2176", url="https://nvd.nist.gov/vuln/detail/CVE-2016-2176",
           project="openssl", commit="", simplification="剥离 EBCDIC 转换层，保留『高位字节触发转义分支时向前多读一字节且不检查边界』核心缺陷"),
  trigger="名字串最后一个字节是高位字节（crafted EBCDIC 数据），转义分支读 name[len]",
  notes="CVE-2016-2176: X509_NAME_oneline 处理 crafted EBCDIC ASN.1 数据时 buffer over-read（CVE 描述: obtain sensitive information from process stack memory or cause a denial of service (buffer over-read)）。",
), r'''
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
'''),

("G010", dict(
  defect_type="integer_overflow", func="EVP_EncodeUpdate", severity="high", planted=False,
  verdict="catch", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2016-2105", url="https://nvd.nist.gov/vuln/detail/CVE-2016-2105",
           project="openssl", commit="", simplification="剥离 base64 编码主体，保留『输出长度按 5*n/4+1 用 int 计算』核心缺陷，输入长度由运行时变量给出"),
  trigger="输入数据量接近 2^29，5*n 乘法发生 int 溢出",
  notes="CVE-2016-2105: EVP_EncodeUpdate 整数溢出 → heap memory corruption（CVE 描述: Integer overflow in the EVP_EncodeUpdate ... via a large amount of binary data）。本样本镜像长度计算的溢出点。",
), r'''
#include <cstdio>
// CVE-2016-2105: EVP_EncodeUpdate 输出长度按 int 计算 → 5*n 溢出
static int evp_encode_size(int in_len) {
    // 原始代码: 每组 3 字节编码为 4 字符, 输出上界按 5*n/4+1 预留
    /* DEFECT */ int total = 5 * in_len / 4 + 1;   // in_len 由攻击者数据量决定 → 乘法溢出
    return total;
}

int main() {
    // 运行时给出的输入长度(绕过常量折叠), 模拟攻击者构造的超大二进制数据
    volatile int n = 0x20000000;          // 2^29
    int total = evp_encode_size(n);
    std::printf("encode size=%d (应为 %lld)\n", total, ((long long)n * 5) / 4 + 1);
    return 0;
}
'''),
]
