// sample_G020
// defect_type: logic_error
// severity: high
// planted: false
// expected_verdict: miss
// expected_detectors: ubsan
// source: CVE-2015-1793 (https://nvd.nist.gov/vuln/detail/CVE-2015-1793) [openssl]
// (authoritative annotation in sample_G020.json)
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
