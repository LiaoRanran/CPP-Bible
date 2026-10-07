// RW-085 | CVE-2021-29628 | FreeBSD | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-29628
// project_url: https://www.freebsd.org/
// year: 2021 | severity: MEDIUM | source_type: cve
// mechanism: ktls 发送路径中多个 TLS 记录共享同一 mbuf 时的清零顺序问题，
//   已加密记录被重放/明文泄露。
// notes: 最小重构（记录边界状态判定）。
#include <cstdio>
#include <cstring>

struct KtlsRecord {
    unsigned char buf[64];
    size_t stored;         // bytes currently stored (not yet sent)
    unsigned seq;          // TLS record sequence number
};

// BUG: zeroing after append forgets to reflect the appended bytes in `stored`,
// so the *next* record re-sends / exposes stale plaintext bytes.
void ktls_append(KtlsRecord& r, const unsigned char* data, size_t len) {
    std::memcpy(r.buf + r.stored, data, len);
    std::memset(r.buf, 0, r.stored);        // BUG: clears the head, not the tail,
                                            // stored never grows -> replay window
}

int main() {
    KtlsRecord r{{0}, 0, 1};
    unsigned char plaintext[17] = "SECRET-PLAINTEXT";  // 16 chars + NUL
    ktls_append(r, plaintext, 16);
    ktls_append(r, plaintext, 16);          // second append reuses stale bytes
    std::printf("record stored=%zu seq=%u (stale bytes exposed)\n", r.stored, r.seq);
    return 0;
}
