// sample_G022
// defect_type: logic_error
// severity: high
// planted: false
// expected_verdict: miss
// expected_detectors: ubsan
// source: CVE-2015-0204 (https://nvd.nist.gov/vuln/detail/CVE-2015-0204) [openssl]
// (authoritative annotation in sample_G022.json)
#include <cstdio>
// CVE-2015-0204: 服务器提供 export 弱密钥未被客户端拒绝
struct KeyExchange {
    bool requested_export;   // 客户端实际请求的套件强度
    int  server_key_bits;    // 服务器返回的临时 RSA 密钥强度
};

static bool ssl3_get_key_exchange(const KeyExchange* kx) {
    /* DEFECT */ // 原始缺陷: 未校验 (requested_export && server_key_bits <= 512)
    //             与 (!requested_export && server_key_bits >= 1024) 的一致性
    return true;   // 任何服务器响应都被接受
}

int main() {
    KeyExchange kx{ false, 512 };   // 客户端要普通套件, 服务器只给 512 位 export 密钥
    bool accepted = ssl3_get_key_exchange(&kx);
    std::printf("key exchange %s: server_key_bits=%d requested_export=%d (正确行为: reject)\n",
                accepted ? "ACCEPT[错误]" : "reject", kx.server_key_bits, (int)kx.requested_export);
    return 0;
}
