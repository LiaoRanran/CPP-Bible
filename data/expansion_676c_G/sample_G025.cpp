// sample_G025
// defect_type: heap_overflow
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2026-72897 (https://nvd.nist.gov/vuln/detail/CVE-2026-72897) [openssl]
// (authoritative annotation in sample_G025.json)
#include <cstdio>
#include <cstring>
// CVE-2026-72897: SSL_set_SSL_CTX 证书槽位数组越界（用户态等价重构）
struct SslCtx {
    int            num_sig_algs;   // 该上下文支持的签名算法数
    unsigned char* cert_slots;     // 证书槽位数组(每个签名算法一个槽)
    int            slots_cap;
};

static void SSL_set_SSL_CTX(SslCtx** cur, SslCtx* new_ctx) {
    *cur = new_ctx;
    /* DEFECT */ // 原始缺陷: 之后按 new_ctx->num_sig_algs 索引/填充证书槽位,
    //             但槽位数组可能仍按旧上下文容量分配
}

int main() {
    SslCtx old_ctx{ 2, new unsigned char[2]{ 0, 0 }, 2 };
    SslCtx new_ctx{ 8, new unsigned char[2]{ 0, 0 }, 2 };   // 新上下文算法更多, 槽位同样只有 2
    SslCtx* active = &old_ctx;
    SSL_set_SSL_CTX(&active, &new_ctx);
    for (int i = 0; i < active->num_sig_algs; ++i)
        active->cert_slots[i] = (unsigned char)i;   /* DEFECT */ // i>=2 越界写 → 堆溢出
    std::printf("slots[0]=%d\n", active->cert_slots[0]);
    return 0;
}
