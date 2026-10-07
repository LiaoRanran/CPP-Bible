// RW-032 | CVE-2017-9047 | libxml2 | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2017-9047
// project_url: https://gitlab.gnome.org/GNOME/libxml2
// year: 2017 | severity: HIGH | source_type: cve
// mechanism: xmlSnprintfElementContent 的递归拼接在复合内容模型上超过 5000 字节
//   栈缓冲，直接 sprintf 造成栈缓冲区溢出。
// notes: 最小重构。ASan 应报 stack-buffer-overflow write。
#include <cstdio>
#include <cstring>

// BUG: recursive dump appends into a FIXED stack buffer with unbounded sprintf.
void dump_content_model(const char** parts, int n, char* buf5000, size_t* used) {
    for (int i = 0; i < n; ++i) {
        int wrote = std::sprintf(buf5000 + *used, "(%s,", parts[i]); // no bound check
        *used += static_cast<size_t>(wrote);
    }
    int wrote = std::sprintf(buf5000 + *used, ")");
    *used += static_cast<size_t>(wrote);
}

int main() {
    // attacker-supplied DTD with huge element-content model
    static char bigs[64][120];
    const char* parts[64];
    for (int i = 0; i < 64; ++i) {
        std::memset(bigs[i], 'a' + (i % 26), 119);
        bigs[i][119] = '\0';
        parts[i] = bigs[i];
    }
    char stack_buf[5000];
    size_t used = 0;
    dump_content_model(parts, 64, stack_buf, &used);   // ~64*120 = 7680 > 5000
    std::printf("dumped %zu bytes into a 5000-byte stack buffer\n", used);
    return 0;
}
