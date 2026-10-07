// RW-079 | CVE-2021-3156 | sudo | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-3156
// project_url: https://www.sudo.ws/
// year: 2021 | severity: HIGH | source_type: cve
// mechanism: Baron Samedit —— sudo -s 模式下 argv 解析：反斜杠转义把结尾 NUL
//   改写后，解析例程访问 argv[argc+1]（越界读/写，本地提权）。
// notes: 最小重构 —— **用户态复刻**参数解析（不执行 sudo 逻辑）。
#include <cstdio>
#include <cstring>

// BUG: when the final argument ends with '\', the escape logic rewrites the
// string and the parser then reads argv[argc + 1] (off-by-one past the vector).
int parse_args_user_mode(char** argv, int argc) {
    int hits = 0;
    for (int i = 0; i < argc; ++i) {
        size_t len = std::strlen(argv[i]);
        if (len && argv[i][len - 1] == '\\') {
            argv[i][len - 1] = '\0';           // rewrite trailing escape
            // parser continues one slot too far:
            const char* extra = argv[argc + 1]; // OOB read of the argv vector
            hits += (extra != nullptr) ? (int)std::strlen(extra) : 0;
        }
    }
    return hits;
}

int main() {
    char a0[] = "sudo";
    char a1[] = "-s";
    char a2[] = "user\\";                       // crafted trailing backslash
    char* argv[4] = {a0, a1, a2, nullptr};      // argv[3] = NULL terminator
    // parse_args_user_mode reads argv[4] -> one past the array
    int h = parse_args_user_mode(argv, 3);
    std::printf("parse hits = %d\n", h);
    return 0;
}
