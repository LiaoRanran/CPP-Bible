// RW-078 | CVE-2021-33909 | Linux kernel | defect_type: integer_overflow
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-33909
// project_url: https://www.kernel.org/
// year: 2021 | severity: HIGH | source_type: cve
// mechanism: Sequoia —— seq_file 路径名拼接中 size_t 下溢（~2GB 深目录路径），
//   之后越界写（本地提权）。
// notes: 最小重构 —— **用户态复刻**路径长度计算（不创建真实深目录）。
#include <cstdio>
#include <cstdlib>
#include <cstring>

// BUG: path_len computed as int; a path > 2GB (via deep dir nesting) wraps
// negative, then (size_t) casts make the buffer sizing nonsense.
char* seq_path_sprintf(int path_len, const char* leaf) {
    // real shape: remaining = size - path_len - 1 with size ~ PATH_MAX-like
    size_t remaining = 4096 - (size_t)path_len;      // wraps for large path_len
    char* buf = static_cast<char*>(std::malloc(remaining ? remaining : 16));
    if (!buf) return nullptr;
    std::strcpy(buf, leaf);                          // writes past tiny buffer
    std::printf("remaining-underflow value: %zu\n", remaining);
    return buf;
}

int main() {
    // crafted: logical path length just above 2^31 (simulated by the int value)
    int path_len = -2147483000;      // wrapped large value as seen by the buggy int
    char* p = seq_path_sprintf(path_len, "/deeply/nested/leaf");
    std::free(p);
    return 0;
}
