// sample_G060
// defect_type: pointer_overflow
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2016-9840 (https://nvd.nist.gov/vuln/detail/CVE-2016-9840) [zlib]
// (authoritative annotation in sample_G060.json)
#include <cstdio>
#include <cstdint>
// CVE-2016-9840: inftrees.c 码表填充指针算术不当 → 指针越界回绕
struct Code {
    unsigned short op;    // 操作/长度位
    unsigned short val;   // 值
};

static unsigned inflate_table_build(const unsigned char* lengths, int n, Code* table, int table_cap) {
    Code* here = table;
    Code* end = table + table_cap;
    for (int i = 0; i < n; ++i) {
        if (!lengths[i]) continue;
        /* DEFECT */ // 原始缺陷: 码长非法分布时 here 推进越过表尾而不停止
        here += (1 << (15 - lengths[i]));
        if (here > end) {
            // crafted 分布: 持续推进直到指针算术回绕(未定义行为)
            here += (1 << 15);
        }
        *here = Code{ (unsigned short)lengths[i], (unsigned short)i };
    }
    return (unsigned)(here - table);
}

int main() {
    Code table[16];
    // crafted 码长: 全部为 15 位码 → 每码推进 1, 随后非法再推进 2^15 → 回绕
    unsigned char lengths[32];
    for (int i = 0; i < 32; ++i) lengths[i] = 15;
    std::printf("table used=%u\n", inflate_table_build(lengths, 32, table, 16));
    return 0;
}
