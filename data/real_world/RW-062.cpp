// RW-062 | CVE-2019-13750 | SQLite（Chromium 内置） | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2019-13750
// project_url: https://sqlite.org/
// year: 2019 | severity: MEDIUM | source_type: cve
// mechanism: FTS3/4 分词器处理畸形 MATCH 查询段时片段边界校验缺失（越界读）。
// notes: 最小重构。ASan 应报 heap-buffer-overflow read。
#include <cstdio>
#include <cstring>
#include <vector>

// BUG: the phrase parser assumes the query ends with a NUL; crafted FTS MATCH
// input with embedded '"' runs the scan past the buffer end.
int fts3_phrase_scan(const char* q, size_t qlen) {
    int phrases = 0;
    size_t i = 0;
    while (q[i] != '\0') {                    // bound uses NUL, not qlen
        if (q[i] == '"') {
            ++phrases;
            ++i;
            while (i < qlen + 8 && q[i] != '"') ++i;   // may pass qlen -> OOB read
        } else {
            ++i;
        }
    }
    return phrases;
}

int main() {
    // crafted MATCH input: unterminated quoted phrase at buffer end
    std::vector<char> q(16, 'a');
    q[0] = '"';
    // no closing quote, no NUL inside the viewed window
    int n = fts3_phrase_scan(q.data(), q.size());
    std::printf("phrases = %d\n", n);
    return 0;
}
