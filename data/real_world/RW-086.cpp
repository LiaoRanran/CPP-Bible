// RW-086 | CVE-2017-16995 | Linux kernel | defect_type: integer_overflow
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2017-16995
// project_url: https://www.kernel.org/
// year: 2017 | severity: HIGH | source_type: pwn
// mechanism: eBPF 验证器 check_alu_op 符号扩展缺陷 —— 32 位立即数经
//   ALU 操作后被按 64 位无符号解释，可构造任意读写（著名 CTF 提权原型）。
// notes: 最小重构 —— **用户态复刻**验证器的符号扩展判定（不加载 eBPF）。
#include <cstdio>
#include <cstdint>

// BUG: verifier tracks `reg` as signed 32-bit but execution uses the full
// 64-bit unsigned value; crafted imm makes bounds checks pass while the real
// offset is huge.
bool verifier_check(int32_t reg_before, int32_t imm, int32_t off) {
    int32_t sum = reg_before + imm;              // signed analysis
    bool in_bounds = (sum >= 0 && sum <= 512);   // "verifier approved"
    return in_bounds;
}

int main() {
    // crafted: reg=-1, imm=1 -> sum=0 (passes) but executed as u64 math:
    // (-1 as u64) + 1 = 0 -> ok; the classic abuse uses imm that wraps to a
    // SMALL negative sum while the runtime value is HUGE (e.g. map ptr + off)
    int32_t reg = 0x7FFFFFFF;      // large positive tracked
    int32_t imm = 1;               // +1 overflows the tracked value
    bool ok = verifier_check(reg, imm, 0);       // overflowed sum fails here...
    int64_t runtime_val = (int64_t)(uint64_t)(uint32_t)reg + imm; // ...but exec wraps
    std::printf("verifier ok=%d, runtime value=%lld (mismatch = exploit primitive)\n",
                (int)ok, (long long)runtime_val);
    return 0;
}
