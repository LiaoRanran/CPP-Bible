// RW-080 | CVE-2019-18634 | sudo | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2019-18634
// project_url: https://www.sudo.ws/
// year: 2020 | severity: HIGH | source_type: cve
// mechanism: pwfeedback 启用时，tgetpass 对超长密码输入的处理栈缓冲区溢出
//   （非 tty 环境下触发）。
// notes: 最小重构 —— **用户态复刻**密码读取循环。
#include <cstdio>
#include <cstring>

#define TGP_MAX_PASS 128

// BUG: the read loop keeps writing into the fixed stack buffer when input has
// no newline (crafted non-tty stream), overflowing pass[].
int tgetpass_sim(const char* input, size_t in_len) {
    char pass[TGP_MAX_PASS];
    size_t off = 0;
    for (size_t i = 0; i < in_len; ++i) {
        char c = input[i];
        if (c == '\n') break;
        pass[off++] = c;                 // no bound check against sizeof(pass)
    }
    pass[off] = '\0';
    return (int)off;
}

int main() {
    // crafted: 300 bytes of password without newline
    char input[300];
    std::memset(input, 'p', sizeof(input));
    int n = tgetpass_sim(input, sizeof(input));
    std::printf("read %d bytes into 128-byte buffer\n", n);
    return 0;
}
