// RW-011 | CVE-2015-7547 | glibc | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2015-7547
// project_url: https://www.gnu.org/software/libc/
// year: 2016 | severity: CRITICAL | source_type: cve
// mechanism: getaddrinfo 处理畸形 DNS 应答时，alloca 分配的栈缓冲长度计算错误，
//   多段应答拼接时栈缓冲区溢出（远程代码执行面）。
// notes: 最小重构（用户态模拟 DNS 应答重组）。ASan 应报 stack-buffer-overflow。
#include <cstdint>
#include <cstdio>
#include <cstring>

struct DnsResponse {
    const char* first_chunk;   // e.g. 2048 bytes
    size_t first_len;
    const char* second_chunk;  // attacker continuation
    size_t second_len;
};

// BUG: buffer sized on the *first* chunk only, then both chunks are copied in.
size_t reassemble_answers(const DnsResponse& rsp, char* out) {
    std::memcpy(out, rsp.first_chunk, rsp.first_len);
    std::memcpy(out + rsp.first_len, rsp.second_chunk, rsp.second_len); // overflow
    return rsp.first_len + rsp.second_len;
}

int main() {
    static char big_first[2048];
    std::memset(big_first, 'A', sizeof(big_first));
    static char extra[64];
    std::memset(extra, 'B', sizeof(extra));

    DnsResponse rsp{big_first, sizeof(big_first), extra, sizeof(extra)};
    char stack_buf[2048]; // sized for first chunk only
    size_t n = reassemble_answers(rsp, stack_buf);
    std::printf("reassembled %zu bytes\n", n);
    return 0;
}
