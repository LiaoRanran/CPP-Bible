// sample_G012
// defect_type: integer_overflow
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: ubsan
// source: CVE-2016-6303 (https://nvd.nist.gov/vuln/detail/CVE-2016-6303) [openssl]
// (authoritative annotation in sample_G012.json)
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
