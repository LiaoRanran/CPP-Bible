// RW-088 | CVE-2021-3490 | Linux kernel | defect_type: integer_overflow
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-3490
// project_url: https://www.kernel.org/
// year: 2021 | severity: HIGH | source_type: pwn
// mechanism: eBPF ALU32 边界跟踪缺陷 —— 32 位操作后 verifier 的 umin/umax
//   与运行时真值不一致，构造越界访问（Manfred Paul Pwn2Own 2021 链的一环）。
// notes: 最小重构 —— **用户态复刻**边界跟踪表。
#include <cstdint>
#include <cstdio>

struct RegBounds {
    uint64_t umin, umax;    // verifier's tracked bounds
};

// BUG: AND with 32-bit mask updates the tracked bounds as if 64-bit; runtime
// value ends up outside the tracked [umin, umax] range.
RegBounds track_alu32_and(RegBounds b, uint32_t mask) {
    b.umin &= mask;          // tracked as 64-bit AND
    b.umax &= mask;
    return b;
}

uint64_t runtime_alu32_and(uint64_t v, uint32_t mask) {
    uint32_t lo = (uint32_t)v;      // ALU32 operates on low 32 bits
    lo &= mask;
    return lo;                      // zero-extended result
}

int main() {
    RegBounds b{0, 0xFFFFFFFFull};
    b = track_alu32_and(b, 0x7FFFFFFF);      // tracked umax = 0x7FFFFFFF
    uint64_t real = runtime_alu32_and(0xFFFFFFFFull, 0x7FFFFFFF); // = 0x7FFFFFFF
    uint64_t crafted = runtime_alu32_and(0x80000000ull | 0x7FFFFFFFull, 0x7FFFFFFF);
    std::printf("tracked umax=0x%llX real=%llu crafted=%llu outside=%s\n",
                (unsigned long long)b.umax, (unsigned long long)real,
                (unsigned long long)crafted,
                crafted > b.umax ? "YES (exploit primitive)" : "no");
    return 0;
}
