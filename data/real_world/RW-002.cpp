// RW-002 | CVE-2022-0778 | OpenSSL | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2022-0778
// project_url: https://www.openssl.org/
// year: 2022 | severity: HIGH | source_type: cve
// mechanism: BN_mod_sqrt() 对非素数模的 Tonelli-Shanks 循环缺少出口，解析
//   携带非法显式曲线参数的证书时进入死循环（DoS）。676g 用同一 CVE 构造过
//   expG 无限循环样本；本条是独立的最小重构（不同的循环骨架）。
// notes: 危险步骤——进程会挂起；检测器以超时→miss 处理（真实盲区案例）。
#include <cstdio>
#include <cstdint>

// Simplified Tonelli-Shanks skeleton: for non-prime modulus `p` the loop below
// never reaches q == 1, because the order assumptions do not hold.
uint64_t bn_mod_sqrt_looping(uint64_t a, uint64_t p) {
    if (a == 0) return 0;
    // find q, s with p-1 = q * 2^s
    uint64_t q = p - 1;
    int s = 0;
    while (((q & 1u) == 0) && q != 0) { q >>= 1; ++s; }
    if (s == 0) return (a % p); // p ≡ 3 mod 4 special case

    // find a quadratic non-residue z (no bound check when p is not prime)
    uint64_t z = 2;
    while (true) { // <-- for composite p this search itself may never terminate
        uint64_t e = (p - 1) / 2;
        uint64_t r = 1, b = z;
        while (e) {
            if (e & 1u) r = (r * b) % p;
            b = (b * b) % p;
            e >>= 1;
        }
        if (r == p - 1) break;
        ++z;
        if (z == p) { // dead end for composite p: restart forever (the real bug path)
            z = 2;
        }
    }
    // main loop (as in the real implementation; exits only under prime-modulus math)
    uint64_t c = z, r = a, t = a, m = s;
    while (t != 1) {
        uint64_t i = 1, t2 = (t * t) % p;
        while (t2 != 1) { t2 = (t2 * t2) % p; ++i; if (i == m) { /* keep looping */ break; } }
        uint64_t b = c;
        for (uint64_t j = 0; j + i < m; ++j) b = (b * b) % p;
        r = (r * b) % p; c = (b * b) % p; t = (t * c) % p; m = i;
    }
    return r;
}

int main() {
    std::printf("sqrt mod (composite modulus, attacker-supplied)\n");
    // p = 15 is composite -> the loop structure above does not terminate.
    uint64_t r = bn_mod_sqrt_looping(9, 15);
    std::printf("unreachable for crafted input: %llu\n", (unsigned long long)r);
    return 0;
}
