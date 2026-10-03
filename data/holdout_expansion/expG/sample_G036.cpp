// sample_G036
// defect_type: double_free
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2026-8925 (https://nvd.nist.gov/vuln/detail/CVE-2026-8925) [curl]
// (authoritative annotation in sample_G036.json)
#include <cstdio>
#include <cstring>
// CVE-2026-8925: GSASL 上下文清理两次 → double free
struct GsaslCtx {
    char* out;    // 认证输出缓冲
};

static void gsasl_cleanup(GsaslCtx** ctx) {
    if (!ctx || !*ctx) return;
    delete[] (*ctx)->out;
    delete *ctx;
    /* DEFECT */ // 原始缺陷: 清理后未置 *ctx = NULL
}

static int sasl_authenticate(bool retry_needed) {
    GsaslCtx* c = new GsaslCtx{ new char[64] };
    std::memcpy(c->out, "AUTH-RESPONSE", 14);
    gsasl_cleanup(&c);
    if (retry_needed)
        gsasl_cleanup(&c);   /* DEFECT */ // 第二次清理(错误重试路径) → double free
    return 0;
}

int main() {
    sasl_authenticate(true);
    return 0;
}
