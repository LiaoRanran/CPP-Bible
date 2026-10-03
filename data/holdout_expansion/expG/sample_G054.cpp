// sample_G054
// defect_type: integer_overflow
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: ubsan
// source: CVE-2022-35737 (https://nvd.nist.gov/vuln/detail/CVE-2022-35737) [sqlite]
// (authoritative annotation in sample_G054.json)
#include <cstdio>
// CVE-2022-35737: 超长字符串参数 → 长度 int 累加溢出
struct SqliteStr {
    char* z;
    int   nUsed;
    int   nAlloc;
};

static void str_append(SqliteStr* s, int n) {
    /* DEFECT */ s->nUsed += n;   // 原始缺陷: 巨大 n 时 int 溢出, 后续按 nUsed 索引越界
}

int main() {
    SqliteStr s{ 0, 2147483000, 2147483647 };
    volatile int n = 1000000;      // crafted: 巨大字符串追加
    str_append(&s, n);
    std::printf("nUsed=%d (应为 %lld)\n", s.nUsed, (long long)s.nUsed);
    return 0;
}
