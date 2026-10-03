// sample_G058
// defect_type: division_by_zero
// severity: medium
// planted: false
// expected_verdict: catch
// expected_detectors: ubsan
// source: CVE-2018-13785 (https://nvd.nist.gov/vuln/detail/CVE-2018-13785) [libpng]
// (authoritative annotation in sample_G058.json)
#include <cstdio>
#include <cstdint>
// CVE-2018-13785: row_factor 错误计算 → 整数溢出 / 除零
static void png_check_chunk_length(unsigned int length, unsigned int height, unsigned int idat_limit) {
    // 原始 pngrutil.c 的 row_factor 公式(有符号 32 位计算)
    /* DEFECT */ int32_t hh = (int32_t)height + 7;   // 2147483644 + 7 → 有符号 32 位加法溢出(UB)
    int32_t denom = (int32_t)((hh & 0x7fffffffL) / (int32_t)height + 1L);
    unsigned int row_factor = idat_limit / (unsigned int)denom;
    // length 检查按 row_factor 分块进行
    unsigned int blocks = length / row_factor;   // 原始缺陷链: 溢出可致除零
    std::printf("chunk length check: %u blocks of %u (hh=%d)\n", blocks, row_factor, hh);
}

int main() {
    // crafted PNG: IHDR 高度 0x7FFFFFFC → height+7 有符号溢出
    png_check_chunk_length(0x7FFFFFF4u, 0x7FFFFFFCu, 0x40000000u);
    return 0;
}
