# -*- coding: utf-8 -*-
# 676c-G spec part4: OpenSSL asan/miss 组 (G016-G020)
PART = [
("G016", dict(
  defect_type="null_deref", func="GENERAL_NAME_cmp", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2020-1971", url="https://nvd.nist.gov/vuln/detail/CVE-2020-1971",
           project="openssl", commit="", simplification="剥离 X.509 GENERAL_NAME 全部实际类型，只保留 EDIPartyName 分支缺失 + other 联合成员为 NULL 的核心缺陷"),
  trigger="两个 EDIPARTYNAME 类型的 GENERAL_NAME 比较 → otherName 未分配为 NULL → 解引用",
  notes="CVE-2020-1971: GENERAL_NAME_cmp 对 EDIPartyName 缺少比较分支 → NULL pointer dereference（CVE 描述: This function can crash ... both GENERAL_NAMEs are EDIPartyName）。",
), r'''
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
'''),

("G017", dict(
  defect_type="heap_overread", func="ASN1_STRING_cmp", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2021-3712", url="https://nvd.nist.gov/vuln/detail/CVE-2021-3712",
           project="openssl", commit="", simplification="剥离 ASN1_STRING 全部用途，保留『内部 (data,len) 存储不含 NUL、比较路径误用 strlen』核心缺陷"),
  trigger="ASN1_STRING 内容 4 字节无 NUL，比较按 strlen 处理 → 读越界",
  notes="CVE-2021-3712: ASN1_STRING 以 (data, length) 表示、不保证 NUL 结尾（CVE 描述: contrasts with normal C strings which are repesented as a buffer for the string data），误按 C 字符串读 → 越界读/信息泄露。",
), r'''
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
'''),

("G018", dict(
  defect_type="stack_overflow_write", func="ossl_punycode_decode", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2022-3602", url="https://nvd.nist.gov/vuln/detail/CVE-2022-3602",
           project="openssl", commit="", simplification="剥离 X.509 name constraint 检查链路，保留 punycode 解码『输出循环缺少边界检查』核心缺陷（修复版加入 out==out_max 判断）"),
  trigger="crafted X.509 punycode 名字带超长 literal 前缀（40 字节 > 输出缓冲 8）",
  notes="CVE-2022-3602: X.509 punycode 解码缓冲区溢出（CVE 描述: A buffer overrun can be triggered in X.509 certificate verification ... name constraint checking）。原始缺陷即 ossl_punycode_decode 输出无界写入。",
), r'''
#include <cstdio>
#include <cstring>
#include <cstdint>
// CVE-2022-3602: punycode 解码输出循环缺少边界检查 → 栈缓冲溢出
static int punycode_decode(const char* in, size_t inlen, unsigned int* out, size_t out_cap) {
    size_t out_count = 0;
    size_t i = 0;
    // 1) literal 前缀: 复制到第一个 '-' 为止
    while (i < inlen && in[i] != '-') {
        /* DEFECT */ out[out_count++] = (unsigned char)in[i];   // 缺少 out_count < out_cap 检查
        ++i;
    }
    if (i < inlen) ++i;   // 跳过分隔符
    // 2) 编码数字部分(简化: 只计数)
    for (; i < inlen; ++i)
        if (in[i] >= 'a' && in[i] <= 'z') ++out_count;
    return (int)out_count;
}

int main() {
    unsigned int out[8];                       // 修复版输出缓冲容量 8
    char crafted[48];                          // 攻击者 crafted 名字: 40 字节前缀 + '-' + 数字
    std::memset(crafted, 'a', 40);
    crafted[40] = '-';
    crafted[41] = 'x'; crafted[42] = '9'; crafted[43] = 'a'; crafted[44] = '\0';
    int n = punycode_decode(crafted, 44, out, 8);
    std::printf("decoded=%d first=%u\n", n, out[0]);   // 写满 8 槽后继续写 → 栈溢出
    return 0;
}
'''),

("G019", dict(
  defect_type="infinite_loop", func="bn_mod_sqrt", severity="high", planted=True,
  verdict="miss", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2022-0778", url="https://nvd.nist.gov/vuln/detail/CVE-2022-0778",
           project="openssl", commit="", simplification="基于 CVE 描述（BN_mod_sqrt 对非素数模数死循环）以等价的 Tonelli-Shanks 循环骨架重构，非原始代码逐行镜像，故标 planted=true"),
  trigger="非素数模数 p=15, a=3：平方迭代陷入 3→9→6→6→… 不动点循环，永不终止",
  notes="CVE-2022-0778: BN_mod_sqrt 对非素数模数永不过返回（CVE 描述: contains a bug that can cause it to loop forever for non-prime moduli），解析证书时可远程 DoS。纯逻辑缺陷，sanitizer 无运行时报告 → 诚实标 miss（DoS 盲区，验证时进程超时）。",
), r'''
#include <cstdio>
// CVE-2022-0778: BN_mod_sqrt 对非素数模数死循环（DoS）
static unsigned int bn_mod_sqrt(unsigned int a, unsigned int p) {
    unsigned int y = a % p;
    // Tonelli-Shanks 风格迭代骨架; 原始缺陷: 非素数 p 下退出条件永不满足
    for (;;) {
        if (y == 1) return 0;           // 正常退出路径(素数 p 可达)
        /* DEFECT */ y = (y * y) % p;   // p=15, a=3: 3→9→6→6→6→... 永不等于 1
    }
}

int main() {
    // crafted 证书中的非素数模数
    std::printf("sqrt=%u\n", bn_mod_sqrt(3, 15));   // 永不返回 → DoS
    return 0;
}
'''),

("G020", dict(
  defect_type="logic_error", func="X509_verify_cert", severity="high", planted=False,
  verdict="miss", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2015-1793", url="https://nvd.nist.gov/vuln/detail/CVE-2015-1793",
           project="openssl", commit="", simplification="剥离证书解码/签名验证，以等价链构建状态机镜像『alternate chain 中 untrusted 证书未查 Basic Constraints cA』核心缺陷"),
  trigger="叶子证书由攻击者自签的 FakeRoot 签发，FakeRoot 非 CA 且不在信任库",
  notes="CVE-2015-1793: X509_verify_cert 未正确处理 alternate chain 的 Basic Constraints cA 值 → 伪造 CA 被接受（CVE 描述: does not properly process X.509 Basic Constraints cA values ... spoof a Certification Authority）。纯逻辑错误，正确行为=reject、实际=accept，sanitizer 无报告 → 诚实标 miss。",
), r'''
#include <cstdio>
#include <string>
// CVE-2015-1793: alternate chain 未检查 cA 标志 → 伪造 CA 被接受
struct Cert {
    const char* subject;
    const char* issuer;
    bool        is_ca;
    bool        trusted;
};

static const Cert kTrustStore[] = { { "RootCA", "RootCA", true, true } };
static const Cert kUntrusted[] = {
    { "FakeRoot", "FakeRoot", false, false },   // 攻击者提供的自签"中间证书"(非 CA)
    { "Leaf",     "FakeRoot", false, false },   // 受害者收到的叶子证书
};

static const Cert* find_by_subject(const Cert* pool, int n, const char* subject) {
    for (int i = 0; i < n; ++i)
        if (std::string(pool[i].subject) == subject) return &pool[i];
    return 0;
}

static bool verify_cert_vulnerable(const Cert* leaf) {
    // alternate chain 构建: 沿 issuer 只在 untrusted 集合中向上找
    const Cert* cur = leaf;
    int depth = 0;
    while (!cur->trusted && depth++ < 4) {
        const Cert* issuer = find_by_subject(kUntrusted, 2, cur->issuer);
        if (!issuer) break;
        cur = issuer;
    }
    /* DEFECT */ // 原始缺陷: 循环结束后未回查信任库, 也未检查 cur->is_ca
    return cur != 0;   // FakeRoot(非 CA、不受信)被当作合法锚点 → 返回 accept
}

int main() {
    bool accepted = verify_cert_vulnerable(&kUntrusted[1]);
    std::printf("verify(Leaf)=%s  (正确行为: reject, 因为 FakeRoot 非 CA 且不在信任库)\n",
                accepted ? "ACCEPT[错误]" : "reject");
    return 0;
}
'''),
]
