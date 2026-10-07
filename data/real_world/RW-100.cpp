// RW-100 | CVE-2018-1000005 | curl | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2018-1000005
// project_url: https://curl.se/
// year: 2018 | severity: MEDIUM | source_type: cve
// mechanism: FTP URL 路径（含通配符）处理堆越界读 —— 路径分段解析越界。
// notes: 最小重构。ASan 应报 heap-buffer-overflow read。
#include <cstdio>
#include <cstring>
#include <string>

// BUG: the parser looks *ahead* for the next '/' via pointer arithmetic that
// misses the end-of-string case for paths ending in ';type='.
size_t ftp_path_parse(const char* url_path) {
    const char* p = url_path;
    size_t segs = 0;
    while (*p) {
        const char* next = std::strchr(p, '/');
        if (next == nullptr) {
            // crafted "dir;type=i" suffix: this lookup runs past the NUL
            next = std::strchr(p + 1, ';');          // misses when ';' absent -> OOB walk
            size_t dummy = std::strlen(next);        // reads from far region
            (void)dummy;
            break;
        }
        p = next + 1;
        ++segs;
    }
    return segs;
}

int main() {
    const char* url_path = "a/b/c/d/e/f";            // no ';' anywhere
    size_t segs = ftp_path_parse(url_path);
    std::printf("parsed %zu segments\n", segs);
    return 0;
}
