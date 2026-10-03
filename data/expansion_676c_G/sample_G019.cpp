// sample_G019
// defect_type: infinite_loop
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// source: CVE-2022-0778 (https://nvd.nist.gov/vuln/detail/CVE-2022-0778) [openssl]
// (authoritative annotation in sample_G019.json)
#include <cstdio>
// CVE-2022-0778: BN_mod_sqrt 对非素数模数死循环（DoS）
static unsigned int bn_mod_sqrt(unsigned int a, unsigned int p) {
    unsigned int y = a % p;
    // Tonelli-Shanks 风格迭代骨架; 原始缺陷: 非素数 p 下退出条件永不满足
    for (;;) {
        if (y == 1) return 0;           // 正常退出路径(素数 p 可达)
        /* DEFECT */ y = (y * y) % p;   // p=15, a=3: 3→9→6→6→6→... 永不等于 1
    }
}

int main() {
    // crafted 证书中的非素数模数
    std::printf("sqrt=%u\n", bn_mod_sqrt(3, 15));   // 永不返回 → DoS
    return 0;
}
