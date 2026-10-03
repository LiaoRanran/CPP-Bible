// sample_G047
// defect_type: logic_error
// severity: medium
// planted: false
// expected_verdict: miss
// expected_detectors: ubsan
// source: CVE-2020-8286 (https://nvd.nist.gov/vuln/detail/CVE-2020-8286) [curl]
// (authoritative annotation in sample_G047.json)
#include <cstdio>
// CVE-2020-8286: OCSP 响应校验不足 → 撤销检查失效
struct OcspResponse {
    int  status;          // 0=good 1=revoked 2=unknown
    bool malformed;
};

static bool certificate_revoked(const OcspResponse* r) {
    /* DEFECT */ // 原始缺陷: malformed 响应未按"校验失败"处理, 而是当作"未撤销"
    if (r->malformed) return false;   // 应当: 校验失败 → 视为验证不通过
    return r->status == 1;
}

int main() {
    OcspResponse r{ 2, true };   // 恶意服务器返回畸形 OCSP 响应
    std::printf("证书已撤销? %s (响应畸形: %s)\n",
                certificate_revoked(&r) ? "是" : "否[错误: 校验失败应阻断连接]",
                r.malformed ? "是" : "否");
    return 0;
}
