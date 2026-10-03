// sample_G049
// defect_type: logic_error
// severity: medium
// planted: false
// expected_verdict: miss
// expected_detectors: ubsan
// source: CVE-2016-7141 (https://nvd.nist.gov/vuln/detail/CVE-2016-7141) [curl]
// (authoritative annotation in sample_G049.json)
#include <cstdio>
#include <string>
// CVE-2016-7141: 连接复用不校验客户端证书状态
struct TlsConn {
    std::string client_cert_file;   // 该连接使用的客户端证书
    bool        in_pool;
};

static TlsConn* reuse_or_create(TlsConn* pool, int n, const std::string& wanted_cert) {
    /* DEFECT */ // 原始缺陷: 复用判定不比较 client_cert_file
    for (int i = 0; i < n; ++i)
        if (pool[i].in_pool) return &pool[i];
    TlsConn* c = new TlsConn{ wanted_cert, true };
    return c;
}

int main() {
    TlsConn pool[1] = { { "/home/alice/client.pem", true } };   // alice 证书的连接
    // 攻击者(无证书)发起新连接 → 错误复用 alice 的已认证连接
    TlsConn* c = reuse_or_create(pool, 1, "");
    std::printf("新连接使用的客户端证书: '%s' (正确行为: 无证书应新建连接)\n",
                c->client_cert_file.c_str());
    return 0;
}
