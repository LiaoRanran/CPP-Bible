# -*- coding: utf-8 -*-
# 676c-G spec part3: OpenSSL ubsan/asan 组 (G011-G015)
PART = [
("G011", dict(
  defect_type="integer_overflow", func="EVP_EncryptUpdate", severity="high", planted=False,
  verdict="catch", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2016-2106", url="https://nvd.nist.gov/vuln/detail/CVE-2016-2106",
           project="openssl", commit="", simplification="剥离加解密主体，保留『inl + block_size 有符号溢出且缺少溢出检查』核心缺陷（修复版本加入 inl+bl<inl 检查）"),
  trigger="输入长度 inl = INT_MAX-15，块大小 16，inl+bl 有符号溢出",
  notes="CVE-2016-2106: EVP_EncryptUpdate 整数溢出（CVE 描述: Integer overflow in the EVP_EncryptUpdate ... via a large amount of data）。修复 commit 增加的正是 inl+bl 溢出检查，本样本保留无检查版本。",
), r'''
#include <cstdio>
// CVE-2016-2106: EVP_EncryptUpdate 的 inl + bl 无溢出检查
static const int BLK = 16;

static bool evp_encrypt_check(int inl) {
    /* DEFECT */ int padded = inl + BLK;   // 修复版加的是 if (inl + bl < inl) 检查
    return padded > 0;
}

int main() {
    // 运行时构造的输入长度: 距 INT_MAX 差 15, 加块大小 16 → 有符号溢出
    volatile int inl = 2147483647 - 15;
    std::printf("check=%d\n", (int)evp_encrypt_check(inl));
    return 0;
}
'''),

("G012", dict(
  defect_type="integer_overflow", func="MDC2_Update", severity="high", planted=False,
  verdict="catch", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2016-6303", url="https://nvd.nist.gov/vuln/detail/CVE-2016-6303",
           project="openssl", commit="", simplification="剥离 MDC2 哈希主体，保留『ctx->num += inl 用 int 累加』核心缺陷，后续越界写按 CVE 描述为 OOB write"),
  trigger="多次 Update 累加使 ctx->num 越过 INT_MAX",
  notes="CVE-2016-6303: MDC2_Update 整数溢出 → out-of-bounds write（CVE 描述: Integer overflow in the MDC2_Update ... out-of-bounds write and application crash）。本样本镜像 num 累加溢出点。",
), r'''
#include <cstdio>
#include <cstring>
// CVE-2016-6303: MDC2_Update 的 ctx->num 用 int 累加 → 溢出
struct MDC2_CTX {
    int            num;
    unsigned char  data[16];
};

static int MDC2_Update(MDC2_CTX* c, const unsigned char* in, int inl) {
    /* DEFECT */ c->num += inl;   // int 累加溢出 → 后续按 num 索引 data[] 越界写
    if (c->num >= 0 && c->num <= 16)
        std::memcpy(c->data + c->num, in, (size_t)inl < 16u - (size_t)c->num ? (size_t)inl : 0);
    return 0;
}

int main() {
    MDC2_CTX ctx;
    ctx.num = 2147483640;          // 运行时已接近 INT_MAX 的累积值(超长输入序列)
    unsigned char chunk[4] = {1, 2, 3, 4};
    volatile int inl = 100;
    MDC2_Update(&ctx, chunk, inl);
    std::printf("num=%d\n", ctx.num);
    return 0;
}
'''),

("G013", dict(
  defect_type="pointer_overflow", func="check_boundary", severity="high", planted=False,
  verdict="miss", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2016-2177", url="https://nvd.nist.gov/vuln/detail/CVE-2016-2177",
           project="openssl", commit="", simplification="剥离协议解析层，保留『用指针算术做堆缓冲边界检查且长度攻击者可控』核心模式，长度字段由运行时变量给出"),
  trigger="包长字段为 LLONG_MAX，p + len 指针算术回绕 → 边界检查被绕过",
  notes="CVE-2016-2177: OpenSSL 用指针算术做堆缓冲边界检查（incorrectly uses pointer arithmetic for heap-buffer boundary checks），长度极端时整数溢出。指针回绕本身是 UB，但 GCC 的 -fsanitize=undefined **不包含 pointer-overflow 检查**（该资产为 clang 专属）→ 本机检测器无报告。真实检测器盲区，诚实标 miss。",
), r'''
#include <cstdio>
#include <cstdint>
// CVE-2016-2177: p + len 形式的边界检查在 len 极端时指针回绕(检查被绕过)
static bool within_bounds(const unsigned char* p, size_t plen, long long len) {
    // 原始模式: if (p + len > p + plen) reject —— len 来自攻击者的包长字段
    /* DEFECT */ return (p + len) <= (p + plen);
}

int main() {
    unsigned char* heap_buf = new unsigned char[64];
    // crafted 包长字段: LLONG_MAX → p + len 指针算术回绕(未定义行为)
    volatile long long len = 0x7FFFFFFFFFFFFFFFLL;
    bool pass = within_bounds(heap_buf, 64, len);
    std::printf("in_bounds=%d (回绕使越界长度通过边界检查)\n", (int)pass);
    delete[] heap_buf;
    return 0;
}
'''),

("G014", dict(
  defect_type="heap_overread", func="chacha20_poly1305_decrypt", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2017-3731", url="https://nvd.nist.gov/vuln/detail/CVE-2017-3731",
           project="openssl", commit="", simplification="剥离 ChaCha20-Poly1305 主体，保留『tag 指针在长度检查之前计算』核心缺陷，截断包长度硬编码"),
  trigger="截断的 AEAD 包 len=5 < tag_len=16，tag 指针指向缓冲区之前 → 前向越界读",
  notes="CVE-2017-3731: 截断包触发 out-of-bounds read（CVE 描述: a truncated packet can cause ... an out-of-bounds read, usually resulting in a crash）。本样本镜像 tag = in + len - tag_len 的前向越界。",
), r'''
#include <cstdio>
#include <cstring>
#include <cstdint>
// CVE-2017-3731: 截断 AEAD 包 → tag 指针计算越过缓冲区起点 → 前向越界读
static const size_t TAG_LEN = 16;

static int aead_decrypt(const unsigned char* in, size_t len, unsigned char* out) {
    // 原始缺陷: 在校验 len >= TAG_LEN 之前就计算 tag 位置
    /* DEFECT */ const unsigned char* tag = in + len - TAG_LEN;
    for (size_t i = 0; i < TAG_LEN; ++i)
        out[i] = (unsigned char)(in[i] ^ tag[i]);   // len=5 时读 in[-11..] → 越界
    return 0;
}

int main() {
    unsigned char* truncated = new unsigned char[5]{ 0x17, 0x03, 0x03, 0x00, 0x01 };
    unsigned char out[32];
    std::memset(out, 0, sizeof(out));
    aead_decrypt(truncated, 5, out);
    std::printf("decrypt done, out[0]=%02x\n", out[0]);
    delete[] truncated;
    return 0;
}
'''),

("G015", dict(
  defect_type="stack_overflow", func="asn1_parse_constructed", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2018-0739", url="https://nvd.nist.gov/vuln/detail/CVE-2018-0739",
           project="openssl", commit="", simplification="剥离 ASN.1 具体结构（PKCS7 等），保留『递归定义的构造类型解析无深度限制』核心缺陷，嵌套输入在 main 中构造"),
  trigger="200 万层嵌套的 ASN.1 构造类型 → 递归解析耗尽调用栈",
  notes="CVE-2018-0739: 递归构造类型的 ASN.1 输入导致栈耗尽（CVE 描述: Constructed ASN.1 types with a recursive definition ... exceed the stack）。ASan 报告 stack-overflow。",
), r'''
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
'''),
]
