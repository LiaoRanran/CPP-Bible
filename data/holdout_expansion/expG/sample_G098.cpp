// sample_G098
// defect_type: logic_error
// severity: medium
// planted: false
// expected_verdict: miss
// expected_detectors: ubsan
// source: open-source-parsers/jsoncpp#1545 (https://github.com/open-source-parsers/jsoncpp/issues/1545) [jsoncpp]
// (authoritative annotation in sample_G098.json)
#include <cstdio>
#include <cstdint>
#include <stdexcept>
// jsoncpp#1545: uint64 解析经 double 往返 → [2^64, 2^64+2^11] 静默归 0
static uint64_t value_as_uint64(const char* digits) {
    /* DEFECT */ // 原始缺陷: 值先转 double, 大整数精度丢失后再转回 uint64
    double d = 0.0;
    for (const char* p = digits; *p; ++p)
        d = d * 10.0 + (*p - '0');
    if (d > 1.8446744073709552e19 + 2048.0)     // 超过 2^64+2^11 才报错(issue 描述的边界)
        throw std::runtime_error("double out of UInt64 range");
    return (uint64_t)d;                          // 2^64+1 → double 舍入为 2^64 → 截断为 0
}

int main() {
    try {
        // issue 中的确切输入: 18446744073709551616 = 2^64 (max+1) → 期望报错, 实际返回 0
        uint64_t v = value_as_uint64("18446744073709551616");
        std::printf("parsed=%llu (期望: 抛异常, 实际: %llu)\n",
                    (unsigned long long)v, (unsigned long long)v);
    } catch (const std::exception& e) {
        std::printf("exception: %s\n", e.what());
    }
    return 0;
}
