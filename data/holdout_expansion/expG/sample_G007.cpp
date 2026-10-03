// sample_G007
// defect_type: null_deref
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2015-0288 (https://nvd.nist.gov/vuln/detail/CVE-2015-0288) [openssl]
// (authoritative annotation in sample_G007.json)
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
