// RW-015 | CVE-2023-6246 | glibc | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2023-6246
// project_url: https://www.gnu.org/software/libc/
// year: 2024 | severity: HIGH | source_type: cve
// mechanism: __vsyslog_internal 中消息长度计算与实际写入不一致，超长程序名/消息
//   触发堆缓冲区溢出（本地提权面）。
// notes: 最小重构。ASan 应报 heap-buffer-overflow write。
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>

// BUG: buffer sized from `msg_len` but the prefix (ident) + separator is not
// accounted for; a long `ident` overflows the heap allocation.
char* format_syslog_line(const char* ident, const char* msg, size_t msg_len) {
    size_t ident_len = std::strlen(ident);
    char* line = static_cast<char*>(std::malloc(msg_len + 1)); // misses ident_len
    std::memcpy(line, ident, ident_len);                       // heap overflow
    line[ident_len] = ':';
    std::memcpy(line + ident_len + 1, msg, msg_len);           // and again here
    line[ident_len + 1 + msg_len] = '\0';
    return line;
}

int main() {
    const char* ident = "very-long-program-name-from-attacker-setuid-binary"; // 56 bytes
    const char* msg = "log message";
    char* line = format_syslog_line(ident, msg, std::strlen(msg));
    std::printf("line = %.80s\n", line);
    std::free(line);
    return 0;
}
