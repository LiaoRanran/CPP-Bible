// sample_G050
// defect_type: stack_overflow_write
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2015-3416 (https://nvd.nist.gov/vuln/detail/CVE-2015-3416) [sqlite]
// (authoritative annotation in sample_G050.json)
#include <cstdio>
#include <cstring>
// CVE-2015-3416: VXPrintf 浮点转换 width 未截断 → 栈缓冲溢出
static void vxprintf_float(char* buf, double v, int width) {
    char digits[64];
    int n = std::snprintf(digits, sizeof(digits), "%.3f", v);
    int i = 0;
    /* DEFECT */ // 原始缺陷: width 未按 buf 容量截断
    for (; i < width; ++i)
        buf[i] = (i < n) ? digits[i] : ' ';
    buf[i] = '\0';
}

int main() {
    // crafted SQL: SELECT printf('%.200f', 3.14159) — width=200 远超输出缓冲 100
    char buf[100];
    vxprintf_float(buf, 3.14159, 200);
    std::printf("printf result=%.20s...\n", buf);
    return 0;
}
