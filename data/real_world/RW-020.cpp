// RW-020 | CVE-2017-1000257 | curl | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2017-1000257
// project_url: https://curl.se/
// year: 2017 | severity: HIGH | source_type: cve
// mechanism: FTP 通配符（glob）响应解析时，服务端返回的超长文件名被拷贝进
//   固定长度缓冲，堆越界写（恶意 FTP 服务器可控）。
// notes: 最小重构。ASan 应报 heap-buffer-overflow write。
#include <cstdio>
#include <cstring>
#include <vector>

// BUG: copies the *whole* server-provided filename into a fixed 256-byte slot.
std::vector<char> parse_ftp_list_entry(const char* line) {
    std::vector<char> entry(256);
    const char* name = std::strrchr(line, ' ');
    if (!name) name = line; else ++name;
    std::strcpy(entry.data(), name);   // long filename -> heap overflow
    return entry;
}

int main() {
    // crafted LIST response with a 300-byte filename from the server
    std::vector<char> line(400, 'n');
    line[0] = '-';
    line[1] = 'r';
    for (size_t i = 2; i < 60; ++i) line[i] = ' '; // padding before name
    line[60] = 'x';
    line.push_back('\0');
    std::vector<char> e = parse_ftp_list_entry(line.data());
    std::printf("entry: %.16s...\n", e.data());
    return 0;
}
