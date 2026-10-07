// RW-093 | CVE-2022-1271 | XZ Utils | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2022-1271
// project_url: https://tukaani.org/xz/
// year: 2022 | severity: HIGH | source_type: cve
// mechanism: xzgrep/zgrep 脚本类工具中文件名处理缺陷（多项命令任意文件写）；
//   C 库侧的对应形态：文件名缓冲在拼接多个目标时越界。
// notes: 最小重构（工具链文件名拼接路径）。
#include <cstdio>
#include <cstring>

// BUG: builds "target:file" chains in a fixed C-string buffer with strcat.
void build_multi_target(char* buf, size_t cap, const char* targets, const char* file) {
    size_t len = std::strlen(buf);
    std::strcat(buf, targets);          // no length accounting per component
    buf[len + std::strlen(targets)] = ':';
    std::strcat(buf, file);             // keeps appending past `cap`
    (void)cap;
}

int main() {
    char pathbuf[32] = "/tmp/" "";      // small stack buffer
    // crafted: many ':' separated targets from attacker-controlled argv
    const char* targets =
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
    build_multi_target(pathbuf, sizeof(pathbuf), targets, "w/x/y");
    std::printf("built target string (%zu chars)\n", std::strlen(pathbuf));
    return 0;
}
