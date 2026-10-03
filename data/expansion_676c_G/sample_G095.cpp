// sample_G095
// defect_type: logic_error
// severity: medium
// planted: false
// expected_verdict: miss
// expected_detectors: ubsan
// source: leethomason/tinyxml2#728 (https://github.com/leethomason/tinyxml2/issues/728) [tinyxml2]
// (authoritative annotation in sample_G095.json)
#include <cstdio>
#include <cstdlib>
// tinyxml2#728: QueryUnsignedAttribute 溢出静默截断
static bool query_unsigned_attribute(const char* value, unsigned* out) {
    char* end = 0;
    /* DEFECT */ // 原始缺陷: strtoul 之后直接截断为 unsigned, 无范围检查
    unsigned long v = std::strtoul(value, &end, 10);
    if (end == value) return false;      // 只检查"不是数字"
    *out = (unsigned)v;                  // 10000000000 → 1410065408 (静默截断)
    return true;
}

int main() {
    // issue 中的确切输入: 10 000 000 000 (hex 0x2_540B_E400)
    unsigned parsed = 0;
    bool ok = query_unsigned_attribute("10000000000", &parsed);
    std::printf("ok=%d parsed=%u (期望: 报错或 4294967295, 实际: 1410065408)\n",
                (int)ok, parsed);
    return 0;
}
