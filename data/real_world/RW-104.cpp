// RW-104 | CVE-2021-22898 | curl | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-22898
// project_url: https://curl.se/
// year: 2021 | severity: MEDIUM | source_type: cve
// mechanism: TELNET 选项协商（IAC 序列）处理栈缓冲区溢出。
// notes: 最小重构。ASan 应报栈越界写。
#include <cstdio>
#include <cstring>

#define IAC 255
#define SB 250
#define SE 240

// BUG: sub-negotiation payload accumulates into a fixed 64-byte stack buffer
// without bounds check on long crafted IAC SB ... SE sequences.
int telnet_neg_writer(const unsigned char* seq, size_t n) {
    unsigned char optbuf[64];
    size_t used = 0;
    for (size_t i = 0; i < n; ++i) {
        if (seq[i] == IAC && i + 1 < n && seq[i + 1] == SB) {
            i += 2;
            while (i < n && seq[i] != SE) {
                optbuf[used++] = seq[i++];       // no bound check
            }
        }
    }
    return (int)used;
}

int main() {
    unsigned char seq[128];
    seq[0] = IAC; seq[1] = SB;
    for (int i = 2; i < 126; ++i) seq[i] = 0x41;
    seq[126] = SE; seq[127] = 0x00;
    int n = telnet_neg_writer(seq, 128);         // 124 bytes into a 64-byte buffer
    std::printf("wrote %d option bytes\n", n);
    return 0;
}
