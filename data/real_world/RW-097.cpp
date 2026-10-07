// RW-097 | CVE-2021-3999 | glibc | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-3999
// project_url: https://www.gnu.org/software/libc/
// year: 2022 | severity: MEDIUM | source_type: cve
// mechanism: getcwd 在缓冲区恰好与路径等长时 off-by-one 单字节下溢写。
// notes: 最小重构。ASan 应报 buffer-underflow/overflow（1 byte）。
#include <cstdio>
#include <cstring>

// BUG: writes the NUL terminator one byte BEFORE the buffer start when the
// path exactly fills the buffer (the classic -1 index).
size_t getcwd_sim(char* buf, size_t size, const char* cwd) {
    size_t len = std::strlen(cwd);
    if (len < size) {
        std::memcpy(buf, cwd, len);
        buf[len] = '\0';
        return len;
    }
    // "exactly fits" path: copy to end then write terminator at [-1]
    std::memcpy(buf, cwd, size);
    buf[-1] = '\0';               // single-byte underflow write
    return size;
}

int main() {
    const char* cwd = "/home/user/projects/app";     // length 23
    char buf[23];                                    // exactly the path length
    size_t n = getcwd_sim(buf, sizeof(buf), cwd);
    std::printf("getcwd returned %zu\n", n);
    return 0;
}
